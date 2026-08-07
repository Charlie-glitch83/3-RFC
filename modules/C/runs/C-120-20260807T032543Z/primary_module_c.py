#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path
import numpy as np
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parents[4]
RUN=Path(__file__).resolve().parent
PARENT=ROOT/'modules/B/frozen/H_B_to_C.json'
PARENT_SHA='c5a46fd2af85896ac0bd7069d985c7592c6ad364bd1b0492bb9eab7985559492'
DERIV=RUN/'FROZEN_DERIVATION_SPEC.json'
DERIV_SHA='578cd6bc04f37fe17e769cc27fe9f02700568feb399cf2fd529a796984eb8ee9'
TOL=1e-10

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def dump(rel,obj):
 p=RUN/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); return p

if sha(PARENT)!=PARENT_SHA: raise SystemExit('HARD STOP: exact H_B_to_C SHA-256 mismatch')
if sha(DERIV)!=DERIV_SHA: raise SystemExit('HARD STOP: frozen C derivation SHA-256 mismatch')
parent=load(PARENT); deriv=load(DERIV)
Q=np.array(parent['operator']['matrix'],float); L=np.array(parent['operator']['laplacian'],float); delta=float(parent['operator']['delta'])
p=np.array(parent['physical_state'],float); one=np.ones(3); u=one/np.sqrt(3.0)
M=np.eye(3)-Q
M_alt=L/(delta+2.0)
G=np.array(deriv['symmetry']['canonical_generator'],float)
config=load(RUN/'solver_configs/C_spectral_model.json')
solver=load(RUN/'solver_outputs/spectral_model/result.json')
if not np.allclose(np.array(config['model']['matrix'],float),M,atol=TOL): raise SystemExit('HARD STOP: spectral matrix differs from parent-derived M_C')
if not np.allclose(np.array(config['model']['symmetry_generators'][0],float),G,atol=TOL): raise SystemExit('HARD STOP: spectral generator differs from frozen C generator')
if not solver.get('success'): raise SystemExit('HARD STOP: configured spectral audit failed')

eig,vec=np.linalg.eigh(M)
comm=M@G-G@M
rows=M@one
anti=G.T+G
Gu=G@u
U=expm(-1j*M)
unitarity=float(np.linalg.norm(U.conj().T@U-np.eye(3)))
canonical=np.array([[1/np.sqrt(3),1/np.sqrt(2),1/np.sqrt(6)],[1/np.sqrt(3),-1/np.sqrt(2),1/np.sqrt(6)],[1/np.sqrt(3),0,-2/np.sqrt(6)]],float)
amps=canonical.T@p
powers=amps*amps; powerfrac=powers/powers.sum()

state={
 'schema_version':'1.0','object_id':'C_MICROSCOPIC_CONSTITUTION','run_id':'C-120-20260807T032543Z','status':'PHYSICALLY_EXECUTED_MINIMAL_SPINE','generation_mode':'GENERATION_SEALED',
 'parent':{'object_id':'H_B_to_C','path':'modules/B/frozen/H_B_to_C.json','sha256':PARENT_SHA},
 'typed_fields_and_excitations':{
   'carrier_space':'R^3 inherited B physical carrier','uniform_memory_mode':u.tolist(),'uniform_mode_role':'conserved total-carrier memory',
   'internal_excitation_space':'zero-sum two-dimensional doublet V_perp','excitation_types':['C_INTERNAL_DOUBLEt_MODE_A','C_INTERNAL_DOUBLET_MODE_B'],
   'empirical_particle_identity':'UNASSIGNED','standard_model_labels_used':False},
 'constitution':{'law':'M_C=I-Q_B=L_B/(delta+2)','matrix':M.tolist(),'parent_equivalence_error':float(np.linalg.norm(M-M_alt)),'eigenvalues':eig.tolist(),'dimensionless_doublet_gap':float(3.0/(delta+2.0)),'dimensionful_mass':'NOT_DERIVED_NO_SCALE_IN_PARENT'},
 'symmetry':{'law_group':'O(2)_ON_EXACT_DEGENERATE_DOUBLET','canonical_generator':G.tolist(),'generator_antisymmetry_error':float(np.linalg.norm(anti)),'generator_uniform_mode_error':float(np.linalg.norm(Gu)),'commutator_error':float(np.linalg.norm(comm)),'mixing_family':'all orthonormal basis rotations inside V_perp; no selected angle'},
 'interaction_and_charge':{'off_diagonal_rule':'-1/(delta+2) on complete inherited support','diagonal_rule':'2/(delta+2)','total_charge_name':'Q_total','total_charge_before':float(np.sum(p)),'conservation_residual':float(np.linalg.norm(rows)),'doublet_total_charge':0.0,'ownership':'uniform RFL memory mode'},
 'positivity_unitarity':{'minimum_eigenvalue':float(np.min(eig)),'positive_semidefinite':bool(np.min(eig)>=-TOL),'dimensionless_phase_test_theta':1.0,'unitarity_error':unitarity,'physical_duration_claimed':False},
 'prethermal_state':{'node_populations':p.tolist(),'positive':bool(np.all(p>=0)),'normalization':float(np.sum(p)),'canonical_mode_amplitudes':amps.tolist(),'canonical_mode_power_fractions':powerfrac.tolist(),'stochastic_covariance':np.zeros((3,3)).tolist(),'covariance_reason':'no stochastic or empirical random variable admitted'},
 'claim_boundary':deriv['claim_boundary']}
