# Current Context

Generated: 2026-08-09T04:25:50.479488+00:00

## Project truth

- Status: `ACTIVE`
- Generation mode: `GENERATION_SEALED`
- Active work unit: `G-160` — Close Module G: Nonequilibrium Recombination and Last-Scattering State
- Current module: `G`
- Last verified commit: `9df3cdd1b262770c4be1e50f5d4a8bbc77adb1d6`

## Strongest supported claim

G-160 generates a finite-relational MINIMAL_SPINE nonequilibrium recombination, process-opacity, optical-depth, normalized visibility and radiation-surface branch family from exact H_F_to_G_v2, preserving branch identity, charge/accounting, covariance, restart, memory and ancestry and supplying child-ready H_G_to_HU and H_G_to_I interfaces without external target values.

## Strongest unsupported claim

No unique measured atomic coefficients, unique SI calibration, unique observed last-scattering coordinate, public recombination-code equivalence, final CMB spectra, late reionization history, or empirical agreement is claimed.

## Immediate objective

Generate recombination, visibility, opacity, and radiation-surface histories from the physical plasma state.

## Required deliverables

- modules/G/runs/<RUN_ID>/RUN_PLAN.md
- modules/G/runs/<RUN_ID>/SOURCE_REGISTER.json
- modules/G/runs/<RUN_ID>/GATE_RESULTS.json
- modules/G/runs/<RUN_ID>/INDEPENDENT_VERIFICATION.md
- modules/G/runs/<RUN_ID>/CLOSEOUT.md
- frozen output packet and artifact registry entries

## Mandatory gates

- rate and opacity lineage
- normalization and positivity
- stiff convergence
- independent reconstruction

## Module states

- A: `FROZEN` / `PRODUCTION`
- B: `FROZEN` / `PRODUCTION`
- C: `FROZEN` / `PRODUCTION`
- D: `FROZEN` / `PRODUCTION`
- E: `FROZEN` / `PRODUCTION`
- F: `FROZEN` / `PRODUCTION`
- G: `FROZEN` / `MINIMAL_SPINE`
- HU: `DESIGN` / `UNSTARTED`
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
- frozen artifacts: 26
- indexed runs: 21

## Recent runs

- B-115-20260808T060000Z: PASS (B)
- C-125-20260808T061947Z: BLOCKED (C)
- C-125-20260808T063010Z: BLOCKED (C)
- C-125-20260808T063500Z: PASS (C)
- D-135-20260808T163243Z: PASS (D)
- E-145-20260808T164410Z: PASS (E)
- F-155-20260808T165152Z: PASS (F)
- G-160-20260809T025252Z: PASS (G)

## Recent decisions

- ADVANCE-F-155-20260809T022428Z: Marked F-155 PASS and activated G-160
- REOPEN-G-20260809T030415Z: Reopened Module G from BLOCKED/UNSTARTED at target fidelity MINIMAL_SPINE for the authorized superseding lineage.
- PROMOTE-G-FORMALIZED-20260809T042549Z: Promoted Module G from DESIGN to FORMALIZED at MINIMAL_SPINE
- PROMOTE-G-IMPLEMENTED-20260809T042549Z: Promoted Module G from FORMALIZED to IMPLEMENTED at MINIMAL_SPINE
- PROMOTE-G-VERIFIED-20260809T042550Z: Promoted Module G from IMPLEMENTED to VERIFIED at MINIMAL_SPINE
- PROMOTE-G-PHYSICALLY_EXECUTED-20260809T042550Z: Promoted Module G from VERIFIED to PHYSICALLY_EXECUTED at MINIMAL_SPINE
- PROMOTE-G-INDEPENDENTLY_REPRODUCED-20260809T042550Z: Promoted Module G from PHYSICALLY_EXECUTED to INDEPENDENTLY_REPRODUCED at MINIMAL_SPINE
- PROMOTE-G-FROZEN-20260809T042550Z: Promoted Module G from INDEPENDENTLY_REPRODUCED to FROZEN at MINIMAL_SPINE

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
