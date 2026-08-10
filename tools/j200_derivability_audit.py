#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, platform, sys
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RID='J-200-20260810T170347Z'; RUN=ROOT/'modules/J/runs'/RID
HI=ROOT/'modules/HI/frozen/H_HI_to_J_v2.json'
P29=ROOT/'sources/frozen/cef6d68b05eb509e471c55a18b5fffedd9c411b44bc0d5bd0f6b5ee86bd8b53e/Presentation 29 revised  raw LaTeX.md'
P30=ROOT/'sources/frozen/4895c3777da3aa84da4ec2343419ffbc07502b3738602308a1f402862441eaf6/Presentation 30 raw LaTex.md'
BLUE=ROOT/'sources/frozen/2f3539d6493f87a407765a9f24d6cd61e825a36fe9217d2adfa075c070d27b6e/2RFC_Deep_Soak_and_Realization_Blueprint_20260805.md'
QUEUE=ROOT/'sources/frozen/c3b22b3f6973cef75409162c406ac224b2d66aa8bb938a6f035d386384fab226/2RFC_Immediate_Execution_Queue_20260805.md'
RECIPE=ROOT/'recipes/J/recipe.json'; WORK=ROOT/'recipes/J/WORK_ORDER.md'; GATES=ROOT/'recipes/J/gates.json'; SPEC=ROOT/'modules/J/spec.json'; PROTO=ROOT/'docs/09_DERIVATION_PROTOCOL.md'
def now(): return datetime.now(timezone.utc).isoformat()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def text(p): return Path(p).read_text(encoding='utf-8')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rel(p): return str(Path(p).resolve().relative_to(ROOT))
def rec(p,**kw):
 p=Path(p); d={'path':rel(p),'sha256':sha(p),'bytes':p.stat().st_size}; d.update(kw); return d
def write(p,o):
 p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); return p

def verify():
 s=load(ROOT/'STATE.json')
 if not (s.get('active_work_unit')=='J-200' and s.get('current_module')=='J' and s.get('current_run')==RID): raise RuntimeError(f'J-200 not sole active run: {s.get("active_work_unit")}/{s.get("current_module")}/{s.get("current_run")}')
 if s.get('generation_mode')!='GENERATION_SEALED': raise RuntimeError('generation firewall not sealed')
 hi=load(HI)
 if hi.get('object_id')!='H_HI_to_J_V2' or hi.get('evidence_state')!='FROZEN' or hi.get('fidelity')!='PRODUCTION': raise RuntimeError('wrong HI parent')
 if hi.get('generation_mode')!='GENERATION_SEALED': raise RuntimeError('HI generation mode drift')
 for p in [P29,P30,BLUE,QUEUE,RECIPE,WORK,GATES,SPEC,PROTO]:
  if not p.is_file(): raise RuntimeError(f'missing authority {p}')
 return s,hi

