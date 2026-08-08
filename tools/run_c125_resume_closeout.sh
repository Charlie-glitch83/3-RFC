#!/usr/bin/env bash
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
git config user.name '3-RFC governed repair executor'
git config user.email 'actions@users.noreply.github.com'

RID=$(python - <<'PY'
import json
s=json.load(open('STATE.json'))
assert s['active_work_unit']=='C-125' and s['current_module']=='C',s
rid=s['current_run']; assert rid and rid.startswith('C-125-'),s
print(rid)
PY
)
R="modules/C/runs/$RID"

python - <<'PY'
import json
s=json.load(open('STATE.json'))
rec=s['modules']['C']
assert rec['evidence_state']=='FROZEN' and rec['fidelity']=='MINIMAL_SPINE',rec
PY
python tools/rfc.py reopen-module C --fidelity PRODUCTION --evidence recovery/BG_SUPERSEDING_LINEAGE_PACKET.md
python tools/director.py prepare-active
python tools/execute_c125.py prepare --run "$R"
python tools/rfc.py context
python tools/rfc.py doctor
python tools/director.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan

git add -A
git commit -m 'Freeze C-125 channel-complete microscopic replay package'
git pull --rebase origin agent/frontier-050-execution
git push origin HEAD:agent/frontier-050-execution
LOCK_SHA=$(git rev-parse HEAD)
echo "C125_LOCK_SHA=$LOCK_SHA"

git fetch origin agent/frontier-050-execution
git reset --hard origin/agent/frontier-050-execution
python tools/execute_c125.py execute --run "$R"
rm -rf /tmp/c125-lock /tmp/c125-replay
git worktree add --detach /tmp/c125-lock "$LOCK_SHA"
(
  cd /tmp/c125-lock
  python tools/execute_c125.py execute --run "$R" --output-root /tmp/c125-replay
)
python tools/execute_c125.py finalize --run "$R" --replay-root /tmp/c125-replay

python tools/scientific_completion_guard.py --run "$R"
python tools/rfc.py doctor
python tools/director.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan

python tools/rfc.py close-run --run-id "$RID" --result PASS --closeout "$R/CLOSEOUT.md"
python tools/rfc.py promote-module C --to FORMALIZED --fidelity PRODUCTION --evidence "$R/FROZEN_DERIVATION_SPEC.json"
python tools/rfc.py promote-module C --to IMPLEMENTED --fidelity PRODUCTION --evidence "$R/primary/MICROSCOPIC_CONSTITUTION_V2.json"
python tools/rfc.py promote-module C --to VERIFIED --fidelity PRODUCTION --evidence "$R/GATE_RESULTS.json"
python tools/rfc.py promote-module C --to PHYSICALLY_EXECUTED --fidelity PRODUCTION --evidence "$R/primary/MICROSCOPIC_CONSTITUTION_V2.json"
python tools/rfc.py promote-module C --to INDEPENDENTLY_REPRODUCED --fidelity PRODUCTION --evidence "$R/independent/INDEPENDENT_RECONSTRUCTION.json"
python tools/rfc.py promote-module C --to FROZEN --fidelity PRODUCTION --evidence modules/C/frozen/H_C_to_D_v2.json
python tools/rfc.py freeze modules/C/frozen/H_C_to_D_v2.json --kind MODULE_HANDOFF
python tools/rfc.py record-claim --file "$R/CLAIM_RECORD.json"
python tools/rfc.py advance --task C-125 --result PASS --evidence "$R/CLOSEOUT.md" --note 'Channel-complete C replay closed; activate only D-135 for nonequilibrium thermal replay.'
python tools/rfc.py context
python tools/rfc.py doctor
python tools/director.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan
python - <<'PY'
import json
s=json.load(open('STATE.json')); q={x['id']:x for x in json.load(open('WORK_QUEUE.json'))['items']}
assert s['active_work_unit']=='D-135' and s['current_module']=='D' and s['current_run'] is None,s
assert s['modules']['C']['evidence_state']=='FROZEN' and s['modules']['C']['fidelity']=='PRODUCTION',s['modules']['C']
assert q['C-125']['status']=='PASS' and q['D-135']['status']=='ACTIVE' and q['E-145']['status']=='BLOCKED'
PY

git add -A
git commit -m 'Close C-125 and activate channel-complete thermal replay D-135'
git pull --rebase origin agent/frontier-050-execution
git push origin HEAD:agent/frontier-050-execution
CLOSEOUT_SHA=$(git rev-parse HEAD)
python tools/rfc.py record-commit "$CLOSEOUT_SHA" --branch agent/frontier-050-execution --note 'Verified C-125 superseding microscopic replay at PRODUCTION with exact B-v2/A ancestry, child-ready D contract, clean replay and independent reconstruction.'
python tools/rfc.py context
git add STATE.json memory/DECISION_LOG.jsonl memory/CURRENT_CONTEXT.md
git commit -m 'Record verified C-125 repair closeout'
git pull --rebase origin agent/frontier-050-execution
git push origin HEAD:agent/frontier-050-execution

git fetch origin agent/frontier-050-execution
git reset --hard origin/agent/frontier-050-execution
python - <<'PY'
import json
s=json.load(open('STATE.json'))
assert s['active_work_unit']=='D-135' and s['current_module']=='D' and s['current_run'] is None,s
assert s['modules']['C']['evidence_state']=='FROZEN' and s['modules']['C']['fidelity']=='PRODUCTION'
PY
python tools/rfc.py doctor
