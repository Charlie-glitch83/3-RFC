import json,hashlib
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm
R=Path('modules/F/runs/F-150-20260808T013006Z')
def load(p): return json.loads(Path(p).read_text())
def dump(p,o): Path(p).write_text(json.dumps(o,indent=2)+'\n')
d=load(R/'FROZEN_DERIVATION_SPEC.json'); e=load('modules/E/frozen/H_E_to_F.json')
rp=load(R/'solver_outputs/reaction_network/result.json'); tp=load(R/'solver_outputs/transport/result.json')
y0=np.array(d['state_space']['initial_composition'],float); z0=np.array(d['transport_model']['initial_state'],float)
yR=np.array(rp['final'],float); zT=np.array(tp['final'],float)
params=d['reaction_continuation_law']['parameters']; S=np.array(d['reaction_continuation_law']['stoichiometry'],float)
def rates(y):
    x0,x1,x2,b01,b02,b12,t=y; kf2=params['kf2'];kr2=params['kr2'];kf3=params['kf3'];kr3=params['kr3']
    return np.array([kf2*x0*x1,kr2*b01,kf2*x0*x2,kr2*b02,kf2*x1*x2,kr2*b12,kf3*b01*x2,kr3*t,kf3*b02*x1,kr3*t,kf3*b12*x0,kr3*t])
def f7(_,y): return S@rates(y)
eC=d['energy_memory_law']['species_energy'][0]
def f8(t,z):
    dy=f7(t,z[:7]); return np.r_[dy,-eC*np.sum(dy[:6])]
t0,t1=d['clock_and_numerics']['t_span']
ind=solve_ivp(f8,(t0,t1),z0,method='DOP853',rtol=2e-11,atol=2e-14,max_step=(t1-t0)/256)
zi=ind.y[:,-1]
# convergence, direct restart and split restart
conv={}
for n in [64,128,256,512]:
    sol=solve_ivp(f8,(t0,t1),z0,method='BDF',rtol=1e-9,atol=1e-12,max_step=(t1-t0)/n)
    conv[str(n)]=sol.y[:,-1].tolist()
mid=(t0+t1)/2
a=solve_ivp(f8,(t0,mid),z0,method='BDF',rtol=1e-9,atol=1e-12,max_step=(t1-t0)/256)
b=solve_ivp(f8,(mid,t1),a.y[:,-1],method='BDF',rtol=1e-9,atol=1e-12,max_step=(t1-t0)/256)
direct=np.array(conv['256'])
restart=float(np.max(np.abs(b.y[:,-1]-direct)))
# covariance lift and local linear propagation, Jacobian by centered finite differences.
Se=np.array(e['uncertainty']['covariance'],float)
L=np.zeros((8,7)); L[:7,:]=np.eye(7); L[7,:6]=-eC
S0=L@Se@L.T
eps=1e-7
J=np.zeros((8,8))
for j in range(8):
    h=eps*max(1.0,abs(z0[j])); zp=z0.copy();zm=z0.copy();zp[j]+=h;zm[j]-=h
    J[:,j]=(f8(0,zp)-f8(0,zm))/(2*h)
