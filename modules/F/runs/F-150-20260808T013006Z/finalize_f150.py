#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
RUN = ROOT / 'modules/F/runs/F-150-20260808T013006Z'
FROZEN = ROOT / 'modules/F/frozen'
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
spec = load(RUN/'FROZEN_DERIVATION_SPEC.json')
primary = load(RUN/'primary/POST_NUCLEAR_PERSISTENCE_STATE.json')
reaction = load(RUN/'solver_outputs/reaction_network/result.json')
transport = load(RUN/'solver_outputs/transport/result.json')
reaction_cfg = load(RUN/'solver_configs/F_reaction_network.json')
transport_cfg = load(RUN/'solver_configs/F_transport.json')
ind = load(RUN/'independent/INDEPENDENT_RECONSTRUCTION.json')
conv = load(RUN/'verification/CONVERGENCE.json')
cov = load(RUN/'verification/COVARIANCE.json')
restart = load(RUN/'verification/RESTART.json')
counter = load(RUN/'verification/COUNTERMODELS.json')
replay = load(RUN/'REPLAY_RECORD.json')
parent_path = ROOT/'modules/E/frozen/H_E_to_F.json'

assert sha(parent_path) == '975c4fcdfa2f4f861dd3085e14678116377bbe4d0fc23dd4e51f4373f9c2ecbf'
assert gates['overall'] == 'PASS'
assert all(v['pass'] for v in gates['componentwise'].values())
assert all(gates['additional_frozen_checks'].values())
assert reaction['success'] is True and transport['success'] is True
assert ind['pass'] is True and conv['pass'] is True and cov['pass'] is True and restart['pass'] is True
assert replay['result'] == 'PASS' and replay['clean_checkout'] is True and replay['artifact_hashes_match'] is True
assert primary['invariant_drifts'] == {'Q0':0.0,'Q1':0.0,'Q2':0.0,'Q_total':0.0,'U_plus_RFL':0.0}

