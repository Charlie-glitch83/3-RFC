#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,subprocess,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads(Path(p).read_text())
def dump(p,o):
 p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
def run(cfg,out):
 cp=subprocess.run([sys.executable,str(ROOT/'tools/run_configured_solver.py'),'--config',str(cfg),'--output-dir',str(out)],cwd=ROOT)
 if cp.returncode: raise SystemExit(cp.returncode)
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--run',required=True); a=ap.parse_args(); r=(ROOT/a.run).resolve()
 base=load(r/'solver_configs/G_recombination_network.json'); span=base['t_span']; duration=float(span[1])-float(span[0])
 tol=1e-8; ntol=1e-9; finals={}; rows={}
 for div in [64,128,256,512]:
  c=json.loads(json.dumps(base)); c['max_step']=duration/div
  cpath=r/'convergence'/str(div)/'configs/G_recombination_network.json'; dump(cpath,c)
  rout=r/'convergence'/str(div)/'outputs/reaction_network'; run(cpath,rout)
  rr=load(rout/'result.json'); finals[div]=np.asarray(rr['final'],float)
  t=np.asarray(rr['t'],float); y=np.asarray(rr['y'],float); kf=float(c['model']['parameters']['kf']); kr=float(c['model']['parameters']['kr'])
  opacity=(kf*y[0]*y[1]+kr*y[2]).tolist()
  vc={'schema_version':'1.0','classification':'PROVENANCE_BOUND_EXECUTION_CONFIG','generation_mode':'GENERATION_SEALED','solver':'visibility','model':{'time':t.tolist(),'opacity_rate':opacity,'normalization_tolerance':ntol}}
  vcpath=r/'convergence'/str(div)/'configs/G_visibility.json'; dump(vcpath,vc)
  vout=r/'convergence'/str(div)/'outputs/visibility'; run(vcpath,vout)
  vr=load(vout/'result.json')
  rows[str(div)]={'reaction_success':bool(rr.get('success')),'visibility_success':bool(vr.get('success')),'visibility_normalized':abs(float(vr.get('normalized_integral',0.0))-1.0)<=ntol,'visibility_nonnegative':min(vr.get('normalized_visibility',[0.0]))>=-1e-15}
 ref=finals[512]
 for div in [64,128,256,512]: rows[str(div)]['reaction_endpoint_linf_vs_512']=float(np.max(np.abs(finals[div]-ref))); rows[str(div)]['endpoint_pass']=rows[str(div)]['reaction_endpoint_linf_vs_512']<=tol
 overall=all(all(v for k,v in row.items() if isinstance(v,bool)) for row in rows.values())
 out={'classification':'G160_FROZEN_CONVERGENCE_MATRIX','divisors':[64,128,256,512],'endpoint_tolerance':tol,'visibility_normalization_tolerance':ntol,'rows':rows,'pass':overall}
 dump(r/'convergence/CONVERGENCE.json',out); print(json.dumps(out,indent=2)); raise SystemExit(0 if overall else 1)
if __name__=='__main__': main()
