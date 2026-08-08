#!/usr/bin/env bash
set -euo pipefail

BRANCH='agent/frontier-050-execution'
OLD='C-125-20260808T063010Z'
RUN_ID='C-125-20260808T063500Z'
RUN="modules/C/runs/$RUN_ID"

python - <<'PY'
import json
from pathlib import Path
s=json.load(open('STATE.json')); r=json.load(open('modules/C/runs/C-125-20260808T063010Z/run.json'))
assert s['active_work_unit']=='C-125' and s['current_module']=='C' and s['current_run']=='C-125-20260808T063010Z',s
assert s['modules']['C']['evidence_state']=='DESIGN' and s['modules']['C']['fidelity']=='PRODUCTION',s['modules']['C']
assert r['status']=='CREATED',r
assert not Path('modules/C/runs/C-125-20260808T063010Z/primary/MICROSCOPIC_CONSTITUTION_V2.json').exists()
PY

python - <<'PY'
from pathlib import Path
R=Path('modules/C/runs/C-125-20260808T063010Z')
(R/'CLOSEOUT.md').write_text('''# C-125-20260808T063010Z Pre-Primary Source Audit Closeout

## Result

**BLOCKED BEFORE PRIMARY EXECUTION.**

The frozen pre-execution package instantiated a concrete route-kernel/phase representative that is not explicitly supplied by the recovered C theorem bytes available in 3-RFC. The issue was discovered before any primary C science was executed. This attempt is preserved unchanged as evidence. A fresh governed C-125 run will freeze the recovered theorem as an explicit source-owned branch family instead of silently selecting missing route matrices/phases.

## Strongest supported claim

The exact B-v2/A ancestry and recovered C theorem determine parent-fixed compression/scale/shell quantities, the finite symmetry/charge/zero-mode laws, and a lawful source-owned microscopic branch family.

## Strongest unsupported claim

No unique source-owned W_j/phase/block-norm/scale representative was established in this attempt, and no primary C physical result is claimed.
''',encoding='utf-8')
PY
python tools/rfc.py close-run --run-id "$OLD" --result BLOCKED --closeout "modules/C/runs/$OLD/CLOSEOUT.md"

python tools/rfc.py new-run C --run-id "$RUN_ID"
python tools/director.py prepare-active
python tools/execute_c125.py prepare --run "$RUN"
mkdir -p "$RUN/solver_configs"
python tools/materialize_solver_config.py --template "$RUN/solver_templates/C_spectral_model.template.json" --binding-sheet "$RUN/binding_sheets/C_spectral_model.bindings.json" --output "$RUN/solver_configs/C_spectral_model.json"
python - <<'PY'
import hashlib,json
from pathlib import Path
R=Path('modules/C/runs/C-125-20260808T063500Z')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=R/'PRE_EXECUTION_LOCK.json'; lock=json.load(open(p))
lock['corroborative_solver_binding']={'config_path':str(R/'solver_configs/C_spectral_model.json'),'config_sha256':sha(R/'solver_configs/C_spectral_model.json'),'binding_sha256':sha(R/'binding_sheets/C_spectral_model.bindings.json'),'purpose':'exact parent-derived finite-core corroboration only; not full C mass/mixing branch selection'}
lock['post_lock_execution_authorized']='ONLY_AFTER_CONNECTED_C_WL_001_AND_C_WL_002_ARE_RECORDED_PASS'
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
s=json.load(open('STATE.json')); R=Path('modules/C/runs/C-125-20260808T063500Z')
assert s['current_run']=='C-125-20260808T063500Z',s
assert json.load(open(R/'run.json'))['status']=='CREATED'
lock=json.load(open(R/'PRE_EXECUTION_LOCK.json'))
assert lock['status']=='FROZEN' and lock['required_post_lock_wolfram']==['C-WL-001','C-WL-002'],lock
assert not (R/'primary/MICROSCOPIC_CONSTITUTION_V2.json').exists()
print('C125_SAFE_PREP_PASS')
PY

git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
git add -A
git commit -m 'Freeze source-safe C-125 branch-family retry before Wolfram'
git fetch origin "$BRANCH"
git rebase "origin/$BRANCH"
git push origin HEAD:"$BRANCH"
SHA=$(git rev-parse HEAD)
remote=$(git ls-remote origin "refs/heads/$BRANCH" | awk '{print $1}')
test "$remote" = "$SHA"
echo "C125_SAFE_LOCK_SHA=$SHA"
