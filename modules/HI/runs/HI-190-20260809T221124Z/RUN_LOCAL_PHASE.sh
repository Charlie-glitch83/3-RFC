#!/usr/bin/env bash
set -euo pipefail
RUN_DIR='modules/HI/runs/HI-190-20260809T221124Z'

# Materialize each config only after filling its binding sheet.
# Instantiate the frozen transfer operator on the exact realized background.
python tools/materialize_solver_config.py --template ${RUN_DIR}/solver_templates/HI_instantiated_transfer.template.json --binding-sheet ${RUN_DIR}/binding_sheets/HI_instantiated_transfer.bindings.json --output ${RUN_DIR}/solver_configs/HI_instantiated_transfer.json

bash tools/finish_local_phase.sh HI "${RUN_DIR}"
