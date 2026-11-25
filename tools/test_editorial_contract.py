#!/usr/bin/env python3
"""Dependency-free regressions only for the new editorial example's contract."""
from pathlib import Path
import tempfile, shutil, subprocess, unittest, re, ast
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
PILOT=ROOT/'examples'/'pilot-03-margin-atlas'
SITE=PILOT/'site'

class ArticleText(HTMLParser):
 def __init__(self):
  super().__init__(); self.depth=0; self.parts=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='article' and 'article-body' in d.get('class','').split(): self.depth+=1
  elif self.depth and tag=='article':self.depth+=1
 def handle_endtag(self,tag):
  if tag=='article' and self.depth:self.depth-=1
 def handle_data(self,data):
  if self.depth:self.parts.append(data)

class EditorialContract(unittest.TestCase):
 def test_article_reading_time_is_credible(self):
  for name in ('the-art-of-noticing.html','a-bench-is-a-small-promise.html'):
   with self.subTest(name=name):
    html=(SITE/name).read_text(encoding='utf-8')
    words=ArticleText();words.feed(html)
    count=len(' '.join(words.parts).split())
    self.assertGreater(count,175)
    self.assertLess(count,451)
    self.assertIn('2 MIN READ',html)
 def test_listing_hierarchy(self):
  html=(SITE/'journal.html').read_text(encoding='utf-8')
  self.assertIn('<h2 class="sr-only">Journal articles</h2>',html)
  self.assertEqual(html.count('2 MIN READ'),2)
 def test_five_staging_routes(self):
  pages=sorted(p.name for p in SITE.glob('*.html'))
  self.assertEqual(pages,sorted(['index.html','journal.html','about.html','the-art-of-noticing.html','a-bench-is-a-small-promise.html']))
  for name in pages:
   html=(SITE/name).read_text(encoding='utf-8')
   self.assertIn('<meta name="robots" content="noindex, nofollow">',html)
   self.assertNotIn('rel="canonical"',html)
 def test_microcopy_size_correction(self):
  css=(SITE/'assets/site.css').read_text(encoding='utf-8')
  self.assertIn('.art-bottom{font-size:11px}',css)
  self.assertRegex(css,r'\.footer-bottom\{[^{}]*font-size:11px')
 def test_generator_explicit_lf_on_all_files(self):
  """Keep generator byte-stable when executed on Windows or Unix."""
  tree=ast.parse((PILOT/'build.py').read_text(encoding='utf-8'))
  calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='write_text']
  self.assertEqual(len(calls),5)
  for call in calls:
   with self.subTest(lineno=call.lineno):
    values={kw.arg:kw.value for kw in call.keywords}
    self.assertIn('newline',values)
    self.assertIsInstance(values['newline'],ast.Constant)
    self.assertEqual(values['newline'].value,'\n')
 def test_generator_reproduces_source_without_mutating_release(self):
  with tempfile.TemporaryDirectory(prefix='editorial-contract-') as t:
   dest=Path(t);shutil.copy2(PILOT/'build.py',dest/'build.py')
   subprocess.run(['python',str(dest/'build.py')],cwd=str(dest),check=True,capture_output=True)
   generated=dest/'site'
   original={str(p.relative_to(SITE)):p.read_bytes() for p in SITE.rglob('*') if p.is_file()}
   other={str(p.relative_to(generated)):p.read_bytes() for p in generated.rglob('*') if p.is_file()}
   self.assertEqual(original,other)

if __name__=='__main__':unittest.main(verbosity=2)
