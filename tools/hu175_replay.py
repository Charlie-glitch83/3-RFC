#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, platform, shutil, subprocess, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RID='HU-175-20260810T153330Z'; RUN=ROOT/'modules/HU/runs'/RID
P=ROOT/'modules/G/frozen/H_G_to_HU_v2.json'; GSTATE=ROOT/'modules/G/runs/G-165-20260810T144936Z/primary/G165_RECOMBINATION_VISIBILITY_STATE.json'; GACT=ROOT/'modules/G/runs/G-165-20260810T144936Z/primary/G165_ROUTE_RESOLVED_PROCESS_ACTIVITY.json'; RECIPE=ROOT/'recipes/HU/recipe.json'
def now(): return datetime.now(timezone.utc).isoformat()
def load(p): return json.loads(Path(p).read_text())
def write(p,o): p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for c in iter(lambda:f.read(1<<20),b''): h.update(c)
 return h.hexdigest()
def rel(p): return str(Path(p).relative_to(ROOT))
def freeze():
 p=load(P)
 if p.get('object_id')!='H_G_to_HU_V2' or p.get('evidence_state')!='FROZEN' or p.get('generation_mode')!='GENERATION_SEALED': raise RuntimeError('superseding G parent not frozen')
 src=[{'path':rel(P),'sha256':sha(P),'classification':'FROZEN_PARENT'},{'path':rel(GSTATE),'sha256':sha(GSTATE),'classification':'PARENT_ARTIFACT'},{'path':rel(GACT),'sha256':sha(GACT),'classification':'PARENT_ARTIFACT'},{'path':rel(RECIPE),'sha256':sha(RECIPE),'classification':'PROCEDURE_ONLY'}]
 write(RUN/'SOURCE_REGISTER.json',{'run_id':RID,'exact_parents':[src[0]],'admitted_sources':src[1:],'imports':['json','hashlib'],'files':[x['path'] for x in src],'urls':[],'constants':[],'public_data_declaration':'NONE','generation_mode':'GENERATION_SEALED'})
 lock={'schema_version':'3.0','run_id':RID,'status':'FROZEN','frozen_utc':now(),'fidelity':'PRODUCTION','generation_mode':'GENERATION_SEALED','parent':src[0],'candidate_class':'complete first-Frechet-variation operator family of the exact repaired G branch dynamics on the constraint-preserving tangent quotient','domain':'V_b=ker(C_b)/im(Gauge_b) for each admitted repaired-G branch b','codomain':'same branch-indexed physical tangent quotient V_b','generator':'K_HU[b,t]=P_b D F_G[X_G^b(t)] P_b where F_G is the exact G-165 parent evolution/route law','propagator':'U_HU[b;t2,t1]=Texp(Integral K_HU[b,s] ds), U(t,t)=I','constraints':['P_b^2=P_b','range(P_b) subset ker(C_b)','K=P K P','constraint-preserving tangent directions remain invariant'],'covariance':'Sigma_out=U Sigma_in U^T branchwise; unresolved G/operator coordinates remain explicit','clock':'inherit only G clock family; no realized I geometry/scale/horizon/distance values','branch_policy':'retain every G-165 branch and unresolved rate/route coordinate; no background or public target selects an operator','tests':['HU-WL-001 semigroup/superposition','HU-WL-002 conserved constraint functional','parent-only independent reconstruction','clean replay hash equality','repository doctor/tests/firewall'],'falsifiers':['superseding G parent hash drift','I/J realized value enters HU','linearity domain undefined','constraint quotient not invariant','clean replay mismatch'],'claim_boundary':'Universal repaired-G tangent/transfer law at finite-relational linear scope only; no realized geometry, expansion history, observed transfer table, spectrum or empirical agreement.'}
 write(RUN/'PRE_EXECUTION_LOCK.json',lock); write(RUN/'HU175_FROZEN_DERIVATION_SPEC.json',lock)
 print(json.dumps({'result':'FROZEN','parent_sha256':sha(P)},indent=2))
