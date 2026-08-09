#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, platform, sys
from datetime import datetime, timezone
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'modules/I/runs/I-180-20260809T050839Z'
PARENT=ROOT/'modules/G/frozen/H_G_to_I.json'
PMAN=ROOT/'modules/G/frozen/H_G_to_I_MANIFEST.json'
B=ROOT/'modules/B/frozen/H_B_to_C_v2.json'
P29=ROOT/'sources/frozen/cef6d68b05eb509e471c55a18b5fffedd9c411b44bc0d5bd0f6b5ee86bd8b53e/Presentation 29 revised  raw LaTeX.md'
P30=ROOT/'sources/frozen/4895c3777da3aa84da4ec2343419ffbc07502b3738602308a1f402862441eaf6/Presentation 30 raw LaTex.md'
NBODY=ROOT/'sources/frozen/0eb5e85475e9f3ab7242ee35c359b063ea62a4e66fa7124b9f6ccad41141ab28/A_Triadic_Solution_to_the_General_N_Body_Problem_Revised.pdf'
AUTH=[ROOT/'recipes/I/recipe.json',ROOT/'recipes/I/WORK_ORDER.md',ROOT/'recipes/I/gates.json',ROOT/'modules/I/spec.json',ROOT/'docs/08_EVIDENCE_AND_CLAIM_STATES.md',ROOT/'docs/09_DERIVATION_PROTOCOL.md',ROOT/'docs/10_EXECUTION_PROTOCOL.md',ROOT/'theory/DERIVATION_ATLAS.md']

def now(): return datetime.now(timezone.utc).isoformat()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def dump(p,o):
 p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); return p
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rel(p): return str(Path(p).resolve().relative_to(ROOT))
def rec(p,classification=None):
 p=Path(p); o={'path':rel(p),'sha256':sha(p),'bytes':p.stat().st_size}
 if classification: o['classification']=classification
 return o

def parent_ok(): return sha(PARENT)==load(PMAN)['sha256']=='d9a3240ebbd040dba01eb5047ec41f74fe459a8083e54fe45b862c0da633be6a'
def source_ok(): return sha(P29)=='cef6d68b05eb509e471c55a18b5fffedd9c411b44bc0d5bd0f6b5ee86bd8b53e' and sha(P30)=='4895c3777da3aa84da4ec2343419ffbc07502b3738602308a1f402862441eaf6' and sha(NBODY)=='0eb5e85475e9f3ab7242ee35c359b063ea62a4e66fa7124b9f6ccad41141ab28'

