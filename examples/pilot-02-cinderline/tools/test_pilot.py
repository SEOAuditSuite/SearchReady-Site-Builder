#!/usr/bin/env python3
"""Focused local HTTP, form security and persistence acceptance for staging second pilot."""
from contextlib import contextmanager
import http.cookiejar
from http.server import ThreadingHTTPServer
from http import HTTPStatus
from pathlib import Path
import re
import sqlite3
import sys
import tempfile
import threading
from urllib.request import build_opener, HTTPCookieProcessor, Request
from urllib.parse import urlencode
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import app

@contextmanager
def running(db):
    app.init_db(db)
    server=ThreadingHTTPServer(('127.0.0.1',0),app.create_handler(db,b'private-test-secret'))
    t=threading.Thread(target=server.serve_forever,daemon=True);t.start()
    try:yield server.server_address[1]
    finally:server.shutdown();server.server_close();t.join(timeout=2)

def fetch(opener,url,data=None,headers=None):
    import urllib.error
    req=Request(url,data=data,headers=headers or {})
    try:r=opener.open(req,timeout=5)
    except urllib.error.HTTPError as e:r=e
    return r.status,r.read().decode('utf8',errors='replace'),r.headers

def extract_csrf(html):
    m=re.search(r'name="csrf" value="([a-f0-9]{64})"',html)
    assert m, 'CSRF missing'
    return m.group(1)

