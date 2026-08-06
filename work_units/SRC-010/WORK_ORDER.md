# SRC-010 — Hash and Admit the Core Source Corpus

## Objective

Admit exact source bytes from source_seed into immutable sources/frozen, classify authority, and create a reproducible source manifest.

## Exact sequence

1. Recompute every source-seed SHA-256 independently.
2. Promote only exact original source bytes; analysis files remain advisory.
3. Write a source-role record for P29, P30, N-body proof, and N-body metadata.
4. Verify source_seed manifest.
5. Admit P29, N-body, P30 and metadata first.
6. Classify historical, explanatory, candidate-addendum, recovery, and interpretation sources.
7. Hash every admitted object and reconstruct manifest independently.

## Commands

```bash
python tools/rfc.py admit-seed
python tools/rfc.py doctor
```

## Deliverables

- sources/SOURCE_MANIFEST.json
- memory/SOURCE_REGISTRY.json
- runs/SRC-010/CLOSEOUT.md

## Componentwise gates

- all core bytes resolvable
- hashes match
- authority class explicit
- no summary used as parent

## Hard stops

- required source or parent hash is missing
- a public target would influence a generation decision
- a claimed artifact cannot be fetched and independently verified
- a componentwise gate fails

## Commit

`Admit and lock the core RFC source corpus`
