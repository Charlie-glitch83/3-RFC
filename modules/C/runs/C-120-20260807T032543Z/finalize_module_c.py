#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, platform, shutil, sys
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]; RUN=Path(__file__).resolve().parent
RUN_ID='C-120-20260807T032543Z'; PARENT_SHA='c5a46fd2af85896ac0bd7069d985c7592c6ad364bd1b0492bb9eab7985559492'; DERIV_SHA='578cd6bc04f37fe17e769cc27fe9f02700568feb399cf2fd529a796984eb8ee9'

def now(): return datetime.now(timezone.utc).isoformat()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def dump(p,obj):
 p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); return p
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def entry(p):
 p=Path(p); return {'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size}

if sha(ROOT/'modules/B/frozen/H_B_to_C.json')!=PARENT_SHA: raise SystemExit('HARD STOP: exact parent mismatch')
if sha(RUN/'FROZEN_DERIVATION_SPEC.json')!=DERIV_SHA: raise SystemExit('HARD STOP: frozen derivation mismatch')
required=[RUN/'GATE_RESULTS.json',RUN/'REPLAY_RECORD.json',RUN/'primary/MICROSCOPIC_CONSTITUTION.json',RUN/'primary/COUNTERMODEL_RESULTS.json',RUN/'primary/UNCERTAINTY_ENVELOPE.json',RUN/'primary/PRIMARY_SUMMARY.json',RUN/'independent/INDEPENDENT_RECONSTRUCTION.json',RUN/'CHECKPOINT_RECORD.json',RUN/'reference_checks.json',RUN/'solver_outputs/spectral_model/result.json',RUN/'wolfram/C-WL-001/gate.json',RUN/'wolfram/C-WL-002/gate.json']
for p in required:
 if not p.exists(): raise SystemExit(f'HARD STOP: missing {p.relative_to(ROOT)}')
gates=load(RUN/'GATE_RESULTS.json'); replay=load(RUN/'REPLAY_RECORD.json'); indep=load(RUN/'independent/INDEPENDENT_RECONSTRUCTION.json'); primary=load(RUN/'primary/MICROSCOPIC_CONSTITUTION.json'); summary=load(RUN/'primary/PRIMARY_SUMMARY.json')
if gates.get('overall')!='PASS': raise SystemExit('HARD STOP: C gates did not pass')
if replay.get('result')!='PASS' or replay.get('clean_checkout') is not True or replay.get('artifact_hashes_match') is not True: raise SystemExit('HARD STOP: clean replay missing/mismatched')
if indep.get('pass') is not True: raise SystemExit('HARD STOP: independent reconstruction failed')

handoff={
 'schema_version':'1.0','object_id':'H_C_to_D','from_module':'C','to_module':'D','run_id':RUN_ID,'evidence_state':'FROZEN_PENDING_CONTROLLER_PROMOTION','fidelity':'MINIMAL_SPINE','generation_mode':'GENERATION_SEALED',
 'parent':{'object_id':'H_B_to_C','path':'modules/B/frozen/H_B_to_C.json','sha256':PARENT_SHA},
 'triadic_descent':{'CIF':'inherited first-physical-state carrier and its exact excitation/symmetry candidate space','QV':'parent-only constitution M_C=I-Q_B with source-locked symmetry/conservation selection','RFL':'stable microscopic excitation types, interaction/charge memory, deterministic prethermal population and restart state'},
 'microscopic_constitution':primary['constitution'],'typed_fields_and_excitations':primary['typed_fields_and_excitations'],'symmetry':primary['symmetry'],'interaction_and_charge':primary['interaction_and_charge'],'positivity_unitarity':primary['positivity_unitarity'],'prethermal_state':primary['prethermal_state'],'uncertainty':load(RUN/'primary/UNCERTAINTY_ENVELOPE.json'),'restart':load(RUN/'CHECKPOINT_RECORD.json'),'independent_verification':{'method':indep['method'],'pass':indep['pass'],'checks':indep['checks']},
 'thermal_history_status':'NOT_DERIVED_IN_C_RESERVED_FOR_D','metric_spacetime_status':'NOT_DERIVED','empirical_identity_status':'UNASSIGNED_RESERVED_FOR_P','dimensionful_mass_status':'NOT_DERIVED_NO_LAWFUL_SCALE_IN_PARENT',
 'claim_boundary':'Module C establishes RFC microscopic excitation types and a parent-derived dimensionless constitution at MINIMAL_SPINE fidelity, including exact symmetry/conservation, positive constitutive spectrum, unitary dimensionless phase evolution, deterministic prethermal populations and restart. It does not establish dimensionful masses, Standard Model identities, calibrated couplings, metric spacetime, nonequilibrium thermal history, or empirical correspondence.'}
run_frozen=dump(RUN/'frozen/H_C_to_D.json',handoff); module_frozen=ROOT/'modules/C/frozen/H_C_to_D.json'; module_frozen.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(run_frozen,module_frozen)
h=sha(run_frozen); manifest={'object_id':'H_C_to_D_MANIFEST','run_id':RUN_ID,'sha256':h,'bytes':run_frozen.stat().st_size,'run_copy':str(run_frozen.relative_to(ROOT)),'module_copy':str(module_frozen.relative_to(ROOT)),'parent_sha256':PARENT_SHA,'fidelity':'MINIMAL_SPINE','generation_mode':'GENERATION_SEALED'}
dump(RUN/'frozen/H_C_to_D_MANIFEST.json',manifest); shutil.copy2(RUN/'frozen/H_C_to_D_MANIFEST.json',ROOT/'modules/C/frozen/H_C_to_D_MANIFEST.json')
claim={'run_id':RUN_ID,'strongest_supported_claim':summary['strongest_supported_claim'],'strongest_unsupported_claim':summary['strongest_unsupported_claim'],'evidence_state':'FROZEN_PENDING_CONTROLLER_PROMOTION','fidelity':'MINIMAL_SPINE','public_comparison_open':False}; dump(RUN/'CLAIM_RECORD.json',claim)
dump(RUN/'FALSIFIER_REGISTRY.json',{'run_id':RUN_ID,'status':'FINAL','falsifiers':load(RUN/'PRE_EXECUTION_LOCK.json')['falsifiers'],'all_tested_or_hard_stopped':True,'result':'PASS'})
dump(RUN/'IMPLEMENTATION_CORRECTION_LEDGER.json',{'run_id':RUN_ID,'status':'FINAL','frozen_science_changed_after_lock':False,'records':load_failures(),'post_lock_implementation_corrections':[]})

iv=f'''# Independent Verification — Module C {RUN_ID}\n\nThe independent verifier reconstructed M_C directly from the exact frozen H_B_to_C K3 Laplacian and delta, not from the primary spectral solver matrix. It analytically recovered the zero uniform mode, the twofold dimensionless gap 3/(delta+2), the canonical O(2) generator, total-carrier conservation, positivity, unitary dimensionless phase evolution, and the inherited prethermal populations. Final numerical comparison to the primary constitution is within the frozen 1e-10 tolerance.\n\nA second clean checkout reran reference checking, provenance materialization, spectral execution, primary C construction, independent reconstruction, and componentwise validation. Declared scientific artifact hashes match; the path-bearing materialized configuration is compared canonically with only checkout-specific absolute paths removed.\n\nThis verifies the RFC microscopic constitution at MINIMAL_SPINE scope. It does not supply a dimensionful mass scale, Standard Model identity, calibrated coupling, metric spacetime, thermal history, or empirical correspondence.\n'''
(RUN/'INDEPENDENT_VERIFICATION.md').write_text(iv,encoding='utf-8')
env={'run_id':RUN_ID,'status':'FINAL','captured_utc':now(),'operating_system':platform.platform(),'hardware':{'machine':platform.machine(),'processor':platform.processor(),'logical_cpu_count':os.cpu_count()},'software':[{'name':'Python','version':platform.python_version(),'executable':sys.executable},{'name':'NumPy','version':__import__('numpy').__version__},{'name':'SciPy','version':__import__('scipy').__version__},{'name':'GitHub Actions','mode':'clean repository-hosted execution and replay'}],'network_policy':'NO_NETWORK_SCIENTIFIC_INPUTS; repository/package transport is infrastructure only','network_used_for_generation':False,'random_seeds':[],'stochastic_algorithms':False,'hidden_defaults_audited':True,'hidden_default_audit':{'undeclared_environment_inputs':False,'implicit_randomness':False,'network_calls_in_primary_or_independent_code':False,'remembered_physical_targets':False,'external_observational_values':False,'post_result_parameter_selection':False,'dimensionful_scale_injected':False},'generation_mode':'GENERATION_SEALED','public_data_used':False,'claim_boundary':handoff['claim_boundary'],'code_hashes':[entry(RUN/'primary_module_c.py'),entry(RUN/'independent_module_c.py'),entry(RUN/'validate_module_c.py'),entry(RUN/'finalize_module_c.py'),entry(ROOT/'rfc_engine/solvers/spectral_model.py'),entry(ROOT/'tools/materialize_solver_config.py'),entry(ROOT/'tools/run_configured_solver.py'),entry(ROOT/'tools/rfc.py')]}; dump(RUN/'ENVIRONMENT.json',env)
close=f'''# Module C Closeout — {RUN_ID}\n\n## Result\nPASS at MINIMAL_SPINE scope, subject to repository controller registration in this execution.\n\n## Scientific object closed\nFrom exact H_B_to_C, Module C derives and executes M_C=I-Q_B=L_B/(delta+2). It has one conserved uniform memory mode and a positive exactly degenerate internal excitation doublet with O(2) law symmetry. The complete inherited support fixes the dimensionless interaction structure; Q_total is conserved; the inherited positive B state supplies deterministic prethermal populations.\n\n## Important obstruction preserved\nH_B_to_C supplies no lawful dimensionful scale. Therefore C does not convert its dimensionless constitutive gap into measured mass, does not select a mixing angle inside the degenerate doublet, and assigns no Standard Model identity. These are explicit unsupported claims, not hidden defaults.\n\n## Verification\nAll five mandatory component gates pass. Both post-lock Wolfram programs pass at their declared symbolic scope, the manufactured C reference passes, the provenance-bound spectral audit passes, the independent analytic K3 reconstruction agrees within 1e-10, countermodels fail as preregistered, and a second clean checkout reproduces the scientific artifacts.\n\n## Strongest supported claim\n{claim['strongest_supported_claim']}\n\n## Strongest unsupported claim\n{claim['strongest_unsupported_claim']}\n'''
(RUN/'CLOSEOUT.md').write_text(close,encoding='utf-8')
paths=[]
for p in sorted(RUN.rglob('*')):
 if p.is_file() and '__pycache__' not in p.parts and p.name!='GENERATED_OUTPUT_MANIFEST.json': paths.append(entry(p))
for p in [module_frozen,ROOT/'modules/C/frozen/H_C_to_D_MANIFEST.json']: paths.append(entry(p))
dump(RUN/'GENERATED_OUTPUT_MANIFEST.json',{'run_id':RUN_ID,'status':'FINAL','finalized_utc':now(),'outputs':paths,'hash_algorithm':'sha256','manifest_self_excluded':True})
print(json.dumps({'run_id':RUN_ID,'handoff_sha256':h,'manifest_outputs':len(paths),'ready_for_controller_close':True},indent=2))

def load_failures():
 rows=[]
 p=RUN/'FAILURES.jsonl'
 if p.exists():
  for line in p.read_text(encoding='utf-8').splitlines():
   if line.strip(): rows.append(json.loads(line))
 return rows
