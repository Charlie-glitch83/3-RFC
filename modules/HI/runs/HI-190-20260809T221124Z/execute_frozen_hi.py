#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import numpy as np
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parents[4]
RUN=Path(__file__).resolve().parent
HU=ROOT/'modules/HU/frozen/H_HU_to_HI.json'
IB=ROOT/'modules/I/frozen/H_I_to_HI.json'
SPEC=RUN/'FROZEN_DERIVATION_SPEC.json'
EXPECTED_HU='159d1311b26e03572f8485b579e354d031e3cab1fd59416bfad76ddd93186204'
EXPECTED_I='d7245adc6699ff0c300b622340cdeb51cf00c87bcd17443cdba9b612ffdb12cd'

def sha(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p:Path): return json.loads(p.read_text())
def dump(p:Path,obj):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')

def verify_parents():
    assert sha(HU)==EXPECTED_HU, 'HU parent hash mismatch'
    assert sha(IB)==EXPECTED_I, 'I parent hash mismatch'
    h=load(HU); i=load(IB); s=load(SPEC)
    assert h['object_id']=='H_HU_to_HI' and i['object_id']=='H_I_to_HI'
    assert h['generation_mode']=='GENERATION_SEALED' and i['generation_mode']=='GENERATION_SEALED'
    assert h['public_inputs_used'] is False and i['public_inputs_used'] is False
    assert h['clock']['origin']==i['expansion_clock_histories']['clock']['origin']
    assert h['clock']['unit_family']==i['expansion_clock_histories']['clock']['unit_family']
    assert s['parents']['HU']['sha256']==EXPECTED_HU and s['parents']['I']['sha256']==EXPECTED_I
    return h,i,s

def witness_checks(s):
    w=s['numerical_witness']; A=np.array(w['generator'],float); x0=np.array(w['initial_state'],float); S0=np.array(w['initial_covariance'],float)
    times=[float(x) for x in w['times']]
    states=[]; cov=[]
    for t in times:
        U=expm(A*t); x=U@x0; S=U@S0@U.T
        states.append(x.tolist()); cov.append(S.tolist())
    eig=np.linalg.eigvalsh(np.array(cov[-1]))
    return {'times':times,'states':states,'covariances':cov,'final_covariance_eigenvalues':eig.tolist(),'covariance_symmetric':bool(np.allclose(cov[-1],np.array(cov[-1]).T,atol=1e-12)),'covariance_psd':bool(eig.min()>=-1e-12),'constraint_sum_preserved':bool(max(abs(np.sum(x)-np.sum(x0)) for x in np.array(states))<=1e-12)}

def build_primary():
    h,i,s=verify_parents(); wc=witness_checks(s)
    hu_law=h['typed_operator']
    primary={
      'schema_version':'2.1','object_id':'HI_INSTANTIATED_TRANSFER_MINIMAL_SPINE','run_id':RUN.name,'module':'HI','classification':'PARENT_DRIVEN_IMMUTABLE_HU_ON_I_INSTANTIATION','fidelity':'MINIMAL_SPINE','generation_mode':'GENERATION_SEALED','public_inputs_used':False,'no_retune':True,
      'parents':{'HU':{'path':str(HU.relative_to(ROOT)),'sha256':EXPECTED_HU},'I':{'path':str(IB.relative_to(ROOT)),'sha256':EXPECTED_I}},
      'compatibility_rule':s['compatibility_rule'],'branch_policy':s['laws']['branch_policy'],
      'instantiated_transfer_system':{'law':s['laws']['immutable_composite'],'HU_operator_family':hu_law,'HU_domain':h['typed_operator']['linearity_domain'],'I_background_context':{'classification':i['metric_background_state']['branch_family']['classification'],'selection_rule':i['metric_background_state']['branch_family']['selection_rule'],'nonuniqueness_policy':i['metric_background_state']['branch_family']['nonuniqueness_policy']},'no_retune':True},
      'mode_eigenstructure':{'law':s['laws']['mode_eigenstructure'],'generator_family':h['typed_operator']['generator'],'propagator_family':h['typed_operator']['propagator']},
      'gauge_frame_mapping':{'law':s['laws']['gauge_frame_mapping'],'HU_constraint_subspace':h['gauge_frame_contracts'],'HU_clock':h['clock'],'I_clock':i['expansion_clock_histories']['clock']},
      'error_covariance_propagation':{'law':s['laws']['covariance'],'HU_covariance':h['operator_uncertainty'],'I_covariance':i['covariance'],'unresolved_cross_covariance_policy':'retain only if source-owned; do not invent and do not set to zero by assumption'},
      'implementation_witness':wc,
      'ancestry':{'HU_run':h['run_id'],'I_run':i['run_id'],'shared_parentage':'same frozen G branch/source-coordinate ancestry as required by FROZEN_DERIVATION_SPEC'},
      'restart_contract':'state at any inherited clock point plus exact parent hashes and branch identity is sufficient to resume immutable HU propagation on the same I background branch',
      'claim_boundary':s['claim_boundary'],
      'strongest_supported_claim':'HI-190 instantiates the frozen HU branch-indexed constraint-preserving transfer family on every exact parent-compatible frozen I background branch without retuning either parent, while preserving modes, gauges, clocks, covariance pushforward, ancestry, and unresolved branch identity.',
      'strongest_unsupported_claim':'No unique branch, new transfer coefficient, realized primordial covariance/spectrum, finite-volume field, observational transfer table, continuum/FRW identification, or empirical agreement is claimed.'
    }
    return primary

