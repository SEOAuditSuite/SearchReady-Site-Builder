#!/usr/bin/env python3
import shutil
import tempfile
import unittest
from pathlib import Path
from site_preflight import inspect

PILOT=Path(__file__).resolve().parents[1]/'pilot'/'site'

class TestPreflight(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)/'site'
        shutil.copytree(PILOT,self.root)
    def tearDown(self): self.tmp.cleanup()
    def modify(self,name,old,new):
        p=self.root/name
        s=p.read_text(encoding='utf-8');self.assertIn(old,s)
        p.write_text(s.replace(old,new,1),encoding='utf-8')
    def test_staging_good(self): self.assertEqual(inspect(self.root)['errors'],[])
    def test_detect_missing_title(self):
        self.modify('index.html','<title>','<not-title>')
        self.assertTrue(any('title' in e for e in inspect(self.root)['errors']))
    def test_detect_missing_noindex(self):
        self.modify('index.html','noindex,nofollow','index,follow')
        self.assertTrue(any('missing noindex' in e for e in inspect(self.root)['errors']))
    def test_detect_broken_internal_link(self):
        self.modify('index.html','href="services.html"','href="missing.html"')
        self.assertTrue(any('broken internal link' in e for e in inspect(self.root)['errors']))
    def test_detect_missing_image_alt(self):
        self.modify('index.html','alt="Stylized organized living nook with shelves, plants and seating"','')
        self.assertTrue(any('lack alt' in e for e in inspect(self.root)['errors']))
    def test_detect_invalid_jsonld(self):
        self.modify('index.html','</head>','<script type="application/ld+json">{broken</script></head>')
        self.assertTrue(any('JSON-LD' in e for e in inspect(self.root)['errors']))
    def test_detect_duplicate_title(self):
        title='Clearroom | Thoughtful Home Organizing — Fictional Design Preview'
        other='Example Organizing Services | Clearroom Design Preview'
        self.modify('services.html',other,title)
        self.assertTrue(any('duplicate title' in e for e in inspect(self.root)['errors']))
    def test_production_refuses_staging_demo(self):
        res=inspect(self.root,'production','https://clearroom.example')
        self.assertEqual(res['status'],'FAIL')
        self.assertTrue(any('noindex' in e for e in res['errors']))
        self.assertTrue(any('sitemap.xml' in e for e in res['errors']))
        self.assertTrue(any('canonical' in e for e in res['errors']))
    def test_detect_missing_local_asset(self):
        (self.root/'assets'/'hero-art.svg').unlink()
        self.assertTrue(any('missing local asset' in e for e in inspect(self.root)['errors']))

if __name__=='__main__': unittest.main(verbosity=2)
