# ACTIVE WORK PACKET — B-110

**This is the only authorized work. Execute it in order.**

- Module: `B`
- Objective: Execute the sole first physical event from the exact prephysical parent and generate the first restartable physical RFC state.
- Run workspace: `modules/B/runs/B-110-20260807T002248Z`

## Exact sequence

1. Read `recipes/B/WORK_ORDER.md` and `recipes/B/recipe.json`.
2. Verify all exact parent hashes and fill the run source register.
3. Freeze the pre-execution lock before primary execution.
4. Run these Wolfram calls exactly and record their complete outputs:

   - `python tools/director.py wolfram-show --call B-WL-001`
   - `python tools/director.py wolfram-show --call B-WL-002`

5. Run `python tools/run_reference_checks.py --module B --output modules/B/runs/B-110-20260807T002248Z/reference_checks.json`.
6. Bind and run the prebuilt local engines listed below. Every `__BIND_` token is a hard stop:

   - `python tools/director.py solver-copy --module B --solver big_implosion --destination modules/B/runs/B-110-20260807T002248Z`
   - fill `configured_runs/binding_sheets/B_big_implosion.bindings.json` after it is copied into the run; every value requires an origin SHA-256
   - `python tools/materialize_solver_config.py --template modules/B/runs/B-110-20260807T002248Z/solver_templates/B_big_implosion.template.json --binding-sheet modules/B/runs/B-110-20260807T002248Z/binding_sheets/B_big_implosion.bindings.json --output modules/B/runs/B-110-20260807T002248Z/solver_configs/B_big_implosion.json`
   - `python tools/run_configured_solver.py --config modules/B/runs/B-110-20260807T002248Z/solver_configs/B_big_implosion.json --output-dir modules/B/runs/B-110-20260807T002248Z/solver_outputs/big_implosion`

7. Execute any remaining parent-driven domain code named in the recipe. Manufactured checks and generic engines do not replace the physical result.
8. Run countermodels, ablations, convergence, restart, replay, uncertainty/covariance, and independent reconstruction.
9. Finalize manifests only after outputs stop changing. State strongest supported and unsupported claims.
10. Commit and verify the exact GitHub SHA/diff before advancing.

## Required deliverables

- modules/B/runs/<RUN_ID>/RUN_PLAN.md
- modules/B/runs/<RUN_ID>/SOURCE_REGISTER.json
- modules/B/runs/<RUN_ID>/GATE_RESULTS.json
- modules/B/runs/<RUN_ID>/INDEPENDENT_VERIFICATION.md
- modules/B/runs/<RUN_ID>/CLOSEOUT.md
- frozen output packet and artifact registry entries

## Componentwise gates

- no pre-event physical time
- exact parent bytes
- strict nontrivial compression or derived equivalent
- total ledger preservation
- no-loss reopening
- no later physics smuggled into B
- ablation, replay, restart, and independent reconstruction

## Commit message

`Close Module B at its verified scientific scope`
