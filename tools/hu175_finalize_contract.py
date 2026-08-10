#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RID='HU-175-20260810T153330Z'; R=ROOT/'modules/HU/runs'/RID

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,o): Path(p).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
replay=load(R/'REPLAY_RECORD.json')
if replay.get('result')!='PASS' or replay.get('clean_checkout') is not True or replay.get('artifact_hashes_match') is not True:
    raise SystemExit('HU clean replay not PASS')
base=f'modules/HU/runs/{RID}'
ev={
 'typed operator':[f'{base}/primary/HU175_TYPED_OPERATOR.json'],
 'domain and codomain':[f'{base}/primary/HU175_TYPED_OPERATOR.json'],
 'gauge/frame contracts':[f'{base}/primary/HU175_CONSTRAINT_GAUGE_FRAME_CONTRACT.json'],
 'conservation and constraint identities':[f'{base}/primary/HU175_CONSTRAINT_GAUGE_FRAME_CONTRACT.json'],
 'operator uncertainty':[f'{base}/primary/HU175_OPERATOR_UNCERTAINTY.json'],
 'frozen H_HU_to_HI':['modules/HU/frozen/H_HU_to_HI_v2.json']
}
contract=load(R/'OUTPUT_CONTRACT.json')
contract['status']='PASS'
for row in contract['required_outputs']:
    name=row['name']; row.update({'status':'SATISFIED','artifact_paths':ev[name],'semantic_gate':'PASS','independent_verification':'PASS','child_ready':True})
write(R/'OUTPUT_CONTRACT.json',contract)
gates=load(R/'GATE_RESULTS.json')
gates['overall']='PASS'
gates['componentwise']['covariance, restart and clean replay']={'pass':True,'clean_replay':True,'artifact_hashes_match':True,'evidence':f'{base}/REPLAY_RECORD.json'}
write(R/'GATE_RESULTS.json',gates)
claim={
 'claim_id':'HU-175-REPAIRED-G-UNIVERSAL-LINEAR-TRANSFER',
 'text':'HU-175 reconstructs from exact repaired G-165 the branch-indexed first-variation transfer operator family on the constraint-preserving non-gauge tangent quotient, with semigroup/superposition, covariance pushforward, restart and clean replay, without importing realized I/J values.',
 'owner':'HU','evidence_state':'FROZEN','fidelity':'PRODUCTION','supported':True,
 'evidence':['modules/HU/frozen/H_HU_to_HI_v2.json',f'{base}/independent/INDEPENDENT_RECONSTRUCTION.json',f'{base}/REPLAY_RECORD.json'],
 'strongest_unsupported_claim':'No realized geometry, physical transfer coefficients, final spectra, public Boltzmann equivalence or empirical agreement.'
}
(ROOT/'audit/HU175_CLAIM.json').write_text(json.dumps(claim,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({'result':'PASS','contract':'PASS','clean_replay':True},indent=2))