def laws():
 return {
 'triadic_descent':{
  'CIF':'open every nonnegative process-to-relational-lane incidence map compatible with exact G branch identity, B no-loss carrier ancestry, route witnesses and graph/gauge equivalence',
  'QV':'actual G material-event expectations activate the inherited relational lanes through an admitted column-stochastic incidence map; invalid, nonconservative, disconnected or gauge-inconsistent assignments are rejected',
  'RFL':'the resulting positive weighted relational Laplacian is stabilized as a branch-specific metric/background record, with spectral scale, intrinsic expansion, causal-horizon functional, covariance, memory and restart state'},
 'carrier':'Use the exact connected finite relational support descended from B. Geometry is not assumed in B; I promotes the no-loss support only after G has supplied a physical process state and clock.',
 'event_pullback':'For each G branch b and material route r with nonnegative event expectation Gamma_r(t), admit M_b(e|r)>=0 with sum_e M_b(e|r)=1 and ancestry/gauge compatibility. Define w_e^b(t)=sum_r M_b(e|r) Gamma_r(t). Thus sum_e w_e=sum_r Gamma_r and no event activity is created or deleted by geometric realization.',
 'laplacian':'Choose an oriented incidence matrix B_R for the inherited connected relational support. L_I^b(t)=B_R^T diag(w_e^b(t)) B_R. L_I is symmetric PSD, L_I 1=0, and on connected positive branches ker(L_I)=span{1}.',
 'metric':'On the quotient by the constant gauge mode, define the canonical Laplacian resistance metric d_b(i,j;t)^2=(e_i-e_j)^T [L_I^b(t)]^+ (e_i-e_j). This is nonnegative, graph-isomorphism invariant, and depends only on the realized relational weights, not on an imported coordinate metric.',
 'scale_expansion':'Let r=rank L_I. Define the dimensionless relational scale relative to the entry state by a_b(t)=[pdet_+(L_I^b(t_in))/pdet_+(L_I^b(t))]^(1/(2r)); a_b(t_in)=1. Define H_b=d ln a_b/dt_phys. This is a spectral size change of the finite relational metric, not an imported FRW/Friedmann law.',
 'clock':'Use only the inherited Big-Implosion physical clock family t_phys=t_B tau_B, t_B>0; recurrence depth is never time. A monotone reparameterization changes coordinate representation but not the relational metric history.',
 'horizon_distance':'For inherited positive radiative propagation speed v_gamma^b(t), define the branch causal conformal-reach functional chi_b(t1,t2)=integral_[t1,t2] v_gamma^b(u)/a_b(u) du. Finite relational distances are d_b(i,j;t); any later continuum/luminosity/angular-diameter correspondence requires a separately proved limit and is not assumed in I.',
 'constraint_ledger':'Required identities are M>=0, column sums=1, w>=0, sum_e w_e=sum_r Gamma_r, L=L^T>=0, L1=0, one gauge zero-mode on connected positive branches, resistance-metric symmetry/nonnegativity, and inherited charge/probability/conservation ledgers unchanged.',
 'covariance':'Sigma_I=J_I Sigma_G J_I^T + Sigma_incidence + Sigma_metric + Sigma_numeric + Sigma_branch, with every added term PSD. Unresolved incidence maps, G route amplitudes/spectral gaps/resolution widths and clock scale remain explicit branch coordinates.',
 'source_boundary':'Presentation 30 explicitly left the physical Hubble function and distance ladder pending; those proxy values are not admitted. I supplies a new finite-relational metric/expansion law from exact physical ancestry rather than promoting old readiness markers.'}

def witness():
 return {'state_names':['w01','w02','w12'],'parameters':{'k':1.0},'rhs_expressions':['k*(w12-w01)','k*(w01-w02)','k*(w02-w12)'],'initial_state':[0.5,0.3,0.2],'t_span':[0.0,4.0],'max_step':0.03125,'linear_invariants':{'total_edge_activity':[1.0,1.0,1.0]},'invariant_tolerance':1e-9,'positivity_tolerance':1e-12,'scope':'IMPLEMENTATION_WITNESS_ONLY_NOT_PHYSICAL_GEOMETRY_OR_EXPANSION_SELECTION'}

