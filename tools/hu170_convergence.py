#!/usr/bin/env python3
from pathlib import Path
import json, numpy as np
from scipy.linalg import expm
R=Path('modules/HU/runs/HU-170-20260809T045528Z')
d=json.loads((R/'FROZEN_DERIVATION_SPEC.json').read_text())
A=np.asarray(d['numerical_witness']['generator'],float)
x=np.asarray(d['numerical_witness']['initial_state'],float)
C=np.asarray(d['numerical_witness']['initial_covariance'],float)
rows={}
for n in (1,2,4,8,16):
 dt=1.0/n; U=np.eye(A.shape[0])
 for _ in range(n): U=expm(A*dt)@U
 direct=expm(A)
 cov=U@C@U.T
 rows[str(n)]={'operator_linf_vs_direct':float(np.max(np.abs(U-direct))),'state_linf_vs_direct':float(np.max(np.abs(U@x-direct@x))),'covariance_min_eigenvalue':float(np.min(np.linalg.eigvalsh(cov))),'pass':bool(np.max(np.abs(U-direct))<=1e-12 and np.min(np.linalg.eigvalsh(cov))>=-1e-10)}
Uhalf=expm(A*0.5); restart=Uhalf@(Uhalf@x); direct_state=expm(A)@x
out={'classification':'HU170_CONVERGENCE_RESTART_MATRIX','rows':rows,'restart_linf':float(np.max(np.abs(restart-direct_state))),'restart_pass':bool(np.max(np.abs(restart-direct_state))<=1e-12),'pass':all(v['pass'] for v in rows.values()) and bool(np.max(np.abs(restart-direct_state))<=1e-12)}
(R/'convergence').mkdir(exist_ok=True); (R/'convergence/HU_CONVERGENCE_RESTART.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
raise SystemExit(0 if out['pass'] else 1)
