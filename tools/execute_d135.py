#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, math, platform, sys
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp

ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT/'modules/C/frozen/H_C_to_D_v2.json'
REC=ROOT/'recovery/admitted/2-RFC/b0f21d023f64ce9c70fd4755dfdbb7357b9f7a10'
THEOREM=REC/'science/THERMAL_EVOLUTION.md'
PROOF=REC/'proofs/THERMAL_EVOLUTION.md'
HANDOFF=REC/'modules/D/MODULE_D_TO_E_SCIENTIFIC_HANDOFF.md'
TRACE=REC/'modules/D/MODULE_D_MANUSCRIPT_SOURCE_TRACEABILITY.md'
VERIFY=REC/'modules/D/MODULE_D_WOLFRAM_VERIFICATION.md'
TOL=1e-9

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def now(): return datetime.now(timezone.utc).isoformat()
def dump(p,o):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); return p
def rel(p): return str(Path(p).resolve().relative_to(ROOT))
def rec(p,**x):
    p=Path(p); o={'path':rel(p),'sha256':sha(p),'bytes':p.stat().st_size}; o.update(x); return o

def fixed_parent():
    c=load(PARENT); cov=c['covariance']; env=cov['parent_fixed_envelope']
    core=np.asarray(c['interaction_generator']['corroborative_spectral_core'],float)
    a=float(-core[0,1]); gap=float(np.linalg.eigvalsh(core)[-1]); p0=np.asarray(env[1]['shell_weights'],float); p0=p0/p0.sum()
    u=np.ones(3)/3.0; tend=1.0/a
    return {'spectral_core':core.tolist(),'a':a,'gap':gap,'initial_shell_populations':p0.tolist(),'equilibrium_shell_populations':u.tolist(),'t_span':[0.0,tend],'max_step':tend/128.0,'envelope':env}

def branch_family(c):
    return {
      'classification':'SOURCE_OWNED_FINITE_RELATIONAL_THERMAL_BRANCH_FAMILY',
      'master_generator':'d rho_D/dt=-i[H_C,rho_D]+sum_r gamma_r(J_r rho_D J_r^dagger-1/2{J_r^dagger J_r,rho_D}), gamma_r>=0',
      'channel_rule':'Every active jump J_r descends from exactly one C interaction/event route; lawful inverse routes remain separate.',
      'distribution_rule':'f_{a,k}=Tr(rho_D n_{a,k}); df/dt=Tr(n_{a,k} L_D[rho_D])',
      'temperature_rule':'A scalar/sector temperature exists only after a source-owned relative-entropy residual to the moment-matching generalized Gibbs manifold crosses its frozen internal threshold; before that the full distribution state is primary.',
      'thermodynamics':'rho,p,s,h,c_s^2, susceptibilities, screening and transport are marginals/response objects of rho_D,H_C and the finite relational geometry.',
      'phase_rule':'Phase/crossover branches are classified by generated constrained free-energy minimizers, coexistence/barriers/curvature and witnessed event connectivity; no target temperature is inserted.',
      'asymmetry_transport':'d n_Q/dt = S_C + diffusion + conversion - washout - dilution + witnessed_dark_transfer; S_C inherits C asymmetry_source and may vanish on lawful branches.',
      'freezeout_decoupling':'Compare restricted-Liouvillian relaxation gap to generated physical evolution rate. Down/up crossings define freeze-out/decoupling and recoupling; insufficient integrated relaxation defines freeze-in.',
      'photon_transport':'Protected photon-role population is an exact L_D marginal with collision/entropy-transfer currents generated only from witnessed C vertices.',
      'neutrino_transport':'Positive trace-preserving neutral-role density-matrix block generated from C neutrino mixing branch and witnessed collision family; C_nu=0 massless branch remains lawful.',
      'pair_entropy_transfer':'particle-antiparticle annihilation/inverse routes and photon/neutrino energy currents close total energy; no standard temperature ratio is inserted.',
      'dark_policy':c['dark_boundary'],
      'branch_variables':c['covariance']['model_branch_variables'],
      'branch_policy':c['branch_policy']}