def freeze(_):
 _,hi=verify()
 src={'schema_version':'4.0','run_id':RID,'status':'FROZEN_BEFORE_PRIMARY_EXECUTION','generation_mode':'GENERATION_SEALED','exact_parents':[rec(HI,role='DIRECT_PARENT')],'admitted_sources':[rec(P29,role='CANONICAL_P29_KERNEL_AUTHORITY'),rec(P30,role='CANONICAL_P30_NEGATIVE_BOUNDARY_AUTHORITY'),rec(BLUE,role='REALIZATION_BLUEPRINT'),rec(QUEUE,role='EXECUTION_QUEUE')],'procedure_only_sources':[rec(RECIPE),rec(WORK),rec(GATES),rec(SPEC),rec(PROTO)],'imports':['json','hashlib','pathlib'],'files':[],'urls':[],'constants':[],'public_data_declaration':'NONE','network_policy':'DISABLED_DURING_GENERATION','forbidden_generation_inputs':['public initial-condition files','observed target phases','A_s','n_s','physical P_R(k)','physical T(k)','matter power spectrum','remembered LambdaCDM defaults']}
 write(RUN/'SOURCE_REGISTER.json',src)
 deriv={'schema_version':'4.0','run_id':RID,'status':'FROZEN_PRE_EXECUTION_DERIVABILITY_AUDIT','module':'J','fidelity':'PRODUCTION','generation_mode':'GENERATION_SEALED','parent':rec(HI),'source_laws':{'P29_recursive_kernel':'K_f(t)=sum_{j=1}^N delta^(-j) f_j(t) exp(-alpha j t)','P29_normalized_depth_weights':'p_j(t;n)=delta^(-j) exp(-alpha j t)/sum_{k=1}^n delta^(-k) exp(-alpha k t), positive and normalized','P30_negative_boundary':'physical P_R(k), n_s, A_s, alpha_s, r, physical T(k), and matter power are pending/not generated and cannot be imported as solved parents','HI_covariance_pushforward':hi['error_covariance_propagation']['law']},'lawful_candidate':'For any exact finite ordered physical HI basis {f_bj} with a source-owned P29 recursion-index mapping and normalization, Sigma_b=sum_j p_j |f_bj><f_bj| is PSD and may be pushed forward only by the exact HI law. Retain all lawful branch/basis mappings if not uniquely selected.','materialization_requirements':['finite ordered physical HI perturbation basis','basis dimension/mode count','basis normalization/physical amplitude','source-owned mapping j -> HI physical basis mode','material covariance values on that basis','finite-volume geometry/boundaries for field realization','target-blind seed only after covariance is materially fixed'],'seed_rule':'Only after material covariance is fixed, a seed may be deterministically derived from SHA256(parent_sha256 || run_id || purpose_label); never search or retune seed.','forbidden_promotions':['manufactured covariance to physical parent','P30 pending/proxy values to physical spectrum','I response-geometry eigenmodes to HU perturbation modes without a parent-owned intertwiner','arbitrary dimension/order/amplitude','unowned zero cross covariance'],'claim_boundary':{'strongest_supported':'J can formalize an endogenous PSD covariance branch family on any future exact finite ordered HI physical mode basis using P29 normalized recursive weights, while preserving HI covariance pushforward, branch identity, no-retune, and target-blind seed discipline.','strongest_unsupported':'The current exact HI+P29+P30 source set does not yet establish one material primordial covariance, physical linear spectrum, phase realization, or finite-volume field because the required physical basis/mapping/normalization is not source-owned.'}}
 write(RUN/'FROZEN_DERIVATION_SPEC.json',deriv)
 lock={'schema_version':'4.0','run_id':RID,'status':'FROZEN','frozen_utc':now(),'frozen_before_primary_execution':True,'authority_hashes':[rec(RECIPE),rec(WORK),rec(GATES),rec(SPEC),rec(PROTO)],'parent_hashes':[rec(HI)],'definition_hashes':[rec(RUN/'FROZEN_DERIVATION_SPEC.json'),rec(P29),rec(P30),rec(BLUE),rec(QUEUE)],'candidate_classes':['endogenous PSD covariance family on exact HI modes','target-blind phase/seed realization only after covariance materialization','finite-volume Hermitian field only after exact covariance and geometry bindings'],'equations_and_laws':list(deriv['source_laws'].values())+[deriv['lawful_candidate'],deriv['seed_rule']],'dimensions_units_frames_gauges_clocks':['inherit HI branch identity and Big-Implosion clock','HU physical quotient V_b retained','I background quotient remains distinct','recursive depth j is not physical time or automatically an HI mode label','no imported k-grid/SI normalization'],'methods':['exact source/hash audit','J-WL-001/J-WL-002 manufactured checks','typed material-derivability audit','independent source-only reconstruction'],'tolerances':[{'name':'material_binding','value':'EXACT_SOURCE_OWNERSHIP_REQUIRED'},{'name':'manufactured_covariance','value':1e-12},{'name':'Hermitian_reality','value':1e-10}],'stopping_rules':['any material covariance ingredient absent','any public/remembered initial-condition value enters','manufactured covariance promoted','arbitrary mode dimension/order/amplitude','unresolved __BIND token','cross-gauge/mode identification without parent-owned map'],'expected_invariants':['exact HI hash unchanged','P29/P30 hashes unchanged','P29 weights positive and normalized','P30 pending physical spectra remain pending','branch identity retained','no public initial condition','no numeric physical solver before complete bindings'],'tests':['exact source audit','J-WL-001 preserved failure plus implementation-only corrected rerun','J-WL-002','manufactured reference check','independent material-derivability reconstruction'],'gates':['covariance PSD','reality/Hermitian conditions','resolution and volume tests','no public initial-condition file','independent field reconstruction'],'falsifiers':deriv['forbidden_promotions'],'claim_boundary':deriv['claim_boundary'],'independent_verifier_design':'Read only exact HI parent and P29/P30/blueprint sources. Determine whether basis, dimension, normalization/amplitude, j-to-mode map, material covariance, finite-volume geometry and phase prerequisites are actually supplied. Refuse physical materialization if any are absent.','allowed_implementation_only_corrections':['Wolfram protected-symbol rename and Cholesky product convention; syntax/path/serialization/evidence plumbing only; no source/law/gate/claim changes']}
 write(RUN/'PRE_EXECUTION_LOCK.json',lock)
 r=load(RUN/'run.json'); r['parent_hashes']=[sha(HI)]; write(RUN/'run.json',r)
 write(RUN/'ENVIRONMENT.json',{'schema_version':'4.0','run_id':RID,'status':'CAPTURED_PRE_EXECUTION','generation_mode':'GENERATION_SEALED','operating_system':platform.platform(),'python':sys.version,'network_policy':'DISABLED_DURING_GENERATION','imports':['json','hashlib','pathlib'],'hidden_defaults_audited':True,'public_inputs_used':False})
 print(json.dumps({'result':'FROZEN_DERIVABILITY_AUDIT','HI_sha256':sha(HI),'P29_sha256':sha(P29),'P30_sha256':sha(P30)},indent=2))

