# ACTIVE WORK PACKET — C-120

**This is the only authorized work. Execute it in order.**

- Module: `C`
- Objective: Derive and execute the microscopic field, particle, interaction, mass, mixing, and prethermal population content from the first physical state.
- Run workspace: `modules/C/runs/C-120-20260807T032543Z`

## Exact sequence

1. Read `recipes/C/WORK_ORDER.md` and `recipes/C/recipe.json`.
2. Verify all exact parent hashes and fill the run source register.
3. Freeze the pre-execution lock before primary execution.
4. Run these Wolfram calls exactly and record their complete outputs:

   - `python tools/director.py wolfram-show --call C-WL-001`
   - `python tools/director.py wolfram-show --call C-WL-002`

5. Run `python tools/run_reference_checks.py --module C --output modules/C/runs/C-120-20260807T032543Z/reference_checks.json`.
6. Bind and run the prebuilt local engines listed below. Every `__BIND_` token is a hard stop:

   - `python tools/director.py solver-copy --module C --solver spectral_model --destination modules/C/runs/C-120-20260807T032543Z`
   - fill `configured_runs/binding_sheets/C_spectral_model.bindings.json` after it is copied into the run; every value requires an origin SHA-256
   - `python tools/materialize_solver_config.py --template modules/C/runs/C-120-20260807T032543Z/solver_templates/C_spectral_model.template.json --binding-sheet modules/C/runs/C-120-20260807T032543Z/binding_sheets/C_spectral_model.bindings.json --output modules/C/runs/C-120-20260807T032543Z/solver_configs/C_spectral_model.json`
   - `python tools/run_configured_solver.py --config modules/C/runs/C-120-20260807T032543Z/solver_configs/C_spectral_model.json --output-dir modules/C/runs/C-120-20260807T032543Z/solver_outputs/spectral_model`

7. Execute any remaining parent-driven domain code named in the recipe. Manufactured checks and generic engines do not replace the physical result.
8. Run countermodels, ablations, convergence, restart, replay, uncertainty/covariance, and independent reconstruction.
9. Finalize manifests only after outputs stop changing. State strongest supported and unsupported claims.
10. Commit and verify the exact GitHub SHA/diff before advancing.

## Required deliverables

- modules/C/runs/<RUN_ID>/RUN_PLAN.md
- modules/C/runs/<RUN_ID>/SOURCE_REGISTER.json
- modules/C/runs/<RUN_ID>/GATE_RESULTS.json
- modules/C/runs/<RUN_ID>/INDEPENDENT_VERIFICATION.md
- modules/C/runs/<RUN_ID>/CLOSEOUT.md
- frozen output packet and artifact registry entries

## Componentwise gates

- units and dimensions
- symmetry/constraint closure
- positivity/unitarity or declared alternative
- no Standard Model label without derivation or correspondence theorem
- independent symbolic and numerical checks

## Commit message

`Close Module C at its verified scientific scope`
