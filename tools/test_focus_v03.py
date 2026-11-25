#!/usr/bin/env python3
"""Current D5: keyboard Tab scan of actual v0.3 HTML/CSS, including mobile menu.
Default mode serves static source over real local HTTP. --dom is an explicitly
limited offline browser fallback. Computed contrast, not a complete pixel/WCAG audit.
Evidence is always outside the release tree. No form submissions or external calls.
"""
import argparse, base64, functools, json, os, re, shutil, threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
SITES={'clearroom':(ROOT/'pilot/site',('index.html','services.html','process.html','contact.html')),
       'cinderline':(ROOT/'examples/pilot-02-cinderline/site',('index.html','tune-ups.html','repairs.html','process.html','request.html'))}
OUT=Path(os.environ.get('SEARCHREADY_REVIEW_OUTPUT',str(ROOT.parent/(ROOT.name+'-review-evidence')))).expanduser().resolve()
if OUT==ROOT or ROOT in OUT.parents: raise SystemExit('Review output must be outside release directory')
OUT=OUT/'v03-focus'; OUT.mkdir(parents=True,exist_ok=True)

def contrast(a,b):
    def lum(s):
        rgb=re.search(r'rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)',s)
        vals=[int(x)/255 for x in rgb.groups()]
        return sum((x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4)*w for x,w in zip(vals,(.2126,.7152,.0722)))
    x,y=sorted((lum(a),lum(b))); return (y+.05)/(x+.05)

OBSERVE=r'''() => {
 const e=document.activeElement,c=getComputedStyle(e);
 if(e===document.body||e===document.documentElement)return null;
 const all=[...document.querySelectorAll('a[href],button,input,select,textarea,[tabindex]')];
 let back=[],n=e.parentElement;
 while(n){const s=getComputedStyle(n);
   if(s.backgroundImage.includes('gradient'))back.push(...(s.backgroundImage.match(/rgba?\([^)]*\)/g)||[]));
   if(s.backgroundColor!=='rgba(0, 0, 0, 0)'&&s.backgroundColor!=='transparent'){back.push(s.backgroundColor);break;}n=n.parentElement;}
 if(!back.length)back=['rgb(255, 255, 255)'];
 return {id:all.indexOf(e),label:(e.getAttribute('aria-label')||e.innerText||e.name||e.id||'').trim().slice(0,100),visible:e.matches(':focus-visible'),outline:c.outlineColor,style:c.outlineStyle,width:parseFloat(c.outlineWidth),offset:parseFloat(c.outlineOffset),shadow:c.boxShadow,backgrounds:back,skip:e.matches('.skip'),footer:e.matches('.footer a'),card:e.matches('.service-cards a'),toggle:e.matches('.menu-toggle,.nav-toggle'),strip:document.querySelector('.demo-strip')?getComputedStyle(document.querySelector('.demo-strip')).backgroundColor:null,header:document.querySelector('.site-header')?getComputedStyle(document.querySelector('.site-header')).backgroundColor:null};
}'''