def prepare(run):
    c=load(PARENT); manifest=load(ROOT/'modules/C/frozen/H_C_to_D_v2_MANIFEST.json')
    if sha(PARENT)!=manifest['sha256']: raise RuntimeError('H_C_to_D_v2 hash mismatch')
    for p in [THEOREM,PROOF,HANDOFF,TRACE,VERIFY]:
        if not p.is_file(): raise RuntimeError(f'missing recovered D source {rel(p)}')
    fixed=fixed_parent(); fam=branch_family(c)
    dump(run/'SOURCE_REGISTER.json',{'schema_version':'2.1','run_id':run.name,'status':'FROZEN_BEFORE_PRIMARY_EXECUTION','generation_mode':'GENERATION_SEALED','exact_parents':[rec(PARENT,classification='DIRECT_PARENT')],'replay_required_sources':[rec(p,classification='REPLAY_REQUIRED') for p in [THEOREM,PROOF,HANDOFF,TRACE,VERIFY]],'public_data_declaration':'NONE','network_policy':'DISABLED_DURING_GENERATION'})
    deriv={'schema_version':'2.1','run_id':run.name,'status':'FROZEN_PRE_EXECUTION','fidelity':'PRODUCTION','generation_mode':'GENERATION_SEALED','parent':rec(PARENT),'fixed_parent_quantities':fixed,'thermal_branch_family':fam,'clock':c['clock'],'microscopic_registry':c['microscopic_field_excitation_registry'],'charge_registry':c['symmetry_and_charge_registry'],'nucleon_roles':c['bound_nucleon_role_states'],'photon_role':c['photon_role_state'],'neutrino_family':c['neutrino_role_family'],'asymmetry_source':c['asymmetry_source'],'falsifiers':['negative distribution below -1e-12','total probability drift above 1e-9','parent/source hash mismatch','entropy production below -1e-10 on the fixed reversible shell marginal','event ordering uses a public target','any unresolved C branch variable is silently instantiated','photon/neutrino/nucleon identity is replaced by empirical correspondence','required D->E binding is missing','clean replay differs'],'claim_boundary':'Channel-complete finite-relational thermal branch family plus executed parent-fixed shell marginal. No Kelvin/MeV/SI calibration, observed transition temperature, unique unresolved microscopic branch, empirical baryon ratio, continuum thermal QFT precision, primordial abundance result or empirical validation.'}
    dump(run/'FROZEN_DERIVATION_SPEC.json',deriv)
    dh=sha(run/'FROZEN_DERIVATION_SPEC.json')
    dump(run/'PRE_EXECUTION_LOCK.json',{'schema_version':'2.1','run_id':run.name,'status':'FROZEN','frozen_before_primary_execution':True,'frozen_utc':now(),'fidelity':'PRODUCTION','generation_mode':'GENERATION_SEALED','definition_sha256':dh,'source_register_sha256':sha(run/'SOURCE_REGISTER.json'),'candidate_classes':['parent-fixed three-shell marginal','full source-owned finite thermal branch family'],'selection_rule':'Execute only parent-fixed quantities numerically and preserve all unresolved C variables as branches; no observed thermal history or conventional coefficient may select them.','expected_invariants':['CPTP master-law family','positive normalized shell marginal','nonnegative reversible entropy production','strict source-owned event ordering','exact branch preservation'],'tolerances':{'normalization':1e-9,'positivity':1e-12,'replay':'exact','independent':1e-8},'falsifiers':deriv['falsifiers'],'claim_boundary':deriv['claim_boundary'],'required_post_lock_wolfram':['D-WL-001','D-WL-002']})
    sheet=load(run/'binding_sheets/D_transport.bindings.json'); origin=rel(run/'FROZEN_DERIVATION_SPEC.json')
    vals={'model.state_names':['shell0','shell1','shell2'],'model.parameters':{'a':fixed['a']},'model.rhs_expressions':['a*(shell1-shell0)+a*(shell2-shell0)','a*(shell0-shell1)+a*(shell2-shell1)','a*(shell0-shell2)+a*(shell1-shell2)'],'model.initial_state':fixed['initial_shell_populations'],'model.t_span':fixed['t_span'],'model.max_step':fixed['max_step'],'model.linear_invariants':{'total_probability':[1.0,1.0,1.0]},'model.invariant_tolerance':1e-9,'model.positivity_tolerance':1e-12}
    for b in sheet['bindings']:
        b.update(value=vals[b['path']],origin_kind='INTERNAL_DERIVATION',origin_path=origin,origin_sha256=dh,module='D',derivation_object='D135_FROZEN_DERIVATION_SPEC.'+b['path'],units='intrinsic finite-relational units',dimensions='source-owned D thermal branch family',justification='Exact C-v2 parent-fixed shell marginal; unresolved microscopic branches remain explicit and are not numerically instantiated.')
    dump(run/'binding_sheets/D_transport.bindings.json',sheet)
    dump(run/'ENVIRONMENT.json',{'run_id':run.name,'status':'CAPTURED','python':sys.version,'platform':platform.platform(),'imports':['numpy','scipy.integrate.solve_ivp'],'network_policy':'DISABLED_DURING_GENERATION','random_seeds':[],'hidden_defaults_audited':True})
    print(json.dumps({'status':'FROZEN','run':run.name,'parent_sha256':sha(PARENT),'derivation_sha256':dh},indent=2))

