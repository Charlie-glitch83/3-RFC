#!/usr/bin/env bash
set -euo pipefail
RUN_DIR='modules/C/runs/C-125-20260808T061947Z'

# Materialize each config only after filling its binding sheet.
# Audit internally derived mass/mixing/interaction matrix candidates and their symmetries.
python tools/materialize_solver_config.py --template ${RUN_DIR}/solver_templates/C_spectral_model.template.json --binding-sheet ${RUN_DIR}/binding_sheets/C_spectral_model.bindings.json --output ${RUN_DIR}/solver_configs/C_spectral_model.json

bash tools/finish_local_phase.sh C "${RUN_DIR}"
