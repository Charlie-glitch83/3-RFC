# ACTIVE WORK PACKET — D-130

**This is the only authorized work. Execute it in order.**

- Module: `D`
- Objective: Evolve the microscopic state through nonequilibrium thermodynamics, transport, phase changes, entropy production, and clock/frame-consistent expansion.
- Run workspace: `not yet created`

## Exact sequence

1. Read `recipes/D/WORK_ORDER.md` and `recipes/D/recipe.json`.
2. Verify all exact parent hashes and fill the run source register.
3. Freeze the pre-execution lock before primary execution.
4. Run these Wolfram calls exactly and record their complete outputs:

   - `python tools/director.py wolfram-show --call D-WL-001`
   - `python tools/director.py wolfram-show --call D-WL-002`

5. Run `python tools/run_reference_checks.py --module D --output <RUN_DIR>/reference_checks.json`.
6. Bind and run the prebuilt local engines listed below. Every `__BIND_` token is a hard stop:

   - `python tools/director.py solver-copy --module D --solver transport --destination <RUN_DIR>`
   - fill `configured_runs/binding_sheets/D_transport.bindings.json` after it is copied into the run; every value requires an origin SHA-256
   - `python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/D_transport.template.json --binding-sheet <RUN_DIR>/binding_sheets/D_transport.bindings.json --output <RUN_DIR>/solver_configs/D_transport.json`
   - `python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/D_transport.json --output-dir <RUN_DIR>/solver_outputs/transport`

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
