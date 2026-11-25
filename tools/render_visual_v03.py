from pathlib import Path
from playwright.sync_api import sync_playwright
import re,base64,shutil,os,tempfile
root=Path(__file__).resolve().parents[1]
out=Path(os.environ.get('SEARCHREADY_REVIEW_OUTPUT',str(Path(tempfile.gettempdir())/'searchready-v03-visual-review')));out.mkdir(parents=True,exist_ok=True)
if out.resolve().is_relative_to(root.resolve()): raise SystemExit('Review evidence must be written outside the source tree')
def page_assets(site,page):
 html=(site/page).read_text()
 css=(site/'assets/site.css').read_text()
 js=(site/'assets/site.js').read_text()
 for p in (site/'assets').glob('*.svg'):
  encoded=base64.b64encode(p.read_bytes()).decode()
  html=html.replace(f'"/assets/{p.name}"',f'"data:image/svg+xml;base64,{encoded}"')
  html=html.replace(f'"assets/{p.name}"',f'"data:image/svg+xml;base64,{encoded}"')
 html=re.sub(r'<link[^>]+rel="stylesheet"[^>]*>', '', html)
 html=re.sub(r'<script[^>]+src="(?:/)?assets/site\.js"[^>]*></script>', '', html)
 return html,css,js
with sync_playwright() as pw:
 exe=shutil.which('chromium') or shutil.which('chromium-browser')
 b=pw.chromium.launch(headless=True,**({'executable_path':exe} if exe else {'channel':'chrome'}))
 for name,site,filename in [('Clearroom',root/'pilot/site','index.html'),('Cinderline',root/'examples/pilot-02-cinderline/site','index.html')]:
  for label,w,h in [('desktop',1440,960),('mobile',375,812)]:
   p=b.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
   html,css,js=page_assets(site,filename)
   p.set_content(html,wait_until='load')
   p.add_style_tag(content=css);p.add_script_tag(content=js)
   print(name,label,'h1',p.locator('h1').inner_text(),'h1count',p.locator('h1').count(),'overflow',p.evaluate('document.documentElement.scrollWidth - window.innerWidth'))
   p.screenshot(path=str(out/f'{name}-{label}.png'),full_page=True)
   if label=='mobile':
    toggle=p.locator('.menu-toggle' if name=='Clearroom' else '.nav-toggle')
    toggle.click();print('menu expanded:',toggle.get_attribute('aria-expanded'))
    p.keyboard.press('Escape');print('escape collapsed:',toggle.get_attribute('aria-expanded'))
   p.close()
 b.close()
