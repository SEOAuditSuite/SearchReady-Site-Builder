#!/usr/bin/env python3
"""Local HTTP + actual headless Chromium pilot acceptance. Requires playwright & installed browser."""
from __future__ import annotations
import shutil
import sys
import json
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.request import urlopen

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'pilot'/'site'
EVIDENCE=ROOT/'pilot'/'evidence'
PAGES=['index.html','services.html','process.html','contact.html']
VIEWPORTS=[320,375,768,1024,1440]

class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(SITE),**kwargs)
    def log_message(self,*args): pass

def main():
    EVIDENCE.mkdir(exist_ok=True)
    failures=[]; checks=0; page_errors=[]; console_errors=[]; metadata=[]
    http=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    thread=threading.Thread(target=http.serve_forever,daemon=True)
    thread.start();base=f'http://127.0.0.1:{http.server_port}'
    def check(value,desc):
        nonlocal checks
        checks+=1
        if not value: failures.append(desc)
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True,channel='chrome') if sys.platform=='win32' else p.chromium.launch(headless=True,executable_path=shutil.which('chromium') or '/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
            context=browser.new_context(accept_downloads=True,viewport={'width':1440,'height':900},device_scale_factor=1)
            for width in VIEWPORTS:
                page=context.new_page()
                page.set_viewport_size({'width':width,'height':900})
                page.on('pageerror',lambda e:page_errors.append(str(e)))
                page.on('console',lambda m:console_errors.append(m.text) if m.type=='error' else None)
                for name in PAGES:
                    response=page.goto(f'{base}/{name}',wait_until='networkidle')
                    check(response is not None and response.status==200,f'{name}@{width} HTTP 200')
                    check(page.locator('main h1').count()==1 and page.locator('main h1').first.is_visible(),f'{name}@{width} visible H1')
                    overflow=page.evaluate('document.documentElement.scrollWidth > window.innerWidth+1')
                    check(not overflow,f'{name}@{width} no horizontal overflow')
                    check(page.locator('meta[name="robots"]').get_attribute('content')=='noindex,nofollow',f'{name}@{width} staging noindex')
                    if width==1440 and name=='index.html':page.screenshot(path=str(EVIDENCE/'home-desktop-1440.png'),full_page=True)
                    if width==375 and name=='index.html':page.screenshot(path=str(EVIDENCE/'home-mobile-375.png'),full_page=True)
                    if width==375 and name=='contact.html':page.screenshot(path=str(EVIDENCE/'contact-mobile-375.png'),full_page=True)
                if width==375:
                    page.goto(f'{base}/index.html')
                    toggle=page.get_by_role('button',name='Menu')
                    check(toggle.is_visible(),'mobile menu toggle visible')
                    toggle.click()
                    check(toggle.get_attribute('aria-expanded')=='true','mobile menu opens')
                    page.keyboard.press('Escape')
                    check(toggle.get_attribute('aria-expanded')=='false','mobile menu closes on Escape')
                    toggle.click();page.get_by_role('navigation',name='Primary navigation').get_by_role('link',name='Method').click()
                    check(page.url.endswith('process.html'),'mobile menu Method navigation')
                page.close()
            response=urlopen(base+'/assets/site.css')
            check(response.status==200 and b'.hero' in response.read(),'HTTP CSS asset served')
            response=urlopen(base+'/assets/site.js')
            check(response.status==200 and b'download' in response.read(),'HTTP JS asset served')
            page=context.new_page()
            page.on('pageerror',lambda e:page_errors.append(str(e)))
            page.goto(f'{base}/contact.html')
            page.get_by_role('button',name='Download my brief').click()
            check(page.get_by_role('status').inner_text()=='' ,'invalid empty form does not show fake success')
            page.get_by_label('Your name').fill('Demo Visitor')
            page.get_by_label('Which space?').fill('Home office')
            page.get_by_label('What would you like to improve?').fill('Make storage easier to use.')
            with page.expect_download() as download_event:
                page.get_by_role('button',name='Download my brief').click()
            download=download_event.value
            check(download.suggested_filename=='clearroom-demo-brief.txt','local brief downloads correct filename')
            file_path=EVIDENCE/'brief-downloaded-during-test.txt';download.save_as(str(file_path))
            contents=file_path.read_text(encoding='utf-8')
            check('Demo Visitor' in contents and 'Nothing was transmitted' not in contents and 'No information was transmitted' in contents,'local brief content with privacy label')
            check('Nothing was sent' in page.get_by_role('status').inner_text(),'honest form feedback')
            file_path.unlink(missing_ok=True)
            page.close()
            check(not page_errors,'no uncaught JavaScript errors')
            check(not console_errors,'no console errors')
            context.close();browser.close()
            metadata=['real loopback HTTP requests','actual headless installed Chromium','responsive width checks','JS menu and download events']
    except Exception as e:
        failures.append(f'Test execution blocked or failed: {type(e).__name__}: {e}')
    finally:
        http.shutdown();thread.join(timeout=4);http.server_close()
    result={'pilot':'Clearroom fictional service website','url_tested':'http://127.0.0.1:<ephemeral-port>','pages':PAGES,'viewports':VIEWPORTS,'checks':checks,'passed':max(0,checks-len(failures)),'failed':len(failures),'errors':failures,'uncaught_page_errors':page_errors,'console_errors':console_errors,'scope':metadata,'production':'BLOCKED: fictional business, no verified domain, no live contact backend, no field CWV'}
    (EVIDENCE/'browser-results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('pages','viewports','scope')},indent=2))
    return 1 if failures else 0
if __name__=='__main__':raise SystemExit(main())
