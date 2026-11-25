#!/usr/bin/env python3
"""Narrow D5 regression: computed focus outline vs adjacent dark surfaces.

Uses actual extracted HTML/CSS in a local DOM, without HTTP or the older test suites.
Tests dark CTA and footer backgrounds at desktop and mobile widths.
Does not constitute a full WCAG audit or real URL-navigation acceptance.
"""
from pathlib import Path
import json, os, re, shutil, sys
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT.parent.parent
# Reviewer-generated screenshots/results must never modify the release tree or its manifests.
PACKAGE_ROOT = ROOT.parent.parent
_evidence_base = Path(os.environ.get(
    'SEARCHREADY_REVIEW_OUTPUT',
    str(PACKAGE_ROOT.parent / (PACKAGE_ROOT.name + '-review-evidence')),
)).expanduser().resolve()
if _evidence_base == PACKAGE_ROOT or PACKAGE_ROOT in _evidence_base.parents:
    raise SystemExit('SEARCHREADY_REVIEW_OUTPUT must be outside the extracted release directory')
EVIDENCE = _evidence_base / 'pilot-02-cinderline'
EVIDENCE.mkdir(parents=True, exist_ok=True)

def rgb(value):
    parts = re.findall(r'[\d.]+', value)
    return tuple(int(float(x)) for x in parts[:3])

def luminance(color):
    r, g, b = color
    comps = [c / 255 for c in (r, g, b)]
    comps = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in comps]
    return sum(a * b for a, b in zip(comps, (.2126, .7152, .0722)))

def contrast(a, b):
    x, y = sorted((luminance(a), luminance(b)))
    return (y + .05) / (x + .05)

checks = []
try:
    with sync_playwright() as play:
        chromium = shutil.which('chromium')
        browser = play.chromium.launch(headless=True, args=['--no-sandbox'], **({'executable_path': chromium} if chromium else {'channel': 'chrome'}))
        try:
            scenarios = [
                ('pilot01-cta', SKILL / 'pilot', '.cta-band a', '.cta-band'),
                ('pilot01-footer', SKILL / 'pilot', '.footer a', '.footer'),
                ('pilot02-closing', ROOT, '.closing a', '.closing'),
            ]
            for width in (375, 1440):
                for label, folder, link_sel, backdrop_sel in scenarios:
                    page = browser.new_page(viewport={'width': width, 'height': 900})
                    page.set_content((folder / 'site/index.html').read_text(encoding='utf-8'))
                    page.add_style_tag(content=(folder / 'site/assets/site.css').read_text(encoding='utf-8'))
                    link = page.locator(link_sel).first
                    link.focus()
                    observed = link.evaluate('''(el) => ({
                        outline: getComputedStyle(el).outlineColor,
                        width: getComputedStyle(el).outlineWidth,
                        offset: getComputedStyle(el).outlineOffset,
                        focused: document.activeElement === el,
                    })''')
                    backdrop = page.locator(backdrop_sel).first.evaluate('(el) => getComputedStyle(el).backgroundColor')
                    ratio = contrast(rgb(observed['outline']), rgb(backdrop))
                    passed = observed['focused'] and float(observed['width'].replace('px', '')) >= 2 and ratio >= 3
                    record = {
                        'name': f'{label} {width}px keyboard focus vs dark surface',
                        'status': 'PASS' if passed else 'FAIL',
                        'outline': observed['outline'], 'background': backdrop,
                        'contrast_ratio': round(ratio, 2), 'required_ratio': 3.0,
                        'focused': observed['focused'], 'outline_width': observed['width'],
                        'outline_offset': observed['offset'],
                    }
                    checks.append(record)
                    if width == 375:
                        link.scroll_into_view_if_needed()
                        page.screenshot(path=str(EVIDENCE / (label + '-focus-375.png')))
                    page.close()
        finally:
            browser.close()
except Exception as exc:
    checks.append({'name': 'browser availability', 'status': 'BLOCKED', 'reason': type(exc).__name__ + ': ' + str(exc)[:400]})

counts = {s: sum(x['status'] == s for x in checks) for s in ('PASS', 'FAIL', 'BLOCKED')}
report = {
    'scope': 'D5 dark-surface focus contrast only: DOM-render test, not live URL navigation',
    'rule': 'WCAG 1.4.11 contrast ratio >= 3:1 for visible non-text focus indicator',
    'counts': counts, 'checks': checks,
}
(EVIDENCE / 'dark-focus-results.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print('Review evidence:', EVIDENCE)
print(json.dumps({'counts': counts, 'samples': [(x['name'], x.get('contrast_ratio')) for x in checks]}, indent=2))
raise SystemExit(2 if counts['BLOCKED'] else (1 if counts['FAIL'] else 0))