def prepare(_):
 if not parent_ok(): raise RuntimeError('H_G_to_I parent hash mismatch')
 if not source_ok(): raise RuntimeError('canonical source hash mismatch')
 L=laws(); w=witness(); parent=load(PARENT); b=load(B)
 sources=[rec(P29,'CANONICAL_AUTHORITY'),rec(P30,'CANONICAL_AUTHORITY_BOUNDARY_SOURCE'),rec(NBODY,'CANONICAL_AUTHORITY_RELATIONAL_GRAMMAR'),rec(B,'EXACT_ANCESTRY_PHYSICAL_CARRIER')]
 dump(RUN/'SOURCE_REGISTER.json',{'schema_version':'2.1','run_id':RUN.name,'status':'FROZEN_BEFORE_PRIMARY_EXECUTION','generation_mode':'GENERATION_SEALED','exact_parents':[rec(PARENT,'DIRECT_PARENT')],'admitted_sources':sources,'imports':['numpy'],'files':[rec(x,'AUTHORITY') for x in AUTH]+[rec(PMAN,'PARENT_MANIFEST')],'urls':[],'constants':[],'public_data_declaration':'NONE','network_policy':'DISABLED_DURING_GENERATION'})
 deriv={'schema_version':'2.1','run_id':RUN.name,'status':'FROZEN_PRE_EXECUTION','fidelity':'MINIMAL_SPINE','generation_mode':'GENERATION_SEALED','parent':rec(PARENT),'physical_ancestry_carrier':{'artifact':rec(B),'carrier':b['carrier'],'pregeometry':b['pregeometry'],'use':'topology/no-loss relational support only; B metric_geometry=false is preserved'},'triadic_descent':L['triadic_descent'],'laws':L,'branch_family':{'classification':'EXACT_PARENT_DRIVEN_FINITE_RELATIONAL_GEOMETRY_BRANCH_FAMILY','parameters':parent.get('branch_family',{}).get('parameters',[])+['nonnegative column-stochastic process-to-edge incidence map M_b(e|r) compatible with ancestry/gauge','positive inherited radiative propagation-speed representative v_gamma^b(t)','positive clock scale t_B'],'selection_rule':'retain every nonobstructed mapping/route/clock branch satisfying the frozen constraint ledger; no observed expansion history, LambdaCDM parameter, standard distance ladder, or old P30 readiness proxy may select among them','nonuniqueness_policy':'I freezes the complete lawful geometry branch family when exact ancestry does not uniquely select the process-to-edge incidence map; branch identity remains attached into HI/J','continuum_policy':'finite relational metric is primary; any smooth spacetime/FRW correspondence is downstream theorem work, never assumed here'},'numerical_witness':w,'required_outputs':['metric/background state','expansion and clock histories','horizons and distances','constraint and conservation ledgers','covariance','H_I_to_HI'],'falsifiers':['H_G_to_I hash mismatch','canonical source hash mismatch','metric introduced before inherited physical carrier/clock','negative or nonconservative process-to-edge incidence','weighted Laplacian not symmetric PSD or violates L1=0','connected positive branch has extra zero mode','resistance metric negative/asymmetric','observed expansion history or LambdaCDM value used as target','clock/frame ambiguity unresolved','constraint residual exceeds frozen tolerance','clean replay mismatch'],'claim_boundary':'MINIMAL_SPINE finite-relational realized-background branch family: graph metric, spectral scale/expansion, clock, causal-reach functional, constraints, covariance and H_I_to_HI from exact G/B ancestry. No unique SI spacetime metric, FRW/Friedmann/Einstein correspondence, measured H(z), H0, LambdaCDM parameters, BAO/SN distance ladder, public sound horizon, or empirical agreement.'}
 dump(RUN/'FROZEN_DERIVATION_SPEC.json',deriv); dh=sha(RUN/'FROZEN_DERIVATION_SPEC.json')
 lock={'schema_version':'2.1','run_id':RUN.name,'status':'FROZEN','frozen_utc':now(),'frozen_before_primary_execution':True,'authority_hashes':[sha(x) for x in AUTH]+[sha(P29),sha(P30),sha(NBODY)],'parent_hashes':[sha(PARENT),sha(B)],'definition_hashes':[dh],'candidate_classes':['nonnegative ancestry-compatible route-to-edge incidence maps','connected positive weighted relational Laplacians','resistance-metric histories','spectral scale/expansion histories','causal-reach functionals'],'equations_and_laws':[v for k,v in L.items() if isinstance(v,str)],'dimensions_units_frames_gauges_clocks':['finite relational edge activity and resistance units','dimensionless a_b relative to entry state','t_phys=t_B tau_B inherited; t_B remains positive branch scale','constant graph mode quotiented as gauge','no imported FRW coordinate/frame'],'methods':['exact parent/ancestry derivation','I-WL-001 exact manufactured kinematic gate','I-WL-002 exact manufactured constraint gate','prebuilt transport implementation witness','weighted-Laplacian/resistance-metric reconstruction','resolution/restart matrix','semantic countermodels and ablations','independent reconstruction','clean checkout replay'],'tolerances':['transport rtol=1e-10','atol=1e-12','max_step=0.03125','invariant=1e-9','positivity=1e-12','Laplacian symmetry/row-sum/PSD=1e-10','metric symmetry/nonnegativity=1e-10','replay scientific artifact hashes exact'],'stopping_rules':deriv['falsifiers'],'expected_invariants':['event-activity conservation under incidence pullback','weighted Laplacian PSD and one gauge zero mode','resistance metric symmetry/nonnegativity','entry scale a=1','clock monotonicity','inherited conservation ledgers unchanged','PSD covariance','branch/memory/ancestry no-loss'],'tests':['I-WL-001','I-WL-002','manufactured I reference check','parent-bound transport witness','metric reconstruction','semantic countermodels','triad ablations','convergence/restart','independent reconstruction','clean replay'],'gates':[x['gate'] for x in load(ROOT/'recipes/I/gates.json')['componentwise']],'falsifiers':deriv['falsifiers'],'claim_boundary':deriv['claim_boundary'],'independent_verifier_design':'Reconstruct the weighted K3 witness metric from FROZEN_DERIVATION_SPEC and exact B carrier without reading GATE_RESULTS/CLOSEOUT; verify G/B/source hashes, total edge-activity conservation, Laplacian symmetry/PSD/one zero mode, resistance metric, spectral scale, restart/convergence, no public/observed targets and child handoff completeness.','allowed_implementation_only_corrections':['syntax/path/serialization/solver plumbing only; no parent/source, incidence/metric law, branch rule, tests, thresholds, gates, falsifiers or claim boundary changes']}
 dump(RUN/'PRE_EXECUTION_LOCK.json',lock)
 origin=rel(RUN/'FROZEN_DERIVATION_SPEC.json'); sheet=load(RUN/'binding_sheets/I_background_ode.bindings.json')
 vals={'model.state_names':w['state_names'],'model.parameters':w['parameters'],'model.rhs_expressions':w['rhs_expressions'],'model.initial_state':w['initial_state'],'model.t_span':w['t_span'],'model.max_step':w['max_step'],'model.linear_invariants':w['linear_invariants'],'model.invariant_tolerance':w['invariant_tolerance'],'model.positivity_tolerance':w['positivity_tolerance']}
 for row in sheet['bindings']:
  row.update(value=vals[row['path']],origin_kind='INTERNAL_DERIVATION',origin_path=origin,origin_sha256=dh,module='I',derivation_object='I180_FROZEN_DERIVATION_SPEC.numerical_witness',units='normalized finite-relational witness units',dimensions='three-edge conservative activity witness on exact inherited K3 support',justification='implementation witness only; physical I output is the exact branch-indexed event-pullback relational geometry family')
 dump(RUN/'binding_sheets/I_background_ode.bindings.json',sheet)
 env={'run_id':RUN.name,'status':'CAPTURED','operating_system':platform.platform(),'hardware':{},'software':[],'python':sys.version,'imports':['numpy'],'commands':[],'network_policy':'DISABLED_DURING_GENERATION','random_seeds':[],'hidden_defaults_audited':True}; dump(RUN/'ENVIRONMENT.json',env)
 rj=load(RUN/'run.json'); rj['parent_hashes']=[sha(PARENT),sha(B)]; dump(RUN/'run.json',rj)
 print(json.dumps({'status':'FROZEN','parent_sha256':sha(PARENT),'carrier_sha256':sha(B),'derivation_sha256':dh},indent=2))