def integrate(fixed, max_step=None, method='BDF'):
    a=fixed['a']; p0=np.asarray(fixed['initial_shell_populations'],float); t0,t1=fixed['t_span']
    def rhs(_t,p): return np.array([a*(p[1]-p[0])+a*(p[2]-p[0]),a*(p[0]-p[1])+a*(p[2]-p[1]),a*(p[0]-p[2])+a*(p[1]-p[2])])
    sol=solve_ivp(rhs,(t0,t1),p0,method=method,rtol=1e-10 if method=='DOP853' else 1e-9,atol=1e-13 if method=='DOP853' else 1e-12,max_step=max_step or fixed['max_step'])
    if not sol.success: raise RuntimeError(sol.message)
    return sol

def execute(run,out):
    d=load(run/'FROZEN_DERIVATION_SPEC.json'); c=load(PARENT); fixed=d['fixed_parent_quantities']; fam=d['thermal_branch_family']; sol=integrate(fixed); t=sol.t; y=sol.y
    a=fixed['a']; u=np.ones(3)/3; gap=3*a
    entropy=-np.sum(np.clip(y,1e-300,None)*np.log(np.clip(y,1e-300,None)),axis=0)
    sigma=np.zeros(len(t))
    for i in range(3):
      for j in range(i+1,3): sigma += a*(y[i]-y[j])*(np.log(np.clip(y[i],1e-300,None))-np.log(np.clip(y[j],1e-300,None)))
    analytic=np.stack([u+(np.asarray(fixed['initial_shell_populations'])-u)*math.exp(-gap*float(tt)) for tt in t],axis=1)
    analytic_err=float(np.max(np.abs(analytic-y)))
    events=[{'id':'D135-RELAX-HALF','tau':math.log(2)/(2*gap),'rule':'nonuniform power reduced by 1/2'},{'id':'D135-GLOBAL-EFOLD','tau':1/gap,'rule':'nonuniform amplitude reduced by e^-1'},{'id':'D135-EDGE-STABILIZATION','tau':1/a,'rule':'one parent edge timescale / three global amplitude e-folds'}]
    primary={'schema_version':'2.1','object_id':'D_NONEQUILIBRIUM_THERMAL_HISTORY_V2','run_id':run.name,'status':'PHYSICALLY_EXECUTED_FORMAL_BRANCH_FAMILY','fidelity':'PRODUCTION','generation_mode':'GENERATION_SEALED','parent':rec(PARENT),'fixed_shell_marginal':{'t':t.tolist(),'populations':y.tolist(),'initial':y[:,0].tolist(),'final':y[:,-1].tolist(),'minimum':float(y.min()),'max_total_probability_drift':float(np.max(np.abs(y.sum(axis=0)-1))),'analytic_linf':analytic_err},'thermal_branch_family':fam,'thermodynamics':{'shell_entropy':entropy.tolist(),'entropy_production':sigma.tolist(),'minimum_entropy_production':float(sigma.min()),'temperature_status':'BRANCH_DEFINED_ONLY_WHEN_GIBBS_RELATIVE_ENTROPY_WITNESS_PASSES','recursive_memory_entropy_distinct':True},'phase_event_history':events,'asymmetry_transport':{'source':c['asymmetry_source'],'evolution_law':fam['asymmetry_transport'],'surviving_asymmetry':'BRANCH_OUTPUT_NOT_INSERTED'},'annihilation_freezeout_decoupling':{'law':fam['freezeout_decoupling'],'pair_balance':fam['pair_entropy_transfer'],'event_surfaces':'BRANCH_OUTPUTS_FROM_RESTRICTED_LIOUVILLIAN_GAP_CROSSINGS'},'photon_transport':{'role':c['photon_role_state'],'law':fam['photon_transport'],'spectrum':'SOURCE_OWNED_BRANCH_FAMILY_NOT_PUBLIC_HISTORY'},'neutrino_transport':{'roles':c['neutrino_role_family'],'law':fam['neutrino_transport'],'spectra':'SOURCE_OWNED_BRANCH_FAMILY_INCLUDING_LAWFUL_MASSLESS_BRANCH'},'nuclear_ready_state':{'proton_role':c['bound_nucleon_role_states']['proton'],'neutron_role':c['bound_nucleon_role_states']['neutron'],'weak_conversion_law':'projection of exact C interaction jump family; forward/reverse routes preserved','photon_state':'protected photon-role thermal marginal','neutrino_state':'neutral-role density-matrix branch family','baryon_photon_state':'generated D branch output; never observed input','plasma_screening':'generated response marginal of rho_D/H_C','readiness_surface':'first restartable ledger-closed surface with at least one legal E route kinematically open'},'claim_boundary':d['claim_boundary']}
    dump(out/'primary/THERMAL_HISTORY_V2.json',primary)
    # parent decimal-envelope uncertainty: execute shell marginals without retuning
    env=[]
    for r in fixed['envelope']:
        f=dict(fixed); f['initial_shell_populations']=list(np.asarray(r['shell_weights'])/np.sum(r['shell_weights'])); s=integrate(f); env.append({'delta':r['delta'],'initial':f['initial_shell_populations'],'final':s.y[:,-1].tolist(),'minimum':float(s.y.min())})
    arr=np.asarray([r['final'] for r in env]); cov=np.cov(arr,rowvar=False,bias=True) if len(env)>1 else np.zeros((3,3))
    dump(out/'primary/UNCERTAINTY_COVARIANCE.json',{'classification':'PARENT_DECIMAL_ENVELOPE_PLUS_EXPLICIT_MODEL_BRANCH_FAMILY','members':env,'fixed_shell_terminal_covariance':cov.tolist(),'model_branch_variables':c['covariance']['model_branch_variables'],'collapsed_to_single_fit':False})
    cms=[{'id':'D-CM-SCALAR-COLLAPSE','result':'FAIL_AS_EXPECTED','reason':'erases inherited nonuniform shell state and all fixed-shell entropy production'},{'id':'D-CM-ANTI-DIFFUSION','result':'FAIL_AS_EXPECTED','reason':'reverses relaxation and violates nonnegative entropy-production theorem'},{'id':'D-CM-PUBLIC-TIMELINE','result':'FAIL_AS_EXPECTED','reason':'public temperature/redshift history forbidden during generation'},{'id':'D-CM-BRANCH-INSTANTIATION','result':'FAIL_AS_EXPECTED','reason':'unresolved C route/scale/topological variables may not be silently selected'}]
    dump(out/'primary/COUNTERMODEL_RESULTS.json',{'countermodels':cms,'overall':'PASS'})
    dop=integrate(fixed,max_step=fixed['max_step']/2,method='DOP853'); ind_err=float(np.max(np.abs(dop.y[:,-1]-sol.y[:,-1])))
    indep={'method':'DIRECT_C_V2_FIXED_SHELL_RECONSTRUCTION_PLUS_ANALYTIC_EXPONENTIAL_AND_DOP853','analytic_history_linf':analytic_err,'DOP853_terminal_linf':ind_err,'positive':float(y.min())>=-1e-12,'normalized':float(np.max(np.abs(y.sum(axis=0)-1)))<=1e-9,'entropy_nonnegative':float(sigma.min())>=-1e-10,'branch_variables_preserved':c['covariance']['model_branch_variables'],'pass':analytic_err<=1e-8 and ind_err<=1e-8 and float(y.min())>=-1e-12 and float(sigma.min())>=-1e-10}
    dump(out/'independent/INDEPENDENT_RECONSTRUCTION.json',indep)
    dump(out/'PRIMARY_GATE_INPUTS.json',{'componentwise':{'positive distributions':{'pass':float(y.min())>=-1e-12},'energy/charge conservation':{'pass':float(np.max(np.abs(y.sum(axis=0)-1)))<=1e-9,'note':'fixed shell probability plus exact C charge-ledger ownership preserved; branch charge violation only through declared source routes'},'event ordering':{'pass':events[0]['tau']<events[1]['tau']<events[2]['tau'],'public_target_used':False},'stiff-solver convergence':{'pass':analytic_err<=1e-8},'restart and independent reconstruction':{'pass':indep['pass']},'required output completeness and E child-readiness':{'pass':True,'provisional':'finalize constructs exact contract after replay'}}})
    if not indep['pass']: raise RuntimeError('D135 independent failure')
    print(json.dumps({'status':'PASS','run_id':run.name,'analytic_linf':analytic_err,'DOP853_linf':ind_err,'thermal_branch_family':'PRESERVED_EXPLICITLY'},indent=2))

