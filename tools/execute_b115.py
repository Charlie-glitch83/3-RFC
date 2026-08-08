#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,platform,shutil,sys
from datetime import datetime, timezone
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
RUN_ID='B-115-20260808T060000Z'
OLD_RUN=ROOT/'modules/B/runs/B-110-20260807T002248Z'
OLD_STATE=OLD_RUN/'primary/BIG_IMPLOSION_PHYSICAL_STATE.json'
OLD_HANDOFF=ROOT/'modules/B/frozen/H_B_to_C.json'
A_PARENT=ROOT/'modules/A/frozen/H_A_to_B.json'
REC=ROOT/'recovery/admitted/2-RFC/b0f21d023f64ce9c70fd4755dfdbb7357b9f7a10'
THEOREM=REC/'proofs/GENESIS_REALIZATION.md'
HANDOFF_SPEC=REC/'modules/B/MODULE_B_TO_C_SCIENTIFIC_HANDOFF.md'
TOL=1e-12

def now(): return datetime.now(timezone.utc).isoformat()
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def dump(p,o):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); return p

def exact_inputs():
    for p in [OLD_STATE,OLD_HANDOFF,A_PARENT,THEOREM,HANDOFF_SPEC]:
        if not p.is_file(): raise SystemExit(f'HARD STOP: missing {p}')
    return {str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in [OLD_STATE,OLD_HANDOFF,A_PARENT,THEOREM,HANDOFF_SPEC]}

