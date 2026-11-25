#!/usr/bin/env python3
"""Focused render-only browser checks for changed form and focus styling.
No network navigation, no production or WCAG certification claim.
"""
from pathlib import Path
import json,sys,shutil
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT.parent.parent
sys.path.insert(0,str(ROOT))
import app
checks=[]
def ck(name,ok,detail=''):
 checks.append({'check':name,'status':'PASS' if ok else 'FAIL','detail':detail})
try:
 with sync_playwright() as p:
  b=p.chromium.launch(headless=True,**({'executable_path':shutil.which('chromium')} if shutil.which('chromium') else {'channel':'chrome'}),args=['--no-sandbox'])
  try:
   for w in (320,375):
    page=b.new_page(viewport={'width':w,'height':900})
    html=app.render('request','a'*64,values={'full_name':'A','email':'bad','message':'short'},error='Please review the highlighted fields.',errors={'full_name':'Enter a name between 2 and 80 characters.','email':'Enter a valid email address.','message':'Enter 12 to 1,000 characters describing the issue.','ack':'Confirm that you understand this is a demo.'})
    page.set_content(html)
    page.add_style_tag(content=(ROOT/'site/assets/site.css').read_text())
    page.add_script_tag(path=str(ROOT/'site/assets/site.js'))
    focused=page.evaluate("document.activeElement?.hasAttribute('data-form-message')")
    ck(f'D3 error summary gets keyboard focus at {w}',focused,'browser focus state')
    ck(f'D3 error summary links to invalid field at {w}',page.locator('[data-form-message] a[href="#full_name"]').count()==1,'summary link')
    ck(f'D2 field border styling at {w}',page.locator('#full_name').evaluate('(n) => getComputedStyle(n).borderTopWidth')=='2px','invalid field outline')
    page.close()
   page=b.new_page(viewport={'width':375,'height':900})
   page.set_content((SKILL/'pilot/site/index.html').read_text())
   page.add_style_tag(content=(SKILL/'pilot/site/assets/site.css').read_text())
   link=page.locator('main a').first
   link.focus()
   outline=link.evaluate('(n) => getComputedStyle(n).outlineColor')
   ck('D5 Pilot01 focus ring applied in browser',outline=='rgb(42, 99, 91)',outline)
   for sel in ('.cta-band a', '.footer a'):
    element=page.locator(sel).first
    element.focus()
    got=element.evaluate('(n) => getComputedStyle(n).outlineColor')
    ck(f'D5 Pilot01 dark {sel} light focus ring',got=='rgb(255, 247, 230)',got)
   page.close()
   page=b.new_page(viewport={'width':375,'height':900})
   page.set_content((ROOT/'site/index.html').read_text())
   page.add_style_tag(content=(ROOT/'site/assets/site.css').read_text())
   element=page.locator('.closing a').first
   element.focus()
   got=element.evaluate('(n) => getComputedStyle(n).outlineColor')
   ck('D5 Pilot02 dark closing light focus ring',got=='rgb(255, 247, 230)',got)
   page.close()
  finally:b.close()
except Exception as e:
 checks.append({'check':'browser render availability','status':'BLOCKED','detail':type(e).__name__+': '+str(e)[:180]})
status={name:sum(v['status']==name for v in checks) for name in ['PASS','FAIL','BLOCKED']}
out=ROOT/'evidence/review-focus-results.json'
out.write_text(json.dumps({'scope':'targeted browser render of remediated states; no URL navigation','counts':status,'results':checks},indent=2)+'\n')
print(status)
for c in checks:print(c)
raise SystemExit(1 if status['FAIL'] else 0)