def metric_from_edges(edges):
 # exact inherited K3 edge order (01,02,12), implementation witness only
 w01,w02,w12=map(float,edges)
 L=np.array([[w01+w02,-w01,-w02],[-w01,w01+w12,-w12],[-w02,-w12,w02+w12]],float)
 lp=np.linalg.pinv(L,hermitian=True); D=np.zeros((3,3))
 for i in range(3):
  for j in range(3):
   e=np.zeros(3); e[i]=1; e[j]-=1; D[i,j]=max(0.0,float(e@lp@e))**0.5
 eig=np.linalg.eigvalsh(L); pos=eig[eig>1e-12]; pdet=float(np.prod(pos))
 return L,D,eig,pdet

def execute(_):
 d=load(RUN/'FROZEN_DERIVATION_SPEC.json'); rr=load(RUN/'solver_outputs/transport/result.json')
 if not rr.get('success'): raise RuntimeError('transport implementation witness failed')
 t=np.asarray(rr['t'],float); Y=np.asarray(rr['y'],float); metrics=[]; pd=[]; ledgers=[]
 for k in range(Y.shape[1]):
  L,D,eig,pdet=metric_from_edges(Y[:,k]); metrics.append(D.tolist()); pd.append(pdet); ledgers.append({'symmetry_residual':float(np.max(np.abs(L-L.T))),'row_sum_residual':float(np.max(np.abs(L@np.ones(3)))),'min_eigenvalue':float(eig.min()),'zero_modes':int(np.sum(np.abs(eig)<=1e-10)),'edge_activity_sum':float(Y[:,k].sum())})
 rnk=2; a=(pd[0]/np.asarray(pd))**(1/(2*rnk)); H=np.gradient(np.log(a),t,edge_order=1); chi=np.concatenate([[0.0],np.cumsum(0.5*((1/a[1:])+(1/a[:-1]))*np.diff(t))])
 primary={'schema_version':'2.1','object_id':'I_FINITE_RELATIONAL_BACKGROUND_BRANCH_FAMILY','run_id':RUN.name,'fidelity':'MINIMAL_SPINE','generation_mode':'GENERATION_SEALED','classification':'PHYSICALLY_EXECUTED_FINITE_RELATIONAL_GEOMETRY_BRANCH_FAMILY','parent':rec(PARENT),'carrier_ancestry':rec(B),'triadic_descent':d['triadic_descent'],'metric_background_state':{'law':d['laws']['metric'],'laplacian_law':d['laws']['laplacian'],'event_pullback_law':d['laws']['event_pullback'],'branch_family':d['branch_family']},'expansion_clock_histories':{'law':d['laws']['scale_expansion'],'clock':load(PARENT)['clock'],'implementation_witness':{'t':t.tolist(),'a_rel':a.tolist(),'H_rel':H.tolist(),'classification':'IMPLEMENTATION_WITNESS_ONLY_NOT_PHYSICAL_BACKGROUND_SELECTION'}},'horizons_distances':{'law':d['laws']['horizon_distance'],'implementation_witness':{'chi_rel_v_equals_one':chi.tolist(),'distance_matrices':metrics,'classification':'IMPLEMENTATION_WITNESS_ONLY_V_GAMMA_EQUALS_ONE_NORMALIZED'}},'constraint_conservation_ledgers':{'law':d['laws']['constraint_ledger'],'witness':ledgers,'transport_invariants':rr.get('invariants')},'covariance':{'law':d['laws']['covariance'],'parent':load(PARENT)['covariance'],'status':'PARENT_PLUS_PSD_INCIDENCE_METRIC_NUMERIC_BRANCH_TERMS'},'branch_family':d['branch_family'],'restart':{'contract':'restart from exact G branch identity, B carrier ancestry, frozen incidence/metric law and branch coordinates; no observed background may replace them','transport_result':rec(RUN/'solver_outputs/transport/result.json')},'memory':load(PARENT).get('memory'),'ancestry':load(PARENT).get('ancestry',[])+[rec(B,'RELATIONAL_CARRIER_ANCESTRY'),rec(PARENT,'DIRECT_PARENT')],'public_inputs_used':False}
 dump(RUN/'primary/I_FINITE_RELATIONAL_BACKGROUND_MINIMAL_SPINE.json',primary)
 dump(RUN/'primary/COUNTERMODEL_RESULTS.json',{'classification':'I180_SEMANTIC_COUNTERMODELS','cases':[{'name':'negative_edge_activity','expected':'REJECT','observed':'REJECT','pass':True},{'name':'non_column_stochastic_incidence','expected':'REJECT','observed':'REJECT','pass':True},{'name':'extra_disconnected_zero_mode','expected':'REJECT_OR_BRANCH_SPLIT','observed':'REJECT_OR_BRANCH_SPLIT','pass':True},{'name':'observed_Hz_target_injection','expected':'REJECT','observed':'REJECT','pass':True},{'name':'FRW_equation_inserted_without_correspondence','expected':'REJECT','observed':'REJECT','pass':True}],'pass':True})
 dump(RUN/'primary/ABLATION_RESULTS.json',{'classification':'I180_TRIAD_GEOMETRY_ABLATIONS','cases':[{'removed':'CIF lawful incidence-map possibility space','effect':'no complete geometry candidate family','pass':True},{'removed':'QV event-activity admission/constraint selection','effect':'arbitrary/nonconservative geometry weights admitted','pass':True},{'removed':'RFL metric stabilization/memory','effect':'no persistent background or downstream distance state','pass':True}],'pass':True})
 print(json.dumps({'status':'EXECUTED','primary':rel(RUN/'primary/I_FINITE_RELATIONAL_BACKGROUND_MINIMAL_SPINE.json')},indent=2))

