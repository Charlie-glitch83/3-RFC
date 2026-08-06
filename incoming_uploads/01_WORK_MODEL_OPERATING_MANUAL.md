# Work Model Operating Manual

## Mandatory session loop

At session start:

```bash
bash tools/start_work.sh
```

Then execute `work_packets/ACTIVE_WORK_PACKET.md` exactly.

At session end:

```bash
python tools/rfc.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan
python tools/rfc.py context
```

Commit and verify before leaving.

## Do not overthink the repository

The active queue item is the work. Read only the documents it cites, execute it, close it, and advance. Do not rebuild the architecture because a different organization seems cleaner.

## Analysis-to-output cadence

- Convert source learning into repository notes or evidence quickly.
- A long work session must produce verified commits, frozen artifacts, or an explicit blocker—not only chat analysis.
- Verify each GitHub write immediately.
- Never claim progress from text that exists only in chat or a local scratch buffer.

## Provenance-bound computation

Do not hand-edit a solver template into an executable configuration. Fill the generated binding sheet with exact values and origin hashes, materialize it with `tools/materialize_solver_config.py`, then run the module local phase with `tools/finish_local_phase.sh`. Exact commands are in the active packet and module work order.

Every Wolfram input is prewritten. Submit it verbatim, preserve the complete output, and register it so the frozen output gate is applied.

## Scientific work sequence

1. Verify authority and exact parent.
2. Freeze workspace, definitions, source hashes, schemas, tests, tolerances, falsifiers, and claim boundary.
3. Derive before implementing.
4. Run primary execution.
5. Run semantic countermodels and ablations.
6. Preserve failed attempts.
7. Correct only implementation defects without changing frozen science; otherwise create a new versioned scientific run.
8. Run independent reconstruction.
9. Run clean replay.
10. Freeze outputs and finalize manifests only after files stop changing.
11. State strongest supported and unsupported claims.
12. Commit and verify.

## When derivation is missing

Study the admitted triad, kernel, N-body relational laws, exact parent state, dimensions, symmetries, conservation, causality, and branch structure. Produce one of:

- a unique derived law;
- a finite or parameterized lawful branch family with internally derived admissibility conditions;
- an obstruction theorem;
- a declared underdetermination that blocks downstream execution.

Do not import the standard answer because it is familiar.

## Corrections and known failures

A known old failure can be a regression test, but the replacement cannot be chosen by minimizing that failure against its public answer. Freeze the internally compelled repair first, then rerun the regression and additional withheld consequences.

## GitHub workflow

1. Confirm repository and branch.
2. Pull/fetch current state.
3. Make a coherent work-unit change.
4. Run local validation.
5. Commit with the queue's prescribed message.
6. Push.
7. Fetch the commit/branch through GitHub.
8. Confirm SHA and diff.
9. Record SHA in closeout/context.

If the integration fails to write, switch to `git`/`gh` or another supported method immediately. Do not assume.

## Run and evidence commands

For an execution-owning unit:

```bash
python tools/rfc.py new-run <MODULE_OR_UNIT>
# complete and freeze the run files
python tools/rfc.py close-run --run-id <RUN_ID> --result PASS --closeout <RUN_DIR>/CLOSEOUT.md
python tools/rfc.py promote-module <MODULE> --to <STATE> --fidelity <FIDELITY> --evidence <FILE>
python tools/rfc.py record-claim --file <CLAIM_RECORD.json>
```

A module task cannot advance unless a PASS run is closed and registered, its required evidence states appear in its history, and its target fidelity has been reached. `HR-255` additionally requires all A-N/KLM modules to be frozen at hyper-realistic fidelity before the final universe freeze.
