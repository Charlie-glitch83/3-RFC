# FRONTIER-050 — Determine the Earliest Missing Physical Parent

## Objective

Audit A–J and choose the earliest exact break between formal law and one physically executed parent chain.

## Exact sequence

1. Populate one row per A-J boundary with exact hashes and evidence.
2. Distinguish law, implementation, representative test, physical state, restart, covariance, and independent reconstruction.
3. Select the earliest missing parent and authorize exactly one child.
4. For each boundary, record source, law, representative test, physical parent, solver, output, restart, covariance, independent reconstruction, and evidence state.
5. Select the earliest missing object.
6. Authorize exactly one next module.

## Commands

```bash
python tools/director.py doctor
```

## Deliverables

- audit/PHYSICAL_FRONTIER.json
- audit/PHYSICAL_FRONTIER.md
- runs/FRONTIER-050/CLOSEOUT.md

## Componentwise gates

- no status word hides a missing object
- one frontier selected
- recovered parents verified

## Hard stops

- required source or parent hash is missing
- a public target would influence a generation decision
- a claimed artifact cannot be fetched and independently verified
- a componentwise gate fails

## Commit

`Locate the exact RFC physical execution frontier`
