#!/usr/bin/env bash
set -euo pipefail
RUN_DIR='modules/I/runs/I-180-20260809T050839Z'

# Materialize each config only after filling its binding sheet.
# Integrate the internally derived background geometry/clock system.
python tools/materialize_solver_config.py --template ${RUN_DIR}/solver_templates/I_background_ode.template.json --binding-sheet ${RUN_DIR}/binding_sheets/I_background_ode.bindings.json --output ${RUN_DIR}/solver_configs/I_background_ode.json

bash tools/finish_local_phase.sh I "${RUN_DIR}"
