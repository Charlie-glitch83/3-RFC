#!/usr/bin/env bash
set -euo pipefail
RUN_DIR='modules/A/runs/A-100-20260806T173458Z'

# Materialize each config only after filling its binding sheet.
# Execute recursive depth law, typed constituents, and complete directed non-self carrier.
python tools/materialize_solver_config.py --template ${RUN_DIR}/solver_templates/A_triad_kernel.template.json --binding-sheet ${RUN_DIR}/binding_sheets/A_triad_kernel.bindings.json --output ${RUN_DIR}/solver_configs/A_triad_kernel.json

bash tools/finish_local_phase.sh A "${RUN_DIR}"
