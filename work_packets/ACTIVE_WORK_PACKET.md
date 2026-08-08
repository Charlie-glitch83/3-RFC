# ACTIVE WORK PACKET — G-160

**This is the only authorized work. Execute it in order.**

- Module: `G`
- Objective: Generate recombination, visibility, opacity, and radiation-surface histories from the physical plasma state.
- Run workspace: `modules/G/runs/G-160-20260808T021341Z`

## Exact sequence

1. Read `recipes/G/WORK_ORDER.md` and `recipes/G/recipe.json`.
2. Verify all exact parent hashes and fill the run source register.
3. Freeze the pre-execution lock before primary execution.
4. Run these Wolfram calls exactly and record their complete outputs:

   - `python tools/director.py wolfram-show --call G-WL-001`
   - `python tools/director.py wolfram-show --call G-WL-002`

5. Run `python tools/run_reference_checks.py --module G --output modules/G/runs/G-160-20260808T021341Z/reference_checks.json`.
6. Bind and run the prebuilt local engines listed below. Every `__BIND_` token is a hard stop:

   - `python tools/director.py solver-copy --module G --solver reaction_network --destination modules/G/runs/G-160-20260808T021341Z`
   - fill `configured_runs/binding_sheets/G_recombination_network.bindings.json` after it is copied into the run; every value requires an origin SHA-256
   - `python tools/materialize_solver_config.py --template modules/G/runs/G-160-20260808T021341Z/solver_templates/G_recombination_network.template.json --binding-sheet modules/G/runs/G-160-20260808T021341Z/binding_sheets/G_recombination_network.bindings.json --output modules/G/runs/G-160-20260808T021341Z/solver_configs/G_recombination_network.json`
   - `python tools/run_configured_solver.py --config modules/G/runs/G-160-20260808T021341Z/solver_configs/G_recombination_network.json --output-dir modules/G/runs/G-160-20260808T021341Z/solver_outputs/reaction_network`
   - `python tools/director.py solver-copy --module G --solver visibility --destination modules/G/runs/G-160-20260808T021341Z`
   - fill `configured_runs/binding_sheets/G_visibility.bindings.json` after it is copied into the run; every value requires an origin SHA-256
   - `python tools/materialize_solver_config.py --template modules/G/runs/G-160-20260808T021341Z/solver_templates/G_visibility.template.json --binding-sheet modules/G/runs/G-160-20260808T021341Z/binding_sheets/G_visibility.bindings.json --output modules/G/runs/G-160-20260808T021341Z/solver_configs/G_visibility.json`
   - `python tools/run_configured_solver.py --config modules/G/runs/G-160-20260808T021341Z/solver_configs/G_visibility.json --output-dir modules/G/runs/G-160-20260808T021341Z/solver_outputs/visibility`

7. Execute any remaining parent-driven domain code named in the recipe. Manufactured checks and generic engines do not replace the physical result.
8. Run countermodels, ablations, convergence, restart, replay, uncertainty/covariance, and independent reconstruction.
9. Finalize manifests only after outputs stop changing. State strongest supported and unsupported claims.
10. Commit and verify the exact GitHub SHA/diff before advancing.

## Required deliverables

- modules/G/runs/<RUN_ID>/RUN_PLAN.md
- modules/G/runs/<RUN_ID>/SOURCE_REGISTER.json
- modules/G/runs/<RUN_ID>/GATE_RESULTS.json
- modules/G/runs/<RUN_ID>/INDEPENDENT_VERIFICATION.md
- modules/G/runs/<RUN_ID>/CLOSEOUT.md
- frozen output packet and artifact registry entries

## Componentwise gates

- rate and opacity lineage
- normalization and positivity
- stiff convergence
- independent reconstruction

## Commit message

`Close Module G at its verified scientific scope`
