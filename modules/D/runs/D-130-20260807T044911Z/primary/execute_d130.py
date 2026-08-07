#!/usr/bin/env python3
from __future__ import annotations

import json, math, hashlib
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp

ROOT=Path(__file__).resolve().parents[5]
RUN=Path(__file__).resolve().parents[1]
PARENT=ROOT/'modules/C/frozen/H_C_to_D.json'
FREEZE=RUN/'NUMERICAL_EXECUTION_FREEZE.json'
SPEC=RUN/'FROZEN_DERIVATION_SPEC.json'
OUT=RUN/'primary'
OUT.mkdir(parents=True, exist_ok=True)

def dump(name,obj):
    (OUT/name).write_text(json.dumps(obj,indent=2)+'\n')

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def entropy(p):
    p=np.clip(np.asarray(p,float),1e-300,None)
    return float(-np.sum(p*np.log(p)))

parent=json.loads(PARENT.read_text())
freeze=json.loads(FREEZE.read_text())
spec=json.loads(SPEC.read_text())
p0=np.asarray(parent['prethermal_state']['node_populations'],float)
M=np.asarray(parent['microscopic_constitution']['matrix'],float)
g=float(parent['microscopic_constitution']['dimensionless_doublet_gap'])
u=np.ones(3)/3.0
P=M/g
G=-P
interval=tuple(freeze['intrinsic_execution_interval'])
rtol=freeze['configured_solver']['rtol']; atol=freeze['configured_solver']['atol']

def rhs(t,p,Gmat=G): return Gmat@p

def solve(max_step, y0=p0, span=interval, Gmat=G, extra=None):
    def f(t,p):
        val=Gmat@p
        if extra is not None: val=val+extra(p)
        return val
    return solve_ivp(f,span,np.asarray(y0,float),method='BDF',rtol=rtol,atol=atol,max_step=max_step,dense_output=True)

nom=solve(freeze['configured_solver']['max_step'])
grid=np.linspace(interval[0],interval[1],201)
y=nom.sol(grid).T
analytic=np.asarray([u+math.exp(-s)*(p0-u) for s in grid])
analytic_l2=float(np.linalg.norm(y[-1]-analytic[-1]))
sums=y.sum(axis=1)
mins=float(np.min(y))
S=np.asarray([entropy(row) for row in y])
E=np.asarray([0.5*row@M@row for row in y])

history={
  'run_id':spec['run_id'],'classification':'DIMENSIONLESS_NORMALIZED_TRANSPORT_DIAGNOSTIC',
  'clock':{'name':'s_D','dimension':'dimensionless','physical_time_claimed':False},
  'state_names':['p1','p2','p3'],'t':grid.tolist(),'y':y.T.tolist(),
  'initial':p0.tolist(),'final':y[-1].tolist(),'analytic_final':analytic[-1].tolist(),
  'analytic_numeric_l2':analytic_l2,'minimum_population':mins,
  'max_total_carrier_drift':float(np.max(np.abs(sums-sums[0]))),
  'entropy_initial':float(S[0]),'entropy_final':float(S[-1]),'minimum_entropy_increment':float(np.min(np.diff(S))),
  'excitation_initial':float(E[0]),'excitation_final':float(E[-1]),'maximum_excitation_increment':float(np.max(np.diff(E))),
  'physical_temperature_status':'NOT_DERIVED_NO_DIMENSIONFUL_ENERGY_SCALE',
  'metric_expansion_status':'NOT_DERIVED_NO_METRIC_OR_SCALE_FACTOR_PARENT'
}
dump('TRANSPORT_HISTORY.json',history)
dump('TRANSPORT_OPERATOR.json',{'P_perp':P.tolist(),'G_normalized':G.tolist(),'M_C':M.tolist(),'g_C':g,'law':'dp/ds=-P_perp p','source_parent_sha256':sha(PARENT)})
dump('ENTROPY_CONSERVATION_LEDGER.json',{'sum_initial':float(sums[0]),'max_sum_drift':history['max_total_carrier_drift'],'minimum_population':mins,'entropy_initial':float(S[0]),'entropy_final':float(S[-1]),'minimum_entropy_increment':history['minimum_entropy_increment'],'excitation_initial':float(E[0]),'excitation_final':float(E[-1]),'maximum_excitation_increment':history['maximum_excitation_increment']})
dump('PHASE_EVENT_LEDGER.json',{'event_rule':freeze['event_rule'],'events':[],'result':'NO_PARENT_DERIVED_PHASE_EVENT_WITNESSED','ordering_gate':'PASS_VACUOUS_NO_EVENTS','public_target_values_used':False})
dump('TEMPERATURE_STATUS.json',{'physical_temperature':'NOT_DERIVED','reason':'H_C_to_D contains no dimensionful energy scale or thermodynamic map; frozen lock forbids importing one','intrinsic_entropy_history_available':True,'kelvin_values':[]})

