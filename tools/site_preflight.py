#!/usr/bin/env python3
"""Read-only offline HTML SEO preflight. Not a crawler, browser or WCAG verifier."""
from __future__ import annotations
import argparse
import json
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
from xml.etree import ElementTree as ET

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = ''
        self.titles = []
        self.descriptions = []
        self.robots = []
        self.viewport = False
        self.canonicals = []
        self.h1 = 0
        self.ids = set()
        self.links = []
        self.assets = []
        self.images_without_alt = 0
        self.jsonld = []
        self.inside_title = False
        self.inside_script_jsonld = False
        self.cur_title = ''
        self.cur_script = ''

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == 'html': self.lang = d.get('lang','') or ''
        if d.get('id'): self.ids.add(d['id'])
        if tag == 'title': self.inside_title = True; self.cur_title = ''
        if tag == 'meta':
            name = (d.get('name') or '').lower()
            if name == 'description': self.descriptions.append(d.get('content') or '')
            if name == 'robots': self.robots.append(d.get('content') or '')
            if name == 'viewport': self.viewport = bool(d.get('content'))
        if tag == 'link' and 'canonical' in (d.get('rel') or '').lower().split(): self.canonicals.append(d.get('href') or '')
        if tag == 'h1': self.h1 += 1
        if tag == 'a' and d.get('href') is not None: self.links.append(d['href'])
        if tag in ('img','script') and d.get('src'): self.assets.append(d['src'])
        if tag in ('link',) and d.get('href') and 'stylesheet' in (d.get('rel') or '').lower(): self.assets.append(d['href'])
        if tag == 'img' and 'alt' not in d: self.images_without_alt += 1
        if tag == 'script' and (d.get('type') or '').lower() == 'application/ld+json':
            self.inside_script_jsonld = True; self.cur_script = ''

    def handle_data(self, data):
        if self.inside_title: self.cur_title += data
        if self.inside_script_jsonld: self.cur_script += data

    def handle_endtag(self, tag):
        if tag == 'title' and self.inside_title:
            self.titles.append(self.cur_title.strip()); self.inside_title = False
        if tag == 'script' and self.inside_script_jsonld:
            self.jsonld.append(self.cur_script); self.inside_script_jsonld = False


def resolve_local(root: Path, current: Path, uri: str) -> tuple[Path, str] | None:
    u = urlsplit(uri)
    if u.scheme or u.netloc or uri.startswith('//') or not u.path and not u.fragment: return None
    if u.path.startswith('/'): target = root / unquote(u.path).lstrip('/')
    elif u.path: target = current.parent / unquote(u.path)
    else: target = current
    if u.path.endswith('/') or not u.path:  # / or fragment-only
        if u.path.endswith('/'): target = target / 'index.html'
    target = target.resolve()
    if not target.is_relative_to(root.resolve()): return target, u.fragment
    if target.is_dir(): target /= 'index.html'
    return target, u.fragment


