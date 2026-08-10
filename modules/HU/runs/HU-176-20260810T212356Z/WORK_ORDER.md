# Module HU Exact Work Order — Frozen Universal Linear Transfer Operator

## Objective

Derive and freeze the background-independent portion of the linear transfer machinery before instantiation on a realized geometry.

## Frozen triadic descent

- **CIF:** admissible linear perturbation states
- **QV:** universal linear propagation
- **RFL:** frozen transfer operator
- **N-body mode:** `RELATIONAL_GRAMMAR_ACTIVE`

## Derive these objects; do not substitute familiar answers

1. background-independent operator domain/codomain
2. gauge/frame and constraint identities
3. operator uncertainty and frozen interface

## Exact Wolfram calls

- `HU-WL-001` — Linear transfer semigroup and superposition
- `HU-WL-002` — Operator constraint-invariant subspace audit

Run each through:

```bash
python tools/director.py wolfram-show --call <CALL_ID>
```

Submit the exact code to `WolframLanguageEvaluator`, save the returned output verbatim, and register it with `wolfram-record`.

## Local manufactured reference check

```bash
python tools/run_reference_checks.py --module HU --output <RUN_DIR>/reference_checks.json
```

This is an implementation/invariant test only. It is not the actual module execution.

## Actual numerical execution obligations

1. semigroup and superposition tests
2. symbolic identity verification
3. hash freeze before I instantiation

## Required final outputs

- typed operator
- domain and codomain
- gauge/frame contracts
- conservation and constraint identities
- operator uncertainty
- frozen H_HU_to_HI

## Componentwise mandatory gates

- no realized-background values smuggled into universal operator
- linearity-domain proof
- symbolic identity verification
- hash freeze

## Hard stop conditions

- realized I values enter HU
- linearity domain undefined
- operator changes after HI

## Claim boundary

Universal RFC transfer law at declared linear scope.

## Prebuilt local execution engines

These engines execute a law already derived and frozen from admitted parents. They do **not** choose the law or its coefficients. Each configuration is created only through a provenance-complete binding sheet.

### `linear_transfer`

Execute and freeze the universal linear transfer operator.

Template: `configured_runs/templates/HU_linear_transfer.template.json`  
Binding sheet: `configured_runs/binding_sheets/HU_linear_transfer.bindings.json`

```bash
python tools/director.py solver-copy --module HU --solver linear_transfer --destination <RUN_DIR>
# Fill every binding record with an exact value, origin path, origin SHA-256, units, dimensions, and derivation object.
python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/HU_linear_transfer.template.json --binding-sheet <RUN_DIR>/binding_sheets/HU_linear_transfer.bindings.json --output <RUN_DIR>/solver_configs/HU_linear_transfer.json
python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/HU_linear_transfer.json --output-dir <RUN_DIR>/solver_outputs/linear_transfer
```

Every `__BIND_...` token is a hard stop. The materializer verifies hashes and refuses unresolved or provenance-free values.
