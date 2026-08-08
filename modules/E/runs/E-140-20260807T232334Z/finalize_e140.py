#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
RUN = ROOT / 'modules/E/runs/E-140-20260807T232334Z'
FROZEN = ROOT / 'modules/E/frozen'
FROZEN.mkdir(parents=True, exist_ok=True)


def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def sha(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def size(path: Path):
    return path.stat().st_size


gates = load(RUN/'GATE_RESULTS.json')
summary = load(RUN/'verification/VERIFICATION_SUMMARY.json')
primary = load(RUN/'solver_outputs/reaction_network/result.json')
cfg = load(RUN/'solver_configs/E_reaction_network.json')
spec = load(RUN/'FROZEN_DERIVATION_SPEC.json')
freeze = load(RUN/'verification/FREEZE_OUT_WITNESS.json')
cov = load(RUN/'verification/UNCERTAINTY_COVARIANCE.json')
energy = load(RUN/'verification/ENERGY_MEMORY_LEDGER.json')
ind = load(RUN/'verification/INDEPENDENT_RECONSTRUCTION.json')
replay = load(RUN/'REPLAY_RECORD.json')
checkpoint = load(RUN/'CHECKPOINT_RECORD.json')
parent = load(ROOT/'modules/D/frozen/H_D_to_E.json')

assert gates['overall'] == 'PASS'
assert all(v['pass'] for v in gates['componentwise'].values())
assert summary['convergence_pass'] and summary['withheld_pass'] and summary['restart_pass'] and summary['replay_pass'] and summary['independent_pass'] and summary['covariance_pass'] and summary['freeze_pass']
assert primary['success'] is True
assert replay['result'] == 'PASS'
assert ind['pass'] is True
assert freeze['pass'] is True
assert cov['pass'] is True
assert energy['pass'] is True

species = cfg['model']['species']
terminal = primary['final']

primary_state = {
  'schema_version':'1.0',
  'object_id':'E_PRIMORDIAL_COMPOSITE_NETWORK_STATE',
  'run_id':'E-140-20260807T232334Z',
  'evidence_state':'PHYSICALLY_EXECUTED_PENDING_CONTROLLER_PROMOTION',
  'fidelity':'MINIMAL_SPINE',
  'generation_mode':'GENERATION_SEALED',
  'parent':{'object_id':'H_D_to_E','path':'modules/D/frozen/H_D_to_E.json','sha256':'37839ecc3a570a3d9fc4ee6e29ec36ebe921bf6ae7a710f816c741d1fa498231'},
  'species_order':species,
  'species_identity_status':'INTERNAL_RFC_COMPOSITE_IDENTITIES_ONLY; EMPIRICAL_ISOTOPE_CORRESPONDENCE_UNASSIGNED',
  'initial_state':cfg['initial_state'],
  'terminal_state':terminal,
  'minimum_abundance':primary['minimum_abundance'],
  'clock':'tau_E, dimensionless continuation of tau_D',
  't_span':cfg['t_span'],
  'reaction_model':cfg['model'],
  'freeze_out':freeze,
  'constitutive_energy_memory':energy,
  'abundance_covariance':cov['total_covariance'],
  'uncertainty_classification':cov['classification'],
  'checkpoint':checkpoint,
  'verification_summary':summary,
  'claim_boundary':'Internally generated, dimensionless, reaction-resolved RFC MINIMAL_SPINE primordial-composite network only. No Standard Model isotope identity, measured nuclear mass/binding/cross section/lifetime, Kelvin/MeV scale, conventional precision BBN or empirical abundance agreement is established.'
}
primary_path = RUN/'primary/PRIMORDIAL_COMPOSITE_NETWORK_STATE.json'
write(primary_path, primary_state)

ind_copy = {
  'schema_version':'1.0',
  'object_id':'E140_INDEPENDENT_RECONSTRUCTION',
  'run_id':'E-140-20260807T232334Z',
  **ind,
  'replay_final_linf':replay['final_linf'],
  'replay_artifact_hashes_match':replay['artifact_hashes_match']
}
ind_path = RUN/'independent/INDEPENDENT_RECONSTRUCTION.json'
write(ind_path, ind_copy)

handoff = {
  'schema_version':'1.0',
  'object_id':'H_E_to_F',
  'from_module':'E',
  'to_module':'F',
  'run_id':'E-140-20260807T232334Z',
  'evidence_state':'FROZEN_PENDING_CONTROLLER_PROMOTION',
  'fidelity':'MINIMAL_SPINE',
  'generation_mode':'GENERATION_SEALED',
  'parent':{'object_id':'H_D_to_E','path':'modules/D/frozen/H_D_to_E.json','sha256':'37839ecc3a570a3d9fc4ee6e29ec36ebe921bf6ae7a710f816c741d1fa498231'},
  'triadic_descent':{
    'CIF':'The exact D three-carrier parent opens protected additive composite occupancies and all locally witnessed disjoint-support positive-binding union possibilities.',
    'QV':'The source-owned reversible reaction hypergraph, with rates derived only from the inherited K3 edge rate, parent constitutive binding witnesses and Theta_E0, converts primitive carriers into composite states while preserving all three carrier ledgers.',
    'RFL':'The terminal composite composition, constitutive binding-memory transfer, freeze-out witnesses, covariance, route ancestry, restart state and failed-attempt history are stabilized as E memory.'
  },
  'nbody_mode':'RELATIONAL_GRAMMAR_ACTIVE',
  'clock':'tau_E, intrinsic dimensionless continuation of tau_D; no seconds imported',
  'frame':'A-D finite relational pregeometry; no metric/FRW geometry introduced in E',
  'species':{
    'order':species,
    'occupancy_vectors':{r['id']:r['occupancy'] for r in spec['derived_species_registry']},
    'identity_status':'INTERNAL_RFC_COMPOSITE_IDENTITIES_ONLY',
    'empirical_isotope_correspondence':'UNASSIGNED'
  },
  'reaction_network':{
    'directional_stoichiometry':cfg['model']['stoichiometry'],
    'rate_expressions':cfg['model']['rate_expressions'],
    'parameters':cfg['model']['parameters'],
    'invariants':cfg['model']['invariants'],
    'source_rule':'kf=m_r*a; kr=kf*exp(-B/Theta_E0), all quantities inherited/derived from frozen A-D lineage',
    'public_rate_table_used':False
  },
  'composition':{
    'initial':cfg['initial_state'],
    'terminal':terminal,
    'minimum_abundance':primary['minimum_abundance'],
    'freeze_tau_E':freeze['freeze_tau'],
    'freeze_state':freeze['freeze_state'],
    'final_rhs_norm':freeze['final_rhs_norm']
  },
  'constitutive_energy_memory':energy,
  'uncertainty':{
    'classification':cov['classification'],
    'covariance':cov['total_covariance'],
    'minimum_covariance_eigenvalue':cov['minimum_covariance_eigenvalue'],
    'empirical_rate_uncertainty_used':False,
    'stochastic_nuclear_uncertainty_claimed':False
  },
  'verification':{
    'gates_overall':'PASS',
    'primary_result_sha256':summary['primary_result_sha256'],
    'config_sha256':summary['config_sha256'],
    'frozen_derivation_sha256':summary['frozen_derivation_sha256'],
    'finest_two_linf':gates['componentwise']['network convergence']['finest_two_linf'],
    'tightened_linf':gates['componentwise']['network convergence']['tightened_linf'],
    'restart_linf':gates['componentwise']['withheld reaction and independent implementation checks']['restart_linf'],
    'independent_linf':gates['componentwise']['withheld reaction and independent implementation checks']['independent_linf'],
    'clean_replay':'PASS',
    'route_withholding':'PASS_WITH_FULL_TRAJECTORY_MATERIALITY',
    'preserved_failed_attempt':'verification/failures/attempt_001/GATE_RESULTS.json'
  },
  'restart_contract':'F receives the exact seven-component internally typed E terminal composition, frozen reversible route/rate registry, three carrier ledgers, dimensionless tau_E chronology, freeze-out witness, constitutive binding-memory state, covariance and ancestry. F may persist/evolve this internal RFC post-composite state but may not infer proton/neutron/isotope identities, Kelvin/MeV scales, measured nuclear data, public abundance targets, metric/FRW expansion or conventional post-BBN initial conditions from this handoff.',
  'strongest_supported_claim':'From the exact frozen D three-carrier state, Module E derives and physically executes a source-owned seven-state reversible primordial-composite reaction network with parent-derived binding/rates, exact carrier accounting, positive abundance history, material witnessed reaction routes, convergence, freeze-out, covariance, restart/replay and independent reconstruction.',
  'strongest_unsupported_claim':'Module E does not establish Standard Model isotope correspondence, measured nuclear masses/bindings/cross sections/lifetimes, physical Kelvin/MeV temperature, a conventional full BBN network, empirical primordial abundance agreement, metric cosmological expansion or full hyper-realistic nuclear physics.',
  'claim_boundary':'MINIMAL_SPINE internally typed RFC primordial-composite reaction state only.'
}
run_handoff = RUN/'frozen/H_E_to_F.json'
module_handoff = FROZEN/'H_E_to_F.json'
write(run_handoff, handoff)
shutil.copy2(run_handoff, module_handoff)
assert run_handoff.read_bytes() == module_handoff.read_bytes()

manifest = {
  'object_id':'H_E_to_F',
  'sha256':sha(module_handoff),
  'bytes':size(module_handoff),
  'generation_mode':'GENERATION_SEALED',
  'evidence_state':'FROZEN_PENDING_CONTROLLER_PROMOTION',
  'fidelity':'MINIMAL_SPINE'
}
write(FROZEN/'H_E_to_F_MANIFEST.json', manifest)
write(RUN/'frozen/H_E_to_F_MANIFEST.json', manifest)

closeout = f'''# E-140 Closeout\n\n## Result\n\nPASS at `MINIMAL_SPINE`. Module E now physically materializes the source-owned primordial-composite reaction network required by the active repository packet from the exact frozen Module-D parent. The run derives the internally typed seven-state composite registry, positive-binding admission law, six reversible witnessed association families, parent-derived forward/reverse rates, full abundance trajectory, exact internal carrier ledgers, constitutive-energy/RFL-memory transfer, freeze-out witness, inherited covariance propagation, checkpoint/restart, clean replay, semantic countermodels, route-withholding trajectories, and canonical `H_E_to_F`.\n\nThe first verification attempt is preserved: it incorrectly tested route materiality only by terminal equilibrium change and therefore returned FAIL. The frozen falsifier requires a detectable route effect, not a terminal-only effect. The implementation-only correction reran the full frozen matrix and measured full-trajectory route effects without changing species, rates, thresholds, initial state, interval, tolerances, gates, falsifiers, or claim boundary. All six withheld route families materially change the trajectory by `0.0560` to `0.0938`, far above the frozen `1e-8` threshold, while converging to the same detailed-balance terminal equilibrium.\n\n## Key generated state\n\n- terminal internal RFC composition: `{terminal}`\n- freeze witness: `tau_E={freeze['freeze_tau']}` with final RHS norm `{freeze['final_rhs_norm']}`\n- final constitutive energy: `{energy['U_final']}`\n- final RFL binding-memory transfer: `{energy['Q_RFL_final']}`\n- finest-two convergence L_inf: `{gates['componentwise']['network convergence']['finest_two_linf']}`\n- tightened-tolerance L_inf: `{gates['componentwise']['network convergence']['tightened_linf']}`\n- independent endpoint L_inf: `{gates['componentwise']['withheld reaction and independent implementation checks']['independent_linf']}`\n- restart L_inf: `{gates['componentwise']['withheld reaction and independent implementation checks']['restart_linf']}`\n- clean exact-config replay: `PASS`\n- covariance: `PASS`, minimum eigenvalue `{cov['minimum_covariance_eigenvalue']}`\n- canonical handoff SHA-256: `{manifest['sha256']}`\n\n## Componentwise gates\n\nAll mandatory E gates PASS: internal carrier/constitutive-energy accounting, network convergence, rate-source audit, no scalar-channel collapse, and withheld-reaction/independent-implementation checks. Aggregate scoring does not override componentwise gates.\n\n## Failures preserved and corrections made\n\n`verification/failures/attempt_001/GATE_RESULTS.json` preserves the first failed verification. The only correction was the route-materiality verifier: terminal-equilibrium-only comparison was replaced by the frozen gate's actual full-trajectory detectable-effect criterion. No scientific definition or threshold changed.\n\n## Independent reconstruction\n\nThe independent verifier rebuilt `M_C`, composite occupancy energies, binding increments, the twelve directional stoichiometric columns, `Q0/Q1/Q2`, all four rate coefficients, and the initial state directly from the frozen C/D parents, then integrated with DOP853. Result: PASS.\n\n## Strongest supported claim\n\nFrom the exact frozen D three-carrier state, RFC now has a generated, physically executed, independently reconstructed and cleanly replayed Module-E MINIMAL_SPINE primordial-composite reaction history with source-owned composite admission, reversible rates, exact carrier accounting, positive abundance dynamics, material route witnesses, constitutive binding-memory transfer, freeze-out and covariance.\n\n## Strongest unsupported claim\n\nModule E does not establish Standard Model proton/neutron/isotope correspondence, measured nuclear masses/bindings/cross sections/lifetimes, Kelvin/MeV calibration, conventional precision BBN, empirical primordial abundance agreement, metric/FRW expansion, or full hyper-realistic nuclear physics.\n\n## Exact next child\n\nController-owned. After E is closed and promoted to `FROZEN / MINIMAL_SPINE`, `rfc.py advance --task E-140 --result PASS` may activate only direct child `F-150` under `AUTO_SINGLE_CHILD_AFTER_PASS`. This closeout itself does not manually activate F.\n'''
(RUN/'CLOSEOUT.md').write_text(closeout, encoding='utf-8')

# Final generated-output manifest is last: it excludes itself and runtime/cache files.
outputs=[]
for p in sorted(RUN.rglob('*')):
    if not p.is_file():
        continue
    rel=p.relative_to(RUN)
    if rel.as_posix()=='GENERATED_OUTPUT_MANIFEST.json':
        continue
    if any(part in {'__pycache__','runtime_cache','scratch'} for part in rel.parts):
        continue
    outputs.append({'path':rel.as_posix(),'sha256':sha(p),'bytes':size(p)})
tree_h=hashlib.sha256()
for rec in outputs:
    tree_h.update(rec['path'].encode()); tree_h.update(b'\0'); tree_h.update(rec['sha256'].encode()); tree_h.update(b'\n')
write(RUN/'GENERATED_OUTPUT_MANIFEST.json',{
  'run_id':'E-140-20260807T232334Z','status':'FINALIZED','finalized_utc':'CONTROLLER_CLOSEOUT_PENDING',
  'outputs':outputs,'tree_sha256':tree_h.hexdigest(),
  'note':'Finalized after E scientific outputs stopped changing. Manifest excludes itself from tree hash.'
})

print(json.dumps({'handoff_sha256':manifest['sha256'],'handoff_bytes':manifest['bytes'],'gate_overall':gates['overall'],'terminal':terminal},indent=2))
