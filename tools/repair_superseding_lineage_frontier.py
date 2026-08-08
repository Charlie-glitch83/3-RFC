#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, json
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
STATE=ROOT/'STATE.json'; QUEUE=ROOT/'WORK_QUEUE.json'
def now(): return datetime.now(timezone.utc).isoformat()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def save(p,o):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def append_jsonl(p,o):
    with Path(p).open('a',encoding='utf-8') as f: f.write(json.dumps(o,ensure_ascii=False)+'\n')

def load_child_guard_helper():
    p=ROOT/'tools/repair_child_readiness.py'
    spec=importlib.util.spec_from_file_location('child_guard_helper',p)
    m=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(m); return m

def install_controller_guard():
    m=load_child_guard_helper(); m.patch_rfc()

def binding(name, absence=False): return {'name':name,'allow_derived_absence':absence}
def write_contracts():
    save(ROOT/'config/required_output_contracts.json',{
      'schema_version':'2.0',
      'rule':'PASS/advance requires every live module-spec required output to be artifact-backed, semantically PASS, independently verified and child-ready. Lower-fidelity historical runs remain valid at earned scope but cannot satisfy a superseding child contract.',
      'superseding_lineage_packet':'recovery/BG_SUPERSEDING_LINEAGE_PACKET.md',
      'modules':{
        'B':{'child':'C','required_child_bindings':[binding(x) for x in ['first_physical_state','intrinsic_clock_origin','pregeometry_or_geometry','ordinary_sector_seed','radiative_sector_seed','compression_relic_seed','dissipative_tail_seed','field_current_conservation_state','route_event_branch_memory','uncertainty','restart','no_loss_ancestry']]},
        'C':{'child':'D','required_child_bindings':[binding(x) for x in ['microscopic_field_excitation_registry','interaction_generator','symmetry_and_charge_registry','mass_mixing_operators','rate_generating_interaction_grammar','bound_nucleon_role_states','photon_role_state','neutrino_role_family','asymmetry_source','prethermal_populations','covariance','restart']]},
        'D':{'child':'E','required_child_bindings':[binding(x) for x in ['nonequilibrium_distributions','thermal_phase_event_history','asymmetry_transport','annihilation_freezeout_decoupling','photon_transport','neutrino_transport','entropy_conservation_ledger','nuclear_ready_state','covariance','clock','restart']]},
        'E':{'child':'F','required_child_bindings':[binding(x) for x in ['isotope_registry','reaction_graph','source_owned_rates','abundance_trajectories','isotope_covariance','freezeout_witnesses','plasma_ready_composition','charge_ownership','radiation_neutrino_carryover','clock','restart']]},
        'F':{'child':'G','required_child_bindings':[binding('plasma_composition'),binding('ionization_state'),binding('radiation_state'),binding('neutrino_state',True),binding('charge_or_interaction_operator'),binding('atomic_candidate_registry'),binding('opacity_law'),binding('transport_state'),binding('recombination_entry_state'),binding('source_transfer_ownership'),binding('covariance'),binding('clock'),binding('restart')]},
        'G':{'children':['HU','I'],'required_child_bindings':[binding(x) for x in ['recombination_history','opacity_history','optical_depth','visibility_function','radiation_surface','covariance','clock','restart']]}
      },
      'forbidden_substitutions':['old PASS inheritance','public or remembered target values','textbook coefficient insertion','readiness scores in place of physical outputs','renaming generic internal hazards as physical opacity','familiar-particle labels without derived role/correspondence']})

def patch_recipe(module, child_label):
    name=f'required output completeness and {child_label} child-readiness'
    gp=ROOT/f'recipes/{module}/gates.json'; g=load(gp)
    if name not in [x.get('gate') for x in g.get('componentwise',[])]: g.setdefault('componentwise',[]).append({'gate':name,'required':'PASS'})
    save(gp,g)
    rp=ROOT/f'recipes/{module}/recipe.json'; r=load(rp)
    if name not in r.get('mandatory_gates',[]): r.setdefault('mandatory_gates',[]).append(name)
    r['child_readiness_contract']=f'config/required_output_contracts.json#modules.{module}'
    r['superseding_lineage_packet']='recovery/BG_SUPERSEDING_LINEAGE_PACKET.md'
    r['closure_rule']='A preserved lower-fidelity run may remain valid, but the superseding run cannot PASS until every live required output and required child binding is generated and independently verified.'
    for x in ['OUTPUT_CONTRACT.json contains any UNSATISFIED required output','a required child binding is missing source lineage or independent verification','a historical PASS/proxy/public target is used as a generative substitute']:
        if x not in r.get('hard_stop_conditions',[]): r.setdefault('hard_stop_conditions',[]).append(x)
    save(rp,r)