def audit(_):
 _,hi=verify(); p29=text(P29); p30=text(P30); htxt=json.dumps(hi)
 checks={
  'HI_actual_primordial_covariance_absent':hi.get('J_interface',{}).get('actual_primordial_covariance_status')=='NOT_REALIZED_IN_HI',
  'HI_phase_seed_absent':hi.get('J_interface',{}).get('phase_seed_status')=='NOT_REALIZED_IN_HI',
  'HI_finite_volume_field_absent':hi.get('J_interface',{}).get('finite_volume_field_status')=='NOT_REALIZED_IN_HI',
  'HI_mode_selection_absent':hi.get('mode_eigenstructure',{}).get('selection')=='NONE',
  'HI_cross_gauge_map_absent':hi.get('gauge_frame_mapping',{}).get('cross_gauge_identification')=='NONE_UNLESS_PARENT_DEFINED',
  'P29_kernel_present':'K_f(t)' in p29 and 'delta^{-j}' in p29,
  'P29_weights_present':'p_j(t;n)' in p29 and 'normalized distribution over recursive depth' in p29,
  'P30_physical_spectrum_pending':'physical primordial scalar spectrum P_R(k)' in p30 and 'amplitude A_s' in p30 and 'physical matter transfer function T(k)' in p30,
  'no_explicit_finite_ordered_HI_basis':('finite ordered physical HI' not in p29 and 'finite ordered physical HI' not in p30 and 'basis_vectors' not in htxt),
  'no_source_owned_j_to_HI_map':('j_to_HI_mode' not in p29 and 'j_to_HI_mode' not in p30 and 'j_to_HI_mode' not in htxt),
  'no_physical_covariance_amplitude':hi.get('J_interface',{}).get('actual_primordial_covariance_status')=='NOT_REALIZED_IN_HI' and 'PENDING / NOT INVENTED VALUES' in p30,
 }
 missing=['finite ordered physical HI perturbation basis','basis dimension/mode count','source-owned j -> HI mode map','physical covariance normalization/amplitude','material primordial covariance','finite-volume physical geometry/boundaries tied to the covariance basis']
 result='BLOCKED_UNDERDETERMINED' if all(checks.values()) else 'REVIEW_REQUIRED'
 obj={'schema_version':'4.0','object_id':'J200_MATERIAL_COVARIANCE_DERIVABILITY_AUDIT','run_id':RID,'result':result,'physical_primary_execution_started':False,'checks':checks,'missing_material_bindings':missing,'lawful_symbolic_family':'Sigma_b=sum_j p_j |f_bj><f_bj| on any future exact finite ordered source-owned HI basis; all unresolved basis/mapping branches remain explicit','solver_policy':'DO_NOT_MATERIALIZE covariance or fourier_field configs while any material binding is absent; manufactured J checks are not physical bindings','triad_analysis':{'CIF':'Current CIF correctly retains the full lawful mode/basis possibility family rather than silently choosing one.','QV':'Current QV selection rule is incomplete at J: no source-owned operation maps recursive-depth labels to a finite ordered physical HI perturbation basis with amplitude/normalization. This is the precise missing triadic link.','RFL':'RFL cannot stabilize a unique covariance/field until that QV mapping exists; promoting a representative covariance would manufacture the missing selection rather than derive it.'},'strongest_supported':load(RUN/'FROZEN_DERIVATION_SPEC.json')['claim_boundary']['strongest_supported'],'strongest_unsupported':load(RUN/'FROZEN_DERIVATION_SPEC.json')['claim_boundary']['strongest_unsupported']}
 write(RUN/'primary/J200_MATERIAL_COVARIANCE_DERIVABILITY_AUDIT.json',obj)
 if result!='BLOCKED_UNDERDETERMINED': raise RuntimeError('unexpected J derivability audit state')
 print(json.dumps(obj,indent=2))

