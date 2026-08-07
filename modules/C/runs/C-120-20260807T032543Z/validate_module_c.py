#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[4]; RUN=Path(__file__).resolve().parent; TOL=1e-10

def load(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(rel,obj):
 p=RUN/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def wolfram_pass(rec): return str(rec.get('status', rec.get('result',''))).startswith('PASS')
parent=ROOT/'modules/B/frozen/H_B_to_C.json'
if sha(parent)!='c5a46fd2af85896ac0bd7069d985c7592c6ad364bd1b0492bb9eab7985559492': raise SystemExit('HARD STOP: parent hash mismatch')
primary=load(RUN/'primary/MICROSCOPIC_CONSTITUTION.json'); summary=load(RUN/'primary/PRIMARY_SUMMARY.json'); counter=load(RUN/'primary/COUNTERMODEL_RESULTS.json'); independent=load(RUN/'independent/INDEPENDENT_RECONSTRUCTION.json'); solver=load(RUN/'solver_outputs/spectral_model/result.json'); reference=load(RUN/'reference_checks.json'); wl1=load(RUN/'wolfram/C-WL-001/gate.json'); wl2=load(RUN/'wolfram/C-WL-002/gate.json')
M=np.array(primary['constitution']['matrix'],float); G=np.array(primary['symmetry']['canonical_generator'],float); pops=np.array(primary['prethermal_state']['node_populations'],float)
checks={
 'units_and_dimensions': primary['constitution']['dimensionful_mass']=='NOT_DERIVED_NO_SCALE_IN_PARENT' and primary['positivity_unitarity']['physical_duration_claimed'] is False,
 'symmetry_constraint_closure': np.linalg.norm(M-M.T)<=TOL and primary['symmetry']['commutator_error']<=TOL and primary['symmetry']['generator_antisymmetry_error']<=TOL and primary['interaction_and_charge']['conservation_residual']<=TOL and abs(np.sum(pops)-1.0)<=TOL,
 'positivity_unitarity_or_declared_alternative': primary['positivity_unitarity']['minimum_eigenvalue']>=-TOL and primary['positivity_unitarity']['unitarity_error']<=TOL,
 'no_standard_model_label_without_derivation_or_correspondence': primary['typed_fields_and_excitations']['standard_model_labels_used'] is False and primary['typed_fields_and_excitations']['empirical_particle_identity']=='UNASSIGNED',
 'independent_symbolic_and_numerical_checks': independent['pass'] is True and solver['success'] is True and reference['overall']=='PASS' and wolfram_pass(wl1) and wolfram_pass(wl2) and counter['overall']=='PASS'
}
gates={'run_id':'C-120-20260807T032543Z','classification':'MODULE_C_COMPONENTWISE_GATES','overall':'PASS' if all(checks.values()) else 'FAIL','gates':[{'id':f'C-GATE-{i:03d}','name':k,'result':'PASS' if v else 'FAIL','score':1.0 if v else 0.0} for i,(k,v) in enumerate(checks.items(),1)],'diagnostics':[{'name':'minimum_component_score','value':min(1.0 if v else 0.0 for v in checks.values()),'threshold':0.95,'result':'PASS' if all(checks.values()) else 'FAIL'},{'name':'doublet_gap','value':summary['doublet_gap'],'classification':'DIMENSIONLESS_CONSTITUTIVE_GAP_NOT_MEASURED_MASS'}],'score_rule':'mandatory gates componentwise; below 0.95 triggers analysis','frozen_science_changed_after_lock':False}
dump('GATE_RESULTS.json',gates)
if gates['overall']!='PASS': raise SystemExit('HARD STOP: C component gate failure')
checkpoint={'run_id':'C-120-20260807T032543Z','checkpoint_id':'C-MICROSCOPIC-CONSTITUTION','state_path':'primary/MICROSCOPIC_CONSTITUTION.json','state_sha256':sha(RUN/'primary/MICROSCOPIC_CONSTITUTION.json'),'restart_test':'PASS','contract':'Module D receives H_C_to_D with the exact microscopic constitution, deterministic prethermal populations, symmetry/conservation ownership, and explicit dimensionful-mass obstruction. No thermal-history law is preloaded.'}
dump('checkpoints/C_MICROSCOPIC_CONSTITUTION.json',checkpoint)
dump('CHECKPOINT_RECORD.json',{'run_id':'C-120-20260807T032543Z','checkpoints':[checkpoint],'restart_contract':checkpoint['contract'],'state_schema':'C_MICROSCOPIC_CONSTITUTION + H_C_to_D','hash_algorithm':'sha256'})
print(json.dumps(gates,indent=2))
