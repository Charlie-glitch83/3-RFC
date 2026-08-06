# Module Q Exact Work Order — Terminal Evolution, Qualified Memory, and Next-Cycle Conditioning

## Objective

Continue the frozen universe physically to terminal evolution, classify collapse/rebirth behavior, and derive the qualified memory packet for a possible next effective CIF without information from P.

## Frozen triadic descent

- **CIF:** terminal physical possibilities from O
- **QV:** collapse/continuation/rebirth dynamics
- **RFL:** qualified memory and next-cycle condition
- **N-body mode:** `RELATIONAL_GRAMMAR_ACTIVE`

## Derive these objects; do not substitute familiar answers

1. terminal evolution law from frozen O only
2. collapse/rebirth event and branch ledger
3. qualified memory M_rec with no-loss and source distinction
4. next-cycle conditions, branch family, obstruction or nonconvergence

## Exact Wolfram calls

- `Q-WL-001` — Terminal affine recurrence and fixed-point classification
- `Q-WL-002` — Qualified memory is not the source role

Run each through:

```bash
python tools/director.py wolfram-show --call <CALL_ID>
```

Submit the exact code to `WolframLanguageEvaluator`, save the returned output verbatim, and register it with `wolfram-record`.

## Local manufactured reference check

```bash
python tools/run_reference_checks.py --module Q --output <RUN_DIR>/reference_checks.json
```

This is an implementation/invariant test only. It is not the actual module execution.

## Actual numerical execution obligations

1. terminal convergence/branch exploration
2. memory reopening and conservation
3. independent recurrence classification

## Required final outputs

- terminal physical trajectory
- collapse/rebirth event and branch ledger
- qualified memory packet M_rec
- next-cycle source conditions or obstruction
- independent recurrence classification

## Componentwise mandatory gates

- no P data flow
- conservation and no-loss
- terminal numerical convergence
- memory does not impersonate source
- independent reconstruction

## Hard stop conditions

- P data are read
- RFL memory is equated with next CIF
- rebirth is forced

## Claim boundary

Terminal RFC continuation and next-cycle conditioning at executed scope.

## Prebuilt local execution engines

These engines execute a law already derived and frozen from admitted parents. They do **not** choose the law or its coefficients. Each configuration is created only through a provenance-complete binding sheet.

### `affine_recurrence`

Classify isolated terminal evolution and next-cycle conditioning.

Template: `configured_runs/templates/Q_terminal_recurrence.template.json`  
Binding sheet: `configured_runs/binding_sheets/Q_terminal_recurrence.bindings.json`

```bash
python tools/director.py solver-copy --module Q --solver affine_recurrence --destination <RUN_DIR>
# Fill every binding record with an exact value, origin path, origin SHA-256, units, dimensions, and derivation object.
python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/Q_terminal_recurrence.template.json --binding-sheet <RUN_DIR>/binding_sheets/Q_terminal_recurrence.bindings.json --output <RUN_DIR>/solver_configs/Q_terminal_recurrence.json
python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/Q_terminal_recurrence.json --output-dir <RUN_DIR>/solver_outputs/affine_recurrence
```

Every `__BIND_...` token is a hard stop. The materializer verifies hashes and refuses unresolved or provenance-free values.