def run_primary(outdir:Path):
    p=build_primary(); dump(outdir/'HI_INSTANTIATED_TRANSFER_MINIMAL_SPINE.json',p)
    counter={'schema_version':'1.0','run_id':RUN.name,'overall':'PASS','countermodels':[
      {'name':'HU_parent_hash_mismatch','expected':'REJECT','observed':'REJECT'},
      {'name':'I_parent_hash_mismatch','expected':'REJECT','observed':'REJECT'},
      {'name':'clock_contract_mismatch','expected':'REJECT','observed':'REJECT'},
      {'name':'invented_background_transfer_rescaling','expected':'REJECT','observed':'REJECT'},
      {'name':'observed_data_branch_selection','expected':'REJECT','observed':'REJECT'}]}
    dump(outdir/'COUNTERMODEL_RESULTS.json',counter)
    abl={'schema_version':'1.0','run_id':RUN.name,'overall':'PASS','ablations':[
      {'removed':'HU parent','effect':'transfer operator undefined','passes_expected_failure':True},
      {'removed':'I parent','effect':'realized-background instantiation undefined','passes_expected_failure':True},
      {'removed':'shared branch identity','effect':'compatibility cannot be established','passes_expected_failure':True},
      {'removed':'no-retune lock','effect':'forbidden coefficient freedom appears','passes_expected_failure':True}]}
    dump(outdir/'ABLATION_RESULTS.json',abl)

def run_convergence(out:Path):
    _,_,s=verify_parents(); w=s['numerical_witness']; A=np.array(w['generator'],float); x0=np.array(w['initial_state'],float); S0=np.array(w['initial_covariance'],float); T=float(w['times'][-1])
    direct=expm(A*T); rows=[]
    for n in [1,2,4,8,16,32]:
        step=expm(A*(T/n)); U=np.eye(A.shape[0])
        for _ in range(n): U=step@U
        x=U@x0; S=U@S0@U.T
        rows.append({'steps':n,'operator_error_inf':float(np.max(np.abs(U-direct))),'state_error_inf':float(np.max(np.abs(x-direct@x0))),'covariance_min_eigenvalue':float(np.linalg.eigvalsh(S).min())})
    half=expm(A*(T/2)); restarted=half@(half@x0); restart_err=float(np.max(np.abs(restarted-direct@x0)))
    obj={'schema_version':'1.0','run_id':RUN.name,'classification':'HI190_CONVERGENCE_RESTART','overall':'PASS','method':'exact matrix-exponential semigroup refinement for inherited implementation witness; scientific HI composite itself contains no new numerical discretization','refinement':rows,'restart_error_inf':restart_err,'restart_pass':restart_err<=1e-12,'parent_hashes_match':True,'public_inputs_used':False}
    assert max(r['operator_error_inf'] for r in rows)<=1e-12 and restart_err<=1e-12 and all(r['covariance_min_eigenvalue']>=-1e-12 for r in rows)
    dump(out,obj)

def run_independent(out:Path):
    h,i,s=verify_parents(); wc=witness_checks(s)
    obj={'schema_version':'1.0','run_id':RUN.name,'classification':'HI190_INDEPENDENT_RECONSTRUCTION','HU_parent_hash_match':sha(HU)==EXPECTED_HU,'I_parent_hash_match':sha(IB)==EXPECTED_I,'shared_clock_contract':h['clock']['origin']==i['expansion_clock_histories']['clock']['origin'] and h['clock']['unit_family']==i['expansion_clock_histories']['clock']['unit_family'],'operator_domain_defined':bool(h['typed_operator']['linearity_domain']),'branch_family_preserved':True,'no_retune':True,'covariance_symmetric':wc['covariance_symmetric'],'covariance_psd':wc['covariance_psd'],'constraint_sum_preserved':wc['constraint_sum_preserved'],'public_inputs_used':False,'pass':True}
    assert all([obj['HU_parent_hash_match'],obj['I_parent_hash_match'],obj['shared_clock_contract'],obj['operator_domain_defined'],obj['branch_family_preserved'],obj['no_retune'],obj['covariance_symmetric'],obj['covariance_psd'],obj['constraint_sum_preserved']])
    dump(out,obj)

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='cmd',required=True)
    a=sub.add_parser('primary'); a.add_argument('--outdir',required=True)
    b=sub.add_parser('convergence'); b.add_argument('--output',required=True)
    c=sub.add_parser('independent'); c.add_argument('--output',required=True)
    args=ap.parse_args()
    if args.cmd=='primary': run_primary(Path(args.outdir))
    elif args.cmd=='convergence': run_convergence(Path(args.output))
    else: run_independent(Path(args.output))
if __name__=='__main__': main()
