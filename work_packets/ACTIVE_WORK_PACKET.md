# ACTIVE WORK PACKET — F-155

**This is the only authorized work. Execute it in order.**

- Module: `F`
- Objective: Execute charge/plasma composition, photon/neutrino persistence, atomic candidates, opacity/transport and recombination-entry state from H_E_to_F_v2.
- Run workspace: `not yet created`

## Exact sequence

1. Read `recipes/F/WORK_ORDER.md` and `recipes/F/recipe.json`.
2. Verify all exact parent hashes and fill the run source register.
3. Freeze the pre-execution lock before primary execution.
4. Run these Wolfram calls exactly and record their complete outputs:

   - `python tools/director.py wolfram-show --call F-WL-001`
   - `python tools/director.py wolfram-show --call F-WL-002`

5. Run `python tools/run_reference_checks.py --module F --output <RUN_DIR>/reference_checks.json`.
6. Bind and run the prebuilt local engines listed below. Every `__BIND_` token is a hard stop:

   - `python tools/director.py solver-copy --module F --solver reaction_network --destination <RUN_DIR>`
   - fill `configured_runs/binding_sheets/F_reaction_network.bindings.json` after it is copied into the run; every value requires an origin SHA-256
   - `python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/F_reaction_network.template.json --binding-sheet <RUN_DIR>/binding_sheets/F_reaction_network.bindings.json --output <RUN_DIR>/solver_configs/F_reaction_network.json`
   - `python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/F_reaction_network.json --output-dir <RUN_DIR>/solver_outputs/reaction_network`
   - `python tools/director.py solver-copy --module F --solver transport --destination <RUN_DIR>`
   - fill `configured_runs/binding_sheets/F_transport.bindings.json` after it is copied into the run; every value requires an origin SHA-256
   - `python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/F_transport.template.json --binding-sheet <RUN_DIR>/binding_sheets/F_transport.bindings.json --output <RUN_DIR>/solver_configs/F_transport.json`
   - `python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/F_transport.json --output-dir <RUN_DIR>/solver_outputs/transport`

7. Execute any remaining parent-driven domain code named in the recipe. Manufactured checks and generic engines do not replace the physical result.
8. Run countermodels, ablations, convergence, restart, replay, uncertainty/covariance, and independent reconstruction.
9. Finalize manifests only after outputs stop changing. State strongest supported and unsupported claims.
10. Commit and verify the exact GitHub SHA/diff before advancing.

## Required deliverables

- modules/F/runs/<RUN_ID>/OUTPUT_CONTRACT.json
- modules/F/runs/<RUN_ID>/SOURCE_REGISTER.json
- modules/F/runs/<RUN_ID>/GATE_RESULTS.json
- modules/F/runs/<RUN_ID>/INDEPENDENT_VERIFICATION.md
- modules/F/runs/<RUN_ID>/CLOSEOUT.md
- versioned superseding H_F_to_G_v2 handoff and manifest

## Componentwise gates

- all module-spec required outputs SATISFIED
- all configured child bindings SATISFIED
- exact source/parent lineage
- no public-data generation leakage
- semantic countermodels
- convergence, covariance, restart/replay and independent reconstruction

## Commit message

`Close F-155 superseding F replay at verified scope`
