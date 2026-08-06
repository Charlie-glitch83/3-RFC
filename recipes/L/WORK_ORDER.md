# Module L Exact Work Order — Baryonic and Stellar Universe

## Objective

Execute hydro/MHD, radiation, thermochemistry, turbulence, collapse, generated stellar birth, stellar/binary populations, feedback, remnants, accretion, cosmic rays, and radiation sources.

## Frozen triadic descent

- **CIF:** gas/radiation/cloud/core/stellar possibilities
- **QV:** MHD, radiation, chemistry, collapse and star-birth evolution
- **RFL:** baryonic, stellar, feedback and remnant histories
- **N-body mode:** `DIRECT_MANY_BODY_ACTIVE`

## Derive these objects; do not substitute familiar answers

1. hydro/MHD/radiation/thermochemistry/turbulence/shock law
2. cloud/core/fragmentation/collapse witnesses
3. generated stellar birth measure rather than imported IMF
4. stellar/binary/population, feedback, remnant, accretion, cosmic-ray and ionizing-source states
5. exact L->M and L->K ownership returns

## Exact Wolfram calls

- `L-WL-001` — Finite-volume periodic conservation identity
- `L-WL-002` — Internally generated stellar birth-measure normalization

Run each through:

```bash
python tools/director.py wolfram-show --call <CALL_ID>
```

Submit the exact code to `WolframLanguageEvaluator`, save the returned output verbatim, and register it with `wolfram-record`.

## Local manufactured reference check

```bash
python tools/run_reference_checks.py --module L --output <RUN_DIR>/reference_checks.json
```

This is an implementation/invariant test only. It is not the actual module execution.

## Actual numerical execution obligations

1. mass/momentum/energy/species conservation
2. resolution/subgrid and birth-measure convergence
3. replay locality and independent implementation

## Required final outputs

- gas/MHD/radiation state
- cloud/core/collapse witnesses
- generated stellar birth measure
- stellar/binary/population histories
- feedback/remnant/accretion state
- L_to_M and L_to_K returns

## Componentwise mandatory gates

- mass/momentum/energy/species conservation
- resolution and subgrid convergence
- feedback ownership
- uncertainty/covariance
- replay locality
- independent implementation

## Hard stop conditions

- public scaling law calibration
- imported IMF is unexplained primitive
- old first-pass architecture is promoted to physical L without exact K parent

## Claim boundary

Physically executed RFC baryonic and stellar state.

## Prebuilt local execution engines

These engines execute a law already derived and frozen from admitted parents. They do **not** choose the law or its coefficients. Each configuration is created only through a provenance-complete binding sheet.

### `finite_volume`

Execute conservative baryonic finite-volume updates.

Template: `configured_runs/templates/L_finite_volume.template.json`  
Binding sheet: `configured_runs/binding_sheets/L_finite_volume.bindings.json`

```bash
python tools/director.py solver-copy --module L --solver finite_volume --destination <RUN_DIR>
# Fill every binding record with an exact value, origin path, origin SHA-256, units, dimensions, and derivation object.
python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/L_finite_volume.template.json --binding-sheet <RUN_DIR>/binding_sheets/L_finite_volume.bindings.json --output <RUN_DIR>/solver_configs/L_finite_volume.json
python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/L_finite_volume.json --output-dir <RUN_DIR>/solver_outputs/finite_volume
```

### `reaction_network`

Execute gas thermochemistry and composition-aware source terms.

Template: `configured_runs/templates/L_thermochemistry.template.json`  
Binding sheet: `configured_runs/binding_sheets/L_thermochemistry.bindings.json`

```bash
python tools/director.py solver-copy --module L --solver reaction_network --destination <RUN_DIR>
# Fill every binding record with an exact value, origin path, origin SHA-256, units, dimensions, and derivation object.
python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/L_thermochemistry.template.json --binding-sheet <RUN_DIR>/binding_sheets/L_thermochemistry.bindings.json --output <RUN_DIR>/solver_configs/L_thermochemistry.json
python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/L_thermochemistry.json --output-dir <RUN_DIR>/solver_outputs/reaction_network
```

Every `__BIND_...` token is a hard stop. The materializer verifies hashes and refuses unresolved or provenance-free values.
