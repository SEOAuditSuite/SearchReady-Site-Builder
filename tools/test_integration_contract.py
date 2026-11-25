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
  current=text('CURRENT-ACCEPTANCE.md').split('## Historical record',1)[0]
  readme=text('README.md').split('## Historical record',1)[0]
  self.assertIn('RELEASE-ready for public distribution of the instruction Skill',current)
  self.assertIn('RELEASE-ready for instruction Skill distribution',readme)
  self.assertIn('Shopify native storefront, Elementor/WooCommerce runtime',current)
  self.assertIn('Shopify storefront, Elementor/WooCommerce runtime, external tool execution and production launches are not verified.',readme)
  self.assertIn('No search ranking, WCAG or production certification.',readme)
 def test_no_vendored_beyondseo(self):
  self.assertFalse(any(p.name.lower()=='beyond-seo' for p in R.rglob('*')))
if __name__=='__main__': unittest.main(verbosity=2)
