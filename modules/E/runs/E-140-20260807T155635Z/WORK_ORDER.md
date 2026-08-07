# Module E Exact Work Order — Primordial Nuclear Network

## Objective

Execute a source-owned reaction network to generate primordial isotope abundances and their full uncertainty state.

## Frozen triadic descent

- **CIF:** reaction graph and isotope possibilities
- **QV:** reaction flow and freeze-out
- **RFL:** abundance and covariance memory
- **N-body mode:** `RELATIONAL_GRAMMAR_ACTIVE`

## Derive these objects; do not substitute familiar answers

1. source-owned species and reaction graph
2. rate laws and uncertainty without public abundance fitting
3. conservation/nullspace structure
4. freeze-out witnesses and isotope covariance

## Exact Wolfram calls

- `E-WL-001` — Stoichiometric baryon and charge conservation
- `E-WL-002` — Reaction Jacobian and stiffness structure

Run each through:

```bash
python tools/director.py wolfram-show --call <CALL_ID>
```

Submit the exact code to `WolframLanguageEvaluator`, save the returned output verbatim, and register it with `wolfram-record`.

## Local manufactured reference check

```bash
python tools/run_reference_checks.py --module E --output <RUN_DIR>/reference_checks.json
```

This is an implementation/invariant test only. It is not the actual module execution.

## Actual numerical execution obligations

1. network-size and rate convergence
2. withheld-reaction tests
3. independent reaction integrator

## Required final outputs

- reaction graph and rates with source lineage
- abundance trajectories
- isotope covariance
- conservation and positivity ledger
- freeze-out/event witnesses
- H_E_to_F

## Componentwise mandatory gates

- baryon/charge/energy accounting
- network convergence
- rate-source audit
- no scalar-channel collapse
- withheld reaction and independent implementation checks

## Hard stop conditions

- solar or public abundance target influences generation
- scalar-channel collapse hides isotope failures
- baryon/charge ledger fails

## Claim boundary

Internally generated primordial nuclear state; observations remain sealed.

## Prebuilt local execution engines

These engines execute a law already derived and frozen from admitted parents. They do **not** choose the law or its coefficients. Each configuration is created only through a provenance-complete binding sheet.

### `reaction_network`

Execute the internally derived primordial reaction network with stoichiometric invariants.

Template: `configured_runs/templates/E_reaction_network.template.json`  
Binding sheet: `configured_runs/binding_sheets/E_reaction_network.bindings.json`

```bash
python tools/director.py solver-copy --module E --solver reaction_network --destination <RUN_DIR>
# Fill every binding record with an exact value, origin path, origin SHA-256, units, dimensions, and derivation object.
python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/E_reaction_network.template.json --binding-sheet <RUN_DIR>/binding_sheets/E_reaction_network.bindings.json --output <RUN_DIR>/solver_configs/E_reaction_network.json
python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/E_reaction_network.json --output-dir <RUN_DIR>/solver_outputs/reaction_network
```

Every `__BIND_...` token is a hard stop. The materializer verifies hashes and refuses unresolved or provenance-free values.
