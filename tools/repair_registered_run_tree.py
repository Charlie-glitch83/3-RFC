#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def sha256_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def tree_entries(path:Path):
    rows=[]
    for p in sorted(path.rglob('*')):
        if not p.is_file(): continue
        rel=p.relative_to(ROOT)
        if any(part in {'.git','__pycache__','runtime_cache','scratch'} for part in rel.parts): continue
        rows.append({'path':str(rel),'sha256':sha256_file(p),'bytes':p.stat().st_size})
    return rows

def tree_sha(path:Path)->str:
    h=hashlib.sha256()
    for row in tree_entries(path):
        h.update(row['path'].encode()); h.update(b'\0'); h.update(row['sha256'].encode()); h.update(b'\n')
    return h.hexdigest()

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def save(p,obj): Path(p).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--run-id',required=True); ap.add_argument('--record'); args=ap.parse_args()
    reg_path=ROOT/'memory/ARTIFACT_REGISTRY.json'; reg=load(reg_path)
    matches=[x for x in reg.get('artifacts',[]) if x.get('kind')=='RUN_BUNDLE' and x.get('run_id')==args.run_id]
    if len(matches)!=1: raise SystemExit('HARD STOP: run registry record does not resolve exactly once')
    rec=matches[0]; run=ROOT/rec['path']; run_json=load(run/'run.json')
    if run_json.get('status')!='PASS': raise SystemExit('HARD STOP: only closed PASS runs may receive administrative tree-registry repair')
    manifest=load(run/'GENERATED_OUTPUT_MANIFEST.json')
    if manifest.get('status')!='FINAL' or not manifest.get('outputs'): raise SystemExit('HARD STOP: FINAL generated-output manifest required')
    verified=[]
    for item in manifest['outputs']:
        p=ROOT/item['path']
        if not p.exists() or not p.is_file(): raise SystemExit(f"HARD STOP: manifested output missing: {item['path']}")
        actual=sha256_file(p)
        if actual!=item['sha256']: raise SystemExit(f"HARD STOP: manifested output hash mismatch: {item['path']}")
        verified.append(item['path'])
    old=rec['sha256']; current=tree_sha(run)
    if old!=current:
        rec['sha256']=current
        save(reg_path,reg)
    repair={'schema_version':'1.0','repair_type':'ADMINISTRATIVE_RUN_TREE_REGISTRY_REFRESH','run_id':args.run_id,'run_path':rec['path'],'old_registered_tree_sha256':old,'current_verified_tree_sha256':current,'changed':old!=current,'manifest_status':'FINAL','manifested_outputs_verified':len(verified),'scientific_output_bytes_changed':False,'scope':'Registry metadata only; no run scientific/evidence file is modified by this tool.','timestamp_utc':datetime.now(timezone.utc).isoformat()}
    if args.record:
        out=ROOT/args.record; out.parent.mkdir(parents=True,exist_ok=True); save(out,repair)
    print(json.dumps(repair,indent=2))

if __name__=='__main__': main()
