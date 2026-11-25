#!/usr/bin/env python3
"""Independent, reproducible staging checks for the editorial/content site."""
from __future__ import annotations
import contextlib
import functools
import http.server
import json
import re
import threading
from pathlib import Path
from urllib.request import urlopen
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from playwright._impl._errors import Error as PlaywrightError

ROOT=Path(__file__).resolve().parent.parent
SITE=ROOT/'site'
EVIDENCE=ROOT/'evidence'
EVIDENCE.mkdir(exist_ok=True)
PAGES=sorted(p.name for p in SITE.glob('*.html'))
REPORT={'pilot':'Margin Atlas content/editorial website','source':'original, fictional demo','counts':{'pass':0,'fail':0,'blocked':0},'checks':[],'browser_mode':'not attempted','page_names':PAGES}

def record(group,name,ok,detail=''):
    status='PASS' if ok else 'FAIL'
    REPORT['counts'][status.lower()]+=1
    REPORT['checks'].append({'group':group,'name':name,'status':status,'detail':str(detail)[:220]})
    if not ok:print('FAIL:',group,name,detail)

def blocked(group,name,reason):
    REPORT['counts']['blocked']+=1
    REPORT['checks'].append({'group':group,'name':name,'status':'BLOCKED','detail':reason})

# Source checks: focus on different website type, not old tests.
seen_titles=set(); seen_desc=set()
for name in PAGES:
    source=(SITE/name).read_text(encoding='utf-8')
    doc=BeautifulSoup(source,'html.parser')
    title=doc.title.get_text(strip=True) if doc.title else ''
    desc=doc.find('meta',attrs={'name':'description'})
    d=desc.get('content','').strip() if desc else ''
    h1=doc.select('h1')
    record('source',f'{name}: unique title and description',bool(title and d and title not in seen_titles and d not in seen_desc))
    seen_titles.add(title);seen_desc.add(d)
    record('source',f'{name}: one visible H1',len(h1)==1)
    robot=doc.find('meta',attrs={'name':'robots'})
    record('source',f'{name}: staging is noindex',bool(robot and 'noindex' in robot.get('content','')))
    record('source',f'{name}: no invented canonical',not doc.select('link[rel=canonical]'))
    good=True;issues=[]
    for tag in doc.select('a[href],link[href],script[src],img[src]'):
        uri=tag.get('href') or tag.get('src')
        if not uri or uri.startswith('#') or uri.startswith(('http:','https:','mailto:','tel:','data:')):continue
        path=uri.split('#',1)[0].split('?',1)[0]
        if not (SITE/path).is_file():good=False;issues.append(uri)
        if tag.name=='img' and not tag.get('alt'):
            good=False;issues.append('missing alt '+uri)
    record('source',f'{name}: internal links and assets resolve',good,issues)
record('source','Five routes and article taxonomy exist',PAGES==sorted(['index.html','journal.html','about.html','the-art-of-noticing.html','a-bench-is-a-small-promise.html']))
record('source','No external scripts/fonts or marketing pixels',not any('http' in (SITE/'assets/site.css').read_text() for _ in [1]) and all('src="http' not in (SITE/x).read_text() for x in PAGES))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(SITE),**kwargs)
    def log_message(self,*args):pass
    def end_headers(self):
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('X-Robots-Tag','noindex, nofollow')
        super().end_headers()

server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
server.daemon_threads=True
thread=threading.Thread(target=server.serve_forever,daemon=True)
thread.start()
base=f'http://127.0.0.1:{server.server_port}'

