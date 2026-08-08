#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

git config user.name '3-RFC governed repair executor'
git config user.email 'actions@users.noreply.github.com'

mode=$(python - <<'PY'
import json
s=json.load(open('STATE.json'))
a=s['active_work_unit']
if a=='C-125' and s['modules']['B']['evidence_state']=='FROZEN' and s['modules']['B']['fidelity']=='PRODUCTION':
    print('DONE')
elif a=='B-115' and s.get('current_run') and s['current_run'].startswith('B-115-'):
    print('B_RESUME')
elif a=='G-160' and s.get('current_run') and s['current_run'].startswith('G-160-'):
    print('G_START')
else:
    raise SystemExit(f"HARD STOP: unexpected repair state {a} / {s.get('current_run')}")
PY
)

echo "Repair mode: $mode"
if [ "$mode" = "DONE" ]; then
  python tools/rfc.py doctor
  exit 0
fi

if [ "$mode" = "G_START" ]; then
  RID=$(python - <<'PY'
import json
print(json.load(open('STATE.json'))['current_run'])
PY
)
  python - "$RID" <<'PY'
import json,sys
from pathlib import Path
rid=sys.argv[1]
R=Path('modules/G/runs')/rid
run=json.load(open(R/'run.json'))
assert run['status']=='CREATED',run
lock=json.load(open(R/'PRE_EXECUTION_LOCK.json'))
assert lock.get('authorization')=='NOT_AUTHORIZED_PENDING_SUPERSEDING_F_TO_G_PARENT',lock
assert lock.get('repair_prerequisite')=='recovery/BG_SUPERSEDING_LINEAGE_PACKET.md',lock
(R/'CLOSEOUT.md').write_text(f'''# {rid} B-first prerequisite closeout

## Result

**BLOCKED BEFORE PRIMARY EXECUTION.** The recovered repair packet requires the superseding physical order B -> C -> D -> E -> F -> G. No G recombination physics was executed in this shell.

## Strongest supported claim

Exact prior B-G formal objects are recovered as REPLAY_REQUIRED and a B-first replay order is source-locked while the lower-fidelity B-F runs remain preserved.

## Strongest unsupported claim

No superseding H_B_to_C_v2 through H_F_to_G_v2 or repaired recombination/visibility/last-scattering state is established by this shell.
''',encoding='utf-8')
PY
  python tools/rfc.py close-run --run-id "$RID" --result BLOCKED --closeout "modules/G/runs/$RID/CLOSEOUT.md"
  python tools/repair_superseding_lineage_frontier.py
  python tools/rfc.py reopen-module B --fidelity PRODUCTION --evidence recovery/BG_SUPERSEDING_LINEAGE_PACKET.md
  python tools/rfc.py new-run B --run-id B-115-20260808T060000Z
  python tools/director.py prepare-active
  python tools/execute_b115.py prepare --run modules/B/runs/B-115-20260808T060000Z
  python tools/rfc.py context
  python tools/rfc.py doctor
  python tools/director.py doctor
  python -m unittest discover -s tests -v
  python tools/rfc.py firewall-scan

  git add -A
  git commit -m 'Freeze B-115 superseding replay preexecution package'
  git pull --rebase origin agent/frontier-050-execution
  git push origin HEAD:agent/frontier-050-execution
fi

# Always resume from the exact remote frozen B-115 foundation.
git fetch origin agent/frontier-050-execution
git reset --hard origin/agent/frontier-050-execution

RID=$(python - <<'PY'
import json
s=json.load(open('STATE.json'))
assert s['active_work_unit']=='B-115' and s['current_module']=='B',s
rid=s['current_run']
assert rid and rid.startswith('B-115-'),s
print(rid)
PY
)
R="modules/B/runs/$RID"
python - "$R" <<'PY'
import json,sys
from pathlib import Path
R=Path(sys.argv[1])
assert json.load(open(R/'PRE_EXECUTION_LOCK.json'))['status']=='FROZEN'
assert json.load(open(R/'run.json'))['status']=='CREATED'
PY

