#!/usr/bin/env bash
set -euo pipefail
RUN_DIR='modules/F/runs/F-150-20260808T013006Z'

# Materialize each config only after filling its binding sheet.
# Execute the post-nuclear plasma reaction network.
python tools/materialize_solver_config.py --template ${RUN_DIR}/solver_templates/F_reaction_network.template.json --binding-sheet ${RUN_DIR}/binding_sheets/F_reaction_network.bindings.json --output ${RUN_DIR}/solver_configs/F_reaction_network.json
# Execute coupled plasma/radiation transport.
python tools/materialize_solver_config.py --template ${RUN_DIR}/solver_templates/F_transport.template.json --binding-sheet ${RUN_DIR}/binding_sheets/F_transport.bindings.json --output ${RUN_DIR}/solver_configs/F_transport.json

bash tools/finish_local_phase.sh F "${RUN_DIR}"
