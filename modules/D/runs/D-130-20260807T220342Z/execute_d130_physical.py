#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from rfc_engine.solvers.transport import run_transport


def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def dump(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def linf(a, b) -> float:
    return float(np.max(np.abs(np.asarray(a, dtype=float) - np.asarray(b, dtype=float))))


def model_from_spec(spec: dict, initial_state=None, t_span=None, max_step=None, rhs=None):
    num = spec['interval_and_numerics']
    law = spec['transport_collision_law']
    return {
        'state_names': spec['state_space']['state_names'],
        'parameters': {'a': float(law['edge_rate_a'])},
        'rhs_expressions': list(rhs or law['rhs_expressions']),
        'initial_state': list(initial_state if initial_state is not None else spec['state_space']['initial_state']),
        't_span': list(t_span if t_span is not None else num['t_span']),
        'method': num['primary_method'],
        'rtol': float(num['rtol']),
        'atol': float(num['atol']),
        'max_step': float(max_step if max_step is not None else num['max_step']),
        'linear_invariants': {'total_carrier': [1.0, 1.0, 1.0], 'Q_total': [1.0, 1.0, 1.0]},
        'invariant_tolerance': float(num['invariant_tolerance']),
        'positivity_required': True,
        'positivity_tolerance': float(num['positivity_tolerance']),
    }


def metrics(t, y, spec):
    t = np.asarray(t, dtype=float)
    p = np.asarray(y, dtype=float)
    if p.ndim == 1:
        p = p.reshape(3, 1)
    M = np.asarray(spec['transport_collision_law']['parent_matrix_M_C'], dtype=float)
    a = float(spec['transport_collision_law']['edge_rate_a'])
    g = float(spec['transport_collision_law']['gap_g_C'])
    u = np.asarray(spec['state_space']['equilibrium_state'], dtype=float).reshape(3, 1)
    d = p - u
    U = np.einsum('it,ij,jt->t', p, M, p)
    p0 = np.asarray(spec['state_space']['initial_state'], dtype=float)
    U0 = float(p0 @ M @ p0)
    Q = U0 - U
    S = -np.sum(p * np.log(p), axis=0)
    sigma = np.zeros(p.shape[1], dtype=float)
    for i in range(3):
        for j in range(i + 1, 3):
            sigma += a * (p[i] - p[j]) * (np.log(p[i]) - np.log(p[j]))
    Veff = np.exp(S)
    X = np.sum(d * d, axis=0)
    denom = (1.0 / 3.0) + X
    q0 = (1.0 / 3.0) / denom
    qexc = X / denom
    ratio = 2.0 * q0 / qexc
    theta = g / np.log(ratio)
    return {
        'U': U,
        'U0': U0,
        'Q_RFL': Q,
        'S': S,
        'sigma': sigma,
        'V_eff': Veff,
        'X': X,
        'q0': q0,
        'qexc': qexc,
        'theta': theta,
    }


def analytic_state(spec: dict, tau: float):
    p0 = np.asarray(spec['state_space']['initial_state'], dtype=float)
    u = np.asarray(spec['state_space']['equilibrium_state'], dtype=float)
    g = float(spec['transport_collision_law']['gap_g_C'])
    return u + (p0 - u) * math.exp(-g * float(tau))


def run_member(matrix, p0, gap, delta, rtol, atol, inv_tol, pos_tol):
    M = np.asarray(matrix, dtype=float)
    a = float(-M[0, 1])
    tend = 1.0 / a
    cfg = {
        'state_names': ['p0', 'p1', 'p2'],
        'parameters': {'a': a},
        'rhs_expressions': [
            'a*(p1-p0)+a*(p2-p0)',
            'a*(p0-p1)+a*(p2-p1)',
            'a*(p0-p2)+a*(p1-p2)',
        ],
        'initial_state': list(map(float, p0)),
        't_span': [0.0, tend],
        'method': 'BDF',
        'rtol': rtol,
        'atol': atol,
        'max_step': tend / 128.0,
        'linear_invariants': {'total_carrier': [1.0, 1.0, 1.0], 'Q_total': [1.0, 1.0, 1.0]},
        'invariant_tolerance': inv_tol,
        'positivity_required': True,
        'positivity_tolerance': pos_tol,
    }
    res = run_transport(cfg)
    if not res['success']:
        raise RuntimeError(f'uncertainty member {delta} transport failed')
    pf = np.asarray(res['final'], dtype=float)
    u = np.ones(3) / 3.0
    U0 = float(np.asarray(p0) @ M @ np.asarray(p0))
    Uf = float(pf @ M @ pf)
    Sf = float(-np.sum(pf * np.log(pf)))
    Xf = float(np.sum((pf - u) ** 2))
    q0 = (1.0 / 3.0) / ((1.0 / 3.0) + Xf)
    qexc = Xf / ((1.0 / 3.0) + Xf)
    thetaf = float(gap / math.log(2.0 * q0 / qexc))
    return {
        'delta': float(delta),
        'a': a,
        'g_C': float(gap),
        't_end': tend,
        'initial_state': list(map(float, p0)),
        'final_state': pf.tolist(),
        'U0': U0,
        'U_final': Uf,
        'Q_RFL_final': U0 - Uf,
        'S_final': Sf,
        'Theta_final': thetaf,
        'event_times': [math.log(2.0) / (2.0 * float(gap)), 1.0 / float(gap), tend],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    ap.add_argument('--solver-result', required=True)
    ap.add_argument('--output-root')
    args = ap.parse_args()

    run = Path(args.run).resolve()
    root = run.parents[3]
    out = Path(args.output_root).resolve() if args.output_root else run
    spec = load(run / 'FROZEN_DERIVATION_SPEC.json')
    parent = load(root / spec['exact_parent']['path'])
    solver_result = load(Path(args.solver_result).resolve())
    if not solver_result.get('success'):
        raise SystemExit('HARD STOP: configured primary transport solver did not pass')

    t = np.asarray(solver_result['t'], dtype=float)
    y = np.asarray(solver_result['y'], dtype=float)
    if y.shape[0] != 3 or y.shape[1] != t.size:
        raise SystemExit('HARD STOP: primary solver result has unexpected shape')
    met = metrics(t, y, spec)
    M = np.asarray(spec['transport_collision_law']['parent_matrix_M_C'], dtype=float)
    G = np.asarray(spec['transport_collision_law']['generator_G_D'], dtype=float)
    p0 = np.asarray(spec['state_space']['initial_state'], dtype=float)
    u = np.asarray(spec['state_space']['equilibrium_state'], dtype=float)
    num = spec['interval_and_numerics']
    tol_num = 1e-8
    inv_tol = float(num['invariant_tolerance'])
    pos_tol = float(num['positivity_tolerance'])

    distribution = {
        'run_id': run.name,
        'classification': 'RFC_PARENT_DRIVEN_NONEQUILIBRIUM_DISTRIBUTION_HISTORY',
        'clock': spec['state_space']['clock'],
        'frame': spec['state_space']['frame'],
        'state_names': spec['state_space']['state_names'],
        't': t.tolist(),
        'populations': y.tolist(),
        'initial_state': y[:, 0].tolist(),
        'final_state': y[:, -1].tolist(),
        'minimum_population': float(np.min(y)),
        'equilibrium_state': u.tolist(),
        'max_total_carrier_drift': float(np.max(np.abs(np.sum(y, axis=0) - np.sum(y[:, 0])))),
        'source_solver_result': str(Path(args.solver_result).resolve()),
    }
    dump(out / 'primary/THERMAL_DISTRIBUTION_HISTORY.json', distribution)

    temperature = {
        'run_id': run.name,
        'classification': 'RFC_INTRINSIC_SPECTRAL_TEMPERATURE_HISTORY',
        'status': spec['temperature_correspondence']['classification'],
        'definition': spec['temperature_correspondence']['intrinsic_spectral_temperature'],
        'units': spec['temperature_correspondence']['units'],
        'kelvin_or_MeV_status': spec['temperature_correspondence']['kelvin_or_MeV_status'],
        'generator_role': 'DIAGNOSTIC_ONLY_DOES_NOT_SELECT_DYNAMICS_OR_EVENTS',
        't': t.tolist(),
        'Theta_D': met['theta'].tolist(),
        'ground_power_fraction_q0': met['q0'].tolist(),
        'doublet_power_fraction_qexc': met['qexc'].tolist(),
        'initial_Theta_D': float(met['theta'][0]),
        'final_Theta_D': float(met['theta'][-1]),
    }
    dump(out / 'primary/TEMPERATURE_HISTORY.json', temperature)

    energy_resid = met['U'] + met['Q_RFL'] - met['U0']
    entropy_ledger = {
        'run_id': run.name,
        'classification': 'QV_TO_RFL_THERMAL_ENTROPY_CONSERVATION_LEDGER',
        't': t.tolist(),
        'constitutive_excitation_U_D': met['U'].tolist(),
        'rfl_transfer_memory_Q_RFL': met['Q_RFL'].tolist(),
        'U_D_initial': float(met['U0']),
        'max_abs_U_plus_Q_minus_U0': float(np.max(np.abs(energy_resid))),
        'shannon_entropy_S_D': met['S'].tolist(),
        'entropy_production_sigma_D': met['sigma'].tolist(),
        'minimum_entropy_production': float(np.min(met['sigma'])),
        'entropy_change': float(met['S'][-1] - met['S'][0]),
        'effective_nonmetric_state_space_volume_V_eff': met['V_eff'].tolist(),
        'V_eff_change': float(met['V_eff'][-1] - met['V_eff'][0]),
        'metric_expansion_claimed': False,
    }
    dump(out / 'primary/ENTROPY_CONSERVATION_LEDGER.json', entropy_ledger)

    operator = {
        'run_id': run.name,
        'classification': 'PARENT_DERIVED_TRANSPORT_COLLISION_OPERATOR',
        'M_C': M.tolist(),
        'G_D': G.tolist(),
        'edge_rate_a': float(spec['transport_collision_law']['edge_rate_a']),
        'gap_g_C': float(spec['transport_collision_law']['gap_g_C']),
        'rhs_expressions': spec['transport_collision_law']['rhs_expressions'],
        'generator_eigenvalues': np.linalg.eigvalsh(G).tolist(),
        'matrix_symmetry_error': float(np.max(np.abs(M - M.T))),
        'generator_row_sum_error': float(np.max(np.abs(np.sum(G, axis=1)))),
        'complete_support': True,
        'new_coefficient_introduced': False,
    }
    dump(out / 'primary/TRANSPORT_COLLISION_OPERATORS.json', operator)

    event_rows = []
    for ev in spec['phase_event_witnesses']:
        tau = float(ev['tau_D'])
        pe = analytic_state(spec, tau)
        mm = metrics(np.asarray([tau]), pe, spec)
        row = {
            'event': ev['event'],
            'tau_D': tau,
            'rule': ev['rule'],
            'meaning': ev['meaning'],
            'state': pe.tolist(),
            'U_D': float(mm['U'][0]),
            'Q_RFL': float(mm['Q_RFL'][0]),
            'S_D': float(mm['S'][0]),
            'Theta_D': float(mm['theta'][0]),
            'V_eff': float(mm['V_eff'][0]),
        }
        if ev['event'] == 'QV_RFL_MEMORY_BALANCE':
            row['witness_residual'] = abs(row['U_D'] - row['Q_RFL'])
        elif ev['event'] == 'GLOBAL_RELAXATION_EFOLD':
            row['witness_residual'] = abs(float(np.linalg.norm(pe-u) / np.linalg.norm(p0-u)) - math.exp(-1.0))
        else:
            row['witness_residual'] = abs(float(np.linalg.norm(pe-u) / np.linalg.norm(p0-u)) - math.exp(-3.0))
        event_rows.append(row)
    event_times = [x['tau_D'] for x in event_rows]
    event_ledger = {
        'run_id': run.name,
        'classification': 'SOURCE_DERIVED_PHASE_EVENT_CHRONOLOGY',
        'events': event_rows,
        'strictly_ordered': all(event_times[i] < event_times[i+1] for i in range(len(event_times)-1)),
        'max_witness_residual': max(float(x['witness_residual']) for x in event_rows),
        'observed_target_used_for_ordering': False,
    }
    dump(out / 'primary/PHASE_EVENT_LEDGER.json', event_ledger)

    convergence_rows = []
    finals = []
    for step in num['convergence_max_steps']:
        res = run_transport(model_from_spec(spec, max_step=float(step)))
        if not res['success']:
            raise SystemExit(f'HARD STOP: convergence run failed at max_step={step}')
        finals.append(res['final'])
        convergence_rows.append({'max_step': float(step), 'final_state': res['final'], 'minimum_state': res['minimum_state'], 'invariants': res['invariants']})
    pair_errors = [linf(finals[i], finals[i+1]) for i in range(len(finals)-1)]
    convergence = {
        'run_id': run.name,
        'classification': 'DYADIC_BDF_MAX_STEP_CONVERGENCE',
        'runs': convergence_rows,
        'successive_final_linf': pair_errors,
        'finest_pair_linf': pair_errors[-1],
        'tolerance': tol_num,
        'pass': pair_errors[-1] <= tol_num,
    }
    dump(out / 'CONVERGENCE.json', convergence)

    mid = 0.5 * (float(num['t_span'][0]) + float(num['t_span'][1]))
    first_half = run_transport(model_from_spec(spec, t_span=[float(num['t_span'][0]), mid]))
    if not first_half['success']:
        raise SystemExit('HARD STOP: checkpoint first-half run failed')
    midpoint_state = first_half['final']
    second_half = run_transport(model_from_spec(spec, initial_state=midpoint_state, t_span=[mid, float(num['t_span'][1])]))
    if not second_half['success']:
        raise SystemExit('HARD STOP: checkpoint restart run failed')
    restart_err = linf(second_half['final'], solver_result['final'])
    checkpoint = {
        'run_id': run.name,
        'checkpoint_id': 'D_MIDPOINT_TRANSPORT_STATE',
        'tau_D': mid,
        'state': midpoint_state,
        'restart_final_state': second_half['final'],
        'primary_final_state': solver_result['final'],
        'linf': restart_err,
        'tolerance': tol_num,
        'pass': restart_err <= tol_num,
    }
    dump(out / 'CHECKPOINT_RECORD.json', checkpoint)

    scalar = run_transport(model_from_spec(spec, initial_state=u.tolist()))
    scalar_difference = linf(scalar['final'], solver_result['final'])
    edge_rhs = [
        'a*(p1-p0)',
        'a*(p0-p1)+a*(p2-p1)',
        'a*(p1-p2)',
    ]
    withheld = run_transport(model_from_spec(spec, rhs=edge_rhs))
    withheld_difference = linf(withheld['final'], solver_result['final']) if withheld.get('final') else float('inf')
    anti_rhs = ['-(' + x + ')' for x in spec['transport_collision_law']['rhs_expressions']]
    anti = run_transport(model_from_spec(spec, rhs=anti_rhs))
    anti_rejected = not anti.get('success', False)
    anti_entropy_change = None
    if anti.get('final'):
        af = np.asarray(anti['final'], dtype=float)
        if np.all(af > 0):
            anti_entropy_change = float(-np.sum(af*np.log(af)) + np.sum(p0*np.log(p0)))
            anti_rejected = anti_rejected or anti_entropy_change < -1e-10 or np.linalg.norm(af-u) > np.linalg.norm(p0-u)
    counter = {
        'run_id': run.name,
        'classification': 'SEMANTIC_COUNTERMODELS_AND_ABLATIONS',
        'scalar_collapse': {'final_state': scalar['final'], 'linf_from_parent_driven_final': scalar_difference, 'rejected': scalar_difference > tol_num},
        'edge_withheld': {'withheld_edge': [0, 2], 'final_state': withheld.get('final'), 'linf_from_full_K3_final': withheld_difference, 'rejected': withheld_difference > tol_num},
        'anti_diffusion': {'solver_success': anti.get('success'), 'final_state': anti.get('final'), 'entropy_change_if_defined': anti_entropy_change, 'rejected': bool(anti_rejected)},
        'nonconservative_parameterized': {'family': 'G_epsilon = G_D + epsilon E_00, epsilon != 0', 'total_derivative_at_parent_state': 'epsilon*p0(0) != 0', 'rejected': True},
        'public_temperature_anchor': {'used': False, 'rejected_by_firewall': True},
    }
    counter['pass'] = all(counter[k]['rejected'] if 'rejected' in counter[k] else True for k in ['scalar_collapse','edge_withheld','anti_diffusion','nonconservative_parameterized']) and not counter['public_temperature_anchor']['used']
    dump(out / 'COUNTERMODELS_AND_ABLATIONS.json', counter)

    members = []
    for mem in parent['uncertainty']['runs']:
        members.append(run_member(mem['matrix'], mem['prethermal_populations'], mem['dimensionless_doublet_gap'], mem['delta'], float(num['rtol']), float(num['atol']), inv_tol, pos_tol))
    F = np.asarray([m['final_state'] for m in members], dtype=float)
    E = np.asarray([m['event_times'] for m in members], dtype=float)
    scalars = np.asarray([[m['U_final'], m['Q_RFL_final'], m['S_final'], m['Theta_final']] for m in members], dtype=float)
    uncertainty = {
        'run_id': run.name,
        'classification': 'INHERITED_DECIMAL_ENVELOPE_UNCERTAINTY_COVARIANCE',
        'stochastic_covariance': np.zeros((3,3)).tolist(),
        'members': members,
        'final_state_mean': F.mean(axis=0).tolist(),
        'final_state_covariance': np.cov(F, rowvar=False, ddof=1).tolist(),
        'event_time_covariance': np.cov(E, rowvar=False, ddof=1).tolist(),
        'thermal_scalar_order': ['U_final','Q_RFL_final','S_final','Theta_final'],
        'thermal_scalar_covariance': np.cov(scalars, rowvar=False, ddof=1).tolist(),
        'retuned': False,
    }
    dump(out / 'primary/UNCERTAINTY_COVARIANCE.json', uncertainty)

    inv_drifts = [float(x.get('max_abs_drift', 0.0)) for x in solver_result.get('invariants', {}).values()]
    primary_gates = {
        'run_id': run.name,
        'classification': 'PRIMARY_GATE_INPUTS_PENDING_INDEPENDENT_RECONSTRUCTION',
        'positive_distributions': {'pass': float(np.min(y)) >= -pos_tol, 'minimum': float(np.min(y)), 'tolerance': pos_tol},
        'energy_charge_conservation': {
            'pass': (max(inv_drifts or [0.0]) <= inv_tol and float(np.max(np.abs(energy_resid))) <= inv_tol),
            'max_linear_invariant_drift': max(inv_drifts or [0.0]),
            'max_energy_ledger_residual': float(np.max(np.abs(energy_resid))),
            'tolerance': inv_tol,
        },
        'event_ordering': {'pass': event_ledger['strictly_ordered'] and event_ledger['max_witness_residual'] <= tol_num, 'max_witness_residual': event_ledger['max_witness_residual']},
        'stiff_solver_convergence': {'pass': convergence['pass'], 'finest_pair_linf': convergence['finest_pair_linf'], 'tolerance': tol_num},
        'restart': {'pass': checkpoint['pass'], 'linf': checkpoint['linf'], 'tolerance': tol_num},
        'entropy_and_countermodels': {'pass': entropy_ledger['minimum_entropy_production'] >= -1e-10 and counter['pass'], 'minimum_entropy_production': entropy_ledger['minimum_entropy_production'], 'countermodels_pass': counter['pass']},
        'independent_reconstruction': {'pass': False, 'status': 'PENDING_SEPARATE_IMPLEMENTATION'},
    }
    dump(out / 'PRIMARY_GATE_INPUTS.json', primary_gates)

    preliminary = {
        'schema_version': '1.0',
        'object_id': 'H_D_to_E_PRELIMINARY',
        'from_module': 'D',
        'to_module': 'E',
        'run_id': run.name,
        'evidence_state': 'PHYSICALLY_EXECUTED_PENDING_INDEPENDENT_AND_CLEAN_REPLAY',
        'fidelity': spec['fidelity'],
        'generation_mode': spec['generation_mode'],
        'exact_parent': spec['exact_parent'],
        'clock': spec['state_space']['clock'],
        'final_distribution': distribution['final_state'],
        'intrinsic_temperature_final': temperature['final_Theta_D'],
        'phase_events': [{'event': x['event'], 'tau_D': x['tau_D']} for x in event_rows],
        'entropy_final': float(met['S'][-1]),
        'rfl_memory_final': float(met['Q_RFL'][-1]),
        'uncertainty': {'final_state_covariance': uncertainty['final_state_covariance'], 'event_time_covariance': uncertainty['event_time_covariance']},
        'claim_boundary': spec['claim_boundary'],
    }
    dump(out / 'primary/H_D_to_E.preliminary.json', preliminary)

    output_paths = [
        'primary/THERMAL_DISTRIBUTION_HISTORY.json','primary/TEMPERATURE_HISTORY.json','primary/PHASE_EVENT_LEDGER.json',
        'primary/TRANSPORT_COLLISION_OPERATORS.json','primary/ENTROPY_CONSERVATION_LEDGER.json','primary/UNCERTAINTY_COVARIANCE.json',
        'CONVERGENCE.json','CHECKPOINT_RECORD.json','COUNTERMODELS_AND_ABLATIONS.json','PRIMARY_GATE_INPUTS.json','primary/H_D_to_E.preliminary.json'
    ]
    manifest_rows = []
    for rel in output_paths:
        path = out / rel
        manifest_rows.append({'path': rel, 'sha256': sha256(path), 'bytes': path.stat().st_size})
    dump(out / 'GENERATED_OUTPUT_MANIFEST_PRE_REPLAY.json', {
        'status': 'PHYSICAL_EXECUTION_COMPLETE_PENDING_INDEPENDENT_AND_CLEAN_REPLAY',
        'generation_mode': spec['generation_mode'],
        'outputs': manifest_rows,
    })

    if not all(v['pass'] for k, v in primary_gates.items() if isinstance(v, dict) and k != 'independent_reconstruction'):
        raise SystemExit('FROZEN D PRIMARY GATES FAILED')
    print(json.dumps({
        'run_id': run.name,
        'primary_final_state': distribution['final_state'],
        'Theta_initial': temperature['initial_Theta_D'],
        'Theta_final': temperature['final_Theta_D'],
        'entropy_change': entropy_ledger['entropy_change'],
        'rfl_memory_final': float(met['Q_RFL'][-1]),
        'finest_convergence_linf': convergence['finest_pair_linf'],
        'restart_linf': checkpoint['linf'],
        'primary_gates_except_independent': 'PASS',
    }, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
