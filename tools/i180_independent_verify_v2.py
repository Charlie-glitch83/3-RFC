#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; RID='I-180-20260810T154430Z'; RUN=ROOT/'modules/I/runs'/RID
P=ROOT/'modules/G/frozen/H_G_to_I_v2.json'; B=ROOT/'modules/B/frozen/H_B_to_C_v2.json'; C=ROOT/'modules/I/repair/I180_CORRECTED_DERIVATION_SPEC.json'
def load(p): return json.loads(Path(p).read_text())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,o): p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,indent=2)+'\n')
def main():
 p,b,c=load(P),load(B),load(C)
 actp=ROOT/p['route_resolved_process_activity']['path']; ancp=ROOT/p['route_to_relational_ancestry']['path']
 if sha(actp)!=p['route_resolved_process_activity']['sha256'] or sha(ancp)!=p['route_to_relational_ancestry']['sha256']: raise SystemExit('parent child hash mismatch')
 act,anc=load(actp),load(ancp); edges=anc['B_edges']; checks={}
 checks['parent_frozen_production']=p.get('evidence_state')=='FROZEN' and p.get('fidelity')=='PRODUCTION'
 checks['gamma_exact_branch_replacement']=p.get('Gamma_binding_classification')=='EXACT_PARENT_BOUND_BRANCH_INDEXED_REPLACEMENT'
 checks['ancestry_complete']=anc.get('ancestry_complete_for_I') is True and [x['edge_id'] for x in edges]==['e01','e02','e12']
 checks['activity_family_nonempty']=len(act.get('concrete_activity',[]))>0 and len(act.get('parametric_activity_fibers',[]))>0
 checks['M_support_complete']=all(x.get('support_edges')==['e01','e02','e12'] for x in anc.get('route_supports',[])+anc.get('parametric_family_supports',[]))
 max_row=max_pdet=max_green=max_rsym=max_rneg=0.0
 H=np.eye(3)-np.ones((3,3))/3.0
 for vals in [(1.0,1.0,1.0),(0.5,0.3,0.2),(2.0,1.0,0.25)]:
  a,bv,cv=vals
  L=np.array([[a+bv,-a,-bv],[-a,a+cv,-cv],[-bv,-cv,bv+cv]],float)
  max_row=max(max_row,float(np.max(np.abs(L@np.ones(3)))))
  D=a*bv+a*cv+bv*cv
  disc=a*a+bv*bv+cv*cv-a*bv-a*cv-bv*cv
  lm=a+bv+cv-math.sqrt(max(0,disc)); lp=a+bv+cv+math.sqrt(max(0,disc))
  eig=np.linalg.eigvalsh(L); pos=eig[eig>1e-12]
  max_pdet=max(max_pdet,abs(float(np.prod(pos))-3*D),abs(lm*lp-3*D),abs(float(pos[0])-lm),abs(float(pos[1])-lp))
  Lp=np.linalg.pinv(L,hermitian=True); R=np.zeros((3,3))
  for i in range(3):
   for j in range(3):
    e=np.zeros(3); e[i]=1; e[j]-=1; R[i,j]=float(e@Lp@e)
  recon=-0.5*H@R@H
  max_green=max(max_green,float(np.max(np.abs(recon-Lp))),float(np.max(np.abs(L@Lp-H))))
  max_rsym=max(max_rsym,float(np.max(np.abs(R-R.T))))
  max_rneg=max(max_rneg,max(0.0,-float(R.min())))
 checks['K3_laplacian_spectrum_pdet']=max_row<=1e-12 and max_pdet<=1e-10
 checks['green_resistance_lossless_reconstruction']=max_green<=1e-10 and max_rsym<=1e-12 and max_rneg<=1e-12
 def Rvals(a,b,c):
  D=a*b+a*c+b*c; return ((b+c)/D,(a+c)/D,(a+b)/D)
 r1,r2=Rvals(1,1,.4),Rvals(1,1,.1); checks['shortest_path_countermodel']=max(abs(x-y) for x,y in zip(r1,r2))>.1
 ratios=[.5,1.0]; checks['nonhomothetic_scalar_countermodel']=abs(math.sqrt(ratios[0]*ratios[1])-math.sqrt((ratios[0]**2+ratios[1]**2)/2))>1e-3
 checks['homothetic_theorem_witness']=all(abs(x-.5)<1e-15 for x in [math.sqrt(2/8),math.sqrt(6/24)])
 Ldisc=np.array([[1,-1,0],[-1,1,0],[0,0,0]],float); checks['disconnected_rejection']=int(np.sum(np.abs(np.linalg.eigvalsh(Ldisc))<=1e-12))==2
 checks['clock_preserved']=p['clock'].get('recursive_depth_is_time') is False and 't_B' in p['clock'].get('unit_family','')
 checks['generation_sealed']=p.get('generation_mode')=='GENERATION_SEALED'
 checks['unique_horizon_not_parent_fixed']=c['causal_reach']['status']=='BRANCH_FUNCTIONAL_PENDING_GEOMETRY_AND_PROPAGATION_BINDING'
 result='PASS' if all(checks.values()) else 'FAIL'
 out={'schema_version':'4.0','object_id':'I180_INDEPENDENT_PARENT_ONLY_RECONSTRUCTION','run_id':RID,'result':result,'method':'PARENT_ONLY_K3_RESPONSE_RECONSTRUCTION_NO_I_PRIMARY_OR_GATE_SUMMARY_READ','inputs':{'H_G_to_I_v2_sha256':sha(P),'H_B_to_C_v2_sha256':sha(B),'corrected_I_spec_sha256':sha(C),'G_activity_sha256':sha(actp),'G_ancestry_sha256':sha(ancp)},'reconstructed':{'source_index_count':len(act['concrete_activity'])+len(act['parametric_activity_fibers']),'edge_ids':[x['edge_id'] for x in edges],'L':'[[a+b,-a,-b],[-a,a+c,-c],[-b,-c,b+c]]','pdet':'3(ab+ac+bc)','R01':'(b+c)/(ab+ac+bc)','R02':'(a+c)/(ab+ac+bc)','R12':'(a+b)/(ab+ac+bc)','Lplus_from_R':'-1/2 H R H','a_vol':'[D_in/D]^(1/4)','homothety':'constant a:b:c ratios'},'numeric_residuals':{'max_row_sum':max_row,'max_spectrum_pdet':max_pdet,'max_green_reconstruction':max_green,'max_R_symmetry':max_rsym,'max_R_negativity':max_rneg},'checks':checks,'trusted_I_primary_files':False,'trusted_gate_summary':False}
 write(RUN/'independent/INDEPENDENT_RECONSTRUCTION.json',out)
 print(json.dumps(out,indent=2)); raise SystemExit(0 if result=='PASS' else 1)
if __name__=='__main__': main()
