# ACTIVE WORK PACKET — REC-040

**This is the only authorized work. Execute it in order.**

- Module: `RECOVERY`
- Objective: Inspect old repository branches and libraries, admit only exact valid scientific objects, and quarantine obsolete machinery and failed outputs.
- Run workspace: `runs/REC-040-20260806T135256Z`

## Exact sequence

1. Read `work_units/REC-040/WORK_ORDER.md` and `work_units/REC-040/recipe.json`.
2. Execute the frozen sequence below without redesigning it:

   1. Fetch candidate objects from 2-RFC by exact commit and path.
   2. Hash, replay, and independently inspect each object.
   3. Do not import an old PASS label, state file, numerical output, or public-data-contaminated artifact as authority.
   4. Treat repaired Module L as a recovery candidate at its exact verified scope only.
   5. Inspect Charlie-glitch83/2-RFC and known lineages.
   6. Verify exact commits and files.
   7. Replay or reconstruct candidate assets.
   8. Classify each object: CANONICAL_PARENT, ADMITTED_SOURCE, REPLAY_REQUIRED, COMPARISON_ONLY, HISTORICAL_WARNING, QUARANTINED, SUPERSEDED, EXCLUDED.
   9. Preserve Module L first-pass work only at its verified scope.

3. Run the exact commands:

   - `python tools/director.py doctor`

## Required deliverables

- recovery/LINEAGE_CROSSWALK.json
- recovery/ADMITTED_ASSET_MANIFEST.json
- recovery/QUARANTINE.md
- runs/REC-040/CLOSEOUT.md

## Componentwise gates

- exact commit/file hashes
- no old PASS auto-promoted
- no public-data contamination
- replay evidence

## Commit message

`Recover verified RFC assets without inheriting failures`
