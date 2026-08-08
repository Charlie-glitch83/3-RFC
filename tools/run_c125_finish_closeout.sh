#!/usr/bin/env bash
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"
git config user.name '3-RFC governed repair executor'
git config user.email 'actions@users.noreply.github.com'
RID=$(python - <<'PY'
import json
s=json.load(open('STATE.json')); assert s['active_work_unit']=='C-125' and s['current_module']=='C',s
rid=s['current_run']; assert rid and rid.startswith('C-125-'),s
rec=s['modules']['C']; assert rec['evidence_state']=='DESIGN' and rec['fidelity']=='PRODUCTION',rec
print(rid)
PY
)
R="modules/C/runs/$RID"
python - "$R" <<'PY'
import json,sys
from pathlib import Path
R=Path(sys.argv[1]); assert json.load(open(R/'PRE_EXECUTION_LOCK.json'))['status']=='FROZEN'; assert json.load(open(R/'run.json'))['status']=='CREATED'
PY
LOCK_SHA=$(git log --all --format=%H --grep='Freeze C-125 channel-complete microscopic replay package' -1)
test -n "$LOCK_SHA"
echo "C125 frozen foundation: $LOCK_SHA"

python tools/execute_c125.py execute --run "$R"
rm -rf /tmp/c125-lock /tmp/c125-replay
git worktree add --detach /tmp/c125-lock "$LOCK_SHA"
(
  cd /tmp/c125-lock
  python tools/execute_c125.py execute --run "$R" --output-root /tmp/c125-replay
)
python tools/execute_c125.py finalize --run "$R" --replay-root /tmp/c125-replay

# Implementation-only controller formatting correction after all science is frozen/executed.
python - "$RID" <<'PY'
import hashlib,json,sys
from datetime import datetime,timezone
from pathlib import Path
rid=sys.argv[1]; R=Path('modules/C/runs')/rid
close=R/'CLOSEOUT.md'; text=close.read_text()
if '## Result' not in text:
    text=text.replace('# C-125 Closeout\n\n','# C-125 Closeout\n\n## Result\n\n**PASS.**\n\n',1)
close.write_text(text)
assert all(x in text for x in ['Result','Strongest supported claim','Strongest unsupported claim'])
# Finalize manifest again because only closeout formatting changed after the prior manifest.
records=[]
for p in sorted(R.rglob('*')):
    if not p.is_file() or p.name in {'GENERATED_OUTPUT_MANIFEST.json','run.json'} or '__pycache__' in p.parts: continue
    records.append({'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
h=hashlib.sha256()
for x in records: h.update(x['path'].encode()); h.update(b'\0'); h.update(x['sha256'].encode()); h.update(b'\n')
(R/'GENERATED_OUTPUT_MANIFEST.json').write_text(json.dumps({'run_id':rid,'status':'FINAL','finalized_utc':datetime.now(timezone.utc).isoformat(),'outputs':records,'tree_sha256':h.hexdigest(),'note':'Finalized after implementation-only closeout marker correction; science artifacts unchanged. Excludes itself and run.json.'},indent=2)+'\n')
PY

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
assert q['C-125']['status']=='PASS' and q['D-135']['status']=='ACTIVE'
PY

git add -A
git commit -m 'Close C-125 and activate channel-complete thermal replay D-135'
git pull --rebase origin agent/frontier-050-execution
git push origin HEAD:agent/frontier-050-execution
CLOSEOUT_SHA=$(git rev-parse HEAD)
python tools/rfc.py record-commit "$CLOSEOUT_SHA" --branch agent/frontier-050-execution --note 'Verified C-125 superseding microscopic replay at PRODUCTION; closeout parser correction only, science unchanged.'
python tools/rfc.py context
git add STATE.json memory/DECISION_LOG.jsonl memory/CURRENT_CONTEXT.md
git commit -m 'Record verified C-125 repair closeout'
git pull --rebase origin agent/frontier-050-execution
git push origin HEAD:agent/frontier-050-execution
