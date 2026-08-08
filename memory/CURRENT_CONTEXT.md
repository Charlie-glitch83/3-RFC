# Current Context

Generated: 2026-08-08T16:42:15.777236+00:00

## Project truth

- Status: `ACTIVE`
- Generation mode: `GENERATION_SEALED`
- Active work unit: `E-145` — Supersede Module E: Source-Owned Primordial Nucleosynthesis
- Current module: `E`
- Last verified commit: `ff72654b32d1d17dc37f462c5558603848a8dd9f`

## Strongest supported claim

The unchanged physically executed B-110 Big-Implosion state now has a complete, nonduplicated, independently reconstructed and cleanly replayed four-sector genesis partition at PRODUCTION fidelity. H_B_to_C_v2 is frozen and child-ready, preserving exact first-physical-state ancestry while supplying ordinary, radiative, compression-relic and dissipative-tail preparticle seeds for the sole active C-125 microscopic replay.

## Strongest unsupported claim

No superseding channel-complete microscopic constitution H_C_to_D_v2, full nonequilibrium thermal history H_D_to_E_v2, source-owned nucleosynthesis H_E_to_F_v2, child-ready post-nuclear plasma/opacity H_F_to_G_v2, physical recombination/visibility/last-scattering state, or empirical agreement is yet established by the repaired lineage.

## Immediate objective

Execute the recovered source-owned nuclear network with isotope identities, rates, abundances, covariance and plasma-ready output.

## Required deliverables

- modules/E/runs/<RUN_ID>/OUTPUT_CONTRACT.json
- modules/E/runs/<RUN_ID>/SOURCE_REGISTER.json
- modules/E/runs/<RUN_ID>/GATE_RESULTS.json
- modules/E/runs/<RUN_ID>/INDEPENDENT_VERIFICATION.md
- modules/E/runs/<RUN_ID>/CLOSEOUT.md
- versioned superseding H_E_to_F_v2 handoff and manifest

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
- E: `FROZEN` / `MINIMAL_SPINE`
- F: `FROZEN` / `MINIMAL_SPINE`
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
- frozen artifacts: 20
- indexed runs: 18

## Recent runs

- F-150-20260808T013006Z: PASS (F)
- G-160-20260808T021341Z: BLOCKED (G)
- G-160-20260808T051613Z: BLOCKED (G)
- B-115-20260808T060000Z: PASS (B)
- C-125-20260808T061947Z: BLOCKED (C)
- C-125-20260808T063010Z: BLOCKED (C)
- C-125-20260808T063500Z: PASS (C)
- D-135-20260808T163243Z: PASS (D)

## Recent decisions

- REOPEN-D-20260808T164207Z: Reopened Module D from FROZEN/MINIMAL_SPINE at target fidelity PRODUCTION for the authorized superseding lineage.
- PROMOTE-D-FORMALIZED-20260808T164215Z: Promoted Module D from DESIGN to FORMALIZED at PRODUCTION
- PROMOTE-D-IMPLEMENTED-20260808T164215Z: Promoted Module D from FORMALIZED to IMPLEMENTED at PRODUCTION
- PROMOTE-D-VERIFIED-20260808T164215Z: Promoted Module D from IMPLEMENTED to VERIFIED at PRODUCTION
- PROMOTE-D-PHYSICALLY_EXECUTED-20260808T164215Z: Promoted Module D from VERIFIED to PHYSICALLY_EXECUTED at PRODUCTION
- PROMOTE-D-INDEPENDENTLY_REPRODUCED-20260808T164215Z: Promoted Module D from PHYSICALLY_EXECUTED to INDEPENDENTLY_REPRODUCED at PRODUCTION
- PROMOTE-D-FROZEN-20260808T164215Z: Promoted Module D from INDEPENDENTLY_REPRODUCED to FROZEN at PRODUCTION
- ADVANCE-D-135-20260808T164215Z: Marked D-135 PASS and activated E-145

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
