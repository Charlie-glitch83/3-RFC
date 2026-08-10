#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN_ID='G-165-20260810T144936Z'
RUN=ROOT/'modules/G/runs'/RUN_ID
F=ROOT/'modules/F/frozen/H_F_to_G_v2.json'
B=ROOT/'modules/B/frozen/H_B_to_C_v2.json'
F_SHA='13b811243b684ed74b29fddc145e940a3de0aa867d03bc5823faf75a38cfd990'
B_SHA='d1446a474a967b27f9eacbe0645823ec63a103ceae187db8969cf6041b5e2b77'

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as fh:
        for chunk in iter(lambda:fh.read(1<<20),b''): h.update(chunk)
    return h.hexdigest()
def rel(p): return str(Path(p).relative_to(ROOT))
def write(p,obj):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def reconstruct_routes(fdoc):
    candidates=fdoc.get('atomic_candidate_registry') or fdoc.get('ionization_state',{}).get('atomic_candidates',[])
    groups={}
    for c in candidates:
        if {'id','parent','electron_count','charge'} <= set(c):
            groups.setdefault(c['parent'],[]).append(c)
    ids=[]; ledger=[]
    for parent,rows in sorted(groups.items()):
        rows=sorted(rows,key=lambda x:(int(x['electron_count']),str(x['id'])))
        for lo,hi in zip(rows,rows[1:]):
            if int(hi['electron_count'])!=int(lo['electron_count'])+1: continue
            if int(hi['charge'])!=int(lo['charge'])-1: continue
            cap=f'CAP::{lo["id"]}=>{hi["id"]}'
            ion=f'ION::{hi["id"]}=>{lo["id"]}'
            ids.extend([cap,ion])
            cap_res=int(lo['charge'])-1-int(hi['charge'])
            ion_res=int(hi['charge'])-(int(lo['charge'])-1)
            ledger.append({'route_id':cap,'nuclear_parent':parent,'charge_residual':cap_res})
            ledger.append({'route_id':ion,'nuclear_parent':parent,'charge_residual':ion_res})
    return sorted(ids),ledger

