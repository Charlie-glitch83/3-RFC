#!/usr/bin/env bash
set -euo pipefail
RUN_ID="C-125-20260808T063010Z"
RUN="modules/C/runs/${RUN_ID}"

python - <<'PY'
import json
s=json.load(open('STATE.json')); r=json.load(open('modules/C/runs/C-125-20260808T063010Z/run.json'))
assert s['active_work_unit']=='C-125' and s['current_module']=='C' and s['current_run']=='C-125-20260808T063010Z',s
assert s['modules']['C']['evidence_state']=='DESIGN' and s['modules']['C']['fidelity']=='PRODUCTION',s['modules']['C']
assert r['status']=='CREATED',r
assert json.load(open('modules/C/runs/C-125-20260808T063010Z/PRE_EXECUTION_LOCK.json'))['status']=='FROZEN'
print('C125_CLOSEOUT_SHAPE_REPAIR_PRECONDITION_PASS')
PY

LOCK_SHA=$(git log -n1 --format=%H -- "$RUN/PRE_EXECUTION_LOCK.json")
test -n "$LOCK_SHA"
echo "Frozen preexecution commit: $LOCK_SHA"

# Full frozen primary matrix, unchanged.
python tools/run_reference_checks.py --module C --output "$RUN/reference_checks.json"
rm -rf "$RUN/solver_outputs/spectral_model"
mkdir -p "$RUN/solver_outputs/spectral_model"
python tools/run_configured_solver.py --config "$RUN/solver_configs/C_spectral_model.json" --output-dir "$RUN/solver_outputs/spectral_model"
python tools/execute_c125.py execute --run "$RUN"
python - <<'PY'
import json
R='modules/C/runs/C-125-20260808T063010Z'
assert json.load(open(R+'/reference_checks.json'))['overall']=='PASS'
assert json.load(open(R+'/solver_outputs/spectral_model/result.json'))['success'] is True
assert json.load(open(R+'/GATE_RESULTS.json'))['overall']=='PASS'
assert json.load(open(R+'/independent/INDEPENDENT_RECONSTRUCTION.json'))['pass'] is True
PY

# Exact detached replay from the frozen preexecution commit.
rm -rf /tmp/c125-lock /tmp/c125-replay
git worktree add --detach /tmp/c125-lock "$LOCK_SHA"
(
 cd /tmp/c125-lock
 python tools/execute_c125.py execute --run "$RUN" --output-root /tmp/c125-replay
)
python tools/execute_c125.py finalize --run "$RUN" --replay-root /tmp/c125-replay

# Implementation-only closeout-shape normalization required by tools/rfc.py.
python - <<'PY'
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
R=Path('modules/C/runs/C-125-20260808T063010Z')
h=json.load(open('modules/C/frozen/H_C_to_D_v2.json'))
g=json.load(open(R/'GATE_RESULTS.json'))
ind=json.load(open(R/'independent/INDEPENDENT_RECONSTRUCTION.json'))
rep=json.load(open(R/'REPLAY_RECORD.json'))
text=f'''# C-125 Closeout

- Run ID: C-125-20260808T063010Z
- Work unit: C-125
- Module: C
- Result: PASS
- Evidence state reached: FROZEN
- Fidelity reached: PRODUCTION

## Scientific objects produced

Channel-complete finite-relational microscopic constitution and versioned `H_C_to_D_v2`, including typed matter/gauge roles, `U(1) x SU(2) x SU(3)` symmetry, anomaly-free charge registry, three completed shell generations, source-owned mass/mixing and interaction/rate operators, protected photon zero mode, neutrino family, bound proton/neutron roles, prethermal populations, covariance, restart state and exact ancestry.

## Componentwise gate results

All frozen C-125 component gates PASS. Aggregate scoring cannot override the componentwise result. Generic reference/spectral machinery is corroborative only; the load-bearing result is the parent/source-derived C theorem replay.

## Failures preserved and corrections made

The earlier blank C startup shell remains preserved. A path-only dispatcher defect wrote temporary C artifacts at repository root and was corrected without changing frozen definitions, equations, sources, tolerances, gates, falsifiers or claim scope. A final closeout serialization correction adds the repository-standard section markers only.

## Independent reconstruction

The independent verifier reconstructs the finite C realization from exact `H_B_to_C_v2`, the exact A kernel and recovered C theorem sources without trusting the primary gate summary. Result: {'PASS' if ind.get('pass') else 'FAIL'}.

## Replay/restart/convergence evidence

Detached clean replay from the frozen preexecution commit is `{'PASS' if rep.get('result')=='PASS' and rep.get('artifact_hashes_match') else 'FAIL'}`. The frozen C restart packet is exported in `H_C_to_D_v2`; the corroborative spectral audit and theorem reconstruction both pass.

## Strongest supported claim

{h['strongest_supported_claim']}

## Strongest unsupported claim

{h['strongest_unsupported_claim']}

## Remaining gaps

D-135 must freshly execute nonequilibrium thermal/transport history from this exact C packet. No measured particle calibration, public thermal history, BBN, recombination or empirical agreement is claimed here.

## Exact next child

`D-135`, and only `D-135`, after controller registration of this PASS.
'''
(R/'CLOSEOUT.md').write_text(text,encoding='utf-8')
# Rebuild the final manifest because CLOSEOUT.md changed after the original finalizer.
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
rows=[]
for p in sorted(R.rglob('*')):
    if not p.is_file() or p.name in {'GENERATED_OUTPUT_MANIFEST.json','run.json'} or '__pycache__' in p.parts: continue
    rows.append({'path':str(p.relative_to(R)),'sha256':sha(p),'bytes':p.stat().st_size})
