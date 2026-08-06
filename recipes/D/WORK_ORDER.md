# Module D Exact Work Order — Nonequilibrium Thermal and Phase History

## Objective

Evolve the microscopic state through nonequilibrium thermodynamics, transport, phase changes, entropy production, and clock/frame-consistent expansion.

## Frozen triadic descent

- **CIF:** distribution and phase possibilities
- **QV:** collisions, transport and phase-event selection
- **RFL:** thermal history, entropy and event memory
- **N-body mode:** `RELATIONAL_GRAMMAR_ACTIVE`

## Derive these objects; do not substitute familiar answers

1. nonequilibrium state variables and clocks from C
2. collision/transport operators with exact ownership
3. phase-event witnesses and entropy production law
4. stiff solver and uncertainty/covariance evolution

## Exact Wolfram calls

- `D-WL-001` — Exact two-state transport conservation and Lyapunov decay
- `D-WL-002` — Transport Jacobian eigenstructure and stiffness diagnostic

Run each through:

```bash
python tools/director.py wolfram-show --call <CALL_ID>
```

Submit the exact code to `WolframLanguageEvaluator`, save the returned output verbatim, and register it with `wolfram-record`.

## Local manufactured reference check

```bash
python tools/run_reference_checks.py --module D --output <RUN_DIR>/reference_checks.json
```

This is an implementation/invariant test only. It is not the actual module execution.

## Actual numerical execution obligations

1. positive distribution manufactured cases
2. stiffness and time-step convergence
3. conservation and entropy ledger

## Required final outputs

- temperature and distribution histories
- phase/event ledger
- transport and collision operators
- entropy and conservation ledger
- uncertainty/covariance
- H_D_to_E

## Componentwise mandatory gates

- positive distributions
- energy/charge conservation
- event ordering
- stiff-solver convergence
- restart and independent reconstruction

## Hard stop conditions

- negative distributions beyond tolerance
- energy/charge drift
- event order depends on observed target values

## Claim boundary

Generated RFC thermal history, not yet primordial abundances.

## Prebuilt local execution engines

These engines execute a law already derived and frozen from admitted parents. They do **not** choose the law or its coefficients. Each configuration is created only through a provenance-complete binding sheet.

### `transport`

Integrate the frozen nonequilibrium thermal/transport state with explicit invariants.

Template: `configured_runs/templates/D_transport.template.json`  
Binding sheet: `configured_runs/binding_sheets/D_transport.bindings.json`

```bash
python tools/director.py solver-copy --module D --solver transport --destination <RUN_DIR>
# Fill every binding record with an exact value, origin path, origin SHA-256, units, dimensions, and derivation object.
python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/D_transport.template.json --binding-sheet <RUN_DIR>/binding_sheets/D_transport.bindings.json --output <RUN_DIR>/solver_configs/D_transport.json
python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/D_transport.json --output-dir <RUN_DIR>/solver_outputs/transport
```

Every `__BIND_...` token is a hard stop. The materializer verifies hashes and refuses unresolved or provenance-free values.
