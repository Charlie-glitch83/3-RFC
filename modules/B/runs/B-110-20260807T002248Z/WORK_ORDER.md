# Module B Exact Work Order — Big Implosion and First Physical State

## Objective

Execute the sole first physical event from the exact prephysical parent and generate the first restartable physical RFC state.

## Frozen triadic descent

- **CIF:** exact prephysical A modes
- **QV:** Big Implosion compression/crossing
- **RFL:** first physical carrier, event and memory
- **N-body mode:** `RELATIONAL_GRAMMAR_ACTIVE`

## Derive these objects; do not substitute familiar answers

1. Big Implosion candidate from exact A carrier and graph/relational operator
2. proof that physical time is absent before the event and intrinsic ordering begins at it
3. compression, conservation, sector ownership, uncertainty and branch laws
4. restartable first physical state and no-loss reopening map

## Exact Wolfram calls

- `B-WL-001` — Spectral audit of the Big Implosion compression operator
- `B-WL-002` — No-loss reopening and strict nontrivial-mode compression

Run each through:

```bash
python tools/director.py wolfram-show --call <CALL_ID>
```

Submit the exact code to `WolframLanguageEvaluator`, save the returned output verbatim, and register it with `wolfram-record`.

## Local manufactured reference check

```bash
python tools/run_reference_checks.py --module B --output <RUN_DIR>/reference_checks.json
```

This is an implementation/invariant test only. It is not the actual module execution.

## Actual numerical execution obligations

1. execute multiple graph sizes and nontrivial modes
2. check spectral compression, conserved carrier mode, restart and exact reopening
3. ablate compression and relational coupling

## Required final outputs

- physically executed Big Implosion state
- intrinsic physical event order and clock origin
- generated geometry or explicitly typed pregeometry
- field/current/conservation-bearing state
- ordinary, radiative, compression-relic, and dissipative-tail sector seeds only where derived
- route, event, branch, memory, uncertainty, and no-loss ancestry
- restartable H_B_to_C

## Componentwise mandatory gates

- no pre-event physical time
- exact parent bytes
- strict nontrivial compression or derived equivalent
- total ledger preservation
- no-loss reopening
- no later physics smuggled into B
- ablation, replay, restart, and independent reconstruction

## Hard stop conditions

- a physical clock or geometry is assumed in the A parent
- later-module particles/constants are inserted
- compression is trivial or ledger is not conserved

## Claim boundary

First physical RFC state at declared fidelity; no microscopic or cosmological late-time completion.

## Prebuilt local execution engines

These engines execute a law already derived and frozen from admitted parents. They do **not** choose the law or its coefficients. Each configuration is created only through a provenance-complete binding sheet.

### `big_implosion`

Execute the frozen Big Implosion compression operator on the exact A parent.

Template: `configured_runs/templates/B_big_implosion.template.json`  
Binding sheet: `configured_runs/binding_sheets/B_big_implosion.bindings.json`

```bash
python tools/director.py solver-copy --module B --solver big_implosion --destination <RUN_DIR>
# Fill every binding record with an exact value, origin path, origin SHA-256, units, dimensions, and derivation object.
python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/B_big_implosion.template.json --binding-sheet <RUN_DIR>/binding_sheets/B_big_implosion.bindings.json --output <RUN_DIR>/solver_configs/B_big_implosion.json
python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/B_big_implosion.json --output-dir <RUN_DIR>/solver_outputs/big_implosion
```

Every `__BIND_...` token is a hard stop. The materializer verifies hashes and refuses unresolved or provenance-free values.