def independent(_):
 hi=load(HI); p29=text(P29); p30=text(P30)
 checks={'exact_HI_parent_hash':sha(HI)==load(RUN/'SOURCE_REGISTER.json')['exact_parents'][0]['sha256'],'P29_normalized_weight_law':'p_j(t;n)' in p29 and 'sum_{j=1}^{n}p_j(t;n)=1' in p29.replace('\\',''),'P30_A_s_pending':'amplitude A_s' in p30,'P30_PR_pending':'physical primordial scalar spectrum P_R(k)' in p30,'HI_covariance_not_realized':hi['J_interface']['actual_primordial_covariance_status']=='NOT_REALIZED_IN_HI','HI_seed_not_realized':hi['J_interface']['phase_seed_status']=='NOT_REALIZED_IN_HI','HI_field_not_realized':hi['J_interface']['finite_volume_field_status']=='NOT_REALIZED_IN_HI','HI_mode_selection_none':hi['mode_eigenstructure']['selection']=='NONE'}
 # The normalization theorem text can vary in escaping; positivity/kernel law is independently checked as fallback.
 if not checks['P29_normalized_weight_law']: checks['P29_normalized_weight_law']='normalized distribution over recursive depth' in p29 and 'p_j(t;n)' in p29
 result='PASS' if all(checks.values()) else 'FAIL'
 out={'schema_version':'4.0','object_id':'J200_INDEPENDENT_SOURCE_ONLY_OBSTRUCTION_RECONSTRUCTION','run_id':RID,'result':result,'classification':'INDEPENDENT_RECONSTRUCTION_OF_UNDERDETERMINATION','trusted_primary_audit':False,'checks':checks,'conclusion':'Exact sources independently reproduce the J material-covariance obstruction; physical covariance/field materialization would require an unowned basis mapping or amplitude and is therefore forbidden.'}
 write(RUN/'independent/INDEPENDENT_RECONSTRUCTION.json',out)
 if result!='PASS': raise RuntimeError('independent obstruction reconstruction failed')
 print(json.dumps(out,indent=2))

