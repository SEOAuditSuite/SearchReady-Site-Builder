#!/usr/bin/env python3
"""Real loopback HTTP transport checks, separate from browser navigation."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json,threading
from urllib.request import urlopen
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'pilot'/'site'; EVIDENCE=ROOT/'pilot'/'evidence'
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw): super().__init__(*a,directory=str(SITE),**kw)
 def log_message(self,*a):pass
with ThreadingHTTPServer(('127.0.0.1',0),Handler) as server:
 thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
 base=f'http://127.0.0.1:{server.server_port}'
 paths=['/','/index.html','/services.html','/process.html','/contact.html','/assets/site.css','/assets/site.js','/assets/mark.svg','/assets/hero-art.svg']
 result={'type':'real local HTTP transport; no browser navigation','checked':len(paths),'passed':0,'failed':0,'details':[]}
 try:
  for path in paths:
   try:
    with urlopen(base+path,timeout=5) as response:
     content=response.read()
     good=response.status==200 and len(content)>100
     result['details'].append({'path':path,'status':response.status,'length':len(content),'pass':good})
     result['passed']+=int(good);result['failed']+=int(not good)
   except Exception as e:
    result['failed']+=1;result['details'].append({'path':path,'error':repr(e),'pass':False})
 finally: server.shutdown();thread.join(timeout=5)
EVIDENCE.mkdir(exist_ok=True)
(EVIDENCE/'http-results.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!='details'},indent=2))
raise SystemExit(int(result['failed']>0))
