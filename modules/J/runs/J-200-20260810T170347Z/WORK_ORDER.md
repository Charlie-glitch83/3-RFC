# Module J Exact Work Order — Primordial Covariance, Linear Spectra, and Finite-Volume Fields

## Objective

Generate the actual covariance, linear spectra, phases/seeds, and finite-volume field realization consumed by nonlinear gravity.

## Frozen triadic descent

- **CIF:** covariance and mode possibilities
- **QV:** PSD selection, phase realization and finite-volume promotion
- **RFL:** actual linear fields and restart memory
- **N-body mode:** `RELATIONAL_GRAMMAR_ACTIVE`

## Derive these objects; do not substitute familiar answers

1. actual primordial covariance from HI
2. linear spectra/growth and uncertainty
3. seed/phase provenance not selected for observational agreement
4. finite-volume fields and reality constraints

## Exact Wolfram calls

- `J-WL-001` — Positive-definite covariance and Cholesky reconstruction
- `J-WL-002` — Hermitian Fourier reality condition

Run each through:

```bash
python tools/director.py wolfram-show --call <CALL_ID>
```

Submit the exact code to `WolframLanguageEvaluator`, save the returned output verbatim, and register it with `wolfram-record`.

## Local manufactured reference check

```bash
python tools/run_reference_checks.py --module J --output <RUN_DIR>/reference_checks.json
```

This is an implementation/invariant test only. It is not the actual module execution.

## Actual numerical execution obligations

1. PSD and Cholesky checks
2. volume/resolution ensembles
3. independent field reconstruction

## Required final outputs

- positive-semidefinite covariance
- linear spectra and growth
- finite-volume fields
- phase/seed provenance
- promotion witnesses
- restartable P_J_to_K

## Componentwise mandatory gates

- covariance PSD
- reality/Hermitian conditions
- resolution and volume tests
- no public initial-condition file
- independent field reconstruction

## Hard stop conditions

- public initial-condition files or target phases enter
- covariance non-PSD
- representative spectrum is promoted to actual parent

## Claim boundary

One realized RFC linear universe and its uncertainty state.

## Prebuilt local execution engines

These engines execute a law already derived and frozen from admitted parents. They do **not** choose the law or its coefficients. Each configuration is created only through a provenance-complete binding sheet.

### `covariance`

Audit and sample the internally derived primordial covariance.

Template: `configured_runs/templates/J_covariance.template.json`  
Binding sheet: `configured_runs/binding_sheets/J_covariance.bindings.json`

```bash
python tools/director.py solver-copy --module J --solver covariance --destination <RUN_DIR>
# Fill every binding record with an exact value, origin path, origin SHA-256, units, dimensions, and derivation object.
python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/J_covariance.template.json --binding-sheet <RUN_DIR>/binding_sheets/J_covariance.bindings.json --output <RUN_DIR>/solver_configs/J_covariance.json
python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/J_covariance.json --output-dir <RUN_DIR>/solver_outputs/covariance
```

### `fourier_field`

Generate finite-volume fields with a frozen seed and Hermitian reality.

Template: `configured_runs/templates/J_fourier_field.template.json`  
Binding sheet: `configured_runs/binding_sheets/J_fourier_field.bindings.json`

```bash
python tools/director.py solver-copy --module J --solver fourier_field --destination <RUN_DIR>
# Fill every binding record with an exact value, origin path, origin SHA-256, units, dimensions, and derivation object.
python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/J_fourier_field.template.json --binding-sheet <RUN_DIR>/binding_sheets/J_fourier_field.bindings.json --output <RUN_DIR>/solver_configs/J_fourier_field.json
python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/J_fourier_field.json --output-dir <RUN_DIR>/solver_outputs/fourier_field
```

Every `__BIND_...` token is a hard stop. The materializer verifies hashes and refuses unresolved or provenance-free values.