def task(id,title,module,status,dep,obj,child,fidelity='PRODUCTION'):
    return {'id':id,'title':title,'module':module,'status':status,'depends_on':[dep],'objective':obj,
      'steps':['Use recovery/BG_SUPERSEDING_LINEAGE_PACKET.md as the required repair order.','Preserve the earlier MINIMAL_SPINE run and exact executed ancestry; do not inherit its PASS as proof of the superseding output.','Admit recovered equations/derivations only as REPLAY_REQUIRED and bind every use to exact hashes.','Freeze definitions, source roles, candidate classes, equations, expected outcomes, tolerances, semantic gates, falsifiers, OUTPUT_CONTRACT and independent-verifier design before primary execution.','Execute the source-owned parent-driven science at the required fidelity; no public targets, remembered coefficients or resemblance-based labels may enter generation.','Run componentwise gates, semantic countermodels, convergence/resolution, covariance, restart, clean replay and independent reconstruction.','Freeze a versioned child handoff only if every required output and child binding is SATISFIED.'],
      'deliverables':[f'modules/{module}/runs/<RUN_ID>/OUTPUT_CONTRACT.json',f'modules/{module}/runs/<RUN_ID>/SOURCE_REGISTER.json',f'modules/{module}/runs/<RUN_ID>/GATE_RESULTS.json',f'modules/{module}/runs/<RUN_ID>/INDEPENDENT_VERIFICATION.md',f'modules/{module}/runs/<RUN_ID>/CLOSEOUT.md',f'versioned superseding {child} handoff and manifest'],
      'gates':['all module-spec required outputs SATISFIED','all configured child bindings SATISFIED','exact source/parent lineage','no public-data generation leakage','semantic countermodels','convergence, covariance, restart/replay and independent reconstruction'],
      'commit_message':f'Close {id} superseding {module} replay at verified scope','required_evidence_state':'FROZEN','required_fidelity':fidelity}

