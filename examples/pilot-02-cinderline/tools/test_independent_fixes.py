#!/usr/bin/env python3
"""Focused review regressions only; does not replay previous Pilot 02 tests."""
from pathlib import Path
import http.client
import json
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.parse

ROOT = Path(__file__).resolve().parents[1]
results = []

def check(name, predicate, detail):
    results.append({'check': name, 'status': 'PASS' if predicate else 'FAIL', 'detail': detail})

with tempfile.TemporaryDirectory(prefix='cinderline-independent-') as d:
    db = Path(d) / 'isolated.sqlite'
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]
    log_path = Path(d) / 'server.log'
    with log_path.open('w') as log:
        proc = subprocess.Popen([sys.executable, str(ROOT/'app.py'),'--port',str(port),'--db',str(db)],stdout=log,stderr=subprocess.STDOUT)
        try:
            for _ in range(60):
                try:
                    c=http.client.HTTPConnection('127.0.0.1',port,timeout=1)
                    c.request('GET','/index.html')
                    r=c.getresponse();r.read();c.close()
                    break
                except Exception:
                    time.sleep(.1)
            else:
                raise RuntimeError('Server did not start')
            def req(method,body=None,headers=None):
                c=http.client.HTTPConnection('127.0.0.1',port,timeout=3)
                try:
                    c.request(method,'/index.html' if method=='HEAD' else '/submit' if method=='POST' else '/index.html', body=body,headers=headers or {})
                    r=c.getresponse(); payload=r.read(); return r.status,dict(r.getheaders()),payload
                finally:c.close()
            st,h,b=req('GET')
            check('Unchanged GET index works',st==200 and b'<main' in b, f'status={st}')
            st,hh,bh=req('HEAD')
            check('HEAD matches GET content length without body',st==200 and bh==b'' and int(hh.get('Content-Length','-1'))==len(b),f'status={st}, length={hh.get("Content-Length")}, body={len(bh)}')
            body=urllib.parse.urlencode({f'key{i}':f'value{i}' for i in range(9)})
            st,hs,bs=req('POST',body=body,headers={'Content-Type':'application/x-www-form-urlencoded'})
            check('Malformed extra form fields return HTTP 400',st==400 and b'Malformed form fields' in bs,f'status={st}, bytes={len(bs)}')
            check('No dummy entries created by malformed request',db.exists() and __import__('sqlite3').connect(db).execute('SELECT count(*) FROM requests').fetchone()[0]==0,'isolate demo DB row count=0')
        finally:
            proc.terminate()
            try:proc.wait(timeout=4)
            except subprocess.TimeoutExpired:proc.kill()

try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True, executable_path=shutil.which('chromium') or None, args=['--no-sandbox'])
        page=browser.new_page()
        page.set_content('''<input id="message" aria-label="Message"><button class="nav-toggle" aria-controls="site-nav" aria-expanded="false" aria-label="Open navigation">Menu</button><nav id="site-nav"><a href="#">One</a></nav>''')
        page.add_script_tag(path=str(ROOT/'site/assets/site.js'))
        page.locator('#message').focus()
        page.keyboard.press('Escape')
        remained=page.evaluate("document.activeElement?.id === 'message'")
        check('Escape in form does not steal focus when menu closed',remained,f'remained={remained}')
        page.locator('.nav-toggle').click()
        page.keyboard.press('Escape')
        closed=page.locator('.nav-toggle').get_attribute('aria-expanded')=='false'
        focused=page.evaluate("document.activeElement?.classList.contains('nav-toggle')")
        check('Escape closes expanded menu and restores button focus',closed and focused,f'closed={closed}, focused={focused}')
        browser.close()
except Exception as exc:
    results.append({'check':'Focused browser keyboard behavior','status':'BLOCKED','detail':type(exc).__name__+': '+str(exc)[:180]})

counts={status:sum(x['status']==status for x in results) for status in ['PASS','FAIL','BLOCKED']}
summary={'purpose':'Independent review targeted regressions only','results':results,'counts':counts,'source':'reviewed copy; original ZIP preserved'}
out=ROOT/'evidence/reviewer-targeted-results.json';out.write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary,indent=2))
raise SystemExit(1 if counts['FAIL'] else 0)
