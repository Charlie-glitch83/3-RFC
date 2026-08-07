#!/usr/bin/env python3
from __future__ import annotations

import hashlib, json, math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parents[1]
PARENT = ROOT / 'modules/C/frozen/H_C_to_D.json'
SPEC = RUN / 'FROZEN_DERIVATION_SPEC.json'
LOCK = RUN / 'PRE_EXECUTION_LOCK.json'
OUT = RUN / 'primary'
OUT.mkdir(parents=True, exist_ok=True)

def dump(name, obj):
    (OUT / name).write_text(json.dumps(obj, indent=2) + '\n')

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def entropy(p):
    p = np.clip(np.asarray(p, float), 1e-300, None)
    return float(-np.sum(p * np.log(p)))

def integrate(G, p0, span, max_step, rtol, atol, source=None):
    def rhs(_, p):
        v = G @ p
        if source is not None:
            v = v + source
        return v
    return solve_ivp(rhs, tuple(span), np.asarray(p0, float), method='BDF', rtol=rtol, atol=atol, max_step=max_step, dense_output=True)

parent = json.loads(PARENT.read_text())
spec = json.loads(SPEC.read_text())
lock = json.loads(LOCK.read_text())
assert lock['status'] == 'FROZEN'
assert spec['status'] == 'FROZEN_PRE_EXECUTION'
controls = lock['numerical_controls']
p0 = np.asarray(parent['prethermal_state']['node_populations'], float)
M = np.asarray(parent['microscopic_constitution']['matrix'], float)
g = float(parent['microscopic_constitution']['dimensionless_doublet_gap'])
u = np.ones(3) / 3.0
P = M / g
P_exact = np.eye(3) - np.ones((3,3))/3.0
projector_error = float(np.linalg.norm(P - P_exact))
G = -P
span = controls['execution_interval']
rtol = controls['rtol']; atol = controls['atol']; max_step = controls['primary_max_step']

primary = integrate(G, p0, span, max_step, rtol, atol)
grid = np.linspace(span[0], span[1], 257)
y = primary.sol(grid).T
analytic = np.asarray([u + math.exp(-s) * (p0-u) for s in grid])
sums = y.sum(axis=1)
S = np.asarray([entropy(row) for row in y])
E = np.asarray([0.5 * row @ M @ row for row in y])
analytic_l2 = float(np.linalg.norm(y[-1]-analytic[-1]))
min_p = float(np.min(y))
max_charge_drift = float(np.max(np.abs(sums-sums[0])))
min_entropy_step = float(np.min(np.diff(S)))
max_excitation_step = float(np.max(np.diff(E)))

history = {
  'run_id': spec['run_id'], 'classification': 'DIMENSIONLESS_PARENT_DRIVEN_TRANSPORT_DIAGNOSTIC',
  'intrinsic_clock': 's', 'physical_time_claimed': False, 'execution_interval': span,
  'state_names': ['p1','p2','p3'], 's': grid.tolist(), 'populations': y.T.tolist(),
  'initial': p0.tolist(), 'final': y[-1].tolist(), 'analytic_final': analytic[-1].tolist(),
  'analytic_numeric_l2': analytic_l2, 'minimum_population': min_p,
  'max_total_charge_drift': max_charge_drift,
  'entropy': S.tolist(), 'dimensionless_excitation_functional': E.tolist(),
  'physical_temperature_status': 'NOT_DERIVED_NO_PARENT_ENERGY_SCALE_OR_THERMODYNAMIC_MAP',
  'metric_expansion_status': 'NOT_DERIVED_NO_METRIC_OR_SCALE_FACTOR_PARENT'
}
dump('DISTRIBUTION_HISTORY.json', history)
dump('TEMPERATURE_HISTORY.json', {
  'status':'NOT_DERIVED', 'physical_temperature_values':[], 'unit':None,
  'reason':'Exact C parent contains no dimensionful energy scale or thermodynamic temperature map; frozen D rules forbid importing one.',
  'intrinsic_entropy_history_path':'primary/DISTRIBUTION_HISTORY.json'
})
dump('TRANSPORT_COLLISION_OPERATORS.json', {
  'M_C':M.tolist(),'g_C':g,'P_perp_numeric':P.tolist(),'P_perp_exact_form':'I-11^T/3',
  'projector_reconstruction_l2':projector_error,'normalized_generator':G.tolist(),
  'law':'dp/ds=-P_perp p','physical_collision_rate':'NOT_DERIVED','parent_sha256':sha(PARENT)
})
dump('ENTROPY_CONSERVATION_LEDGER.json', {
  'Q_total_initial':float(sums[0]),'Q_total_max_abs_drift':max_charge_drift,
  'minimum_population':min_p,'entropy_initial':float(S[0]),'entropy_final':float(S[-1]),
  'minimum_entropy_step':min_entropy_step,'dimensionless_excitation_initial':float(E[0]),
  'dimensionless_excitation_final':float(E[-1]),'maximum_excitation_step':max_excitation_step,
  'physical_energy_conservation_status':'NOT_TESTABLE_NO_DIMENSIONFUL_ENERGY_OBJECT_IN_PARENT',
  'charge_conservation_status':'PASS' if max_charge_drift <= controls['invariant_tolerance'] else 'FAIL'
})
dump('PHASE_EVENT_LEDGER.json', {
  'rule':spec['phase_event_rule'],'events':[],
  'status':'NO_PARENT_DERIVED_PHASE_EVENT_WITNESS','ordering':'VACUOUS_NO_EVENTS',
  'observed_or_public_target_values_used':False
})

