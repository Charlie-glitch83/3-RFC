# Wolfram protocol

Every scientific module has two frozen, self-contained Wolfram Language programs under `recipes/<MODULE>/wolfram/`. The work model does not rewrite them before the first run.

## Exact sequence

```bash
python tools/director.py wolfram-list --module <MODULE>
python tools/director.py wolfram-show --call <CALL_ID>
```

Submit the displayed code verbatim to `WolframLanguageEvaluator`. The kernel is stateless, so every program already contains its own definitions and assumptions. Save the complete response, including warnings and messages, as `output.txt` and register it:

```bash
python tools/director.py wolfram-record \
  --run <RUN_ID> \
  --call <CALL_ID> \
  --output <OUTPUT_FILE>
```

The recorder freezes input/output hashes and applies `config/WOLFRAM_EXPECTATIONS.json` through `tools/check_wolfram_output.py`.

## Allowed uses

- exact simplification and identities;
- symbolic differential, tensor, graph, and matrix work;
- candidate-class solving under frozen assumptions;
- eigenvalues, stability, fixed points, and bifurcation conditions;
- conservation, covariance, and constraint verification;
- dimensional and unit checks using admitted definitions;
- high-precision numerical checks;
- independent reconstruction.

## Forbidden uses during generation

- Wolfram|Alpha queries for public observational or best-fit values;
- natural-language retrieval of constants not already admitted and frozen;
- choosing a candidate because it approaches a remembered target;
- changing assumptions, equations, branches, or tolerances after seeing a desired result.

A syntax-only correction must be recorded, must not change the scientific expression, and requires a full rerun. A scientific change requires a new versioned run and new pre-execution lock.

A manufactured Wolfram PASS is never a physical module result. The actual parent-bound substitution, numerical execution, countermodels, convergence, restart/replay, and independent reconstruction remain mandatory.
