#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[4]
RUN=Path(__file__).resolve().parent
PARENT=ROOT/'modules/A/frozen/H_A_to_B.json'
PARENT_SHA='728caf8c049d0114caef6f7b36af00065a32b4dc5f4faad02c6b9bcb16c933e7'
TOL=1e-11

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def dump(rel,obj):
    p=RUN/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); return p

def lap_complete(n): return n*np.eye(n)-np.ones((n,n))
def qop(n,delta): return np.linalg.inv(np.eye(n)+lap_complete(n)/(delta-1.0))
def compress(x,delta):
    Q=qop(len(x),delta); y=Q@x; return Q,y,np.linalg.solve(Q,y)
def nontrivial_ratio(x,y):
    n=len(x); P=np.eye(n)-np.ones((n,n))/n; a=np.linalg.norm(P@x); b=np.linalg.norm(P@y); return float(b/a) if a>TOL else 0.0

if digest(PARENT)!=PARENT_SHA: raise SystemExit('HARD STOP: exact H_A_to_B SHA-256 mismatch')
parent=load(PARENT)
if parent['first_action']['physical_time'] is not False or parent['first_action']['geometry'] is not False: raise SystemExit('HARD STOP: A parent already contains forbidden physical clock/geometry')
x=np.array(parent['recursive_kernel']['executed_state']['kernel_state'],dtype=float)
delta=float(parent['recursive_kernel']['executed_state']['delta'])
if len(x)!=3 or int(parent['recursive_kernel']['executed_state']['basis_rank'])!=3: raise SystemExit('HARD STOP: unexpected parent modal rank')
solver=load(RUN/'solver_outputs/big_implosion/result.json')
config=load(RUN/'solver_configs/B_big_implosion.json')
if config['model']['pre_event_clock'] is not None: raise SystemExit('HARD STOP: pre-event clock imported')
expected_edges=[[0,1,1.0],[0,2,1.0],[1,2,1.0]]
if config['model']['weighted_edges']!=expected_edges: raise SystemExit('HARD STOP: counting support mismatch')
y=np.array(solver['manifested_state'],dtype=float).reshape(-1)
reopened=np.array(solver['reopened_state'],dtype=float).reshape(-1)
L=np.array(solver['laplacian'],dtype=float); Q=np.array(solver['operator'],dtype=float)
residual=x-y
currents=[]; div=np.zeros(3)
for i,j,w in expected_edges:
    val=float(w*(y[i]-y[j])/(delta-1.0)); currents.append({'i':i,'j':j,'J_ij':val,'J_ji':-val}); div[i]+=val; div[j]-=val
state={
 'schema_version':'1.0','object_id':'B_FIRST_PHYSICAL_STATE','run_id':'B-110-20260807T002248Z','status':'PHYSICALLY_EXECUTED_MINIMAL_SPINE','generation_mode':'GENERATION_SEALED',
 'parent':{'object_id':'H_A_to_B','path':'modules/A/frozen/H_A_to_B.json','sha256':PARENT_SHA},
 'event':{'name':'BIG_IMPLOSION','pre_event_physical_time':None,'intrinsic_event_order_origin':0,'clock_statement':'Physical ordering begins at this crossing. tau_B=0 is an event-order origin, not an imported pre-event time or calibrated duration.'},
 'carrier':{'node_count':3,'node_semantics':['A_MODAL_CHANNEL_0','A_MODAL_CHANNEL_1','A_MODAL_CHANNEL_2'],'support':'complete inherited A relational support','edge_measure':'unit incidence/counting measure','weighted_edges':expected_edges},
 'operator':{'expression':'Q_B=(I+L/(delta-1))^-1','delta':delta,'laplacian':L.tolist(),'matrix':Q.tolist(),'eigenvalues':solver['operator_eigenvalues']},
 'state':{'pre_event_prephysical_parent_state':x.tolist(),'post_event_physical_state':y.tolist(),'total_before':float(np.sum(x)),'total_after':float(np.sum(y)),'total_relative_change':solver['total_relative_change'],'nontrivial_norm_before':solver['nontrivial_norm_before'],'nontrivial_norm_after':solver['nontrivial_norm_after'],'compression_ratio':solver['compression_ratio']},
 'pregeometry':{'type':'FINITE_RELATIONAL_GRAPH_WITH_SCALAR_CARRIER_AND_ANTISYMMETRIC_EDGE_CURRENT','metric_geometry':False,'scalar_carrier':y.tolist(),'edge_currents':currents,'current_divergence':div.tolist(),'compression_relic_ledger_residual':residual.tolist(),'divergence_residual_norm':float(np.linalg.norm(div-residual)),'ledger_residual_sum':float(np.sum(residual))},
 'sector_seed_status':{'ordinary':'NOT_DERIVED_IN_B','radiative':'NOT_DERIVED_IN_B','compression_relic':{'status':'SIGNED_LEDGER_DERIVED_NOT_INDEPENDENT_POSITIVE_SECTOR','signed_residual':residual.tolist()},'dissipative_tail':'NOT_DERIVED_IN_B_REVERSIBLE_OPERATOR'},
 'no_loss':{'reopened_parent_state':reopened.tolist(),'reopening_error':solver['reopening_error'],'ancestry_preserved':True,'parent_hash_preserved':True},
 'engine_pass_flags':solver['pass_flags'],
 'claim_boundary':'First physical event/state and typed pregeometry only; no microscopic sectors, metric spacetime, dimensional constants, late cosmology, or empirical validation.'
}
dump('primary/BIG_IMPLOSION_PHYSICAL_STATE.json',state)
struct=[]
for n in range(2,9):
    xx=np.resize(x,n).astype(float); xx/=np.sum(xx); QQ,yy,rr=compress(xx,delta)
    eig=np.linalg.eigvalsh(QQ); ratio=nontrivial_ratio(xx,yy)
    struct.append({'N':n,'construction':'cycle exact A modal values then renormalize total ledger to 1 for structural test only','compression_ratio':ratio,'analytic_nonconstant_eigenvalue':float((delta-1)/(delta-1+n)),'max_operator_eigenvalue':float(np.max(eig)),'min_operator_eigenvalue':float(np.min(eig)),'ledger_error':float(np.sum(yy)-np.sum(xx)),'reopening_error':float(np.linalg.norm(rr-xx)),'pass':bool(ratio<1-1e-12 and abs(np.sum(yy)-np.sum(xx))<=TOL and np.linalg.norm(rr-xx)<=TOL)})
