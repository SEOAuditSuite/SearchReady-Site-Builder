#!/usr/bin/env python3
"""Read-only source/release integrity check; ignores Git and local tool caches."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'MANIFEST.json').read_text(encoding='utf8'))
def excluded(p):
    return any(part in {'.git','__pycache__','.pytest_cache','.venv','node_modules'} for part in p.parts) or p.suffix in ('.pyc','.pyo')
real={str(p.relative_to(ROOT)).replace('\\','/'):p for p in ROOT.rglob('*') if p.is_file() and p!=ROOT/'MANIFEST.json' and not excluded(p.relative_to(ROOT))}
expected={x['path']:x for x in manifest['files']}
issues=[]
for path in sorted(set(real)|set(expected)):
    if path not in real:issues.append('missing: '+path)
    elif path not in expected:issues.append('unexpected: '+path)
    else:
        content=real[path].read_bytes()
        if len(content)!=expected[path]['size'] or hashlib.sha256(content).hexdigest()!=expected[path]['sha256']:
            issues.append('checksum: '+path)
if issues:
    print('FAIL manifest:',*issues,sep='\n - ')
    raise SystemExit(1)
print(f'PASS — {len(expected)} files match declared SHA256 and size')
