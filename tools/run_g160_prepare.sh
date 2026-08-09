#!/usr/bin/env bash
set -euo pipefail
RUN_ID='G-160-20260809T025252Z'
R="modules/G/runs/$RUN_ID"
BRANCH='agent/frontier-050-execution'
python -m pip install --disable-pip-version-check -r requirements-lock.txt
python - <<'PY'
import json
s=json.load(open('STATE.json'))
assert s['active_work_unit']=='G-160' and s['current_module']=='G' and s['current_run']=='G-160-20260809T025252Z',s
assert s['modules']['F']['evidence_state']=='FROZEN' and s['modules']['F']['fidelity']=='PRODUCTION',s['modules']['F']
assert s['modules']['G']['evidence_state']=='BLOCKED',s['modules']['G']
PY
python tools/rfc.py reopen-module G --fidelity MINIMAL_SPINE --evidence recovery/BG_SUPERSEDING_LINEAGE_PACKET.md
python tools/g160_parent_bound.py prepare --run "$R"
python tools/director.py doctor
python tools/rfc.py firewall-scan
git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
git add "$R" STATE.json memory/DECISION_LOG.jsonl tools/g160_parent_bound.py tools/run_g160_prepare.sh
git commit -m 'Freeze G-160 pre-execution state'
git pull --rebase origin "$BRANCH"
git push origin HEAD:"$BRANCH"
printf 'G160_PRE_EXECUTION_COMMIT=%s\n' "$(git rev-parse HEAD)"