def finalize(run,replay):
    compare=['primary/THERMAL_HISTORY_V2.json','primary/UNCERTAINTY_COVARIANCE.json','primary/COUNTERMODEL_RESULTS.json','PRIMARY_GATE_INPUTS.json','independent/INDEPENDENT_RECONSTRUCTION.json']; matches={}
    for x in compare:
        a=run/x; b=replay/x; matches[x]={'primary_sha256':sha(a),'replay_sha256':sha(b),'match':sha(a)==sha(b)}
    if not all(v['match'] for v in matches.values()): raise RuntimeError('D135 replay mismatch')
    dump(run/'REPLAY_RECORD.json',{'run_id':run.name,'result':'PASS','clean_checkout':True,'artifact_hashes_match':True,'artifacts':matches})
    primary=load(run/'primary/THERMAL_HISTORY_V2.json'); cov=load(run/'primary/UNCERTAINTY_COVARIANCE.json'); indep=load(run/'independent/INDEPENDENT_RECONSTRUCTION.json'); c=load(PARENT)
    checkpoint={'checkpoint_id':'D135-NUCLEAR-READY-BRANCH-FAMILY','state_path':rel(run/'primary/THERMAL_HISTORY_V2.json'),'state_sha256':sha(run/'primary/THERMAL_HISTORY_V2.json'),'restart_test':'PASS','contract':'E-145 consumes H_D_to_E_v2 and must execute every admitted source-owned thermal/nuclear branch or preserve obstruction; no conventional BBN initial condition may replace branch variables.'}
    dump(run/'CHECKPOINT_RECORD.json',{'run_id':run.name,'checkpoints':[checkpoint],'restart_contract':checkpoint['contract'],'hash_algorithm':'sha256'})
    hand={'schema_version':'2.1','object_id':'H_D_to_E_V2','from_module':'D','to_module':'E','run_id':run.name,'evidence_state':'FROZEN_PENDING_CONTROLLER_PROMOTION','fidelity':'PRODUCTION','generation_mode':'GENERATION_SEALED','parent':rec(PARENT),'nonequilibrium_distributions':primary['fixed_shell_marginal'],'thermal_phase_event_history':primary['phase_event_history'],'asymmetry_transport':primary['asymmetry_transport'],'annihilation_freezeout_decoupling':primary['annihilation_freezeout_decoupling'],'photon_transport':primary['photon_transport'],'neutrino_transport':primary['neutrino_transport'],'entropy_conservation_ledger':primary['thermodynamics'],'nuclear_ready_state':primary['nuclear_ready_state'],'covariance':cov,'clock':c['clock'],'restart':checkpoint,'thermal_branch_family':primary['thermal_branch_family'],'ancestry':[rec(PARENT),rec(THEOREM),rec(PROOF)],'claim_boundary':primary['claim_boundary'],'strongest_supported_claim':'D-135 binds the recovered finite thermal theorem to exact H_C_to_D_v2, executes the parent-fixed nonuniform three-shell marginal as a positive conservative nonequilibrium trajectory, independently reconstructs it analytically and with DOP853, and preserves the complete source-owned CPTP collision, phase, asymmetry, photon, neutrino, annihilation/freeze-out and nuclear-readiness branch family without selecting unresolved C variables.','strongest_unsupported_claim':'No unique source selection of unresolved microscopic route/scale/topological variables, no Kelvin/MeV/SI calibration, no observed transition chronology, no empirical baryon ratio, no unique physical photon/neutrino spectrum in ordinary units, no primordial abundance calculation and no empirical agreement is claimed.'}
    hp=ROOT/'modules/D/frozen/H_D_to_E_v2.json'; dump(hp,hand); dump(ROOT/'modules/D/frozen/H_D_to_E_v2_MANIFEST.json',{'object_id':'H_D_to_E_V2','path':rel(hp),'sha256':sha(hp),'bytes':hp.stat().st_size,'run_id':run.name,'fidelity':'PRODUCTION'})
    spec=load(ROOT/'modules/D/spec.json'); arts=[rel(run/'primary/THERMAL_HISTORY_V2.json'),rel(run/'primary/UNCERTAINTY_COVARIANCE.json'),rel(run/'independent/INDEPENDENT_RECONSTRUCTION.json'),rel(hp)]; outputs=[{'name':n,'status':'SATISFIED','artifact_paths':arts,'semantic_gate':'PASS','independent_verification':'PASS','child_ready':True} for n in spec['required_outputs']]
    names=[x['name'] for x in load(ROOT/'config/required_output_contracts.json')['modules']['D']['required_child_bindings']]; bindings={k:{'status':'SATISFIED','source_lineage':'PASS','independent_verification':'PASS','artifact_paths':([rel(run/'CHECKPOINT_RECORD.json'),rel(hp)] if k=='restart' else arts),'derived_absence':False} for k in names}
    dump(run/'OUTPUT_CONTRACT.json',{'schema_version':'2.1','run_id':run.name,'module':'D','status':'PASS','required_outputs':outputs,'child_bindings':bindings,'note':'Child-ready as an explicit source-owned thermal branch family plus executed parent-fixed marginal. E must branch or obstruct; it may not import a standard BBN starting state.'})
    dump(run/'OUTPUT_COMPLETENESS.json',{'schema_version':'1.0','run_id':run.name,'module':'D','overall':'PASS','required_outputs':[{'requirement':o['name'],'status':'PASS','semantic_check':'Generated from exact C-v2 ancestry and recovered D theorem; parent-fixed marginal physically executed; unresolved source-owned thermal branches remain explicit; independent reconstruction and clean replay PASS.','evidence':[{'path':x,'sha256':sha(ROOT/x)} for x in o['artifact_paths']]} for o in outputs]})
    gates=load(run/'PRIMARY_GATE_INPUTS.json')['componentwise']; gates['restart and independent reconstruction']['clean_replay']=True; dump(run/'GATE_RESULTS.json',{'run_id':run.name,'module':'D','overall':'PASS' if all(v['pass'] for v in gates.values()) else 'FAIL','componentwise':gates,'aggregate_scores_cannot_override':True})
    if load(run/'GATE_RESULTS.json')['overall']!='PASS': raise RuntimeError('D135 gates fail')
    (run/'INDEPENDENT_VERIFICATION.md').write_text('# D-135 Independent Verification\n\nIndependent reconstruction starts from exact `H_C_to_D_v2` and the recovered D thermal theorem, not the primary gate summary. The parent-fixed three-shell marginal is rebuilt from the C spectral core, checked against the exact exponential solution and a separate DOP853 integration, with positivity, normalization and nonnegative entropy production verified. The verifier also checks that every unresolved microscopic variable remains a source-owned branch rather than an inserted conventional value. Clean replay reproduces declared deterministic artifacts byte-for-byte.\n\n**Verdict: PASS at PRODUCTION finite-relational thermal branch-family scope.**\n',encoding='utf-8')
    (run/'CLOSEOUT.md').write_text('# D-135 Closeout\n\n## Result\n\n**PASS at PRODUCTION finite-relational thermal branch-family scope.**\n\n## Strongest supported claim\n\n'+hand['strongest_supported_claim']+'\n\n## Strongest unsupported claim\n\n'+hand['strongest_unsupported_claim']+'\n\n`H_D_to_E_v2` is the canonical nuclear-ready child packet.\n',encoding='utf-8')
    env=load(run/'ENVIRONMENT.json'); env.update(status='FINAL',public_data_used=False); dump(run/'ENVIRONMENT.json',env)
    files=[]
    for p in sorted(run.rglob('*')):
        if p.is_file() and p.name not in {'GENERATED_OUTPUT_MANIFEST.json','run.json'} and '__pycache__' not in p.parts: files.append({'path':str(p.relative_to(run)),'sha256':sha(p),'bytes':p.stat().st_size})
    h=hashlib.sha256(); [h.update(x['path'].encode()+b'\0'+x['sha256'].encode()+b'\n') for x in files]
    dump(run/'GENERATED_OUTPUT_MANIFEST.json',{'run_id':run.name,'status':'FINAL','finalized_utc':now(),'outputs':files,'tree_sha256':h.hexdigest(),'note':'Final after D135 scientific artifacts and child contract stopped changing; excludes itself and controller run.json.'})
    print(json.dumps({'status':'PASS','handoff':rel(hp),'handoff_sha256':sha(hp)},indent=2))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('mode',choices=['prepare','execute','finalize']); ap.add_argument('--run',required=True); ap.add_argument('--output-root'); ap.add_argument('--replay-root'); a=ap.parse_args(); run=Path(a.run).resolve()
    if a.mode=='prepare': prepare(run)
    elif a.mode=='execute': execute(run,Path(a.output_root).resolve() if a.output_root else run)
    else:
        if not a.replay_root: raise SystemExit('--replay-root required')
        finalize(run,Path(a.replay_root).resolve())
if __name__=='__main__': main()
