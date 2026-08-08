# Module C Exact Work Order — Microscopic Constitution

## Objective

Derive and execute the microscopic field, particle, interaction, mass, mixing, and prethermal population content from the first physical state.

## Frozen triadic descent

- **CIF:** physical excitation and symmetry candidates
- **QV:** constitution, interaction and selection
- **RFL:** stable fields, particles and charge/mass memory
- **N-body mode:** `RELATIONAL_GRAMMAR_ACTIVE`

## Derive these objects; do not substitute familiar answers

1. typed microscopic candidate spaces from B
2. symmetry/action candidate class and internally selected branch family
3. field, interaction, charge, mass and mixing structure or explicit obstruction
4. prethermal population and covariance state

## Exact Wolfram calls

- `C-WL-001` — Hermitian mass/mixing candidate and exact spectral invariants
- `C-WL-002` — Generic continuous-symmetry invariance equation solver

Run each through:

```bash
python tools/director.py wolfram-show --call <CALL_ID>
```

Submit the exact code to `WolframLanguageEvaluator`, save the returned output verbatim, and register it with `wolfram-record`.

## Local manufactured reference check

```bash
python tools/run_reference_checks.py --module C --output <RUN_DIR>/reference_checks.json
```

This is an implementation/invariant test only. It is not the actual module execution.

## Actual numerical execution obligations

1. symbolic symmetry and Hermiticity/unitarity checks
2. manufactured spectral reconstruction
3. independent implementation of the selected microscopic law

## Required final outputs

- typed fields and excitations
- interaction and symmetry structure
- mass/mixing generation or lawful branch family
- charge and conservation ownership
- prethermal populations and covariance
- H_C_to_D

## Componentwise mandatory gates

- units and dimensions
- symmetry/constraint closure
- positivity/unitarity or declared alternative
- no Standard Model label without derivation or correspondence theorem
- independent symbolic and numerical checks

## Hard stop conditions

- Standard Model names or constants are inserted without derivation/correspondence classification
- positivity/unitarity or declared replacement fails
- charges or conservation ownership are undefined

## Claim boundary

RFC microscopic constitution at the executed scope; empirical identity remains for Module P.

## Prebuilt local execution engines

These engines execute a law already derived and frozen from admitted parents. They do **not** choose the law or its coefficients. Each configuration is created only through a provenance-complete binding sheet.

### `spectral_model`

Audit internally derived mass/mixing/interaction matrix candidates and their symmetries.

Template: `configured_runs/templates/C_spectral_model.template.json`  
Binding sheet: `configured_runs/binding_sheets/C_spectral_model.bindings.json`

```bash
python tools/director.py solver-copy --module C --solver spectral_model --destination <RUN_DIR>
# Fill every binding record with an exact value, origin path, origin SHA-256, units, dimensions, and derivation object.
python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/C_spectral_model.template.json --binding-sheet <RUN_DIR>/binding_sheets/C_spectral_model.bindings.json --output <RUN_DIR>/solver_configs/C_spectral_model.json
python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/C_spectral_model.json --output-dir <RUN_DIR>/solver_outputs/spectral_model
```

Every `__BIND_...` token is a hard stop. The materializer verifies hashes and refuses unresolved or provenance-free values.
