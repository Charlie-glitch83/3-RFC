#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[4]; RUN=Path(__file__).resolve().parent
PARENT=ROOT/'modules/A/frozen/H_A_to_B.json'; PARENT_SHA='728caf8c049d0114caef6f7b36af00065a32b4dc5f4faad02c6b9bcb16c933e7'; TOL=1e-11

def dig(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def dump(rel,obj):
 p=RUN/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); return p
if dig(PARENT)!=PARENT_SHA: raise SystemExit('parent hash mismatch')
parent=load(PARENT); primary=load(RUN/'primary/BIG_IMPLOSION_PHYSICAL_STATE.json')
x=np.array(parent['recursive_kernel']['executed_state']['kernel_state'],float); delta=float(parent['recursive_kernel']['executed_state']['delta']); n=3
one=np.ones(n); mean=float(np.mean(x)); q=float((delta-1)/(delta-1+n))
y=mean*one + q*(x-mean*one)
ym=float(np.mean(y)); reopened=ym*one + (1.0/q)*(y-ym*one)
curr=[]; div=np.zeros(n)
for i in range(n):
 for j in range(i+1,n):
  v=float((y[i]-y[j])/(delta-1)); curr.append({'i':i,'j':j,'J_ij':v}); div[i]+=v; div[j]-=v
py=np.array(primary['state']['post_event_physical_state'],float); pres=np.array(primary['pregeometry']['compression_relic_ledger_residual'],float)
rec={
 'run_id':'B-110-20260807T002248Z','method':'ANALYTIC_K3_SPECTRAL_RECONSTRUCTION_WITHOUT_PRIMARY_MATRIX_INVERSE','parent_sha256':PARENT_SHA,
 'analytic':{'constant_eigenvalue':1.0,'nonconstant_eigenvalue_q':q,'multiplicity_nonconstant':2,'post_event_state':y.tolist(),'reopened_parent_state':reopened.tolist(),'edge_currents':curr,'current_divergence':div.tolist()},
 'comparisons':{'primary_state_l2_error':float(np.linalg.norm(y-py)),'reopening_l2_error':float(np.linalg.norm(reopened-x)),'divergence_vs_parent_minus_state_l2_error':float(np.linalg.norm(div-(x-y))),'primary_relic_residual_l2_error':float(np.linalg.norm((x-y)-pres)),'ledger_error':float(np.sum(y)-np.sum(x))},
 'pass':bool(np.linalg.norm(y-py)<=TOL and np.linalg.norm(reopened-x)<=TOL and np.linalg.norm(div-(x-y))<=TOL and abs(np.sum(y)-np.sum(x))<=TOL),
 'trust_boundary':'Did not load primary GATE_RESULTS, CLOSEOUT, or operator matrix; only exact parent and the primary physical-state value for final comparison.'
}
dump('independent/INDEPENDENT_RECONSTRUCTION.json',rec)
print(json.dumps(rec,indent=2))
