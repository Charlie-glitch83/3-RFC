# Module G Exact Work Order — Nonequilibrium Recombination and Last-Scattering State

## Objective

Generate recombination, visibility, opacity, and radiation-surface histories from the physical plasma state.

## Frozen triadic descent

- **CIF:** bound/free-state possibilities
- **QV:** recombination, ionization and opacity evolution
- **RFL:** visibility and radiation surface
- **N-body mode:** `RELATIONAL_GRAMMAR_ACTIVE`

## Derive these objects; do not substitute familiar answers

1. nonequilibrium recombination network from F
2. opacity and optical-depth law
3. visibility/radiation-surface construction
4. uncertainty and restart packet

## Exact Wolfram calls

- `G-WL-001` — Visibility normalization identity for a positive opacity model
- `G-WL-002` — Three-state recombination-network conservation template

Run each through:

```bash
python tools/director.py wolfram-show --call <CALL_ID>
```

Submit the exact code to `WolframLanguageEvaluator`, save the returned output verbatim, and register it with `wolfram-record`.

## Local manufactured reference check

```bash
python tools/run_reference_checks.py --module G --output <RUN_DIR>/reference_checks.json
```

This is an implementation/invariant test only. It is not the actual module execution.

## Actual numerical execution obligations

1. stiff network convergence
2. visibility normalization/positivity
3. independent reconstruction

## Required final outputs

- ionization/recombination histories
- visibility and optical-depth functions
- radiation surface
- covariance and restart
- H_G_to_HU
- H_G_to_I

## Componentwise mandatory gates

- rate and opacity lineage
- normalization and positivity
- stiff convergence
- independent reconstruction

## Hard stop conditions

- public recombination history is inserted as target
- visibility is nonpositive or unnormalized
- rate lineage missing

## Claim boundary

Generated RFC last-scattering state, not observed CMB agreement.

## Prebuilt local execution engines

These engines execute a law already derived and frozen from admitted parents. They do **not** choose the law or its coefficients. Each configuration is created only through a provenance-complete binding sheet.

### `reaction_network`

Execute nonequilibrium recombination chemistry.

Template: `configured_runs/templates/G_recombination_network.template.json`  
Binding sheet: `configured_runs/binding_sheets/G_recombination_network.bindings.json`

```bash
python tools/director.py solver-copy --module G --solver reaction_network --destination <RUN_DIR>
# Fill every binding record with an exact value, origin path, origin SHA-256, units, dimensions, and derivation object.
python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/G_recombination_network.template.json --binding-sheet <RUN_DIR>/binding_sheets/G_recombination_network.bindings.json --output <RUN_DIR>/solver_configs/G_recombination_network.json
python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/G_recombination_network.json --output-dir <RUN_DIR>/solver_outputs/reaction_network
```

### `visibility`

Construct the physical visibility kernel from the executed opacity history.

Template: `configured_runs/templates/G_visibility.template.json`  
Binding sheet: `configured_runs/binding_sheets/G_visibility.bindings.json`

```bash
python tools/director.py solver-copy --module G --solver visibility --destination <RUN_DIR>
# Fill every binding record with an exact value, origin path, origin SHA-256, units, dimensions, and derivation object.
python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/G_visibility.template.json --binding-sheet <RUN_DIR>/binding_sheets/G_visibility.bindings.json --output <RUN_DIR>/solver_configs/G_visibility.json
python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/G_visibility.json --output-dir <RUN_DIR>/solver_outputs/visibility
```

Every `__BIND_...` token is a hard stop. The materializer verifies hashes and refuses unresolved or provenance-free values.
