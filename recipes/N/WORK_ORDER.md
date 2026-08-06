# Module N Exact Work Order — Manifested Observer-Ready Universe

## Objective

Prove and construct that all executed sectors coexist in one compatible causal, conservation-bearing universe and generate truth-level observer interfaces.

## Frozen triadic descent

- **CIF:** all compatible sector states
- **QV:** cross-sector compatibility and observer projection
- **RFL:** one universe identity and truth products
- **N-body mode:** `RELATIONAL_GRAMMAR_ACTIVE`

## Derive these objects; do not substitute familiar answers

1. single global causal/conservation graph
2. cross-sector compatibility and covariance
3. truth metric/lightcone/maps/spectra/signals/catalogues
4. multimessenger/transient and observer-record interfaces
5. complete ancestry to A

## Exact Wolfram calls

- `N-WL-001` — Global causal-graph reachability audit
- `N-WL-002` — Block covariance compatibility audit

Run each through:

```bash
python tools/director.py wolfram-show --call <CALL_ID>
```

Submit the exact code to `WolframLanguageEvaluator`, save the returned output verbatim, and register it with `wolfram-record`.

## Local manufactured reference check

```bash
python tools/run_reference_checks.py --module N --output <RUN_DIR>/reference_checks.json
```

This is an implementation/invariant test only. It is not the actual module execution.

## Actual numerical execution obligations

1. global ledger closure
2. synthetic observation reconstruction
3. independent end-to-end replay

## Required final outputs

- single universe identity
- cross-sector causal graph
- truth lightcones/maps/spectra/signals/catalogues
- multimessenger/transient products
- environment and observer-record interfaces
- global uncertainty/covariance
- complete ancestry to the triad

## Componentwise mandatory gates

- no directory-merge substitution
- cross-domain compatibility
- global conservation
- lineage completeness
- synthetic observation closure
- independent end-to-end reconstruction

## Hard stop conditions

- directory merge substituted for one universe
- incompatible snapshots combined
- lineage or global conservation incomplete

## Claim boundary

One manifested RFC universe, not yet frozen or empirically validated.

## Prebuilt local execution engines

These engines execute a law already derived and frozen from admitted parents. They do **not** choose the law or its coefficients. Each configuration is created only through a provenance-complete binding sheet.

### `global_ledger`

Close the one-universe global conservation and ownership ledger.

Template: `configured_runs/templates/N_global_ledger.template.json`  
Binding sheet: `configured_runs/binding_sheets/N_global_ledger.bindings.json`

```bash
python tools/director.py solver-copy --module N --solver global_ledger --destination <RUN_DIR>
# Fill every binding record with an exact value, origin path, origin SHA-256, units, dimensions, and derivation object.
python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/N_global_ledger.template.json --binding-sheet <RUN_DIR>/binding_sheets/N_global_ledger.bindings.json --output <RUN_DIR>/solver_configs/N_global_ledger.json
python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/N_global_ledger.json --output-dir <RUN_DIR>/solver_outputs/global_ledger
```

### `synthetic_observation`

Generate truth-to-observation products without public comparison data.

Template: `configured_runs/templates/N_synthetic_observation.template.json`  
Binding sheet: `configured_runs/binding_sheets/N_synthetic_observation.bindings.json`

```bash
python tools/director.py solver-copy --module N --solver synthetic_observation --destination <RUN_DIR>
# Fill every binding record with an exact value, origin path, origin SHA-256, units, dimensions, and derivation object.
python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/N_synthetic_observation.template.json --binding-sheet <RUN_DIR>/binding_sheets/N_synthetic_observation.bindings.json --output <RUN_DIR>/solver_configs/N_synthetic_observation.json
python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/N_synthetic_observation.json --output-dir <RUN_DIR>/solver_outputs/synthetic_observation
```

Every `__BIND_...` token is a hard stop. The materializer verifies hashes and refuses unresolved or provenance-free values.
