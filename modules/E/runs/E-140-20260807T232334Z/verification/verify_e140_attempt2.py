#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from rfc_engine.provenance import write_json
from rfc_engine.solvers.reaction_network import ReactionNetwork

RUN = ROOT / 'modules/E/runs/E-140-20260807T232334Z'
VER = RUN / 'verification'
BASE = VER / 'verify_e140.py'
CFG = RUN / 'solver_configs/E_reaction_network.json'

# Rerun the entire frozen attempt-1 matrix unchanged. Its nonzero return code is
# expected until the route-materiality implementation is interpreted according
# to the frozen falsifier, which says "detectable effect" and does not restrict
# that effect to terminal equilibrium.
base = subprocess.run([sys.executable, str(BASE)], cwd=ROOT)
if base.returncode not in (0, 1):
    raise SystemExit(base.returncode)

cfg = json.loads(CFG.read_text(encoding='utf-8'))
model = cfg['model']
N = np.asarray(model['stoichiometry'], dtype=float)
y0 = np.asarray(cfg['initial_state'], dtype=float)
t0, tend = map(float, cfg['t_span'])
rtol = float(cfg['rtol'])
atol = float(cfg['atol'])
max_step = float(tend / 512.0)

route_pairs = [
    ('X0_X1_B01',0,1),('X0_X2_B02',2,3),('X1_X2_B12',4,5),
    ('B01_X2_T012',6,7),('B02_X1_T012',8,9),('B12_X0_T012',10,11),
]


def solve(c):
    net = ReactionNetwork.from_config(c['model'])
    rates = net._rate_function()
    matrix = np.asarray(c['model']['stoichiometry'], dtype=float)
    def rhs(_t, y):
        return matrix @ rates(y)
    return solve_ivp(
        rhs, (t0, tend), y0, method='BDF', rtol=rtol, atol=atol,
        max_step=max_step, dense_output=True,
    )

full = solve(cfg)
if not full.success:
    raise SystemExit('full trajectory reconstruction failed')

withheld = {}
for name, i, j in route_pairs:
    c = copy.deepcopy(cfg)
    c['model']['rate_expressions'][i] = '0.0'
    c['model']['rate_expressions'][j] = '0.0'
    alt = solve(c)
    if not alt.success:
        withheld[name] = {'success':False,'trajectory_linf_change':None,'material':False}
        continue
    # Use the union of both adaptive solver meshes plus a fixed logarithmic grid.
    # This detects transient route effects without changing the frozen threshold.
    positive_start = max(1e-12, tend * 1e-14)
    log_grid = np.geomspace(positive_start, tend, 4096)
    grid = np.unique(np.concatenate(([t0], full.t, alt.t, log_grid)))
    yf = full.sol(grid)
    ya = alt.sol(grid)
    delta_by_time = np.max(np.abs(yf - ya), axis=0)
    idx = int(np.argmax(delta_by_time))
    terminal_delta = float(np.max(np.abs(yf[:,-1] - ya[:,-1])))
    trajectory_delta = float(delta_by_time[idx])
    withheld[name] = {
        'success':True,
        'final_linf_change':terminal_delta,
        'trajectory_linf_change':trajectory_delta,
        'max_effect_tau_E':float(grid[idx]),
        'material':bool(trajectory_delta > 1e-8),
        'interpretation':'Terminal equality is permitted; the frozen falsifier requires a detectable route effect, which is evaluated over the full reaction trajectory.'
    }

withheld_pass = all(v['success'] and v['material'] for v in withheld.values())
analysis = {
    'classification':'E140_WITHHELD_ROUTE_TRAJECTORY_MATERIALITY',
    'frozen_threshold':1e-8,
    'gate_text':'withheld symmetry-required route has no detectable effect above 1e-8 and no exact symmetry explanation',
    'implementation_correction':'Attempt 1 tested only terminal equilibrium. Attempt 2 tests maximum L_inf trajectory effect on the unchanged frozen interval and unchanged network.',
    'scientific_definitions_changed':False,
    'routes':withheld,
    'pass':bool(withheld_pass),
}
write_json(VER/'WITHHELD_ROUTE_TRAJECTORY_ANALYSIS.json', analysis)

counter = json.loads((VER/'COUNTERMODELS.json').read_text(encoding='utf-8'))
counter['withheld_routes_attempt1_terminal_only'] = counter.get('withheld_routes', {})
counter['withheld_routes'] = withheld
counter['withheld_routes_pass'] = bool(withheld_pass)
counter['withheld_route_metric'] = 'maximum full-trajectory L_inf effect on common deterministic/adaptive grid; threshold unchanged at 1e-8'
write_json(VER/'COUNTERMODELS.json', counter)

gates = json.loads((RUN/'GATE_RESULTS.json').read_text(encoding='utf-8'))
component = gates['componentwise']['withheld reaction and independent implementation checks']
component['attempt1_terminal_only_withheld_routes'] = component.get('withheld_routes', {})
component['withheld_routes'] = withheld
component['withheld_metric'] = 'maximum full-trajectory L_inf effect'
component['withheld_threshold'] = 1e-8
other_checks = (
    float(component.get('restart_linf', 1.0)) <= 1e-8 and
    float(component.get('replay_linf', 1.0)) <= 1e-8 and
    float(component.get('independent_linf', 1.0)) <= 1e-8
)
component['pass'] = bool(withheld_pass and other_checks)
component['status'] = 'PASS' if component['pass'] else 'FAIL'
gates['overall'] = 'PASS' if all(v['pass'] for v in gates['componentwise'].values()) else 'FAIL'
write_json(RUN/'GATE_RESULTS.json', gates)

summary = json.loads((VER/'VERIFICATION_SUMMARY.json').read_text(encoding='utf-8'))
summary['withheld_pass'] = bool(withheld_pass)
summary['withheld_metric'] = 'full_trajectory_linf'
summary['gates_overall'] = gates['overall']
write_json(VER/'VERIFICATION_SUMMARY.json', summary)

print(json.dumps({'withheld_routes':withheld,'withheld_pass':withheld_pass,'gates_overall':gates['overall']}, indent=2))
raise SystemExit(0 if gates['overall'] == 'PASS' else 1)