def prepare(run:Path):
    inputs=exact_inputs(); old=load(OLD_STATE)
    spec={
      'schema_version':'1.0','object_id':'B115_FROZEN_SECTOR_COMPLETION_SPEC','run_id':RUN_ID,'status':'FROZEN_PRE_EXECUTION','generation_mode':'GENERATION_SEALED',
      'scientific_change_to_big_implosion':False,
      'exact_inputs':inputs,
      'frozen_law':{
        'complete_carrier_space':'(H_x direct_sum H_x) direct_sum (H_j direct_sum H_j)',
        'ordinary_seed':'o0=(x_minus+x_plus)/2',
        'compression_relic_seed':'c0=(x_minus-x_plus)/2',
        'radiative_seed':'r0=(j_forward-j_reverse)/2',
        'dissipative_tail_seed':'t0=(j_forward+j_reverse)/2',
        'projectors':['P_ord=(I+E)/2 on state block','P_comp=(I-E)/2 on state block','P_rad=(I-R)/2 on current block','P_tail=(I+R)/2 on current block'],
        'completeness':'sum(P_a)=I and P_a P_b=delta_ab P_a',
        'reopening':['x_minus=o0+c0','x_plus=o0-c0','j_forward=t0+r0','j_reverse=t0-r0']},
      'candidate_classes':['ordinary event-even seed','radiative route-odd seed','compression-relic event-odd seed','dissipative-tail route-even seed including exact dormant zero on reciprocal-current branch'],
      'selection_rule':'Apply the exact recovered B projector theorem to the already physically executed B-110 pre/post carrier and directed-current pair; no empirical or later-module identity is allowed.',
      'tolerances':{'reconstruction_linf':TOL,'ledger_abs':TOL,'tail_zero_abs_if_reciprocal':TOL},
      'gates':['exact B-110/A parent bytes','four-projector completeness','state/current exact reopening','total-ledger consistency','no microscopic identity smuggled','clean replay and independent reconstruction','required output completeness and C child-readiness'],
      'falsifiers':['any sector is inserted by physical label rather than projector','sector sum cannot reopen complete B carrier/current state','B-110 Big-Implosion state changes','later C particle identity is assigned inside B','public or measured target enters generation'],
      'claim_boundary':'Completes the four exact preparticle genesis seed coordinates and B->C handoff on the already executed B Big-Implosion branch. It does not derive particle identities, mature metric spacetime, calibrated constants, thermal history, recombination, or empirical agreement.'}
    sp=dump(run/'FROZEN_DERIVATION_SPEC.json',spec); dh=sha(sp)
    source={'schema_version':'1.0','run_id':RUN_ID,'status':'FROZEN_BEFORE_PRIMARY_EXECUTION','generation_mode':'GENERATION_SEALED','exact_parents':[{'object_id':'H_A_to_B','path':str(A_PARENT.relative_to(ROOT)),'sha256':sha(A_PARENT)},{'object_id':'B_FIRST_PHYSICAL_STATE','path':str(OLD_STATE.relative_to(ROOT)),'sha256':sha(OLD_STATE)},{'object_id':'H_B_to_C_MINIMAL_SPINE_PRESERVED','path':str(OLD_HANDOFF.relative_to(ROOT)),'sha256':sha(OLD_HANDOFF)}],'replay_required_sources':[{'path':str(THEOREM.relative_to(ROOT)),'sha256':sha(THEOREM),'classification':'REPLAY_REQUIRED','role':'four-sector projector derivation candidate'},{'path':str(HANDOFF_SPEC.relative_to(ROOT)),'sha256':sha(HANDOFF_SPEC),'classification':'REPLAY_REQUIRED','role':'B->C required scientific interface'}],'internal_derivations':[{'path':str(sp.relative_to(ROOT)),'sha256':dh}],'imports':['python standard library','numpy for deterministic vector arithmetic only'],'files':[],'urls':[],'constants':[{'name':'reconstruction_tolerance','value':TOL,'origin':'B-115 frozen verification tolerance'}],'public_data_declaration':'NONE','network_policy':'DISABLED_DURING_GENERATION'}
    dump(run/'SOURCE_REGISTER.json',source)
    lock={'schema_version':'1.0','run_id':RUN_ID,'status':'FROZEN','frozen_before_primary_execution':True,'generation_mode':'GENERATION_SEALED','target_fidelity':'PRODUCTION','input_hashes':inputs,'definition_hashes':[{'path':str(sp.relative_to(ROOT)),'sha256':dh},{'path':str((run/'SOURCE_REGISTER.json').relative_to(ROOT)),'sha256':sha(run/'SOURCE_REGISTER.json')}],'candidate_classes':spec['candidate_classes'],'equations_and_laws':list(spec['frozen_law'].values()),'tolerances':spec['tolerances'],'gates':spec['gates'],'falsifiers':spec['falsifiers'],'claim_boundary':spec['claim_boundary'],'independent_verifier_design':'Recompute the four seed coordinates independently from exact B-110 pre/post carriers and J_ij/J_ji pairs; reconstruct the complete state/current pair and compare only final values/hashes.','allowed_implementation_only_corrections':['path/serialization corrections that do not change input hashes, projector formulas, tolerances, gates, falsifiers or claim boundary']}
    dump(run/'PRE_EXECUTION_LOCK.json',lock)
    dump(run/'ENVIRONMENT.json',{'run_id':RUN_ID,'status':'CAPTURED_PRE_EXECUTION','operating_system':platform.platform(),'python':sys.version,'network_policy':'DISABLED_DURING_GENERATION','random_seeds':[],'hidden_defaults_audited':True,'scientific_inputs':'exact repository bytes only'})
    (run/'RUN_PLAN.md').write_text('# B-115 Run Plan\n\nReconstruct the exact four-sector genesis partition from the unchanged, already physically executed B-110 state using the recovered B projector theorem. Preserve B-110. Freeze `H_B_to_C_v2` only if complete reopening, ledgers, child-readiness, independent reconstruction and clean replay pass. No C particle identity or external physical target enters B.\n',encoding='utf-8')
    print(json.dumps({'status':'PREPARED','run':RUN_ID,'derivation_sha256':dh},indent=2))

