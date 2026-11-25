#!/usr/bin/env python3
"""Fictional Cinderline Cycle Studio staging service. Standard library only.

Run: python app.py --port 8772 [--db /path/to/demo.sqlite]
The example accepts demo requests locally; it sends no email or external traffic.
"""
import argparse
import hashlib
import hmac
import html
import os
from pathlib import Path
import re
import secrets
import sqlite3
import time
from urllib.parse import parse_qs, urlparse
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'site' / 'assets'
ROUTES = {
    '/': ('index.html', 'home'),
    '/index.html': ('index.html', 'home'),
    '/tune-ups.html': ('tune-ups.html', 'tune-ups'),
    '/repairs.html': ('repairs.html', 'repairs'),
    '/process.html': ('process.html', 'process'),
    '/request.html': ('request.html', 'request'),
}
PAGES = [x for x in ROUTES if x != '/']
TITLES = {
    'home': 'Thoughtful Bicycle Care | Cinderline Cycle Studio',
    'tune-ups': 'Bicycle Tune-Up Options | Cinderline Cycle Studio',
    'repairs': 'Bike Repair & Diagnostics | Cinderline Cycle Studio',
    'process': 'How Our Bicycle Service Works | Cinderline Cycle Studio',
    'request': 'Request a Bicycle Service Plan | Cinderline Cycle Studio',
}
DESCRIPTIONS = {
    'home': 'Explore a welcoming bicycle service studio concept, from routine tune-ups to careful repair diagnosis. Demo requests stay on this computer.',
    'tune-ups': 'Understand what a routine bicycle tune-up includes, when to book one, and how Cinderline approaches a careful mechanical inspection.',
    'repairs': 'From a slipping gear to an uncertain brake, see how a diagnosis-first bicycle repair process identifies the right next step.',
    'process': 'Discover the four stages of a practical bicycle service visit: share your concern, inspect, agree the work, and review the result.',
    'request': 'Use the local demonstration form to outline a bicycle issue and preview the request process. No real appointment or email is sent.',
}
NAV = [('index.html','Studio','home'),('tune-ups.html','Tune-ups','tune-ups'),('repairs.html','Repairs','repairs'),('process.html','Our process','process'),('request.html','Request a plan','request')]


def esc(s): return html.escape(str(s), quote=True)

def nav(active):
    links = ''.join(f'<a href="/{url}" {"aria-current=\"page\"" if key==active else ""}>{label}</a>' for url,label,key in NAV)
    return f'''<header class="site-header"><div class="wrap header-inner"><a class="brand" href="/index.html" aria-label="Cinderline home"><img src="/assets/mark.svg" width="33" height="33" alt=""><span>CINDERLINE<small>CYCLE STUDIO</small></span></a><button class="nav-toggle" type="button" aria-controls="site-nav" aria-expanded="false" aria-label="Open navigation"><span></span><span></span><span></span></button><nav class="primary-nav" id="site-nav" aria-label="Main navigation">{links}</nav></div></header>'''