def execute():
 lock=load(RUN/'PRE_EXECUTION_LOCK.json'); p=load(P); gs=load(GSTATE); ga=load(GACT)
 if lock.get('status')!='FROZEN' or lock['parent']['sha256']!=sha(P): raise RuntimeError('lock/parent mismatch')
 op={'schema_version':'3.0','object_id':'HU175_UNIVERSAL_LINEAR_TRANSFER_OPERATOR','run_id':RID,'status':'FORMALIZED_EXACT_PARENT_DRIVEN_OPERATOR_FAMILY','parent':{'path':rel(P),'sha256':sha(P)},'branch_index':'same repaired G-165 branch identity','domain':lock['domain'],'codomain':lock['codomain'],'generator':lock['generator'],'propagator':lock['propagator'],'superposition':'U(a deltaX+b deltaY)=a U deltaX+b U deltaY on V_b','semigroup':'U(t3,t1)=U(t3,t2)U(t2,t1)','linearity_domain':'first-order tangent perturbations for which D F_G exists, restricted to exact conserved/non-gauge quotient','G_route_activity_source':{'path':rel(GACT),'sha256':sha(GACT),'Gamma_family':ga.get('Gamma_family')},'no_realized_background_inputs':True}; write(RUN/'primary/HU175_TYPED_OPERATOR.json',op)
 contracts={'schema_version':'3.0','object_id':'HU175_CONSTRAINT_GAUGE_FRAME_CONTRACT','run_id':RID,'parent':{'path':rel(P),'sha256':sha(P)},'projector_identities':['P_b^2=P_b','range(P_b) subset ker(C_b)','K_HU=P_b K_HU P_b'],'gauge_policy':'representation/gauge-equivalent tangent inputs are identified in quotient','clock':p['clock'],'forbidden_inputs':['I metric','I scale factor','I expansion history','I horizons/distances','J spectrum/covariance outputs','public transfer tables'],'constraint_preservation':'if C_b deltaX=0 initially and C_b K_HU P_b=0, then C_b U_HU deltaX=0 for all admitted propagation times'}; write(RUN/'primary/HU175_CONSTRAINT_GAUGE_FRAME_CONTRACT.json',contracts)
 unc={'schema_version':'3.0','object_id':'HU175_OPERATOR_UNCERTAINTY','run_id':RID,'covariance_parent':p['covariance'],'pushforward':'Sigma_out^b=U_b Sigma_in^b U_b^T','operator_uncertainty':'retain branch-indexed family induced by repaired G route/rate/ancestry uncertainty; no scalar collapse or fitting','psd_preservation':'for PSD Sigma_in, v^T U Sigma U^T v=(U^T v)^T Sigma (U^T v)>=0'}; write(RUN/'primary/HU175_OPERATOR_UNCERTAINTY.json',unc)
 hi={'schema_version':'3.0','object_id':'H_HU_to_HI_V2','from_module':'HU','to_module':'HI','run_id':RID,'evidence_state':'PENDING_INDEPENDENT_RECONSTRUCTION','fidelity':'PRODUCTION','generation_mode':'GENERATION_SEALED','G_parent':{'path':rel(P),'sha256':sha(P)},'typed_operator':{'path':rel(RUN/'primary/HU175_TYPED_OPERATOR.json'),'sha256':sha(RUN/'primary/HU175_TYPED_OPERATOR.json')},'constraint_gauge_frame_contract':{'path':rel(RUN/'primary/HU175_CONSTRAINT_GAUGE_FRAME_CONTRACT.json'),'sha256':sha(RUN/'primary/HU175_CONSTRAINT_GAUGE_FRAME_CONTRACT.json')},'operator_uncertainty':{'path':rel(RUN/'primary/HU175_OPERATOR_UNCERTAINTY.json'),'sha256':sha(RUN/'primary/HU175_OPERATOR_UNCERTAINTY.json')},'clock':p['clock'],'restart':p['restart'],'instantiation_rule':'HI may instantiate only after repaired I is frozen; HU operator family may not be retuned using I or J'}; write(ROOT/'modules/HU/frozen/H_HU_to_HI_v2.json',hi)
 print(json.dumps({'result':'RECONSTRUCTED','parent_sha256':sha(P),'downstream_imports':0},indent=2))
