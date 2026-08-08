#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def validate_source_classes(run: Path):
    errors=[]; srcp=run/'SOURCE_REGISTER.json'
    if not srcp.exists(): return ['missing SOURCE_REGISTER.json']
    src=load(srcp); reg=load(ROOT/'memory/SOURCE_REGISTRY.json')
    classes={}
    for x in reg.get('sources',[]):
        if x.get('sha256') and x.get('classification'): classes.setdefault(x['sha256'],set()).add(x['classification'])
    for bucket in ('admitted_sources','procedure_only_sources','replay_required_sources','sources'):
        for rec in src.get(bucket,[]):
            digest=rec.get('sha256'); local=rec.get('classification')
            if digest in classes and local and local not in classes[digest]: errors.append(f"source classification drift {digest}: run-local {local} vs global {sorted(classes[digest])}")
    return errors
def evidence_path(run: Path, rel: str):
    a=(ROOT/rel).resolve()
    if a.exists() and (a==ROOT or ROOT in a.parents): return a
    b=(run/rel).resolve()
    if b.exists() and ROOT in b.parents: return b
    return None
def validate_required_outputs(run: Path):
    meta=load(run/'run.json'); mod=meta.get('module')
    modules=set(load(ROOT/'config/module_graph.json').get('module_order',[]))
    if mod not in modules: return []
    recipe=load(ROOT/'recipes'/mod/'recipe.json'); expected=recipe.get('required_outputs',[])
    p=run/'OUTPUT_COMPLETENESS.json'
    if not p.exists(): return ['PASS requires OUTPUT_COMPLETENESS.json']
    doc=load(p); errors=[]
    if doc.get('run_id')!=meta.get('run_id'): errors.append('OUTPUT_COMPLETENESS run_id mismatch')
    if doc.get('module')!=mod: errors.append('OUTPUT_COMPLETENESS module mismatch')
    if doc.get('overall')!='PASS': errors.append('OUTPUT_COMPLETENESS overall must be PASS')
    rows=doc.get('required_outputs',[]); by={r.get('requirement'):r for r in rows if isinstance(r,dict) and r.get('requirement')}
    if set(by)!=set(expected):
        missing=[x for x in expected if x not in by]; extra=[x for x in by if x not in expected]
        if missing: errors.append(f'missing required outputs: {missing}')
        if extra: errors.append(f'unexpected required outputs: {extra}')
    for req in expected:
        r=by.get(req)
        if not r: continue
        if r.get('status')!='PASS': errors.append(f'required output not PASS: {req}')
        if len(str(r.get('semantic_check','')).strip())<20: errors.append(f'missing substantive semantic_check: {req}')
        ev=r.get('evidence',[])
        if not isinstance(ev,list) or not ev: errors.append(f'no evidence for required output: {req}'); continue
        for item in ev:
            if isinstance(item,str): rel=item; declared=None
            elif isinstance(item,dict): rel=item.get('path'); declared=item.get('sha256')
            else: errors.append(f'invalid evidence record for {req}'); continue
            if not rel: errors.append(f'evidence path missing for {req}'); continue
            ep=evidence_path(run,rel)
            if ep is None or not ep.is_file(): errors.append(f'evidence file missing for {req}: {rel}'); continue
            if declared and sha(ep)!=declared: errors.append(f'evidence hash mismatch for {req}: {rel}')
    return errors
def validate(run: Path): return validate_source_classes(run)+validate_required_outputs(run)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--run',required=True); args=ap.parse_args(); run=(ROOT/args.run).resolve()
    if ROOT not in run.parents: raise SystemExit('run must be inside repository')
    errors=validate(run)
    if errors:
        print('SCIENTIFIC COMPLETION GUARD: FAIL')
        for e in errors: print('- '+e)
        return 1
    print('SCIENTIFIC COMPLETION GUARD: PASS')
    return 0
if __name__=='__main__': raise SystemExit(main())
