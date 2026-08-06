# Deterministic Work Queue

The executable authority is `WORK_QUEUE.json`. Run:

```bash
bash tools/start_work.sh
```

The director returns the one active unit and installs its exact work packet into the active run. Do not create a parallel plan.

## Prebuilt administrative work packs

The non-module phases are fully specified under `work_units/` and registered in `config/WORK_UNIT_PACKS.json`:

```text
BOOT-000      install and GitHub-visible scaffold verification
SRC-010       exact source hashing and admission
AUTH-020      canonical authority, terminology, and claim lock
XWALK-030     Presentation 29 / N-body / Presentation 30 enhancement crosswalk
REC-040       exact-object recovery from prior RFC work
FRONTIER-050  earliest missing physical-parent audit
HR-255        hyper-realistic and Gold Standard expansion
FINAL-290     clean reconstruction and final claim audit
```

Each pack fixes the sequence, commands, outputs, gates, hard stops, and commit message. `tools/director.py prepare-active` copies the active pack into its run workspace.

## Prebuilt scientific module packs

The module queue executes A, B, C, D, E, F, G, H^U, I, H[I], J, K, L, M, K-L-M, N, O, P, and Q. Every module has:

- a frozen recipe and work order;
- two exact Wolfram programs;
- provenance-bound local solver templates;
- manufactured implementation checks;
- componentwise scientific gates;
- restart, replay, convergence, covariance, countermodel, and independent-verification obligations.

## Hyper-realism expansion

`work_units/HR-255/EXECUTION_MATRIX.json` contains twenty mandatory rows covering the complete planned fidelity expansion. Each row fixes its truth outputs, synthetic-observation outputs, numerical matrix, independent-verification duty, and hard stop. A row cannot be closed with prose or a readiness score.

## End condition

The queue ends only after the frozen universe, isolated empirical comparison, isolated terminal continuation, and clean reconstruction all pass their exact gates. A failed or obstructed scientific result is recorded honestly; the controller does not force a preferred universe outcome.
