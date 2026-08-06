# Module I Exact Work Order — Realized Background Geometry and Expansion

## Objective

Generate the universe's realized geometry, expansion, clocks, horizons, and distance structure from the accumulated physical state.

## Frozen triadic descent

- **CIF:** global physical configuration possibilities
- **QV:** constraint-satisfying geometry and clock evolution
- **RFL:** realized background, horizon and distance memory
- **N-body mode:** `RELATIONAL_GRAMMAR_ACTIVE`

## Derive these objects; do not substitute familiar answers

1. background variables and frames from G
2. geometry/expansion evolution and constraints
3. intrinsic clocks, horizons and distances
4. covariance and restart state

## Exact Wolfram calls

- `I-WL-001` — Kinematic expansion and horizon identities
- `I-WL-002` — Generic constraint-preservation condition

Run each through:

```bash
python tools/director.py wolfram-show --call <CALL_ID>
```

Submit the exact code to `WolframLanguageEvaluator`, save the returned output verbatim, and register it with `wolfram-record`.

## Local manufactured reference check

```bash
python tools/run_reference_checks.py --module I --output <RUN_DIR>/reference_checks.json
```

This is an implementation/invariant test only. It is not the actual module execution.

## Actual numerical execution obligations

1. constraint residual convergence
2. gauge/frame consistency
3. distance/horizon identities and independent solver

## Required final outputs

- metric/background state
- expansion and clock histories
- horizons and distances
- constraint and conservation ledgers
- covariance
- H_I_to_HI

## Componentwise mandatory gates

- equation/constraint derivation
- gauge/frame consistency
- no observed expansion history used as target
- numerical convergence and independent reconstruction

## Hard stop conditions

- observed expansion history is used as target
- clock/frame ambiguity unresolved
- constraint residual fails

## Claim boundary

Realized RFC background geometry.

## Prebuilt local execution engines

These engines execute a law already derived and frozen from admitted parents. They do **not** choose the law or its coefficients. Each configuration is created only through a provenance-complete binding sheet.

### `transport`

Integrate the internally derived background geometry/clock system.

Template: `configured_runs/templates/I_background_ode.template.json`  
Binding sheet: `configured_runs/binding_sheets/I_background_ode.bindings.json`

```bash
python tools/director.py solver-copy --module I --solver transport --destination <RUN_DIR>
# Fill every binding record with an exact value, origin path, origin SHA-256, units, dimensions, and derivation object.
python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/I_background_ode.template.json --binding-sheet <RUN_DIR>/binding_sheets/I_background_ode.bindings.json --output <RUN_DIR>/solver_configs/I_background_ode.json
python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/I_background_ode.json --output-dir <RUN_DIR>/solver_outputs/transport
```

Every `__BIND_...` token is a hard stop. The materializer verifies hashes and refuses unresolved or provenance-free values.