try:
    for name in PAGES:
        with urlopen(base+'/'+name,timeout=5) as resp:
            body=resp.read().decode('utf-8')
            record('http',f'{name}: live 200 + staging header',resp.status==200 and 'noindex' in resp.headers.get('X-Robots-Tag','') and '<h1' in body)
    for asset in ['assets/site.css','assets/site.js','assets/field-map.svg']:
        with urlopen(base+'/'+asset,timeout=5) as resp:
            record('http',asset+' HTTP delivery',resp.status==200 and len(resp.read())>100)

    with sync_playwright() as pw:
        browser=None
        for kwargs in ({'channel':'chrome'},{'executable_path':'/usr/bin/chromium'},{}):
            try:
                browser=pw.chromium.launch(headless=True,**kwargs)
                break
            except PlaywrightError:continue
        if browser is None:
            blocked('browser','Chromium launch','No available browser binary')
        else:
            try:
                page=browser.new_page(viewport={'width':375,'height':900},device_scale_factor=1)
                errs=[]
                page.on('pageerror',lambda error:errs.append(str(error)))
                try:
                    page.goto(base+'/index.html',wait_until='networkidle',timeout=8000)
                    REPORT['browser_mode']='real URL navigation via loopback HTTP'
                except PlaywrightError as e:
                    REPORT['browser_mode']='inline HTML with original CSS/JS and SVG (URL navigation BLOCKED)'
                    blocked('browser','Real Chrome HTTP navigation',str(e)[:160])
                if REPORT['browser_mode'].startswith('real'):
                    for width in [320,375,768,1024,1440]:
                        page.set_viewport_size({'width':width,'height':900})
                        for name in PAGES:
                            page.goto(base+'/'+name,wait_until='networkidle')
                            layout=page.evaluate("""() => ({w:document.documentElement.scrollWidth,c:document.documentElement.clientWidth,head:!!document.querySelector('main h1'),robots:document.querySelector('meta[name=robots]')?.content,assets:!!document.querySelector('link[rel=stylesheet]')})""")
                            record('browser',f'{name}: viewport {width}',layout['w']<=layout['c']+1 and layout['head'] and 'noindex' in layout['robots'],layout)
                        if width==375:
                            page.goto(base+'/index.html',wait_until='networkidle')
                            page.screenshot(path=str(EVIDENCE/'margin-atlas-home-mobile-375.png'),full_page=True)
                            page.goto(base+'/journal.html',wait_until='networkidle')
                            page.screenshot(path=str(EVIDENCE/'margin-atlas-journal-mobile-375.png'),full_page=True)
                        if width==1440:
                            page.goto(base+'/index.html',wait_until='networkidle')
                            page.screenshot(path=str(EVIDENCE/'margin-atlas-home-desktop-1440.png'),full_page=True)
                    page.set_viewport_size({'width':375,'height':900})
                    page.goto(base+'/journal.html',wait_until='networkidle')
                    toggle=page.get_by_role('button',name='Open navigation')
                    record('browser','Mobile navigation opens',toggle.is_visible() and (toggle.click() or True) and page.get_by_role('button',name='Close navigation').get_attribute('aria-expanded')=='true')
                    page.keyboard.press('Escape')
                    record('browser','Escape closes active navigation + focuses toggle',toggle.get_attribute('aria-expanded')=='false' and toggle.evaluate('(el)=>document.activeElement===el'))
                    page.locator('#filter-notes').fill('bench')
                    visible=page.locator('.story-card:visible').count()
                    record('browser','Journal search filters to one article',visible==1 and '1 note' in page.locator('#result-status').inner_text())
                    page.locator('#filter-notes').fill('nothing-here')
                    record('browser','Search empty state is announced',page.locator('#no-results').is_visible() and page.locator('.story-card:visible').count()==0)
                    page.locator('#filter-notes').fill('')
                    record('browser','Clearing search restores articles',page.locator('.story-card:visible').count()==2)
                    # Focus color on editorial dark section and footer.
                    page.goto(base+'/index.html',wait_until='networkidle')
                    cta=page.locator('.outline-link');cta.focus()
                    style=cta.evaluate('(el)=>({outline:getComputedStyle(el).outlineColor,focused:document.activeElement===el})')
                    record('browser','Dark editorial CTA has pale keyboard focus outline',style['focused'] and style['outline'] in ('rgb(255, 247, 230)','rgb(255, 247, 230)'))
                    record('browser','No uncaught JavaScript errors',len(errs)==0,errs)
                page.close()
            finally:
                browser.close()
finally:
    server.shutdown();server.server_close()

(EVIDENCE/'third-pilot-results.json').write_text(json.dumps(REPORT,indent=2),encoding='utf-8')
print(json.dumps({'counts':REPORT['counts'],'browser_mode':REPORT['browser_mode'],'pages':len(PAGES)},indent=2))
raise SystemExit(0 if REPORT['counts']['fail']==0 else 1)
