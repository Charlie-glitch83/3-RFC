# ACTIVE WORK PACKET — F-150

**This is the only authorized work. Execute it in order.**

- Module: `F`
- Objective: Carry isotope, plasma, radiation, neutrino, and transport states from nucleosynthesis into recombination without losing lineage or covariance.
- Run workspace: `modules/F/runs/F-150-20260808T013006Z`

## Exact sequence

1. Read `recipes/F/WORK_ORDER.md` and `recipes/F/recipe.json`.
2. Verify all exact parent hashes and fill the run source register.
3. Freeze the pre-execution lock before primary execution.
4. Run these Wolfram calls exactly and record their complete outputs:

   - `python tools/director.py wolfram-show --call F-WL-001`
   - `python tools/director.py wolfram-show --call F-WL-002`

5. Run `python tools/run_reference_checks.py --module F --output modules/F/runs/F-150-20260808T013006Z/reference_checks.json`.
6. Bind and run the prebuilt local engines listed below. Every `__BIND_` token is a hard stop:

   - `python tools/director.py solver-copy --module F --solver reaction_network --destination modules/F/runs/F-150-20260808T013006Z`
   - fill `configured_runs/binding_sheets/F_reaction_network.bindings.json` after it is copied into the run; every value requires an origin SHA-256
   - `python tools/materialize_solver_config.py --template modules/F/runs/F-150-20260808T013006Z/solver_templates/F_reaction_network.template.json --binding-sheet modules/F/runs/F-150-20260808T013006Z/binding_sheets/F_reaction_network.bindings.json --output modules/F/runs/F-150-20260808T013006Z/solver_configs/F_reaction_network.json`
   - `python tools/run_configured_solver.py --config modules/F/runs/F-150-20260808T013006Z/solver_configs/F_reaction_network.json --output-dir modules/F/runs/F-150-20260808T013006Z/solver_outputs/reaction_network`
   - `python tools/director.py solver-copy --module F --solver transport --destination modules/F/runs/F-150-20260808T013006Z`
   - fill `configured_runs/binding_sheets/F_transport.bindings.json` after it is copied into the run; every value requires an origin SHA-256
   - `python tools/materialize_solver_config.py --template modules/F/runs/F-150-20260808T013006Z/solver_templates/F_transport.template.json --binding-sheet modules/F/runs/F-150-20260808T013006Z/binding_sheets/F_transport.bindings.json --output modules/F/runs/F-150-20260808T013006Z/solver_configs/F_transport.json`
   - `python tools/run_configured_solver.py --config modules/F/runs/F-150-20260808T013006Z/solver_configs/F_transport.json --output-dir modules/F/runs/F-150-20260808T013006Z/solver_outputs/transport`

7. Execute any remaining parent-driven domain code named in the recipe. Manufactured checks and generic engines do not replace the physical result.
8. Run countermodels, ablations, convergence, restart, replay, uncertainty/covariance, and independent reconstruction.
9. Finalize manifests only after outputs stop changing. State strongest supported and unsupported claims.
10. Commit and verify the exact GitHub SHA/diff before advancing.

## Required deliverables

- modules/F/runs/<RUN_ID>/RUN_PLAN.md
- modules/F/runs/<RUN_ID>/SOURCE_REGISTER.json
- modules/F/runs/<RUN_ID>/GATE_RESULTS.json
- modules/F/runs/<RUN_ID>/INDEPENDENT_VERIFICATION.md
- modules/F/runs/<RUN_ID>/CLOSEOUT.md
- frozen output packet and artifact registry entries

## Componentwise gates

- charge neutrality where derived
- energy and particle accounting
- covariance positive semidefinite
- replay from E

## Commit message

`Close Module F at its verified scientific scope`
