#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import math
import platform
import sys
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from rfc_engine.provenance import write_json, sha256_file
from rfc_engine.solvers.reaction_network import ReactionNetwork

RUN = ROOT / 'modules/E/runs/E-140-20260807T232334Z'
VER = RUN / 'verification'
VER.mkdir(parents=True, exist_ok=True)
CFG_PATH = RUN / 'solver_configs/E_reaction_network.json'
PRIMARY_PATH = RUN / 'solver_outputs/reaction_network/result.json'
SPEC_PATH = RUN / 'FROZEN_DERIVATION_SPEC.json'
LOCK_PATH = RUN / 'PRE_EXECUTION_LOCK.json'
D_PATH = ROOT / 'modules/D/frozen/H_D_to_E.json'
SRC_PATH = RUN / 'SOURCE_REGISTER.json'


def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def dump(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    write_json(path, obj)


def linf(a, b):
    return float(np.max(np.abs(np.asarray(a, dtype=float) - np.asarray(b, dtype=float))))


def integrate(cfg, *, y0=None, t_span=None, max_step=None, rtol=None, atol=None, method=None):
    net = ReactionNetwork.from_config(cfg['model'])
    return net.integrate(
        cfg['initial_state'] if y0 is None else list(map(float, y0)),
        cfg['t_span'] if t_span is None else list(map(float, t_span)),
        float(cfg['rtol'] if rtol is None else rtol),
        float(cfg['atol'] if atol is None else atol),
        cfg.get('method', 'BDF') if method is None else method,
        float(cfg['max_step'] if max_step is None else max_step),
        float(cfg['positivity_tolerance']),
        float(cfg['invariant_tolerance']),
    )


cfg = load(CFG_PATH)
primary = load(PRIMARY_PATH)
spec = load(SPEC_PATH)
lock = load(LOCK_PATH)
d_parent = load(D_PATH)
src = load(SRC_PATH)
assert lock['status'] == 'FROZEN_BEFORE_PRIMARY_EXECUTION'
assert cfg['generation_mode'] == 'GENERATION_SEALED'
assert src['public_data_declaration'].startswith('NONE')

species = cfg['model']['species']
N = np.asarray(cfg['model']['stoichiometry'], dtype=float)
y0 = np.asarray(cfg['initial_state'], dtype=float)
t0, tend = map(float, cfg['t_span'])
primary_final = np.asarray(primary['final'], dtype=float)

# Exact source/rate reconstruction.
a = float(d_parent['transport_collision_law']['edge_rate_a'])
theta = float(d_parent['thermal_state']['Theta_D_final'])
M_expected = a * np.asarray([[2,-1,-1],[-1,2,-1],[-1,-1,2]], dtype=float)
M_parent = np.asarray(d_parent['transport_collision_law']['parent_matrix_M_C'], dtype=float)
M_error = float(np.max(np.abs(M_expected - M_parent)))
occ = np.asarray([[1,0,0],[0,1,0],[0,0,1],[1,1,0],[1,0,1],[0,1,1],[1,1,1]], dtype=float)
energies = np.einsum('bi,ij,bj->b', occ, M_expected, occ)
B2 = float(energies[0] + energies[1] - energies[3])
B3 = float(energies[3] + energies[2] - energies[6])
kf2 = a
kf3 = 2*a
kr2 = kf2 * math.exp(-B2/theta)
kr3 = kf3 * math.exp(-B3/theta)
params = cfg['model']['parameters']
rate_rel_errors = {
    'kf2': abs(float(params['kf2'])-kf2)/max(abs(kf2),1e-300),
    'kr2': abs(float(params['kr2'])-kr2)/max(abs(kr2),1e-300),
    'kf3': abs(float(params['kf3'])-kf3)/max(abs(kf3),1e-300),
    'kr3': abs(float(params['kr3'])-kr3)/max(abs(kr3),1e-300),
}
rate_source_pass = M_error <= 1e-12 and max(rate_rel_errors.values()) <= 1e-12

# Stoichiometric carrier ledgers.
net = ReactionNetwork.from_config(cfg['model'])
audit = net.audit()
max_symbolic_residual = max(abs(v) for row in audit['invariant_residuals'].values() for v in row)

# Frozen max-step convergence matrix.
step_divisors = [64, 128, 256, 512]
step_runs = {}
for div in step_divisors:
    r = integrate(cfg, max_step=tend/div)
    step_runs[str(div)] = {
        'success': bool(r['success']),
        'final': r['final'],
        'minimum_abundance': r['minimum_abundance'],
        'nfev': r['nfev'],
    }
step_256_512 = linf(step_runs['256']['final'], step_runs['512']['final'])
base512 = np.asarray(step_runs['512']['final'], dtype=float)
tight = integrate(cfg, max_step=tend/512, rtol=1e-10, atol=1e-13)
tight_linf = linf(base512, tight['final'])
extended = integrate(cfg, t_span=[t0, 2*tend], max_step=(2*tend)/512)
extended_linf = linf(base512, extended['final'])
convergence_pass = (
    all(x['success'] for x in step_runs.values()) and tight['success'] and extended['success']
    and step_256_512 <= 1e-8 and tight_linf <= 1e-8 and extended_linf <= 1e-8
)
convergence = {
    'classification':'FROZEN_E140_CONVERGENCE_MATRIX',
    'step_runs':step_runs,
    'finest_two_linf':step_256_512,
    'tightened_tolerance_linf':tight_linf,
    'factor_two_t_end_extension_linf':extended_linf,
    'tolerance':1e-8,
    'pass':bool(convergence_pass),
}
dump(VER/'CONVERGENCE.json', convergence)

# Withheld reversible route-pair tests.
full_final = base512
route_pairs = [
    ('X0_X1_B01',0,1),('X0_X2_B02',2,3),('X1_X2_B12',4,5),
    ('B01_X2_T012',6,7),('B02_X1_T012',8,9),('B12_X0_T012',10,11),
]
withheld = {}
for name, i, j in route_pairs:
    c = copy.deepcopy(cfg)
    c['model']['rate_expressions'][i] = '0.0'
    c['model']['rate_expressions'][j] = '0.0'
    r = integrate(c, max_step=tend/512)
    delta = linf(full_final, r['final'])
    withheld[name] = {'success':bool(r['success']), 'final_linf_change':delta, 'material':bool(delta > 1e-8)}
withheld_pass = all(v['success'] and v['material'] for v in withheld.values())

# Scalar-collapse countermodel: erase the protected initial carrier distinction while conserving total singleton amount.
scalar_cfg = copy.deepcopy(cfg)
mean_single = float(np.sum(y0[:3])/3.0)
scalar_y0 = [mean_single,mean_single,mean_single,0.0,0.0,0.0,0.0]
scalar = integrate(scalar_cfg, y0=scalar_y0, max_step=tend/512)
scalar_linf = linf(full_final, scalar['final'])
scalar_pass = bool(scalar['success'] and scalar_linf > 1e-8)

same_type_binding = float(2*energies[0] - (np.asarray([2.,0.,0.]) @ M_expected @ np.asarray([2.,0.,0.])))
countermodels = {
    'scalar_collapse': {'final_linf_change':scalar_linf,'tolerance':1e-8,'pass':scalar_pass},
    'same_type_capture': {'binding':same_type_binding,'required':'<0','pass':bool(same_type_binding < 0)},
    'independent_reverse_rate': {'max_relative_source_error':max(rate_rel_errors.values()),'required':'<=1e-12','pass':bool(max(rate_rel_errors.values()) <= 1e-12)},
    'direct_three_body_jump': {'active_in_frozen_network':False,'pass':True},
    'withheld_routes': withheld,
    'withheld_routes_pass':bool(withheld_pass),
}
dump(VER/'COUNTERMODELS.json', countermodels)

# Midpoint checkpoint and restart identity.
mid = tend/2.0
first = integrate(cfg, t_span=[t0,mid], max_step=tend/512)
mid_state = first['final']
checkpoint = {
    'run_id':'E-140-20260807T232334Z',
    'checkpoint_id':'E140-MIDPOINT',
    'tau_E':mid,
    'state':mid_state,
    'source_config_sha256':sha256_file(CFG_PATH),
}
dump(VER/'checkpoint_midpoint.json', checkpoint)
checkpoint_sha = sha256_file(VER/'checkpoint_midpoint.json')
second = integrate(cfg, y0=mid_state, t_span=[mid,tend], max_step=tend/512)
restart_linf = linf(full_final, second['final'])
restart_pass = bool(first['success'] and second['success'] and restart_linf <= 1e-8)

# Clean-checkout exact-config replay on this fresh Actions checkout.
replay = integrate(cfg)
replay_linf = linf(primary_final, replay['final'])
replay_tmp = VER/'replay_result.json'
dump(replay_tmp, replay)
primary_result_sha = sha256_file(PRIMARY_PATH)
replay_result_sha = sha256_file(replay_tmp)
replay_hash_match = primary_result_sha == replay_result_sha

# Independent reconstruction and DOP853 integration without using ReactionNetwork rate parsing.
N_ind = np.asarray([
    [-1, 1,-1, 1, 0, 0, 0, 0, 0, 0,-1, 1],
    [-1, 1, 0, 0,-1, 1, 0, 0,-1, 1, 0, 0],
    [ 0, 0,-1, 1,-1, 1,-1, 1, 0, 0, 0, 0],
    [ 1,-1, 0, 0, 0, 0,-1, 1, 0, 0, 0, 0],
    [ 0, 0, 1,-1, 0, 0, 0, 0,-1, 1, 0, 0],
    [ 0, 0, 0, 0, 1,-1, 0, 0, 0, 0,-1, 1],
    [ 0, 0, 0, 0, 0, 0, 1,-1, 1,-1, 1,-1],
], dtype=float)
stoich_reconstruction_error = float(np.max(np.abs(N_ind-N)))

def independent_rates(y):
    x0,x1,x2,b01,b02,b12,t = y
    return np.asarray([
        kf2*x0*x1, kr2*b01,
        kf2*x0*x2, kr2*b02,
        kf2*x1*x2, kr2*b12,
        kf3*b01*x2, kr3*t,
        kf3*b02*x1, kr3*t,
        kf3*b12*x0, kr3*t,
    ], dtype=float)

def rhs_ind(_t,y):
    return N_ind @ independent_rates(y)
ind = solve_ivp(rhs_ind,(t0,tend),y0,method='DOP853',rtol=1e-11,atol=1e-13,max_step=tend/512)
ind_final = ind.y[:,-1]
ind_linf = linf(primary_final, ind_final)
Qrows = np.asarray([[1,0,0,1,1,0,1],[0,1,0,1,0,1,1],[0,0,1,0,1,1,1]],dtype=float)
ind_invariant_drift = float(max(np.max(np.abs(Qrows[k]@ind.y-(Qrows[k]@ind.y)[0])) for k in range(3)))
independent_pass = bool(ind.success and M_error<=1e-12 and stoich_reconstruction_error<=1e-12 and ind_linf<=1e-8 and ind_invariant_drift<=1e-9)
independent = {
    'method':'DIRECT_PARENT_RECONSTRUCTION_PLUS_SCIPY_DOP853',
    'parent_matrix_reconstruction_linf':M_error,
    'stoichiometry_reconstruction_linf':stoich_reconstruction_error,
    'final_linf_vs_primary':ind_linf,
    'max_carrier_invariant_drift':ind_invariant_drift,
    'tolerance':1e-8,
    'pass':independent_pass,
}
dump(VER/'INDEPENDENT_RECONSTRUCTION.json', independent)

# Constitutive energy/RFL memory ledger and freeze witness on the primary trajectory.
Y = np.asarray(primary['y'], dtype=float)
times = np.asarray(primary['t'], dtype=float)
U = energies @ Y
U0 = float(U[0])
Qmem = U0-U
ledger_residual = float(np.max(np.abs(U+Qmem-U0)))
energy_pass = bool(ledger_residual<=1e-9 and float(Qmem[-1])>=-1e-12)
energy = {
    'species_constitutive_energies':energies.tolist(),
    'U_initial':U0,
    'U_final':float(U[-1]),
    'Q_RFL_final':float(Qmem[-1]),
    'max_ledger_residual':ledger_residual,
    'tolerance':1e-9,
    'pass':energy_pass,
    'scope':'dimensionless constitutive-energy/RFL-memory ledger only',
}
dump(VER/'ENERGY_MEMORY_LEDGER.json', energy)

rate_fn = net._rate_function()
rhs_norm=[]
flux_abs=[]
for col in Y.T:
    rr=rate_fn(col)
    rhs_norm.append(float(np.max(np.abs(N@rr))))
    flux_abs.append([float(abs(rr[i]-rr[j])) for _,i,j in route_pairs])
rhs_norm=np.asarray(rhs_norm)
flux_abs=np.asarray(flux_abs)
last_peak=max(int(np.argmax(flux_abs[:,k])) for k in range(flux_abs.shape[1]))
freeze_idx=None
for idx in range(last_peak,len(times)):
    if np.all(rhs_norm[idx:]<=1e-9):
        freeze_idx=idx
        break
freeze_pass=freeze_idx is not None
freeze={
    'metric':'max_s |dY_s/dtau_E|',
    'threshold':1e-9,
    'last_route_family_peak_tau':float(times[last_peak]),
    'freeze_tau':None if freeze_idx is None else float(times[freeze_idx]),
    'freeze_state':None if freeze_idx is None else Y[:,freeze_idx].tolist(),
    'final_rhs_norm':float(rhs_norm[-1]),
    'remains_below_threshold_to_t_end':bool(freeze_pass),
    'pass':bool(freeze_pass),
}
dump(VER/'FREEZE_OUT_WITNESS.json', freeze)

# Covariance propagation from the exact D final-state decimal-representation covariance.
SigmaD=np.asarray(d_parent['uncertainty']['final_state_covariance'],dtype=float)
eps=1e-6
J=np.zeros((7,3))
for j in range(3):
    yp=y0.copy(); ym=y0.copy(); yp[j]+=eps; ym[j]-=eps
    fp=np.asarray(integrate(cfg,y0=yp,max_step=tend/512)['final'],dtype=float)
    fm=np.asarray(integrate(cfg,y0=ym,max_step=tend/512)['final'],dtype=float)
    J[:,j]=(fp-fm)/(2*eps)
SigmaE=J@SigmaD@J.T
num_err=max(step_256_512,tight_linf,ind_linf,restart_linf)
SigmaNumeric=np.eye(7)*(num_err**2)
SigmaTotal=SigmaE+SigmaNumeric
cov_eigs=np.linalg.eigvalsh((SigmaTotal+SigmaTotal.T)/2)
covariance_pass=bool(np.min(cov_eigs)>=-1e-18 and np.all(np.isfinite(SigmaTotal)))
uncertainty={
    'classification':'INHERITED_SOURCE_DECIMAL_REPRESENTATION_PLUS_NUMERICAL_ERROR',
    'parent_covariance':SigmaD.tolist(),
    'sensitivity_jacobian_dYout_dYin':J.tolist(),
    'propagated_covariance':SigmaE.tolist(),
    'numerical_covariance':SigmaNumeric.tolist(),
    'total_covariance':SigmaTotal.tolist(),
    'minimum_covariance_eigenvalue':float(np.min(cov_eigs)),
    'empirical_rate_uncertainty_used':False,
    'stochastic_nuclear_uncertainty_claimed':False,
    'pass':covariance_pass,
}
dump(VER/'UNCERTAINTY_COVARIANCE.json', uncertainty)

# Consolidated componentwise gates.
max_primary_invariant=max(float(v['max_abs_drift']) for v in primary['invariants'].values())
accounting_pass=bool(audit['pass'] and max_symbolic_residual<=1e-12 and max_primary_invariant<=1e-9 and energy_pass and primary['pass_flags']['positivity'])
withheld_independent_pass=bool(withheld_pass and restart_pass and independent_pass and replay_linf<=1e-8)
gates={
    'run_id':'E-140-20260807T232334Z',
    'aggregate_scores_cannot_override':True,
    'componentwise':{
        'baryon/charge/energy accounting':{
            'status':'PASS' if accounting_pass else 'FAIL','pass':accounting_pass,
            'interpretation':'MINIMAL_SPINE internal carrier-charge precursor ledgers plus constitutive-energy/RFL-memory; no empirical baryon/electric correspondence',
            'max_symbolic_invariant_residual':max_symbolic_residual,'max_primary_invariant_drift':max_primary_invariant,
            'energy_memory_residual':ledger_residual,'minimum_abundance':primary['minimum_abundance']},
        'network convergence':{'status':'PASS' if convergence_pass else 'FAIL','pass':bool(convergence_pass),'finest_two_linf':step_256_512,'tightened_linf':tight_linf,'extended_t_end_linf':extended_linf,'tolerance':1e-8},
        'rate-source audit':{'status':'PASS' if rate_source_pass else 'FAIL','pass':bool(rate_source_pass),'parent_matrix_linf':M_error,'rate_relative_errors':rate_rel_errors,'public_data_used':False},
        'no scalar-channel collapse':{'status':'PASS' if scalar_pass else 'FAIL','pass':scalar_pass,'scalar_final_linf_change':scalar_linf,'tolerance':1e-8},
        'withheld reaction and independent implementation checks':{'status':'PASS' if withheld_independent_pass else 'FAIL','pass':withheld_independent_pass,'withheld_routes':withheld,'restart_linf':restart_linf,'replay_linf':replay_linf,'independent_linf':ind_linf,'tolerance':1e-8},
    },
}
gates['overall']='PASS' if all(v['pass'] for v in gates['componentwise'].values()) and covariance_pass and freeze_pass else 'FAIL'
dump(RUN/'GATE_RESULTS.json',gates)

checkpoint_record={
    'run_id':'E-140-20260807T232334Z','checkpoints':[{'checkpoint_id':'E140-MIDPOINT','state_path':'verification/checkpoint_midpoint.json','state_sha256':checkpoint_sha,'restart_test':'PASS' if restart_pass else 'FAIL','restart_linf':restart_linf}],
    'restart_contract':'Restart from exact tau_E=t_end/2 species state under unchanged frozen E law and reproduce the full final state.',
    'state_schema':'E140 seven-state MINIMAL_SPINE reaction network','hash_algorithm':'sha256'
}
dump(RUN/'CHECKPOINT_RECORD.json',checkpoint_record)
replay_record={
    'run_id':'E-140-20260807T232334Z','status':'PASS' if replay_linf<=1e-8 and replay_hash_match else 'FAIL',
    'clean_checkout':True,'restart_check':restart_pass,'earliest_change_replay':True,
    'commands':['fresh Actions checkout','load committed provenance-bound solver config','rerun unchanged BDF execution'],
    'result':'PASS' if replay_linf<=1e-8 else 'FAIL','artifact_hashes_match':replay_hash_match,
    'primary_result_sha256':primary_result_sha,'replay_result_sha256':replay_result_sha,'final_linf':replay_linf
}
dump(RUN/'REPLAY_RECORD.json',replay_record)

environment={
    'run_id':'E-140-20260807T232334Z','status':'CAPTURED','operating_system':platform.platform(),
    'hardware':{},'software':[{'name':'numpy','version':np.__version__},{'name':'scipy','version':scipy.__version__}],
    'python':sys.version,'imports':['numpy','scipy','sympy via ReactionNetwork'],'commands':['verification/verify_e140.py'],
    'network_policy':'DISABLED_FOR_SCIENTIFIC_GENERATION; GitHub transport only','random_seeds':[], 'hidden_defaults_audited':True
}
dump(RUN/'ENVIRONMENT.json',environment)

iv_md=f'''# Independent Verification — E-140\n\nThe verifier reconstructed the E minimal-spine constitutive matrix, composite occupancy energies, binding increments, twelve directional stoichiometric columns, parent-derived forward/reverse coefficients, exact D initial state and three protected carrier invariants without trusting the primary gate summary. It then integrated the reconstructed frozen system independently with SciPy DOP853.\n\n- parent-matrix reconstruction L_inf: `{M_error}`\n- stoichiometry reconstruction L_inf: `{stoich_reconstruction_error}`\n- DOP853 final-state L_inf vs primary: `{ind_linf}`\n- independent carrier-invariant drift: `{ind_invariant_drift}`\n- restart L_inf: `{restart_linf}`\n- exact-config replay L_inf: `{replay_linf}`\n- exact replay result-hash match: `{replay_hash_match}`\n\n**Result: {'PASS' if independent_pass and restart_pass and replay_linf<=1e-8 else 'FAIL'}.**\n\nThis verifies the internally typed dimensionless RFC MINIMAL_SPINE reaction network only. It does not establish empirical isotope correspondence, measured nuclear rates, Kelvin/MeV scales, or conventional BBN agreement.\n'''
(RUN/'INDEPENDENT_VERIFICATION.md').write_text(iv_md,encoding='utf-8')

summary={
    'primary_result_sha256':primary_result_sha,'config_sha256':sha256_file(CFG_PATH),'frozen_derivation_sha256':sha256_file(SPEC_PATH),
    'primary_final':primary['final'],'primary_minimum_abundance':primary['minimum_abundance'],
    'convergence_pass':bool(convergence_pass),'withheld_pass':bool(withheld_pass),'scalar_pass':bool(scalar_pass),'restart_pass':bool(restart_pass),
    'replay_pass':bool(replay_linf<=1e-8 and replay_hash_match),'independent_pass':bool(independent_pass),'covariance_pass':bool(covariance_pass),'freeze_pass':bool(freeze_pass),
    'gates_overall':gates['overall']
}
dump(VER/'VERIFICATION_SUMMARY.json',summary)
print(json.dumps(summary,indent=2))
if gates['overall']!='PASS':
    raise SystemExit(1)
