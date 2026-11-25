#!/usr/bin/env python3
"""Focused independent-review fixes D1-D5. Runs isolated HTTP and parser checks, not old suites."""
import http.client
import http.cookiejar
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import re
import sqlite3
import sys
import tempfile
import threading
from urllib.parse import urlencode, urlparse
from urllib.request import build_opener, HTTPCookieProcessor, Request
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import app
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT.parent.parent
checks=[]
def ck(name,ok,detail=''):
    checks.append({'check':name,'status':'PASS' if ok else 'FAIL','detail':detail})
def count(db):
    with sqlite3.connect(db) as c:
        return c.execute('SELECT count(*) FROM requests').fetchone()[0]
def fetch(port,method,path,body=None,headers=None):
    c=http.client.HTTPConnection('127.0.0.1',port,timeout=3)
    try:
        c.request(method,path,body=body,headers=headers or {})
        r=c.getresponse();status=r.status;hs=dict(r.getheaders());b=r.read()
        return status,hs,b
    finally:c.close()

def luminance(hexcolor):
    vals=[int(hexcolor[x:x+2],16)/255 for x in (1,3,5)]
    linear=[c/12.92 if c<=0.04045 else ((c+.055)/1.055)**2.4 for c in vals]
    return sum(x*y for x,y in zip(linear,(.2126,.7152,.0722)))
def contrast(a,b):
    v=sorted([luminance(a),luminance(b)])
    return (v[1]+.05)/(v[0]+.05)

css=(ROOT/'site/assets/site.css').read_text()
pilotcss=(SKILL/'pilot/site/assets/site.css').read_text()
ck('D1 hero-foot text contrast AA', 'color:#475447' in css and contrast('#475447','#eee9db')>=4.5, f'ratio {contrast("#475447","#eee9db"):.2f}')
ck('D2 form controls border vs fill and panel AA', 'border:1px solid #5b6156' in css and min(contrast('#5b6156','#faf9f4'),contrast('#5b6156','#e8e5db'))>=3, f'min ratio {min(contrast("#5b6156","#faf9f4"),contrast("#5b6156","#e8e5db")):.2f}')
ck('D5 Pilot01 focus outline contrast', 'outline:3px solid #2a635b' in pilotcss and contrast('#2a635b','#f8f5ee')>=3, f'ratio {contrast("#2a635b","#f8f5ee"):.2f}')
# D5 regression: the offset outline must contrast against EACH adjacent dark section.
for label, stylesheet, selector, background in (
    ('Pilot01 CTA', pilotcss, '.cta-band a:focus-visible', '#183b36'),
    ('Pilot01 dark footer', pilotcss, '.footer a:focus-visible', '#102c26'),
    ('Pilot02 closing CTA', css, '.closing a:focus-visible', '#20352e'),
):
    ck('D5 ' + label + ' focus ring on dark surface',
       selector in stylesheet and 'outline-color:#fff7e6' in stylesheet and contrast('#fff7e6',background)>=3,
       f'focus/background ratio {contrast("#fff7e6",background):.2f}')
with tempfile.TemporaryDirectory() as d:
    db=Path(d)/'tmp.sqlite'; app.init_db(db)
    server=ThreadingHTTPServer(('127.0.0.1',0),app.create_handler(db,b'one-time-demo-key'))
    port=server.server_port; t=threading.Thread(target=server.serve_forever,daemon=True); t.start()
    try:
        status,hs,b=fetch(port,'GET','/request.html')
        cookie=hs['Set-Cookie'].split(';')[0]
        csrf=re.search(rb'name="csrf" value="([a-f0-9]{64})"',b).group(1).decode()
        common={'Origin':f'http://127.0.0.1:{port}','Content-Type':'application/x-www-form-urlencoded','Cookie':cookie}
        invalid=urlencode({'csrf':csrf,'full_name':'A','email':'bad','service':'Tune-up','message':'short'}).encode()
        st,h,body=fetch(port,'POST','/submit',invalid,common)
        decoded=body.decode()
        ck('D3 invalid form returns 422 + linked summary',st==422 and 'data-form-message' in decoded and 'href="#full_name"' in decoded and 'role="alert"' in decoded,f'status={st}')
        ck('D3 per-field aria-invalid + aria-describedby', all(x in decoded for x in ('id="full_name-error"','id="email-error"','id="message-error"','id="ack-error"','aria-describedby="full_name-error"','aria-invalid="true"')), 'field-level errors present')
        ck('D3 preserves valid entered field and focus script', 'value="A"' in decoded and "notice.focus()" in (ROOT/'site/assets/site.js').read_text() and count(db)==0, 'no row saved for invalid')
        valid=urlencode({'csrf':csrf,'full_name':'Demo Person','email':'test@example.invalid','service':'Tune-up','message':'The bike makes a sound when riding on cobblestones.','ack':'yes'}).encode()
        st,h,b=fetch(port,'POST','/submit',valid,common)
        location=h.get('Location','')
        ck('D4 successful POST issues HTTP 303',st==303 and location.startswith('/request.html?receipt=') and count(db)==1,f'status={st}, count={count(db)}')
        st,h,b=fetch(port,'GET',location,headers={'Cookie':cookie})
        ck('D4 redirected GET confirms session-bound receipt',st==200 and b'Demo request saved locally' in b and count(db)==1,f'status={st}, count={count(db)}')
        st,h,b=fetch(port,'GET',location,headers={'Cookie':cookie})
        ck('D4 refresh GET never resubmits duplicate',st==200 and count(db)==1, f'refresh count={count(db)}')
        st,h,b=fetch(port,'GET',location)
        ck('D4 unbound session cannot forge success',st==200 and b'Demo request saved locally' not in b, f'guest status={st}')
        ck('D6 reviewed HEAD fix preserved',fetch(port,'HEAD','/index.html')[0]==200,'HEAD HTTP 200')
        ck('D10 reviewed Escape focus guard preserved',"toggle.getAttribute('aria-expanded') === 'true'" in (ROOT/'site/assets/site.js').read_text(),'menu-state check retained')
    finally:
        server.shutdown();server.server_close();t.join(timeout=2)
summary={'scope':'D1-D5 focused remediation; preserves previously PASS checks','results':checks,'pass':sum(x['status']=='PASS' for x in checks),'fail':sum(x['status']=='FAIL' for x in checks)}
out=ROOT/'evidence/release-fixes-results.json'
out.write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({'pass':summary['pass'],'fail':summary['fail'],'checks':checks},indent=2))
raise SystemExit(1 if summary['fail'] else 0)
