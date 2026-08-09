#!/usr/bin/env bash
set -euo pipefail
RUN_ID='I-180-20260809T050839Z'
R="modules/I/runs/$RUN_ID"
BRANCH='agent/frontier-050-execution'
python -m pip install --disable-pip-version-check -r requirements-lock.txt
python - <<'PY'
import json
from pathlib import Path
s=json.load(open('STATE.json')); r='I-180-20260809T050839Z'
assert s['active_work_unit']=='I-180' and s['current_module']=='I' and s['current_run']==r,s
assert s['modules']['G']['evidence_state']=='FROZEN',s['modules']['G']
lock=json.load(open(f'modules/I/runs/{r}/PRE_EXECUTION_LOCK.json'))
assert lock['status']=='FROZEN' and lock['frozen_before_primary_execution'] is True,lock
patch=json.load(open(f'modules/I/runs/{r}/IMPLEMENTATION_PATCH_RECORD.json'))
assert patch['classification']=='IMPLEMENTATION_ONLY_WOLFRAM_BACKEND_COMPATIBILITY' and patch['science_changed'] is False,patch
assert not Path(f'modules/I/runs/{r}/primary/I_FINITE_RELATIONAL_BACKGROUND_MINIMAL_SPINE.json').exists(),'primary execution predates repaired full rerun'
PY
PRE_SHA="$(git rev-parse HEAD)"
python tools/director.py wolfram-record --run "$RUN_ID" --call I-WL-001 --output "$R/scratch/wolfram_external/I-WL-001.txt"
python tools/director.py wolfram-record --run "$RUN_ID" --call I-WL-002 --output "$R/scratch/wolfram_external/I-WL-002.txt"
python tools/run_reference_checks.py --module I --output "$R/reference_checks.json"
python tools/materialize_solver_config.py --template "$R/solver_templates/I_background_ode.template.json" --binding-sheet "$R/binding_sheets/I_background_ode.bindings.json" --output "$R/solver_configs/I_background_ode.json"
python tools/run_configured_solver.py --config "$R/solver_configs/I_background_ode.json" --output-dir "$R/solver_outputs/transport"
bash tools/finish_local_phase.sh I "$R"
python tools/i180_convergence.py
python tools/i180_parent_bound.py execute
rm -rf /tmp/i180-clean
git worktree add --detach /tmp/i180-clean "$PRE_SHA"
(
 cd /tmp/i180-clean
 R2="modules/I/runs/$RUN_ID"
 python tools/director.py wolfram-record --run "$RUN_ID" --call I-WL-001 --output "$R2/scratch/wolfram_external/I-WL-001.txt"
 python tools/director.py wolfram-record --run "$RUN_ID" --call I-WL-002 --output "$R2/scratch/wolfram_external/I-WL-002.txt"
 python tools/run_reference_checks.py --module I --output "$R2/reference_checks.json"
 python tools/materialize_solver_config.py --template "$R2/solver_templates/I_background_ode.template.json" --binding-sheet "$R2/binding_sheets/I_background_ode.bindings.json" --output "$R2/solver_configs/I_background_ode.json"
 python tools/run_configured_solver.py --config "$R2/solver_configs/I_background_ode.json" --output-dir "$R2/solver_outputs/transport"
 bash tools/finish_local_phase.sh I "$R2"
 python tools/i180_convergence.py
 python tools/i180_parent_bound.py execute
)
python tools/i180_parent_bound.py finalize --replay-run "/tmp/i180-clean/$R" --pre-sha "$PRE_SHA"
python tools/i180_contract_fix.py
python tools/scientific_completion_guard.py --run "$R"
python tools/rfc.py doctor
python tools/director.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan
python tools/rfc.py close-run --run-id "$RUN_ID" --result PASS --closeout "$R/CLOSEOUT.md"
python tools/rfc.py promote-module I --to FORMALIZED --fidelity MINIMAL_SPINE --evidence "$R/FROZEN_DERIVATION_SPEC.json"
python tools/rfc.py promote-module I --to IMPLEMENTED --fidelity MINIMAL_SPINE --evidence "$R/solver_outputs/transport/result.json"
python tools/rfc.py promote-module I --to VERIFIED --fidelity MINIMAL_SPINE --evidence "$R/GATE_RESULTS.json"
python tools/rfc.py promote-module I --to PHYSICALLY_EXECUTED --fidelity MINIMAL_SPINE --evidence "$R/primary/I_FINITE_RELATIONAL_BACKGROUND_MINIMAL_SPINE.json"
python tools/rfc.py promote-module I --to INDEPENDENTLY_REPRODUCED --fidelity MINIMAL_SPINE --evidence "$R/independent/INDEPENDENT_RECONSTRUCTION.json"
python tools/rfc.py promote-module I --to FROZEN --fidelity MINIMAL_SPINE --evidence modules/I/frozen/H_I_to_HI.json
python tools/rfc.py freeze modules/I/frozen/H_I_to_HI.json --kind MODULE_HANDOFF
python tools/rfc.py record-claim --file "$R/CLAIM_RECORD.json"
python - <<'PY'
import json
from pathlib import Path
r=Path('modules/I/runs/I-180-20260809T050839Z'); c=json.load(open(r/'CLAIM_RECORD.json')); p=Path('STATE.json'); s=json.load(open(p))
s['strongest_supported_claim']=c['text']; s['strongest_unsupported_claim']=c['unsupported_boundary']; s['repair_state']='I180_MINIMAL_SPINE_CLOSED_PENDING_VERIFIED_COMMIT_AND_ADVANCE'; p.write_text(json.dumps(s,indent=2)+'\n')
PY
python tools/rfc.py context
python tools/rfc.py doctor
python tools/rfc.py firewall-scan
git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
git add -A
git commit -m 'Close Module I at its verified scientific scope'
git pull --rebase origin "$BRANCH"
git push origin HEAD:"$BRANCH"
printf 'I180_FINAL_COMMIT=%s\n' "$(git rev-parse HEAD)"
