# ACTIVE WORK PACKET — D-130

**This is the only authorized work. Execute it in order.**

- Module: `D`
- Objective: Evolve the microscopic state through nonequilibrium thermodynamics, transport, phase changes, entropy production, and clock/frame-consistent expansion.
- Run workspace: `modules/D/runs/D-130-20260807T053432Z`

## Exact sequence

1. Read `recipes/D/WORK_ORDER.md` and `recipes/D/recipe.json`.
2. Verify all exact parent hashes and fill the run source register.
3. Freeze the pre-execution lock before primary execution.
4. Run these Wolfram calls exactly and record their complete outputs:

   - `python tools/director.py wolfram-show --call D-WL-001`
   - `python tools/director.py wolfram-show --call D-WL-002`

5. Run `python tools/run_reference_checks.py --module D --output modules/D/runs/D-130-20260807T053432Z/reference_checks.json`.
6. Bind and run the prebuilt local engines listed below. Every `__BIND_` token is a hard stop:

   - `python tools/director.py solver-copy --module D --solver transport --destination modules/D/runs/D-130-20260807T053432Z`
   - fill `configured_runs/binding_sheets/D_transport.bindings.json` after it is copied into the run; every value requires an origin SHA-256
   - `python tools/materialize_solver_config.py --template modules/D/runs/D-130-20260807T053432Z/solver_templates/D_transport.template.json --binding-sheet modules/D/runs/D-130-20260807T053432Z/binding_sheets/D_transport.bindings.json --output modules/D/runs/D-130-20260807T053432Z/solver_configs/D_transport.json`
   - `python tools/run_configured_solver.py --config modules/D/runs/D-130-20260807T053432Z/solver_configs/D_transport.json --output-dir modules/D/runs/D-130-20260807T053432Z/solver_outputs/transport`

7. Execute any remaining parent-driven domain code named in the recipe. Manufactured checks and generic engines do not replace the physical result.
8. Run countermodels, ablations, convergence, restart, replay, uncertainty/covariance, and independent reconstruction.
9. Finalize manifests only after outputs stop changing. State strongest supported and unsupported claims.
10. Commit and verify the exact GitHub SHA/diff before advancing.

## Required deliverables

- modules/D/runs/<RUN_ID>/RUN_PLAN.md
- modules/D/runs/<RUN_ID>/SOURCE_REGISTER.json
- modules/D/runs/<RUN_ID>/GATE_RESULTS.json
- modules/D/runs/<RUN_ID>/INDEPENDENT_VERIFICATION.md
- modules/D/runs/<RUN_ID>/CLOSEOUT.md
- frozen output packet and artifact registry entries

## Componentwise gates

- positive distributions
- energy/charge conservation
- event ordering
- stiff-solver convergence
- restart and independent reconstruction

## Commit message

`Close Module D at its verified scientific scope`
