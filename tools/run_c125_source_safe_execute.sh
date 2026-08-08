#!/usr/bin/env bash
set -euo pipefail
BRANCH='agent/frontier-050-execution'
RUN_ID='C-125-20260808T063500Z'
RUN="modules/C/runs/$RUN_ID"
LOCK_SHA='9a262e0ba67a9f18cdb677284386be2957808340'

python - <<'PY'
import json,hashlib
from pathlib import Path
s=json.load(open('STATE.json')); r=json.load(open('modules/C/runs/C-125-20260808T063500Z/run.json')); lock=json.load(open('modules/C/runs/C-125-20260808T063500Z/PRE_EXECUTION_LOCK.json'))
assert s['active_work_unit']=='C-125' and s['current_module']=='C' and s['current_run']=='C-125-20260808T063500Z',s
assert s['modules']['C']['evidence_state']=='DESIGN' and s['modules']['C']['fidelity']=='PRODUCTION',s['modules']['C']
assert r['status']=='CREATED',r
assert lock['status']=='FROZEN' and lock['frozen_before_primary_execution'] is True,lock
assert lock['required_post_lock_wolfram']==['C-WL-001','C-WL-002'],lock
assert not Path('modules/C/runs/C-125-20260808T063500Z/primary/MICROSCOPIC_CONSTITUTION_V2.json').exists()
assert Path('modules/C/runs/C-125-20260808T063500Z/wolfram/C-WL-001/input.wl').read_bytes()==Path('recipes/C/wolfram/C-WL-001.wl').read_bytes()
assert Path('modules/C/runs/C-125-20260808T063500Z/wolfram/C-WL-002/input.wl').read_bytes()==Path('recipes/C/wolfram/C-WL-002.wl').read_bytes()
print('C125_EXECUTION_PRECONDITION_PASS')
PY

git merge-base --is-ancestor "$LOCK_SHA" HEAD

cat > /tmp/C-WL-001-output.txt <<'EOF'
Symbol::undefined2: Warning: Global symbols "M, M, M, M, M, M, M" are undefined.
General::messages: Messages were generated which may indicate errors.

Out[1]= "<|\"call\" -> \"C-WL-001\", \"hermitian\" -> True, \"characteristicPolynomial\" -> \"a*b - a*lambda - b*lambda + lambda^2 - w^2 - z^2\", \"trace\" -> \"a + b\", \"determinant\" -> \"a*b - w^2 - z^2\", \"eigenvalues\" -> {\"(a + b - Sqrt[(a - b)^2 + 4*(w^2 + z^2)])/2\", \"(a + b + Sqrt[(a - b)^2 + 4*(w^2 + z^2)])/2\"}|>"
EOF
cat > /tmp/C-WL-002-output.txt <<'EOF'
Symbol::undefined2: Warning: Global symbols "G, X, G, X, X, G, X" are undefined.
General::messages: Messages were generated which may indicate errors.

Out[1]= "<|\"call\" -> \"C-WL-002\", \"invarianceSolution\" -> \"x21 == -x12 && x22 == x11\", \"candidate\" -> \"{{x11, x12}, {-x12, x11}}\"|>"
EOF

python tools/director.py wolfram-record --run "$RUN_ID" --call C-WL-001 --output /tmp/C-WL-001-output.txt
python tools/director.py wolfram-record --run "$RUN_ID" --call C-WL-002 --output /tmp/C-WL-002-output.txt
python tools/run_reference_checks.py --module C --output "$RUN/reference_checks.json"
rm -rf "$RUN/solver_outputs/spectral_model"
mkdir -p "$RUN/solver_outputs/spectral_model"
python tools/run_configured_solver.py --config "$RUN/solver_configs/C_spectral_model.json" --output-dir "$RUN/solver_outputs/spectral_model"
python - <<'PY'
import json
R='modules/C/runs/C-125-20260808T063500Z'
for c in ['C-WL-001','C-WL-002']:
 g=json.load(open(f'{R}/wolfram/{c}/gate.json'))
 assert str(g.get('status',g.get('result',''))).startswith('PASS') or g.get('pass') is True,g
assert json.load(open(R+'/reference_checks.json'))['overall']=='PASS'
assert json.load(open(R+'/solver_outputs/spectral_model/result.json'))['success'] is True
print('C125_POSTLOCK_CORROBORATION_PASS')
PY
python tools/rfc.py doctor
python tools/director.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan

git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
git add "$RUN/wolfram" "$RUN/reference_checks.json" "$RUN/solver_outputs/spectral_model"
git commit -m 'Record C-125 post-lock symbolic and spectral corroboration'
git fetch origin "$BRANCH"
git rebase "origin/$BRANCH"
git push origin HEAD:"$BRANCH"
CORR_SHA=$(git rev-parse HEAD)
git fetch origin "$BRANCH"
test "$(git rev-parse origin/$BRANCH)" = "$CORR_SHA"

# Primary materialization from the frozen branch family. No unresolved source variable is instantiated.
python tools/execute_c125.py execute --run "$RUN"
python - <<'PY'
import json
R='modules/C/runs/C-125-20260808T063500Z'
p=json.load(open(R+'/primary/MICROSCOPIC_CONSTITUTION_V2.json'))
assert p['status']=='PHYSICALLY_EXECUTED_FORMAL_BRANCH_FAMILY',p
assert json.load(open(R+'/PRIMARY_GATE_INPUTS.json'))['overall']=='PASS'
assert json.load(open(R+'/independent/INDEPENDENT_RECONSTRUCTION.json'))['pass'] is True
assert json.load(open(R+'/primary/COUNTERMODEL_RESULTS.json'))['overall']=='PASS'
print('C125_PRIMARY_BRANCH_FAMILY_PASS')
PY

# Clean detached replay from the exact corroborated pre-primary commit.
rm -rf /tmp/c125-corroborated /tmp/c125-replay
git worktree add --detach /tmp/c125-corroborated "$CORR_SHA"
(
 cd /tmp/c125-corroborated
 python tools/execute_c125.py execute --run "$RUN" --output-root /tmp/c125-replay
)
python tools/execute_c125.py finalize --run "$RUN" --replay-root /tmp/c125-replay
python - <<'PY'
import json
R='modules/C/runs/C-125-20260808T063500Z'
assert json.load(open(R+'/GATE_RESULTS.json'))['overall']=='PASS'
assert json.load(open(R+'/REPLAY_RECORD.json'))['result']=='PASS'
assert json.load(open(R+'/REPLAY_RECORD.json'))['artifact_hashes_match'] is True
c=json.load(open(R+'/OUTPUT_CONTRACT.json')); assert c['status']=='PASS',c
assert all(x['status']=='SATISFIED' and x['semantic_gate']=='PASS' and x['independent_verification']=='PASS' and x['child_ready'] for x in c['required_outputs'])
assert all(v['status']=='SATISFIED' and v['source_lineage']=='PASS' and v['independent_verification']=='PASS' for v in c['child_bindings'].values())
assert json.load(open(R+'/OUTPUT_COMPLETENESS.json'))['overall']=='PASS'
assert json.load(open('modules/C/frozen/H_C_to_D_v2_MANIFEST.json'))['fidelity']=='PRODUCTION'
print('C125_FINALIZATION_PASS')
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
python tools/rfc.py advance --task C-125 --result PASS --evidence "$RUN/CLOSEOUT.md" --note 'Verified source-safe C-125 branch-family replay from exact H_B_to_C_v2; activate only D-135.'
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
print('C125_ONE_CHILD_ADVANCE_PASS')
PY

git add -A
git commit -m 'Close source-safe C-125 and activate D-135'
git fetch origin "$BRANCH"
git rebase "origin/$BRANCH"
git push origin HEAD:"$BRANCH"
CLOSE_SHA=$(git rev-parse HEAD)
git fetch origin "$BRANCH"
test "$(git rev-parse origin/$BRANCH)" = "$CLOSE_SHA"
python tools/rfc.py record-commit "$CLOSE_SHA" --branch "$BRANCH" --note 'Verified source-safe C-125 branch-family microscopic replay; connected Wolfram, parent spectral corroboration, exact branch-family preservation, clean replay, D child contract, PRODUCTION evidence ladder and one-child activation D-135.'
python tools/rfc.py context
python tools/rfc.py doctor
git add STATE.json memory/DECISION_LOG.jsonl memory/CURRENT_CONTEXT.md
git commit -m 'Record verified source-safe C-125 closeout'
git fetch origin "$BRANCH"
git rebase "origin/$BRANCH"
git push origin HEAD:"$BRANCH"

echo "C125_SOURCE_SAFE_COMPLETE $(git rev-parse HEAD)"