handoff = {
  'schema_version':'1.0',
  'object_id':'H_F_to_G',
  'from_module':'F',
  'to_module':'G',
  'run_id':'F-150-20260808T013006Z',
  'evidence_state':'FROZEN_PENDING_CONTROLLER_PROMOTION',
  'fidelity':'MINIMAL_SPINE',
  'generation_mode':'GENERATION_SEALED',
  'parent':{'object_id':'H_E_to_F','path':'modules/E/frozen/H_E_to_F.json','sha256':'975c4fcdfa2f4f861dd3085e14678116377bbe4d0fc23dd4e51f4373f9c2ecbf'},
  'triadic_descent':spec['triadic_descent'],
  'clock':spec['clock_and_numerics']['clock'],
  'frame':'A-E finite relational pregeometry continued into F; no metric/FRW geometry introduced',
  'state':{
    'names':spec['transport_model']['state_names'],
    'entry':primary['entry_state'],
    'terminal':primary['terminal_state'],
    'species_identity_status':spec['state_space']['species_identity_status'],
    'empirical_isotope_correspondence':spec['state_space']['empirical_isotope_correspondence'],
    'internal_bound_free_coordinate':spec['state_space']['internal_bound_free_coordinate'],
    'electromagnetic_charge_status':primary['electromagnetic_charge_status'],
    'photon_status':primary['photon_status'],
    'neutrino_status':primary['neutrino_status']
  },
  'residual_reaction_and_transport':{
    'stoichiometry':spec['reaction_continuation_law']['stoichiometry'],
    'rate_expressions':spec['reaction_continuation_law']['rate_expressions'],
    'parameters':spec['reaction_continuation_law']['parameters'],
    'linear_invariants':spec['transport_model']['linear_invariants'],
    'internal_route_activity_seed':spec['transport_and_opacity_ownership']['internal_interaction_activity_seed'],
    'entry_kappa_int_F':spec['transport_and_opacity_ownership']['entry_kappa_int_F'],
    'physical_opacity_status':spec['transport_and_opacity_ownership']['physical_opacity_status'],
    'handoff_rule':spec['transport_and_opacity_ownership']['handoff_rule']
  },
  'energy_memory':{
    'entry_constitutive_energy':spec['energy_memory_law']['entry_constitutive_energy'],
    'entry_RFL_memory':spec['energy_memory_law']['entry_RFL_memory'],
    'protected_total':spec['energy_memory_law']['protected_total'],
    'transport_lift':spec['energy_memory_law']['transport_lift'],
    'radiation_typing':spec['energy_memory_law']['radiation_typing']
  },
  'uncertainty':{
    'propagated_covariance':cov['propagated'],
    'minimum_eigenvalue':min(cov['eigenvalues']),
    'maximum_eigenvalue':max(cov['eigenvalues']),
    'psd_tolerance':spec['covariance_law']['psd_tolerance'],
    'empirical_stochastic_uncertainty_claimed':False
  },
  'verification':{
    'gates_overall':'PASS',
    'reaction_result_sha256':sha(RUN/'solver_outputs/reaction_network/result.json'),
    'transport_result_sha256':sha(RUN/'solver_outputs/transport/result.json'),
    'reaction_config_sha256':sha(RUN/'solver_configs/F_reaction_network.json'),
    'transport_config_sha256':sha(RUN/'solver_configs/F_transport.json'),
    'frozen_derivation_sha256':sha(RUN/'FROZEN_DERIVATION_SPEC.json'),
    'finest_256_512_linf':conv['finest_256_512_linf'],
    'restart_linf':restart['split_vs_direct_linf'],
    'independent_linf':ind['primary_transport_linf'],
    'covariance_lambda_min':min(cov['eigenvalues']),
    'clean_replay':'PASS',
    'countermodels':'PASS'
  },
  'restart_contract':'G receives the exact internally typed seven-species plus RFL-memory F terminal state, inherited residual route law, three carrier ledgers plus Q_total, U+RFL invariant, internal bound/free coordinate, nonnegative route-activity transfer seed, propagated covariance, exact E ancestry, and explicit unassigned/dormant channel statuses. G may use these as source-transfer inputs but may not reinterpret kappa_int_F as photon opacity or manufacture electromagnetic charge, photons, neutrinos, atomic identities, public recombination history, metric/FRW time, or empirical constants without a new witnessed derivation.',
  'strongest_supported_claim':'From exact H_E_to_F, Module F executes and independently reconstructs a deterministic positive post-nuclear RFC persistence/transport state that preserves the complete internal seven-state composition, Q0/Q1/Q2/Q_total, constitutive-energy/RFL memory, parent route ancestry and covariance, while deriving only the internal bound/free coordinate and route-activity transfer seed supported by the current parent.',
  'strongest_unsupported_claim':'Module F does not establish Standard-Model isotope/electron/ion identities, an electromagnetic charge operator or neutrality theorem, a physical photon or neutrino distribution, measured electromagnetic opacity, atomic data, Kelvin/MeV/SI calibration, metric/FRW evolution, a public recombination coordinate, visibility/last scattering, CMB observables, or empirical agreement.',
  'claim_boundary':spec['claim_boundary']
}
run_handoff = RUN/'frozen/H_F_to_G.json'
module_handoff = FROZEN/'H_F_to_G.json'
write(run_handoff,handoff)
shutil.copy2(run_handoff,module_handoff)
assert run_handoff.read_bytes() == module_handoff.read_bytes()
manifest={'object_id':'H_F_to_G','sha256':sha(module_handoff),'bytes':size(module_handoff),'generation_mode':'GENERATION_SEALED','evidence_state':'FROZEN_PENDING_CONTROLLER_PROMOTION','fidelity':'MINIMAL_SPINE'}
write(FROZEN/'H_F_to_G_MANIFEST.json',manifest)
write(RUN/'frozen/H_F_to_G_MANIFEST.json',manifest)

checkpoint={
  'run_id':'F-150-20260808T013006Z',
  'checkpoints':[{'id':'F_ENTRY_FROM_E','tau_F':0.0,'state':primary['entry_state'],'source':'modules/E/frozen/H_E_to_F.json','source_sha256':'975c4fcdfa2f4f861dd3085e14678116377bbe4d0fc23dd4e51f4373f9c2ecbf'},{'id':'F_TERMINAL','tau_F':spec['clock_and_numerics']['t_span'][1],'state':primary['terminal_state'],'state_sha256':sha(RUN/'primary/POST_NUCLEAR_PERSISTENCE_STATE.json')}],
  'restart_contract':handoff['restart_contract'],
  'state_schema':'[X0,X1,X2,B01,B02,B12,T012,RFL_M], dimensionless internal RFC MINIMAL_SPINE state',
  'restart_split_vs_direct_linf':restart['split_vs_direct_linf'],
  'hash_algorithm':'sha256'
}
write(RUN/'CHECKPOINT_RECORD.json',checkpoint)

