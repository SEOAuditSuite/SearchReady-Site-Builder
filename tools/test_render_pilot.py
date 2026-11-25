#!/usr/bin/env python3
"""DOM rendering test with inline local assets; not equivalent to browser URL navigation."""
from pathlib import Path
import json,re,base64
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'pilot'/'site'; EVIDENCE=ROOT/'pilot'/'evidence'
PAGES=['index.html','services.html','process.html','contact.html']; WIDTHS=[320,375,768,1024,1440]
CSS=(SITE/'assets/site.css').read_text(); JS=(SITE/'assets/site.js').read_text()
def inline_doc(filename):
 s=(SITE/filename).read_text()
 s=s.replace('<link rel="stylesheet" href="assets/site.css">','<style>'+CSS+'</style>')
 s=s.replace('<script src="assets/site.js" defer></script>','<script>'+JS+'</script>')
 for name in ('mark.svg','hero-art.svg'):
  svg=(SITE/'assets'/name).read_bytes()
  data='data:image/svg+xml;base64,'+base64.b64encode(svg).decode()
  s=s.replace('assets/'+name,data)
 return s
checks=0;failures=[];js_errors=[];console_errors=[]
def check(ok,what):
 global checks
 checks+=1
 if not ok:failures.append(what)
EVIDENCE.mkdir(exist_ok=True)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 context=browser.new_context(accept_downloads=True,viewport={'width':1440,'height':900})
 for width in WIDTHS:
  for file in PAGES:
   page=context.new_page();page.set_viewport_size({'width':width,'height':900})
   page.on('pageerror',lambda err:js_errors.append(str(err)))
   page.on('console',lambda m:console_errors.append(m.text) if m.type=='error' else None)
   page.set_content(inline_doc(file),wait_until='load')
   check(page.locator('main h1').count()==1 and page.locator('main h1').first.is_visible(),f'{file}@{width}: h1')
   check(not page.evaluate('document.documentElement.scrollWidth > window.innerWidth+1'),f'{file}@{width}: overflow')
   check(page.locator('meta[name="robots"]').get_attribute('content')=='noindex,nofollow',f'{file}@{width}: noindex')
   check(page.locator('main').is_visible(),f'{file}@{width}: visible main')
   if width==1440 and file=='index.html':page.screenshot(path=str(EVIDENCE/'home-desktop-1440.png'),full_page=True)
   if width==375 and file=='index.html':
    page.screenshot(path=str(EVIDENCE/'home-mobile-375.png'),full_page=True)
    toggle=page.get_by_role('button',name='Menu');check(toggle.is_visible(),'mobile menu visible')
    toggle.click();check(toggle.get_attribute('aria-expanded')=='true','menu opens')
    page.keyboard.press('Escape');check(toggle.get_attribute('aria-expanded')=='false','Escape closes')
   if width==375 and file=='contact.html':
    page.screenshot(path=str(EVIDENCE/'contact-mobile-375.png'),full_page=True)
    page.get_by_role('button',name='Download my brief').click()
    check(page.get_by_role('status').inner_text()=='' ,'required inputs block empty form')
    page.get_by_label('Your name').fill('Demo Visitor')
    page.get_by_label('Which space?').fill('Home office')
    page.get_by_label('What would you like to improve?').fill('Simplify access to supplies.')
    with page.expect_download() as event: page.get_by_role('button',name='Download my brief').click()
    check(event.value.suggested_filename=='clearroom-demo-brief.txt','download generated')
    check('Nothing was sent' in page.get_by_role('status').inner_text(),'honest feedback')
   page.close()
 check(not js_errors,'no uncaught JS')
 check(not console_errors,'no JS console errors')
 context.close();browser.close()
result={'mode':'Browser DOM rendering with inline unchanged local CSS/JS/SVG; NOT real URL navigation','pages':PAGES,'viewports':WIDTHS,'checks':checks,'failed':len(failures),'passed':checks-len(failures),'failures':failures,'js_errors':js_errors,'console_errors':console_errors,'http_navigation':'BLOCKED in execution environment by ERR_BLOCKED_BY_ADMINISTRATOR'}
(EVIDENCE/'render-results.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k not in ('pages','viewports','failures','js_errors','console_errors')},indent=2))
if failures: print('FAILURES',failures)
raise SystemExit(bool(failures))