def update_queue_state():
    s=load(STATE); q=load(QUEUE); items=q['items']; by={x['id']:x for x in items}
    if s.get('active_work_unit')!='G-160' or s.get('current_run') is not None: raise SystemExit('HARD STOP: close the current G planning run before frontier repair')
    for m in 'BCDEF':
        rec=s['modules'][m]
        if rec.get('evidence_state')!='FROZEN' or rec.get('fidelity')!='MINIMAL_SPINE': raise SystemExit(f'HARD STOP: expected preserved {m} FROZEN/MINIMAL_SPINE')
    specs=[
      task('B-115','Supersede Module B Handoff: Four-Sector First-Physical Completion','B','ACTIVE','B-110','Replay the exact four-sector completion on the already executed Big-Implosion state and emit H_B_to_C_v2.','H_B_to_C_v2'),
      task('C-125','Supersede Module C: Channel-Complete Microscopic Constitution','C','BLOCKED','B-115','Replay the recovered finite-relational microscopic constitution from H_B_to_C_v2, including source-owned charge/symmetry/mass-mixing/interaction and photon/neutrino/nucleon-role states.','H_C_to_D_v2'),
      task('D-135','Supersede Module D: Channel-Complete Nonequilibrium Thermal History','D','BLOCKED','C-125','Execute the recovered nonequilibrium chronology from H_C_to_D_v2, including asymmetry, annihilation/freeze-out/decoupling and photon/neutrino transport.','H_D_to_E_v2'),
      task('E-145','Supersede Module E: Source-Owned Primordial Nucleosynthesis','E','BLOCKED','D-135','Execute the recovered source-owned nuclear network with isotope identities, rates, abundances, covariance and plasma-ready output.','H_E_to_F_v2'),
      task('F-155','Supersede Module F: Child-Ready Post-Nuclear Plasma','F','BLOCKED','E-145','Execute charge/plasma composition, photon/neutrino persistence, atomic candidates, opacity/transport and recombination-entry state from H_E_to_F_v2.','H_F_to_G_v2')]
    ids={x['id'] for x in items}; gi=next(i for i,x in enumerate(items) if x['id']=='G-160')
    for rec in specs:
        if rec['id'] not in ids: items.insert(gi,rec); gi+=1; ids.add(rec['id'])
        else:
            old=next(x for x in items if x['id']==rec['id']); old.update(rec)
    by={x['id']:x for x in items}; by['G-160']['status']='BLOCKED'; by['G-160']['depends_on']=['F-155']
    s['active_work_unit']='B-115'; s['current_module']='B'; s['current_run']=None; s['project_status']='ACTIVE'; s['repair_state']='BG_SUPERSEDING_REPLAY_AUTHORIZED_B_FIRST'
    g=s['modules']['G']; g['evidence_state']='BLOCKED'; g['fidelity']='UNSTARTED'; g['active_run']=None
    if not any(h.get('state')=='BLOCKED' and h.get('evidence')=='recovery/BG_SUPERSEDING_LINEAGE_PACKET.md' for h in g.setdefault('evidence_history',[])):
        g['evidence_history'].append({'state':'BLOCKED','fidelity':'UNSTARTED','evidence':'recovery/BG_SUPERSEDING_LINEAGE_PACKET.md','timestamp_utc':now(),'work_unit':'G-160','reason':'G primary execution requires H_F_to_G_v2 after ordered B-C-D-E-F superseding replay.'})
    s['strongest_supported_claim']='The exact prior B-G formal derivation/handoff corpus is recovered as REPLAY_REQUIRED, the existing A-F executed line remains preserved at its earned fidelity, and the repository now has a source-locked B-first superseding replay order whose first target is H_B_to_C_v2.'
    s['strongest_unsupported_claim']='No superseding H_B_to_C_v2 through H_F_to_G_v2 has yet been freshly executed and frozen in 3-RFC, so no repaired physical recombination/visibility/last-scattering state is currently established.'
    s['last_updated_utc']=now(); save(QUEUE,q); save(STATE,s)
    cp=ROOT/'CLAIMS_LEDGER.json'; claims=load(cp)
    for c in claims.get('claims',[]):
        if c.get('owner') in list('BCDEF') and c.get('fidelity')=='MINIMAL_SPINE': c['superseding_replay_status']='PRESERVED_LOWER_FIDELITY_EVIDENCE_NOT_SUPERSEDING_CHILD_PARENT'
    save(cp,claims)

def write_audit_docs():
    audit={'schema_version':'1.0','audit_id':'BG-SUPERSEDING-FRONTIER-20260808','result':'B_FIRST_REPLAY_REQUIRED','basis':['recovery/BG_SUPERSEDING_LINEAGE_PACKET.md','recovery/BG_REPLAY_CANDIDATE_MANIFEST.json','modules/G/runs/G-160-20260808T051613Z/PRE_EXECUTION_LOCK.json'],'preservation':'Existing B-F MINIMAL_SPINE runs remain immutable lower-fidelity evidence; old G obstruction/planning runs remain preserved.','ordered_replay':['B-115 -> H_B_to_C_v2','C-125 -> H_C_to_D_v2','D-135 -> H_D_to_E_v2','E-145 -> H_E_to_F_v2','F-155 -> H_F_to_G_v2','G-160 -> recombination/visibility only after H_F_to_G_v2'],'controller_repair':['OUTPUT_CONTRACT required for new physical runs','PASS requires live spec output completeness','child-binding contracts B through G','reopen higher-fidelity modules without erasing prior evidence'],'public_data_used':False,'created_utc':now()}
    save(ROOT/'audit/BG_SUPERSEDING_REPLAY_FRONTIER_20260808.json',audit)
    (ROOT/'audit/BG_SUPERSEDING_REPLAY_FRONTIER_20260808.md').write_text('# B-G superseding replay frontier\n\nThe recovered source packet fixes the repair order: **B -> C -> D -> E -> F -> G**. Existing B-F `MINIMAL_SPINE` runs are preserved at their earned scope. They are not rewritten and their PASS labels are not inherited by the superseding lineage. G remains blocked until a freshly executed child-ready `H_F_to_G_v2` exists. The active repair frontier is B-115, which preserves the executed Big-Implosion state and completes the four-sector B handoff before C is replayed.\n',encoding='utf-8')
    (ROOT/'docs/28_REQUIRED_OUTPUT_AND_CHILD_READINESS_PROTOCOL.md').write_text('# Required Output and Child-Readiness Protocol\n\nA numerical or generic gate PASS is necessary but not sufficient for canonical module closure. Every live `spec.json` required output must be represented in `OUTPUT_CONTRACT.json`, artifact-backed, semantically PASS, independently verified and child-ready. Required parent-to-child bindings are separately enforced by `config/required_output_contracts.json`. Lower-fidelity runs remain valid at earned scope but cannot silently satisfy a higher-fidelity child contract. `UNASSIGNED`, `NOT_DERIVED`, readiness scores, manufactured examples and generic hazards do not satisfy required physical bindings unless an explicit contract allows a derived absence and the absence is proved. Public targets, remembered textbook constants and resemblance-based identities remain forbidden generation inputs.\n',encoding='utf-8')

