# ACTIVE WORK PACKET — D-135

**This is the only authorized work. Execute it in order.**

- Module: `D`
- Objective: Execute the recovered nonequilibrium chronology from H_C_to_D_v2, including asymmetry, annihilation/freeze-out/decoupling and photon/neutrino transport.
- Run workspace: `modules/D/runs/D-135-20260808T163243Z`

## Exact sequence

1. Read `recipes/D/WORK_ORDER.md` and `recipes/D/recipe.json`.
2. Verify all exact parent hashes and fill the run source register.
3. Freeze the pre-execution lock before primary execution.
4. Run these Wolfram calls exactly and record their complete outputs:

   - `python tools/director.py wolfram-show --call D-WL-001`
   - `python tools/director.py wolfram-show --call D-WL-002`

5. Run `python tools/run_reference_checks.py --module D --output modules/D/runs/D-135-20260808T163243Z/reference_checks.json`.
6. Bind and run the prebuilt local engines listed below. Every `__BIND_` token is a hard stop:

   - `python tools/director.py solver-copy --module D --solver transport --destination modules/D/runs/D-135-20260808T163243Z`
   - fill `configured_runs/binding_sheets/D_transport.bindings.json` after it is copied into the run; every value requires an origin SHA-256
   - `python tools/materialize_solver_config.py --template modules/D/runs/D-135-20260808T163243Z/solver_templates/D_transport.template.json --binding-sheet modules/D/runs/D-135-20260808T163243Z/binding_sheets/D_transport.bindings.json --output modules/D/runs/D-135-20260808T163243Z/solver_configs/D_transport.json`
   - `python tools/run_configured_solver.py --config modules/D/runs/D-135-20260808T163243Z/solver_configs/D_transport.json --output-dir modules/D/runs/D-135-20260808T163243Z/solver_outputs/transport`

7. Execute any remaining parent-driven domain code named in the recipe. Manufactured checks and generic engines do not replace the physical result.
8. Run countermodels, ablations, convergence, restart, replay, uncertainty/covariance, and independent reconstruction.
9. Finalize manifests only after outputs stop changing. State strongest supported and unsupported claims.
10. Commit and verify the exact GitHub SHA/diff before advancing.

## Required deliverables

- modules/D/runs/<RUN_ID>/OUTPUT_CONTRACT.json
- modules/D/runs/<RUN_ID>/SOURCE_REGISTER.json
- modules/D/runs/<RUN_ID>/GATE_RESULTS.json
- modules/D/runs/<RUN_ID>/INDEPENDENT_VERIFICATION.md
- modules/D/runs/<RUN_ID>/CLOSEOUT.md
- versioned superseding H_D_to_E_v2 handoff and manifest

## Componentwise gates

- all module-spec required outputs SATISFIED
- all configured child bindings SATISFIED
- exact source/parent lineage
- no public-data generation leakage
- semantic countermodels
- convergence, covariance, restart/replay and independent reconstruction

## Commit message

`Close D-135 superseding D replay at verified scope`
