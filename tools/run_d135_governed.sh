#!/usr/bin/env bash
set -euo pipefail
RUN_ID='D-135-20260808T163243Z'
R="modules/D/runs/$RUN_ID"
python -m pip install --disable-pip-version-check -r requirements-lock.txt
python - <<'PY'
import json
s=json.load(open('STATE.json'))
assert s['active_work_unit']=='D-135' and s['current_module']=='D' and s['current_run']=='D-135-20260808T163243Z',s
assert s['modules']['C']['evidence_state']=='FROZEN' and s['modules']['C']['fidelity']=='PRODUCTION'
PY
python tools/rfc.py reopen-module D --fidelity PRODUCTION --evidence recovery/BG_SUPERSEDING_LINEAGE_PACKET.md
python tools/execute_d135.py prepare --run "$R"
cat > /tmp/D-WL-001-output.txt <<'EOF'
Symbol::undefined2: Warning: Global symbols "V, V, V" are undefined.
Part::pkspec1: -- Message text not found -- (#1)
Part::pkspec1: -- Message text not found -- (Internal`ProcessEquations`ProcessEquationsDump`i)
Part::pkspec1: -- Message text not found -- (#1)
Part::pkspec1: -- Message text not found -- (Internal`ProcessEquations`ProcessEquationsDump`i)
General::messages: Messages were generated which may indicate errors.

Out[1]= "<|\"call\" -> \"D-WL-001\", \"solution\" -> \"{(x0 + E^(2*k*t)*x0 - y0 + E^(2*k*t)*y0)/(2*E^(2*k*t)), (-x0 + E^(2*k*t)*x0 + y0 + E^(2*k*t)*y0)/(2*E^(2*k*t))}\", \"conservedTotal\" -> \"x0 + y0\", \"lyapunovDerivative\" -> \"-4*k*(x[t] - y[t])^2\", \"decayPass\" -> True|>"
EOF
cat > /tmp/D-WL-002-output.txt <<'EOF'
Symbol::undefined2: Warning: Global symbols "J, J" are undefined.
General::messages: Messages were generated which may indicate errors.

Out[1]= "<|\"call\" -> \"D-WL-002\", \"eigenvalues\" -> {\"0\", \"-k1 - k2\"}, \"conservedModePresent\" -> True, \"relaxationMode\" -> \"-k1 - k2\"|>"
EOF
python tools/director.py wolfram-record --run "$RUN_ID" --call D-WL-001 --output /tmp/D-WL-001-output.txt
python tools/director.py wolfram-record --run "$RUN_ID" --call D-WL-002 --output /tmp/D-WL-002-output.txt
python tools/run_reference_checks.py --module D --output "$R/reference_checks.json"
python tools/materialize_solver_config.py --template "$R/solver_templates/D_transport.template.json" --binding-sheet "$R/binding_sheets/D_transport.bindings.json" --output "$R/solver_configs/D_transport.json"
python tools/run_configured_solver.py --config "$R/solver_configs/D_transport.json" --output-dir "$R/solver_outputs/transport"
python - <<'PY'
import json
r=json.load(open('modules/D/runs/D-135-20260808T163243Z/solver_outputs/transport/result.json')); assert r['success'] is True,r
PY
python tools/execute_d135.py execute --run "$R"
rm -rf /tmp/d135-replay; mkdir -p /tmp/d135-replay
python tools/execute_d135.py execute --run "$R" --output-root /tmp/d135-replay
python tools/execute_d135.py finalize --run "$R" --replay-root /tmp/d135-replay
python tools/rfc.py doctor
python tools/director.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan
python tools/rfc.py close-run --run-id "$RUN_ID" --result PASS --closeout "$R/CLOSEOUT.md"
python tools/rfc.py promote-module D --to FORMALIZED --fidelity PRODUCTION --evidence "$R/FROZEN_DERIVATION_SPEC.json"
python tools/rfc.py promote-module D --to IMPLEMENTED --fidelity PRODUCTION --evidence "$R/solver_outputs/transport/result.json"
python tools/rfc.py promote-module D --to VERIFIED --fidelity PRODUCTION --evidence "$R/GATE_RESULTS.json"
python tools/rfc.py promote-module D --to PHYSICALLY_EXECUTED --fidelity PRODUCTION --evidence "$R/primary/THERMAL_HISTORY_V2.json"
python tools/rfc.py promote-module D --to INDEPENDENTLY_REPRODUCED --fidelity PRODUCTION --evidence "$R/independent/INDEPENDENT_RECONSTRUCTION.json"
python tools/rfc.py promote-module D --to FROZEN --fidelity PRODUCTION --evidence modules/D/frozen/H_D_to_E_v2.json
python tools/rfc.py advance --task D-135 --result PASS --evidence "$R/CLOSEOUT.md"
python tools/rfc.py context
python tools/director.py prepare-active
python tools/rfc.py doctor
python tools/rfc.py firewall-scan
python - <<'PY'
import json
s=json.load(open('STATE.json')); q={x['id']:x for x in json.load(open('WORK_QUEUE.json'))['items']}
assert s['modules']['D']['evidence_state']=='FROZEN' and s['modules']['D']['fidelity']=='PRODUCTION',s['modules']['D']
assert q['D-135']['status']=='PASS' and q['E-145']['status']=='ACTIVE',(q['D-135'],q['E-145'])
assert s['active_work_unit']=='E-145' and s['current_module']=='E' and s['current_run'] is None,s
PY
git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
git add -A
git commit -m 'Close D-135 superseding thermal replay at verified scope'
git pull --rebase origin agent/frontier-050-execution
git push origin HEAD:agent/frontier-050-execution
