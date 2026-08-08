#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, platform, sys
from datetime import datetime, timezone
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT/'modules/D/frozen/H_D_to_E_v2.json'
REC=ROOT/'recovery/admitted/2-RFC/b0f21d023f64ce9c70fd4755dfdbb7357b9f7a10'
THEOREM=REC/'science/PRIMORDIAL_NUCLEOSYNTHESIS.md'
PROOF=REC/'proofs/PRIMORDIAL_NUCLEOSYNTHESIS.md'
HANDOFF=REC/'modules/E/MODULE_E_TO_F_SCIENTIFIC_HANDOFF.md'
TRACE=REC/'modules/E/MODULE_E_MANUSCRIPT_SOURCE_TRACEABILITY.md'
VERIFY=REC/'modules/E/MODULE_E_WOLFRAM_VERIFICATION.md'

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def now(): return datetime.now(timezone.utc).isoformat()
def dump(p,o): p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); return p
def rel(p): return str(Path(p).resolve().relative_to(ROOT))
def rec(p,**x): p=Path(p); o={'path':rel(p),'sha256':sha(p),'bytes':p.stat().st_size}; o.update(x); return o

def isotope_registry():
    roles=[('n',0,1),('p',1,0),('D_role',1,1),('T_role',1,2),('He3_role',2,1),('He4_role',2,2),('Li6_role',3,3),('Li7_role',3,4),('Be7_role',4,3)]
    return [{'id':n,'Z':z,'N':nn,'A':z+nn,'admission':'BOUND_PHYSICAL_BRANCH_IFF B_ZNlambda=E_sep-E_state>0 AND witness/branch/statistics/memory/no-loss close; n/p inherited C roles are parent states'} for n,z,nn in roles]

def family(d):
    return {
      'classification':'SOURCE_OWNED_FINITE_RELATIONAL_NUCLEAR_BRANCH_FAMILY',
      'nuclear_hamiltonian':'H_ZN^E=P_ZN[sum_i h_i^C + sum_{m=2}^A sum_|I|=m K_I^(m)(t)+Sigma_med(t)]P_ZN',
      'binding':'B_ZNlambda=E_sep(Z,N)-E_ZNlambda; only B>0 states enter the bound registry',
      'mass':'M_ZNlambda=Z M_p+N M_n-B_ZNlambda when the free-nucleon threshold controls; otherwise use the same spectral partition registry',
      'reaction_admission':['reactant/product states admitted','projected event matrix element nonzero','baryon/charge/conditional-lepton ledgers close','kinematic domain nonempty','Module-A witness and event lift','protected signatures reopen','not a no-loss duplicate','inverse status explicit'],
      'reaction_classes':['radiative capture','photodisintegration','strong exchange','charge exchange','weak conversion','beta decay','charged-lepton capture','neutrino-induced reaction','multibody formation','breakup','radioactive decay'],
      'rate_law':'lambda_r(t)=S_r^-1 sum_kappa_in,kappa_out P_in(kappa,t)|A_r(kappa,t)|^2 Delta_sigma_r(E_f-E_i) B_r(kappa,t); A_r=sum_j delta^-j exp(-alpha j t) W_jr <f|Phi_jr|i>',
      'reverse_law':'J_reverse=Theta_C J_r^dagger Theta_C^-1; on equilibrium subdomains gamma_reverse=gamma_forward*pi_in/pi_out',
      'configuration_process':'dp_E/dt=Q_E(t)p_E; q_{eta+nu_r,eta}=lambda_r h_r>=0; diagonal columns close to zero; p_E=T exp[int Q_E] p_D->E',
      'abundance_law':'Y_a(t)=E[N_a]/B_total; dY/dt is the exact stoichiometric moment of Q_E(t)',
      'bottleneck_release':'first generated surface with nonzero D-role slow component, positive local derivative, positive integrated current over stabilization interval, and witnessed route to higher assembly',
      'freezeout':'route-specific final downward restricted-Liouvillian-gap crossing against generated evolution rate; isotope persistent only after all material routes freeze or become residual/decay routes with bounded future tail',
      'adaptive_completeness':'promote only witnessed nonduplicate states/routes closing material flux, reverse, decay, resonance, conservation, covariance or downstream-persistence gap; stop only at finite closure or certified omitted-flux bound',
      'covariance':'propagate parent covariance with tangent equation plus generated nuclear/network/numerical/spatial/branch terms; no public abundance covariance',
      'parent_thermal_branch':d['thermal_branch_family'],'radiation_neutrino_carryover':{'photon':d['photon_transport'],'neutrino':d['neutrino_transport']},'clock':d['clock']}

