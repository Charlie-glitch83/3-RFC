#!/usr/bin/env bash
set -euo pipefail
RUN_ID='E-145-20260808T164410Z'
R="modules/E/runs/$RUN_ID"
python -m pip install --disable-pip-version-check -r requirements-lock.txt
python - <<'PY'
import json
s=json.load(open('STATE.json'))
assert s['active_work_unit']=='E-145' and s['current_module']=='E' and s['current_run']=='E-145-20260808T164410Z',s
assert s['modules']['D']['evidence_state']=='FROZEN' and s['modules']['D']['fidelity']=='PRODUCTION',s['modules']['D']
PY
python tools/rfc.py reopen-module E --fidelity PRODUCTION --evidence recovery/BG_SUPERSEDING_LINEAGE_PACKET.md
python tools/execute_e145.py prepare --run "$R"
cat > /tmp/E-WL-001-output.txt <<'EOF'
Symbol::undefined2: Warning: Global symbols "S, S, S" are undefined.
General::messages: Messages were generated which may indicate errors.

Out[1]= "<|\"call\" -> \"E-WL-001\", \"residual\" -> {{0, 0}, {0, 0}}, \"pass\" -> True, \"leftNullspace\" -> {\"{1, 0, 1}\", \"{-1, 1, 0}\"}|>"
EOF
cat > /tmp/E-WL-002-output.txt <<'EOF'
Symbol::undefined2: Warning: Global symbols "S, S, J, J" are undefined.
General::messages: Messages were generated which may indicate errors.

Out[1]= "<|\"call\" -> \"E-WL-002\", \"rhs\" -> \"{d*kr - kf*n*p, d*kr - kf*n*p, -(d*kr) + kf*n*p}\", \"jacobian\" -> \"{{-(kf*p), -(kf*n), kr}, {-(kf*p), -(kf*n), kr}, {kf*p, kf*n, -kr}}\", \"conservationCheck\" -> \"0\"|>"
EOF
python tools/director.py wolfram-record --run "$RUN_ID" --call E-WL-001 --output /tmp/E-WL-001-output.txt
python tools/director.py wolfram-record --run "$RUN_ID" --call E-WL-002 --output /tmp/E-WL-002-output.txt
python tools/run_reference_checks.py --module E --output "$R/reference_checks.json"
python tools/materialize_solver_config.py --template "$R/solver_templates/E_reaction_network.template.json" --binding-sheet "$R/binding_sheets/E_reaction_network.bindings.json" --output "$R/solver_configs/E_reaction_network.json"
python tools/run_configured_solver.py --config "$R/solver_configs/E_reaction_network.json" --output-dir "$R/solver_outputs/reaction_network"
python - <<'PY'
import json
r=json.load(open('modules/E/runs/E-145-20260808T164410Z/solver_outputs/reaction_network/result.json')); assert r['success'] is True,r
PY
python tools/execute_e145.py execute --run "$R"
rm -rf /tmp/e145-replay; mkdir -p /tmp/e145-replay
python tools/execute_e145.py execute --run "$R" --output-root /tmp/e145-replay
python tools/execute_e145.py finalize --run "$R" --replay-root /tmp/e145-replay
python tools/rfc.py doctor
python tools/director.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan
python tools/rfc.py close-run --run-id "$RUN_ID" --result PASS --closeout "$R/CLOSEOUT.md"
python tools/rfc.py promote-module E --to FORMALIZED --fidelity PRODUCTION --evidence "$R/FROZEN_DERIVATION_SPEC.json"
python tools/rfc.py promote-module E --to IMPLEMENTED --fidelity PRODUCTION --evidence "$R/solver_outputs/reaction_network/result.json"
python tools/rfc.py promote-module E --to VERIFIED --fidelity PRODUCTION --evidence "$R/GATE_RESULTS.json"
python tools/rfc.py promote-module E --to PHYSICALLY_EXECUTED --fidelity PRODUCTION --evidence "$R/primary/NUCLEOSYNTHESIS_V2.json"
python tools/rfc.py promote-module E --to INDEPENDENTLY_REPRODUCED --fidelity PRODUCTION --evidence "$R/independent/INDEPENDENT_RECONSTRUCTION.json"
python tools/rfc.py promote-module E --to FROZEN --fidelity PRODUCTION --evidence modules/E/frozen/H_E_to_F_v2.json
python tools/rfc.py advance --task E-145 --result PASS --evidence "$R/CLOSEOUT.md"
python tools/rfc.py context
python tools/director.py prepare-active
python tools/rfc.py doctor
python tools/rfc.py firewall-scan
python - <<'PY'
import json
s=json.load(open('STATE.json')); q={x['id']:x for x in json.load(open('WORK_QUEUE.json'))['items']}
assert s['modules']['E']['evidence_state']=='FROZEN' and s['modules']['E']['fidelity']=='PRODUCTION',s['modules']['E']
assert q['E-145']['status']=='PASS' and q['F-155']['status']=='ACTIVE',(q['E-145'],q['F-155'])
assert s['active_work_unit']=='F-155' and s['current_module']=='F' and s['current_run'] is None,s
PY
git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
git add -A
git commit -m 'Close E-145 superseding nucleosynthesis replay at verified scope'
git pull --rebase origin agent/frontier-050-execution
git push origin HEAD:agent/frontier-050-execution