# Frozen dyadic convergence matrix.
conv=[]
for step in controls['refinement_matrix']:
    sol=integrate(G,p0,span,step,rtol,atol)
    final=sol.y[:,-1]
    conv.append({'max_step':step,'success':bool(sol.success),'nfev':int(sol.nfev),'final':final.tolist(),'analytic_l2':float(np.linalg.norm(final-analytic[-1]))})
errors=[r['analytic_l2'] for r in conv]
convergence_pass=bool(all(r['success'] for r in conv) and max(errors)<=controls['analytic_numeric_l2_tolerance'])
dump('CONVERGENCE.json', {'matrix':conv,'analytic_tolerance':controls['analytic_numeric_l2_tolerance'],'pass':convergence_pass,'note':'BDF convergence of normalized intrinsic branch; no physical-time stiffness claim.'})

# Midpoint restart.
split=controls['restart_split_s']
first=integrate(G,p0,[span[0],split],max_step,rtol,atol)
second=integrate(G,first.y[:,-1],[split,span[1]],max_step,rtol,atol)
restart_l2=float(np.linalg.norm(second.y[:,-1]-primary.y[:,-1]))
restart_pass=restart_l2 <= controls['analytic_numeric_l2_tolerance']
dump('RESTART.json', {'split_s':split,'direct_final':primary.y[:,-1].tolist(),'restart_final':second.y[:,-1].tolist(),'l2':restart_l2,'tolerance':controls['analytic_numeric_l2_tolerance'],'pass':restart_pass})

# Inherited decimal representation envelope only; not stochastic physical uncertainty.
envelope=[]
for rec in parent['uncertainty']['runs']:
    q0=np.asarray(rec['prethermal_populations'],float)
    sol=integrate(G,q0,span,max_step,rtol,atol)
    envelope.append({'delta':rec['delta'],'initial':q0.tolist(),'final':sol.y[:,-1].tolist()})
arr=np.asarray([x['final'] for x in envelope])
dump('UNCERTAINTY_COVARIANCE.json', {
  'classification':'INHERITED_SOURCE_DECIMAL_REPRESENTATION_ENVELOPE_ONLY',
  'stochastic_physical_uncertainty':False,'stochastic_covariance':parent['prethermal_state']['stochastic_covariance'],
  'representation_envelope':envelope,'representation_sample_covariance':np.cov(arr,rowvar=False,ddof=1).tolist()
})

# Structural countermodels/ablations: no public targets and no alternative generative parents.
counter=[]
# 1) exact sign flip of the frozen normalized generator.
sol=integrate(P,p0,span,max_step,rtol,atol)
cy=sol.sol(grid).T
counter.append({'id':'SIGN_FLIP','definition':'dp/ds=+P_perp p','final':cy[-1].tolist(),'minimum_population':float(np.min(cy)),'entropy_change':entropy(cy[-1])-entropy(cy[0]),'role':'negative control for relaxation/entropy direction'})
# 2) all three single-edge normalized K3 support ablations, exhausting label choices.
for a,b in [(0,1),(0,2),(1,2)]:
    L=np.zeros((3,3)); L[a,a]=1; L[b,b]=1; L[a,b]=-1; L[b,a]=-1
    Gedge=-L/2.0
    sol=integrate(Gedge,p0,span,max_step,rtol,atol)
    counter.append({'id':f'SINGLE_EDGE_{a+1}{b+1}','definition':'remove two of three inherited K3 edges; normalize surviving edge relaxation eigenvalue to 1','generator':Gedge.tolist(),'final':sol.y[:,-1].tolist(),'total_drift':float(np.max(np.abs(sol.y.sum(axis=0)-sol.y[:,0].sum()))),'role':'symmetry/support ablation; all label choices executed'})
# 3) exact uniform unit source ablation of conservation.
sol=integrate(G,p0,span,max_step,rtol,atol,source=u)
counter.append({'id':'UNIFORM_SOURCE','definition':'dp/ds=-P_perp p + u','final':sol.y[:,-1].tolist(),'total_change':float(sol.y[:,-1].sum()-sol.y[:,0].sum()),'role':'negative control for total-carrier conservation'})
dump('COUNTERMODELS_ABLATIONS.json', {'classification':'STRUCTURAL_NEGATIVE_CONTROLS_ONLY','generative_parent':False,'public_targets_used':False,'executions':counter})

checks={
  'integrator':bool(primary.success),'projector_reconstruction':projector_error<=1e-12,
  'positive_distributions':min_p>=-controls['positivity_tolerance'],
  'charge_conservation':max_charge_drift<=controls['invariant_tolerance'],
  'analytic_orbit':analytic_l2<=controls['analytic_numeric_l2_tolerance'],
  'entropy_direction':min_entropy_step>=-1e-12,
  'dimensionless_excitation_decay':max_excitation_step<=1e-12,
  'dyadic_convergence':convergence_pass,'restart':restart_pass
}
dump('PRIMARY_DIAGNOSTICS.json', {
  'run_id':spec['run_id'],'diagnostic_pass':bool(all(checks.values())),'checks':checks,
  'hard_obstruction':spec['hard_obstruction'],
  'full_physical_module_D_pass':False,
  'reason':'Physical temperature/clock/phase-event objects remain underived by frozen exact parent.'
})
print(json.dumps({'diagnostic_pass':bool(all(checks.values())),'checks':checks,'analytic_l2':analytic_l2,'restart_l2':restart_l2,'max_charge_drift':max_charge_drift,'minimum_population':min_p},indent=2))