class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._temp=tempfile.TemporaryDirectory();cls.db=Path(cls._temp.name)/'pilot.sqlite'
        cls.c=running(cls.db);cls.port=cls.c.__enter__();cls.url=f'http://127.0.0.1:{cls.port}'
    @classmethod
    def tearDownClass(cls):cls.c.__exit__(None,None,None);cls._temp.cleanup()
    def opener(self):return build_opener(HTTPCookieProcessor(http.cookiejar.CookieJar()))
    def test_01_all_five_real_html_routes_200(self):
        op=self.opener()
        for path in app.PAGES:
            status,s,h=fetch(op,self.url+path)
            with self.subTest(path=path):
                self.assertEqual(status,200)
                self.assertIn('<h1>',s)
    def test_02_server_does_not_render_JS_only_content(self):
        op=self.opener()
        status,s,h=fetch(op,self.url+'/index.html')
        self.assertIn('Every ride',s);self.assertIn('Routine tune-ups',s)
    def test_03_stage_noindex_in_header_and_html(self):
        op=self.opener()
        for path in app.PAGES:
            _,s,h=fetch(op,self.url+path)
            with self.subTest(path=path):
                self.assertIn('noindex',h.get('X-Robots-Tag',''))
                self.assertIn('name="robots" content="noindex,nofollow"',s)
                self.assertNotIn('rel="canonical"',s)
    def test_04_unique_page_titles_and_descriptions(self):
        op=self.opener();titles=[];descs=[]
        for path in app.PAGES:
            _,s,_=fetch(op,self.url+path)
            titles.append(re.search(r'<title>(.*?)</title>',s).group(1))
            descs.append(re.search(r'name="description" content="(.*?)"',s).group(1))
        self.assertEqual(len(set(titles)),5)
        self.assertEqual(len(set(descs)),5)
    def test_05_http_assets(self):
        op=self.opener()
        for file in ('site.css','site.js','mark.svg','hero.svg'):
            status,body,h=fetch(op,self.url+'/assets/'+file)
            with self.subTest(file=file):self.assertEqual(status,200);self.assertGreater(len(body),10)
    def test_06_missing_assets_404(self):
        op=self.opener();status,_,_=fetch(op,self.url+'/assets/missing.svg');self.assertEqual(status,404)
    def test_07_host_restriction(self):
        op=self.opener();status,_,_=fetch(op,self.url+'/index.html',headers={'Host':'evil.example'});self.assertEqual(status,421)
    def test_08_security_headers(self):
        op=self.opener();_,_,h=fetch(op,self.url+'/index.html')
        for key in ('Content-Security-Policy','X-Content-Type-Options','X-Frame-Options','Referrer-Policy'):
            with self.subTest(key=key):self.assertTrue(h.get(key))
    def test_09_no_external_requests_in_html(self):
        op=self.opener()
        for path in app.PAGES:
            _,s,_=fetch(op,self.url+path)
            with self.subTest(path=path):self.assertNotIn('src="https:',s)
    def test_10_cross_site_form_rejected(self):
        op=self.opener();_,s,_=fetch(op,self.url+'/request.html')
        payload=urlencode({'csrf':extract_csrf(s),'full_name':'Demo Tester','email':'test@example.invalid','service':'Tune-up','message':'This is a fake test bicycle request.','ack':'yes'}).encode()
        status,_,_=fetch(op,self.url+'/submit',payload,{'Origin':'https://evil.example','Content-Type':'application/x-www-form-urlencoded'})
        self.assertEqual(status,403)
    def test_11_missing_csrf_rejected(self):
        op=self.opener();_,s,_=fetch(op,self.url+'/request.html')
        status,_,_=fetch(op,self.url+'/submit',urlencode({'full_name':'Test'}).encode(),{'Content-Type':'application/x-www-form-urlencoded'})
        self.assertEqual(status,403)
    def test_12_invalid_form_rejected(self):
        op=self.opener();_,s,_=fetch(op,self.url+'/request.html')
        body=urlencode({'csrf':extract_csrf(s),'full_name':'A','email':'not-email','service':'Tune-up','message':'short','ack':'yes'}).encode()
        status,html,_=fetch(op,self.url+'/submit',body,{'Content-Type':'application/x-www-form-urlencoded'})
        self.assertEqual(status,422);self.assertIn('role="alert"',html)
    def test_13_content_type_guard(self):
        op=self.opener();_,s,_=fetch(op,self.url+'/request.html')
        status,_,_=fetch(op,self.url+'/submit',b'a=b',{'Content-Type':'text/plain'})
        self.assertEqual(status,415)
    def test_14_duplicate_field_guard(self):
        op=self.opener();_,s,_=fetch(op,self.url+'/request.html')
        body='csrf='+extract_csrf(s)+'&csrf=bad'
        status,_,_=fetch(op,self.url+'/submit',body.encode(),{'Content-Type':'application/x-www-form-urlencoded'})
        self.assertEqual(status,400)
    def test_15_max_body_guard(self):
        op=self.opener();_,s,_=fetch(op,self.url+'/request.html')
        status,_,_=fetch(op,self.url+'/submit',b'x'*8193,{'Content-Type':'application/x-www-form-urlencoded'})
        self.assertEqual(status,413)
    def test_16_valid_demo_submission(self):
        op=self.opener();_,s,_=fetch(op,self.url+'/request.html')
        body=urlencode({'csrf':extract_csrf(s),'full_name':'Test Person','email':'test@example.invalid','service':'Brake concern','message':'The rear brake squeaks at low speed on my demo bike.','ack':'yes'}).encode()
        status,html,_=fetch(op,self.url+'/submit',body,{'Content-Type':'application/x-www-form-urlencoded','Origin':self.url})
        self.assertEqual(status,200);self.assertIn('Demo request saved locally',html)
        with sqlite3.connect(self.db) as db:
            data=db.execute('SELECT full_name,email,service,message FROM requests').fetchone()
        self.assertEqual(data[0],'Test Person');self.assertEqual(data[1],'test@example.invalid')
    def test_17_xss_not_rendered_in_invalid_echo(self):
        op=self.opener();_,s,_=fetch(op,self.url+'/request.html')
        msg='<script>alert(1)</script>'
        body=urlencode({'csrf':extract_csrf(s),'full_name':msg,'email':'bad','service':'Tune-up','message':msg,'ack':'yes'}).encode()
        status,html,_=fetch(op,self.url+'/submit',body,{'Content-Type':'application/x-www-form-urlencoded'})
        self.assertEqual(status,422)
        self.assertNotIn(msg,html);self.assertIn('&lt;script&gt;',html)
    def test_18_no_third_party_contact_delivery(self):
        self.assertNotIn('smtplib',Path(app.__file__).read_text())
    def test_19_local_db_retained_after_connection_closed(self):
        with sqlite3.connect(self.db) as db:self.assertGreaterEqual(db.execute('SELECT count(*) FROM requests').fetchone()[0],1)
    def test_20_path_traversal_not_served(self):
        op=self.opener();status,_,_=fetch(op,self.url+'/assets/../app.py');self.assertEqual(status,404)

if __name__=='__main__':unittest.main(verbosity=2)
