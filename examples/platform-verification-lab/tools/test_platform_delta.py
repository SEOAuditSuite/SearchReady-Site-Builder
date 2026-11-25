#!/usr/bin/env python3
"""Targeted regression fixture: actual CSS with representative WP markup; not native runtime.
Shopify checks metadata/locale contract only; not official Theme Check.
"""
from pathlib import Path
import json, os, re, shutil, unittest
from urllib.parse import urlparse
R=Path(__file__).resolve().parents[1]
W=R/'wordpress/fieldnote-learning'; S=R/'shopify/paper-spark'
class PlatformDelta(unittest.TestCase):
 def test_shopify_metadata(self):
  d=json.loads((S/'config/settings_schema.json').read_text())[0]
  self.assertEqual(d['name'],'theme_info')
  self.assertTrue(bool(d.get('theme_support_url')) ^ bool(d.get('theme_support_email')))
  for k in ('theme_documentation_url','theme_support_url'):
   u=urlparse(d[k]);self.assertEqual(u.scheme,'https');self.assertTrue(u.netloc)
 def test_shopify_locale(self):
  d=json.loads((S/'locales/en.default.json').read_text())
  keys=re.findall(r"'([^']+)'\s*\|\s*t\b",(S/'sections/not-found.liquid').read_text())
  self.assertEqual(len(keys),2)
  for key in keys:
   value=d
   for part in key.split('.'): value=value[part]
   self.assertTrue(isinstance(value,str) and value.strip())
 def test_wp_browser_fixture(self):
  from playwright.sync_api import sync_playwright
  css=(W/'style.css').read_text(encoding='utf-8')
  html='''<!doctype html><html lang="en"><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>'''+css+'''</style></head><body><main class="wrap"><div class="entry"><h1>Learning resource</h1><form class="comment-form"><p><label for="comment">Comment</label><textarea id="comment" name="comment" cols="45" rows="8"></textarea></p><p><label for="author">Name</label><input id="author" size="30"></p></form><div class="pagination"><nav class="navigation pagination"><div class="nav-links"><span class="page-numbers current">1</span><a class="page-numbers" href="#two">2</a><a class="next page-numbers" href="#next">Next</a></div></nav></div></div></main></body></html>'''
  with sync_playwright() as p:
   exe=os.environ.get('CHROME_EXECUTABLE') or shutil.which('chromium') or shutil.which('google-chrome')
   browser=p.chromium.launch(**({'executable_path':exe} if exe else {}),args=['--no-sandbox'])
   try:
    page=browser.new_page()
    for width in (320,375,768,1280):
     with self.subTest(width=width):
      page.set_viewport_size({'width':width,'height':900});page.set_content(html)
      self.assertLessEqual(page.evaluate('document.documentElement.scrollWidth'),width)
      self.assertLessEqual(page.locator('textarea').bounding_box()['width'],page.locator('.entry').bounding_box()['width']+.1)
      for target in page.locator('.page-numbers').all():
       b=target.bounding_box();self.assertGreaterEqual(b['width'],44);self.assertGreaterEqual(b['height'],44)
      page.locator('textarea').focus();self.assertGreaterEqual(float(page.locator('textarea').evaluate('(e)=>parseFloat(getComputedStyle(e).outlineWidth)')),3)
   finally: browser.close()
if __name__=='__main__':unittest.main(verbosity=2)