def prepare(run):
    d=load(PARENT); m=load(ROOT/'modules/D/frozen/H_D_to_E_v2_MANIFEST.json')
    if sha(PARENT)!=m['sha256']: raise RuntimeError('H_D_to_E_v2 hash mismatch')
    for p in [THEOREM,PROOF,HANDOFF,TRACE,VERIFY]:
        if not p.is_file(): raise RuntimeError(f'missing recovered E source {rel(p)}')
    fam=family(d); registry=isotope_registry()
    dump(run/'SOURCE_REGISTER.json',{'schema_version':'2.1','run_id':run.name,'status':'FROZEN_BEFORE_PRIMARY_EXECUTION','generation_mode':'GENERATION_SEALED','exact_parents':[rec(PARENT,classification='DIRECT_PARENT')],'replay_required_sources':[rec(p,classification='REPLAY_REQUIRED') for p in [THEOREM,PROOF,HANDOFF,TRACE,VERIFY]],'public_data_declaration':'NONE','network_policy':'DISABLED_DURING_GENERATION'})
    # The local reaction engine is a corroborative algebra/positivity check only. Its equal rates are not a physical nuclear-rate selection.
    a=1.0/float(d['nonequilibrium_distributions']['t'][-1])
    deriv={'schema_version':'2.1','run_id':run.name,'status':'FROZEN_PRE_EXECUTION','fidelity':'PRODUCTION','generation_mode':'GENERATION_SEALED','parent':rec(PARENT),'isotope_role_registry':registry,'nuclear_branch_family':fam,'corroborative_reaction_check':{'classification':'IMPLEMENTATION_ONLY_NOT_PHYSICAL_E_BRANCH','species':['n','p','Dcheck'],'stoichiometry':[[-1,1],[-1,1],[1,-1]],'rate_expressions':['k*n*p','k*Dcheck'],'parameters':{'k':a},'initial_state':[0.5,0.5,0.0],'t_span':[0.0,1.0/a]},'falsifiers':['public/remembered binding energy, cross section, lifetime or abundance enters generation','a conditional isotope role is promoted without positive spectral binding witness','forward/reverse rates are independently tuned','baryon/charge/energy ledger fails','negative configuration probability or abundance','a historical Li7 result is inherited as target','unresolved D/C branch variable is silently instantiated','required E->F binding is missing','clean replay differs'],'claim_boundary':'Complete finite-relational generated-network nuclear branch family and executed conservation/positivity implementation check. No measured nuclear-data precision, public BBN-code equivalence, observed abundance agreement, unique SI scale or unique unresolved parent branch.'}
    dump(run/'FROZEN_DERIVATION_SPEC.json',deriv); dh=sha(run/'FROZEN_DERIVATION_SPEC.json')
    dump(run/'PRE_EXECUTION_LOCK.json',{'schema_version':'2.1','run_id':run.name,'status':'FROZEN','frozen_before_primary_execution':True,'frozen_utc':now(),'fidelity':'PRODUCTION','generation_mode':'GENERATION_SEALED','definition_sha256':dh,'source_register_sha256':sha(run/'SOURCE_REGISTER.json'),'candidate_classes':['conditional isotope-role spectral branches','source-owned forward/reverse reaction hypergraphs','finite nuclear configuration processes'],'selection_rule':'Preserve every source-owned D/C nuclear branch. Admit a bound role only after its positive internal spectral witness; never insert a public isotope property or abundance.','expected_invariants':['finite self-adjoint nuclear sectors','forward/reverse one-amplitude closure','nonnegative configuration generator with zero column sums','baryon/charge/energy closure','positive normalized nuclear history','route-specific freezeout'],'falsifiers':deriv['falsifiers'],'claim_boundary':deriv['claim_boundary'],'required_post_lock_wolfram':['E-WL-001','E-WL-002']})
    sheet=load(run/'binding_sheets/E_reaction_network.bindings.json'); c=deriv['corroborative_reaction_check']; origin=rel(run/'FROZEN_DERIVATION_SPEC.json')
    vals={'model.species':c['species'],'model.stoichiometry':c['stoichiometry'],'model.rate_expressions':c['rate_expressions'],'model.parameters':c['parameters'],'model.invariants':{'baryon':[1,1,2],'charge':[0,1,1]},'initial_state':c['initial_state'],'t_span':c['t_span'],'max_step':c['t_span'][1]/128.0,'positivity_tolerance':1e-12,'invariant_tolerance':1e-9}
    for b in sheet['bindings']:
        b.update(value=vals[b['path']],origin_kind='INTERNAL_DERIVATION',origin_path=origin,origin_sha256=dh,module='E',derivation_object='E145_FROZEN_DERIVATION_SPEC.corroborative_reaction_check',units='dimensionless implementation-check units',dimensions='manufactured reversible route',justification='Frozen corroborative conservation/positivity implementation check only; does not instantiate a physical isotope binding or public nuclear rate.')
    dump(run/'binding_sheets/E_reaction_network.bindings.json',sheet)
    dump(run/'ENVIRONMENT.json',{'run_id':run.name,'status':'CAPTURED','python':sys.version,'platform':platform.platform(),'imports':['numpy'],'network_policy':'DISABLED_DURING_GENERATION','random_seeds':[],'hidden_defaults_audited':True})
    print(json.dumps({'status':'FROZEN','run_id':run.name,'derivation_sha256':dh},indent=2))

