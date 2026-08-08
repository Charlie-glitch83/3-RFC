#!/usr/bin/env bash
set -euo pipefail

BRANCH='agent/frontier-050-execution'
RUN_ID='C-125-20260808T062000Z'
RUN="modules/C/runs/$RUN_ID"

python - <<'PY'
import json
from pathlib import Path
s=json.load(open('STATE.json')); q={x['id']:x for x in json.load(open('WORK_QUEUE.json'))['items']}
assert s['active_work_unit']=='C-125' and s['current_module']=='C',s
assert s['modules']['B']['evidence_state']=='FROZEN' and s['modules']['B']['fidelity']=='PRODUCTION',s['modules']['B']
assert q['C-125']['status']=='ACTIVE' and q['D-135']['status']=='BLOCKED',q
assert Path('modules/B/frozen/H_B_to_C_v2.json').is_file()
PY

# Preserve the generic README-created startup shell. It contains no primary science.
RID=$(python - <<'PY'
import json; print(json.load(open('STATE.json')).get('current_run') or '')
PY
)
if [ -n "$RID" ]; then
  python - "$RID" <<'PY'
import json,sys
from pathlib import Path
rid=sys.argv[1]; R=Path('modules/C/runs')/rid
rec=json.load(open(R/'run.json'))
if rec.get('module')!='C' or rec.get('task_id')!='C-125' or rec.get('status')!='CREATED':
    raise SystemExit(f'HARD STOP: refusing to supersede nonblank C run {rec}')
(R/'CLOSEOUT.md').write_text(f'''# {rid} Startup-Shell Closeout

## Result

**BLOCKED BEFORE SCIENTIFIC EXECUTION.**

This generic README startup shell contains no primary C science. It is preserved and closed before the superseding PRODUCTION replay begins from exact `H_B_to_C_v2`.
''',encoding='utf-8')
PY
  python tools/rfc.py close-run --run-id "$RID" --result BLOCKED --closeout "modules/C/runs/$RID/CLOSEOUT.md"
fi

python tools/rfc.py reopen-module C --fidelity PRODUCTION --evidence recovery/BG_SUPERSEDING_LINEAGE_PACKET.md
python tools/rfc.py new-run C --run-id "$RUN_ID"
python tools/director.py prepare-active
python tools/execute_c125.py prepare --run "$RUN"
python tools/director.py solver-copy --module C --solver spectral_model --destination "$RUN"
python tools/materialize_solver_config.py --template "$RUN/solver_templates/C_spectral_model.template.json" --binding-sheet "$RUN/binding_sheets/C_spectral_model.bindings.json" --output "$RUN/solver_configs/C_spectral_model.json"
python - <<'PY'
import hashlib,json
from pathlib import Path
R=Path('modules/C/runs/C-125-20260808T062000Z')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=R/'PRE_EXECUTION_LOCK.json'; lock=json.load(open(p))
lock['corroborative_solver_binding']={'config_path':str(R/'solver_configs/C_spectral_model.json'),'config_sha256':sha(R/'solver_configs/C_spectral_model.json'),'binding_sha256':sha(R/'binding_sheets/C_spectral_model.bindings.json'),'purpose':'exact parent-derived finite-core corroboration only; not full mass/mixing branch selection'}
lock['post_lock_execution_authorized']='WOLFRAM_C_WL_001_AND_C_WL_002_THEN_FROZEN_MATRIX_ONLY'
p.write_text(json.dumps(lock,indent=2)+'\n')
PY
python tools/rfc.py context
python tools/rfc.py doctor
python tools/director.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan
python - <<'PY'
import json
from pathlib import Path
s=json.load(open('STATE.json'))
assert s['active_work_unit']=='C-125' and s['current_run']=='C-125-20260808T062000Z',s
R=Path('modules/C/runs/C-125-20260808T062000Z')
lock=json.load(open(R/'PRE_EXECUTION_LOCK.json'))
assert lock['status']=='FROZEN' and lock['frozen_before_primary_execution'] is True,lock
assert lock['required_post_lock_wolfram']==['C-WL-001','C-WL-002'],lock
assert json.load(open(R/'run.json'))['status']=='CREATED'
assert not (R/'primary/MICROSCOPIC_CONSTITUTION_V2.json').exists()
print('C125_PREEXECUTION_FREEZE_PASS')
PY

git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
git add -A
git commit -m 'Freeze source-complete C-125 branch-family replay before Wolfram'
git fetch origin "$BRANCH"
git rebase "origin/$BRANCH"
git push origin HEAD:"$BRANCH"
SHA=$(git rev-parse HEAD)
remote=$(git ls-remote origin "refs/heads/$BRANCH" | awk '{print $1}')
test "$remote" = "$SHA"
echo "C125_LOCK_SHA=$SHA"
