# BOOT-000 — Install, Verify, and Commit the Repository Scaffold

## Objective

Place this scaffold at the root of Charlie-glitch83/3-RFC, run all local checks, commit it, and verify the exact GitHub SHA and diff.

## Exact sequence

1. Copy the complete bundle to the empty repository root.
2. Commit the scaffold exactly once.
3. Fetch README.md and the commit through GitHub, verify SHA and diff, then record the commit.
4. Copy the bundle contents into the empty 3-RFC repository without redesigning them.
5. Run python tools/rfc.py doctor, python -m unittest discover -s tests -v, and python tools/rfc.py firewall-scan.
6. Create work branch agent/3rfc-universe-build after the scaffold is visible on the default branch or as the initial branch, according to repository state.
7. Commit with the prescribed message and verify the commit SHA, file list, fetched README, and branch comparison.
8. Record the verified SHA in memory/DECISION_LOG.jsonl and the closeout.

## Commands

```bash
bash bootstrap.sh
python tools/director.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan
```

## Deliverables

- runs/BOOT-000/CLOSEOUT.md
- verified GitHub commit SHA
- passing doctor/tests/firewall scan

## Componentwise gates

- README visible in GitHub
- new commit SHA exists
- diff contains scaffold
- doctor and tests pass

## Hard stops

- required source or parent hash is missing
- a public target would influence a generation decision
- a claimed artifact cannot be fetched and independently verified
- a componentwise gate fails

## Commit

`Initialize the 3-RFC governed universe workspace`
