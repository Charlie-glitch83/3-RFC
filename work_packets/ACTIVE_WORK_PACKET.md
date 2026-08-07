# ACTIVE WORK PACKET — A-100

**This is the only authorized work. Execute it in order.**

- Module: `A`
- Objective: Constitute the exact prephysical RFC source law and integrate the revised N-body proof as the terminal relational completion of the kernel.
- Run workspace: `modules/A/runs/A-100-20260806T173458Z`

## Exact sequence

1. Read `recipes/A/WORK_ORDER.md` and `recipes/A/recipe.json`.
2. Verify all exact parent hashes and fill the run source register.
3. Freeze the pre-execution lock before primary execution.
4. Run these Wolfram calls exactly and record their complete outputs:

   - `python tools/director.py wolfram-show --call A-WL-001`
   - `python tools/director.py wolfram-show --call A-WL-002`

5. Run `python tools/run_reference_checks.py --module A --output modules/A/runs/A-100-20260806T173458Z/reference_checks.json`.
6. Bind and run the prebuilt local engines listed below. Every `__BIND_` token is a hard stop:

   - `python tools/director.py solver-copy --module A --solver triad_kernel --destination modules/A/runs/A-100-20260806T173458Z`
   - fill `configured_runs/binding_sheets/A_triad_kernel.bindings.json` after it is copied into the run; every value requires an origin SHA-256
   - `python tools/materialize_solver_config.py --template modules/A/runs/A-100-20260806T173458Z/solver_templates/A_triad_kernel.template.json --binding-sheet modules/A/runs/A-100-20260806T173458Z/binding_sheets/A_triad_kernel.bindings.json --output modules/A/runs/A-100-20260806T173458Z/solver_configs/A_triad_kernel.json`
   - `python tools/run_configured_solver.py --config modules/A/runs/A-100-20260806T173458Z/solver_configs/A_triad_kernel.json --output-dir modules/A/runs/A-100-20260806T173458Z/solver_outputs/triad_kernel`

7. Execute any remaining parent-driven domain code named in the recipe. Manufactured checks and generic engines do not replace the physical result.
8. Run countermodels, ablations, convergence, restart, replay, uncertainty/covariance, and independent reconstruction.
9. Finalize manifests only after outputs stop changing. State strongest supported and unsupported claims.
10. Commit and verify the exact GitHub SHA/diff before advancing.

## Required deliverables

- modules/A/runs/<RUN_ID>/RUN_PLAN.md
- modules/A/runs/<RUN_ID>/SOURCE_REGISTER.json
- modules/A/runs/<RUN_ID>/GATE_RESULTS.json
- modules/A/runs/<RUN_ID>/INDEPENDENT_VERIFICATION.md
- modules/A/runs/<RUN_ID>/CLOSEOUT.md
- frozen output packet and artifact registry entries

## Componentwise gates

- canonical terminology exact
- no physical time, geometry, constants, or later-module objects assumed
- triad ablations fail as predeclared
- scalar collapse countermodel rejected
- lane increment 2N verified
- new-solution claim requires non-gauge witnessed closure
- dormant direct dynamics has zero backreaction
- independent symbolic reconstruction

## Commit message

`Close Module A at its verified scientific scope`
