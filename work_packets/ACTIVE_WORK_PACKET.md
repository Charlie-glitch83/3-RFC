# ACTIVE WORK PACKET — E-145

**This is the only authorized work. Execute it in order.**

- Module: `E`
- Objective: Execute the recovered source-owned nuclear network with isotope identities, rates, abundances, covariance and plasma-ready output.
- Run workspace: `modules/E/runs/E-145-20260808T164410Z`

## Exact sequence

1. Read `recipes/E/WORK_ORDER.md` and `recipes/E/recipe.json`.
2. Verify all exact parent hashes and fill the run source register.
3. Freeze the pre-execution lock before primary execution.
4. Run these Wolfram calls exactly and record their complete outputs:

   - `python tools/director.py wolfram-show --call E-WL-001`
   - `python tools/director.py wolfram-show --call E-WL-002`

5. Run `python tools/run_reference_checks.py --module E --output modules/E/runs/E-145-20260808T164410Z/reference_checks.json`.
6. Bind and run the prebuilt local engines listed below. Every `__BIND_` token is a hard stop:

   - `python tools/director.py solver-copy --module E --solver reaction_network --destination modules/E/runs/E-145-20260808T164410Z`
   - fill `configured_runs/binding_sheets/E_reaction_network.bindings.json` after it is copied into the run; every value requires an origin SHA-256
   - `python tools/materialize_solver_config.py --template modules/E/runs/E-145-20260808T164410Z/solver_templates/E_reaction_network.template.json --binding-sheet modules/E/runs/E-145-20260808T164410Z/binding_sheets/E_reaction_network.bindings.json --output modules/E/runs/E-145-20260808T164410Z/solver_configs/E_reaction_network.json`
   - `python tools/run_configured_solver.py --config modules/E/runs/E-145-20260808T164410Z/solver_configs/E_reaction_network.json --output-dir modules/E/runs/E-145-20260808T164410Z/solver_outputs/reaction_network`

7. Execute any remaining parent-driven domain code named in the recipe. Manufactured checks and generic engines do not replace the physical result.
8. Run countermodels, ablations, convergence, restart, replay, uncertainty/covariance, and independent reconstruction.
9. Finalize manifests only after outputs stop changing. State strongest supported and unsupported claims.
10. Commit and verify the exact GitHub SHA/diff before advancing.

## Required deliverables

- modules/E/runs/<RUN_ID>/OUTPUT_CONTRACT.json
- modules/E/runs/<RUN_ID>/SOURCE_REGISTER.json
- modules/E/runs/<RUN_ID>/GATE_RESULTS.json
- modules/E/runs/<RUN_ID>/INDEPENDENT_VERIFICATION.md
- modules/E/runs/<RUN_ID>/CLOSEOUT.md
- versioned superseding H_E_to_F_v2 handoff and manifest

## Componentwise gates

- all module-spec required outputs SATISFIED
- all configured child bindings SATISFIED
- exact source/parent lineage
- no public-data generation leakage
- semantic countermodels
- convergence, covariance, restart/replay and independent reconstruction

## Commit message

`Close E-145 superseding E replay at verified scope`
