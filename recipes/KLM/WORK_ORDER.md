# Module KLM Exact Work Order — Causal K–L–M Recurrence and Classification

## Objective

Replay causal backreaction among gravity, baryons/stars, and chemistry until the system reaches a lawfully classified state without forcing convergence.

## Frozen triadic descent

- **CIF:** admissible gravity/baryon/composition return states
- **QV:** causal backreaction and earliest-change replay
- **RFL:** classified coupled-state memory
- **N-body mode:** `DIRECT_MANY_BODY_ACTIVE`

## Derive these objects; do not substitute familiar answers

1. typed K->L, L->M, M->K/L return maps
2. causal witnesses and earliest affected checkpoints
3. componentwise convergence metrics and covariance updates
4. classification without forced fixed point

## Exact Wolfram calls

- `KLM-WL-001` — Fixed-point and Jacobian stability classifier
- `KLM-WL-002` — Exact finite-cycle and nonconvergence countermodels

Run each through:

```bash
python tools/director.py wolfram-show --call <CALL_ID>
```

Submit the exact code to `WolframLanguageEvaluator`, save the returned output verbatim, and register it with `wolfram-record`.

## Local manufactured reference check

```bash
python tools/run_reference_checks.py --module KLM --output <RUN_DIR>/reference_checks.json
```

This is an implementation/invariant test only. It is not the actual module execution.

## Actual numerical execution obligations

1. fixed-point, cycle, attractor and nonconvergence tests
2. restart/replay across earliest-change checkpoints
3. independent recurrence implementation

## Required final outputs

- iteration history
- causal return witnesses
- earliest affected checkpoints
- conservation/covariance updates
- restart/replay
- classification: fixed point, finite cycle, attractor, branch family, obstruction, or nonconvergence
- certified K*, L*, M* or certified alternative

## Componentwise mandatory gates

- no target-driven stopping
- componentwise convergence metrics
- return ownership
- clean replay
- independent implementation
- preserved failed attempts

## Hard stop conditions

- reduced F0 promoted to physical recurrence
- target-driven stopping
- fixed point forced despite other lawful class

## Claim boundary

Physical coupled-universe classification at executed fidelity.

## Prebuilt local execution engines

These engines execute a law already derived and frozen from admitted parents. They do **not** choose the law or its coefficients. Each configuration is created only through a provenance-complete binding sheet.

### `affine_recurrence`

Classify the frozen recurrence without forcing convergence.

Template: `configured_runs/templates/KLM_recurrence.template.json`  
Binding sheet: `configured_runs/binding_sheets/KLM_recurrence.bindings.json`

```bash
python tools/director.py solver-copy --module KLM --solver affine_recurrence --destination <RUN_DIR>
# Fill every binding record with an exact value, origin path, origin SHA-256, units, dimensions, and derivation object.
python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/KLM_recurrence.template.json --binding-sheet <RUN_DIR>/binding_sheets/KLM_recurrence.bindings.json --output <RUN_DIR>/solver_configs/KLM_recurrence.json
python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/KLM_recurrence.json --output-dir <RUN_DIR>/solver_outputs/affine_recurrence
```

Every `__BIND_...` token is a hard stop. The materializer verifies hashes and refuses unresolved or provenance-free values.
