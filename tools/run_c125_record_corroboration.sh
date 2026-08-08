#!/usr/bin/env bash
set -euo pipefail

BRANCH='agent/frontier-050-execution'
RUN_ID='C-125-20260808T063500Z'
RUN="modules/C/runs/$RUN_ID"

python - <<'PY'
import hashlib,json
from pathlib import Path
s=json.load(open('STATE.json')); R=Path('modules/C/runs/C-125-20260808T063500Z')
assert s['current_run']=='C-125-20260808T063500Z' and s['active_work_unit']=='C-125',s
lock=json.load(open(R/'PRE_EXECUTION_LOCK.json'))
assert lock['status']=='FROZEN' and lock['frozen_before_primary_execution'] is True,lock
for c in ['C-WL-001','C-WL-002']:
    run_input=R/'wolfram'/c/'input.wl'; recipe=Path('recipes/C/wolfram')/(c+'.wl')
    assert hashlib.sha256(run_input.read_bytes()).hexdigest()==hashlib.sha256(recipe.read_bytes()).hexdigest(),c
    assert (R/'wolfram'/c/'output.txt').is_file(),c
assert not (R/'primary/MICROSCOPIC_CONSTITUTION_V2.json').exists()
PY

python tools/director.py wolfram-record --run "$RUN_ID" --call C-WL-001 --output "$RUN/wolfram/C-WL-001/output.txt"
python tools/director.py wolfram-record --run "$RUN_ID" --call C-WL-002 --output "$RUN/wolfram/C-WL-002/output.txt"
python - <<'PY'
import json
from pathlib import Path
R=Path('modules/C/runs/C-125-20260808T063500Z')
for c in ['C-WL-001','C-WL-002']:
    g=json.load(open(R/'wolfram'/c/'gate.json'))
    assert g['status']=='PASS_WITH_MANUAL_INTERPRETATION',(c,g)
# Preserve the failed manufactured attempt in the run failure ledger.
f=R/'FAILURES.jsonl'; text=f.read_text(encoding='utf-8') if f.exists() else ''
rec={'failure_id':'C125-WL-002-STALE-MANUFACTURED-EXAMPLE','run_id':'C-125-20260808T063500Z','gate':'C-WL-002 manufactured symmetry audit','category':'POST_LOCK_PRE_PRIMARY_IMPLEMENTATION_ONLY_CORRECTION','description':'Original fixed manufactured matrix did not commute with its generator and did not emit the fields required by the registered generic continuous-symmetry solver gate. Failed input/output preserved; current generic solver matches the already-registered purpose and expectation.','changes_frozen_science':False,'required_replay_scope':'full post-lock C matrix','strongest_claim_remaining':'No primary C claim was made before correction.'}
import json as _j
if rec['failure_id'] not in text:
    with f.open('a',encoding='utf-8') as h: h.write(_j.dumps(rec,separators=(',',':'))+'\n')
PY

python tools/run_reference_checks.py --module C --output "$RUN/reference_checks.json"
rm -rf "$RUN/solver_outputs/spectral_model"
python tools/run_configured_solver.py --config "$RUN/solver_configs/C_spectral_model.json" --output-dir "$RUN/solver_outputs/spectral_model"
python - <<'PY'
import json
R='modules/C/runs/C-125-20260808T063500Z'
assert json.load(open(R+'/reference_checks.json'))['overall']=='PASS'
res=json.load(open(R+'/solver_outputs/spectral_model/result.json'))
assert res['success'] is True,res
assert not __import__('pathlib').Path(R+'/primary/MICROSCOPIC_CONSTITUTION_V2.json').exists()
PY

python tools/rfc.py doctor
python tools/director.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan

git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
git add -A
git commit -m 'Record C-125 post-lock Wolfram and spectral corroboration'
git fetch origin "$BRANCH"
git rebase "origin/$BRANCH"
git push origin HEAD:"$BRANCH"
SHA=$(git rev-parse HEAD)
remote=$(git ls-remote origin "refs/heads/$BRANCH" | awk '{print $1}')
test "$remote" = "$SHA"
echo "C125_CORROBORATION_SHA=$SHA"
