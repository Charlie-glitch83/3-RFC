#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, shutil, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RID='G-165-20260810T144936Z'
R=ROOT/'modules/G/runs'/RID
SELECTED=[
 'modules/G/runs/'+RID+'/primary/G165_ROUTE_REGISTRY.json',
 'modules/G/runs/'+RID+'/primary/G165_PARAMETRIC_RECOMBINATION_HISTORY.json',
 'modules/G/runs/'+RID+'/primary/G165_ROUTE_RESOLVED_PROCESS_ACTIVITY.json',
 'modules/G/runs/'+RID+'/primary/G165_PROCESS_TO_B_EDGE_ANCESTRY_FAMILY.json',
 'modules/G/runs/'+RID+'/primary/G165_AGGREGATE_NO_LOSS_RECONSTRUCTION.json',
 'modules/G/runs/'+RID+'/primary/G165_RADIATION_SURFACE_BRANCH_FAMILY.json',
 'modules/G/runs/'+RID+'/primary/G165_RECOMBINATION_VISIBILITY_STATE.json',
 'modules/G/runs/'+RID+'/independent/INDEPENDENT_RECONSTRUCTION.json',
 'modules/G/frozen/H_G_to_I_v2.json',
 'modules/G/frozen/H_G_to_HU_v2.json'
]
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for c in iter(lambda:f.read(1<<20),b''): h.update(c)
 return h.hexdigest()
primary={x:sha(ROOT/x) for x in SELECTED}
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
tmp=Path(tempfile.mkdtemp(prefix='g165-clean-replay-'))
try:
 archive=subprocess.Popen(['git','archive','HEAD'],cwd=ROOT,stdout=subprocess.PIPE)
 subprocess.run(['tar','-x','-C',str(tmp)],stdin=archive.stdout,check=True)
 if archive.stdout: archive.stdout.close()
 if archive.wait()!=0: raise RuntimeError('git archive failed')
 for cmd in [
  [sys.executable,'tools/g165_execute_branch_family.py','freeze'],
  [sys.executable,'tools/g165_execute_branch_family.py','execute'],
  [sys.executable,'tools/g165_independent_verify.py'],
  [sys.executable,'tools/g165_execute_branch_family.py','finalize']
 ]:
  subprocess.run(cmd,cwd=tmp,check=True,stdout=subprocess.DEVNULL)
 replay={x:sha(tmp/x) for x in SELECTED}
 artifacts={x:{'primary_sha256':primary[x],'replay_sha256':replay[x],'match':primary[x]==replay[x]} for x in SELECTED}
 ok=all(v['match'] for v in artifacts.values())
 rec={'run_id':RID,'result':'PASS' if ok else 'FAIL','clean_checkout':True,'preexecution_commit':commit,'artifact_hashes_match':ok,'replay_method':'fresh git archive of authority commit; deterministic parent-bound G freeze/execute/independent/finalize rerun','artifacts':artifacts}
 (R/'REPLAY_RECORD.json').write_text(json.dumps(rec,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 print(json.dumps({'result':rec['result'],'clean_checkout':True,'artifact_hashes_match':ok,'artifact_count':len(artifacts)},indent=2))
 if not ok: raise SystemExit(1)
finally:
 shutil.rmtree(tmp,ignore_errors=True)