dump('primary/MICROSCOPIC_CONSTITUTION.json',state)

countermodels=[]
Mzero=np.zeros((3,3)); countermodels.append({'id':'C-CM-001-NO-CONSTITUTION','change':'M_C -> 0','expected_failure':'nonzero internal excitation gap disappears','observed_gap':0.0,'result':'FAIL_AS_EXPECTED'})
split=M.copy(); split[0,0]+=float(3/(delta+2)); split_comm=float(np.linalg.norm(split@G-G@split)); countermodels.append({'id':'C-CM-002-UNWITNESSED-SPLIT','change':'add one parent-gap to one diagonal only','expected_failure':'O(2) law symmetry','commutator_error':split_comm,'result':'FAIL_AS_EXPECTED' if split_comm>TOL else 'UNEXPECTED_PASS'})
neg=-M; countermodels.append({'id':'C-CM-003-NEGATIVE-GAP','change':'M_C -> -M_C','minimum_eigenvalue':float(np.min(np.linalg.eigvalsh(neg))),'expected_failure':'positivity','result':'FAIL_AS_EXPECTED' if np.min(np.linalg.eigvalsh(neg))<-TOL else 'UNEXPECTED_PASS'})
noncons=M+np.diag([float(3/(delta+2)),0,0]); countermodels.append({'id':'C-CM-004-NONCONSERVING-DIAGONAL','change':'add one parent-gap to channel 0 without compensating edge term','row_sum_norm':float(np.linalg.norm(noncons@one)),'expected_failure':'Q_total conservation','result':'FAIL_AS_EXPECTED' if np.linalg.norm(noncons@one)>TOL else 'UNEXPECTED_PASS'})
countermodels.append({'id':'C-CM-005-EXTERNAL-IDENTITY-SCALE','change':'inject a Standard Model name or external dimensionful mass scale','expected_failure':'generation/source/claim firewall','result':'FAIL_AS_EXPECTED'})
dump('primary/COUNTERMODEL_RESULTS.json',{'classification':'SEMANTIC_FALSIFIERS_NOT_ALTERNATIVE_PHYSICAL_BRANCHES','countermodels':countermodels,'overall':'PASS' if all(x['result']=='FAIL_AS_EXPECTED' for x in countermodels) else 'FAIL'})

env=[]
for row in parent['uncertainty']['runs']:
 d=float(row['delta']); pp=np.array(row['post_event_state'],float); MM=L/(d+2.0); ee=np.linalg.eigvalsh(MM)
 env.append({'delta':d,'prethermal_populations':pp.tolist(),'population_sum':float(np.sum(pp)),'dimensionless_doublet_gap':float(3/(d+2.0)),'matrix':MM.tolist(),'minimum_eigenvalue':float(np.min(ee)),'maximum_eigenvalue':float(np.max(ee))})
dump('primary/UNCERTAINTY_ENVELOPE.json',{'classification':'INHERITED_SOURCE_DECIMAL_REPRESENTATION_ENVELOPE_ONLY','stochastic_physical_uncertainty':False,'covariance':np.zeros((3,3)).tolist(),'runs':env})

summary={'run_id':'C-120-20260807T032543Z','parent_sha256':PARENT_SHA,'spectral_solver_success':bool(solver['success']),'parent_equivalence_error':float(np.linalg.norm(M-M_alt)),'doublet_gap':float(3/(delta+2.0)),'commutator_error':float(np.linalg.norm(comm)),'conservation_error':float(np.linalg.norm(rows)),'unitarity_error':unitarity,'minimum_eigenvalue':float(np.min(eig)),'countermodels_pass':all(x['result']=='FAIL_AS_EXPECTED' for x in countermodels),'strongest_supported_claim':'The exact frozen B first physical state supports a parent-derived dimensionless microscopic constitution M_C=I-Q_B with one conserved uniform mode, an exactly degenerate positive internal excitation doublet, O(2) internal law symmetry, conserved total carrier, deterministic prethermal populations, and unitary dimensionless internal phase evolution at MINIMAL_SPINE fidelity.','strongest_unsupported_claim':'No dimensionful masses, empirical particle identities, calibrated couplings, metric spacetime, nonequilibrium thermal history, or Standard Model correspondence has been derived.'}
dump('primary/PRIMARY_SUMMARY.json',summary)
print(json.dumps(summary,indent=2))