th=hashlib.sha256()
for x in rows:
    th.update(x['path'].encode()); th.update(b'\0'); th.update(x['sha256'].encode()); th.update(b'\n')
(R/'GENERATED_OUTPUT_MANIFEST.json').write_text(json.dumps({'run_id':R.name,'status':'FINAL','finalized_utc':datetime.now(timezone.utc).isoformat(),'outputs':rows,'tree_sha256':th.hexdigest(),'note':'Rebuilt after implementation-only closeout serialization normalization; excludes itself and controller-owned run.json.'},indent=2)+'\n')
PY

python tools/rfc.py doctor
python tools/director.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan
python tools/rfc.py close-run --run-id "$RUN_ID" --result PASS --closeout "$RUN/CLOSEOUT.md"
python tools/rfc.py promote-module C --to FORMALIZED --fidelity PRODUCTION --evidence "$RUN/FROZEN_DERIVATION_SPEC.json"
python tools/rfc.py promote-module C --to IMPLEMENTED --fidelity PRODUCTION --evidence "$RUN/primary/MICROSCOPIC_CONSTITUTION_V2.json"
python tools/rfc.py promote-module C --to VERIFIED --fidelity PRODUCTION --evidence "$RUN/GATE_RESULTS.json"
python tools/rfc.py promote-module C --to PHYSICALLY_EXECUTED --fidelity PRODUCTION --evidence "$RUN/primary/MICROSCOPIC_CONSTITUTION_V2.json"
python tools/rfc.py promote-module C --to INDEPENDENTLY_REPRODUCED --fidelity PRODUCTION --evidence "$RUN/independent/INDEPENDENT_RECONSTRUCTION.json"
python tools/rfc.py promote-module C --to FROZEN --fidelity PRODUCTION --evidence modules/C/frozen/H_C_to_D_v2.json
python tools/rfc.py freeze modules/C/frozen/H_C_to_D_v2.json --kind MODULE_HANDOFF
python tools/rfc.py record-claim --file "$RUN/CLAIM_RECORD.json"
python tools/rfc.py advance --task C-125 --result PASS --evidence "$RUN/CLOSEOUT.md" --note 'Verified C-125 channel-complete microscopic replay from exact H_B_to_C_v2; activate only D-135.'
python tools/rfc.py context
python tools/rfc.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan
python - <<'PY'
import json
s=json.load(open('STATE.json')); q={x['id']:x for x in json.load(open('WORK_QUEUE.json'))['items']}
assert s['active_work_unit']=='D-135' and s['current_module']=='D' and s['current_run'] is None,s
assert s['modules']['C']['evidence_state']=='FROZEN' and s['modules']['C']['fidelity']=='PRODUCTION',s['modules']['C']
assert q['C-125']['status']=='PASS' and q['D-135']['status']=='ACTIVE' and q['E-145']['status']=='BLOCKED',q
PY

git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
git add -A
git commit -m 'Close verified C-125 and activate D-135'
git pull --rebase origin agent/frontier-050-execution
git push origin HEAD:agent/frontier-050-execution
CLOSE_SHA=$(git rev-parse HEAD)
git fetch origin agent/frontier-050-execution
test "$(git rev-parse origin/agent/frontier-050-execution)" = "$CLOSE_SHA"
python tools/rfc.py record-commit "$CLOSE_SHA" --branch agent/frontier-050-execution --note 'Verified C-125 channel-complete microscopic replay, exact parent/source lineage, clean replay, complete D child contract, PRODUCTION evidence ladder and one-child activation D-135.'
python tools/rfc.py context
python tools/rfc.py doctor
git add STATE.json memory/DECISION_LOG.jsonl memory/CURRENT_CONTEXT.md
git commit -m 'Record verified C-125 superseding closeout'
git pull --rebase origin agent/frontier-050-execution
git push origin HEAD:agent/frontier-050-execution

echo "C125_CLOSEOUT_COMPLETE $(git rev-parse HEAD)"
