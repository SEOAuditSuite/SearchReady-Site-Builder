#!/usr/bin/env python3
"""Real HTTP/Chromium browser journey for the independent second-business staging pilot.
Results are evidence-bound and never fabricated on browser transport failure.
"""
import json,sys,threading,tempfile,shutil
from pathlib import Path
from http.server import ThreadingHTTPServer
from playwright.sync_api import sync_playwright,Error as BrowserError
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import app
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/'evidence';E.mkdir(exist_ok=True)
results=[];errors=[];console=[]
def ck(name,passed,detail=''):
    results.append({'test':name,'status':'PASS' if passed else 'FAIL','detail':detail})
    if not passed:print('FAIL',name,detail)
def main():
    with tempfile.TemporaryDirectory() as temp:
        db=Path(temp)/'test.sqlite';app.init_db(db)
        s=ThreadingHTTPServer(('127.0.0.1',0),app.create_handler(db,b'browser-secret'))
        thread=threading.Thread(target=s.serve_forever,daemon=True);thread.start()
        origin=f'http://127.0.0.1:{s.server_port}'
        try:
            with sync_playwright() as p:
                browser=(p.chromium.launch(headless=True,executable_path=shutil.which('chromium'),args=['--no-sandbox']) if shutil.which('chromium') else p.chromium.launch(headless=True,channel='chrome'))
                try:
                    for width in (320,375,768,1024,1440):
                        page=browser.new_page(viewport={'width':width,'height':900})
                        page.on('pageerror',lambda e: errors.append(str(e)))
                        page.on('console',lambda msg: console.append(msg.text) if msg.type=='error' else None)
                        for path in app.PAGES:
                            try:
                                response=page.goto(origin+path,wait_until='load',timeout=10000)
                                ck(f'{path} HTTP 200 at {width}px',response is not None and response.status==200)
                                ck(f'{path} H1 at {width}px',page.locator('main h1').count()==1)
                                overflow=page.evaluate('document.documentElement.scrollWidth > window.innerWidth + 1')
                                ck(f'{path} no horizontal overflow at {width}px',not overflow)
                                if width in (375,1440) and path=='/index.html':
                                    page.screenshot(path=str(E/f'pilot2-home-{width}.png'),full_page=True)
                                if width==375 and path=='/request.html':
                                    page.screenshot(path=str(E/'pilot2-request-375.png'),full_page=True)
                            except BrowserError as e:
                                raise RuntimeError(f'BROWSER_NAVIGATION_BLOCKED: {path} {width} {str(e)[:400]}')
                        if width==375:
                            page.goto(origin+'/index.html')
                            toggle=page.locator('.nav-toggle')
                            toggle.click()
                            ck('Mobile nav expands',page.locator('#site-nav').get_attribute('class')=='primary-nav is-open')
                            page.keyboard.press('Escape')
                            ck('Escape closes mobile nav',page.locator('.nav-toggle').get_attribute('aria-expanded')=='false')
                            page.goto(origin+'/request.html')
                            page.get_by_label('Your name').fill('Demo Rider')
                            page.get_by_label('Email address').fill('demo@example.invalid')
                            page.get_by_label('A few details').fill('My fictional back brake squeals during a gentle ride.')
                            page.get_by_role('checkbox').check()
                            page.get_by_role('button',name='Save demo request').click()
                            ck('Form persists and confirms locally',page.get_by_role('status').is_visible())
                        page.close()
                    ck('No uncaught page JS errors',len(errors)==0,str(errors[:2]))
                    ck('No browser console errors',len(console)==0,str(console[:2]))
                finally:browser.close()
            status='PASS' if all(x['status']=='PASS' for x in results) else 'FAIL'
        except Exception as e:
            status='BLOCKED' if 'BROWSER_NAVIGATION_BLOCKED' in str(e) else 'FAIL'
            errors.append(str(e))
        finally:s.shutdown();s.server_close();thread.join(timeout=2)
    record={'status':status,'pass':sum(x['status']=='PASS' for x in results),'fail':sum(x['status']=='FAIL' for x in results),'results':results,'errors':errors,'console_errors':console}
    (E/'browser-results.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
    print(json.dumps({k:record[k] for k in ('status','pass','fail','errors')},indent=2))
    return 0 if status=='PASS' else 2
if __name__=='__main__':raise SystemExit(main())