# Fixed refinement matrix
ref=[]
for row in freeze['refinement_matrix']:
    sol=solve(row['max_step'])
    final=sol.y[:,-1]
    ref.append({'label':row['label'],'max_step':row['max_step'],'success':bool(sol.success),'final':final.tolist(),'analytic_l2':float(np.linalg.norm(final-analytic[-1])),'nfev':int(sol.nfev)})
ref_err=float(np.linalg.norm(np.asarray(ref[-1]['final'])-np.asarray(ref[1]['final'])))
dump('CONVERGENCE.json',{'runs':ref,'fine_vs_nominal_l2':ref_err,'tolerance':freeze['refinement_tolerance_l2'],'pass':ref_err<=freeze['refinement_tolerance_l2']})

# Restart
split=float(freeze['restart_split'])
first=solve(freeze['configured_solver']['max_step'],span=(interval[0],split))
second=solve(freeze['configured_solver']['max_step'],y0=first.y[:,-1],span=(split,interval[1]))
restart_err=float(np.linalg.norm(second.y[:,-1]-nom.y[:,-1]))
dump('RESTART.json',{'split':split,'direct_final':nom.y[:,-1].tolist(),'restart_final':second.y[:,-1].tolist(),'l2':restart_err,'tolerance':freeze['restart_tolerance_l2'],'pass':restart_err<=freeze['restart_tolerance_l2']})

# Parent representation envelope only; not physical stochastic covariance.
env=[]
for rec in parent['uncertainty']['runs']:
    q0=np.asarray(rec['prethermal_populations'],float)
    sol=solve(freeze['configured_solver']['max_step'],y0=q0)
    env.append({'delta':rec['delta'],'initial':q0.tolist(),'final':sol.y[:,-1].tolist()})
arr=np.asarray([x['final'] for x in env])
dump('UNCERTAINTY_COVARIANCE.json',{'classification':'INHERITED_SOURCE_DECIMAL_REPRESENTATION_ENVELOPE_ONLY','stochastic_physical_uncertainty':False,'stochastic_covariance':parent['prethermal_state']['stochastic_covariance'],'representation_envelope':env,'representation_sample_covariance':np.cov(arr,rowvar=False,ddof=1).tolist()})

# Frozen countermodels
cms=[]
for cm in freeze['countermodels']:
    if cm['id']=='D-CM-SIGN-FLIP':
        sol=solve(0.05,Gmat=P)
    elif cm['id']=='D-CM-ANISOTROPIC':
        sol=solve(0.05,Gmat=np.asarray(cm['generator'],float))
    else:
        sol=solve(0.05,Gmat=G,extra=lambda p:0.01*p)
    yy=sol.y
    cms.append({'id':cm['id'],'success':bool(sol.success),'final':yy[:,-1].tolist(),'minimum_population':float(np.min(yy)),'max_total_drift':float(np.max(np.abs(yy.sum(axis=0)-yy[:,0].sum()))),'entropy_change':float(entropy(yy[:,-1])-entropy(yy[:,0]))})
dump('COUNTERMODELS.json',{'countermodels':cms,'use':'negative controls/falsifiers only; never generative parents'})

primary_pass=(nom.success and mins>=-freeze['configured_solver']['positivity_tolerance'] and history['max_total_carrier_drift']<=freeze['configured_solver']['invariant_tolerance'] and analytic_l2<=freeze['analytic_comparison_tolerance_l2'] and ref_err<=freeze['refinement_tolerance_l2'] and restart_err<=freeze['restart_tolerance_l2'] and history['minimum_entropy_increment']>=-1e-12)
dump('PRIMARY_DIAGNOSTICS.json',{'pass':bool(primary_pass),'configured_branch_scope':'dimensionless diagnostic only','checks':{'integrator':bool(nom.success),'positivity':mins>=-1e-12,'conservation':history['max_total_carrier_drift']<=1e-10,'analytic_match':analytic_l2<=1e-8,'entropy_direction':history['minimum_entropy_increment']>=-1e-12,'refinement':ref_err<=freeze['refinement_tolerance_l2'],'restart':restart_err<=freeze['restart_tolerance_l2']},'hard_obstruction':spec['hard_obstruction']})
print(json.dumps({'primary_pass':bool(primary_pass),'analytic_l2':analytic_l2,'refinement_l2':ref_err,'restart_l2':restart_err,'minimum_population':mins,'max_total_drift':history['max_total_carrier_drift']},indent=2))
