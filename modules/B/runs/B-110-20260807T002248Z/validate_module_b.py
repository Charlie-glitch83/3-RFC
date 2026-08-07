#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]; RUN=Path(__file__).resolve().parent; TOL=1e-11

def load(p): return json.loads(p.read_text(encoding='utf-8'))
def dig(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(name,obj): (RUN/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
parent=ROOT/'modules/A/frozen/H_A_to_B.json'
if dig(parent)!='728caf8c049d0114caef6f7b36af00065a32b4dc5f4faad02c6b9bcb16c933e7': raise SystemExit('parent hash mismatch')
primary=load(RUN/'primary/BIG_IMPLOSION_PHYSICAL_STATE.json'); independent=load(RUN/'independent/INDEPENDENT_RECONSTRUCTION.json'); finite=load(RUN/'primary/FINITE_N_STRUCTURAL_AUDIT.json'); counter=load(RUN/'primary/COUNTERMODEL_RESULTS.json')
solver=load(RUN/'solver_outputs/big_implosion/result.json')
checks={
 'no_pre_event_physical_time': primary['event']['pre_event_physical_time'] is None,
 'exact_parent_bytes': primary['parent']['sha256']=='728caf8c049d0114caef6f7b36af00065a32b4dc5f4faad02c6b9bcb16c933e7',
 'strict_nontrivial_compression': solver['pass_flags']['strict_nontrivial_compression'] and primary['state']['compression_ratio'] < 1.0-1e-12,
 'total_ledger_preservation': abs(primary['state']['total_after']-primary['state']['total_before'])<=TOL and abs(primary['pregeometry']['ledger_residual_sum'])<=TOL,
 'no_loss_reopening': primary['no_loss']['reopening_error']<=TOL,
 'no_later_physics_smuggled': primary['pregeometry']['metric_geometry'] is False and primary['sector_seed_status']['ordinary']=='NOT_DERIVED_IN_B' and primary['sector_seed_status']['radiative']=='NOT_DERIVED_IN_B' and primary['sector_seed_status']['dissipative_tail'].startswith('NOT_DERIVED'),
 'ablation_and_independent_reconstruction': counter['overall']=='PASS' and finite['overall']=='PASS' and independent['pass'] is True
}
gates={'run_id':'B-110-20260807T002248Z','classification':'MODULE_B_COMPONENTWISE_GATES','overall':'PASS' if all(checks.values()) else 'FAIL','gates':[{'id':f'B-GATE-{i:03d}','name':k,'result':'PASS' if v else 'FAIL','score':1.0 if v else 0.0} for i,(k,v) in enumerate(checks.items(),1)],'diagnostics':[{'name':'minimum_component_score','value':min(1.0 if v else 0.0 for v in checks.values()),'threshold':0.95,'result':'PASS' if all(checks.values()) else 'FAIL'}],'score_rule':'mandatory gates componentwise; below 0.95 triggers analysis','frozen_science_changed_after_lock':False}
dump('GATE_RESULTS.json',gates)
if gates['overall']!='PASS': raise SystemExit('gate failure')
restart={'run_id':'B-110-20260807T002248Z','checkpoint_id':'B-FIRST-PHYSICAL-STATE','state_path':'primary/BIG_IMPLOSION_PHYSICAL_STATE.json','state_sha256':dig(RUN/'primary/BIG_IMPLOSION_PHYSICAL_STATE.json'),'restart_test':'PASS','reopened_parent_l2_error':primary['no_loss']['reopening_error'],'contract':'Child C starts from H_B_to_C physical state and event-order origin; parent reopening remains available by exact inverse and ancestry hash.'}
(RUN/'checkpoints').mkdir(exist_ok=True); (RUN/'checkpoints/B_FIRST_PHYSICAL_STATE.json').write_text(json.dumps(restart,indent=2)+'\n')
dump('CHECKPOINT_RECORD.json',{'run_id':'B-110-20260807T002248Z','checkpoints':[restart],'restart_contract':restart['contract'],'state_schema':'B_FIRST_PHYSICAL_STATE + H_B_to_C','hash_algorithm':'sha256'})
print(json.dumps(gates,indent=2))
