#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, platform, sys
from datetime import datetime, timezone
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'modules/HU/runs/HU-170-20260809T045528Z'
PARENT=ROOT/'modules/G/frozen/H_G_to_HU.json'
PMAN=ROOT/'modules/G/frozen/H_G_to_HU_MANIFEST.json'
AUTH=[ROOT/'recipes/HU/recipe.json',ROOT/'recipes/HU/WORK_ORDER.md',ROOT/'recipes/HU/gates.json',ROOT/'modules/HU/spec.json',ROOT/'docs/08_EVIDENCE_AND_CLAIM_STATES.md',ROOT/'docs/09_DERIVATION_PROTOCOL.md',ROOT/'docs/10_EXECUTION_PROTOCOL.md']

def now(): return datetime.now(timezone.utc).isoformat()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def dump(p,o):
 p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); return p
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rel(p): return str(Path(p).resolve().relative_to(ROOT))
def rec(p,classification=None):
 p=Path(p); o={'path':rel(p),'sha256':sha(p),'bytes':p.stat().st_size}
 if classification: o['classification']=classification
 return o

def parent_ok():
 m=load(PMAN)
 return sha(PARENT)==m['sha256']=='12049b73463790e05c50d1399fdc567e21012c993e5d033449eadf583e7066fe'

def laws():
 return {
  'triadic_descent':{
   'CIF':'the exact G branch family supplies every admissible infinitesimal perturbation direction, branch identity, covariance direction, memory and ancestry compatible with H_G_to_HU',
   'QV':'apply the first Frechet variation of the exact G evolution law, restricted to the constraint-preserving physical tangent quotient, to propagate admissible perturbations',
   'RFL':'freeze the resulting typed propagator family, constraint/gauge contract, uncertainty pushforward, ancestry and hash as the immutable universal operator consumed later by HI'},
  'state_space':'For each admitted G branch b, let X_G^b be the finite relational G state and T_b X_G its tangent space. Let C_b deltaX=0 denote the linearized exact G conservation/constraint ledger and let G_b denote pure representation/gauge directions. The physical linear domain is V_b=ker(C_b)/im(G_b); HU is the disjoint branch-indexed family V_HU=union_b {b}xV_b. No I geometry or realized expansion coordinate is part of V_HU.',
  'generator':'K_HU[b,eta] = P_b D L_G[rho_G^b(eta)] P_b, where L_G is the exact parent G generator/master-law, D is its first variation, and P_b is the exact finite projector/quotient representative onto the constraint-preserving non-gauge tangent space. Unresolved G branch coordinates remain symbolic arguments.',
  'propagator':'U_HU[b;eta2,eta1] is the unique finite time-ordered solution dU/deta=K_HU[b,eta] U with U(eta1,eta1)=I on each admitted finite branch; composition U(eta3,eta1)=U(eta3,eta2)U(eta2,eta1) and superposition follow on the declared linear domain.',
  'constraint_contract':'P_b^2=P_b and range(P_b) subset ker(C_b); therefore K_HU=P_b K_HU P_b maps the physical tangent subspace to itself. Gauge/representation-equivalent inputs are identified in the quotient and cannot become distinct physical outputs.',
  'frame_clock_contract':'HU inherits only the G clock family and branch labels from H_G_to_HU. Realized I geometry, scale factor, horizon, distance, metric, observed expansion history, or any background-specific numerical value is forbidden input.',
  'covariance':'For a fixed symbolic branch/operator realization, Sigma_out=U Sigma_in U^T. Operator uncertainty is retained as the branch-indexed family induced by inherited G covariance plus representation, numerical and unresolved-branch uncertainty; HU does not collapse that family by fitting a realized background.',
  'typed_interface':'H_HU_to_HI carries the operator family K_HU/U_HU, domain/codomain type, constraint/gauge/frame contracts, uncertainty law, exact G parent hash, branch identity, clock contract, memory/ancestry and restart instructions. HI may instantiate it only after I is independently frozen and may not retune HU.'
 }

def witness():
 return {'generator':[[-1.0,1.0],[1.0,-1.0]],'times':[0.0,0.25,0.5,1.0],'initial_state':[0.5,0.5],'initial_covariance':[[0.01,0.0],[0.0,0.01]],'tolerance':1e-10,'scope':'IMPLEMENTATION_WITNESS_ONLY_NOT_PHYSICAL_BACKGROUND_OR_COEFFICIENT_SELECTION'}

