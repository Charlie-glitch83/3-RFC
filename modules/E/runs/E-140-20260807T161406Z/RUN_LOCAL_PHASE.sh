#!/usr/bin/env bash
set -euo pipefail
RUN_DIR='modules/E/runs/E-140-20260807T161406Z'

# Materialize each config only after filling its binding sheet.
# Execute the internally derived primordial reaction network with stoichiometric invariants.
python tools/materialize_solver_config.py --template ${RUN_DIR}/solver_templates/E_reaction_network.template.json --binding-sheet ${RUN_DIR}/binding_sheets/E_reaction_network.bindings.json --output ${RUN_DIR}/solver_configs/E_reaction_network.json

bash tools/finish_local_phase.sh E "${RUN_DIR}"