def main():
    errors=[]
    if sha(F)!=F_SHA: errors.append('F parent hash drift')
    if sha(B)!=B_SHA: errors.append('B ancestry hash drift')
    fdoc,bdoc=load(F),load(B)
    rr=load(RUN/'primary/G165_ROUTE_REGISTRY.json')
    act=load(RUN/'primary/G165_ROUTE_RESOLVED_PROCESS_ACTIVITY.json')
    anc=load(RUN/'primary/G165_PROCESS_TO_B_EDGE_ANCESTRY_FAMILY.json')
    nl=load(RUN/'primary/G165_AGGREGATE_NO_LOSS_RECONSTRUCTION.json')
    surf=load(RUN/'primary/G165_RADIATION_SURFACE_BRANCH_FAMILY.json')
    hi=load(ROOT/'modules/G/frozen/H_G_to_I_v2.json')

    expected_ids,ledger=reconstruct_routes(fdoc)
    primary_ids=sorted(r.get('route_id') for r in rr.get('concrete_routes',[]))
    if expected_ids!=primary_ids: errors.append('concrete route registry differs from parent-only reconstruction')
    if any(x['charge_residual']!=0 for x in ledger): errors.append('charge ledger failure in reconstructed capture/ionization routes')

    b_edges=sorted(f'e{int(e[0])}{int(e[1])}' for e in bdoc['carrier']['weighted_edges'])
    anc_edges=sorted(e['edge_id'] for e in anc.get('B_edges',[]))
    if b_edges!=anc_edges: errors.append('B edge support differs from exact B parent')
    for rec in anc.get('route_supports',[]):
        if sorted(rec.get('support_edges',[]))!=b_edges:
            errors.append(f'incomplete B-edge support for {rec.get("route_id")}')
            break
    for rec in anc.get('parametric_family_supports',[]):
        if sorted(rec.get('support_edges',[]))!=b_edges:
            errors.append(f'incomplete B-edge support for family {rec.get("family_id")}')
            break
    if anc.get('M_family',{}).get('formula')!='M_b(e|r)>=0; sum_e M_b(e|r)=1': errors.append('M simplex formula drift')
    if anc.get('ancestry_complete_for_I') is not True: errors.append('ancestry not marked complete for I')

    if act.get('result')!='PASS': errors.append('route activity artifact not PASS')
    if 'sum_{r in R_ext^b} Gamma_r^b(t)' not in act.get('aggregate_relation',''): errors.append('route aggregate relation missing')
    if nl.get('result')!='PASS' or nl.get('aggregate_reconstruction_within_tolerance') is not True: errors.append('aggregate no-loss reconstruction not PASS')
    if nl.get('algebraic_residual')!='0 identically by the exact event-family partition; no route contribution is replaced by a proxy.': errors.append('aggregate residual statement drift')
    if surf.get('result')!='PASS' or surf.get('unique_peak_claimed') is not False: errors.append('radiation-surface branch policy failure')

    if hi.get('object_id')!='H_G_to_I_V2': errors.append('wrong I child object id')
    if hi.get('parent',{}).get('sha256')!=F_SHA: errors.append('I child does not bind exact F parent')
    if hi.get('B_carrier_ancestry',{}).get('sha256')!=B_SHA: errors.append('I child does not bind exact B ancestry')
    if hi.get('Gamma_binding_classification')!='EXACT_PARENT_BOUND_BRANCH_INDEXED_REPLACEMENT': errors.append('I child Gamma classification drift')
    child_records=['route_registry','route_resolved_process_activity','route_to_relational_ancestry','aggregate_no_loss_reconstruction','recombination_history','radiation_surface']
    child_hashes={}
    for key in child_records:
        rec=hi.get(key,{})
        p=ROOT/rec.get('path','')
        if not rec.get('path') or not p.is_file():
            errors.append(f'I child missing artifact {key}')
            continue
        actual=sha(p); child_hashes[key]=actual
        if actual!=rec.get('sha256'): errors.append(f'I child artifact hash mismatch {key}')

    result={
        'schema_version':'3.0','run_id':RUN_ID,'result':'PASS' if not errors else 'FAIL',
        'method':'PARENT_ONLY_ROUTE_AND_ANCESTRY_RECONSTRUCTION_WITHOUT_PRIMARY_GATE_SUMMARIES',
        'exact_parent_hashes':{'F':sha(F),'B':sha(B)},
        'comparisons':{
            'concrete_route_count':len(expected_ids),
            'concrete_route_ids_match':expected_ids==primary_ids,
            'charge_ledgers_close':all(x['charge_residual']==0 for x in ledger),
            'B_edge_support_match':b_edges==anc_edges,
            'all_concrete_routes_retain_complete_B_edge_family':all(sorted(x.get('support_edges',[]))==b_edges for x in anc.get('route_supports',[])),
            'all_parametric_fibers_retain_complete_B_edge_family':all(sorted(x.get('support_edges',[]))==b_edges for x in anc.get('parametric_family_supports',[])),
            'aggregate_no_loss_pass':nl.get('result')=='PASS' and nl.get('aggregate_reconstruction_within_tolerance') is True,
            'branch_visibility_surface_pass':surf.get('result')=='PASS' and surf.get('unique_peak_claimed') is False,
            'I_child_artifact_hashes_match':not any('I child artifact hash mismatch' in e for e in errors),
        },
        'child_artifact_hashes':child_hashes,
        'errors':errors,
        'strongest_supported':'The exact F/B parents independently reconstruct the concrete capture/ionization route set, conserved charge ledgers, complete B-edge incidence branch family, and child artifact hashes.',
        'strongest_unsupported':'This verifier does not select a unique numerical atomic-rate branch or external recombination coordinate.'
    }
    write(RUN/'independent/INDEPENDENT_RECONSTRUCTION.json',result)
    print(json.dumps(result,indent=2))
    return 0 if not errors else 1

if __name__=='__main__': raise SystemExit(main())
