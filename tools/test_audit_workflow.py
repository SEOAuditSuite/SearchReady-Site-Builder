#!/usr/bin/env python3
"""Exercise offline source audit -> finding -> repair -> recheck; no external SEO tool claims."""
from pathlib import Path
import tempfile, shutil, unittest, re
from site_preflight import inspect
ROOT=Path(__file__).resolve().parents[1]
class AuditWorkflow(unittest.TestCase):
    def test_audit_fix_recheck(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp)/'site'; shutil.copytree(ROOT/'pilot/site',dest)
            page=dest/'index.html'; original=page.read_bytes()
            self.assertEqual(inspect(dest)['status'],'PASS')
            text=original.decode('utf-8')
            broken,n=re.subn(r'<title>.*?</title>','',text,count=1,flags=re.S|re.I); self.assertEqual(n,1)
            self.assertIn('href="services.html"',broken)
            broken=broken.replace('href="services.html"','href="missing-review-page.html"',1)
            page.write_text(broken,encoding='utf-8',newline='\n')
            result=inspect(dest); self.assertEqual(result['status'],'FAIL')
            self.assertTrue(any('title' in e and 'index.html' in e for e in result['errors']))
            self.assertTrue(any('missing-review-page.html' in e and 'broken internal link' in e for e in result['errors']))
            print('Observed injected findings:',*result['errors'],sep='\n - ')
            page.write_bytes(original)
            self.assertEqual(inspect(dest)['status'],'PASS');self.assertEqual(page.read_bytes(),original)
    def test_staging_is_not_launch_ready(self):
        result=inspect(ROOT/'pilot/site','production','https://clearroom.example')
        self.assertEqual(result['status'],'FAIL')
        for term in ['noindex','canonical','sitemap']:
            self.assertTrue(any(term in e for e in result['errors']))
if __name__=='__main__': unittest.main(verbosity=2)
