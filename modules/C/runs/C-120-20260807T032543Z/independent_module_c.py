#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[4]; RUN=Path(__file__).resolve().parent
PARENT=ROOT/'modules/B/frozen/H_B_to_C.json'; PARENT_SHA='c5a46fd2af85896ac0bd7069d985c7592c6ad364bd1b0492bb9eab7985559492'; TOL=1e-10

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def dump(rel,obj):
 p=RUN/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
if sha(PARENT)!=PARENT_SHA: raise SystemExit('HARD STOP: parent hash mismatch')
parent=load(PARENT); primary=load(RUN/'primary/MICROSCOPIC_CONSTITUTION.json')
delta=float(parent['operator']['delta']); L=np.array(parent['operator']['laplacian'],float); p=np.array(parent['physical_state'],float)
M=L/(delta+2.0); gap=float(3.0/(delta+2.0)); u=np.ones(3)/np.sqrt(3.0)
G=np.array([[0.,-1/np.sqrt(3),1/np.sqrt(3)],[1/np.sqrt(3),0.,-1/np.sqrt(3)],[-1/np.sqrt(3),1/np.sqrt(3),0.]])
eig=np.linalg.eigvalsh(M); U=expm(-1j*M)
pm=np.array(primary['constitution']['matrix'],float)
rec={
 'run_id':'C-120-20260807T032543Z','method':'ANALYTIC_K3_PARENT_RECONSTRUCTION_WITHOUT_PRIMARY_SOLVER_MATRIX','parent_sha256':PARENT_SHA,
 'reconstructed':{'matrix':M.tolist(),'uniform_mode':u.tolist(),'analytic_spectrum':[0.0,gap,gap],'numeric_spectrum':eig.tolist(),'generator':G.tolist(),'prethermal_populations':p.tolist(),'population_sum':float(np.sum(p))},
 'checks':{'matrix_vs_primary_l2_error':float(np.linalg.norm(M-pm)),'uniform_zero_mode_error':float(np.linalg.norm(M@u)),'generator_antisymmetry_error':float(np.linalg.norm(G.T+G)),'generator_commutator_error':float(np.linalg.norm(M@G-G@M)),'positivity_minimum_eigenvalue':float(np.min(eig)),'unitarity_error_theta_1':float(np.linalg.norm(U.conj().T@U-np.eye(3))),'population_normalization_error':abs(float(np.sum(p))-1.0)},
 'pass':bool(np.linalg.norm(M-pm)<=TOL and np.linalg.norm(M@u)<=TOL and np.linalg.norm(G.T+G)<=TOL and np.linalg.norm(M@G-G@M)<=TOL and np.min(eig)>=-TOL and np.linalg.norm(U.conj().T@U-np.eye(3))<=TOL and abs(np.sum(p)-1)<=TOL),
 'trust_boundary':'Used exact H_B_to_C, analytic K3 structure, and the final primary matrix only for comparison. Did not trust primary gates, spectral solver eigenvectors, closeout, or claim conclusions.'}
dump('independent/INDEPENDENT_RECONSTRUCTION.json',rec)
print(json.dumps(rec,indent=2))