def layout(key, body):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(TITLES[key])}</title><meta name="description" content="{esc(DESCRIPTIONS[key])}"><meta name="robots" content="noindex,nofollow"><meta name="color-scheme" content="light"><link rel="icon" href="/assets/mark.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/site.css"></head><body><a class="skip" href="#main">Skip to main content</a><div class="demo-strip">INTERNAL DESIGN PILOT · Fictional business · Not accepting real appointments</div>{nav(key)}<main id="main">{body}</main><footer class="footer"><div class="wrap footer-grid"><div><a href="/index.html" class="footer-name">CINDERLINE</a><p>Good rides begin with careful work.</p></div><div><strong>Explore</strong><a href="/tune-ups.html">Tune-up options</a><a href="/repairs.html">Repair approach</a><a href="/process.html">What to expect</a></div><div><strong>About this concept</strong><p>A fictional service-business design pilot. All requests remain in a local demo database. No phone, address, or real bookings.</p></div></div><div class="wrap footer-last"><span>© 2026 Cinderline concept demo</span><span>No public business affiliation</span></div></footer><script src="/assets/site.js" defer></script></body></html>'''


def render(key, csrf='DEMO_CSRF_ONLY', values=None, error='', success='', errors=None):
    values = values or {}
    if key=='home':
        body='''<section class="hero"><div class="wrap hero-grid"><div class="hero-copy"><span class="ride-badge" aria-hidden="true">⚡ MADE FOR THE RIDE</span><span class="eyebrow"><span class="eyebrow-line"></span> GOOD BIKES. GOOD ENERGY.</span><h1>Ride bold.<br>Roll <em>better.</em></h1><p class="lead">Every day rides, weekend adventures, and everything between. Thoughtful tune-ups and smart repairs to help you keep moving.</p><div class="button-row"><a class="button" href="/tune-ups.html">Explore tune-ups <span aria-hidden="true">↗</span></a><a class="quiet-link" href="/process.html">How it works <span aria-hidden="true">→</span></a></div><p class="hero-foot">Fictional studio concept · No appointments are offered.</p></div><div class="hero-visual"><span class="visual-sticker" aria-hidden="true">LET'S<br>ROLL!</span><img class="hero-img" src="/assets/hero.svg" width="700" height="700" alt="Bright orange bicycle illustration against a vivid yellow circular backdrop"><span class="visual-caption">MADE FOR YOUR NEXT ADVENTURE</span></div></div></section><section class="services-section wrap"><div class="section-intro"><span class="eyebrow">THE WORKSHOP</span><h2>Good care. More good rides.</h2><p>From an annual refresh to an unexpected rattle, start with the right conversation—not an automatic replacement.</p></div><div class="service-cards"><article><span class="card-index">01 / EVERYDAY RIDERS</span><h3>Routine tune-ups</h3><p>For the bicycle that still rides, but could feel much better. We start with safety and finish with the small details.</p><a href="/tune-ups.html">Find your tune-up <span aria-hidden="true">↗</span></a></article><article><span class="card-index">02 / BIG LITTLE FIXES</span><h3>Thoughtful fixes</h3><p>Unusual noises, slipping gears, worn parts—we identify the issue before proposing a practical fix.</p><a href="/repairs.html">Explore repairs <span aria-hidden="true">↗</span></a></article><article><span class="card-index">03 / THE NEXT ADVENTURE</span><h3>Clear next steps</h3><p>Understand the process, decide what matters most, and make informed choices about your ride.</p><a href="/process.html">See the process <span aria-hidden="true">↗</span></a></article></div></section><section class="closing"><div class="wrap closing-row"><div><span class="eyebrow">READY WHEN YOU ARE</span><h2>Tell us what your bike is trying to say.</h2></div><a class="button button-light" href="/request.html">Request a service plan <span aria-hidden="true">↗</span></a></div></section>'''
    elif key=='tune-ups':
        body='''<section class="subhero wrap"><span class="eyebrow">01 / ROUTINE CARE</span><h1>Better rides begin with a better tune-up.</h1><p class="lead">A practical inspection and adjustment plan for bicycles that deserve to feel comfortable, predictable and ready for the next journey.</p></section><section class="wrap editorial-grid"><div class="editorial-figure"><div class="abstract-circle"><span>01</span><strong>TUNE<br>WITH<br>CARE.</strong></div></div><div class="editorial-content"><h2>What belongs in a careful check?</h2><ul class="check-list"><li>Brakes: response, pad wear and safe adjustment</li><li>Shifting: cable tension and gear engagement</li><li>Wheels and tires: condition, pressure and alignment</li><li>Drivetrain: wear, lubrication and basic cleaning</li><li>Fasteners and contact points: a safety-first review</li></ul><p>Every bicycle is different. A specific service scope and any replacement parts must be agreed after inspection—this demo does not offer pricing or appointments.</p><a class="button" href="/request.html">Describe your bicycle <span aria-hidden="true">↗</span></a></div></section><section class="wrap faq-section"><span class="eyebrow">BEFORE YOU START</span><h2>Common questions</h2><div class="faq-grid"><article><h3>How do I know it needs attention?</h3><p>Rubbing brakes, hesitant shifting, unusual noises or an uncomfortable feel are good reasons to request a mechanical check.</p></article><article><h3>Will every part need replacing?</h3><p>Not necessarily. A responsible inspection separates adjustment from wear-related repairs and explains the difference.</p></article></div></section>'''
    elif key=='repairs':
        body='''<section class="subhero wrap"><span class="eyebrow">02 / PROBLEM SOLVING</span><h1>Find the issue. Then find the right fix.</h1><p class="lead">Good repair work begins with listening: to the rider, to the bicycle, and to the evidence found during inspection.</p></section><section class="wrap repair-grid"><article><span class="repair-num">01</span><h2>Braking trouble</h2><p>Weak stopping feel, squealing or a rubbing wheel can have different causes. Start by describing exactly when it occurs.</p></article><article><span class="repair-num">02</span><h2>Drivetrain friction</h2><p>Skipping chains, reluctant shifts and drivetrain noise call for a check of adjustment and component wear.</p></article><article><span class="repair-num">03</span><h2>Wheel & tire concerns</h2><p>Repeated flats, wobble or uneven wear deserve an inspection before choosing a repair or replacement.</p></article><article><span class="repair-num">04</span><h2>Unexpected noises</h2><p>Details about speed, terrain and pedaling help narrow the issue. A remote description alone cannot diagnose safety.</p></article></section><section class="band"><div class="wrap band-inner"><p><strong>Safety note:</strong> If brakes, steering or wheels may be unsafe, stop riding until the bicycle is properly inspected.</p><a href="/request.html">Describe the issue <span aria-hidden="true">↗</span></a></div></section>'''
    elif key=='process':
        body='''<section class="subhero wrap"><span class="eyebrow">03 / NO GUESSWORK</span><h1>Care with a clear beginning, middle and end.</h1><p class="lead">An understandable process makes the work—and the decision to do it—feel simpler.</p></section><section class="wrap timeline"><article><span>01</span><div><h2>Start with your story.</h2><p>Tell us what has changed and when you notice it. A few useful details help focus the first inspection.</p></div></article><article><span>02</span><div><h2>Inspect before deciding.</h2><p>A workshop inspection should identify likely causes, safety priorities and the available approaches.</p></div></article><article><span>03</span><div><h2>Agree on the work.</h2><p>No assumptions about replacements, costs or timing. The real business would confirm details before beginning.</p></div></article><article><span>04</span><div><h2>Review the result.</h2><p>Understand the work completed, any remaining maintenance needs and when the bicycle is safe to use.</p></div></article></section><section class="closing"><div class="wrap closing-row"><div><span class="eyebrow">NEXT STEP</span><h2>A clearer conversation starts here.</h2></div><a class="button button-light" href="/request.html">Open service request <span aria-hidden="true">↗</span></a></div></section>'''
    elif key=='request':
        errors = errors or {}
        field_labels = {
            'full_name': 'Your name', 'email': 'Email address', 'service': 'Service',
            'message': 'A few details', 'ack': 'Demo acknowledgement',
        }

        def invalid_attr(field):
            return f'aria-invalid="true" aria-describedby="{field}-error"' if field in errors else ''

        def field_error(field):
            return f'<span class="field-error" id="{field}-error">{esc(errors[field])}</span>' if field in errors else ''

        summary_items = ''.join(
            f'<li><a href="#{field}">{field_labels[field]}: {esc(errors[field])}</a></li>'
            for field in field_labels if field in errors
        )
        msgs = ''
        if error:
            msgs = (f'<div class="form-alert" role="alert" tabindex="-1" data-form-message>'
                    f'<strong>{esc(error)}</strong><ul>{summary_items}</ul></div>')
        if success:
            msgs = f'<div class="form-success" role="status" tabindex="-1" data-form-message>{esc(success)}</div>'
        options = ['General question', 'Tune-up', 'Brake concern', 'Drivetrain concern', 'Wheel or tire concern']
        select_options = ''.join(
            f'<option value="{esc(v)}" {"selected" if values.get("service", "General question") == v else ""}>{esc(v)}</option>'
            for v in options
        )
        ack_checked = 'checked' if values.get('ack') == 'yes' else ''
        body = f'''<section class="subhero wrap"><span class="eyebrow">04 / SAY HELLO</span><h1>Tell us a little about your ride.</h1><p class="lead">Use this local demo to see how a service request would work. It does not send an email or reserve a workshop appointment.</p></section><section class="wrap contact-layout"><div class="form-panel"><h2>Outline the concern</h2>{msgs}<form action="/submit" method="post"><input type="hidden" name="csrf" value="{esc(csrf)}"><label for="full_name">Your name <span aria-hidden="true">*</span></label><input id="full_name" name="full_name" autocomplete="name" maxlength="80" required value="{esc(values.get('full_name',''))}" {invalid_attr('full_name')}>{field_error('full_name')}<label for="email">Email address <span aria-hidden="true">*</span></label><input id="email" type="email" name="email" autocomplete="email" maxlength="150" required value="{esc(values.get('email',''))}" {invalid_attr('email')}>{field_error('email')}<label for="service">What would you like help with?</label><select id="service" name="service" {invalid_attr('service')}>{select_options}</select>{field_error('service')}<label for="message">A few details <span aria-hidden="true">*</span></label><textarea id="message" name="message" required maxlength="1000" rows="5" placeholder="For example: my gears skip when climbing." {invalid_attr('message')}>{esc(values.get('message',''))}</textarea>{field_error('message')}<label class="check-field"><input id="ack" name="ack" type="checkbox" value="yes" required {ack_checked} {invalid_attr('ack')}> <span>I understand this is a fictional demo; no real booking or message delivery will happen.</span></label>{field_error('ack')}<button class="button submit-btn" type="submit">Save demo request <span aria-hidden="true">↗</span></button><p class="form-footnote">Data is stored only in a local SQLite file for this demonstration. Use fictional details only.</p></form></div><aside class="contact-aside"><span class="eyebrow">WHAT HAPPENS NEXT?</span><h2>A small note, not a big commitment.</h2><p>In a real service website, the business would review your request and explain available next steps. This prototype intentionally stops at local storage.</p><div class="aside-rule"></div><strong>Before a real launch</strong><p>A verified contact channel, privacy notice, retention controls, hosting and domain details would all need owner approval.</p></aside></section>'''
    else: raise KeyError(key)
    return layout(key,body)


