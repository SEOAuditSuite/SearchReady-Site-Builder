#!/usr/bin/env python3
"""Pending Pilot 03 gate only: real Chrome HTTP URL navigation + interactive paths.

Does NOT rerun the original source, inline-render, or transport suites.
Run from extracted archive with Python Playwright and installed Chrome.
"""
from pathlib import Path
import json, http.server, os, threading
from playwright.sync_api import sync_playwright
from playwright._impl._errors import Error as PlaywrightError

ROOT=Path(__file__).resolve().parent.parent
SITE=ROOT/'site'
# Reviewer-generated screenshots/results must never modify the release tree or its manifests.
PACKAGE_ROOT = ROOT.parent.parent
_evidence_base = Path(os.environ.get(
    'SEARCHREADY_REVIEW_OUTPUT',
    str(PACKAGE_ROOT.parent / (PACKAGE_ROOT.name + '-review-evidence')),
)).expanduser().resolve()
if _evidence_base == PACKAGE_ROOT or PACKAGE_ROOT in _evidence_base.parents:
    raise SystemExit('SEARCHREADY_REVIEW_OUTPUT must be outside the extracted release directory')
EVIDENCE = _evidence_base / 'pilot-03-margin-atlas'
EVIDENCE.mkdir(parents=True, exist_ok=True)
PAGES=['index.html','journal.html','about.html','the-art-of-noticing.html','a-bench-is-a-small-promise.html']
checks=[]
def record(label,passed,detail=''):
 checks.append({'test':label,'status':'PASS' if passed else 'FAIL','detail':detail})
 if not passed:print('FAIL',label,detail)

class Handler(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(SITE),**kwargs)
 def log_message(self,*args): pass
 def end_headers(self):
  self.send_header('X-Content-Type-Options','nosniff')
  self.send_header('X-Robots-Tag','noindex, nofollow')
  super().end_headers()

server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}'
browser=None;errors=[];console=[];status='PASS';blocker=None
try:
 with sync_playwright() as pw:
  for options in ({'channel':'chrome'},{'executable_path':'/usr/bin/chromium'},{}):
   try:browser=pw.chromium.launch(headless=True,**options);break
   except PlaywrightError as exc:blocker=str(exc)[:300]
  if browser is None:status='BLOCKED'
  else:
   page=browser.new_page(viewport={'width':375,'height':900})
   page.on('pageerror',lambda err:errors.append(str(err)))
   page.on('console',lambda msg:console.append(msg.text) if msg.type=='error' else None)
   try:
    for width in (320,375,768,1024,1440):
     page.set_viewport_size({'width':width,'height':950})
     for name in PAGES:
      response=page.goto(base+'/'+name,wait_until='networkidle',timeout=9000)
      state=page.evaluate('''() => ({h1:document.querySelectorAll('main h1').length,sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,css:getComputedStyle(document.body).fontFamily,robots:document.querySelector('meta[name=robots]')?.content,js:document.documentElement.classList.contains('js')})''')
      record(f'{name} real Chrome HTTP @ {width}',response.status==200 and state['h1']==1 and state['sw']<=state['cw']+1 and 'noindex' in (state['robots'] or '') and state['js'],str(state))
     if width==375:
      page.goto(base+'/index.html',wait_until='networkidle')
      page.screenshot(path=str(EVIDENCE/'live-url-home-375.png'),full_page=True)
      page.goto(base+'/journal.html',wait_until='networkidle')
      page.screenshot(path=str(EVIDENCE/'live-url-journal-375.png'),full_page=True)
     if width==1440:
      page.goto(base+'/index.html',wait_until='networkidle')
      page.screenshot(path=str(EVIDENCE/'live-url-home-1440.png'),full_page=True)
    page.set_viewport_size({'width':375,'height':900})
    page.goto(base+'/journal.html',wait_until='networkidle')
    menu=page.get_by_role('button',name='Open navigation');menu.click()
    record('Nav expands with accessible name',page.get_by_role('button',name='Close navigation').get_attribute('aria-expanded')=='true')
    page.keyboard.press('Escape')
    record('Nav Escape closes and restores focus',menu.get_attribute('aria-expanded')=='false' and menu.evaluate('(el)=>document.activeElement===el'))
    q=page.locator('#filter-notes');q.fill('bench')
    record('Journal filter one match with live status',page.locator('.story-card:visible').count()==1 and '1 note' in page.locator('#result-status').inner_text())
    q.fill('not-present-anywhere')
    record('Journal search empty state',page.locator('#no-results').is_visible() and page.locator('.story-card:visible').count()==0)
    q.fill('');record('Journal search clears',page.locator('.story-card:visible').count()==2)
    record('No JS page or console errors',not errors and not console,f'page errors={errors}; console errors={console}')
   except PlaywrightError as exc:
    # This is a true failure once the browser is running and attempting URL navigation,
    # or BLOCKED when policy prevents even first navigation.
    if not checks and 'ERR_BLOCKED_BY_ADMINISTRATOR' in str(exc):status='BLOCKED';blocker=str(exc)[:300]
    else:status='FAIL';blocker=str(exc)[:300]
   finally:page.close()
  if browser:browser.close()
finally:
 server.shutdown();server.server_close()

fail=sum(x['status']=='FAIL' for x in checks)
if fail:status='FAIL'
report={'scope':'Pilot 03 pending real Chrome HTTP URL-navigation only','url_origin':'ephemeral 127.0.0.1 test server, not production hosting','status':status,'pass':sum(x['status']=='PASS' for x in checks),'fail':fail,'blocked_reason':blocker if status!='PASS' else None,'checks':checks,'page_errors':errors,'console_errors':console}
(EVIDENCE/'live-url-browser-results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print("Review evidence:", EVIDENCE)
print(f"Pilot 03 URL browser: {status}, {report['pass']} PASS, {fail} FAIL; {report['blocked_reason'] or ''}")
raise SystemExit(0 if status=='PASS' else 2 if status=='BLOCKED' else 1)