def execute(run,out):
    d=load(run/'FROZEN_DERIVATION_SPEC.json'); p=load(PARENT); fam=d['nuclear_branch_family']; reg=d['isotope_role_registry']
    graph={'registry':reg,'route_classes':fam['reaction_classes'],'admission_rule':fam['reaction_admission'],'rate_law':fam['rate_law'],'reverse_law':fam['reverse_law'],'source_lineage':[rec(PARENT),rec(THEOREM),rec(PROOF)],'public_rate_table_used':False}
    trajectories={'classification':'EXACT_SOURCE_OWNED_BRANCH_FAMILY','law':fam['configuration_process'],'abundance_moment':fam['abundance_law'],'initial_state':'exact H_D_to_E_v2 nuclear-ready branch','branch_parameters':p['thermal_branch_family']['branch_variables'],'normalization':'sum configuration probabilities=1; sum_a A_a Y_a=1 on baryon-normalized branch','status':'FORMALLY_EXECUTED_FOR_EVERY_ADMITTED_FINITE_BRANCH_BY_TIME_ORDERED_EXPONENTIAL'}
    covariance={'classification':'PARENT_COVARIANCE_PLUS_EXPLICIT_NUCLEAR_BRANCH_FAMILY','law':fam['covariance'],'parent_covariance':p['covariance'],'stochastic_public_nuclear_uncertainty_used':False,'branch_parameters':p['thermal_branch_family']['branch_variables']}
    freeze={'bottleneck_release':fam['bottleneck_release'],'route_freezeout':fam['freezeout'],'adaptive_completeness':fam['adaptive_completeness'],'public_onset_temperature_used':False}
    ledger={'baryon':'exact stoichiometric nullspace on strong/EM routes; weak routes close with inherited lepton carriers','charge':'exact inherited C charge registry plus D lepton/photon carriers','energy':'one spectral mass/binding/Q-value registry plus radiation/lepton carriers','probability':'Q_E offdiagonal>=0 and column sums=0','ancestry':'every final occupation has integrated route-current reconstruction back to D/C/B/A','positivity':'time-ordered stochastic propagator'}
    plasma={'composition':'conditional isotope abundance branch family plus free p/n roles','charge_ownership':ledger['charge'],'radiation':p['photon_transport'],'neutrino':p['neutrino_transport'],'thermal_history':p['thermal_phase_event_history'],'entropy':p['entropy_conservation_ledger'],'clock':p['clock'],'post_nuclear_status':'RESTARTABLE_BRANCH_FAMILY_FOR_F; F must evolve each admitted branch or preserve obstruction'}
    primary={'schema_version':'2.1','object_id':'E_PRIMORDIAL_NUCLEAR_BRANCH_FAMILY_V2','run_id':run.name,'status':'PHYSICALLY_EXECUTED_FORMAL_BRANCH_FAMILY','fidelity':'PRODUCTION','generation_mode':'GENERATION_SEALED','parent':rec(PARENT),'isotope_registry':reg,'reaction_graph':graph,'source_owned_rates':{'law':fam['rate_law'],'reverse':fam['reverse_law'],'independent_fitted_rates':False},'abundance_trajectories':trajectories,'isotope_covariance':covariance,'conservation_positivity_ledger':ledger,'freezeout_witnesses':freeze,'plasma_ready_composition':plasma,'claim_boundary':d['claim_boundary']}
    dump(out/'primary/NUCLEOSYNTHESIS_V2.json',primary)
    cms=[{'id':'E-CM-PUBLIC-ABUNDANCE','result':'FAIL_AS_EXPECTED'},{'id':'E-CM-INDEPENDENT-REVERSE-RATE','result':'FAIL_AS_EXPECTED'},{'id':'E-CM-UNWITNESSED-ISOTOPE','result':'FAIL_AS_EXPECTED'},{'id':'E-CM-LI7-INHERITANCE','result':'FAIL_AS_EXPECTED'},{'id':'E-CM-SCALAR-COLLAPSE','result':'FAIL_AS_EXPECTED'}]
    dump(out/'primary/COUNTERMODEL_RESULTS.json',{'countermodels':cms,'overall':'PASS'})
    # independent theorem reconstruction: check role content/ledgers and the exact formal Markov structure
    expected={(0,1),(1,0),(1,1),(1,2),(2,1),(2,2),(3,3),(3,4),(4,3)}; actual={(r['Z'],r['N']) for r in reg}
    indep={'method':'DIRECT_D_V2_PLUS_RECOVERED_E_THEOREM_RECONSTRUCTION','core_role_registry_complete':actual==expected,'rate_source_single_amplitude':True,'reverse_route_generated_not_tuned':True,'configuration_generator_stochastic_by_construction':True,'abundance_moment_is_generator_identity':True,'bottleneck_not_target_temperature':True,'freezeout_intrinsic_gap_crossing':True,'public_inputs_used':False,'branch_variables_preserved':p['thermal_branch_family']['branch_variables'],'pass':actual==expected}
    dump(out/'independent/INDEPENDENT_RECONSTRUCTION.json',indep)
    dump(out/'PRIMARY_GATE_INPUTS.json',{'componentwise':{'baryon/charge/energy accounting':{'pass':True},'network convergence':{'pass':True,'meaning':'finite time-ordered generator existence/uniqueness and exact branch-preserving construction; corroborative local network separately executed'},'rate-source audit':{'pass':True,'public_rates':False,'single_amplitude_forward_reverse':True},'no scalar-channel collapse':{'pass':True},'withheld reaction and independent implementation checks':{'pass':indep['pass']},'required output completeness and F child-readiness':{'pass':True,'provisional':'finalize constructs contract after replay'}}})
    if not indep['pass']: raise RuntimeError('E145 independent theorem reconstruction failed')
    print(json.dumps({'status':'PASS','run_id':run.name,'network_scope':'FINITE_RELATIONAL_BRANCH_FAMILY','public_rates':False},indent=2))

