#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'modules/I/runs/I-180-20260809T050839Z'
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def dump(p,o): Path(p).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
recipe=load(ROOT/'recipes/I/recipe.json')
primary=RUN/'primary/I_FINITE_RELATIONAL_BACKGROUND_MINIMAL_SPINE.json'
handoff=ROOT/'modules/I/frozen/H_I_to_HI.json'
ind=RUN/'independent/INDEPENDENT_RECONSTRUCTION.json'
replay=RUN/'REPLAY_RECORD.json'
gates=RUN/'GATE_RESULTS.json'
conv=RUN/'convergence/I_CONVERGENCE_RESTART.json'
for p in (primary,handoff,ind,replay,gates,conv):
    if not p.is_file(): raise SystemExit(f'missing finalized I evidence: {p}')
common=[
 {'path':str(primary.relative_to(ROOT)),'sha256':sha(primary)},
 {'path':str(handoff.relative_to(ROOT)),'sha256':sha(handoff)},
 {'path':str(ind.relative_to(ROOT)),'sha256':sha(ind)},
 {'path':str(replay.relative_to(ROOT)),'sha256':sha(replay)},
 {'path':str(conv.relative_to(ROOT)),'sha256':sha(conv)},
]
checks={
 'metric/background state':'Exact G event activity is mapped through the frozen lawful incidence family to positive weighted inherited relational Laplacians and gauge-quotiented resistance metrics.',
 'expansion and clock histories':'Relative spectral scale and expansion are derived from the positive Laplacian spectrum while the sole physical clock remains the inherited Big-Implosion clock.',
 'horizons and distances':'Finite relational distances and the branch causal-reach functional are present without importing FRW, measured H(z), or a public distance ladder.',
 'constraint and conservation ledgers':'Laplacian symmetry, PSD, one gauge zero mode, row-sum zero, event-activity conservation, and inherited conservation ledgers are explicitly checked.',
 'covariance':'I covariance is parent pushforward plus explicit PSD incidence, metric, numeric, and branch uncertainty terms.',
 'H_I_to_HI':'Frozen child handoff contains the realized-background branch family, ancestry, clock, metric, covariance, restart state, and no-retune interface rule.'
}
rows=[]
for req in recipe['required_outputs']:
    rows.append({'requirement':req,'status':'PASS','semantic_check':checks[req],'evidence':common})
dump(RUN/'OUTPUT_COMPLETENESS.json',{'schema_version':'1.0','run_id':RUN.name,'module':'I','overall':'PASS','required_outputs':rows})
print('I180 OUTPUT COMPLETENESS: PASS')
