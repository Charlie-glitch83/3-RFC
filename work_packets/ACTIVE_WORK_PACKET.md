# ACTIVE WORK PACKET — HU-170

**This is the only authorized work. Execute it in order.**

- Module: `HU`
- Objective: Derive and freeze the background-independent portion of the linear transfer machinery before instantiation on a realized geometry.
- Run workspace: `modules/HU/runs/HU-170-20260809T045528Z`

## Exact sequence

1. Read `recipes/HU/WORK_ORDER.md` and `recipes/HU/recipe.json`.
2. Verify all exact parent hashes and fill the run source register.
3. Freeze the pre-execution lock before primary execution.
4. Run these Wolfram calls exactly and record their complete outputs:

   - `python tools/director.py wolfram-show --call HU-WL-001`
   - `python tools/director.py wolfram-show --call HU-WL-002`

5. Run `python tools/run_reference_checks.py --module HU --output modules/HU/runs/HU-170-20260809T045528Z/reference_checks.json`.
6. Bind and run the prebuilt local engines listed below. Every `__BIND_` token is a hard stop:

   - `python tools/director.py solver-copy --module HU --solver linear_transfer --destination modules/HU/runs/HU-170-20260809T045528Z`
   - fill `configured_runs/binding_sheets/HU_linear_transfer.bindings.json` after it is copied into the run; every value requires an origin SHA-256
   - `python tools/materialize_solver_config.py --template modules/HU/runs/HU-170-20260809T045528Z/solver_templates/HU_linear_transfer.template.json --binding-sheet modules/HU/runs/HU-170-20260809T045528Z/binding_sheets/HU_linear_transfer.bindings.json --output modules/HU/runs/HU-170-20260809T045528Z/solver_configs/HU_linear_transfer.json`
   - `python tools/run_configured_solver.py --config modules/HU/runs/HU-170-20260809T045528Z/solver_configs/HU_linear_transfer.json --output-dir modules/HU/runs/HU-170-20260809T045528Z/solver_outputs/linear_transfer`

7. Execute any remaining parent-driven domain code named in the recipe. Manufactured checks and generic engines do not replace the physical result.
8. Run countermodels, ablations, convergence, restart, replay, uncertainty/covariance, and independent reconstruction.
9. Finalize manifests only after outputs stop changing. State strongest supported and unsupported claims.
10. Commit and verify the exact GitHub SHA/diff before advancing.

## Required deliverables

- modules/HU/runs/<RUN_ID>/RUN_PLAN.md
- modules/HU/runs/<RUN_ID>/SOURCE_REGISTER.json
- modules/HU/runs/<RUN_ID>/GATE_RESULTS.json
- modules/HU/runs/<RUN_ID>/INDEPENDENT_VERIFICATION.md
- modules/HU/runs/<RUN_ID>/CLOSEOUT.md
- frozen output packet and artifact registry entries

## Componentwise gates

- no realized-background values smuggled into universal operator
- linearity-domain proof
- symbolic identity verification
- hash freeze

## Commit message

`Close Module HU at its verified scientific scope`
