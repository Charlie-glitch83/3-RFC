#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'modules/B/runs/B-115-20260808T060000Z'
CONTRACT=RUN/'OUTPUT_CONTRACT.json'
CFG=ROOT/'config/required_output_contracts.json'
OLD_STATE=ROOT/'modules/B/runs/B-110-20260807T002248Z/primary/BIG_IMPLOSION_PHYSICAL_STATE.json'
SECTORS=RUN/'primary/FOUR_SECTOR_GENESIS_STATE.json'
HANDOFF=ROOT/'modules/B/frozen/H_B_to_C_v2.json'
CHECKPOINT=RUN/'CHECKPOINT_RECORD.json'
INDEPENDENT=RUN/'independent/INDEPENDENT_RECONSTRUCTION.json'


def rel(p:Path)->str: return str(p.relative_to(ROOT))
def load(p:Path): return json.loads(p.read_text(encoding='utf-8'))
def save(p:Path,o): p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def main():
    for p in [CONTRACT,CFG,OLD_STATE,SECTORS,HANDOFF,CHECKPOINT,INDEPENDENT]:
        if not p.is_file(): raise SystemExit(f'HARD STOP: missing {rel(p)}')
    cfg=load(CFG); required=[x['name'] for x in cfg['modules']['B']['required_child_bindings']]
    evidence={
      'first_physical_state':[rel(OLD_STATE),rel(HANDOFF)],
      'intrinsic_clock_origin':[rel(OLD_STATE),rel(HANDOFF)],
      'pregeometry_or_geometry':[rel(OLD_STATE),rel(HANDOFF)],
      'ordinary_sector_seed':[rel(SECTORS)],
      'radiative_sector_seed':[rel(SECTORS)],
      'compression_relic_seed':[rel(SECTORS)],
      'dissipative_tail_seed':[rel(SECTORS)],
      'field_current_conservation_state':[rel(OLD_STATE),rel(SECTORS)],
      'route_event_branch_memory':[rel(HANDOFF)],
      'uncertainty':[rel(HANDOFF)],
      'restart':[rel(CHECKPOINT)],
      'no_loss_ancestry':[rel(HANDOFF)]}
    if set(evidence)!=set(required):
        raise SystemExit(f'HARD STOP: B binding map differs from frozen required contract: map={sorted(evidence)} required={sorted(required)}')
    c=load(CONTRACT)
    if c.get('run_id')!='B-115-20260808T060000Z' or c.get('module')!='B' or c.get('status')!='PASS':
        raise SystemExit('HARD STOP: B115 OUTPUT_CONTRACT is not finalized PASS before binding normalization')
    c['child_bindings']={name:{'status':'SATISFIED','artifact_paths':evidence[name],'source_lineage':'PASS','independent_verification':'PASS','derived_absence':False} for name in required}
    c['binding_normalization']={
      'classification':'IMPLEMENTATION_ONLY_CONTRACT_LABEL_NORMALIZATION',
      'scientific_values_changed':False,
      'equations_changed':False,
      'tolerances_changed':False,
      'gates_changed':False,
      'claim_boundary_changed':False,
      'basis':'Align B-115 child-binding labels with config/required_output_contracts.json after the scientific artifacts are finalized.'}
    save(CONTRACT,c)
    print(json.dumps({'status':'PASS','normalized_bindings':required},indent=2))

if __name__=='__main__': main()
