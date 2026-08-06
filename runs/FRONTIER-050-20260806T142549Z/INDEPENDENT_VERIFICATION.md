# Independent Verification

## Inputs reconstructed

- Rehashed all `29` admitted source objects from `sources/SOURCE_MANIFEST.json`.
- Rehashed all `5` REC-040 admitted objects and independently confirmed `canonical_parents` is empty.
- Read raw `memory/ARTIFACT_REGISTRY.json`, `memory/RUN_INDEX.json`, and every `modules/<A-J>/runs` tree.
- Verified the A finite configured result directly from its declared result hash, while excluding it as a governed Module A run.

## Methods independent from primary execution

The verifier did not use the primary audit's gate verdicts or row statuses. It selected the first topological module with no registered module artifact, no indexed module run, and no non-placeholder module-run files.

## Results

- Source bytes exact: `True`.
- REC-040 objects exact and source-only: `True`.
- Earliest missing governed module output: `A`.
- Primary/independent frontier agreement: `True`.
- A manufactured reference passes its own declared hash but remains outside `modules/A/runs` and the artifact/run registries.

## Disagreements

None.

## Verdict

**PASS** — Module A is independently reconstructed as the unique earliest frontier. This verifies an audit conclusion only; it does not execute Module A or produce `H_A_to_B`.
