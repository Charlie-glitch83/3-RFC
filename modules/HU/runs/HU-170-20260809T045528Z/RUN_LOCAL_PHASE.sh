#!/usr/bin/env bash
set -euo pipefail
RUN_DIR='modules/HU/runs/HU-170-20260809T045528Z'

# Materialize each config only after filling its binding sheet.
# Execute and freeze the universal linear transfer operator.
python tools/materialize_solver_config.py --template ${RUN_DIR}/solver_templates/HU_linear_transfer.template.json --binding-sheet ${RUN_DIR}/binding_sheets/HU_linear_transfer.bindings.json --output ${RUN_DIR}/solver_configs/HU_linear_transfer.json

bash tools/finish_local_phase.sh HU "${RUN_DIR}"
