# Zero-design operator protocol

A future work model must not redesign the project. The repository already supplies the architecture, active queue, module recipe, symbolic calls, binding sheets, numerical engines, output contracts, gates, and evidence transitions.

## Session start

Run one command:

```bash
bash tools/start_work.sh
```

Then open only:

```text
work_packets/ACTIVE_WORK_PACKET.md
```

## Module execution

For an active scientific module:

1. The director creates the run workspace and copies the frozen recipe, work order, gates, Wolfram programs, unbound solver templates, and binding sheets.
2. Fill each binding sheet from exact admitted sources, exact parent artifacts, or a hashed internal derivation. Do not type values directly into solver configs.
3. Materialize each solver config with `tools/materialize_solver_config.py`. It refuses missing hashes and unresolved values.
4. Submit the listed Wolfram programs verbatim. Save outputs verbatim and register them with `director.py wolfram-record`.
5. Run the complete local solver phase:

```bash
bash tools/finish_local_phase.sh <MODULE> <RUN_DIR>
```

6. Execute the module-specific convergence matrix, countermodels, ablations, restart, replay, uncertainty/covariance propagation, and independent reconstruction named in the recipe.
7. Finalize manifests only after files stop changing. Close the run and promote evidence only through repository tools.
8. Commit and verify the exact GitHub SHA and diff before advancing.

## What the model is still allowed to reason about

Reasoning is required only where the admitted triad, exact parent state, and frozen module obligations require a new derivation. The model must produce that derivation as a hashed object. It may not choose a familiar equation or value merely because it resembles standard physics or fixes an old mismatch.

When the premises admit several lawful outcomes, preserve a branch family. When they admit none, record an obstruction. When they underdetermine a coefficient, stop at `BLOCKED_UNDERDETERMINED`; never insert a remembered best-fit value.
