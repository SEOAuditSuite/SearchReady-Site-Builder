#!/usr/bin/env python3
"""Browser DOM/layout rendering without HTTP transport (not a replacement for URL navigation)."""
import base64,json,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import app
R=Path(__file__).resolve().parents[1]
E=R/'evidence';E.mkdir(exist_ok=True)
css=(R/'site/assets/site.css').read_text()
js=(R/'site/assets/site.js').read_text()
svg={p.name: 'data:image/svg+xml;base64,'+base64.b64encode(p.read_bytes()).decode() for p in (R/'site/assets').glob('*.svg')}
results=[];errs=[]
def record(n,p):results.append({'test':n,'status':'PASS' if p else 'FAIL'})
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 try:
  for w in (320,375,768,1024,1440):
   page=b.new_page(viewport={'width':w,'height':900},device_scale_factor=1)
   page.on('pageerror',lambda e:errs.append(str(e)))
   for path,(filename,key) in [(x,app.ROUTES[x]) for x in app.PAGES]:
    source=app.render(key)
    source=source.replace('<link rel="stylesheet" href="/assets/site.css">','<style>'+css+'</style>')
    source=source.replace('<script src="/assets/site.js" defer></script>','')
    for name,url in svg.items():source=source.replace('src="/assets/'+name+'"','src="'+url+'"')
    page.set_content(source,wait_until='load')
    page.add_script_tag(content=js)
    record(f'{path} H1 {w}',page.locator('main h1').count()==1)
    record(f'{path} visible body {w}',page.locator('main').is_visible())
    record(f'{path} no overflow {w}',not page.evaluate('document.documentElement.scrollWidth > window.innerWidth + 1'))
    if w==1440 and path=='/index.html':page.screenshot(path=str(E/'pilot2-home-desktop-1440.png'),full_page=True)
    if w==375 and path=='/index.html':page.screenshot(path=str(E/'pilot2-home-mobile-375.png'),full_page=True)
    if w==375 and path=='/request.html':page.screenshot(path=str(E/'pilot2-request-mobile-375.png'),full_page=True)
    if w==375:
     toggle=page.locator('.nav-toggle');toggle.click()
     record(f'{path} menu expanded',toggle.get_attribute('aria-expanded')=='true')
     page.keyboard.press('Escape')
     record(f'{path} Escape closes',toggle.get_attribute('aria-expanded')=='false')
    if w==1440 and path=='/request.html':
     record('Unfilled form triggers required validation',not page.locator('form').evaluate('(form)=>form.checkValidity()'))
   page.close()
  record('No page exceptions',len(errs)==0)
 finally:b.close()
res={'layer':'render-only (page.set_content + unchanged CSS/JS; not live HTTP browser)','pass':sum(x['status']=='PASS' for x in results),'fail':sum(x['status']=='FAIL' for x in results),'errors':errs,'results':results}
(E/'render-results.json').write_text(json.dumps(res,indent=2))
print(json.dumps({k:res[k] for k in ('layer','pass','fail','errors')},indent=2))
raise SystemExit(0 if res['fail']==0 else 1)