def load_dom(page,site,name):
    html=(site/name).read_text(encoding='utf8')
    for p in (site/'assets').glob('*.svg'):
        data='data:image/svg+xml;base64,'+base64.b64encode(p.read_bytes()).decode()
        html=html.replace(f'"/assets/{p.name}"',f'"{data}"').replace(f'"assets/{p.name}"',f'"{data}"')
    html=re.sub(r'<link[^>]+rel="stylesheet"[^>]*>','',html)
    html=re.sub(r'<script[^>]+src="(?:/)?assets/site\.js"[^>]*></script>','',html)
    page.set_content(html,wait_until='load');page.add_style_tag(content=(site/'assets/site.css').read_text(encoding='utf8'));page.add_script_tag(content=(site/'assets/site.js').read_text(encoding='utf8'))

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--dom',action='store_true');args=parser.parse_args()
    records=[]; pages=[]; issues=[]; servers={}
    try:
        if not args.dom:
            for k,(site,_) in SITES.items():
                s=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(site)));threading.Thread(target=s.serve_forever,daemon=True).start();servers[k]=s
        with sync_playwright() as p:
            exe=shutil.which('chromium') or shutil.which('chromium-browser')
            browser=p.chromium.launch(headless=True,**({'executable_path':exe} if exe else {'channel':'chrome'}))
            try:
                for k,(site,names) in SITES.items():
                    for width in (320,375,1440):
                        for name in names:
                            page=browser.new_page(viewport={'width':width,'height':900},device_scale_factor=1)
                            page.route('**/*',lambda r:r.continue_() if r.request.url.startswith('http://127.0.0.1:') else r.abort())
                            if args.dom:load_dom(page,site,name)
                            else:page.goto(f'http://127.0.0.1:{servers[k].server_port}/{name}',wait_until='load',timeout=10000)
                            page.add_style_tag(content='html{scroll-behavior:auto!important}')
                            seen=set()
                            for _ in range(100):
                                page.keyboard.press('Tab');o=page.evaluate(OBSERVE)
                                if o is None or o['id'] in seen:break
                                seen.add(o['id']);geometry=True
                                if o['skip'] and k=='cinderline':
                                    m=re.search(r'rgba?\([^)]*\)',o['shadow']);outer=m.group() if m else None
                                    vals=[contrast(o['outline'],o['strip']),contrast(outer,o['header']),contrast(o['outline'],outer)] if outer else [0]
                                    o['outer_ring']=outer;o['backgrounds']=[o['strip'],o['header']];geometry=o['offset']==0 and '8px' in o['shadow']
                                else:vals=[contrast(o['outline'],x) for x in o['backgrounds']]
                                o.update(site=k,page=name,viewport=width,contrast=round(min(vals),3),ratios=[round(x,3) for x in vals],status='PASS' if min(vals)>=3 and o['visible'] and o['style']!='none' and o['width']>=2 and geometry else 'FAIL');records.append(o)
                                if name=='index.html' and width==375 and (o['skip'] or o['footer'] or o['card']):page.screenshot(path=str(OUT/f'{k}-{width}-{o["id"]}.png'))
                                if o['toggle'] and page.locator('.menu-toggle,.nav-toggle').first.get_attribute('aria-expanded')=='false':page.keyboard.press('Enter')
                            expected=page.evaluate('''() => [...document.querySelectorAll('a[href],button,input,select,textarea,[tabindex]')].filter(e=>!e.disabled && e.tabIndex>=0 && e.getClientRects().length && getComputedStyle(e).visibility!=='hidden').length''')
                            pages.append({'site':k,'page':name,'width':width,'stops':len(seen),'expected':expected,'status':'PASS' if len(seen)==expected else 'FAIL'});page.close()
            finally:browser.close()
    except Exception as e:issues.append(str(e))
    finally:
        for s in servers.values():s.shutdown();s.server_close()
    counts={s:sum(x['status']==s for x in records) for s in ('PASS','FAIL')};counts['BLOCKED']=len(issues)
    report={'mode':'offline DOM' if args.dom else 'local HTTP static source','scope':'Tab traversal including expanded mobile menus; computed contrast and representative screenshots, not pixel-level or WCAG certification','counts':counts,'pages':pages,'issues':issues,'checks':records}
    (OUT/('focus-dom.json' if args.dom else 'focus-live.json')).write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'counts':counts,'pages':len(pages),'page_failures':[x for x in pages if x['status']=='FAIL'],'failures':[{k:x[k] for k in ('site','page','viewport','label','contrast','outline','backgrounds')} for x in records if x['status']=='FAIL'],'issues':issues},indent=2))
    return 2 if issues else 1 if counts['FAIL'] or len(pages)!=27 or any(x['status']=='FAIL' for x in pages) else 0
if __name__=='__main__':raise SystemExit(main())
