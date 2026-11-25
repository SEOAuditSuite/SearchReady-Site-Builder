#!/usr/bin/env python3
"""Static integration contract tests; not an agent behavior or live CMS test."""
from pathlib import Path
import unittest
R=Path(__file__).resolve().parents[1]
def text(p): return (R/p).read_text(encoding='utf8')
class IntegrationContract(unittest.TestCase):
 def test_platform_routes(self):
  s=text('references/platform-and-implementation.md')
  for term in ['WordPress','Elementor','WooCommerce','Shopify','React/Next.js','canonical','test mode','BLOCKED']: self.assertIn(term,s)
 def test_platform_truth_boundary(self):
  self.assertIn('Do not describe an HTML demo as an installed WordPress theme or Shopify store',text('references/platform-and-implementation.md'))
 def test_optional_tools(self):
  s=text('references/seo-intelligence-and-audit.md')
  for term in ['Neither is bundled or required','explicit authorization','never invent search volume','Never assume that a skill file invokes a tool automatically']: self.assertIn(term,s)
 def test_workflow_coverage(self):
  s=text('SKILL.md')
  for term in ['A2. Search plan','references/seo-intelligence-and-audit.md','pre-delivery audit/fix verification']: self.assertIn(term,s)
 def test_ledger(self):
  s=text('templates/SEO-DECISION-LEDGER.md')
  for term in ['Evidence source/date/locale','Observed evidence','NOT RUN']: self.assertIn(term,s)
 def test_release_boundary(self):
  self.assertIn('HOLD',text('RELEASE-CHECKLIST.md').splitlines()[0]);self.assertIn('Shopify native preview remains BLOCKED',text('README.md'));self.assertIn('Elementor/WooCommerce runtime',text('README.md'))
 def test_no_vendored_beyondseo(self):
  self.assertFalse(any(p.name.lower()=='beyond-seo' for p in R.rglob('*')))
if __name__=='__main__': unittest.main(verbosity=2)
