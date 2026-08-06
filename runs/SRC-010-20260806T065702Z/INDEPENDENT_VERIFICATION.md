# Independent Verification

## Inputs reconstructed

All 29 records in `source_seed/SOURCE_SEED_MANIFEST.json` were independently reopened and hashed, then compared with the admitted registry, source manifest, and frozen byte objects.

## Methods independent from primary execution

The verifier did not trust the primary admission summary. It recomputed SHA-256 and byte length, checked roles and classifications, verified the five canonical sources in reading order 1-5, and rejected analysis summaries as canonical parents.

## Results

- Source objects reconstructed: 29
- Core canonical objects: 5
- Hash, size, role, or classification mismatches: 0
- Missing frozen objects: 0
- Reconstruction SHA-256: `f13f97f0ff1380dcd924447a32610bf4020850fd326009209dac0a238265f030`

## Disagreements

Primary admission emitted machine-specific origins; these were normalized to relocation-safe repository-relative paths without changing bytes or scientific classification.

## Verdict

**PASS.** All SRC-010 componentwise gates are independently satisfied.
