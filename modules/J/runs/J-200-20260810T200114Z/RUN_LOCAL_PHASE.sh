#!/usr/bin/env bash
set -euo pipefail
RUN_DIR='modules/J/runs/J-200-20260810T200114Z'

# Materialize each config only after filling its binding sheet.
# Audit and sample the internally derived primordial covariance.
python tools/materialize_solver_config.py --template ${RUN_DIR}/solver_templates/J_covariance.template.json --binding-sheet ${RUN_DIR}/binding_sheets/J_covariance.bindings.json --output ${RUN_DIR}/solver_configs/J_covariance.json
# Generate finite-volume fields with a frozen seed and Hermitian reality.
python tools/materialize_solver_config.py --template ${RUN_DIR}/solver_templates/J_fourier_field.template.json --binding-sheet ${RUN_DIR}/binding_sheets/J_fourier_field.bindings.json --output ${RUN_DIR}/solver_configs/J_fourier_field.json

bash tools/finish_local_phase.sh J "${RUN_DIR}"
