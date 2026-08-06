# Module HI Exact Work Order — Transfer Operator Instantiation

## Objective

Instantiate the frozen universal transfer operator on the realized background without changing either parent's law.

## Frozen triadic descent

- **CIF:** HU operator and I background
- **QV:** type-safe instantiation
- **RFL:** immutable composite transfer system
- **N-body mode:** `RELATIONAL_GRAMMAR_ACTIVE`

## Derive these objects; do not substitute familiar answers

1. exact parent type compatibility
2. operator/background composition without modifying either parent
3. mode/eigenstructure and covariance propagation

## Exact Wolfram calls

- `HI-WL-001` — Immutable operator-background composition
- `HI-WL-002` — Covariance propagation through instantiated operator

Run each through:

```bash
python tools/director.py wolfram-show --call <CALL_ID>
```

Submit the exact code to `WolframLanguageEvaluator`, save the returned output verbatim, and register it with `wolfram-record`.

## Local manufactured reference check

```bash
python tools/run_reference_checks.py --module HI --output <RUN_DIR>/reference_checks.json
```

This is an implementation/invariant test only. It is not the actual module execution.

## Actual numerical execution obligations

1. parent-hash check
2. composition/reconstruction test
3. independent instantiation

## Required final outputs

- instantiated transfer system
- mode/eigenstructure
- gauge/frame mapping
- error/covariance propagation
- H_HI_to_J

## Componentwise mandatory gates

- exact parent hashes
- no retune of HU or I
- operator-domain compatibility
- independent reconstruction

## Hard stop conditions

- HU or I are changed during instantiation
- domain/codomain mismatch
- retuning appears

## Claim boundary

RFC linear transfer realization.

## Prebuilt local execution engines

These engines execute a law already derived and frozen from admitted parents. They do **not** choose the law or its coefficients. Each configuration is created only through a provenance-complete binding sheet.

### `linear_transfer`

Instantiate the frozen transfer operator on the exact realized background.

Template: `configured_runs/templates/HI_instantiated_transfer.template.json`  
Binding sheet: `configured_runs/binding_sheets/HI_instantiated_transfer.bindings.json`

```bash
python tools/director.py solver-copy --module HI --solver linear_transfer --destination <RUN_DIR>
# Fill every binding record with an exact value, origin path, origin SHA-256, units, dimensions, and derivation object.
python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/HI_instantiated_transfer.template.json --binding-sheet <RUN_DIR>/binding_sheets/HI_instantiated_transfer.bindings.json --output <RUN_DIR>/solver_configs/HI_instantiated_transfer.json
python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/HI_instantiated_transfer.json --output-dir <RUN_DIR>/solver_outputs/linear_transfer
```

Every `__BIND_...` token is a hard stop. The materializer verifies hashes and refuses unresolved or provenance-free values.