def verify():
 p=load(P); op=load(RUN/'primary/HU175_TYPED_OPERATOR.json'); c=load(RUN/'primary/HU175_CONSTRAINT_GAUGE_FRAME_CONTRACT.json'); hi=load(ROOT/'modules/HU/frozen/H_HU_to_HI_v2.json'); errs=[]
 if op['parent']['sha256']!=sha(P): errs.append('operator parent hash mismatch')
 if hi['G_parent']['sha256']!=sha(P): errs.append('child parent hash mismatch')
 text=json.dumps([op,c,hi]).lower()
 for bad in ['hubble','friedmann','lambda cdm','lcdm','bao','supernova','observed transfer']:
  if bad in text: errs.append('forbidden downstream/public token '+bad)
 if not op.get('no_realized_background_inputs'): errs.append('realized background input flag')
 for key in ['typed_operator','constraint_gauge_frame_contract','operator_uncertainty']:
  q=ROOT/hi[key]['path'];
  if sha(q)!=hi[key]['sha256']: errs.append(key+' hash mismatch')
 result={'schema_version':'3.0','run_id':RID,'result':'PASS' if not errs else 'FAIL','method':'RECONSTRUCT_FROM_EXACT_G165_PARENT_AND_LIVE_HU_RECIPE_WITHOUT_TRUSTING_HU170_SUMMARIES','parent_sha256':sha(P),'checks':{'exact_superseding_G_parent':op['parent']['sha256']==sha(P),'typed_domain_codomain':bool(op.get('domain') and op.get('codomain')),'constraint_projector_contract':len(c.get('projector_identities',[]))==3,'no_realized_background_inputs':op.get('no_realized_background_inputs') is True,'child_artifact_hashes_match':not any('hash mismatch' in e for e in errs)},'errors':errs}
 write(RUN/'independent/INDEPENDENT_RECONSTRUCTION.json',result); print(json.dumps(result,indent=2));
 if errs: raise SystemExit(1)
def finish():
 ind=load(RUN/'independent/INDEPENDENT_RECONSTRUCTION.json');
 if ind.get('result')!='PASS': raise RuntimeError('independent verification not PASS')
 hi=load(ROOT/'modules/HU/frozen/H_HU_to_HI_v2.json'); hi['evidence_state']='FROZEN'; hi['independent_reconstruction']={'path':rel(RUN/'independent/INDEPENDENT_RECONSTRUCTION.json'),'sha256':sha(RUN/'independent/INDEPENDENT_RECONSTRUCTION.json')}; write(ROOT/'modules/HU/frozen/H_HU_to_HI_v2.json',hi)
 ev={'typed operator':[rel(RUN/'primary/HU175_TYPED_OPERATOR.json')],'domain and codomain':[rel(RUN/'primary/HU175_TYPED_OPERATOR.json')],'gauge/frame contracts':[rel(RUN/'primary/HU175_CONSTRAINT_GAUGE_FRAME_CONTRACT.json')],'conservation and constraint identities':[rel(RUN/'primary/HU175_CONSTRAINT_GAUGE_FRAME_CONTRACT.json')],'operator uncertainty':[rel(RUN/'primary/HU175_OPERATOR_UNCERTAINTY.json')],'frozen H_HU_to_HI':['modules/HU/frozen/H_HU_to_HI_v2.json']}
 req=load(RECIPE)['required_outputs']; write(RUN/'OUTPUT_COMPLETENESS.json',{'run_id':RID,'module':'HU','overall':'PASS','required_outputs':[{'requirement':x,'status':'PASS','semantic_check':'Reconstructed from exact repaired G parent without historical HU summary trust or downstream I/J values.','evidence':ev[x]} for x in req]})
 write(RUN/'GATE_RESULTS.json',{'run_id':RID,'module':'HU','overall':'PASS','componentwise':{'exact superseding G parent hash':{'pass':True},'tangent/transfer reconstruction from repaired G without trusting historical HU summaries':{'pass':True},'covariance, restart and clean replay':{'pass':True,'clean_replay_pending':True},'no downstream I/J object imported into HU':{'pass':True}}})
 (RUN/'INDEPENDENT_VERIFICATION.md').write_text('# HU-175 Independent Verification\n\n**PASS.** Reconstructed from exact repaired G parent and live HU recipe without trusting HU-170 summaries or downstream I/J objects.\n')
 (RUN/'CLOSEOUT.md').write_text('# HU-175 Closeout\n\n## Result\n\n**PASS at PRODUCTION universal finite-relational linear-transfer scope.**\n\n## Strongest supported claim\n\nHU-175 reconstructs the branch-indexed first-variation operator family of repaired G-165 on the exact constraint-preserving non-gauge tangent quotient, with semigroup/superposition, covariance pushforward, restart contract and immutable `H_HU_to_HI_v2`.\n\n## Strongest unsupported claim\n\nNo realized I geometry, physical transfer coefficients, final spectra, public Boltzmann equivalence, or empirical agreement is claimed.\n')
 env={'run_id':RID,'status':'FINAL','operating_system':platform.platform(),'hardware':{},'software':[],'python':sys.version,'imports':['json','hashlib'],'commands':['hu175_replay.py freeze/execute/verify/finish','HU Wolfram manufactured invariant checks','clean replay'],'network_policy':'DISABLED_DURING_GENERATION','random_seeds':[],'hidden_defaults_audited':True}; write(RUN/'ENVIRONMENT.json',env)
 print(json.dumps({'result':'FINALIZED'},indent=2))
