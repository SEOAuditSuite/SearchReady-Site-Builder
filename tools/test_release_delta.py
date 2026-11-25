#!/usr/bin/env python3
"""Stdlib-only tests for generated-evidence isolation (no browser execution)."""
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = (
    ('examples/pilot-02-cinderline/tools/test_dark_focus_contrast.py', '\ndef rgb(value):', 'pilot-02-cinderline'),
    ('examples/pilot-03-margin-atlas/tools/test_live_url_only.py', '\nPAGES=', 'pilot-03-margin-atlas'),
)


def config_only(path, marker, fake_path):
    """Exercise configuration statements only, never Playwright/HTTP tests."""
    header = path.read_text(encoding='utf-8').split(marker, 1)[0]
    for unused in ('from playwright.sync_api import sync_playwright',
                   'from playwright._impl._errors import Error as PlaywrightError'):
        header = header.replace(unused, '')
    ns = {'__file__': str(fake_path)}
    exec(compile(header, str(path), 'exec'), ns)
    return ns['EVIDENCE']


class EvidenceOutputContract(TestCase):
    def test_default_results_outside_release(self):
        with tempfile.TemporaryDirectory(prefix='searchready-evidence-') as folder:
            package = Path(folder) / 'extracted-release'
            for name, marker, pilot in SCRIPTS:
                fake = package / name
                fake.parent.mkdir(parents=True, exist_ok=True)
                import os
                with patch.dict(os.environ, {}, clear=True):
                    result = config_only(ROOT / name, marker, fake)
                self.assertEqual(result, package.parent / (package.name+'-review-evidence') / pilot)
                self.assertFalse(result.is_relative_to(package))

    def test_rejects_output_inside_release(self):
        with tempfile.TemporaryDirectory(prefix='searchready-evidence-') as folder:
            package = Path(folder) / 'extracted-release'
            for name, marker, pilot in SCRIPTS:
                fake = package / name
                fake.parent.mkdir(parents=True, exist_ok=True)
                with patch.dict('os.environ', {'SEARCHREADY_REVIEW_OUTPUT': str(package / 'evidence')}):
                    with self.assertRaises(SystemExit):
                        config_only(ROOT / name, marker, fake)


if __name__ == '__main__':
    main(verbosity=2)