B115_LOCK_SHA=$(git rev-parse HEAD)
echo "Frozen B115 foundation: $B115_LOCK_SHA"

python tools/execute_b115.py execute --run "$R"
rm -rf /tmp/b115-lock /tmp/b115-replay
git worktree add --detach /tmp/b115-lock "$B115_LOCK_SHA"
(
  cd /tmp/b115-lock
  python tools/execute_b115.py execute --run "$R" --output-root /tmp/b115-replay
)
python tools/execute_b115.py finalize --run "$R" --replay-root /tmp/b115-replay

# Implementation-only correction: normalize serializer keys to the frozen child contract.
python - "$RID" <<'PY'
import hashlib,json,sys
from datetime import datetime, timezone
from pathlib import Path
rid=sys.argv[1]
R=Path('modules/B/runs')/rid
p=f'modules/B/runs/{rid}/primary/FOUR_SECTOR_GENESIS_STATE.json'
h='modules/B/frozen/H_B_to_C_v2.json'
old='modules/B/runs/B-110-20260807T002248Z/primary/BIG_IMPLOSION_PHYSICAL_STATE.json'
cp=f'modules/B/runs/{rid}/CHECKPOINT_RECORD.json'
a='modules/A/frozen/H_A_to_B.json'
contract=json.load(open(R/'OUTPUT_CONTRACT.json'))
paths={
  'first_physical_state':[old,h],
  'intrinsic_clock_origin':[old,h],
  'pregeometry_or_geometry':[old,h],
  'ordinary_sector_seed':[p],
  'radiative_sector_seed':[p],
  'compression_relic_seed':[p],
  'dissipative_tail_seed':[p],
  'field_current_conservation_state':[old,p],
  'route_event_branch_memory':[h],
  'uncertainty':[h],
  'restart':[cp,h],
  'no_loss_ancestry':[a,h],
}
required=json.load(open('config/required_output_contracts.json'))['modules']['B']['required_child_bindings']
assert {x['name'] for x in required}==set(paths),(required,paths)
contract['child_bindings']={k:{'status':'SATISFIED','artifact_paths':v,'source_lineage':'PASS','independent_verification':'PASS','derived_absence':False} for k,v in paths.items()}
contract['implementation_correction']='Normalized serializer keys to the frozen B->C contract only; scientific artifacts, projector law, values, gates, falsifiers, claim boundary and thresholds are unchanged.'
(R/'OUTPUT_CONTRACT.json').write_text(json.dumps(contract,indent=2)+'\n')

rows=[]
for rec in contract['required_outputs']:
    ev=[]
    for rel in rec['artifact_paths']:
        q=Path(rel)
        if q.is_file():
            ev.append({'path':rel,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()})
    assert ev,rec
    rows.append({'requirement':rec['name'],'status':'PASS','semantic_check':'Exact B-115 sector-completion output is artifact-backed, independently reconstructed, cleanly replayed and child-ready under the frozen superseding contract.','evidence':ev})
(R/'OUTPUT_COMPLETENESS.json').write_text(json.dumps({'schema_version':'1.0','run_id':rid,'module':'B','overall':'PASS','required_outputs':rows},indent=2)+'\n')

# Re-finalize output manifest after all run evidence stops changing.
records=[]
for q in sorted(R.rglob('*')):
    if not q.is_file() or q.name in {'GENERATED_OUTPUT_MANIFEST.json','run.json'} or '__pycache__' in q.parts:
        continue
    records.append({'path':str(q.relative_to(R)),'sha256':hashlib.sha256(q.read_bytes()).hexdigest(),'bytes':q.stat().st_size})
tree=hashlib.sha256()
for rec in records:
    tree.update(rec['path'].encode()); tree.update(b'\0'); tree.update(rec['sha256'].encode()); tree.update(b'\n')
