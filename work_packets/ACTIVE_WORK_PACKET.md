# ACTIVE WORK PACKET — J-200

**This is the only authorized work. Execute it in order.**

- Module: `J`
- Objective: Generate the actual covariance, linear spectra, phases/seeds, and finite-volume field realization consumed by nonlinear gravity.
- Run workspace: `modules/J/runs/J-200-20260810T200114Z`

## Exact sequence

1. Read `recipes/J/WORK_ORDER.md` and `recipes/J/recipe.json`.
2. Verify all exact parent hashes and fill the run source register.
3. Freeze the pre-execution lock before primary execution.
4. Run these Wolfram calls exactly and record their complete outputs:

   - `python tools/director.py wolfram-show --call J-WL-001`
   - `python tools/director.py wolfram-show --call J-WL-002`

5. Run `python tools/run_reference_checks.py --module J --output modules/J/runs/J-200-20260810T200114Z/reference_checks.json`.
6. Bind and run the prebuilt local engines listed below. Every `__BIND_` token is a hard stop:

   - `python tools/director.py solver-copy --module J --solver covariance --destination modules/J/runs/J-200-20260810T200114Z`
   - fill `configured_runs/binding_sheets/J_covariance.bindings.json` after it is copied into the run; every value requires an origin SHA-256
   - `python tools/materialize_solver_config.py --template modules/J/runs/J-200-20260810T200114Z/solver_templates/J_covariance.template.json --binding-sheet modules/J/runs/J-200-20260810T200114Z/binding_sheets/J_covariance.bindings.json --output modules/J/runs/J-200-20260810T200114Z/solver_configs/J_covariance.json`
   - `python tools/run_configured_solver.py --config modules/J/runs/J-200-20260810T200114Z/solver_configs/J_covariance.json --output-dir modules/J/runs/J-200-20260810T200114Z/solver_outputs/covariance`
   - `python tools/director.py solver-copy --module J --solver fourier_field --destination modules/J/runs/J-200-20260810T200114Z`
   - fill `configured_runs/binding_sheets/J_fourier_field.bindings.json` after it is copied into the run; every value requires an origin SHA-256
   - `python tools/materialize_solver_config.py --template modules/J/runs/J-200-20260810T200114Z/solver_templates/J_fourier_field.template.json --binding-sheet modules/J/runs/J-200-20260810T200114Z/binding_sheets/J_fourier_field.bindings.json --output modules/J/runs/J-200-20260810T200114Z/solver_configs/J_fourier_field.json`
   - `python tools/run_configured_solver.py --config modules/J/runs/J-200-20260810T200114Z/solver_configs/J_fourier_field.json --output-dir modules/J/runs/J-200-20260810T200114Z/solver_outputs/fourier_field`

7. Execute any remaining parent-driven domain code named in the recipe. Manufactured checks and generic engines do not replace the physical result.
8. Run countermodels, ablations, convergence, restart, replay, uncertainty/covariance, and independent reconstruction.
9. Finalize manifests only after outputs stop changing. State strongest supported and unsupported claims.
10. Commit and verify the exact GitHub SHA/diff before advancing.

## Required deliverables

- modules/J/runs/<RUN_ID>/RUN_PLAN.md
- modules/J/runs/<RUN_ID>/SOURCE_REGISTER.json
- modules/J/runs/<RUN_ID>/GATE_RESULTS.json
- modules/J/runs/<RUN_ID>/INDEPENDENT_VERIFICATION.md
- modules/J/runs/<RUN_ID>/CLOSEOUT.md
- frozen output packet and artifact registry entries

## Componentwise gates

- covariance PSD
- reality/Hermitian conditions
- resolution and volume tests
- no public initial-condition file
- independent field reconstruction

## Commit message

`Close Module J at its verified scientific scope`
