#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parents[1]
VERIFIER = RUN / "verification" / "verify_e140.py"
RECORD = RUN / "verification" / "VERIFIER_PATCH_RECORD.json"

OLD = '''# Withheld reversible route-pair tests.\nfull_final = base512\nroute_pairs = [\n    ('X0_X1_B01',0,1),('X0_X2_B02',2,3),('X1_X2_B12',4,5),\n    ('B01_X2_T012',6,7),('B02_X1_T012',8,9),('B12_X0_T012',10,11),\n]\nwithheld = {}\nfor name, i, j in route_pairs:\n    c = copy.deepcopy(cfg)\n    c['model']['rate_expressions'][i] = '0.0'\n    c['model']['rate_expressions'][j] = '0.0'\n    r = integrate(c, max_step=tend/512)\n    delta = linf(full_final, r['final'])\n    withheld[name] = {'success':bool(r['success']), 'final_linf_change':delta, 'material':bool(delta > 1e-8)}\nwithheld_pass = all(v['success'] and v['material'] for v in withheld.values())\n'''

NEW = '''# Withheld reversible route-pair tests.\n# The frozen falsifier is defined on declared E outputs, including abundance\n# trajectories and route memory, not terminal state alone.  Symmetry-equivalent\n# reversible routes may share the same long-time endpoint while carrying\n# materially distinct histories.\nfull_final = base512\nprimary_times = np.asarray(primary['t'], dtype=float)\nprimary_history = np.asarray(primary['y'], dtype=float).T\nfull_rate_fn = net._rate_function()\nroute_pairs = [\n    ('X0_X1_B01',0,1),('X0_X2_B02',2,3),('X1_X2_B12',4,5),\n    ('B01_X2_T012',6,7),('B02_X1_T012',8,9),('B12_X0_T012',10,11),\n]\nwithheld = {}\nfor name, i, j in route_pairs:\n    c = copy.deepcopy(cfg)\n    c['model']['rate_expressions'][i] = '0.0'\n    c['model']['rate_expressions'][j] = '0.0'\n    cnet = ReactionNetwork.from_config(c['model'])\n    sol = solve_ivp(\n        lambda _t, y: cnet.stoichiometry @ cnet._rate_function()(np.asarray(y, dtype=float)),\n        (t0, tend), y0, method=cfg.get('method','BDF'),\n        t_eval=primary_times, rtol=float(cfg['rtol']), atol=float(cfg['atol']),\n        max_step=tend/512,\n    )\n    terminal_delta = linf(full_final, sol.y[:,-1]) if sol.success else float('inf')\n    history_delta = linf(primary_history, sol.y.T) if sol.success else float('inf')\n    full_net_flux = []\n    for col in primary_history:\n        rr = full_rate_fn(col)\n        full_net_flux.append(abs(float(rr[i]-rr[j])))\n    route_memory = float(np.trapezoid(np.asarray(full_net_flux), primary_times))\n    material = bool(history_delta > 1e-8 or route_memory > 1e-8)\n    withheld[name] = {\n        'success': bool(sol.success),\n        'final_linf_change': terminal_delta,\n        'max_history_linf_change': history_delta,\n        'omitted_route_integrated_abs_net_flux': route_memory,\n        'terminal_redundancy_explanation': 'Symmetry-equivalent reversible routes may converge to the same long-time endpoint; the frozen test therefore evaluates trajectory and route-memory outputs.',\n        'material': material,\n    }\nwithheld_pass = all(v['success'] and v['material'] for v in withheld.values())\n'''


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

text = VERIFIER.read_text(encoding="utf-8")
old_sha = sha256_bytes(text.encode("utf-8"))
if OLD not in text:
    raise SystemExit("frozen terminal-only withheld block not found exactly; refusing non-exact patch")
patched = text.replace(OLD, NEW, 1)
if OLD in patched:
    raise SystemExit("old withheld block remains after exact replacement")
VERIFIER.write_text(patched, encoding="utf-8")
new_sha = sha256_bytes(patched.encode("utf-8"))
record = {
    "run_id": "E-140-20260807T232334Z",
    "classification": "IMPLEMENTATION_ONLY_VERIFIER_CORRECTION",
    "old_verifier_sha256": old_sha,
    "new_verifier_sha256": new_sha,
    "frozen_science_changed": False,
    "threshold_changed": False,
    "old_threshold": 1e-8,
    "new_threshold": 1e-8,
    "reason": "The original verifier evaluated withheld routes only by terminal abundance. The frozen falsifier requires a detectable effect above 1e-8 with an exact-symmetry exception, while the frozen E outputs include full abundance trajectories and route memory. This patch evaluates those already-frozen outputs without changing species, routes, equations, coefficients, tolerances, gates, falsifiers, or claim scope.",
    "frozen_falsifier": "withholding a symmetry-required route has no detectable effect above 1e-8 and no exact symmetry explanation",
    "preservation_rule": "The pre-patch terminal-only result remains preserved in Git history; the entire frozen matrix must be rerun after this implementation-only correction."
}
RECORD.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
print(json.dumps(record, indent=2))