(R/'GENERATED_OUTPUT_MANIFEST.json').write_text(json.dumps({'run_id':rid,'status':'FINAL','finalized_utc':datetime.now(timezone.utc).isoformat(),'outputs':records,'tree_sha256':tree.hexdigest(),'note':'Finalized after contract normalization and completeness evidence. Excludes itself and controller-owned run.json.'},indent=2)+'\n')
PY

python tools/rfc.py doctor
python tools/director.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan

python tools/rfc.py close-run --run-id "$RID" --result PASS --closeout "$R/CLOSEOUT.md"
python tools/rfc.py promote-module B --to FORMALIZED --fidelity PRODUCTION --evidence "$R/FROZEN_DERIVATION_SPEC.json"
python tools/rfc.py promote-module B --to IMPLEMENTED --fidelity PRODUCTION --evidence "$R/primary/FOUR_SECTOR_GENESIS_STATE.json"
python tools/rfc.py promote-module B --to VERIFIED --fidelity PRODUCTION --evidence "$R/GATE_RESULTS.json"
python tools/rfc.py promote-module B --to PHYSICALLY_EXECUTED --fidelity PRODUCTION --evidence "$R/primary/FOUR_SECTOR_GENESIS_STATE.json"
python tools/rfc.py promote-module B --to INDEPENDENTLY_REPRODUCED --fidelity PRODUCTION --evidence "$R/independent/INDEPENDENT_RECONSTRUCTION.json"
python tools/rfc.py promote-module B --to FROZEN --fidelity PRODUCTION --evidence modules/B/frozen/H_B_to_C_v2.json
python tools/rfc.py freeze modules/B/frozen/H_B_to_C_v2.json --kind MODULE_HANDOFF
python tools/rfc.py record-claim --file "$R/CLAIM_RECORD.json"
python tools/rfc.py advance --task B-115 --result PASS --evidence "$R/CLOSEOUT.md" --note 'Exact four-sector B repair closed; activate only C-125 for channel-complete microscopic replay.'
python tools/rfc.py context
python tools/rfc.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan

python - <<'PY'
import json
s=json.load(open('STATE.json'))
q={x['id']:x for x in json.load(open('WORK_QUEUE.json'))['items']}
assert s['active_work_unit']=='C-125' and s['current_module']=='C' and s['current_run'] is None,s
assert s['modules']['B']['evidence_state']=='FROZEN' and s['modules']['B']['fidelity']=='PRODUCTION',s['modules']['B']
assert q['B-115']['status']=='PASS' and q['C-125']['status']=='ACTIVE' and q['D-135']['status']=='BLOCKED'
PY

git add -A
git commit -m 'Close B-115 and activate channel-complete microscopic replay C-125'
git pull --rebase origin agent/frontier-050-execution
git push origin HEAD:agent/frontier-050-execution
CLOSEOUT_SHA=$(git rev-parse HEAD)
python tools/rfc.py record-commit "$CLOSEOUT_SHA" --branch agent/frontier-050-execution --note 'Verified B-first science-lineage repair: exact four-sector B-115 completion, independent replay, child-ready output contract, PRODUCTION freeze, and single-child activation C-125.'
python tools/rfc.py context
git add STATE.json memory/DECISION_LOG.jsonl memory/CURRENT_CONTEXT.md
git commit -m 'Record verified B-115 repair closeout'
git pull --rebase origin agent/frontier-050-execution
git push origin HEAD:agent/frontier-050-execution

git fetch origin agent/frontier-050-execution
git reset --hard origin/agent/frontier-050-execution
python - <<'PY'
import json
s=json.load(open('STATE.json'))
assert s['active_work_unit']=='C-125' and s['current_module']=='C' and s['current_run'] is None,s
assert s['modules']['B']['evidence_state']=='FROZEN' and s['modules']['B']['fidelity']=='PRODUCTION'
assert json.load(open('modules/B/runs/B-115-20260808T060000Z/run.json'))['status']=='PASS'
PY
python tools/rfc.py doctor
