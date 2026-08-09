#!/usr/bin/env bash
set -euo pipefail
RUN_ID='HU-170-20260809T045528Z'
R="modules/HU/runs/$RUN_ID"
BRANCH='agent/frontier-050-execution'
python -m pip install --disable-pip-version-check -r requirements-lock.txt
python - <<'PY'
import json
s=json.load(open('STATE.json')); r='HU-170-20260809T045528Z'
assert s['active_work_unit']=='HU-170' and s['current_module']=='HU' and s['current_run']==r,s
assert s['modules']['G']['evidence_state']=='FROZEN',s['modules']['G']
assert json.load(open(f'modules/HU/runs/{r}/PRE_EXECUTION_LOCK.json'))['status']=='FROZEN'
PY
PRE_SHA="$(git rev-parse HEAD)"
python tools/director.py wolfram-record --run "$RUN_ID" --call HU-WL-001 --output "$R/scratch/wolfram_external/HU-WL-001.txt"
python tools/director.py wolfram-record --run "$RUN_ID" --call HU-WL-002 --output "$R/scratch/wolfram_external/HU-WL-002.txt"
python tools/run_reference_checks.py --module HU --output "$R/reference_checks.json"
python tools/materialize_solver_config.py --template "$R/solver_templates/HU_linear_transfer.template.json" --binding-sheet "$R/binding_sheets/HU_linear_transfer.bindings.json" --output "$R/solver_configs/HU_linear_transfer.json"
python tools/run_configured_solver.py --config "$R/solver_configs/HU_linear_transfer.json" --output-dir "$R/solver_outputs/linear_transfer"
bash tools/finish_local_phase.sh HU "$R"
python tools/hu170_convergence.py
python tools/hu170_parent_bound.py execute
rm -rf /tmp/hu170-clean
git worktree add --detach /tmp/hu170-clean "$PRE_SHA"
(
 cd /tmp/hu170-clean
 R2="modules/HU/runs/$RUN_ID"
 python tools/director.py wolfram-record --run "$RUN_ID" --call HU-WL-001 --output "$R2/scratch/wolfram_external/HU-WL-001.txt"
 python tools/director.py wolfram-record --run "$RUN_ID" --call HU-WL-002 --output "$R2/scratch/wolfram_external/HU-WL-002.txt"
 python tools/run_reference_checks.py --module HU --output "$R2/reference_checks.json"
 python tools/materialize_solver_config.py --template "$R2/solver_templates/HU_linear_transfer.template.json" --binding-sheet "$R2/binding_sheets/HU_linear_transfer.bindings.json" --output "$R2/solver_configs/HU_linear_transfer.json"
 python tools/run_configured_solver.py --config "$R2/solver_configs/HU_linear_transfer.json" --output-dir "$R2/solver_outputs/linear_transfer"
 bash tools/finish_local_phase.sh HU "$R2"
 python tools/hu170_convergence.py
 python tools/hu170_parent_bound.py execute
)
python tools/hu170_parent_bound.py finalize --replay-run "/tmp/hu170-clean/$R" --pre-sha "$PRE_SHA"
python tools/scientific_completion_guard.py --run "$R"
python tools/rfc.py doctor
python tools/director.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan
python tools/rfc.py close-run --run-id "$RUN_ID" --result PASS --closeout "$R/CLOSEOUT.md"
python tools/rfc.py promote-module HU --to FORMALIZED --fidelity MINIMAL_SPINE --evidence "$R/FROZEN_DERIVATION_SPEC.json"
python tools/rfc.py promote-module HU --to VERIFIED --fidelity MINIMAL_SPINE --evidence "$R/GATE_RESULTS.json"
python tools/rfc.py promote-module HU --to INDEPENDENTLY_REPRODUCED --fidelity MINIMAL_SPINE --evidence "$R/independent/INDEPENDENT_RECONSTRUCTION.json"
python tools/rfc.py promote-module HU --to FROZEN --fidelity MINIMAL_SPINE --evidence modules/HU/frozen/H_HU_to_HI.json
python tools/rfc.py freeze modules/HU/frozen/H_HU_to_HI.json --kind MODULE_HANDOFF
python tools/rfc.py record-claim --file "$R/CLAIM_RECORD.json"
python - <<'PY'
import json
from pathlib import Path
r=Path('modules/HU/runs/HU-170-20260809T045528Z'); c=json.load(open(r/'CLAIM_RECORD.json')); p=Path('STATE.json'); s=json.load(open(p))
s['strongest_supported_claim']=c['text']; s['strongest_unsupported_claim']=c['unsupported_boundary']; s['repair_state']='HU170_MINIMAL_SPINE_CLOSED_PENDING_VERIFIED_COMMIT_AND_ADVANCE'; p.write_text(json.dumps(s,indent=2)+'\n')
PY
python tools/rfc.py context
python tools/rfc.py doctor
python tools/rfc.py firewall-scan
git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
git add -A
git commit -m 'Close Module HU at its verified scientific scope'
git pull --rebase origin "$BRANCH"
git push origin HEAD:"$BRANCH"
printf 'HU170_FINAL_COMMIT=%s\n' "$(git rev-parse HEAD)"
