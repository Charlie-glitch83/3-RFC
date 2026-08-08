# Module F Exact Work Order — Post-Nuclear Plasma and Radiation Persistence

## Objective

Carry isotope, plasma, radiation, neutrino, and transport states from nucleosynthesis into recombination without losing lineage or covariance.

## Frozen triadic descent

- **CIF:** plasma/radiation/neutrino possibilities
- **QV:** transport, scattering and persistence
- **RFL:** post-nuclear state and covariance
- **N-body mode:** `RELATIONAL_GRAMMAR_ACTIVE`

## Derive these objects; do not substitute familiar answers

1. species/charge/plasma state from E
2. radiation/neutrino transport and opacity ownership
3. covariance-preserving transfer to G

## Exact Wolfram calls

- `F-WL-001` — Charge-neutral reaction-transfer audit
- `F-WL-002` — Covariance propagation and PSD check

Run each through:

```bash
python tools/director.py wolfram-show --call <CALL_ID>
```

Submit the exact code to `WolframLanguageEvaluator`, save the returned output verbatim, and register it with `wolfram-record`.

## Local manufactured reference check

```bash
python tools/run_reference_checks.py --module F --output <RUN_DIR>/reference_checks.json
```

This is an implementation/invariant test only. It is not the actual module execution.

## Actual numerical execution obligations

1. charge-neutrality and transport manufactured case
2. PSD covariance evolution
3. restart from E

## Required final outputs

- plasma composition and ionization state
- radiation/neutrino persistence
- opacity and transport state
- source-transfer ownership
- H_F_to_G

## Componentwise mandatory gates

- charge neutrality where derived
- energy and particle accounting
- covariance positive semidefinite
- replay from E

## Hard stop conditions

- composition lineage is lost
- charge/energy ledger fails
- covariance becomes non-PSD without diagnosed branch

## Claim boundary

Post-nuclear RFC plasma state.

## Prebuilt local execution engines

These engines execute a law already derived and frozen from admitted parents. They do **not** choose the law or its coefficients. Each configuration is created only through a provenance-complete binding sheet.

### `reaction_network`

Execute the post-nuclear plasma reaction network.

Template: `configured_runs/templates/F_reaction_network.template.json`  
Binding sheet: `configured_runs/binding_sheets/F_reaction_network.bindings.json`

```bash
python tools/director.py solver-copy --module F --solver reaction_network --destination <RUN_DIR>
# Fill every binding record with an exact value, origin path, origin SHA-256, units, dimensions, and derivation object.
python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/F_reaction_network.template.json --binding-sheet <RUN_DIR>/binding_sheets/F_reaction_network.bindings.json --output <RUN_DIR>/solver_configs/F_reaction_network.json
python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/F_reaction_network.json --output-dir <RUN_DIR>/solver_outputs/reaction_network
```

### `transport`

Execute coupled plasma/radiation transport.

Template: `configured_runs/templates/F_transport.template.json`  
Binding sheet: `configured_runs/binding_sheets/F_transport.bindings.json`

```bash
python tools/director.py solver-copy --module F --solver transport --destination <RUN_DIR>
# Fill every binding record with an exact value, origin path, origin SHA-256, units, dimensions, and derivation object.
python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/F_transport.template.json --binding-sheet <RUN_DIR>/binding_sheets/F_transport.bindings.json --output <RUN_DIR>/solver_configs/F_transport.json
python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/F_transport.json --output-dir <RUN_DIR>/solver_outputs/transport
```

Every `__BIND_...` token is a hard stop. The materializer verifies hashes and refuses unresolved or provenance-free values.