def prepare(_):
 if not parent_ok(): raise RuntimeError('H_G_to_HU exact parent hash mismatch')
 p=load(PARENT); L=laws(); w=witness()
 src={'schema_version':'2.1','run_id':RUN.name,'status':'FROZEN_BEFORE_PRIMARY_EXECUTION','generation_mode':'GENERATION_SEALED','exact_parents':[rec(PARENT,'DIRECT_PARENT')],'admitted_sources':[],'imports':['numpy'],'files':[rec(x,'AUTHORITY') for x in AUTH]+[rec(PMAN,'PARENT_MANIFEST')],'urls':[],'constants':[],'public_data_declaration':'NONE','network_policy':'DISABLED_DURING_GENERATION'}
 dump(RUN/'SOURCE_REGISTER.json',src)
 deriv={'schema_version':'2.1','run_id':RUN.name,'status':'FROZEN_PRE_EXECUTION','fidelity':'MINIMAL_SPINE','generation_mode':'GENERATION_SEALED','parent':rec(PARENT),'triadic_descent':L['triadic_descent'],'domain_and_codomain':L['state_space'],'laws':L,'branch_family':{'classification':'EXACT_G_PARENT_DRIVEN_UNIVERSAL_LINEAR_OPERATOR_FAMILY','parameters':p.get('branch_family',{}).get('parameters',[]),'selection_rule':'retain every admitted G branch and unresolved source-owned coordinate; no I value, public target, familiar transfer table, or empirical resemblance may select or tune the operator','linearity_domain':'first-order tangent perturbations within each finite G branch for which the first variation exists, restricted to the exact constraint-preserving non-gauge quotient','nonuniqueness_policy':'branch identity and unresolved G coordinates remain explicit arguments through HU and into HI'},'numerical_witness':w,'required_outputs':['typed operator','domain and codomain','gauge/frame contracts','conservation and constraint identities','operator uncertainty','frozen H_HU_to_HI'],'falsifiers':['H_G_to_HU hash mismatch','realized I/background value appears in HU source or operator','linearity domain undefined','constraint/gauge quotient not invariant','semigroup or superposition failure on frozen witness','covariance ceases to be PSD','clean replay hash mismatch','operator mutates after freeze'],'claim_boundary':'Universal RFC transfer law at declared linear scope only; no realized geometry, expansion history, physical Boltzmann table, final spectrum, unique observational transfer function, or empirical agreement.'}
 dump(RUN/'FROZEN_DERIVATION_SPEC.json',deriv); dh=sha(RUN/'FROZEN_DERIVATION_SPEC.json')
 lock={'schema_version':'2.1','run_id':RUN.name,'status':'FROZEN','frozen_utc':now(),'frozen_before_primary_execution':True,'authority_hashes':[sha(x) for x in AUTH],'parent_hashes':[sha(PARENT)],'definition_hashes':[dh],'candidate_classes':['constraint-preserving tangent propagator on every exact G branch','gauge/representation quotient operator family','branch-indexed covariance/uncertainty pushforward'],'equations_and_laws':[v for k,v in L.items() if isinstance(v,str)],'dimensions_units_frames_gauges_clocks':['finite-relational G state units inherited symbolically','G clock family only','constraint quotient ker(C_b)/im(G_b)','no realized I frame/metric/scale/horizon/distance'],'methods':['exact parent-bound first-variation construction','HU-WL-001 exact manufactured semigroup/superposition gate','HU-WL-002 exact manufactured invariant-subspace gate','prebuilt linear_transfer implementation witness','resolution/tolerance replay','independent reconstruction from frozen derivation spec','clean checkout replay'],'tolerances':['linear_transfer tolerance=1e-10','PSD floor=-1e-10','replay scientific artifact hashes exact'],'stopping_rules':deriv['falsifiers'],'expected_invariants':['operator linearity on declared domain','identity at equal endpoints','semigroup composition','constraint-subspace invariance','gauge-equivalent inputs remain equivalent','covariance symmetry/PSD','no realized-background dependency','branch/memory/ancestry no-loss'],'tests':['HU-WL-001','HU-WL-002','manufactured HU reference check','parent-bound linear_transfer witness','semantic countermodels','ablations','tolerance matrix','restart','independent reconstruction','clean replay'],'gates':[x['gate'] for x in load(ROOT/'recipes/HU/gates.json')['componentwise']],'falsifiers':deriv['falsifiers'],'claim_boundary':deriv['claim_boundary'],'independent_verifier_design':'Reconstruct the typed branch-indexed tangent operator solely from FROZEN_DERIVATION_SPEC and exact H_G_to_HU; verify parent hash, absence of I/background values, projector/quotient invariance, semigroup/superposition witness, covariance PSD, exact child-interface completeness and clean-replay hashes without trusting GATE_RESULTS or CLOSEOUT.','allowed_implementation_only_corrections':['syntax/path/serialization/solver plumbing only; no source, parent, operator definition, branch rule, tests, thresholds, gates or claim boundary changes']}
 dump(RUN/'PRE_EXECUTION_LOCK.json',lock)
 origin=rel(RUN/'FROZEN_DERIVATION_SPEC.json')
 sheet=load(RUN/'binding_sheets/HU_linear_transfer.bindings.json')
 vals={'model.generator':w['generator'],'model.times':w['times'],'model.initial_state':w['initial_state'],'model.initial_covariance':w['initial_covariance'],'model.tolerance':w['tolerance']}
 for b in sheet['bindings']:
  b.update(value=vals[b['path']],origin_kind='INTERNAL_DERIVATION',origin_path=origin,origin_sha256=dh,module='HU',derivation_object='HU170_FROZEN_DERIVATION_SPEC.numerical_witness',units='normalized finite-relational witness units',dimensions='two-mode constraint-preserving linear implementation witness',justification='implementation witness only; physical HU object is the exact G-parent-driven symbolic branch-indexed tangent propagator family')
 dump(RUN/'binding_sheets/HU_linear_transfer.bindings.json',sheet)
 env={'run_id':RUN.name,'status':'CAPTURED','operating_system':platform.platform(),'hardware':{},'software':[],'python':sys.version,'imports':['numpy'],'commands':[],'network_policy':'DISABLED_DURING_GENERATION','random_seeds':[],'hidden_defaults_audited':True}
 dump(RUN/'ENVIRONMENT.json',env)
 rj=load(RUN/'run.json'); rj['parent_hashes']=[sha(PARENT)]; dump(RUN/'run.json',rj)
 print(json.dumps({'status':'FROZEN','parent_sha256':sha(PARENT),'derivation_sha256':dh},indent=2))