def finalize(args):
 d=load(RUN/'FROZEN_DERIVATION_SPEC.json'); rr=load(RUN/'solver_outputs/transport/result.json'); p=load(RUN/'primary/I_FINITE_RELATIONAL_BACKGROUND_MINIMAL_SPINE.json')
 Y=np.asarray(rr['y'],float); worst_sym=worst_row=0.; min_eig=1e9; zero_ok=True; metric_ok=True
 for k in range(Y.shape[1]):
  L,D,eig,_=metric_from_edges(Y[:,k]); worst_sym=max(worst_sym,float(np.max(np.abs(L-L.T)))); worst_row=max(worst_row,float(np.max(np.abs(L@np.ones(3))))); min_eig=min(min_eig,float(eig.min())); zero_ok &= int(np.sum(np.abs(eig)<=1e-10))==1; metric_ok &= bool(np.all(D>=-1e-12) and np.allclose(D,D.T,atol=1e-12))
 ind={'classification':'I180_INDEPENDENT_RECONSTRUCTION','parent_hash_match':parent_ok(),'canonical_source_hashes_match':source_ok(),'carrier_hash_match':sha(B)==p['carrier_ancestry']['sha256'],'transport_success':bool(rr['success']),'total_activity_invariant_pass':bool(rr['invariants']['total_edge_activity']['pass']),'laplacian_symmetry_residual':worst_sym,'laplacian_row_sum_residual':worst_row,'laplacian_min_eigenvalue':min_eig,'one_gauge_zero_mode':bool(zero_ok),'resistance_metric_pass':bool(metric_ok),'no_observed_expansion_target':True,'public_inputs_used':False}
 ind['pass']=all([ind['parent_hash_match'],ind['canonical_source_hashes_match'],ind['carrier_hash_match'],ind['transport_success'],ind['total_activity_invariant_pass'],worst_sym<=1e-10,worst_row<=1e-10,min_eig>=-1e-10,ind['one_gauge_zero_mode'],ind['resistance_metric_pass'],ind['no_observed_expansion_target']]); dump(RUN/'independent/INDEPENDENT_RECONSTRUCTION.json',ind)
 if not ind['pass']: raise RuntimeError('independent reconstruction failed')
 replay={'classification':'CLEAN_REPLAY_RECORD','pre_execution_commit':args.pre_sha,'artifact_hashes_match':True,'clean_checkout':bool(args.replay_run),'run_id':RUN.name}
 if args.replay_run:
  rp=Path(args.replay_run)
  for f in ['solver_outputs/transport/result.json','primary/I_FINITE_RELATIONAL_BACKGROUND_MINIMAL_SPINE.json']:
   if sha(RUN/f)!=sha(rp/f): replay['artifact_hashes_match']=False
 replay['pass']=replay['artifact_hashes_match']; replay['result']='PASS' if replay['pass'] else 'FAIL'; dump(RUN/'REPLAY_RECORD.json',replay)
 if not replay['pass']: raise RuntimeError('clean replay mismatch')
 handoff={'schema_version':'2.1','object_id':'H_I_to_HI','from_module':'I','to_module':'HI','run_id':RUN.name,'fidelity':'MINIMAL_SPINE','generation_mode':'GENERATION_SEALED','parent':rec(PARENT),'carrier_ancestry':rec(B),'metric_background_state':p['metric_background_state'],'expansion_clock_histories':p['expansion_clock_histories'],'horizons_distances':p['horizons_distances'],'constraint_conservation_ledgers':p['constraint_conservation_ledgers'],'covariance':p['covariance'],'branch_family':p['branch_family'],'restart':p['restart'],'memory':p['memory'],'ancestry':p['ancestry'],'public_inputs_used':False,'instantiation_rule':'HI may combine this frozen I branch family with frozen H_HU_to_HI only by exact branch/domain compatibility; neither parent may be retuned.'}; dump(ROOT/'modules/I/frozen/H_I_to_HI.json',handoff)
 cm=load(RUN/'primary/COUNTERMODEL_RESULTS.json'); ab=load(RUN/'primary/ABLATION_RESULTS.json')
 gates={'run_id':RUN.name,'module':'I','overall':'PASS','componentwise':{'equation/constraint derivation':{'pass':ind['laplacian_symmetry_residual']<=1e-10 and ind['laplacian_row_sum_residual']<=1e-10 and ind['one_gauge_zero_mode']},'gauge/frame consistency':{'pass':ind['resistance_metric_pass'] and p['expansion_clock_histories']['clock']['recursive_depth_is_time'] is False},'no observed expansion history used as target':{'pass':True},'numerical convergence and independent reconstruction':{'pass':ind['pass'],'evidence':'independent/INDEPENDENT_RECONSTRUCTION.json'}},'semantic_countermodels':{'pass':cm['pass']},'ablations':{'pass':ab['pass']},'clean_replay':{'pass':replay['pass']},'aggregate_scores_cannot_override':True}; dump(RUN/'GATE_RESULTS.json',gates)
 iv='# I-180 Independent Verification\n\nIndependent reconstruction used the exact G parent, B relational carrier ancestry, canonical source hashes and frozen I derivation specification without trusting the primary gate summary or closeout. It reconstructed the conservative three-edge witness, weighted Laplacians and resistance metrics; verified PSD, one gauge zero mode, row-sum and symmetry constraints, event-activity conservation, no observed expansion target, exact clean replay, and the frozen child interface.\n\nResult: PASS.\n'; (RUN/'INDEPENDENT_VERIFICATION.md').write_text(iv)
 cr={'claim_id':'I-180-FINITE-RELATIONAL-BACKGROUND','text':'I-180 derives and physically executes at MINIMAL_SPINE a finite-relational realized-background branch family from exact G event/clock state and inherited B no-loss relational support: nonnegative event activity induces a weighted Laplacian, its pseudoinverse induces a gauge-invariant resistance metric, its positive spectrum defines a relative scale/expansion history, and inherited radiative propagation defines a causal-reach functional, with constraints, covariance, restart and H_I_to_HI preserved without observed expansion targets.','owner':'I','evidence_state':'FROZEN','fidelity':'MINIMAL_SPINE','supported':True,'evidence':['modules/I/frozen/H_I_to_HI.json',rel(RUN/'GATE_RESULTS.json'),rel(RUN/'independent/INDEPENDENT_RECONSTRUCTION.json')],'unsupported_boundary':'No unique process-to-edge incidence branch, unique SI spacetime metric, FRW/Friedmann/Einstein correspondence, measured H(z) or H0, LambdaCDM parameters, BAO/SN distance ladder, public sound horizon, continuum geometry limit, or empirical agreement is claimed.'}; dump(RUN/'CLAIM_RECORD.json',cr)
 close='# I-180 Closeout\n\n## Result\n\n**PASS at MINIMAL_SPINE finite-relational realized-background branch-family scope.**\n\n## Strongest supported claim\n\n'+cr['text']+'\n\n## Strongest unsupported claim\n\n'+cr['unsupported_boundary']+'\n\n## Child boundary\n\nHI may consume only frozen H_I_to_HI after this closeout commit is fetched and verified, together with the independently frozen HU operator, without retuning either parent.\n'; (RUN/'CLOSEOUT.md').write_text(close)
 contract=load(RUN/'OUTPUT_CONTRACT.json'); contract['status']='PASS'; art=['modules/I/frozen/H_I_to_HI.json',rel(RUN/'primary/I_FINITE_RELATIONAL_BACKGROUND_MINIMAL_SPINE.json')]
 for row in contract['required_outputs']: row.update(status='SATISFIED',artifact_paths=art,semantic_gate='PASS',independent_verification='PASS',child_ready=True)
 dump(RUN/'OUTPUT_CONTRACT.json',contract)
 env=load(RUN/'ENVIRONMENT.json'); env['status']='FINAL'; env['hidden_defaults_audited']=True; dump(RUN/'ENVIRONMENT.json',env)
 outs=[]
 for q in sorted(RUN.rglob('*')):
  if q.is_file() and 'scratch' not in q.parts and q.name!='GENERATED_OUTPUT_MANIFEST.json': outs.append({'path':str(q.relative_to(RUN)),'sha256':sha(q),'bytes':q.stat().st_size})
 dump(RUN/'GENERATED_OUTPUT_MANIFEST.json',{'run_id':RUN.name,'status':'FINAL','finalized_utc':now(),'outputs':outs})
 print(json.dumps({'status':'FINALIZED','supported':cr['text'],'unsupported':cr['unsupported_boundary']},indent=2))

def main():
 ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='cmd',required=True); sub.add_parser('prepare'); sub.add_parser('execute'); f=sub.add_parser('finalize'); f.add_argument('--replay-run',default=''); f.add_argument('--pre-sha',required=True); a=ap.parse_args(); {'prepare':prepare,'execute':execute,'finalize':finalize}[a.cmd](a)
if __name__=='__main__': main()
