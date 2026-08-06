# Module K Exact Work Order — Nonlinear Relational Gravity, Structures, Metric, and Lightcones

## Objective

Evolve the realized fields into nonlinear structure while preserving relativistic/metric, route, event, branch, conservation, lightcone, and lensing truth.

## Frozen triadic descent

- **CIF:** nonlinear relational configurations
- **QV:** gravitational/metric evolution, events and mergers
- **RFL:** structures, metric, lightcones and lensing memory
- **N-body mode:** `DIRECT_MANY_BODY_ACTIVE`

## Derive these objects; do not substitute familiar answers

1. nonlinear gravity/metric law from J and enhanced relational kernel
2. force/field and constraint structure
3. event/merger/branch handling
4. metric, Weyl, lightcone, ray/Jacobi and lensing truth

## Exact Wolfram calls

- `K-WL-001` — Pairwise antisymmetry and total momentum conservation
- `K-WL-002` — Leapfrog symplectic Jacobian determinant

Run each through:

```bash
python tools/director.py wolfram-show --call <CALL_ID>
```

Submit the exact code to `WolframLanguageEvaluator`, save the returned output verbatim, and register it with `wolfram-record`.

## Local manufactured reference check

```bash
python tools/run_reference_checks.py --module K --output <RUN_DIR>/reference_checks.json
```

This is an implementation/invariant test only. It is not the actual module execution.

## Actual numerical execution obligations

1. force and constraint accuracy
2. resolution/volume and integrator convergence
3. independent critical implementation and restart

## Required final outputs

- particle/field nonlinear state
- halos and structures
- metric and Weyl products
- lightcones
- ray/Jacobi/lensing products
- merger/event trees
- return interface to L and KLM

## Componentwise mandatory gates

- force/field accuracy
- constraint closure
- mass-energy conservation
- resolution/volume convergence
- restart/replay
- independent critical implementation

## Hard stop conditions

- gravity-only toy labeled hyper-realistic
- metric/lightcone/lensing products omitted
- initial phases tuned

## Claim boundary

Nonlinear RFC gravitational universe at stated fidelity.

## Prebuilt local execution engines

These engines execute a law already derived and frozen from admitted parents. They do **not** choose the law or its coefficients. Each configuration is created only through a provenance-complete binding sheet.

### `nbody`

Execute the active many-body gravity specialization with explicit coupling and units.

Template: `configured_runs/templates/K_nbody.template.json`  
Binding sheet: `configured_runs/binding_sheets/K_nbody.bindings.json`

```bash
python tools/director.py solver-copy --module K --solver nbody --destination <RUN_DIR>
# Fill every binding record with an exact value, origin path, origin SHA-256, units, dimensions, and derivation object.
python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/K_nbody.template.json --binding-sheet <RUN_DIR>/binding_sheets/K_nbody.bindings.json --output <RUN_DIR>/solver_configs/K_nbody.json
python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/K_nbody.json --output-dir <RUN_DIR>/solver_outputs/nbody
```

### `ray_bundle`

Propagate metric/lensing truth through frozen ray/Jacobi screens.

Template: `configured_runs/templates/K_ray_bundle.template.json`  
Binding sheet: `configured_runs/binding_sheets/K_ray_bundle.bindings.json`

```bash
python tools/director.py solver-copy --module K --solver ray_bundle --destination <RUN_DIR>
# Fill every binding record with an exact value, origin path, origin SHA-256, units, dimensions, and derivation object.
python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/K_ray_bundle.template.json --binding-sheet <RUN_DIR>/binding_sheets/K_ray_bundle.bindings.json --output <RUN_DIR>/solver_configs/K_ray_bundle.json
python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/K_ray_bundle.json --output-dir <RUN_DIR>/solver_outputs/ray_bundle
```

Every `__BIND_...` token is a hard stop. The materializer verifies hashes and refuses unresolved or provenance-free values.
