#!/usr/bin/env python3
"""Limited browser rendering/interaction checks for third pilot when HTTP navigation is blocked."""
from pathlib import Path
import json,base64
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent.parent
SITE=ROOT/'site'; ASSETS=SITE/'assets'; OUT=ROOT/'evidence'
css=(ASSETS/'site.css').read_text(encoding='utf-8')
js=(ASSETS/'site.js').read_text(encoding='utf-8')
svg=base64.b64encode((ASSETS/'field-map.svg').read_bytes()).decode('ascii')
all_pages=sorted(x.name for x in SITE.glob('*.html'))
checks=[]
def record(name,good,data=None):
    checks.append({'name':name,'status':'PASS' if good else 'FAIL','detail':data})
    if not good:print('FAIL',name,data)

def load(page,name):
    text=(SITE/name).read_text(encoding='utf-8')
    text=text.replace('<link rel="stylesheet" href="assets/site.css">','<style>'+css+'</style>')
    text=text.replace('<script src="assets/site.js" defer></script>','')
    text=text.replace('src="assets/field-map.svg"','src="data:image/svg+xml;base64,'+svg+'"')
    text=text.replace('href="assets/mark.svg"','href="data:image/svg+xml;base64,'+base64.b64encode((ASSETS/'mark.svg').read_bytes()).decode('ascii')+'"')
    page.set_content(text,wait_until='load')
    page.add_script_tag(content=js)

def relative_luminance(rgb):
    s=[i/255 for i in rgb]
    s=[x/12.92 if x <=.04045 else ((x+.055)/1.055)**2.4 for x in s]
    return .2126*s[0]+.7152*s[1]+.0722*s[2]

def ratio(a,b):
    x,y=sorted([relative_luminance(a),relative_luminance(b)],reverse=True)
    return round((x+.05)/(y+.05),2)

with sync_playwright() as pw:
    try:
        br=pw.chromium.launch(channel='chrome',headless=True)
    except Exception:
        try:
            br=pw.chromium.launch(headless=True)
        except Exception:
            br=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True)
    page=br.new_page(viewport={'width':375,'height':1000})
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    for width in (320,375,768,1024,1440):
        page.set_viewport_size({'width':width,'height':980})
        for name in all_pages:
            load(page,name)
            state=page.evaluate('''() => ({doc:document.documentElement.scrollWidth,viewport:document.documentElement.clientWidth,h1:document.querySelectorAll('main h1').length,main:document.querySelector('main')!==null})''')
            record(f'{name}@{width} inline-render overflow/H1',state['doc']<=state['viewport']+1 and state['h1']==1 and state['main'],state)
            if width==375 and name in ('index.html','journal.html'):
                page.screenshot(path=str(OUT/('margin-atlas-'+('home' if name=='index.html' else 'journal')+'-375.png')),full_page=True)
            if width==1440 and name=='index.html':
                page.screenshot(path=str(OUT/'margin-atlas-home-1440.png'),full_page=True)
    page.set_viewport_size({'width':375,'height':900})
    load(page,'journal.html')
    btn=page.get_by_role('button',name='Open navigation')
    btn.click()
    record('Menu: open and aria-expanded true',page.get_by_role('button',name='Close navigation').get_attribute('aria-expanded')=='true')
    page.keyboard.press('Escape')
    record('Menu: Escape close and focus return',btn.get_attribute('aria-expanded')=='false' and btn.evaluate('(el)=>document.activeElement===el'))
    # Escape on closed nav should NOT steal focus from search.
    page.locator('#filter-notes').focus();page.keyboard.press('Escape')
    record('Closed menu: Escape preserves search focus',page.locator('#filter-notes').evaluate('(el)=>document.activeElement===el'))
    page.locator('#filter-notes').fill('bench')
    record('Journal search one result',page.locator('.story-card:visible').count()==1)
    page.locator('#filter-notes').fill('no-match-at-all')
    record('Journal search empty state',page.locator('#no-results').is_visible() and page.locator('.story-card:visible').count()==0)
    page.locator('#filter-notes').fill('')
    record('Journal search clear',page.locator('.story-card:visible').count()==2)
    load(page,'index.html')
    page.locator('.outline-link').focus()
    out=page.locator('.outline-link').evaluate('''e=>({color:getComputedStyle(e).outlineColor,background:getComputedStyle(e.closest('.editorial-quote')).backgroundColor,focused:document.activeElement===e})''')
    record('Dark CTA pale focus ring',out['focused'] and out['color']=='rgb(255, 247, 230)',out)
    focus_contrast=ratio((255,247,230),(25,43,53))
    record('Dark CTA contrast >=3',focus_contrast>=3,focus_contrast)
    page.locator('.footer-links a').first.focus()
    out=page.locator('.footer-links a').first.evaluate('''e=>({color:getComputedStyle(e).outlineColor,focused:document.activeElement===e})''')
    record('Dark footer pale focus ring',out['focused'] and out['color']=='rgb(255, 247, 230)',out)
    record('No uncaught JS errors',not errors,errors)
    br.close()
res={'method':'Chromium page.set_content, inline original CSS/JS and data SVG; does NOT prove HTTP URL navigation','pass':sum(x['status']=='PASS' for x in checks),'fail':sum(x['status']=='FAIL' for x in checks),'checks':checks}
(OUT/'third-pilot-render-results.json').write_text(json.dumps(res,indent=2),encoding='utf-8')
print({'pass':res['pass'],'fail':res['fail'],'method':res['method']})
raise SystemExit(0 if not res['fail'] else 1)