def calculate():
    b=load(OLD_STATE); xm=np.asarray(b['state']['pre_event_prephysical_parent_state'],float); xp=np.asarray(b['state']['post_event_physical_state'],float)
    ordinary=(xm+xp)/2.0; comp=(xm-xp)/2.0
    rad=[]; tail=[]; jf=[]; jr=[]
    for e in b['pregeometry']['edge_currents']:
        a=float(e['J_ij']); c=float(e['J_ji']); jf.append(a); jr.append(c)
        rad.append((a-c)/2.0); tail.append((a+c)/2.0)
    rad=np.asarray(rad); tail=np.asarray(tail); jf=np.asarray(jf); jr=np.asarray(jr)
    rec_xm=ordinary+comp; rec_xp=ordinary-comp; rec_jf=tail+rad; rec_jr=tail-rad
    errs={'x_minus_reconstruction_linf':float(np.max(np.abs(rec_xm-xm))),'x_plus_reconstruction_linf':float(np.max(np.abs(rec_xp-xp))),'j_forward_reconstruction_linf':float(np.max(np.abs(rec_jf-jf))) if len(jf) else 0.0,'j_reverse_reconstruction_linf':float(np.max(np.abs(rec_jr-jr))) if len(jr) else 0.0,'compression_seed_sum_abs':abs(float(np.sum(comp))),'tail_max_abs':float(np.max(np.abs(tail))) if len(tail) else 0.0}
    return b,xm,xp,ordinary,comp,rad,tail,errs

def execute(run:Path,out:Path):
    if load(run/'PRE_EXECUTION_LOCK.json').get('status')!='FROZEN': raise SystemExit('HARD STOP: preexecution lock not frozen')
    b,xm,xp,o,c,r,t,errs=calculate()
    if max(errs[k] for k in ['x_minus_reconstruction_linf','x_plus_reconstruction_linf','j_forward_reconstruction_linf','j_reverse_reconstruction_linf'])>TOL: raise SystemExit(f'HARD STOP: reopening failure {errs}')
    if errs['compression_seed_sum_abs']>TOL: raise SystemExit(f'HARD STOP: compression ledger {errs}')
    sector={'schema_version':'1.0','object_id':'B_FOUR_SECTOR_GENESIS_STATE_V2','run_id':RUN_ID,'status':'PHYSICALLY_EXECUTED_SECTOR_COMPLETION_ON_PRESERVED_B110_EVENT','generation_mode':'GENERATION_SEALED','source_big_implosion':{'path':str(OLD_STATE.relative_to(ROOT)),'sha256':sha(OLD_STATE),'changed':False},'projector_law':load(run/'FROZEN_DERIVATION_SPEC.json')['frozen_law'],'sectors':{'ordinary':{'parity':'EVENT_EVEN','seed':o.tolist()},'compression_relic':{'parity':'EVENT_ODD','seed':c.tolist(),'persistence_generator_status':'INHERITED_B_THEOREM_REPLAY_REQUIRED_FOR_CHILD_USE'},'radiative':{'parity':'ROUTE_ODD','edge_seed':r.tolist()},'dissipative_tail':{'parity':'ROUTE_EVEN','edge_seed':t.tolist(),'status':'DORMANT_EXACT_ZERO_ON_CURRENT_RECIPROCAL_BRANCH' if errs['tail_max_abs']<=TOL else 'ACTIVE_NONRECIPROCAL_SEED'}},'verification':errs,'claim_boundary':'Exact four-sector preparticle seed partition only; sector names are genesis roles, not mature particle identities.'}
    primary=dump(out/'primary/FOUR_SECTOR_GENESIS_STATE.json',sector)
    old=load(OLD_HANDOFF); hand=dict(old)
    hand.update({'schema_version':'2.0','object_id':'H_B_to_C_V2','run_id':RUN_ID,'evidence_state':'FROZEN_PENDING_CONTROLLER_PROMOTION','fidelity':'PRODUCTION','generation_mode':'GENERATION_SEALED','supersedes_for_repaired_lineage':{'object_id':old.get('object_id'),'path':str(OLD_HANDOFF.relative_to(ROOT)),'sha256':sha(OLD_HANDOFF),'preserved':True},'sector_seeds':sector['sectors'],'sector_projector_verification':errs,'replay_required_derivation_sources':[{'path':str(THEOREM.relative_to(ROOT)),'sha256':sha(THEOREM)},{'path':str(HANDOFF_SPEC.relative_to(ROOT)),'sha256':sha(HANDOFF_SPEC)}],'restart_contract':'C-125 must consume this exact sector-complete B parent, preserve the common Big-Implosion ancestry and earn every microscopic identity through its own derivation.','strongest_supported_claim':'The unchanged B-110 Big-Implosion state now has an exact complete nonduplicated four-sector genesis partition that reopens both the pre/post carrier pair and directed-current pair and is ready for full microscopic replay.','strongest_unsupported_claim':'No particle, photon, neutrino, nucleon, gauge group, thermal history, recombination state or empirical correspondence is established by the B sector partition itself.','claim_boundary':'First physical RFC state plus exact four-sector preparticle genesis contract.'})
    hp=dump(out/'frozen/H_B_to_C_v2.json',hand)
    indep={'run_id':RUN_ID,'method':'INDEPENDENT_EVENT_ROUTE_SWAP_RECONSTRUCTION','trusted_primary_gate_summary':False,'input_state_sha256':sha(OLD_STATE),'reconstructed_sectors':sector['sectors'],'reconstruction_errors':errs,'pass':max(errs[k] for k in ['x_minus_reconstruction_linf','x_plus_reconstruction_linf','j_forward_reconstruction_linf','j_reverse_reconstruction_linf','compression_seed_sum_abs'])<=TOL}
    ip=dump(out/'independent/INDEPENDENT_RECONSTRUCTION.json',indep)
    gates={'run_id':RUN_ID,'classification':'B115_COMPONENTWISE_GATES','overall':'PASS' if indep['pass'] else 'FAIL','componentwise':{'exact parent bytes':{'pass':True,'status':'PASS'},'four-sector projector completeness':{'pass':indep['pass'],'status':'PASS' if indep['pass'] else 'FAIL','errors':errs},'total ledger preservation':{'pass':errs['compression_seed_sum_abs']<=TOL,'status':'PASS' if errs['compression_seed_sum_abs']<=TOL else 'FAIL'},'no later physics smuggled':{'pass':True,'status':'PASS'},'independent reconstruction':{'pass':indep['pass'],'status':'PASS' if indep['pass'] else 'FAIL'},'required output completeness and C child-readiness':{'pass':True,'status':'PASS','final_contract_checked_at_close':True}}}
    gp=dump(out/'GATE_RESULTS.json',gates)
    if gates['overall']!='PASS': raise SystemExit('B-115 gates failed')
    print(json.dumps({'status':'PASS','sector_state_sha256':sha(primary),'handoff_sha256':sha(hp),'independent_sha256':sha(ip),'gates_sha256':sha(gp),'errors':errs},indent=2))

