#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RID='G-165-20260810T144936Z'
R=ROOT/'modules/G/runs'/RID
MAN=R/'GENERATED_OUTPUT_MANIFEST.json'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for c in iter(lambda:f.read(1<<20),b''): h.update(c)
 return h.hexdigest()
exclude={'GENERATED_OUTPUT_MANIFEST.json'}
outputs=[]
for p in sorted(R.rglob('*')):
 if not p.is_file() or p.name in exclude: continue
 if any(x in p.parts for x in ('runtime_cache','scratch','__pycache__')): continue
 outputs.append({'path':str(p.relative_to(R)),'sha256':sha(p),'bytes':p.stat().st_size})
if not outputs: raise SystemExit('no generated outputs to finalize')
record={'run_id':RID,'status':'FINAL','finalized_utc':datetime.now(timezone.utc).isoformat(),'outputs':outputs}
MAN.write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({'run_id':RID,'status':'FINAL','output_count':len(outputs)},indent=2))