def add_test():
    (ROOT/'tests/test_superseding_lineage_frontier.py').write_text("""from pathlib import Path\nimport json,unittest\nROOT=Path(__file__).resolve().parents[1]\nclass T(unittest.TestCase):\n def test_packet_order(self):\n  q={x['id']:x for x in json.loads((ROOT/'WORK_QUEUE.json').read_text())['items']}\n  self.assertEqual(q['B-115']['depends_on'],['B-110']); self.assertEqual(q['C-125']['depends_on'],['B-115']); self.assertEqual(q['D-135']['depends_on'],['C-125']); self.assertEqual(q['E-145']['depends_on'],['D-135']); self.assertEqual(q['F-155']['depends_on'],['E-145']); self.assertEqual(q['G-160']['depends_on'],['F-155'])\n def test_contract_guard_installed(self):\n  t=(ROOT/'tools/rfc.py').read_text(); self.assertIn('validate_required_output_contract',t); self.assertIn('OUTPUT_CONTRACT.json',t)\n def test_f_to_g_bindings(self):\n  c=json.loads((ROOT/'config/required_output_contracts.json').read_text()); n={x['name'] for x in c['modules']['F']['required_child_bindings']}; self.assertTrue({'plasma_composition','ionization_state','radiation_state','opacity_law','recombination_entry_state'}<=n)\nif __name__=='__main__': unittest.main()\n""",encoding='utf-8')

def record():
    append_jsonl(ROOT/'memory/DECISION_LOG.jsonl',{'decision_id':'BG-SUPERSEDING-REPLAY-FRONTIER-20260808','timestamp_utc':now(),'work_unit':'B-115','decision':'Close the source-lineage repair by preserving B-F MINIMAL_SPINE evidence, blocking G primary execution, and authorizing the exact recovered superseding replay order B->C->D->E->F->G beginning at B-115.','basis':['recovery/BG_SUPERSEDING_LINEAGE_PACKET.md','modules/G/runs/G-160-20260808T051613Z/PRE_EXECUTION_LOCK.json','audit/BG_SUPERSEDING_REPLAY_FRONTIER_20260808.json'],'alternatives_rejected':['jump directly from reduced F to G','jump directly to F and bypass required B-C-D-E replay','inherit old PASS labels','fabricate missing radiation/opacity objects'],'changes_science':False,'required_replay':'B-115 through F-155 before G-160','commit_sha':''})

def main():
    p=ROOT/'recovery/BG_SUPERSEDING_LINEAGE_PACKET.md'; assert p.is_file()
    g=load(ROOT/'modules/G/runs/G-160-20260808T051613Z/PRE_EXECUTION_LOCK.json'); assert g.get('authorization')=='NOT_AUTHORIZED_PENDING_SUPERSEDING_F_TO_G_PARENT'
    install_controller_guard(); write_contracts()
    for m,ch in [('B','C'),('C','D'),('D','E'),('E','F'),('F','G'),('G','HU/I')]: patch_recipe(m,ch)
    update_queue_state(); write_audit_docs(); add_test(); record()
    print(json.dumps({'status':'PASS','active_repair':'B-115','ordered_replay':['B-115','C-125','D-135','E-145','F-155','G-160']},indent=2))
    return 0
if __name__=='__main__': raise SystemExit(main())
