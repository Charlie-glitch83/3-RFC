#!/usr/bin/env bash
set -euo pipefail
RUN_DIR='modules/G/runs/G-165-20260810T144936Z'

# Materialize each config only after filling its binding sheet.
# Execute nonequilibrium recombination chemistry.
python tools/materialize_solver_config.py --template ${RUN_DIR}/solver_templates/G_recombination_network.template.json --binding-sheet ${RUN_DIR}/binding_sheets/G_recombination_network.bindings.json --output ${RUN_DIR}/solver_configs/G_recombination_network.json
# Construct the physical visibility kernel from the executed opacity history.
python tools/materialize_solver_config.py --template ${RUN_DIR}/solver_templates/G_visibility.template.json --binding-sheet ${RUN_DIR}/binding_sheets/G_visibility.bindings.json --output ${RUN_DIR}/solver_configs/G_visibility.json

bash tools/finish_local_phase.sh G "${RUN_DIR}"
