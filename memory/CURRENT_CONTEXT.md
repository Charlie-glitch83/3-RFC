# Current Context

Generated: 2026-08-09T02:22:56.105242+00:00

## Project truth

- Status: `ACTIVE`
- Generation mode: `GENERATION_SEALED`
- Active work unit: `F-155` — Supersede Module F: Child-Ready Post-Nuclear Plasma
- Current module: `F`
- Last verified commit: `ff72654b32d1d17dc37f462c5558603848a8dd9f`

## Strongest supported claim

F-155 replays the recovered finite-relational Module F construction against exact H_E_to_F_v2 at PRODUCTION fidelity: isotope-resolved post-nuclear persistence, relational charge/Gauss closure, generated plasma response and transport operators, photon/neutrino persistence, witnessed-event opacity seeds, conditional atomic candidates and no-loss promotion, intrinsic recombination-entry state, source-transfer ownership, covariance, restart and complete G child bindings, with no public post-BBN or recombination target used in generation.

## Strongest unsupported claim

No measured plasma/atomic coefficients, unique SI calibration, public recombination coordinate, solved nonequilibrium recombination/free-electron/optical-depth/visibility/last-scattering history, or empirical agreement is claimed.

## Immediate objective

Execute charge/plasma composition, photon/neutrino persistence, atomic candidates, opacity/transport and recombination-entry state from H_E_to_F_v2.

## Required deliverables

- modules/F/runs/<RUN_ID>/OUTPUT_CONTRACT.json
- modules/F/runs/<RUN_ID>/SOURCE_REGISTER.json
- modules/F/runs/<RUN_ID>/GATE_RESULTS.json
- modules/F/runs/<RUN_ID>/INDEPENDENT_VERIFICATION.md
- modules/F/runs/<RUN_ID>/CLOSEOUT.md
- versioned superseding H_F_to_G_v2 handoff and manifest

## Mandatory gates

- all module-spec required outputs SATISFIED
- all configured child bindings SATISFIED
- exact source/parent lineage
- no public-data generation leakage
- semantic countermodels
- convergence, covariance, restart/replay and independent reconstruction

## Module states

- A: `FROZEN` / `PRODUCTION`
- B: `FROZEN` / `PRODUCTION`
- C: `FROZEN` / `PRODUCTION`
- D: `FROZEN` / `PRODUCTION`
- E: `FROZEN` / `PRODUCTION`
- F: `FROZEN` / `PRODUCTION`
- G: `BLOCKED` / `UNSTARTED`
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
- frozen artifacts: 23
- indexed runs: 20

## Recent runs

- G-160-20260808T051613Z: BLOCKED (G)
- B-115-20260808T060000Z: PASS (B)
- C-125-20260808T061947Z: BLOCKED (C)
- C-125-20260808T063010Z: BLOCKED (C)
- C-125-20260808T063500Z: PASS (C)
- D-135-20260808T163243Z: PASS (D)
- E-145-20260808T164410Z: PASS (E)
- F-155-20260808T165152Z: PASS (F)

## Recent decisions

- ADVANCE-E-145-20260808T165005Z: Marked E-145 PASS and activated F-155
- REOPEN-F-20260809T021556Z: Reopened Module F from FROZEN/MINIMAL_SPINE at target fidelity PRODUCTION for the authorized superseding lineage.
- PROMOTE-F-FORMALIZED-20260809T022255Z: Promoted Module F from DESIGN to FORMALIZED at PRODUCTION
- PROMOTE-F-IMPLEMENTED-20260809T022255Z: Promoted Module F from FORMALIZED to IMPLEMENTED at PRODUCTION
- PROMOTE-F-VERIFIED-20260809T022255Z: Promoted Module F from IMPLEMENTED to VERIFIED at PRODUCTION
- PROMOTE-F-PHYSICALLY_EXECUTED-20260809T022255Z: Promoted Module F from VERIFIED to PHYSICALLY_EXECUTED at PRODUCTION
- PROMOTE-F-INDEPENDENTLY_REPRODUCED-20260809T022255Z: Promoted Module F from PHYSICALLY_EXECUTED to INDEPENDENTLY_REPRODUCED at PRODUCTION
- PROMOTE-F-FROZEN-20260809T022255Z: Promoted Module F from INDEPENDENTLY_REPRODUCED to FROZEN at PRODUCTION

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
