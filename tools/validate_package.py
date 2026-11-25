#!/usr/bin/env python3
"""Focused consistency checks for the SearchReady candidate package, no third-party dependencies."""
from pathlib import Path
import re
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
EXPECTED_REFS={
 'goal-and-scope.md','brand-and-visual-design.md','content-and-information-architecture.md',
 'ux-accessibility.md','technical-seo-and-indexability.md','structured-data-and-local-seo.md',
 'performance-and-cwv.md','security-privacy-and-forms.md','platform-and-implementation.md',
 'verification-and-release-gates.md','recovery-and-delivery.md','official-standards.md','seo-intelligence-and-audit.md'
}
class PackageChecks(unittest.TestCase):
 def test_main_skill_header(self):
  s=(ROOT/'SKILL.md').read_text(encoding='utf8')
  self.assertTrue(s.startswith('---\nname: searchready-site-builder\n'))
  self.assertIn('description:',s[:900])
 def test_references_present_and_resolved(self):
  s=(ROOT/'SKILL.md').read_text(encoding='utf8')
  refs=set(re.findall(r'references/([a-z0-9-]+\.md)',s))
  self.assertEqual(refs,EXPECTED_REFS)
  self.assertEqual({p.name for p in (ROOT/'references').glob('*.md')},EXPECTED_REFS)
 def test_consolidated_reference_contains_all(self):
  s=(ROOT/'SEARCHREADY-REFERENCE-GUIDE.md').read_text(encoding='utf8')
  for x in EXPECTED_REFS:
   self.assertIn('## Reference: '+x+'\n\n'+(ROOT/'references'/x).read_text(encoding='utf8').rstrip(),s)
 def test_project_setup_guides(self):
  guide=(ROOT/'INSTALL-AND-USE-INSTRUCTIONS.md').read_text(encoding='utf8')
  for name in ('SKILL.md','SEARCHREADY-REFERENCE-GUIDE.md','PROJECT-INSTRUCTIONS.txt'): self.assertIn(name,guide)
  self.assertIn('Project',guide);self.assertIn('Native',guide)
 def test_pilot_pages_present(self):
  for name in ('index.html','services.html','process.html','contact.html'):
   self.assertTrue((ROOT/'pilot'/'site'/name).is_file())
 def test_no_pretend_prod_claim(self):
  s=(ROOT/'SKILL.md').read_text(encoding='utf8').lower()
  self.assertIn('never promise search rankings',s)
  self.assertIn('production blocked',s)
 def test_editorial_example_and_checklist(self):
  p=ROOT/'examples'/'pilot-03-margin-atlas'
  self.assertTrue((p/'build.py').is_file())
  for name in ('index.html','journal.html','about.html','the-art-of-noticing.html','a-bench-is-a-small-promise.html'):
   self.assertTrue((p/'site'/name).is_file())
  self.assertTrue((ROOT/'templates'/'CONTENT-PUBLICATION-CHECKLIST.md').is_file())
  self.assertIn('Editorial and content-publication websites',(ROOT/'SKILL.md').read_text(encoding='utf8'))
 def test_licenses(self): self.assertTrue((ROOT/'LICENSE').is_file())

if __name__=='__main__':unittest.main(verbosity=2)
