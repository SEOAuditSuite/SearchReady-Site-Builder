#!/usr/bin/env python3
"""Run ONLY changed Pilot 03 editorial content/semantics/readability checks.

Produces distinct evidence; historical 35+35 pilot suites are not repeated.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import tempfile, subprocess, shutil, json, re, base64
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parents[1]
site=root/'site'; evidence=root/'evidence'; evidence.mkdir(exist_ok=True)
checks=[]
def ck(name, condition, detail=''):
 checks.append({'check':name,'status':'PASS' if condition else 'FAIL','detail':detail})
 if not condition: print('FAIL',name,detail)

pages={f.name:BeautifulSoup(f.read_text(encoding='utf-8'),'html.parser') for f in site.glob('*.html')}
for f in ('the-art-of-noticing.html','a-bench-is-a-small-promise.html'):
 word_count=len(pages[f].select_one('article.article-body').get_text(' ',strip=True).split())
 labels=[t.get_text(strip=True) for t in pages[f].select('.article-type span')]
 ck(f+' honest reading time', 175<=word_count<=450 and labels[-1]=='2 MIN READ',f'{word_count} words; label {labels[-1]}')

doc=pages['journal.html']
headings=[t.name for t in doc.select('main h1,main h2,main h3')]
ck('Journal H1-H2-H3 landmark hierarchy',headings==['h1','h2','h3','h3'],str(headings))
ck('Journal section H2 is accessible not visually decorative',doc.select_one('h2.sr-only').get_text(strip=True)=='Journal articles')
ck('Journal cards have truthful reading times', [x.get_text(strip=True) for x in doc.select('.story-topline span:last-child')]==['2 MIN READ','2 MIN READ'])

# Source generator must reproduce the checked production HTML and local code exactly.
with tempfile.TemporaryDirectory(prefix='margin-atlas-build-parity-') as temp:
 p=Path(temp);shutil.copy2(root/'build.py',p/'build.py')
 subprocess.run(['python',str(p/'build.py')],cwd=str(p),check=True,capture_output=True,text=True)
 expected={str(x.relative_to(site)):x.read_bytes() for x in site.rglob('*') if x.is_file()}
 got={str(x.relative_to(p/'site')):x.read_bytes() for x in (p/'site').rglob('*') if x.is_file()}
 wrong=[name for name in sorted(set(expected)|set(got)) if expected.get(name)!=got.get(name)]
 ck('Generator-byte parity for five HTML pages and linked assets',not wrong,f'{len(expected)} files compared; mismatch={wrong}')

css=(site/'assets/site.css').read_text(encoding='utf-8')
js=(site/'assets/site.js').read_text(encoding='utf-8')
svg=base64.b64encode((site/'assets/field-map.svg').read_bytes()).decode('ascii')
def content(name):
 return (site/name).read_text(encoding='utf-8').replace('<link rel="stylesheet" href="assets/site.css">','<style>'+css+'</style>').replace('<script src="assets/site.js" defer></script>','').replace('src="assets/field-map.svg"','src="data:image/svg+xml;base64,'+svg+'"')

def color_values(vals):
 def rgb(v):
  m=re.match(r'rgba?\((\d+),\s*(\d+),\s*(\d+)',v)
  return tuple(int(x) for x in m.groups()) if m else None
 def lum(c):
  vals=[v/255 for v in c]; vals=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in vals]
  return .2126*vals[0]+.7152*vals[1]+.0722*vals[2]
 a,b=map(rgb,vals);return round((max(lum(a),lum(b))+.05)/(min(lum(a),lum(b))+.05),2) if a and b else 0

with sync_playwright() as pw:
 browser=None
 for args in ({'channel':'chrome'},{'executable_path':'/usr/bin/chromium'},{}):
  try:browser=pw.chromium.launch(headless=True,**args);break
  except Exception:continue
 if browser is None:ck('Browser available for focused layout audit',False,'No installed browser; record NOT RUN in manual gate')
 else:
  pg=browser.new_page(viewport={'width':375,'height':900})
  for width in (320,375,1440):
   pg.set_viewport_size({'width':width,'height':900});pg.set_content(content('index.html'),wait_until='load');pg.add_script_tag(content=js)
   state=pg.evaluate('''() => ({width:innerWidth,doc:document.documentElement.scrollWidth,client:document.documentElement.clientWidth,artSize:parseFloat(getComputedStyle(document.querySelector('.art-bottom')).fontSize),footerSize:parseFloat(getComputedStyle(document.querySelector('.footer-bottom')).fontSize),focus:[], heroLabel:document.querySelector('.art-bottom').innerText})''')
   ck(f'Changed metadata is legible and no horizontal overflow at {width}px',state['artSize']>=11 and state['footerSize']>=11 and state['doc']<=state['client']+1,str(state))
   if width==375:
    (evidence/'editorial-postreview-home-375.png').parent.mkdir(exist_ok=True)
    pg.screenshot(path=str(evidence/'editorial-postreview-home-375.png'),full_page=True)
  # WCAG non-text focus visibility in the dark section after source change (focused check only).
  pg.set_viewport_size({'width':375,'height':900})
  pg.locator('.outline-link').focus()
  state=pg.locator('.outline-link').evaluate('''e=>({focus:document.activeElement===e,outline:getComputedStyle(e).outlineColor,bg:getComputedStyle(e.closest('.editorial-quote')).backgroundColor})''')
  ratio=color_values((state['outline'],state['bg']))
  ck('Dark editorial CTA keyboard focus has >=3:1 contrast',state['focus'] and ratio>=3,f'{state}, contrast={ratio}')
  pg.locator('.footer-links a').first.focus()
  state=pg.locator('.footer-links a').first.evaluate('''e=>({focus:document.activeElement===e,outline:getComputedStyle(e).outlineColor,bg:getComputedStyle(e.closest('.site-footer')).backgroundColor})''')
  ratio=color_values((state['outline'],state['bg']))
  ck('Dark footer keyboard focus has >=3:1 contrast',state['focus'] and ratio>=3,f'{state}, contrast={ratio}')
  browser.close()

result={'scope':'Pilot 03 editorial delta only; HTTP URL browser NOT rerun; not complete WCAG audit','pass':sum(c['status']=='PASS' for c in checks),'fail':sum(c['status']=='FAIL' for c in checks),'checks':checks}
(evidence/'editorial-delta-results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print({'pass':result['pass'],'fail':result['fail'],'scope':result['scope']})
raise SystemExit(0 if not result['fail'] else 1)
