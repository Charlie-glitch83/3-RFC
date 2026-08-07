#!/usr/bin/env bash
set -euo pipefail
RUN_DIR='modules/B/runs/B-110-20260807T002248Z'

# Materialize each config only after filling its binding sheet.
# Execute the frozen Big Implosion compression operator on the exact A parent.
python tools/materialize_solver_config.py --template ${RUN_DIR}/solver_templates/B_big_implosion.template.json --binding-sheet ${RUN_DIR}/binding_sheets/B_big_implosion.bindings.json --output ${RUN_DIR}/solver_configs/B_big_implosion.json

bash tools/finish_local_phase.sh B "${RUN_DIR}"
