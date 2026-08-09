# ACTIVE WORK PACKET — HI-190

**This is the only authorized work. Execute it in order.**

- Module: `HI`
- Objective: Instantiate the frozen universal transfer operator on the realized background without changing either parent's law.
- Run workspace: `modules/HI/runs/HI-190-20260809T221124Z`

## Exact sequence

1. Read `recipes/HI/WORK_ORDER.md` and `recipes/HI/recipe.json`.
2. Verify all exact parent hashes and fill the run source register.
3. Freeze the pre-execution lock before primary execution.
4. Run these Wolfram calls exactly and record their complete outputs:

   - `python tools/director.py wolfram-show --call HI-WL-001`
   - `python tools/director.py wolfram-show --call HI-WL-002`

5. Run `python tools/run_reference_checks.py --module HI --output modules/HI/runs/HI-190-20260809T221124Z/reference_checks.json`.
6. Bind and run the prebuilt local engines listed below. Every `__BIND_` token is a hard stop:

   - `python tools/director.py solver-copy --module HI --solver linear_transfer --destination modules/HI/runs/HI-190-20260809T221124Z`
   - fill `configured_runs/binding_sheets/HI_instantiated_transfer.bindings.json` after it is copied into the run; every value requires an origin SHA-256
   - `python tools/materialize_solver_config.py --template modules/HI/runs/HI-190-20260809T221124Z/solver_templates/HI_instantiated_transfer.template.json --binding-sheet modules/HI/runs/HI-190-20260809T221124Z/binding_sheets/HI_instantiated_transfer.bindings.json --output modules/HI/runs/HI-190-20260809T221124Z/solver_configs/HI_instantiated_transfer.json`
   - `python tools/run_configured_solver.py --config modules/HI/runs/HI-190-20260809T221124Z/solver_configs/HI_instantiated_transfer.json --output-dir modules/HI/runs/HI-190-20260809T221124Z/solver_outputs/linear_transfer`

7. Execute any remaining parent-driven domain code named in the recipe. Manufactured checks and generic engines do not replace the physical result.
8. Run countermodels, ablations, convergence, restart, replay, uncertainty/covariance, and independent reconstruction.
9. Finalize manifests only after outputs stop changing. State strongest supported and unsupported claims.
10. Commit and verify the exact GitHub SHA/diff before advancing.

## Required deliverables

- modules/HI/runs/<RUN_ID>/RUN_PLAN.md
- modules/HI/runs/<RUN_ID>/SOURCE_REGISTER.json
- modules/HI/runs/<RUN_ID>/GATE_RESULTS.json
- modules/HI/runs/<RUN_ID>/INDEPENDENT_VERIFICATION.md
- modules/HI/runs/<RUN_ID>/CLOSEOUT.md
- frozen output packet and artifact registry entries

## Componentwise gates

- exact parent hashes
- no retune of HU or I
- operator-domain compatibility
- independent reconstruction

## Commit message

`Close Module HI at its verified scientific scope`
