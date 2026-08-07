#!/usr/bin/env bash
set -euo pipefail
RUN_DIR='modules/D/runs/D-130-20260807T044911Z'

# Materialize each config only after filling its binding sheet.
# Integrate the frozen nonequilibrium thermal/transport state with explicit invariants.
python tools/materialize_solver_config.py --template ${RUN_DIR}/solver_templates/D_transport.template.json --binding-sheet ${RUN_DIR}/binding_sheets/D_transport.bindings.json --output ${RUN_DIR}/solver_configs/D_transport.json

bash tools/finish_local_phase.sh D "${RUN_DIR}"