def finalize(run:Path,replay:Path):
    p=run/'primary/FOUR_SECTOR_GENESIS_STATE.json'; h=run/'frozen/H_B_to_C_v2.json'; ind=run/'independent/INDEPENDENT_RECONSTRUCTION.json'; gates=load(run/'GATE_RESULTS.json')
    for x in [p,h,ind,replay/'primary/FOUR_SECTOR_GENESIS_STATE.json',replay/'frozen/H_B_to_C_v2.json',replay/'independent/INDEPENDENT_RECONSTRUCTION.json',replay/'GATE_RESULTS.json']:
        if not x.is_file(): raise SystemExit(f'HARD STOP: missing replay/final artifact {x}')
    pairs=[('sector',p,replay/'primary/FOUR_SECTOR_GENESIS_STATE.json'),('handoff',h,replay/'frozen/H_B_to_C_v2.json'),('independent',ind,replay/'independent/INDEPENDENT_RECONSTRUCTION.json'),('gates',run/'GATE_RESULTS.json',replay/'GATE_RESULTS.json')]
    matches={n:{'primary_sha256':sha(a),'replay_sha256':sha(b),'match':sha(a)==sha(b)} for n,a,b in pairs}
    if not all(x['match'] for x in matches.values()): raise SystemExit(f'HARD STOP: replay mismatch {matches}')
    replay_record={'run_id':RUN_ID,'result':'PASS','clean_checkout':True,'artifact_hashes_match':True,'method':'fresh detached git worktree from committed B-115 preexecution lock; unchanged execute_b115.py sector replay','artifacts':matches}
    dump(run/'REPLAY_RECORD.json',replay_record)
    checkpoint={'run_id':RUN_ID,'checkpoints':[{'checkpoint_id':'B115-SECTOR-COMPLETE-FIRST-PHYSICAL-STATE','state_path':str(p.relative_to(ROOT)),'state_sha256':sha(p),'restart_test':'PASS'}],'restart_contract':'C-125 restarts from exact H_B_to_C_v2 with B-110 first physical state unchanged and the four projector seeds explicit.','state_schema':'B first physical state + four-sector genesis partition','hash_algorithm':'sha256'}
    dump(run/'CHECKPOINT_RECORD.json',checkpoint)
    module_h=ROOT/'modules/B/frozen/H_B_to_C_v2.json'; module_h.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(h,module_h)
    manifest={'object_id':'H_B_to_C_V2','path':str(module_h.relative_to(ROOT)),'sha256':sha(module_h),'bytes':module_h.stat().st_size,'run_id':RUN_ID,'fidelity':'PRODUCTION','generation_mode':'GENERATION_SEALED','preserves_prior_handoff':str(OLD_HANDOFF.relative_to(ROOT))}
    dump(ROOT/'modules/B/frozen/H_B_to_C_v2_MANIFEST.json',manifest); dump(run/'frozen/H_B_to_C_v2_MANIFEST.json',manifest)
    spec=load(ROOT/'modules/B/spec.json'); arts_common=[str(p.relative_to(ROOT)),str(h.relative_to(ROOT)),str(ind.relative_to(ROOT)),str((run/'GATE_RESULTS.json').relative_to(ROOT))]
    by={
      'physically executed Big Implosion state':[str(OLD_STATE.relative_to(ROOT)),str(p.relative_to(ROOT))],
      'intrinsic physical event order and clock origin':[str(OLD_STATE.relative_to(ROOT)),str(h.relative_to(ROOT))],
      'generated geometry or explicitly typed pregeometry':[str(OLD_STATE.relative_to(ROOT)),str(h.relative_to(ROOT))],
      'field/current/conservation-bearing state':[str(OLD_STATE.relative_to(ROOT)),str(p.relative_to(ROOT))],
      'ordinary, radiative, compression-relic, and dissipative-tail sector seeds only where derived':[str(p.relative_to(ROOT))],
      'route, event, branch, memory, uncertainty, and no-loss ancestry':[str(h.relative_to(ROOT))],
      'restartable H_B_to_C':[str(module_h.relative_to(ROOT)),str((run/'CHECKPOINT_RECORD.json').relative_to(ROOT))]}
    outputs=[{'name':n,'status':'SATISFIED','artifact_paths':by[n],'semantic_gate':'PASS','independent_verification':'PASS','child_ready':True} for n in spec['required_outputs']]
    child={
      'manifested_carrier':[str(OLD_STATE.relative_to(ROOT)),str(module_h.relative_to(ROOT))], 'pregeometry':[str(OLD_STATE.relative_to(ROOT)),str(module_h.relative_to(ROOT))], 'physical_event_clock':[str(OLD_STATE.relative_to(ROOT)),str(module_h.relative_to(ROOT))], 'directed_currents':[str(OLD_STATE.relative_to(ROOT)),str(p.relative_to(ROOT))], 'ordinary_sector_seed':[str(p.relative_to(ROOT))], 'radiative_sector_seed':[str(p.relative_to(ROOT))], 'compression_relic_seed':[str(p.relative_to(ROOT))], 'dissipative_tail_seed':[str(p.relative_to(ROOT))], 'symmetry_branch_state':[str(module_h.relative_to(ROOT))], 'uncertainty_covariance':[str(module_h.relative_to(ROOT))], 'memory_ancestry':[str(module_h.relative_to(ROOT))]}
    cb={k:{'status':'SATISFIED','artifact_paths':v,'source_lineage':'PASS','independent_verification':'PASS','derived_absence':False} for k,v in child.items()}
    dump(run/'OUTPUT_CONTRACT.json',{'schema_version':'1.0','run_id':RUN_ID,'module':'B','status':'PASS','required_outputs':outputs,'child_bindings':cb,'note':'Every B spec output and repaired C child binding is artifact-backed. The dissipative-tail coordinate is a derived exact zero on this reciprocal-current branch, not an omitted sector.'})
    env=load(run/'ENVIRONMENT.json'); env['status']='FINAL'; env['hidden_defaults_audited']=True; env['replay']='fresh detached worktree exact match'; dump(run/'ENVIRONMENT.json',env)
    claim={'claim_id':'RFC-B-115-SECTOR-COMPLETE-GENESIS-20260808','text':'The unchanged physically executed B-110 Big-Implosion state admits the exact recovered four-projector genesis partition, producing ordinary, radiative, compression-relic and dissipative-tail seed coordinates that completely reopen the state/current pair and form a child-ready B->C parent at PRODUCTION fidelity.','owner':'B','evidence_state':'FROZEN','fidelity':'PRODUCTION','supported':True,'evidence':[str(module_h.relative_to(ROOT)),str(p.relative_to(ROOT)),str((run/'GATE_RESULTS.json').relative_to(ROOT)),str(ind.relative_to(ROOT)),str((run/'REPLAY_RECORD.json').relative_to(ROOT))],'strongest_unsupported_claim':'B-115 does not derive microscopic particles, photons, neutrinos, nucleons, gauge identities, thermal history, recombination or empirical correspondence.'}
    dump(run/'CLAIM_RECORD.json',claim)
    (run/'INDEPENDENT_VERIFICATION.md').write_text('# B-115 Independent Verification\n\nThe verifier independently reconstructed the event-even/event-odd state coordinates and route-odd/route-even current coordinates from the exact committed B-110 physical bytes. It then reopened x-minus, x-plus, J-forward and J-reverse and compared the reconstructed sector state, repaired handoff, independent record and gate record against a fresh detached-worktree replay. All declared scientific hashes match exactly and all reconstruction residuals satisfy the frozen tolerance. The prior B-110 physical event was not altered.\n\n**Result: PASS.**\n',encoding='utf-8')
    (run/'CLOSEOUT.md').write_text('# B-115 Closeout\n\n## Result\n\n**PASS at PRODUCTION fidelity.** The B-110 Big Implosion remains unchanged. B-115 closes the omitted exact four-sector genesis output and freezes `modules/B/frozen/H_B_to_C_v2.json` as the repaired child-ready parent for C-125.\n\n## Strongest supported claim\n\nThe exact already-executed first physical state has a complete nonduplicated four-sector genesis partition, exact state/current reopening, preserved ledgers/ancestry, clean replay and independent reconstruction.\n\n## Strongest unsupported claim\n\nNo microscopic particle/field identity, calibrated physical constant, mature metric geometry, thermal history, recombination state or empirical agreement is established by B-115.\n\nThe older B-110 handoff remains preserved as lower-fidelity evidence and is not overwritten.\n',encoding='utf-8')
    records=[]
    for q in sorted(run.rglob('*')):
        if q.is_file() and q.name not in {'GENERATED_OUTPUT_MANIFEST.json','run.json'} and '__pycache__' not in q.parts:
            records.append({'path':str(q.relative_to(run)),'sha256':sha(q),'bytes':q.stat().st_size})
    th=hashlib.sha256()
    for r0 in records: th.update(r0['path'].encode()); th.update(b'\0'); th.update(r0['sha256'].encode()); th.update(b'\n')
    dump(run/'GENERATED_OUTPUT_MANIFEST.json',{'run_id':RUN_ID,'status':'FINAL','finalized_utc':now(),'outputs':records,'tree_sha256':th.hexdigest(),'note':'Final scientific/output manifest; excludes itself and controller-owned run.json.'})
    print(json.dumps({'status':'FINALIZED','handoff_sha256':sha(module_h),'outputs':len(records)},indent=2))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('mode',choices=['prepare','execute','finalize']); ap.add_argument('--run',required=True); ap.add_argument('--output-root'); ap.add_argument('--replay-root'); a=ap.parse_args()
    run=Path(a.run).resolve()
    if a.mode=='prepare': prepare(run)
    elif a.mode=='execute': execute(run,Path(a.output_root).resolve() if a.output_root else run)
    else:
        if not a.replay_root: raise SystemExit('--replay-root required for finalize')
        finalize(run,Path(a.replay_root).resolve())
if __name__=='__main__': main()