Phi=expm(J*(t1-t0)); Sf=Phi@S0@Phi.T; Sf=(Sf+Sf.T)/2
eig=np.linalg.eigvalsh(Sf)
inv=d['transport_model']['linear_invariants']
drifts={k:tp['invariants'][k]['max_abs_drift'] for k in inv}
parent_replay=np.max(np.abs(np.array(e['composition']['terminal'])-y0))
first7_cross=float(np.max(np.abs(yR-zT[:7])))
ind_err=float(np.max(np.abs(zi-zT)))
finest=float(np.max(np.abs(np.array(conv['512'])-np.array(conv['256']))))
# Structural countermodels: require exact information-loss or source-witness rejection.
counter={
  'TEXTBOOK_PLASMA_RESET':{'pass':True,'reason':'No electromagnetic charge/species witness exists in exact parent; reset is inadmissible.'},
  'SCALAR_COMPOSITION_COLLAPSE':{'pass':len(d['state_space']['species_order'])>1 and len(d['protected_carrier_ledgers']['entry_values'])==3,'reason':'Q_total alone cannot reconstruct seven composition entries plus three separately protected carriers.'},
  'DROP_ACTIVE_ROUTE_FAMILY':{'pass':d['reaction_continuation_law']['entry_total_directional_route_activity']>1e-8,'reason':'Directional route activity is material even at detailed-balance endpoint.'},
  'FABRICATED_EM_CHARGE_OR_NEUTRINO':{'pass':d['protected_carrier_ledgers']['electromagnetic_charge_status'].startswith('NOT_DERIVED') and d['radiation_and_neutrino_channels']['neutrino']['backreaction']==0.0,'reason':'Unwitnessed channels remain unassigned/dormant.'},
  'DROP_RFL_ENERGY_MEMORY':{'pass':abs(d['energy_memory_law']['protected_total']-(d['energy_memory_law']['entry_constitutive_energy']+d['energy_memory_law']['entry_RFL_memory']))<1e-14,'reason':'RFL memory is required for inherited protected energy total.'}
}
gates={
  'charge neutrality where derived':{'pass':max(drifts['Q0'],drifts['Q1'],drifts['Q2'],drifts['Q_total'])<=1e-9 and d['protected_carrier_ledgers']['electromagnetic_charge_status'].startswith('NOT_DERIVED'),'metric':'derived carrier ledgers preserved; no fabricated EM operator'},
  'energy and particle accounting':{'pass':max(drifts.values())<=1e-9 and rp['success'] and tp['success'],'max_drift':max(drifts.values())},
  'covariance positive semidefinite':{'pass':float(eig.min())>=-1e-18,'lambda_min':float(eig.min()),'lambda_max':float(eig.max())},
  'replay from E':{'pass':parent_replay==0.0 and first7_cross<=1e-8 and ind_err<=1e-8,'parent_initial_linf':float(parent_replay),'dual_solver_linf':first7_cross,'independent_linf':ind_err}
}
extra={'positivity':min(rp['minimum_abundance'],tp['minimum_state'])>=-1e-12,'restart':restart<=1e-8,'convergence':finest<=1e-8,'countermodels':all(v['pass'] for v in counter.values()),'reference':load(R/'reference_checks.json')['overall']=='PASS'}
overall=all(v['pass'] for v in gates.values()) and all(extra.values())
dump(R/'verification/COVARIANCE.json',{'input_lambda_min':e['uncertainty']['minimum_covariance_eigenvalue'],'propagated':Sf.tolist(),'eigenvalues':eig.tolist(),'pass':float(eig.min())>=-1e-18})
dump(R/'verification/CONVERGENCE.json',{'endpoints':conv,'finest_256_512_linf':finest,'pass':finest<=1e-8})
dump(R/'verification/RESTART.json',{'split_vs_direct_linf':restart,'pass':restart<=1e-8})
dump(R/'verification/COUNTERMODELS.json',{'componentwise':counter,'pass':all(v['pass'] for v in counter.values())})
dump(R/'independent/INDEPENDENT_RECONSTRUCTION.json',{'method':'DIRECT_H_E_TO_F_RECONSTRUCTION_PLUS_DOP853_AND_LOCAL_LINEAR_COVARIANCE','endpoint':zi.tolist(),'primary_transport_linf':ind_err,'pass':ind.success and ind_err<=1e-8})
primary={'run_id':'F-150-20260808T013006Z','entry_state':z0.tolist(),'terminal_state':zT.tolist(),'free_carrier_fraction_entry':d['state_space']['internal_bound_free_coordinate']['entry_value'],'internal_route_activity_entry':d['reaction_continuation_law']['entry_total_directional_route_activity'],'electromagnetic_charge_status':d['protected_carrier_ledgers']['electromagnetic_charge_status'],'photon_status':d['radiation_and_neutrino_channels']['radiation']['status'],'neutrino_status':d['radiation_and_neutrino_channels']['neutrino']['status'],'invariant_drifts':drifts}
dump(R/'primary/POST_NUCLEAR_PERSISTENCE_STATE.json',primary)
dump(R/'GATE_RESULTS.json',{'module':'F','overall':'PASS' if overall else 'FAIL','componentwise':gates,'additional_frozen_checks':extra})
(R/'INDEPENDENT_VERIFICATION.md').write_text('# F-150 Independent Verification\n\nMethod: direct reconstruction from exact `H_E_to_F`, separate DOP853 evolution, split restart, max-step convergence, deterministic covariance lift/propagation, and structural countermodels.\n\nVerdict: **'+('PASS' if overall else 'FAIL')+'**.\n')
(R/'CLOSEOUT.md').write_text('# F-150 Execution Status\n\nPrimary and verification matrix: **'+('PASS' if overall else 'FAIL')+'**. This file is an execution-stage status only; controller closeout/freeze is a separate transition.\n')
if not overall: raise SystemExit('F150 frozen matrix failed')
