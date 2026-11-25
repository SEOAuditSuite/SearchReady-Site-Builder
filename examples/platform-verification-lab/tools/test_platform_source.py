#!/usr/bin/env python3
"""Focused checks for native theme source. Not WordPress or Shopify runtime tests."""
from pathlib import Path
import json,re,shutil,subprocess,unittest
R=Path(__file__).resolve().parents[1]
W=R/'wordpress/fieldnote-learning'; S=R/'shopify/paper-spark'
def read(p): return p.read_text(encoding='utf8')
class PlatformSource(unittest.TestCase):
 def test_wp_php_syntax(self):
  if not shutil.which('php'): self.skipTest('PHP unavailable')
  for p in W.glob('*.php'):
   with self.subTest(file=p.name):
    r=subprocess.run(['php','-l',str(p)],capture_output=True,text=True); self.assertEqual(r.returncode,0,r.stderr)
 def test_wp_native_hooks(self):
  for p in ['index.php','page.php','single.php','search.php','404.php','comments.php','style.css','functions.php','header.php','footer.php']: self.assertTrue((W/p).is_file())
  for hook in ['wp_head()','wp_body_open()','language_attributes()','body_class()']: self.assertIn(hook,read(W/'header.php'))
  self.assertIn('wp_footer()',read(W/'footer.php'))
  for hook in ["add_theme_support('title-tag')","register_nav_menus(","wp_enqueue_style("]: self.assertIn(hook,read(W/'functions.php'))
 def test_wp_seo_ownership_and_real_content(self):
  src='\n'.join(read(p) for p in W.glob('*.php'))
  self.assertNotIn('<title>',src); self.assertNotIn('rel="canonical"',src); self.assertNotIn('application/ld+json',src)
  for k in ['the_post()','the_content()','get_permalink()','the_posts_pagination()','get_search_form()']: self.assertIn(k,src)
 def test_wp_route_templates(self):
  for p in ['index.php','single.php','page.php','search.php','404.php']:
   s=read(W/p);self.assertEqual(s.count('<h1>'),1);self.assertIn('get_header()',s);self.assertIn('get_footer()',s)
 def test_shopify_layout_contract(self):
  s=read(S/'layout/theme.liquid')
  for k in ['content_for_header','content_for_layout','page_title','page_description','canonical_url','asset_url','routes.cart_url']:self.assertIn(k,s)
  self.assertEqual(s.count('rel="canonical"'),1);self.assertEqual(s.count('<title>'),1)
 def test_shopify_json_templates_and_schema(self):
  for p in (S/'templates').glob('*.json'):
   with self.subTest(template=p.name):
    d=json.loads(read(p));self.assertEqual(set(d['order']),set(d['sections']));
    for sec in d['sections'].values():
     path=S/'sections'/f"{sec['type']}.liquid";self.assertTrue(path.is_file());schema=json.loads(re.search(r'{% schema %}(.*?){% endschema %}',read(path),re.S).group(1)); self.assertTrue(schema['name']); ids=[x['id'] for x in schema['settings']]; self.assertEqual(len(ids),len(set(ids)))
  for p in (S/'config').glob('*.json'):json.loads(read(p))
 def test_shopify_native_commerce(self):
  s=read(S/'sections/product-main.liquid');c=read(S/'sections/cart-main.liquid')
  for k in ["form 'product', product",'name="id"','variant.id','variant.available','variant.price | money','selected_or_first_available_variant']:self.assertIn(k,s)
  for k in ['routes.cart_url','cart.items','name="updates[]"','name="checkout"','cart.total_price | money']:self.assertIn(k,c)
  self.assertNotIn('application/ld+json',s) # Deliberately not claiming product rich results yet.
 def test_shopify_assets_and_references(self):
  src='\n'.join(read(p) for p in S.rglob('*.liquid'))
  for a in re.findall(r"'([^']+)'\s*\|\s*asset_url",src): self.assertTrue((S/'assets'/a).is_file())
  for sn in re.findall(r"{%\s*render\s+'([^']+)'",src):self.assertTrue((S/'snippets'/f'{sn}.liquid').is_file())
  self.assertNotIn('innerHTML',read(S/'assets/variants.js'));self.assertNotIn('http://',src)
 def test_shopify_js_syntax(self):
  if not shutil.which('node'): self.skipTest('Node unavailable')
  r=subprocess.run(['node','--check',str(S/'assets/variants.js')],capture_output=True,text=True);self.assertEqual(r.returncode,0,r.stderr)
if __name__=='__main__':unittest.main(verbosity=2)