closeout=f'''# F-150 Closeout\n\n## Result\n\nPASS at `MINIMAL_SPINE`. Module F closes the post-nuclear persistence/transport link from the exact frozen E parent without resetting to familiar Standard-Model plasma assumptions. The executed state retains the seven internal RFC composite species and adds only the inherited RFL constitutive-energy memory coordinate.\n\nThe exact E residual reversible route law was continued over the frozen intrinsic `tau_F` persistence horizon. The state is numerically stationary to the frozen tolerances, while the inherited directional route activity remains nonzero and is retained as an internal transfer seed rather than retyped as physical photon opacity.\n\n## Componentwise gates\n\n- charge neutrality where derived: PASS; no electromagnetic charge operator was fabricated, and all actually derived carrier ledgers are exactly preserved.\n- energy and particle accounting: PASS; Q0/Q1/Q2/Q_total and U+RFL maximum drift is `0.0`.\n- covariance positive semidefinite: PASS; minimum propagated eigenvalue is `{min(cov['eigenvalues'])}`, above the frozen `-1e-18` tolerance.\n- replay from E: PASS; parent initial-state L_inf is `{gates['componentwise']['replay from E']['parent_initial_linf']}`, dual-solver L_inf is `{gates['componentwise']['replay from E']['dual_solver_linf']}`, and independent L_inf is `{gates['componentwise']['replay from E']['independent_linf']}`.\n\nAdditional frozen checks PASS: positivity, restart (`{restart['split_vs_direct_linf']}` L_inf), 64/128/256/512 convergence (`{conv['finest_256_512_linf']}` finest-pair L_inf), semantic countermodels, manufactured reference checks, and independent DOP853 reconstruction (`{ind['primary_transport_linf']}` L_inf).\n\n## Preserved implementation context\n\nThe initial verbatim F-WL-002 manufactured covariance program attempted to assign Wolfram's protected built-in symbol `C`. Repository context established that this call is a manufactured congruence/PSD test rather than the F physical law. The failed attempt is preserved, the syntax-only local-symbol rename is recorded, and the intended unchanged covariance check passes. No species, route, coefficient, state, interval, threshold, gate, falsifier, or claim boundary changed.\n\n## Canonical handoff\n\n`modules/F/frozen/H_F_to_G.json` SHA-256: `{manifest['sha256']}`.\n\nG receives exact composition/RFL state, carrier and energy ledgers, residual route law, internal bound/free coordinate, route-activity transfer seed, propagated covariance, ancestry, and explicit typing of unwitnessed electromagnetic/photon/neutrino channels.\n\n## Strongest supported claim\n\n{handoff['strongest_supported_claim']}\n\n## Strongest unsupported claim\n\n{handoff['strongest_unsupported_claim']}\n\n## Exact next child\n\nController-owned. After this PASS run is registered and F is promoted through the evidence ladder to `FROZEN / MINIMAL_SPINE`, `rfc.py advance --task F-150 --result PASS` may activate exactly one direct child, `G-160`, under `AUTO_SINGLE_CHILD_AFTER_PASS`.\n'''
(RUN/'CLOSEOUT.md').write_text(closeout,encoding='utf-8')

outputs=[]
for p in sorted(RUN.rglob('*')):
    if not p.is_file():
        continue
    rel=p.relative_to(RUN)
    if rel.as_posix()=='GENERATED_OUTPUT_MANIFEST.json':
        continue
    if rel.as_posix()=='run.json':
        continue
    if any(part in {'__pycache__','runtime_cache','scratch'} for part in rel.parts):
        continue
    outputs.append({'path':rel.as_posix(),'sha256':sha(p),'bytes':size(p)})
h=hashlib.sha256()
for rec in outputs:
    h.update(rec['path'].encode()); h.update(b'\0'); h.update(rec['sha256'].encode()); h.update(b'\n')
write(RUN/'GENERATED_OUTPUT_MANIFEST.json',{'run_id':'F-150-20260808T013006Z','status':'FINAL','finalized_utc':'PRE_CONTROLLER_CLOSE_FINAL','outputs':outputs,'tree_sha256':h.hexdigest(),'note':'Final generated scientific/output manifest. Excludes itself, caches/scratch, and controller-owned run.json, which close-run mutates exactly once during registration.'})

print(json.dumps({'handoff_sha256':manifest['sha256'],'handoff_bytes':manifest['bytes'],'gate_overall':gates['overall'],'terminal':primary['terminal_state']},indent=2))