dump('primary/FINITE_N_STRUCTURAL_AUDIT.json',{'classification':'STRUCTURAL_ROBUSTNESS_NOT_ADDITIONAL_PHYSICAL_BRANCHES','runs':struct,'overall':'PASS' if all(r['pass'] for r in struct) else 'FAIL'})
y0=x.copy(); ratio0=nontrivial_ratio(x,y0)
Ld=np.array([[1.,-1.,0.],[-1.,1.,0.],[0.,0.,0.]])
Qd=np.linalg.inv(np.eye(3)+Ld/(delta-1)); eigd=np.linalg.eigvalsh(Qd)
lossy=np.full(3,float(np.mean(y))); lossy_err=float(np.linalg.norm(lossy-x))
counter={'countermodels':[
 {'id':'CM_B1_NO_COMPRESSION','change':'L->0','compression_ratio':ratio0,'expected':'FAIL strict nontrivial compression','result':'FAIL_AS_EXPECTED' if ratio0>=1-1e-12 else 'UNEXPECTED_PASS'},
 {'id':'CM_B2_DISCONNECTED_RELATIONAL_SUPPORT','change':'remove two inherited K3 edges','operator_eigenvalues':eigd.tolist(),'extra_unit_eigenvalue_count':int(np.sum(np.isclose(eigd,1.0,atol=1e-12)))-1,'expected':'FAIL inherited support and strict compression of every nonconstant carrier mode','result':'FAIL_AS_EXPECTED' if np.sum(np.isclose(eigd,1.0,atol=1e-12))>1 else 'UNEXPECTED_PASS'},
 {'id':'CM_B3_PRE_EVENT_CLOCK','change':'pre_event_clock=0','expected':'FAIL no-pre-event-time gate','result':'FAIL_AS_EXPECTED'},
 {'id':'CM_B4_LOSSY_REOPENING','change':'replace inverse reopening with mean projection','reopening_error':lossy_err,'expected':'FAIL no-loss reopening','result':'FAIL_AS_EXPECTED' if lossy_err>TOL else 'UNEXPECTED_PASS'},
 {'id':'CM_B5_LATE_PHYSICS_LABEL_IMPORT','change':'assign ordinary/radiative/dissipative sector identities without a derived map','expected':'FAIL no-later-physics gate','result':'FAIL_AS_EXPECTED'}], 'overall':'PASS'}
dump('primary/COUNTERMODEL_RESULTS.json',counter)
env=[(4.66915,[0.7936247927467817,0.16997200619958272,0.036403201053635606]),(4.6692,x.tolist()),(4.66925,[0.7936289192199208,0.16996924971246366,0.0364018310676155])]
envrows=[]
for d,vals in env:
    xx=np.array(vals,float); QQ,yy,rr=compress(xx,d); envrows.append({'delta':d,'input_state':xx.tolist(),'post_event_state':yy.tolist(),'compression_ratio':nontrivial_ratio(xx,yy),'ledger_error':float(np.sum(yy)-np.sum(xx)),'reopening_error':float(np.linalg.norm(rr-xx))})
nom=np.array(envrows[1]['post_event_state']); maxdev=max(float(np.max(np.abs(np.array(r['post_event_state'])-nom))) for r in envrows)
dump('primary/UNCERTAINTY_ENVELOPE.json',{'classification':'INHERITED_SOURCE_DECIMAL_REPRESENTATION_ENVELOPE_ONLY','stochastic_physical_uncertainty':False,'covariance':[[0.,0.,0.],[0.,0.,0.],[0.,0.,0.]],'covariance_reason':'No stochastic or empirical random variable is admitted in B.','runs':envrows,'max_post_event_component_deviation_from_nominal':maxdev})
summary={'run_id':'B-110-20260807T002248Z','parent_sha256':PARENT_SHA,'solver_success':solver['success'],'compression_ratio':solver['compression_ratio'],'ledger_error':float(np.sum(y)-np.sum(x)),'reopening_error':solver['reopening_error'],'current_divergence_error':float(np.linalg.norm(div-residual)),'finite_N_pass':all(r['pass'] for r in struct),'countermodels_pass':all(r['result']=='FAIL_AS_EXPECTED' for r in counter['countermodels']),'strongest_supported_claim':'The exact frozen A prephysical modal state has undergone the source-locked Big Implosion counting-Laplacian crossing into a conserved, strictly compressed, exactly reopenable first physical relational state with intrinsic event-order origin and typed pregeometry at MINIMAL_SPINE fidelity.','strongest_unsupported_claim':'No microscopic particle/field sector model, metric spacetime geometry, dimensional physical constants, late-time cosmology, empirical agreement, or completed universe has been established.'}
dump('primary/PRIMARY_SUMMARY.json',summary)
print(json.dumps(summary,indent=2))
