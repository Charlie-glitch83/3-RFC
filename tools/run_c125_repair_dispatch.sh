#!/usr/bin/env bash
set -euo pipefail
RUN_ID="C-125-20260808T062000Z"
RUN="modules/C/runs/${RUN_ID}"

python - <<'PY'
import json
from pathlib import Path
s=json.load(open('STATE.json')); q={x['id']:x for x in json.load(open('WORK_QUEUE.json'))['items']}
assert s['active_work_unit']=='C-125' and s['current_module']=='C' and s['current_run'] is None,s
assert s['modules']['B']['evidence_state']=='FROZEN' and s['modules']['B']['fidelity']=='PRODUCTION',s['modules']['B']
assert s['modules']['C']['evidence_state']=='FROZEN' and s['modules']['C']['fidelity']=='MINIMAL_SPINE',s['modules']['C']
assert q['C-125']['status']=='ACTIVE' and q['D-135']['status']=='BLOCKED',q
assert Path('modules/B/frozen/H_B_to_C_v2.json').is_file()
assert Path('recovery/BG_SUPERSEDING_LINEAGE_PACKET.md').is_file()
print('C125_PREP_PASS')
PY

python tools/rfc.py reopen-module C --fidelity PRODUCTION --evidence recovery/BG_SUPERSEDING_LINEAGE_PACKET.md
python tools/rfc.py new-run C --run-id "$RUN_ID"
python tools/director.py prepare-active
python tools/execute_c125.py prepare --run "$RUN"
python tools/director.py solver-copy --module C --solver spectral_model --destination "$RUN"
python - <<'PY'
import hashlib,json,math
from pathlib import Path
R=Path('modules/C/runs/C-125-20260808T062000Z')
parent=json.load(open('modules/B/frozen/H_B_to_C_v2.json'))
M=[]
Q=parent['operator']['matrix']
for i,row in enumerate(Q): M.append([(1.0 if i==j else 0.0)-float(x) for j,x in enumerate(row)])
G=[[0.0,-1/math.sqrt(3),1/math.sqrt(3)],[1/math.sqrt(3),0.0,-1/math.sqrt(3)],[-1/math.sqrt(3),1/math.sqrt(3),0.0]]
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=R/'binding_sheets/C_spectral_model.bindings.json'; sheet=json.load(open(p)); src=R/'FROZEN_DERIVATION_SPEC.json'; h=sha(src)
for rec in sheet['bindings']:
 rec.update(origin_kind='INTERNAL_DERIVATION',origin_path=str(src),origin_sha256=h,module='C',units='dimensionless',dimensions='1',justification='Corroborative exact parent spectral audit; not the full C-125 scientific generator.')
 if rec['path']=='model.matrix': rec.update(value=M,derivation_object='I-Q_B')
 elif rec['path']=='model.symmetry_generators': rec.update(value=[G],derivation_object='conserved-mode O(2) audit generator')
 else: raise SystemExit(rec['path'])
p.write_text(json.dumps(sheet,indent=2)+'\n')
PY
python tools/materialize_solver_config.py --template "$RUN/solver_templates/C_spectral_model.template.json" --binding-sheet "$RUN/binding_sheets/C_spectral_model.bindings.json" --output "$RUN/solver_configs/C_spectral_model.json"
python - <<'PY'
import hashlib,json
from pathlib import Path
R=Path('modules/C/runs/C-125-20260808T062000Z')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=R/'PRE_EXECUTION_LOCK.json'; lock=json.load(open(p)); lock['corroborative_solver_binding']={'config_path':str(R/'solver_configs/C_spectral_model.json'),'config_sha256':sha(R/'solver_configs/C_spectral_model.json'),'binding_sha256':sha(R/'binding_sheets/C_spectral_model.bindings.json'),'purpose':'corroborative parent-derived spectral audit only'}; p.write_text(json.dumps(lock,indent=2)+'\n')
PY
python tools/rfc.py context
python tools/rfc.py doctor
python tools/director.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan

git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
git add -A
git commit -m 'Freeze C-125 channel-complete superseding replay'
git pull --rebase origin agent/frontier-050-execution
git push origin HEAD:agent/frontier-050-execution
LOCK_SHA=$(git rev-parse HEAD)
git fetch origin agent/frontier-050-execution
test "$(git rev-parse origin/agent/frontier-050-execution)" = "$LOCK_SHA"

python tools/run_reference_checks.py --module C --output "$RUN/reference_checks.json"
python tools/run_configured_solver.py --config "$RUN/solver_configs/C_spectral_model.json" --output-dir "$RUN/solver_outputs/spectral_model"
python tools/execute_c125.py execute --run "$RUN"
python - <<'PY'
import json
R='modules/C/runs/C-125-20260808T062000Z'
assert json.load(open(R+'/reference_checks.json'))['overall']=='PASS'
assert json.load(open(R+'/solver_outputs/spectral_model/result.json'))['success'] is True
assert json.load(open(R+'/GATE_RESULTS.json'))['overall']=='PASS'
assert json.load(open(R+'/independent/INDEPENDENT_RECONSTRUCTION.json'))['pass'] is True
PY

rm -rf /tmp/c125-lock /tmp/c125-replay
git worktree add --detach /tmp/c125-lock "$LOCK_SHA"
(
 cd /tmp/c125-lock
 python tools/execute_c125.py execute --run "$RUN" --output-root /tmp/c125-replay
)
python tools/execute_c125.py finalize --run "$RUN" --replay-root /tmp/c125-replay
python - <<'PY'
import json
R='modules/C/runs/C-125-20260808T062000Z'
c=json.load(open(R+'/OUTPUT_CONTRACT.json')); assert c['status']=='PASS',c
assert all(x['status']=='SATISFIED' and x['child_ready'] for x in c['required_outputs'])
assert all(x['status']=='SATISFIED' and x['source_lineage']=='PASS' and x['independent_verification']=='PASS' for x in c['child_bindings'].values())
assert json.load(open(R+'/OUTPUT_COMPLETENESS.json'))['overall']=='PASS'
assert json.load(open(R+'/REPLAY_RECORD.json'))['artifact_hashes_match'] is True
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
python tools/rfc.py advance --task C-125 --result PASS --evidence "$RUN/CLOSEOUT.md" --note 'Channel-complete C-125 microscopic replay closed from exact H_B_to_C_v2; activate only D-135.'
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

git add -A
git commit -m 'Close C-125 and activate nonequilibrium replay D-135'
git pull --rebase origin agent/frontier-050-execution
git push origin HEAD:agent/frontier-050-execution
CLOSE_SHA=$(git rev-parse HEAD)
git fetch origin agent/frontier-050-execution
test "$(git rev-parse origin/agent/frontier-050-execution)" = "$CLOSE_SHA"
python tools/rfc.py record-commit "$CLOSE_SHA" --branch agent/frontier-050-execution --note 'Verified C-125 channel-complete microscopic replay, exact parent/source lineage, spectral corroboration, clean replay, complete D child contract, PRODUCTION evidence ladder, H_C_to_D_v2 and one-child activation D-135.'
python tools/rfc.py context
python tools/rfc.py doctor
git add STATE.json memory/DECISION_LOG.jsonl memory/CURRENT_CONTEXT.md
git commit -m 'Record verified C-125 science-lineage repair closeout'
git pull --rebase origin agent/frontier-050-execution
git push origin HEAD:agent/frontier-050-execution

echo "C125_REPAIR_COMPLETE $(git rev-parse HEAD)"
