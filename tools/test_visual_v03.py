#!/usr/bin/env python3
"""Focused v0.3 visual-direction regression guard (stdlib; no old suites rerun).

The visual verdict still requires human review and real-browser evidence. Tests here only
check changed source/art-direction invariants, snapshots, SEO essentials, and HTTP assets.
"""
from pathlib import Path
import importlib.util
import json
import re
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
CLEAR = ROOT / 'pilot' / 'site'
CINDER = ROOT / 'examples' / 'pilot-02-cinderline'


def contrast(a,b):
    def rgb(h):
        z=[int(h[i:i+2],16)/255 for i in (1,3,5)]
        return [x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in z]
    la,lb=[sum(c*w for c,w in zip(rgb(x),(.2126,.7152,.0722))) for x in (a,b)]
    return (max(la,lb)+.05)/(min(la,lb)+.05)


class VisualV03Tests(unittest.TestCase):
    def test_distinctive_brand_directions(self):
        a=(CLEAR/'assets/site.css').read_text(encoding='utf-8')
        b=(CINDER/'site/assets/site.css').read_text(encoding='utf-8')
        self.assertIn('SUNNY, AIRY, OPTIMISTIC',a)
        self.assertIn('ELECTRIC, PREMIUM, ENERGETIC',b)
        self.assertIn('benefit-ribbon',a)
        self.assertIn('visual-sticker',b)
        self.assertIn('background:#264be4',b)
        self.assertIn('background:#ff653f',b)

    def test_original_assets_and_no_remote_references(self):
        for site,svg in ((CLEAR,'hero-art.svg'),(CINDER/'site','hero.svg')):
            asset=(site/'assets'/svg).read_text(encoding='utf-8')
            self.assertIn('<svg',asset)
            self.assertNotIn('http://',asset.replace('http://www.w3.org/2000/svg',''))
            self.assertNotIn('https://',asset)
        self.assertIn('Bright and organized', (CLEAR/'assets/hero-art.svg').read_text())
        self.assertIn('Energetic orange', (CINDER/'site/assets/hero.svg').read_text())

    def test_preview_pages_keep_seo_and_staging_truth(self):
        for root,files in ((CLEAR,['index.html','services.html','process.html','contact.html']),
                          (CINDER/'site',['index.html','tune-ups.html','repairs.html','process.html','request.html'])):
            for name in files:
                s=(root/name).read_text(encoding='utf-8')
                with self.subTest(path=f'{root.name}/{name}'):
                    self.assertIn('noindex,nofollow',s)
                    self.assertEqual(len(re.findall(r'<h1[\s>]',s)),1)
                    self.assertIn('<title>',s)
                    self.assertIn('<meta name="description"',s)
                    self.assertIn('href=',s)

    def test_cinderline_static_snapshot_parity(self):
        p=CINDER/'app.py'
        spec=importlib.util.spec_from_file_location('cinderline_visual_fixture',p)
        app=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app)
        for page,(name,key) in app.ROUTES.items():
            if page=='/':continue
            with self.subTest(page=page):
                self.assertEqual((CINDER/'site'/name).read_text(encoding='utf-8'),app.render(key))

    def test_contrast_in_new_visual_systems(self):
        for a,b,min_ratio in [
            ('#ffffff','#264be4',4.5), # Cinderline hero copy
            ('#111b39','#ff653f',4.5), # Cinderline button copy
            ('#ffffff','#111b39',4.5), # Cinderline navigation
            ('#173447','#ffdf86',4.5), # Clearroom CTA
            ('#16384b','#eaf9f8',4.5), # Clearroom footer
            ('#fff4b9','#264be4',3.0), # Focus outline on Cinderline hero
            ('#fff4b9','#111b39',3.0), # Focus outline on Cinderline footer
            ('#111b39','#ff653f',3.0), # Focus outline on Cinderline closing section
            ('#185d95','#eaf9f8',3.0), # Clearroom mint footer
            ('#185d95','#ffdf86',3.0), # Clearroom yellow CTA
            ('#fff7e6','#111b39',3.0), # Cinderline navy card / skip outer ring
            ('#111b39','#ff744d',3.0), # Cinderline coral card
            ('#111b39','#ffe36d',3.0), # Cinderline yellow card
            ('#111b39','#ffcf47',3.0), # Cinderline skip inner ring on yellow
            ('#111b39','#fff7e6',3.0), # Two-tone skip ring contrast
        ]:
            with self.subTest(colors=(a,b)):
                self.assertGreaterEqual(contrast(a,b),min_ratio)

    def test_focus_rules_follow_current_surfaces(self):
        a=(CLEAR/'assets/site.css').read_text(encoding='utf-8')
        b=(CINDER/'site/assets/site.css').read_text(encoding='utf-8')
        self.assertIn('.footer a:focus-visible,.footer button:focus-visible{outline-color:#185d95}',a)
        self.assertNotIn('.footer button:focus-visible{outline-color:#fff7e6}',a)
        self.assertIn('.service-cards article a:focus-visible{outline-color:#fff7e6}',b)
        self.assertIn('.service-cards article:nth-child(n+2) a:focus-visible{outline-color:#111b39}',b)
        self.assertIn('.skip:focus-visible{outline:4px solid #111b39;outline-offset:0;box-shadow:0 0 0 8px #fff7e6}',b)
        self.assertIn('@media(forced-colors:active){.skip:focus-visible{outline-color:Highlight;box-shadow:none}}',b)

    def test_cinderline_local_http_assets_and_pages(self):
        p=CINDER/'app.py';spec=importlib.util.spec_from_file_location('cinderline_http_fixture',p)
        app=importlib.util.module_from_spec(spec);spec.loader.exec_module(app)
        with tempfile.TemporaryDirectory() as tmp:
            db=Path(tmp)/'demo.sqlite';app.init_db(db)
            import secrets
            server=ThreadingHTTPServer(('127.0.0.1',0),app.create_handler(db,secrets.token_bytes(32)))
            worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
            try:
                for route in list(app.ROUTES)+['/assets/site.css','/assets/hero.svg','/assets/mark.svg']:
                    with self.subTest(route=route):
                        with urlopen(f'http://127.0.0.1:{server.server_port}{route}',timeout=3) as response:
                            self.assertEqual(response.status,200)
                            self.assertEqual(response.headers['X-Robots-Tag'],'noindex, nofollow')
            finally:
                server.shutdown();server.server_close();worker.join(timeout=3)

if __name__=='__main__':
    unittest.main(verbosity=2)