def init_db(db):
    db.parent.mkdir(parents=True,exist_ok=True)
    with sqlite3.connect(db) as c:
        c.execute('CREATE TABLE IF NOT EXISTS requests (id INTEGER PRIMARY KEY, created_at INTEGER NOT NULL, full_name TEXT NOT NULL, email TEXT NOT NULL, service TEXT NOT NULL, message TEXT NOT NULL)')


def create_handler(db,secret,clock=time.monotonic):
    requests_by_ip={}
    receipt_tokens={}
    class Handler(BaseHTTPRequestHandler):
        server_version='CinderlineStaging/0.1'
        sys_version=''
        def log_message(self,fmt,*args): pass
        def headers_out(self,code,content_type='text/html; charset=utf-8',length=None,cookie=None,location=None):
            self.send_response(code)
            self.send_header('Content-Type',content_type)
            self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('X-Frame-Options','DENY')
            self.send_header('Referrer-Policy','strict-origin-when-cross-origin')
            self.send_header('X-Robots-Tag','noindex, nofollow')
            self.send_header('Cache-Control','no-store')
            self.send_header('Content-Security-Policy',"default-src 'none'; style-src 'self'; script-src 'self'; img-src 'self'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'")
            if location:self.send_header('Location',location)
            if cookie:self.send_header('Set-Cookie',cookie)
            if length is not None:self.send_header('Content-Length',str(length))
            self.end_headers()
        def send_bytes(self,code,payload,type='text/html; charset=utf-8',cookie=None):
            self.headers_out(code,type,len(payload),cookie)
            if self.command!='HEAD': self.wfile.write(payload)
        def allowed_host(self):
            return self.headers.get('Host','') in {f'127.0.0.1:{self.server.server_port}',f'localhost:{self.server.server_port}'}
        def cookie_nonce(self):
            cookies=SimpleCookie()
            try:cookies.load(self.headers.get('Cookie',''))
            except Exception:pass
            raw=cookies.get('demo_sess')
            if raw:
                try:
                    nonce,mac=raw.value.split('.',1)
                    if re.fullmatch(r'[0-9a-f]{32}',nonce) and hmac.compare_digest(mac,hmac.new(secret,nonce.encode(),hashlib.sha256).hexdigest()):return nonce,None
                except ValueError:pass
            nonce=secrets.token_hex(16)
            token=nonce+'.'+hmac.new(secret,nonce.encode(),hashlib.sha256).hexdigest()
            return nonce,'demo_sess='+token+'; HttpOnly; SameSite=Strict; Path=/'
        def csrf(self,nonce): return hmac.new(secret,b'csrf:'+nonce.encode(),hashlib.sha256).hexdigest()
        def do_HEAD(self):
            # Serve the same headers/status as GET, without a response body.
            return self.do_GET()
        def do_GET(self):
            if not self.allowed_host():return self.send_bytes(421,b'Invalid host')
            path=urlparse(self.path).path
            if path in ROUTES:
                _,key=ROUTES[path]
                nonce,cookie=self.cookie_nonce()
                success=''
                if key=='request':
                    codes=parse_qs(urlparse(self.path).query).get('receipt',[])
                    if len(codes)==1:
                        match=receipt_tokens.get(codes[0])
                        if match and match[0]==nonce and clock()-match[1] < 600:
                            success='Demo request saved locally. No email was sent and no booking was made.'
                html_text=render(key,self.csrf(nonce),success=success)
                return self.send_bytes(200,html_text.encode(),cookie=cookie)
            if path.startswith('/assets/'):
                # fixed allow-list of assets; no untrusted path joining
                allowed={'/assets/site.css':('site.css','text/css; charset=utf-8'),'/assets/site.js':('site.js','application/javascript; charset=utf-8'),'/assets/mark.svg':('mark.svg','image/svg+xml'),'/assets/hero.svg':('hero.svg','image/svg+xml')}
                if path not in allowed:return self.send_bytes(404,b'Not found')
                name,typ=allowed[path]
                return self.send_bytes(200,(ASSETS/name).read_bytes(),typ)
            return self.send_bytes(404,b'Not found')
        def do_POST(self):
            if not self.allowed_host():return self.send_bytes(421,b'Invalid host')
            if urlparse(self.path).path!='/submit':return self.send_bytes(404,b'Not found')
            expected=f'http://{self.headers.get("Host")}'
            origin=self.headers.get('Origin')
            if origin and origin!=expected:return self.send_bytes(403,b'Invalid origin')
            if self.headers.get('Content-Type','').split(';')[0].strip()!='application/x-www-form-urlencoded':return self.send_bytes(415,b'Unsupported media')
            try:length=int(self.headers.get('Content-Length','0'))
            except ValueError:return self.send_bytes(400,b'Invalid content length')
            if length<=0 or length>8192:return self.send_bytes(413,b'Invalid request size')
            try:
                data=parse_qs(self.rfile.read(length).decode('utf-8',errors='replace'),keep_blank_values=True, max_num_fields=8)
            except ValueError:
                return self.send_bytes(400,b'Malformed form fields')
            if any(len(v)!=1 for v in data.values()):return self.send_bytes(400,b'Duplicate field')
            fields={k:v[0] for k,v in data.items()}
            nonce,cookie=self.cookie_nonce()
            if cookie or not hmac.compare_digest(fields.get('csrf',''),self.csrf(nonce)):return self.send_bytes(403,b'Invalid form session')
            ip=self.client_address[0]
            now=clock(); history=[x for x in requests_by_ip.get(ip,[]) if now-x<60]
            if len(history)>=4:return self.send_bytes(429,b'Too many demo requests')
            requests_by_ip[ip]=history+[now]
            name=fields.get('full_name','').strip();email=fields.get('email','').strip();service=fields.get('service','').strip();message=fields.get('message','').strip()
            options=['General question','Tune-up','Brake concern','Drivetrain concern','Wheel or tire concern']
            errors={}
            if not 2 <= len(name) <= 80:
                errors['full_name']='Enter a name between 2 and 80 characters.'
            if not 4 <= len(email) <= 150 or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',email):
                errors['email']='Enter a valid email address.'
            if service not in options:
                errors['service']='Choose a listed service.'
            if not 12 <= len(message) <= 1000:
                errors['message']='Enter 12 to 1,000 characters describing the issue.'
            if fields.get('ack')!='yes':
                errors['ack']='Confirm that you understand this is a demo.'
            if errors:
                raw=render('request',self.csrf(nonce),fields,error='Please review the highlighted fields.',errors=errors).encode()
                return self.send_bytes(422,raw)
            with sqlite3.connect(db) as c:
                c.execute('INSERT INTO requests (created_at, full_name, email, service, message) VALUES (?,?,?,?,?)',
                          (int(time.time()),name,email,service,message))
            # Post/Redirect/Get prevents a browser refresh from submitting a duplicate.
            # The opaque in-memory receipt is bound to the original signed session.
            expired=[t for t,(session,at) in receipt_tokens.items() if clock()-at >= 600]
            for token in expired: receipt_tokens.pop(token,None)
            if len(receipt_tokens)>=200: receipt_tokens.clear()
            token=secrets.token_urlsafe(18)
            receipt_tokens[token]=(nonce,clock())
            return self.headers_out(303,length=0,location='/request.html?receipt='+token)
    return Handler


def export_snapshots():
    site=ROOT/'site'
    for path,(filename,key) in ROUTES.items():
        if path=='/':continue
        (site/filename).write_text(render(key),encoding='utf-8')


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--port',type=int,default=8772)
    ap.add_argument('--db',type=Path,default=ROOT/'data'/'demo-requests.sqlite')
    args=ap.parse_args()
    if not 1<=args.port<=65535:raise SystemExit('Invalid port')
    init_db(args.db)
    server=ThreadingHTTPServer(('127.0.0.1',args.port),create_handler(args.db,secrets.token_bytes(32)))
    print(f'CINDERLINE_DEMO http://127.0.0.1:{args.port}/index.html',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:server.shutdown()

if __name__=='__main__':main()
