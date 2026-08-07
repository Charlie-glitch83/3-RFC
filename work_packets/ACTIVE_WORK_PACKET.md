# ACTIVE WORK PACKET — B-110

**This is the only authorized work. Execute it in order.**

- Module: `B`
- Objective: Execute the sole first physical event from the exact frozen prephysical parent and generate the first restartable physical RFC state.
- Run workspace: `not yet created`

## Exact sequence

1. Read `recipes/B/WORK_ORDER.md` and `recipes/B/recipe.json`.
2. Admit only the exact frozen `modules/A/frozen/H_A_to_B.json` parent and verify its SHA-256 before deriving anything.
3. Freeze the Module B source register, physical-event definitions, candidate classes, branch laws, conservation ownership, falsifiers, component gates, tolerances, claim boundary, and independent-verifier design before primary execution.
4. Prove that physical time is absent in the Module A parent and begins only with the Big Implosion event.
5. Run these Wolfram calls exactly and record their complete outputs:

   - `python tools/director.py wolfram-show --call B-WL-001`
   - `python tools/director.py wolfram-show --call B-WL-002`

6. Run `python tools/run_reference_checks.py --module B --output <RUN_DIR>/reference_checks.json` as an implementation/invariant check only.
7. Bind and run the prebuilt `big_implosion` engine. Every `__BIND_` token is a hard stop:

   - `python tools/director.py solver-copy --module B --solver big_implosion --destination <RUN_DIR>`
   - fill `<RUN_DIR>/binding_sheets/B_big_implosion.bindings.json`; every value requires exact origin path, origin SHA-256, units, dimensions, and derivation object
   - `python tools/materialize_solver_config.py --template <RUN_DIR>/solver_templates/B_big_implosion.template.json --binding-sheet <RUN_DIR>/binding_sheets/B_big_implosion.bindings.json --output <RUN_DIR>/solver_configs/B_big_implosion.json`
   - `python tools/run_configured_solver.py --config <RUN_DIR>/solver_configs/B_big_implosion.json --output-dir <RUN_DIR>/solver_outputs/big_implosion`

8. Execute multiple graph sizes and nontrivial modes; verify strict nontrivial compression, conserved carrier mode, restart, exact reopening, event ordering, route, branch, memory, uncertainty, and no-loss ancestry.
9. Run compression and relational-coupling ablations, countermodels, convergence, restart, clean replay, and independent reconstruction.
10. Finalize manifests only after outputs stop changing. State the strongest supported and unsupported claims without importing later-module particles, constants, geometry, or cosmology.
11. Commit and verify the exact GitHub SHA and changed-file scope before closing or advancing.

## Required deliverables

- `modules/B/runs/<RUN_ID>/RUN_PLAN.md`
- `modules/B/runs/<RUN_ID>/SOURCE_REGISTER.json`
- `modules/B/runs/<RUN_ID>/PRE_EXECUTION_LOCK.json`
- `modules/B/runs/<RUN_ID>/GATE_RESULTS.json`
- `modules/B/runs/<RUN_ID>/INDEPENDENT_VERIFICATION.md`
- `modules/B/runs/<RUN_ID>/REPLAY_RECORD.json`
- `modules/B/runs/<RUN_ID>/GENERATED_OUTPUT_MANIFEST.json`
- `modules/B/runs/<RUN_ID>/CLOSEOUT.md`
- restartable frozen `H_B_to_C` packet and manifest

## Componentwise gates

- no pre-event physical time
- exact frozen Module A parent bytes and hashes
- strict nontrivial compression or derived equivalent
- total ledger preservation and explicit sector ownership
- no-loss reopening and restartability
- no later physics smuggled into Module B
- compression and relational-coupling ablations fail as predeclared
- clean replay and independent reconstruction

## Hard stops

- a physical clock or geometry is assumed in the Module A parent
- later-module particles, constants, empirical targets, or hidden defaults are inserted
- compression is trivial, branch selection is post hoc, or the total ledger is not conserved
- any mandatory component scores below `0.95`

## Claim boundary

At most: first physical RFC state at declared fidelity. No microscopic-sector completion, late-time cosmology, manifested universe, or empirical agreement is established here.

## Commit message

`Close Module B at its verified scientific scope`
