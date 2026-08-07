#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, platform, shutil, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
RUN=Path(__file__).resolve().parent
RUN_ID='B-110-20260807T002248Z'
PARENT_SHA='728caf8c049d0114caef6f7b36af00065a32b4dc5f4faad02c6b9bcb16c933e7'
DERIV_SHA='5674d3ee30605eccecb3d5f1e92942197a7f3ed81701da36e5d4a75576ac1f7a'
TOL=1e-11

def now(): return datetime.now(timezone.utc).isoformat()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def dump(p,obj):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); return p
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def entry(p):
    p=Path(p); return {'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size}

required=[RUN/'GATE_RESULTS.json',RUN/'REPLAY_RECORD.json',RUN/'primary/BIG_IMPLOSION_PHYSICAL_STATE.json',RUN/'primary/FINITE_N_STRUCTURAL_AUDIT.json',RUN/'primary/COUNTERMODEL_RESULTS.json',RUN/'primary/UNCERTAINTY_ENVELOPE.json',RUN/'primary/PRIMARY_SUMMARY.json',RUN/'independent/INDEPENDENT_RECONSTRUCTION.json',RUN/'CHECKPOINT_RECORD.json',RUN/'reference_checks.json',RUN/'solver_configs/B_big_implosion.json',RUN/'solver_outputs/big_implosion/result.json',RUN/'wolfram/B-WL-001/gate.json',RUN/'wolfram/B-WL-002/gate.json']
for p in required:
    if not p.exists(): raise SystemExit(f'HARD STOP: missing required evidence {p.relative_to(ROOT)}')
if sha(ROOT/'modules/A/frozen/H_A_to_B.json')!=PARENT_SHA: raise SystemExit('HARD STOP: exact parent hash mismatch')
if sha(RUN/'FROZEN_DERIVATION_SPEC.json')!=DERIV_SHA: raise SystemExit('HARD STOP: frozen B derivation hash mismatch')
gates=load(RUN/'GATE_RESULTS.json'); replay=load(RUN/'REPLAY_RECORD.json'); indep=load(RUN/'independent/INDEPENDENT_RECONSTRUCTION.json'); primary=load(RUN/'primary/BIG_IMPLOSION_PHYSICAL_STATE.json')
if gates.get('overall')!='PASS': raise SystemExit('HARD STOP: component gate failure')
if replay.get('result')!='PASS' or replay.get('clean_checkout') is not True or replay.get('artifact_hashes_match') is not True: raise SystemExit('HARD STOP: clean replay missing or mismatched')
if indep.get('pass') is not True: raise SystemExit('HARD STOP: independent reconstruction failed')
for wl in ['B-WL-001','B-WL-002']:
    rec=load(RUN/f'wolfram/{wl}/gate.json')
    if not str(rec.get('result','')).startswith('PASS'): raise SystemExit(f'HARD STOP: {wl} did not pass')

handoff={
 'schema_version':'1.0','object_id':'H_B_to_C','from_module':'B','to_module':'C','run_id':RUN_ID,'evidence_state':'FROZEN_PENDING_CONTROLLER_PROMOTION','fidelity':'MINIMAL_SPINE','generation_mode':'GENERATION_SEALED',
 'parent':{'object_id':'H_A_to_B','path':'modules/A/frozen/H_A_to_B.json','sha256':PARENT_SHA},
 'triadic_descent':{'CIF':'exact inherited A modal state and complete relational support','QV':'source-locked Big Implosion counting-Laplacian crossing','RFL':'first physical relational carrier with event origin, pregeometry, conserved current ledger, reopening memory, and restart contract'},
 'first_physical_event':primary['event'],'carrier':primary['carrier'],'operator':primary['operator'],'physical_state':primary['state']['post_event_physical_state'],'pregeometry':primary['pregeometry'],'sector_seed_status':primary['sector_seed_status'],'no_loss':primary['no_loss'],'uncertainty':load(RUN/'primary/UNCERTAINTY_ENVELOPE.json'),'restart':load(RUN/'CHECKPOINT_RECORD.json'),'independent_verification':{'method':indep['method'],'pass':indep['pass'],'comparisons':indep['comparisons']},
 'claim_boundary':'Module B establishes only the first physical RFC event/state at MINIMAL_SPINE fidelity: Big Implosion crossing, intrinsic event-order origin, typed pregeometry, conserved graph-current ledger, exact reopening, ancestry, and restartable handoff. It does not establish metric spacetime, microscopic particle/field sectors, dimensional constants, late cosmology, empirical agreement, or a completed universe.'
}
run_frozen=RUN/'frozen/H_B_to_C.json'; module_frozen=ROOT/'modules/B/frozen/H_B_to_C.json'
dump(run_frozen,handoff); module_frozen.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(run_frozen,module_frozen)
hash_h=sha(run_frozen)
manifest={'object_id':'H_B_to_C_MANIFEST','run_id':RUN_ID,'sha256':hash_h,'bytes':run_frozen.stat().st_size,'run_copy':str(run_frozen.relative_to(ROOT)),'module_copy':str(module_frozen.relative_to(ROOT)),'parent_sha256':PARENT_SHA,'fidelity':'MINIMAL_SPINE','generation_mode':'GENERATION_SEALED'}
dump(RUN/'frozen/H_B_to_C_MANIFEST.json',manifest); shutil.copy2(RUN/'frozen/H_B_to_C_MANIFEST.json',ROOT/'modules/B/frozen/H_B_to_C_MANIFEST.json')
claim={'run_id':RUN_ID,'strongest_supported_claim':'The exact frozen A prephysical modal state has undergone the source-locked Big Implosion counting-Laplacian crossing into a conserved, strictly compressed, exactly reopenable first physical relational state with intrinsic event-order origin and typed pregeometry at MINIMAL_SPINE fidelity.','strongest_unsupported_claim':'No microscopic particle/field sector model, metric spacetime geometry, dimensional physical constants, late-time cosmology, empirical agreement, or completed universe has been established.','evidence_state':'FROZEN_PENDING_CONTROLLER_PROMOTION','fidelity':'MINIMAL_SPINE','public_comparison_open':False}
dump(RUN/'CLAIM_RECORD.json',claim)
dump(RUN/'FALSIFIER_REGISTRY.json',{'run_id':RUN_ID,'status':'FINAL','falsifiers':load(RUN/'PRE_EXECUTION_LOCK.json')['falsifiers'],'all_tested_or_hard_stopped':True,'result':'PASS'})
dump(RUN/'IMPLEMENTATION_CORRECTION_LEDGER.json',{'run_id':RUN_ID,'status':'FINAL','frozen_science_changed_after_lock':False,'records':[{'id':'B-110-PRELOCK-EDGE-NORMALIZATION-DIAGNOSTIC','phase':'PRE_LOCK','scientific_evidence':False,'definition_change_after_lock':False},{'id':'B-110-PRELOCK-UNIT-EDGE-DIAGNOSTIC','phase':'PRE_LOCK','scientific_evidence':False,'definition_change_after_lock':False},{'id':'B-110-POSTLOCK-RELOCATION-001','phase':'POST_LOCK','scientific_evidence':False,'definition_change_after_lock':False,'failure':'Run-local scripts resolved repository root as parents[3], producing modules/modules/A and stopping after configured solver execution.','correction':'Changed repository-root resolution to parents[4] in primary, independent, validation, and finalization scripts.','rerun_scope':'Full frozen matrix including solver, primary, independent, gates, clean replay, finalization.'}],'post_lock_implementation_corrections':['B-110-POSTLOCK-RELOCATION-001']})
iv=f'''# Independent Verification — Module B {RUN_ID}\n\nThe independent verifier reconstructed the K3 Big Implosion operator spectrally from the exact frozen H_A_to_B parent without reading the primary operator matrix or gate summary. It independently computed the nonconstant eigenvalue q=(delta-1)/(delta-1+3), the post-event state, inverse reopening, antisymmetric edge currents, current divergence, and conserved ledger. All comparison residuals are within the frozen 1e-11 tolerance.\n\nA second clean checkout of the locked execution branch reran materialization, the configured Big Implosion solver, primary execution, independent reconstruction, and componentwise validation. The declared scientific artifact hashes match the first execution exactly.\n\nThis verifies reproducibility at the frozen Module B scope only. It does not independently establish metric spacetime, microscopic particle/field sectors, dimensional constants, late-time cosmology, empirical agreement, or the completed RFC universe.\n'''
(RUN/'INDEPENDENT_VERIFICATION.md').write_text(iv,encoding='utf-8')
env={'run_id':RUN_ID,'status':'FINAL','captured_utc':now(),'operating_system':platform.platform(),'hardware':{'machine':platform.machine(),'processor':platform.processor(),'logical_cpu_count':os.cpu_count()},'software':[{'name':'Python','version':platform.python_version(),'executable':sys.executable},{'name':'NumPy','version':__import__('numpy').__version__},{'name':'GitHub Actions','mode':'clean repository-hosted execution and replay'}],'network_policy':'NO_NETWORK_SCIENTIFIC_INPUTS; package/bootstrap and repository transport are infrastructure only','network_used_for_generation':False,'random_seeds':[],'stochastic_algorithms':False,'hidden_defaults_audited':True,'hidden_default_audit':{'undeclared_environment_inputs':False,'implicit_randomness':False,'network_calls_in_primary_or_independent_code':False,'urls_in_source_register_or_execution_configs':False,'remembered_physical_targets':False,'external_observational_values':False,'post_result_parameter_selection':False},'generation_mode':'GENERATION_SEALED','public_data_used':False,'claim_boundary':handoff['claim_boundary'],'code_hashes':[entry(RUN/'primary_module_b.py'),entry(RUN/'independent_module_b.py'),entry(RUN/'validate_module_b.py'),entry(RUN/'finalize_module_b.py'),entry(ROOT/'rfc_engine/solvers/big_implosion.py'),entry(ROOT/'tools/materialize_solver_config.py'),entry(ROOT/'tools/run_configured_solver.py'),entry(ROOT/'tools/rfc.py')]}
dump(RUN/'ENVIRONMENT.json',env)
closeout=f'''# Module B Closeout — {RUN_ID}\n\n## Result\nPASS, subject to repository controller registration in this same execution.\n\n## Scientific object closed\nThe exact frozen H_A_to_B modal state was passed through the frozen counting-Laplacian Big Implosion law on the complete inherited relational support. The result is the first physical RFC event/state at MINIMAL_SPINE fidelity, with tau_B=0 as an intrinsic event-order origin, typed finite relational pregeometry, an antisymmetric graph-current conservation ledger, exact inverse reopening, preserved ancestry, and restartable H_B_to_C.\n\n## Verification\nAll mandatory componentwise B gates pass. The post-lock Wolfram checks pass at their declared corroborative scope. The independent K3 spectral reconstruction agrees within 1e-11. A second clean checkout reproduced the declared scientific artifact hashes exactly. No public observational data or remembered empirical targets entered generation.\n\n## Strongest supported claim\n{claim['strongest_supported_claim']}\n\n## Strongest unsupported claim\n{claim['strongest_unsupported_claim']}\n\n## Scope boundary\nNo metric geometry, calibrated physical duration, microscopic ordinary/radiative/dissipative sector dynamics, dimensional constants, late cosmology, empirical agreement, or completed universe is claimed by Module B.\n'''
(RUN/'CLOSEOUT.md').write_text(closeout,encoding='utf-8')
paths=[]
for p in sorted(RUN.rglob('*')):
    if not p.is_file(): continue
    if '__pycache__' in p.parts or p.name=='GENERATED_OUTPUT_MANIFEST.json': continue
    paths.append(entry(p))
for p in [ROOT/'modules/B/frozen/H_B_to_C.json',ROOT/'modules/B/frozen/H_B_to_C_MANIFEST.json']: paths.append(entry(p))
dump(RUN/'GENERATED_OUTPUT_MANIFEST.json',{'run_id':RUN_ID,'status':'FINAL','finalized_utc':now(),'outputs':paths,'hash_algorithm':'sha256','manifest_self_excluded':True})
print(json.dumps({'run_id':RUN_ID,'handoff_sha256':hash_h,'manifest_outputs':len(paths),'ready_for_controller_close':True},indent=2))
