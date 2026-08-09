#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'modules/G/runs/G-160-20260809T025252Z'
FILES=['tools/g160_parent_bound.py','tools/g160_convergence.py','tools/g160_contract_fix.py','tools/run_g160_governed.sh','tools/materialize_solver_config.py','tools/run_configured_solver.py','tools/run_module_pipeline.py','tools/finish_local_phase.sh']
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=RUN/'PRE_EXECUTION_LOCK.json'; d=json.loads(p.read_text())
if d.get('status')!='FROZEN': raise SystemExit('G160 lock is not frozen')
d['implementation_hashes']=[{'path':x,'sha256':sha(ROOT/x)} for x in FILES]
d['implementation_frozen_before_primary_execution']=True
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':'PASS','implementation_hashes':d['implementation_hashes']},indent=2))