def inspect(root: Path, mode: str = 'staging', domain: str | None = None) -> dict:
    root = root.resolve()
    if mode not in ('staging','production'): raise ValueError('mode must be staging or production')
    pages = sorted(root.rglob('*.html')) if root.exists() else []
    errors, warnings = [], []
    parsed = {}
    if not pages: errors.append('No HTML pages found')
    for f in pages:
        rel = f.relative_to(root).as_posix()
        p = PageParser()
        try: p.feed(f.read_text(encoding='utf-8'))
        except (UnicodeDecodeError, OSError, ValueError) as e:
            errors.append(f'{rel}: cannot parse HTML ({e})'); continue
        parsed[f] = p
        if not p.lang.strip(): errors.append(f'{rel}: missing html lang')
        if len(p.titles)!=1 or not p.titles[0]: errors.append(f'{rel}: missing or repeated nonempty title')
        if len(p.descriptions)!=1 or not p.descriptions[0].strip(): errors.append(f'{rel}: missing or repeated nonempty meta description')
        if p.h1 < 1: errors.append(f'{rel}: missing H1')
        if not p.viewport: errors.append(f'{rel}: missing viewport')
        if p.images_without_alt: errors.append(f'{rel}: {p.images_without_alt} img elements lack alt attribute')
        if len(p.canonicals)>1: errors.append(f'{rel}: multiple canonical tags')
        index_off = any('noindex' in value.lower() for value in p.robots)
        if mode=='staging' and not index_off: errors.append(f'{rel}: staging page missing noindex')
        if mode=='production':
            if index_off: errors.append(f'{rel}: production page has noindex')
            if len(p.canonicals)!=1: errors.append(f'{rel}: missing unique production canonical')
            elif not p.canonicals[0].startswith('https://'): errors.append(f'{rel}: production canonical must use HTTPS absolute URL')
            elif domain and urlsplit(p.canonicals[0]).netloc != urlsplit(domain).netloc: errors.append(f'{rel}: canonical host disagrees with production domain')
            elif any(x in p.canonicals[0] for x in ('example.com','localhost','127.0.0.1')): errors.append(f'{rel}: canonical uses placeholder/local domain')
        else:
            if p.canonicals: warnings.append(f'{rel}: staging canonical needs production-domain review')
        for raw in p.jsonld:
            try:
                ld = json.loads(raw)
                if not isinstance(ld,(list,dict)): raise ValueError('JSON-LD top level must be object/list')
            except (json.JSONDecodeError,ValueError): errors.append(f'{rel}: invalid JSON-LD')
        for uri in p.assets:
            resolved=resolve_local(root,f,uri)
            if resolved is not None and not resolved[0].exists(): errors.append(f'{rel}: missing local asset {uri}')
    for f,p in parsed.items():
        rel=f.relative_to(root).as_posix()
        for link in p.links:
            found=resolve_local(root,f,link)
            if found is None: continue
            target, fragment=found
            if not target.is_relative_to(root): errors.append(f'{rel}: internal link escapes site root: {link}'); continue
            if not target.is_file(): errors.append(f'{rel}: broken internal link: {link}'); continue
            if fragment and target in parsed and unquote(fragment) not in parsed[target].ids:
                errors.append(f'{rel}: missing anchor target: {link}')
    title_counts=Counter(p.titles[0] for p in parsed.values() if len(p.titles)==1 and p.titles[0])
    for title,count in title_counts.items():
        if count>1: errors.append(f'duplicate title across {count} pages: {title}')
    if mode=='production':
        if not domain or not domain.startswith('https://') or not urlsplit(domain).netloc: errors.append('Production requires verified HTTPS base domain')
        if not (root/'robots.txt').is_file(): errors.append('Production missing robots.txt')
        sf=root/'sitemap.xml'
        if not sf.is_file(): errors.append('Production missing sitemap.xml')
        else:
            try: ET.parse(sf)
            except ET.ParseError: errors.append('Production sitemap XML invalid')
        warnings.append('Static source preflight cannot verify served HTTP status, X-Robots-Tag, redirects, live forms or indexation')
    else: warnings.append('Staging source preflight: HTTP/browser and production-domain checks are separate')
    return {'mode':mode,'root':str(root),'pages':len(parsed),'errors':errors,'warnings':warnings,'status':'PASS' if not errors else 'FAIL'}


def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('root',type=Path)
    ap.add_argument('--mode',choices=('staging','production'),default='staging')
    ap.add_argument('--domain',help='Owner-verified production base URL, e.g. https://yourdomain.com')
    ap.add_argument('--json-out',type=Path)
    args=ap.parse_args()
    result=inspect(args.root,args.mode,args.domain)
    print(f"{result['status']}: {result['pages']} pages, {len(result['errors'])} errors, {len(result['warnings'])} notes")
    for x in result['errors']: print('ERROR:',x)
    for x in result['warnings']: print('INFO:',x)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True,exist_ok=True)
        args.json_out.write_text(json.dumps(result,indent=2),encoding='utf-8')
    return 0 if result['status']=='PASS' else 1
if __name__=='__main__': raise SystemExit(main())
