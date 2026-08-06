# Module P Exact Work Order — Blind Empirical Comparison

## Objective

Ingest public evidence only after O, apply preregistered observation operators/statistics, and classify survival, tension, or falsification without retuning.

## Frozen triadic descent

- **CIF:** preregistered public comparison space
- **QV:** read-only statistics and falsifiers
- **RFL:** empirical result ledger
- **N-body mode:** `RELATIONAL_GRAMMAR_ACTIVE`

## Derive these objects; do not substitute familiar answers

1. version-locked datasets only after O
2. preregistered observation operators/statistics/covariance
3. multi-probe survival/tension/falsification classification
4. baseline comparisons without retuning

## Exact Wolfram calls

- `P-WL-001` — Generic frozen-prediction Gaussian statistic
- `P-WL-002` — Covariance positive-definiteness preregistration condition

Run each through:

```bash
python tools/director.py wolfram-show --call <CALL_ID>
```

Submit the exact code to `WolframLanguageEvaluator`, save the returned output verbatim, and register it with `wolfram-record`.

## Local manufactured reference check

```bash
python tools/run_reference_checks.py --module P --output <RUN_DIR>/reference_checks.json
```

This is an implementation/invariant test only. It is not the actual module execution.

## Actual numerical execution obligations

1. reproduce statistics independently
2. selection/window/covariance checks
3. verify O hash unchanged

## Required final outputs

- version-locked public datasets
- preregistered statistics
- covariance/selection/window treatment
- multi-probe residuals and likelihoods
- baseline comparators
- tension/falsifier ledger
- blind validation report

## Componentwise mandatory gates

- O hash unchanged
- no target deletion
- no covariance inflation
- no branch/seed/tolerance changes
- reproducible independent comparison

## Hard stop conditions

- target or statistic deleted post-reveal
- covariance inflated
- any information flows back to O or Q

## Claim boundary

Empirical survival, tension, or falsification of the frozen universe at tested scope.

## Prebuilt local execution engines

These engines execute a law already derived and frozen from admitted parents. They do **not** choose the law or its coefficients. Each configuration is created only through a provenance-complete binding sheet.

### `gaussian_comparison`

Perform read-only comparison after the O freeze.

Template: `configured_runs/templates/P_gaussian_comparison.template.json`  
Binding sheet: `configured_runs/binding_sheets/P_gaussian_comparison.bindings.json`

```bash
python tools/director.py solver-copy --module P --solver gaussian_comparison --destination <RUN_DIR>
# Fill every binding record with an exact value, origin path, origin SHA-256, units, dimensions, and derivation object.
python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/P_gaussian_comparison.template.json --binding-sheet <RUN_DIR>/binding_sheets/P_gaussian_comparison.bindings.json --output <RUN_DIR>/solver_configs/P_gaussian_comparison.json
python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/P_gaussian_comparison.json --output-dir <RUN_DIR>/solver_outputs/gaussian_comparison
```

Every `__BIND_...` token is a hard stop. The materializer verifies hashes and refuses unresolved or provenance-free values.