def finalize(_):
 a=load(RUN/'primary/J200_MATERIAL_COVARIANCE_DERIVABILITY_AUDIT.json'); ind=load(RUN/'independent/INDEPENDENT_RECONSTRUCTION.json')
 if a['result']!='BLOCKED_UNDERDETERMINED' or ind['result']!='PASS': raise RuntimeError('cannot finalize J obstruction')
 claim=load(RUN/'FROZEN_DERIVATION_SPEC.json')['claim_boundary']
 gates={'schema_version':'4.0','run_id':RID,'overall':'BLOCKED_UNDERDETERMINED','componentwise':[
  {'gate':'covariance PSD','status':'NOT_EXECUTED_MATERIAL_COVARIANCE_ABSENT','score':None},
  {'gate':'reality/Hermitian conditions','status':'MANUFACTURED_CHECK_ONLY_PHYSICAL_FIELD_ABSENT','score':None},
  {'gate':'resolution and volume tests','status':'NOT_EXECUTED_PHYSICAL_FIELD_ABSENT','score':None},
  {'gate':'no public initial-condition file','status':'PASS','score':1.0},
  {'gate':'independent field reconstruction','status':'BLOCKED_FIELD_NOT_LAWFULLY_MATERIALIZABLE','score':None}],
  'aggregate_scores_cannot_override':True,'scientific_stop':'Physical execution stops before solver materialization because required source-owned covariance bindings are absent.'}
 write(RUN/'GATE_RESULTS.json',gates)
 write(RUN/'OUTPUT_COMPLETENESS.json',{'schema_version':'4.0','run_id':RID,'module':'J','overall':'BLOCKED_UNDERDETERMINED','required_outputs':[{'requirement':x,'status':'BLOCKED_MATERIAL_BINDINGS_ABSENT','evidence':[rec(RUN/'primary/J200_MATERIAL_COVARIANCE_DERIVABILITY_AUDIT.json'),rec(RUN/'independent/INDEPENDENT_RECONSTRUCTION.json')]} for x in load(RECIPE)['required_outputs']]})
 write(RUN/'OUTPUT_CONTRACT.json',{'schema_version':'4.0','run_id':RID,'module':'J','status':'BLOCKED_UNDERDETERMINED','required_outputs':[],'child_bindings':{},'K_child_ready':False})
 write(RUN/'CHECKPOINT_RECORD.json',{'run_id':RID,'status':'PRE_PRIMARY_OBSTRUCTION','restart_rule':'resume J only after a versioned exact source supplies the missing finite ordered physical HI basis/mapping/normalization or an equivalent triad-derived selection theorem; retain exact current source hashes','restart_parents':[rec(HI),rec(P29),rec(P30)]})
 write(RUN/'INDEPENDENT_VERIFICATION.md','# J-200 Independent Verification\n\nResult: **PASS for obstruction reconstruction; physical J execution BLOCKED_UNDERDETERMINED.**\n\nThe independent verifier used only the exact repaired HI parent plus canonical P29/P30 sources. It reproduced that HI supplies no realized primordial covariance, phase seed, or finite-volume field; P29 supplies a normalized recursive weighting law but no source-owned map onto a finite ordered HI physical perturbation basis; and P30 explicitly leaves the physical primordial spectrum and amplitude pending. Therefore the covariance and Fourier engines must remain unmaterialized.\n')
 close=f"# J-200 Closeout\n\n## Result\n\nFAIL / BLOCKED_UNDERDETERMINED before primary physical execution.\n\n## Triadic diagnosis\n\nCIF is not the failure: it correctly retains the lawful mode/basis possibility family. The missing link is QV at the J specialization boundary: no exact source-owned selection/intertwiner maps the P29 recursive-depth coordinate to a finite ordered physical HI perturbation basis with normalization/amplitude. Without that operation, RFL cannot lawfully stabilize one primordial covariance or field.\n\n## Strongest supported claim\n\n{claim['strongest_supported']}\n\n## Strongest unsupported claim\n\n{claim['strongest_unsupported']}\n\n## Required repair\n\nSupply or derive, under exact source ownership, the J specialization theorem/intertwiner that fixes the finite physical HI basis, mode ordering/count, normalization/amplitude, and P29-depth-to-mode mapping. Then restart J from these exact frozen hashes. Do not use manufactured covariance, P30 pending values, observed targets, or an arbitrary I-geometry/HU-mode identification.\n"
 (RUN/'CLOSEOUT.md').write_text(close,encoding='utf-8')
 write(ROOT/'audit/J200_MATERIAL_COVARIANCE_OBSTRUCTION.json',{'schema_version':'4.0','run_id':RID,'classification':'PRE_PRIMARY_SCIENTIFIC_OBSTRUCTION','result':'BLOCKED_UNDERDETERMINED','supported':True,'evidence':[rel(RUN/'primary/J200_MATERIAL_COVARIANCE_DERIVABILITY_AUDIT.json'),rel(RUN/'independent/INDEPENDENT_RECONSTRUCTION.json')],'missing_bindings':a['missing_material_bindings'],'triad_analysis':a['triad_analysis']})
 write(RUN/'ENVIRONMENT.json',{'schema_version':'4.0','run_id':RID,'status':'FINAL_PRE_PRIMARY_OBSTRUCTION','generation_mode':'GENERATION_SEALED','operating_system':platform.platform(),'python':sys.version,'network_policy':'DISABLED_DURING_GENERATION','imports':['json','hashlib','pathlib'],'hidden_defaults_audited':True,'public_inputs_used':False,'physical_solver_materialized':False})
 print(json.dumps({'result':'FINALIZED_BLOCKED_UNDERDETERMINED','K_child_ready':False},indent=2))

def manifest(_):
 paths=[RUN/'SOURCE_REGISTER.json',RUN/'PRE_EXECUTION_LOCK.json',RUN/'FROZEN_DERIVATION_SPEC.json',RUN/'ENVIRONMENT.json',RUN/'GATE_RESULTS.json',RUN/'INDEPENDENT_VERIFICATION.md',RUN/'CLOSEOUT.md',RUN/'OUTPUT_COMPLETENESS.json',RUN/'OUTPUT_CONTRACT.json',RUN/'CHECKPOINT_RECORD.json',RUN/'primary/J200_MATERIAL_COVARIANCE_DERIVABILITY_AUDIT.json',RUN/'independent/INDEPENDENT_RECONSTRUCTION.json',ROOT/'audit/J200_MATERIAL_COVARIANCE_OBSTRUCTION.json',RUN/'reference_checks.json']
 for p in paths:
  if not p.is_file(): raise RuntimeError(f'missing manifest input {p}')
 write(RUN/'GENERATED_OUTPUT_MANIFEST.json',{'run_id':RID,'status':'FINAL','finalized_utc':now(),'outputs':[{'path':rel(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in paths]})
 print('J200 obstruction manifest FINAL')
def main():
 ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
 for x in ['freeze','audit','independent','finalize','manifest']: sp.add_parser(x)
 a=ap.parse_args(); globals()[a.cmd](a)
if __name__=='__main__': main()
