# REC-040 — Recover Valid Prior 2-RFC Assets by Exact Object Admission

## Objective

Inspect old repository branches and libraries, admit only exact valid scientific objects, and quarantine obsolete machinery and failed outputs.

## Exact sequence

1. Fetch candidate objects from 2-RFC by exact commit and path.
2. Hash, replay, and independently inspect each object.
3. Do not import an old PASS label, state file, numerical output, or external-target-contaminated artifact as authority.
4. Treat repaired Module L as a recovery candidate at its exact verified scope only.
5. Inspect Charlie-glitch83/2-RFC and known lineages.
6. Verify exact commits and files.
7. Replay or reconstruct candidate assets.
8. Classify each object: CANONICAL_PARENT, ADMITTED_SOURCE, REPLAY_REQUIRED, COMPARISON_ONLY, HISTORICAL_WARNING, QUARANTINED, SUPERSEDED, EXCLUDED.
9. Preserve Module L first-pass work only at its verified scope.

## Commands

```bash
python tools/director.py doctor
```

## Deliverables

- recovery/LINEAGE_CROSSWALK.json
- recovery/ADMITTED_ASSET_MANIFEST.json
- recovery/QUARANTINE.md
- runs/REC-040/CLOSEOUT.md

## Componentwise gates

- exact commit/file hashes
- no old PASS auto-promoted
- no external-target influence
- replay evidence

## Hard stops

- required source or parent hash is missing
- a public target would influence a generation decision
- a claimed artifact cannot be fetched and independently verified
- a componentwise gate fails

## Commit

`Recover verified RFC assets without inheriting failures`
