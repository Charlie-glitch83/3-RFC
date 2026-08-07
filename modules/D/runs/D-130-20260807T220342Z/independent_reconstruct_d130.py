#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def dump(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def linf(a, b) -> float:
    return float(np.max(np.abs(np.asarray(a, dtype=float) - np.asarray(b, dtype=float))))


def theta_from_state(p, g):
    p = np.asarray(p, dtype=float)
    u = np.ones(3) / 3.0
    X = float(np.sum((p-u)**2))
    q0 = (1.0/3.0)/((1.0/3.0)+X)
    qexc = X/((1.0/3.0)+X)
    return float(g / math.log(2.0*q0/qexc))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    ap.add_argument('--physical-root')
    ap.add_argument('--output-root')
    args = ap.parse_args()

    run = Path(args.run).resolve()
    root = run.parents[3]
    physical = Path(args.physical_root).resolve() if args.physical_root else run
    out = Path(args.output_root).resolve() if args.output_root else physical
    spec = load(run / 'FROZEN_DERIVATION_SPEC.json')
    parent_path = root / spec['exact_parent']['path']
    parent = load(parent_path)

    M = np.asarray(parent['microscopic_constitution']['matrix'], dtype=float)
    p0 = np.asarray(parent['prethermal_state']['node_populations'], dtype=float)
    g = float(parent['microscopic_constitution']['dimensionless_doublet_gap'])
    a = float(-M[0,1])
    t0, tend = map(float, spec['interval_and_numerics']['t_span'])
    tol = 1e-8
    if abs(g - 3.0*a) > 1e-12:
        raise SystemExit('independent parent reconstruction: g_C != 3a')

    dist = load(physical / 'primary/THERMAL_DISTRIBUTION_HISTORY.json')
    temp = load(physical / 'primary/TEMPERATURE_HISTORY.json')
    events = load(physical / 'primary/PHASE_EVENT_LEDGER.json')
    checkpoint = load(physical / 'CHECKPOINT_RECORD.json')
    primary_gate = load(physical / 'PRIMARY_GATE_INPUTS.json')

    times = np.asarray(dist['t'], dtype=float)
    u = np.ones(3)/3.0
    analytic = np.stack([u + (p0-u)*math.exp(-g*float(t)) for t in times], axis=1)
    primary_y = np.asarray(dist['populations'], dtype=float)
    analytic_linf = linf(analytic, primary_y)

    dop = solve_ivp(lambda _t, p: -M @ p, (t0, tend), p0, method='DOP853', rtol=1e-12, atol=1e-14, max_step=float(spec['interval_and_numerics']['max_step'])/2.0)
    if not dop.success:
        raise SystemExit('independent DOP853 reconstruction failed')
    analytic_final = u + (p0-u)*math.exp(-g*tend)
    primary_final = np.asarray(dist['final_state'], dtype=float)
    final_analytic_linf = linf(analytic_final, primary_final)
    dop_linf = linf(dop.y[:, -1], primary_final)

    event_expected = [math.log(2.0)/(2.0*g), 1.0/g, 1.0/a]
    event_observed = [float(x['tau_D']) for x in events['events']]
    event_linf = linf(event_expected, event_observed)
    theta_initial = theta_from_state(p0, g)
    theta_final = theta_from_state(analytic_final, g)
    theta_error = max(abs(theta_initial - float(temp['initial_Theta_D'])), abs(theta_final - float(temp['final_Theta_D'])))

    independent_pass = analytic_linf <= tol and final_analytic_linf <= tol and dop_linf <= tol and event_linf <= 1e-12 and theta_error <= tol
    result = {
        'run_id': run.name,
        'classification': 'INDEPENDENT_PARENT_ONLY_RECONSTRUCTION',
        'method': 'ANALYTIC_K3_SPECTRAL_RECONSTRUCTION_PLUS_DOP853',
        'trusted_primary_gate_summary': False,
        'parent_path': str(parent_path.relative_to(root)),
        'parent_matrix_reconstructed': M.tolist(),
        'parent_initial_state_reconstructed': p0.tolist(),
        'a_reconstructed': a,
        'g_C_reconstructed': g,
        'analytic_history_linf': analytic_linf,
        'analytic_final_linf': final_analytic_linf,
        'DOP853_final_linf': dop_linf,
        'event_time_linf': event_linf,
        'temperature_endpoint_linf': theta_error,
        'tolerance': tol,
        'pass': independent_pass,
    }
    dump(out / 'independent/INDEPENDENT_RECONSTRUCTION.json', result)

    gates = {
        'run_id': run.name,
        'aggregate_scores_cannot_override': True,
        'componentwise': {
            'positive distributions': primary_gate['positive_distributions'],
            'energy/charge conservation': primary_gate['energy_charge_conservation'],
            'event ordering': primary_gate['event_ordering'],
            'stiff-solver convergence': primary_gate['stiff_solver_convergence'],
            'restart and independent reconstruction': {
                'pass': bool(primary_gate['restart']['pass']) and independent_pass,
                'status': 'PASS' if bool(primary_gate['restart']['pass']) and independent_pass else 'FAIL',
                'restart_linf': checkpoint['linf'],
                'analytic_history_linf': analytic_linf,
                'DOP853_final_linf': dop_linf,
                'tolerance': tol,
            },
            'entropy/countermodels': primary_gate['entropy_and_countermodels'],
        },
    }
    for v in gates['componentwise'].values():
        if 'status' not in v:
            v['status'] = 'PASS' if v.get('pass') else 'FAIL'
    gates['overall'] = 'PASS' if all(v.get('pass') for v in gates['componentwise'].values()) else 'FAIL'
    dump(out / 'GATE_RESULTS.json', gates)

    iv = (
        '# Independent Verification — D-130\n\n'
        'The frozen Module-D law was reconstructed directly from the exact frozen C parent without trusting the primary gate summary. '
        'The verifier rebuilt the complete-support K3 constitutive matrix, edge rate, doublet gap, initial prethermal carrier state, exact spectral relaxation solution, phase-event times, and intrinsic spectral-temperature endpoints. '
        'It then cross-checked the primary BDF history against the exact analytic solution and a separate DOP853 integration.\n\n'
        f"Analytic history L_inf: `{analytic_linf:.17g}`. DOP853 final L_inf: `{dop_linf:.17g}`. Event-time L_inf: `{event_linf:.17g}`. Temperature endpoint L_inf: `{theta_error:.17g}`.\n\n"
        f"**Result: {gates['overall']}.** A separate clean-checkout replay is still required before final freeze/closeout.\n"
    )
    (out / 'INDEPENDENT_VERIFICATION.md').write_text(iv, encoding='utf-8')

    dump(out / 'REPLAY_RECORD.json', {
        'run_id': run.name,
        'result': 'PENDING_CLEAN_CHECKOUT_REPLAY' if gates['overall'] == 'PASS' else 'FAIL',
        'clean_checkout': False,
        'artifact_hashes_match': False,
        'independent_reconstruction_pass': independent_pass,
    })

    if gates['overall'] != 'PASS':
        raise SystemExit('FROZEN D INDEPENDENT GATES FAILED')
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
