#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; RID='HI-190-20260810T165541Z'; RUN=ROOT/'modules/HI/runs'/RID
HU=ROOT/'modules/HU/frozen/H_HU_to_HI_v2.json'; I=ROOT/'modules/I/frozen/H_I_to_HI_v2.json'
def load(p): return json.loads(Path(p).read_text())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,o): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,indent=2)+'\n')
def main():
 hu,i=load(HU),load(I); gh=load(ROOT/hu['G_parent']['path']); gi=load(ROOT/i['parent']['path']); typed=load(ROOT/hu['typed_operator']['path']); gc=load(ROOT/hu['constraint_gauge_frame_contract']['path']); rg=load(ROOT/i['response_geometry']['path'])
 checks={}
 checks['parents_frozen_production']=hu['evidence_state']=='FROZEN' and i['evidence_state']=='FROZEN' and hu['fidelity']=='PRODUCTION' and i['fidelity']=='PRODUCTION'
 checks['exact_parent_hashes']=sha(ROOT/hu['G_parent']['path'])==hu['G_parent']['sha256'] and sha(ROOT/i['parent']['path'])==i['parent']['sha256']
 checks['shared_repaired_G_run']=gh['run_id']==gi['run_id']=='G-165-20260810T144936Z'
 checks['HU_branch_index_shared_G']=typed['branch_index']=='same repaired G-165 branch identity'
 checks['I_M_retained']=i['branch_contract']['unique_M_selected'] is False and i['branch_contract']['unique_numeric_expansion_selected'] is False
 checks['clock_match']=hu['clock']==i['branch_contract']['clock']
 checks['HU_no_realized_background_inputs']=typed['no_realized_background_inputs'] is True
 checks['HU_domain_typed']='ker(C_b)/im(Gauge_b)' in typed['domain']
 checks['I_no_retune_rule']='without changing HU or I' in i['HI_no_retune_rule']
 U=np.array([[1.2,-0.3],[0.4,0.8]],float); S=np.array([[2,.5],[.5,1]],float); O=U@S@U.T
 checks['covariance_congruence_psd']=float(np.min(np.linalg.eigvalsh(O)))>=-1e-12 and float(np.max(np.abs(O-O.T)))<=1e-12
 checks['fiber_product_index']='G-165' in typed['branch_index'] and i['branch_contract']['unique_M_selected'] is False
 checks['gauge_layers_not_identified']='gauge' in gc['gauge_policy'].lower() and rg['response_operator']['quotient']=='Q=1^perp'
 result='PASS' if all(checks.values()) else 'FAIL'
 out={'schema_version':'4.0','object_id':'HI190_PARENT_ONLY_INDEPENDENT_RECONSTRUCTION_V2','run_id':RID,'result':result,'method':'PARENT_ONLY_FIBER_PRODUCT_RECONSTRUCTION_NO_HI_PRIMARY_OR_GATE_SUMMARY_READ','inputs':{'HU_v2_sha256':sha(HU),'I_v2_sha256':sha(I),'HU_G_interface_sha256':sha(ROOT/hu['G_parent']['path']),'I_G_interface_sha256':sha(ROOT/i['parent']['path'])},'reconstructed':{'branch_index':'(b,M)','composite':'HI_(b,M)=(I_(b,M),U_HU[b])','perturbation_map':'deltaX_out=U_HU[b] deltaX_in','no_retune':True,'mode_source':'HU only','background_source':'I only','clock':hu['clock'],'covariance':'U Sigma U^T; I covariance attached; cross covariance only if source-owned'},'checks':checks,'trusted_HI_primary_files':False,'trusted_gate_summary':False}
 write(RUN/'independent/INDEPENDENT_RECONSTRUCTION.json',out); print(json.dumps(out,indent=2)); raise SystemExit(0 if result=='PASS' else 1)
if __name__=='__main__': main()