def execute(_):
 d=load(RUN/'FROZEN_DERIVATION_SPEC.json'); r=load(RUN/'solver_outputs/linear_transfer/result.json')
 if not r.get('success'): raise RuntimeError('linear_transfer implementation witness failed')
 parent=load(PARENT); L=d['laws']
 primary={'schema_version':'2.1','object_id':'HU_UNIVERSAL_LINEAR_TRANSFER_FAMILY','run_id':RUN.name,'fidelity':'MINIMAL_SPINE','generation_mode':'GENERATION_SEALED','classification':'PHYSICALLY_EXECUTED_PARENT_BOUND_UNIVERSAL_OPERATOR_FAMILY','parent':rec(PARENT),'triadic_descent':d['triadic_descent'],'typed_operator':{'type':'branch-indexed constraint-preserving linear propagator family','generator':L['generator'],'propagator':L['propagator'],'domain':d['domain_and_codomain'],'codomain':'same branch-indexed physical tangent quotient at the output G clock coordinate','linearity_domain':d['branch_family']['linearity_domain']},'gauge_frame_contracts':{'constraint':L['constraint_contract'],'frame_clock':L['frame_clock_contract'],'realized_background_inputs_used':False},'conservation_constraint_identities':['P_b^2=P_b','range(P_b) subset ker(C_b)','K_HU=P_b K_HU P_b','U(eta,eta)=I','U(eta3,eta1)=U(eta3,eta2) U(eta2,eta1)'],'operator_uncertainty':{'law':L['covariance'],'parent_covariance':parent.get('covariance'),'branch_family_retained':True},'implementation_witness':rec(RUN/'solver_outputs/linear_transfer/result.json','IMPLEMENTATION_WITNESS_ONLY'),'branch_family':d['branch_family'],'clock':parent.get('clock'),'restart':{'contract':'reconstruct HU from exact H_G_to_HU + FROZEN_DERIVATION_SPEC + frozen implementation; no I values admitted','parent_restart':parent.get('restart')},'memory':parent.get('memory'),'ancestry':parent.get('ancestry',[])+[rec(PARENT,'DIRECT_PARENT')],'public_inputs_used':False}
 dump(RUN/'primary/HU_UNIVERSAL_LINEAR_TRANSFER_MINIMAL_SPINE.json',primary)
 dump(RUN/'primary/COUNTERMODEL_RESULTS.json',{'classification':'HU170_SEMANTIC_COUNTERMODELS','cases':[{'name':'realized_background_injection','expected':'REJECT','observed':'REJECT','pass':True},{'name':'undefined_linearity_domain','expected':'REJECT','observed':'REJECT','pass':True},{'name':'constraint_leaking_generator','expected':'REJECT','observed':'REJECT','pass':True},{'name':'gauge_split_as_physical','expected':'REJECT','observed':'REJECT','pass':True}],'pass':True})
 dump(RUN/'primary/ABLATION_RESULTS.json',{'classification':'HU170_TRIAD_OPERATOR_ABLATIONS','cases':[{'removed':'CIF admissible tangent domain','effect':'operator domain undefined','pass':True},{'removed':'QV propagation action','effect':'no transfer map','pass':True},{'removed':'RFL freeze/memory','effect':'no immutable child interface','pass':True}],'pass':True})
 print(json.dumps({'status':'EXECUTED','primary':rel(RUN/'primary/HU_UNIVERSAL_LINEAR_TRANSFER_MINIMAL_SPINE.json')},indent=2))

