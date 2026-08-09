# ACTIVE WORK PACKET — I-180

**This is the only authorized work. Execute it in order.**

- Module: `I`
- Objective: Generate the universe's realized geometry, expansion, clocks, horizons, and distance structure from the accumulated physical state.
- Run workspace: `modules/I/runs/I-180-20260809T050839Z`

## Exact sequence

1. Read `recipes/I/WORK_ORDER.md` and `recipes/I/recipe.json`.
2. Verify all exact parent hashes and fill the run source register.
3. Freeze the pre-execution lock before primary execution.
4. Run these Wolfram calls exactly and record their complete outputs:

   - `python tools/director.py wolfram-show --call I-WL-001`
   - `python tools/director.py wolfram-show --call I-WL-002`

5. Run `python tools/run_reference_checks.py --module I --output modules/I/runs/I-180-20260809T050839Z/reference_checks.json`.
6. Bind and run the prebuilt local engines listed below. Every `__BIND_` token is a hard stop:

   - `python tools/director.py solver-copy --module I --solver transport --destination modules/I/runs/I-180-20260809T050839Z`
   - fill `configured_runs/binding_sheets/I_background_ode.bindings.json` after it is copied into the run; every value requires an origin SHA-256
   - `python tools/materialize_solver_config.py --template modules/I/runs/I-180-20260809T050839Z/solver_templates/I_background_ode.template.json --binding-sheet modules/I/runs/I-180-20260809T050839Z/binding_sheets/I_background_ode.bindings.json --output modules/I/runs/I-180-20260809T050839Z/solver_configs/I_background_ode.json`
   - `python tools/run_configured_solver.py --config modules/I/runs/I-180-20260809T050839Z/solver_configs/I_background_ode.json --output-dir modules/I/runs/I-180-20260809T050839Z/solver_outputs/transport`

7. Execute any remaining parent-driven domain code named in the recipe. Manufactured checks and generic engines do not replace the physical result.
8. Run countermodels, ablations, convergence, restart, replay, uncertainty/covariance, and independent reconstruction.
9. Finalize manifests only after outputs stop changing. State strongest supported and unsupported claims.
10. Commit and verify the exact GitHub SHA/diff before advancing.

## Required deliverables

- modules/I/runs/<RUN_ID>/RUN_PLAN.md
- modules/I/runs/<RUN_ID>/SOURCE_REGISTER.json
- modules/I/runs/<RUN_ID>/GATE_RESULTS.json
- modules/I/runs/<RUN_ID>/INDEPENDENT_VERIFICATION.md
- modules/I/runs/<RUN_ID>/CLOSEOUT.md
- frozen output packet and artifact registry entries

## Componentwise gates

- equation/constraint derivation
- gauge/frame consistency
- no observed expansion history used as target
- numerical convergence and independent reconstruction

## Commit message

`Close Module I at its verified scientific scope`
