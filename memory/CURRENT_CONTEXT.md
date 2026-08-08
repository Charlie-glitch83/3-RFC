# Current Context

Generated: 2026-08-08T01:30:09.928122+00:00

## Project truth

- Status: `ACTIVE`
- Generation mode: `GENERATION_SEALED`
- Active work unit: `F-150` — Close Module F: Post-Nuclear Plasma and Radiation Persistence
- Current module: `F`
- Last verified commit: `4a9f3f5e5b76c9612120b427cffd60642c891662`

## Strongest supported claim

From the exact frozen D three-carrier state, Module E derives and physically executes a source-owned seven-state reversible primordial-composite reaction network with parent-derived binding and rates, exact internal carrier accounting, positive abundance dynamics, material witnessed reaction routes, constitutive binding-memory transfer, convergence, freeze-out, covariance, restart/replay and independent reconstruction.

## Strongest unsupported claim

Module E does not establish Standard Model proton/neutron/isotope correspondence, measured nuclear masses/bindings/cross sections/lifetimes, Kelvin/MeV calibration, conventional precision BBN, empirical primordial abundance agreement, metric/FRW expansion, or full hyper-realistic nuclear physics.

## Immediate objective

Carry isotope, plasma, radiation, neutrino, and transport states from nucleosynthesis into recombination without losing lineage or covariance.

## Required deliverables

- modules/F/runs/<RUN_ID>/RUN_PLAN.md
- modules/F/runs/<RUN_ID>/SOURCE_REGISTER.json
- modules/F/runs/<RUN_ID>/GATE_RESULTS.json
- modules/F/runs/<RUN_ID>/INDEPENDENT_VERIFICATION.md
- modules/F/runs/<RUN_ID>/CLOSEOUT.md
- frozen output packet and artifact registry entries

## Mandatory gates

- charge neutrality where derived
- energy and particle accounting
- covariance positive semidefinite
- replay from E

## Module states

- A: `FROZEN` / `PRODUCTION`
- B: `FROZEN` / `MINIMAL_SPINE`
- C: `FROZEN` / `MINIMAL_SPINE`
- D: `FROZEN` / `MINIMAL_SPINE`
- E: `FROZEN` / `MINIMAL_SPINE`
- F: `DESIGN` / `UNSTARTED`
- G: `DESIGN` / `UNSTARTED`
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

- admitted sources: 29
- frozen artifacts: 10
- indexed runs: 11

## Recent runs

- REC-040-20260806T135256Z: PASS (RECOVERY)
- FRONTIER-050-20260806T142549Z: PASS (AUDIT)
- A-100-20260806T173458Z: PASS (A)
- B-110-20260807T002248Z: PASS (B)
- C-120-20260807T032543Z: PASS (C)
- D-130-20260807T220342Z: PASS (D)
- E-140-20260807T232334Z: PASS (E)
- F-150-20260808T013006Z: CREATED (F)

## Recent decisions

- ADVANCE-D-130-20260807T232330Z: Marked D-130 PASS and activated E-140
- PROMOTE-E-FORMALIZED-20260808T010553Z: Promoted Module E from DESIGN to FORMALIZED at MINIMAL_SPINE
- PROMOTE-E-IMPLEMENTED-20260808T010553Z: Promoted Module E from FORMALIZED to IMPLEMENTED at MINIMAL_SPINE
- PROMOTE-E-VERIFIED-20260808T010553Z: Promoted Module E from IMPLEMENTED to VERIFIED at MINIMAL_SPINE
- PROMOTE-E-PHYSICALLY_EXECUTED-20260808T010553Z: Promoted Module E from VERIFIED to PHYSICALLY_EXECUTED at MINIMAL_SPINE
- PROMOTE-E-INDEPENDENTLY_REPRODUCED-20260808T010553Z: Promoted Module E from PHYSICALLY_EXECUTED to INDEPENDENTLY_REPRODUCED at MINIMAL_SPINE
- PROMOTE-E-FROZEN-20260808T010553Z: Promoted Module E from INDEPENDENTLY_REPRODUCED to FROZEN at MINIMAL_SPINE
- ADVANCE-E-140-20260808T010554Z: Marked E-140 PASS and activated F-150

## Recent failures

- BOOT-000-ACTIVE-QUEUE-TEST-HARDCODE: The deterministic-next test hardcoded BOOT-000 instead of reading active state.
- SRC-010-FIREWALL-TOKEN-BOUNDARY: The mechanical scanner matched DESI inside design and public_data inside a NONE declaration key.
- SRC-010-RUN-ID-STATE-DRIFT: Generated timestamped run workspace existed but current_run and RUN_INDEX were not retained by the startup commit; verifier now resolves and registers the sole governed SRC-010 workspace.
- AUTH-020-FIREWALL-PROTOCOL-WORDING: The mechanical firewall scanner matched protocol wording inside AUTHORITY_SOURCE_TRACE.json even though no external target values were used. The trace wording was normalized without changing sources, definitions, claims, or gates.
- XWALK-030-MISSING-PROVENANCE-AND-MD: The prebuilt crosswalk lacked required source hashes and evidence states, and its Markdown deliverable was absent. Provenance and review structure were added without changing original dispositions.
- REC-040-FIREWALL-AUDIT-WORDING: The mechanical scanner matched external-comparison names and protocol wording in temporary discovery and audit records. Temporary discovery artifacts were removed after incorporation and audit wording normalized without changing source hashes, classifications, gates, or claim scope.
- REC-040-DISCOVERY-ORDERING: The temporary discovery record was removed before a later replay attempted to consume it. The record is now reconstructed from all exact remote refs before recovery and removed only after incorporation.
- REC-040-VERIFIED-SHA-RACE: Concurrent successful replays caused formal transition bookkeeping to record an earlier valid evidence SHA instead of the final clean replay SHA. Provenance was corrected to the final verified commit without changing run evidence, classifications, gates, result, or next-child authorization.

## Resume commands

```bash
python tools/rfc.py doctor
python tools/rfc.py next
```
