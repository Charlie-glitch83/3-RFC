#!/usr/bin/env bash
set -euo pipefail

BRANCH='agent/frontier-050-execution'

python -m pip install --disable-pip-version-check -r requirements-lock.txt

python - <<'PY'
import json
s=json.load(open('STATE.json'))
assert s['active_work_unit']=='C-125',s
assert s['current_module']=='C',s
assert s['current_run'] is None,s
assert s['modules']['B']['evidence_state']=='FROZEN' and s['modules']['B']['fidelity']=='PRODUCTION',s['modules']['B']
assert s['modules']['C']['evidence_state']=='FROZEN' and s['modules']['C']['fidelity']=='MINIMAL_SPINE',s['modules']['C']
PY

bash bootstrap.sh
bash tools/start_work.sh

python - <<'PY'
import json
from pathlib import Path
s=json.load(open('STATE.json'))
rid=s['current_run']
assert s['active_work_unit']=='C-125' and s['current_module']=='C',s
assert rid and rid.startswith('C-125-'),s
run=Path('modules/C/runs')/rid
assert run.is_dir(),run
packet=Path('work_packets/ACTIVE_WORK_PACKET.md').read_text(encoding='utf-8')
assert '# ACTIVE WORK PACKET — C-125' in packet,packet[:300]
assert str(run) in packet,packet[:600]
for name in ['RUN_PLAN.md','SOURCE_REGISTER.json','PRE_EXECUTION_LOCK.json','ENVIRONMENT.json','CHECKPOINT_RECORD.json','GENERATED_OUTPUT_MANIFEST.json','OUTPUT_COMPLETENESS.json','OUTPUT_CONTRACT.json','REPLAY_RECORD.json','GATE_RESULTS.json','INDEPENDENT_VERIFICATION.md','CLOSEOUT.md','FROZEN_RECIPE.json','WORK_ORDER.md','REQUIRED_GATES.json','WOLFRAM_SEQUENCE.md','LOCAL_EXECUTION_BINDINGS.json','RUN_LOCAL_PHASE.sh']:
    assert (run/name).exists(),run/name
print(rid)
PY

python tools/director.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan
python tools/rfc.py context

git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
git add STATE.json memory/RUN_INDEX.json memory/CURRENT_CONTEXT.md work_packets/ACTIVE_WORK_PACKET.md modules/C
if git diff --cached --quiet; then
  echo 'HARD STOP: C125 startup produced no governed changes'
  exit 1
fi
git commit -m 'Start C-125 superseding microscopic replay from H_B_to_C_v2'
git fetch origin "$BRANCH"
git rebase "origin/$BRANCH"
git push origin HEAD:"$BRANCH"
sha=$(git rev-parse HEAD)
remote=$(git ls-remote origin "refs/heads/$BRANCH" | awk '{print $1}')
test "$remote" = "$sha"
echo "C125_STARTUP_SHA=$sha"
