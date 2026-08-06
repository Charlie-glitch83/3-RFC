# Module M Exact Work Order — Stellar/Explosive Nucleosynthesis, Chemistry, Dust, Cooling, and Opacity

## Objective

Generate element/isotope production, chemical enrichment, dust, cooling, opacity, and composition-dependent returns from the executed stellar history.

## Frozen triadic descent

- **CIF:** nuclear/chemical/dust possibilities
- **QV:** stellar/explosive processing and transport
- **RFL:** composition, cooling and opacity memory
- **N-body mode:** `RELATIONAL_GRAMMAR_ACTIVE`

## Derive these objects; do not substitute familiar answers

1. stellar/explosive reaction and yield laws from L histories
2. element/isotope and chemical-evolution state
3. dust/molecular/cooling/opacity state
4. causal M->K and M->L returns

## Exact Wolfram calls

- `M-WL-001` — Composition-network conserved-count audit
- `M-WL-002` — Cooling/opacity return Jacobian template

Run each through:

```bash
python tools/director.py wolfram-show --call <CALL_ID>
```

Submit the exact code to `WolframLanguageEvaluator`, save the returned output verbatim, and register it with `wolfram-record`.

## Local manufactured reference check

```bash
python tools/run_reference_checks.py --module M --output <RUN_DIR>/reference_checks.json
```

This is an implementation/invariant test only. It is not the actual module execution.

## Actual numerical execution obligations

1. network and yield convergence
2. species/nuclear conservation
3. earliest-change replay and independent reconstruction

## Required final outputs

- stellar/explosive yields with provenance
- element/isotope histories
- galactic/cosmic chemical evolution
- dust and molecular state
- cooling/opacity returns
- M_to_K and M_to_L interfaces

## Componentwise mandatory gates

- nuclear/species conservation
- yield source/derivation audit
- network convergence
- return causality and earliest-change replay
- independent reconstruction

## Hard stop conditions

- yields fitted to solar/public abundance patterns
- composition covariance dropped
- return causality missing

## Claim boundary

Generated RFC chemical and composition state.

## Prebuilt local execution engines

These engines execute a law already derived and frozen from admitted parents. They do **not** choose the law or its coefficients. Each configuration is created only through a provenance-complete binding sheet.

### `reaction_network`

Execute stellar/explosive nucleosynthesis and isotope return.

Template: `configured_runs/templates/M_nucleosynthesis.template.json`  
Binding sheet: `configured_runs/binding_sheets/M_nucleosynthesis.bindings.json`

```bash
python tools/director.py solver-copy --module M --solver reaction_network --destination <RUN_DIR>
# Fill every binding record with an exact value, origin path, origin SHA-256, units, dimensions, and derivation object.
python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/M_nucleosynthesis.template.json --binding-sheet <RUN_DIR>/binding_sheets/M_nucleosynthesis.bindings.json --output <RUN_DIR>/solver_configs/M_nucleosynthesis.json
python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/M_nucleosynthesis.json --output-dir <RUN_DIR>/solver_outputs/reaction_network
```

### `transport`

Execute chemical/dust/cooling/opacity transport.

Template: `configured_runs/templates/M_chemical_transport.template.json`  
Binding sheet: `configured_runs/binding_sheets/M_chemical_transport.bindings.json`

```bash
python tools/director.py solver-copy --module M --solver transport --destination <RUN_DIR>
# Fill every binding record with an exact value, origin path, origin SHA-256, units, dimensions, and derivation object.
python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/M_chemical_transport.template.json --binding-sheet <RUN_DIR>/binding_sheets/M_chemical_transport.bindings.json --output <RUN_DIR>/solver_configs/M_chemical_transport.json
python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/M_chemical_transport.json --output-dir <RUN_DIR>/solver_outputs/transport
```

Every `__BIND_...` token is a hard stop. The materializer verifies hashes and refuses unresolved or provenance-free values.