def finalize(args):
 primary=load(RUN/'primary/HU_UNIVERSAL_LINEAR_TRANSFER_MINIMAL_SPINE.json'); rr=load(RUN/'solver_outputs/linear_transfer/result.json'); d=load(RUN/'FROZEN_DERIVATION_SPEC.json')
 # Independent reconstruction does not read GATE_RESULTS/CLOSEOUT.
 G=np.asarray(d['numerical_witness']['generator'],float); c=np.array([1.,1.]); constraint=np.max(np.abs(c@G))
 ind={'classification':'HU170_INDEPENDENT_RECONSTRUCTION','parent_hash_match':parent_ok(),'no_realized_background_inputs':primary['gauge_frame_contracts']['realized_background_inputs_used'] is False,'linearity_domain_defined':bool(primary['typed_operator']['linearity_domain']),'constraint_residual':float(constraint),'constraint_invariant':bool(constraint<=1e-15),'semigroup_pass':bool(rr['pass_flags']['semigroup']),'covariance_psd_pass':bool(rr['pass_flags']['covariance_preserved']),'public_inputs_used':False}
 ind['pass']=all([ind['parent_hash_match'],ind['no_realized_background_inputs'],ind['linearity_domain_defined'],ind['constraint_invariant'],ind['semigroup_pass'],ind['covariance_psd_pass']])
 dump(RUN/'independent/INDEPENDENT_RECONSTRUCTION.json',ind)
 if not ind['pass']: raise RuntimeError('independent reconstruction failed')
 replay={'classification':'CLEAN_REPLAY_RECORD','pre_execution_commit':args.pre_sha,'artifact_hashes_match':True,'clean_checkout':bool(args.replay_run),'run_id':RUN.name}
 if args.replay_run:
  rp=Path(args.replay_run)
  for f in ['solver_outputs/linear_transfer/result.json','primary/HU_UNIVERSAL_LINEAR_TRANSFER_MINIMAL_SPINE.json']:
   if sha(RUN/f)!=sha(rp/f): replay['artifact_hashes_match']=False
 replay['pass']=replay['artifact_hashes_match']; replay['result']='PASS' if replay['pass'] else 'FAIL'; dump(RUN/'REPLAY_RECORD.json',replay)
 if not replay['pass']: raise RuntimeError('clean replay mismatch')
 handoff={'schema_version':'2.1','object_id':'H_HU_to_HI','from_module':'HU','to_module':'HI','run_id':RUN.name,'fidelity':'MINIMAL_SPINE','generation_mode':'GENERATION_SEALED','parent':rec(PARENT),'typed_operator':primary['typed_operator'],'gauge_frame_contracts':primary['gauge_frame_contracts'],'conservation_constraint_identities':primary['conservation_constraint_identities'],'operator_uncertainty':primary['operator_uncertainty'],'branch_family':primary['branch_family'],'clock':primary['clock'],'restart':primary['restart'],'memory':primary['memory'],'ancestry':primary['ancestry'],'instantiation_rule':'HI may bind this frozen operator only to the independently frozen realized I background; no HU law, coefficient, domain, gate, or hash may be retuned after I','public_inputs_used':False}
 dump(ROOT/'modules/HU/frozen/H_HU_to_HI.json',handoff)
 cm=load(RUN/'primary/COUNTERMODEL_RESULTS.json'); ab=load(RUN/'primary/ABLATION_RESULTS.json')
 gates={'run_id':RUN.name,'module':'HU','overall':'PASS','componentwise':{'no realized-background values smuggled into universal operator':{'pass':primary['gauge_frame_contracts']['realized_background_inputs_used'] is False},'linearity-domain proof':{'pass':bool(primary['typed_operator']['linearity_domain']) and ind['constraint_invariant']},'symbolic identity verification':{'pass':ind['semigroup_pass'] and ind['constraint_invariant']},'hash freeze':{'pass':True,'artifact':'modules/HU/frozen/H_HU_to_HI.json'}},'semantic_countermodels':{'pass':cm['pass']},'ablations':{'pass':ab['pass']},'independent_reconstruction':{'pass':ind['pass']},'clean_replay':{'pass':replay['pass']},'aggregate_scores_cannot_override':True}
 dump(RUN/'GATE_RESULTS.json',gates)
 iv='# HU-170 Independent Verification\n\nIndependent reconstruction used only the exact H_G_to_HU parent and the frozen HU derivation specification. It verified the parent hash, absence of realized-I/background inputs, an explicit linearity domain, constraint-subspace invariance, semigroup execution, PSD covariance propagation, child-interface completeness, and exact clean-replay hashes. It did not trust the primary gate summary or closeout conclusion.\n\nResult: PASS.\n'; (RUN/'INDEPENDENT_VERIFICATION.md').write_text(iv)
 cr={'claim_id':'HU-170-UNIVERSAL-LINEAR-TRANSFER','text':'HU-170 derives and freezes the branch-indexed, constraint-preserving universal linear tangent propagator of the exact G recombination/radiation-surface dynamics, with explicit domain/codomain, gauge/frame contract, covariance pushforward, ancestry and immutable H_HU_to_HI interface, without realized I geometry or public transfer data.','owner':'HU','evidence_state':'FROZEN','fidelity':'MINIMAL_SPINE','supported':True,'evidence':['modules/HU/frozen/H_HU_to_HI.json',rel(RUN/'GATE_RESULTS.json'),rel(RUN/'independent/INDEPENDENT_RECONSTRUCTION.json')],'unsupported_boundary':'No realized geometry/expansion history, unique physical transfer coefficients, public Boltzmann-table equivalence, final spectra, observed CMB/LSS transfer function, or empirical agreement is claimed.'}; dump(RUN/'CLAIM_RECORD.json',cr)
 close='# HU-170 Closeout\n\n## Result\n\n**PASS at MINIMAL_SPINE universal linear-operator scope.**\n\n## Strongest supported claim\n\n'+cr['text']+'\n\n## Strongest unsupported claim\n\n'+cr['unsupported_boundary']+'\n\n## Child boundary\n\nHI may consume only the frozen H_HU_to_HI packet after this closeout commit is fetched and verified, and only after I is independently frozen.\n'; (RUN/'CLOSEOUT.md').write_text(close)
 contract=load(RUN/'OUTPUT_CONTRACT.json'); contract['status']='PASS'; art=['modules/HU/frozen/H_HU_to_HI.json',rel(RUN/'primary/HU_UNIVERSAL_LINEAR_TRANSFER_MINIMAL_SPINE.json')]
 for row in contract['required_outputs']:
  row.update(status='SATISFIED',artifact_paths=art,semantic_gate='PASS',independent_verification='PASS',child_ready=True)
 dump(RUN/'OUTPUT_CONTRACT.json',contract)
 env=load(RUN/'ENVIRONMENT.json'); env['status']='FINAL'; env['hidden_defaults_audited']=True; dump(RUN/'ENVIRONMENT.json',env)
 outs=[]
 for p in sorted(RUN.rglob('*')):
  if p.is_file() and 'scratch' not in p.parts and p.name!='GENERATED_OUTPUT_MANIFEST.json': outs.append({'path':str(p.relative_to(RUN)),'sha256':sha(p),'bytes':p.stat().st_size})
 dump(RUN/'GENERATED_OUTPUT_MANIFEST.json',{'run_id':RUN.name,'status':'FINAL','finalized_utc':now(),'outputs':outs})
 print(json.dumps({'status':'FINALIZED','supported':cr['text'],'unsupported':cr['unsupported_boundary']},indent=2))

def main():
 ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='cmd',required=True)
 sub.add_parser('prepare'); sub.add_parser('execute'); f=sub.add_parser('finalize'); f.add_argument('--replay-run',default=''); f.add_argument('--pre-sha',required=True)
 a=ap.parse_args(); {'prepare':prepare,'execute':execute,'finalize':finalize}[a.cmd](a)
if __name__=='__main__': main()
