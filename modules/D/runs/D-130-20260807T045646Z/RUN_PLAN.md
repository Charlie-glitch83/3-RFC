# Run Plan — D-130

PRE-CHEWED MODULE PLAN

Objective: Evolve the microscopic state through nonequilibrium thermodynamics, transport, phase changes, entropy production, and clock/frame-consistent expansion.

The exact derivation obligations, calls, outputs, gates, and stop conditions are frozen in `FROZEN_RECIPE.json`, `WORK_ORDER.md`, and `REQUIRED_GATES.json`.

Before execution, replace every placeholder in the source register, pre-execution lock, environment, expected outcomes, tolerances, falsifiers, and claim boundary with exact frozen values.

## Frozen numerical execution controls

- Intrinsic interval: `s in [0,1]` (one normalized e-fold; not physical time)
- Primary max step: `1/16`
- Convergence matrix: `1/4, 1/8, 1/16, 1/32`
- Restart split: `s=1/2`
- These were frozen before Wolfram/numerical execution and may not be retuned.
