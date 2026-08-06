# Module O Exact Work Order — Immutable Universe and Prediction Freeze

## Objective

Create one immutable content-addressed universe, environment, prediction, falsifier, and observation-interface packet and seal generation.

## Frozen triadic descent

- **CIF:** all generated truth and prediction objects
- **QV:** content-addressed sealing
- **RFL:** immutable universe identity
- **N-body mode:** `RELATIONAL_GRAMMAR_ACTIVE`

## Derive these objects; do not substitute familiar answers

1. canonical serialization and full artifact manifest
2. prediction/falsifier registries before reveal
3. P/Q branch isolation and replay environment

## Exact Wolfram calls

- `O-WL-001` — Canonical packet hash and mutation sensitivity
- `O-WL-002` — Generation/comparison dependency firewall

Run each through:

```bash
python tools/director.py wolfram-show --call <CALL_ID>
```

Submit the exact code to `WolframLanguageEvaluator`, save the returned output verbatim, and register it with `wolfram-record`.

## Local manufactured reference check

```bash
python tools/run_reference_checks.py --module O --output <RUN_DIR>/reference_checks.json
```

This is an implementation/invariant test only. It is not the actual module execution.

## Actual numerical execution obligations

1. clean replay and exact hashes
2. mutation test
3. firewall scan

## Required final outputs

- content-addressed universe bundle
- prediction registry
- falsifier registry
- public comparison manifest without values
- environment and replay package
- isolated P and Q branch authorizations

## Componentwise mandatory gates

- all files stopped changing before manifest
- full clean replay
- hash verification
- P and Q isolation
- no public data present

## Hard stop conditions

- N not independently reproduced
- files still changing
- public data present

## Claim boundary

Frozen generative universe and predictions.

## Prebuilt local execution engines

These engines execute a law already derived and frozen from admitted parents. They do **not** choose the law or its coefficients. Each configuration is created only through a provenance-complete binding sheet.

### `freeze_packet`

Content-address the immutable universe and prediction packet.

Template: `configured_runs/templates/O_freeze_packet.template.json`  
Binding sheet: `configured_runs/binding_sheets/O_freeze_packet.bindings.json`

```bash
python tools/director.py solver-copy --module O --solver freeze_packet --destination <RUN_DIR>
# Fill every binding record with an exact value, origin path, origin SHA-256, units, dimensions, and derivation object.
python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/O_freeze_packet.template.json --binding-sheet <RUN_DIR>/binding_sheets/O_freeze_packet.bindings.json --output <RUN_DIR>/solver_configs/O_freeze_packet.json
python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/O_freeze_packet.json --output-dir <RUN_DIR>/solver_outputs/freeze_packet
```

Every `__BIND_...` token is a hard stop. The materializer verifies hashes and refuses unresolved or provenance-free values.