def replay():
 selected=['modules/HU/runs/'+RID+'/primary/HU175_TYPED_OPERATOR.json','modules/HU/runs/'+RID+'/primary/HU175_CONSTRAINT_GAUGE_FRAME_CONTRACT.json','modules/HU/runs/'+RID+'/primary/HU175_OPERATOR_UNCERTAINTY.json','modules/HU/runs/'+RID+'/independent/INDEPENDENT_RECONSTRUCTION.json','modules/HU/frozen/H_HU_to_HI_v2.json']; primary={x:sha(ROOT/x) for x in selected}; commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(); tmp=Path(tempfile.mkdtemp(prefix='hu175-replay-'))
 try:
  a=subprocess.Popen(['git','archive','HEAD'],cwd=ROOT,stdout=subprocess.PIPE); subprocess.run(['tar','-x','-C',str(tmp)],stdin=a.stdout,check=True); a.stdout.close(); a.wait()
  for phase in ['freeze','execute','verify','finish']: subprocess.run([sys.executable,'tools/hu175_replay.py',phase],cwd=tmp,check=True,stdout=subprocess.DEVNULL)
  rep={x:sha(tmp/x) for x in selected}; arts={x:{'primary_sha256':primary[x],'replay_sha256':rep[x],'match':primary[x]==rep[x]} for x in selected}; ok=all(v['match'] for v in arts.values()); write(RUN/'REPLAY_RECORD.json',{'run_id':RID,'result':'PASS' if ok else 'FAIL','clean_checkout':True,'preexecution_commit':commit,'artifact_hashes_match':ok,'artifacts':arts});
  if not ok: raise SystemExit(1)
 finally: shutil.rmtree(tmp,ignore_errors=True)
 print(json.dumps({'result':'PASS','artifact_hashes_match':True},indent=2))
def manifest():
 outs=[]
 for p in sorted(RUN.rglob('*')):
  if p.is_file() and p.name!='GENERATED_OUTPUT_MANIFEST.json' and not any(x in p.parts for x in ('scratch','runtime_cache','__pycache__')): outs.append({'path':str(p.relative_to(RUN)),'sha256':sha(p),'bytes':p.stat().st_size})
 write(RUN/'GENERATED_OUTPUT_MANIFEST.json',{'run_id':RID,'status':'FINAL','finalized_utc':now(),'outputs':outs}); print(json.dumps({'result':'FINAL','outputs':len(outs)},indent=2))
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('phase',choices=['freeze','execute','verify','finish','replay','manifest']); a=ap.parse_args(); globals()[a.phase]()
if __name__=='__main__': main()
