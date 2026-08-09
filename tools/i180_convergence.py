#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'modules/I/runs/I-180-20260809T050839Z'
d=json.loads((R/'FROZEN_DERIVATION_SPEC.json').read_text())
w=d['numerical_witness']
y0=np.asarray(w['initial_state'],float)
k=float(w['parameters']['k'])
A=k*np.asarray([[-1,0,1],[1,-1,0],[0,1,-1]],float)
t0,t1=map(float,w['t_span'])
exact=expm(A*(t1-t0))@y0
rows={}
for ms in (0.125,0.0625,0.03125,0.015625):
    sol=solve_ivp(lambda t,y:A@y,(t0,t1),y0,method='DOP853',rtol=1e-10,atol=1e-12,max_step=ms)
    err=float(np.max(np.abs(sol.y[:,-1]-exact)))
    inv=float(abs(sol.y[:,-1].sum()-y0.sum()))
    min_state=float(sol.y.min())
    rows[str(ms)]={'success':bool(sol.success),'final_linf_vs_exact':err,'total_activity_residual':inv,'minimum_state':min_state,'pass':bool(sol.success and err<=1e-9 and inv<=1e-9 and min_state>=-1e-12)}
errors=[rows[str(x)]['final_linf_vs_exact'] for x in (0.125,0.0625,0.03125,0.015625)]
convergent=all(errors[i+1] <= max(errors[i]*1.05,1e-13) for i in range(len(errors)-1))
mid=(t0+t1)/2
s1=solve_ivp(lambda t,y:A@y,(t0,mid),y0,method='DOP853',rtol=1e-10,atol=1e-12,max_step=0.03125)
s2=solve_ivp(lambda t,y:A@y,(mid,t1),s1.y[:,-1],method='DOP853',rtol=1e-10,atol=1e-12,max_step=0.03125)
full=solve_ivp(lambda t,y:A@y,(t0,t1),y0,method='DOP853',rtol=1e-10,atol=1e-12,max_step=0.03125)
restart=float(np.max(np.abs(s2.y[:,-1]-full.y[:,-1])))
out={'classification':'I180_CONVERGENCE_RESTART_MATRIX','rows':rows,'error_sequence':errors,'monotone_convergence_pass':bool(convergent),'restart_linf':restart,'restart_pass':bool(restart<=1e-10),'pass':bool(all(v['pass'] for v in rows.values()) and convergent and restart<=1e-10)}
(R/'convergence').mkdir(exist_ok=True)
(R/'convergence/I_CONVERGENCE_RESTART.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
raise SystemExit(0 if out['pass'] else 1)
