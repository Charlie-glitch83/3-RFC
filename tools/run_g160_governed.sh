#!/usr/bin/env bash
set -euo pipefail
RUN_ID='G-160-20260809T025252Z'
R="modules/G/runs/$RUN_ID"
BRANCH='agent/frontier-050-execution'
python -m pip install --disable-pip-version-check -r requirements-lock.txt
python - <<'PY'
import json
from pathlib import Path
s=json.load(open('STATE.json')); r=Path('modules/G/runs/G-160-20260809T025252Z')
assert s['active_work_unit']=='G-160' and s['current_module']=='G' and s['current_run']==r.name,s
assert s['modules']['F']['evidence_state']=='FROZEN' and s['modules']['F']['fidelity']=='PRODUCTION',s['modules']['F']
assert json.load(open(r/'PRE_EXECUTION_LOCK.json'))['status']=='FROZEN'
PY
PRE_SHA="$(git log -1 --format=%H --grep='^Freeze G-160 pre-execution state$')"
test -n "$PRE_SHA"
python tools/director.py wolfram-record --run "$RUN_ID" --call G-WL-001 --output "$R/scratch/wolfram_external/G-WL-001.txt"
python tools/director.py wolfram-record --run "$RUN_ID" --call G-WL-002 --output "$R/scratch/wolfram_external/G-WL-002.txt"
python tools/run_reference_checks.py --module G --output "$R/reference_checks.json"
python tools/materialize_solver_config.py --template "$R/solver_templates/G_recombination_network.template.json" --binding-sheet "$R/binding_sheets/G_recombination_network.bindings.json" --output "$R/solver_configs/G_recombination_network.json"
python tools/run_configured_solver.py --config "$R/solver_configs/G_recombination_network.json" --output-dir "$R/solver_outputs/reaction_network"
python tools/g160_parent_bound.py bind-visibility --run "$R"
python tools/materialize_solver_config.py --template "$R/solver_templates/G_visibility.template.json" --binding-sheet "$R/binding_sheets/G_visibility.bindings.json" --output "$R/solver_configs/G_visibility.json"
python tools/run_configured_solver.py --config "$R/solver_configs/G_visibility.json" --output-dir "$R/solver_outputs/visibility"
bash tools/finish_local_phase.sh G "$R"
python tools/g160_convergence.py --run "$R"
python tools/g160_parent_bound.py execute --run "$R"
rm -rf /tmp/g160-clean
git worktree add --detach /tmp/g160-clean "$PRE_SHA"
(
 cd /tmp/g160-clean
 R2="modules/G/runs/$RUN_ID"
 python tools/director.py wolfram-record --run "$RUN_ID" --call G-WL-001 --output "$R2/scratch/wolfram_external/G-WL-001.txt"
 python tools/director.py wolfram-record --run "$RUN_ID" --call G-WL-002 --output "$R2/scratch/wolfram_external/G-WL-002.txt"
 python tools/run_reference_checks.py --module G --output "$R2/reference_checks.json"
 python tools/materialize_solver_config.py --template "$R2/solver_templates/G_recombination_network.template.json" --binding-sheet "$R2/binding_sheets/G_recombination_network.bindings.json" --output "$R2/solver_configs/G_recombination_network.json"
 python tools/run_configured_solver.py --config "$R2/solver_configs/G_recombination_network.json" --output-dir "$R2/solver_outputs/reaction_network"
 python tools/g160_parent_bound.py bind-visibility --run "$R2"
 python tools/materialize_solver_config.py --template "$R2/solver_templates/G_visibility.template.json" --binding-sheet "$R2/binding_sheets/G_visibility.bindings.json" --output "$R2/solver_configs/G_visibility.json"
 python tools/run_configured_solver.py --config "$R2/solver_configs/G_visibility.json" --output-dir "$R2/solver_outputs/visibility"
 bash tools/finish_local_phase.sh G "$R2"
 python tools/g160_convergence.py --run "$R2"
 python tools/g160_parent_bound.py execute --run "$R2"
)
python tools/g160_parent_bound.py finalize --run "$R" --replay-run "/tmp/g160-clean/$R" --pre-sha "$PRE_SHA"
python tools/g160_contract_fix.py
python tools/scientific_completion_guard.py --run "$R"
python tools/rfc.py doctor
python tools/director.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan
python tools/rfc.py close-run --run-id "$RUN_ID" --result PASS --closeout "$R/CLOSEOUT.md"
python tools/rfc.py promote-module G --to FORMALIZED --fidelity MINIMAL_SPINE --evidence "$R/FROZEN_DERIVATION_SPEC.json"
python tools/rfc.py promote-module G --to IMPLEMENTED --fidelity MINIMAL_SPINE --evidence "$R/solver_outputs/reaction_network/result.json"
python tools/rfc.py promote-module G --to VERIFIED --fidelity MINIMAL_SPINE --evidence "$R/GATE_RESULTS.json"
python tools/rfc.py promote-module G --to PHYSICALLY_EXECUTED --fidelity MINIMAL_SPINE --evidence "$R/primary/G_RECOMBINATION_LAST_SCATTERING_MINIMAL_SPINE.json"
python tools/rfc.py promote-module G --to INDEPENDENTLY_REPRODUCED --fidelity MINIMAL_SPINE --evidence "$R/independent/INDEPENDENT_RECONSTRUCTION.json"
python tools/rfc.py promote-module G --to FROZEN --fidelity MINIMAL_SPINE --evidence modules/G/frozen/H_G_to_HU.json
python tools/rfc.py freeze modules/G/frozen/H_G_to_HU.json --kind MODULE_HANDOFF
python tools/rfc.py freeze modules/G/frozen/H_G_to_I.json --kind MODULE_HANDOFF
python tools/rfc.py record-claim --file "$R/CLAIM_RECORD.json"
python - <<'PY'
import json
from pathlib import Path
r=Path('modules/G/runs/G-160-20260809T025252Z'); c=json.load(open(r/'CLAIM_RECORD.json')); p=Path('STATE.json'); s=json.load(open(p))
s['strongest_supported_claim']=c['text']; s['strongest_unsupported_claim']=c['unsupported_boundary']; s['repair_state']='G160_MINIMAL_SPINE_CLOSED_PENDING_VERIFIED_COMMIT_AND_ADVANCE'; p.write_text(json.dumps(s,indent=2)+'\n')
PY
python tools/rfc.py context
python tools/rfc.py doctor
python tools/rfc.py firewall-scan
git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
git add -A
git commit -m 'Close Module G at its verified scientific scope'
git pull --rebase origin "$BRANCH"
git push origin HEAD:"$BRANCH"
printf 'G160_FINAL_COMMIT=%s\n' "$(git rev-parse HEAD)"
