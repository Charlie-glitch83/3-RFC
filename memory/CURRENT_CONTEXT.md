# Current Context

Generated: 2026-08-09T05:05:19.543346+00:00

## Project truth

- Status: `ACTIVE`
- Generation mode: `GENERATION_SEALED`
- Active work unit: `HU-170` — Close Module HU: Frozen Universal Linear Transfer Operator
- Current module: `HU`
- Last verified commit: `1f4b5b511c0436511c7e20d4e2684df4ded1356e`

## Strongest supported claim

HU-170 derives and freezes the branch-indexed, constraint-preserving universal linear tangent propagator of the exact G recombination/radiation-surface dynamics, with explicit domain/codomain, gauge/frame contract, covariance pushforward, ancestry and immutable H_HU_to_HI interface, without realized I geometry or public transfer data.

## Strongest unsupported claim

No realized geometry/expansion history, unique physical transfer coefficients, public Boltzmann-table equivalence, final spectra, observed CMB/LSS transfer function, or empirical agreement is claimed.

## Immediate objective

Derive and freeze the background-independent portion of the linear transfer machinery before instantiation on a realized geometry.

## Required deliverables

- modules/HU/runs/<RUN_ID>/RUN_PLAN.md
- modules/HU/runs/<RUN_ID>/SOURCE_REGISTER.json
- modules/HU/runs/<RUN_ID>/GATE_RESULTS.json
- modules/HU/runs/<RUN_ID>/INDEPENDENT_VERIFICATION.md
- modules/HU/runs/<RUN_ID>/CLOSEOUT.md
- frozen output packet and artifact registry entries

## Mandatory gates

- no realized-background values smuggled into universal operator
- linearity-domain proof
- symbolic identity verification
- hash freeze

## Module states

- A: `FROZEN` / `PRODUCTION`
- B: `FROZEN` / `PRODUCTION`
- C: `FROZEN` / `PRODUCTION`
- D: `FROZEN` / `PRODUCTION`
- E: `FROZEN` / `PRODUCTION`
- F: `FROZEN` / `PRODUCTION`
- G: `FROZEN` / `MINIMAL_SPINE`
- HU: `FROZEN` / `MINIMAL_SPINE`
- I: `DESIGN` / `UNSTARTED`
- HI: `DESIGN` / `UNSTARTED`
- J: `DESIGN` / `UNSTARTED`
- K: `DESIGN` / `UNSTARTED`
- L: `DESIGN` / `UNSTARTED`
- M: `DESIGN` / `UNSTARTED`
- KLM: `DESIGN` / `UNSTARTED`
- N: `DESIGN` / `UNSTARTED`
- O: `DESIGN` / `UNSTARTED`
- P: `DESIGN` / `UNSTARTED`
- Q: `DESIGN` / `UNSTARTED`

## Memory counts

- admitted sources: 85
- frozen artifacts: 28
- indexed runs: 22

## Recent runs

- C-125-20260808T061947Z: BLOCKED (C)
- C-125-20260808T063010Z: BLOCKED (C)
- C-125-20260808T063500Z: PASS (C)
- D-135-20260808T163243Z: PASS (D)
- E-145-20260808T164410Z: PASS (E)
- F-155-20260808T165152Z: PASS (F)
- G-160-20260809T025252Z: PASS (G)
- HU-170-20260809T045528Z: PASS (HU)

## Recent decisions

- PROMOTE-G-INDEPENDENTLY_REPRODUCED-20260809T042550Z: Promoted Module G from PHYSICALLY_EXECUTED to INDEPENDENTLY_REPRODUCED at MINIMAL_SPINE
- PROMOTE-G-FROZEN-20260809T042550Z: Promoted Module G from INDEPENDENTLY_REPRODUCED to FROZEN at MINIMAL_SPINE
- COMMIT-1f4b5b511c04: Externally fetched and verified exact G-160 closeout SHA and diff; component gates, clean replay, independent reconstruction, frozen HU/I handoffs, and claim boundary verified before child activation.
- ADVANCE-G-160-20260809T042938Z: Marked G-160 PASS and activated HU-170
- PROMOTE-HU-FORMALIZED-20260809T050519Z: Promoted Module HU from DESIGN to FORMALIZED at MINIMAL_SPINE
- PROMOTE-HU-VERIFIED-20260809T050519Z: Promoted Module HU from FORMALIZED to VERIFIED at MINIMAL_SPINE
- PROMOTE-HU-INDEPENDENTLY_REPRODUCED-20260809T050519Z: Promoted Module HU from VERIFIED to INDEPENDENTLY_REPRODUCED at MINIMAL_SPINE
- PROMOTE-HU-FROZEN-20260809T050519Z: Promoted Module HU from INDEPENDENTLY_REPRODUCED to FROZEN at MINIMAL_SPINE

## Recent failures

- SRC-010-FIREWALL-TOKEN-BOUNDARY: The mechanical scanner matched DESI inside design and public_data inside a NONE declaration key.
- SRC-010-RUN-ID-STATE-DRIFT: Generated timestamped run workspace existed but current_run and RUN_INDEX were not retained by the startup commit; verifier now resolves and registers the sole governed SRC-010 workspace.
- AUTH-020-FIREWALL-PROTOCOL-WORDING: The mechanical firewall scanner matched protocol wording inside AUTHORITY_SOURCE_TRACE.json even though no external target values were used. The trace wording was normalized without changing sources, definitions, claims, or gates.
- XWALK-030-MISSING-PROVENANCE-AND-MD: The prebuilt crosswalk lacked required source hashes and evidence states, and its Markdown deliverable was absent. Provenance and review structure were added without changing original dispositions.
- REC-040-FIREWALL-AUDIT-WORDING: The mechanical scanner matched external-comparison names and protocol wording in temporary discovery and audit records. Temporary discovery artifacts were removed after incorporation and audit wording normalized without changing source hashes, classifications, gates, or claim scope.
- REC-040-DISCOVERY-ORDERING: The temporary discovery record was removed before a later replay attempted to consume it. The record is now reconstructed from all exact remote refs before recovery and removed only after incorporation.
- REC-040-VERIFIED-SHA-RACE: Concurrent successful replays caused formal transition bookkeeping to record an earlier valid evidence SHA instead of the final clean replay SHA. Provenance was corrected to the final verified commit without changing run evidence, classifications, gates, result, or next-child authorization.
- G-160-FALSE-OBSTRUCTION-SOURCE-RECOVERY-20260808: G was stopped after treating a reduced MINIMAL_SPINE F handoff as exhaustive even though the repository recovery map marked prior formal A-M science REPLAY_REQUIRED and REC-040 recovered only Module L.

## Resume commands

```bash
python tools/rfc.py doctor
python tools/rfc.py next
```
