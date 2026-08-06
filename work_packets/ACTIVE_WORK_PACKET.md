# ACTIVE WORK PACKET — SRC-010

**This is the only authorized work. Execute it in order.**

- Module: `SOURCES`
- Objective: Admit exact source bytes from source_seed into immutable sources/frozen, classify authority, and create a reproducible source manifest.
- Run workspace: `runs/SRC-010-20260806T065702Z`

## Exact sequence

1. Read `work_units/SRC-010/WORK_ORDER.md` and `work_units/SRC-010/recipe.json`.
2. Execute the frozen sequence below without redesigning it:

   1. Recompute every source-seed SHA-256 independently.
   2. Promote only exact original source bytes; analysis files remain advisory.
   3. Write a source-role record for P29, P30, N-body proof, and N-body metadata.
   4. Verify source_seed manifest.
   5. Admit P29, N-body, P30 and metadata first.
   6. Classify historical, explanatory, candidate-addendum, recovery, and interpretation sources.
   7. Hash every admitted object and reconstruct manifest independently.

3. Run the exact commands:

   - `python tools/rfc.py admit-seed`
   - `python tools/rfc.py doctor`

## Required deliverables

- sources/SOURCE_MANIFEST.json
- memory/SOURCE_REGISTRY.json
- runs/SRC-010/CLOSEOUT.md

## Componentwise gates

- all core bytes resolvable
- hashes match
- authority class explicit
- no summary used as parent

## Commit message

`Admit and lock the core RFC source corpus`
