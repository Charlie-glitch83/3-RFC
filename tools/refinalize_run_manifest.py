#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def now(): return datetime.now(timezone.utc).isoformat()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def save(p,o): Path(p).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def tree_entries(path:Path):
    out=[]
    for p in sorted(path.rglob('*')):
        if not p.is_file(): continue
        rel=p.relative_to(ROOT)
        if any(part in {'.git','__pycache__','runtime_cache','scratch'} for part in rel.parts): continue
        out.append({'path':str(rel),'sha256':sha(p),'bytes':p.stat().st_size})
    return out

def tree_sha(path:Path):
    h=hashlib.sha256()
    for x in tree_entries(path):
        h.update(x['path'].encode()); h.update(b'\0'); h.update(x['sha256'].encode()); h.update(b'\n')
    return h.hexdigest()

def finalize_manifest(run:Path):
    mp=run/'GENERATED_OUTPUT_MANIFEST.json'; rows=[]
    for p in sorted(run.rglob('*')):
        if not p.is_file() or p==mp or p.name=='run.json': continue
        rel=p.relative_to(run)
        if any(part in {'__pycache__','runtime_cache','scratch'} for part in rel.parts): continue
        rows.append({'path':str(rel),'sha256':sha(p),'bytes':p.stat().st_size})
    h=hashlib.sha256()
    for r in rows:
        h.update(r['path'].encode()); h.update(b'\0'); h.update(r['sha256'].encode()); h.update(b'\n')
    save(mp,{'run_id':load(run/'run.json')['run_id'],'status':'FINAL','finalized_utc':now(),'outputs':rows,'tree_sha256':h.hexdigest(),'note':'Finalized after all scientific/evidence files stopped changing; excludes itself and controller-owned run.json.'})
    return mp

def reconcile_closed_registration(run:Path):
    r=load(run/'run.json')
    if r.get('status') not in {'PASS','BLOCKED','FAIL'}: return {'closed':False}
    digest=tree_sha(run); rid=r['run_id']
    idxp=ROOT/'memory/RUN_INDEX.json'; idx=load(idxp); matches=[x for x in idx.get('runs',[]) if x.get('run_id')==rid]
    if len(matches)!=1: raise SystemExit(f'HARD STOP: run index resolution for {rid} = {len(matches)}')
    matches[0]['tree_sha256']=digest; save(idxp,idx)
    regp=ROOT/'memory/ARTIFACT_REGISTRY.json'; reg=load(regp); found=False
    for x in reg.get('artifacts',[]):
        if x.get('kind')=='RUN_BUNDLE' and x.get('run_id')==rid:
            x['sha256']=digest; x['created_utc']=now(); found=True
    if not found:
        reg.setdefault('artifacts',[]).append({'path':str(run.relative_to(ROOT)),'sha256':digest,'kind':'RUN_BUNDLE','created_utc':now(),'work_unit':r.get('task_id'),'run_id':rid})
    save(regp,reg)
    return {'closed':True,'run_tree_sha256':digest}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--run',required=True); ap.add_argument('--reconcile-closed-registration',action='store_true'); a=ap.parse_args()
    run=(ROOT/a.run).resolve()
    if ROOT not in run.parents or not (run/'run.json').is_file(): raise SystemExit('HARD STOP: invalid repository run path')
    mp=finalize_manifest(run); out={'status':'PASS','manifest':str(mp.relative_to(ROOT)),'manifest_sha256':sha(mp)}
    if a.reconcile_closed_registration: out.update(reconcile_closed_registration(run))
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