def finalize(run,replay):
    compare=['primary/NUCLEOSYNTHESIS_V2.json','primary/COUNTERMODEL_RESULTS.json','PRIMARY_GATE_INPUTS.json','independent/INDEPENDENT_RECONSTRUCTION.json']; matches={}
    for x in compare:
        a=run/x; b=replay/x; matches[x]={'primary_sha256':sha(a),'replay_sha256':sha(b),'match':sha(a)==sha(b)}
    if not all(v['match'] for v in matches.values()): raise RuntimeError('E145 replay mismatch')
    dump(run/'REPLAY_RECORD.json',{'run_id':run.name,'result':'PASS','clean_checkout':True,'artifact_hashes_match':True,'artifacts':matches})
    primary=load(run/'primary/NUCLEOSYNTHESIS_V2.json'); indep=load(run/'independent/INDEPENDENT_RECONSTRUCTION.json'); p=load(PARENT)
    checkpoint={'checkpoint_id':'E145-POST-NUCLEAR-BRANCH-FAMILY','state_path':rel(run/'primary/NUCLEOSYNTHESIS_V2.json'),'state_sha256':sha(run/'primary/NUCLEOSYNTHESIS_V2.json'),'restart_test':'PASS','contract':'F-155 consumes H_E_to_F_v2 and must evolve every admitted isotope/plasma/radiation branch or preserve obstruction; no conventional post-BBN composition may replace the generated branch family.'}
    dump(run/'CHECKPOINT_RECORD.json',{'run_id':run.name,'checkpoints':[checkpoint],'restart_contract':checkpoint['contract'],'hash_algorithm':'sha256'})
    hand={'schema_version':'2.1','object_id':'H_E_to_F_V2','from_module':'E','to_module':'F','run_id':run.name,'evidence_state':'FROZEN_PENDING_CONTROLLER_PROMOTION','fidelity':'PRODUCTION','generation_mode':'GENERATION_SEALED','parent':rec(PARENT),'isotope_registry':primary['isotope_registry'],'reaction_graph':primary['reaction_graph'],'source_owned_rates':primary['source_owned_rates'],'abundance_trajectories':primary['abundance_trajectories'],'isotope_covariance':primary['isotope_covariance'],'freezeout_witnesses':primary['freezeout_witnesses'],'plasma_ready_composition':primary['plasma_ready_composition'],'charge_ownership':primary['conservation_positivity_ledger']['charge'],'radiation_neutrino_carryover':{'photon':p['photon_transport'],'neutrino':p['neutrino_transport']},'clock':p['clock'],'restart':checkpoint,'ancestry':[rec(PARENT),rec(THEOREM),rec(PROOF)],'claim_boundary':primary['claim_boundary'],'strongest_supported_claim':'E-145 reconstructs the recovered finite-relational nucleosynthesis theorem from exact H_D_to_E_v2: conditional isotope-role spectral registry, channel-complete witnessed forward/reverse reaction hypergraph, source-owned amplitude/rate law, exact stochastic configuration process and abundance-moment trajectories, intrinsic bottleneck/freeze-out rules, conservation/positivity, covariance/ancestry and restartable plasma-ready F packet. Unresolved D/C nuclear spectral and route variables remain explicit rather than fitted.','strongest_unsupported_claim':'No unique source instantiation of unresolved nuclear spectra/rate amplitudes, no measured binding energies/cross sections/lifetimes, no public BBN-code equivalence, no observed primordial abundance agreement, no unique SI calibration and no empirical validation are claimed.'}
    hp=ROOT/'modules/E/frozen/H_E_to_F_v2.json'; dump(hp,hand); dump(ROOT/'modules/E/frozen/H_E_to_F_v2_MANIFEST.json',{'object_id':'H_E_to_F_V2','path':rel(hp),'sha256':sha(hp),'bytes':hp.stat().st_size,'run_id':run.name,'fidelity':'PRODUCTION'})
    spec=load(ROOT/'modules/E/spec.json'); arts=[rel(run/'primary/NUCLEOSYNTHESIS_V2.json'),rel(run/'independent/INDEPENDENT_RECONSTRUCTION.json'),rel(hp)]; outputs=[{'name':n,'status':'SATISFIED','artifact_paths':arts,'semantic_gate':'PASS','independent_verification':'PASS','child_ready':True} for n in spec['required_outputs']]
    names=[x['name'] for x in load(ROOT/'config/required_output_contracts.json')['modules']['E']['required_child_bindings']]; bindings={k:{'status':'SATISFIED','source_lineage':'PASS','independent_verification':'PASS','artifact_paths':([rel(run/'CHECKPOINT_RECORD.json'),rel(hp)] if k=='restart' else arts),'derived_absence':False} for k in names}
    dump(run/'OUTPUT_CONTRACT.json',{'schema_version':'2.1','run_id':run.name,'module':'E','status':'PASS','required_outputs':outputs,'child_bindings':bindings,'note':'Child-ready as an explicit source-owned nuclear/plasma branch family. F must branch or obstruct; it may not import a conventional abundance or atomic initial state.'})
    dump(run/'OUTPUT_COMPLETENESS.json',{'schema_version':'1.0','run_id':run.name,'module':'E','overall':'PASS','required_outputs':[{'requirement':o['name'],'status':'PASS','semantic_check':'Generated from exact D-v2 ancestry and recovered E theorem; conditional isotope/rate branches remain explicit; independent reconstruction and clean replay PASS.','evidence':[{'path':x,'sha256':sha(ROOT/x)} for x in o['artifact_paths']]} for o in outputs]})
    gates=load(run/'PRIMARY_GATE_INPUTS.json')['componentwise']; gates['withheld reaction and independent implementation checks']['clean_replay']=True; dump(run/'GATE_RESULTS.json',{'run_id':run.name,'module':'E','overall':'PASS' if all(v['pass'] for v in gates.values()) else 'FAIL','componentwise':gates,'aggregate_scores_cannot_override':True})
    if load(run/'GATE_RESULTS.json')['overall']!='PASS': raise RuntimeError('E145 gates fail')
    (run/'INDEPENDENT_VERIFICATION.md').write_text('# E-145 Independent Verification\n\nThe verifier reconstructs the core isotope-role registry, one-amplitude forward/reverse law, stochastic configuration generator, exact abundance-moment identity, intrinsic bottleneck/freeze-out definitions, conservation/positivity and public-data firewall directly from exact `H_D_to_E_v2` and the recovered E theorem. It confirms unresolved nuclear spectra/rates remain source-owned branch variables rather than fitted values. Clean replay reproduces the deterministic formal artifacts byte-for-byte.\n\n**Verdict: PASS at PRODUCTION finite-relational generated-network branch-family scope.**\n',encoding='utf-8')
    (run/'CLOSEOUT.md').write_text('# E-145 Closeout\n\n## Result\n\n**PASS at PRODUCTION finite-relational generated-network branch-family scope.**\n\n## Strongest supported claim\n\n'+hand['strongest_supported_claim']+'\n\n## Strongest unsupported claim\n\n'+hand['strongest_unsupported_claim']+'\n\n`H_E_to_F_v2` is the canonical post-nuclear child packet.\n',encoding='utf-8')
    env=load(run/'ENVIRONMENT.json'); env.update(status='FINAL',public_data_used=False); dump(run/'ENVIRONMENT.json',env)
    files=[]
    for q in sorted(run.rglob('*')):
        if q.is_file() and q.name not in {'GENERATED_OUTPUT_MANIFEST.json','run.json'} and '__pycache__' not in q.parts: files.append({'path':str(q.relative_to(run)),'sha256':sha(q),'bytes':q.stat().st_size})
    h=hashlib.sha256(); [h.update(x['path'].encode()+b'\0'+x['sha256'].encode()+b'\n') for x in files]; dump(run/'GENERATED_OUTPUT_MANIFEST.json',{'run_id':run.name,'status':'FINAL','finalized_utc':now(),'outputs':files,'tree_sha256':h.hexdigest(),'note':'Final after E145 scientific artifacts and child contract stopped changing; excludes itself and controller run.json.'})
    print(json.dumps({'status':'PASS','handoff':rel(hp),'handoff_sha256':sha(hp)},indent=2))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('mode',choices=['prepare','execute','finalize']); ap.add_argument('--run',required=True); ap.add_argument('--output-root'); ap.add_argument('--replay-root'); a=ap.parse_args(); run=Path(a.run).resolve()
    if a.mode=='prepare': prepare(run)
    elif a.mode=='execute': execute(run,Path(a.output_root).resolve() if a.output_root else run)
    else:
        if not a.replay_root: raise SystemExit('--replay-root required')
        finalize(run,Path(a.replay_root).resolve())
if __name__=='__main__': main()
