# Current Context

Generated: 2026-08-07T15:59:04.858523+00:00

## Project truth

- Status: `FAIL_REQUIRES_ANALYSIS`
- Generation mode: `GENERATION_SEALED`
- Active work unit: `E-140` — Close Module E: Primordial Nuclear Network
- Current module: `E`
- Last verified commit: `44ed126d494f41e0448e5e751b3b17b5d8f1848e`

## Strongest supported claim

Generated RFC dimensionless nonequilibrium thermal/phase history at MINIMAL_SPINE fidelity from the exact C parent, including conservative transport, positive distributions, entropy production, internal conjugate temperature, thermodynamic state-volume expansion, a parameter-free RFL-memory balance phase event, inherited uncertainty envelope, restart, clean replay, and independent reconstruction.

## Strongest unsupported claim

No source-owned numerical nuclear reaction-rate law, nuclear energy ledger, physical primordial isotope trajectory, isotope covariance, or physical freeze-out state has been derived. E is blocked at E_SOURCE_OWNED_NUCLEAR_RATE_LAW; historical/proxy abundance-target results are not generative parents.

## Immediate objective

Execute a source-owned reaction network to generate primordial isotope abundances and their full uncertainty state.

## Required deliverables

- modules/E/runs/<RUN_ID>/RUN_PLAN.md
- modules/E/runs/<RUN_ID>/SOURCE_REGISTER.json
- modules/E/runs/<RUN_ID>/GATE_RESULTS.json
- modules/E/runs/<RUN_ID>/INDEPENDENT_VERIFICATION.md
- modules/E/runs/<RUN_ID>/CLOSEOUT.md
- frozen output packet and artifact registry entries

## Mandatory gates

- baryon/charge/energy accounting
- network convergence
- rate-source audit
- no scalar-channel collapse
- withheld reaction and independent implementation checks

## Module states

- A: `FROZEN` / `PRODUCTION`
- B: `FROZEN` / `MINIMAL_SPINE`
- C: `FROZEN` / `MINIMAL_SPINE`
- D: `FROZEN` / `MINIMAL_SPINE`
- E: `DESIGN` / `UNSTARTED`
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
- frozen artifacts: 14
- indexed runs: 13

## Recent runs

- A-100-20260806T173458Z: PASS (A)
- B-110-20260807T002248Z: PASS (B)
- C-120-20260807T032543Z: PASS (C)
- D-130-20260807T044911Z: FAIL (D)
- D-130-20260807T045646Z: BLOCKED (D)
- D-130-20260807T053432Z: PASS (D)
- E-140-20260807T142445Z: BLOCKED (E)
- E-140-20260807T155635Z: CREATED (E)

## Recent decisions

- COMMIT-44ed126d494f: Verified D130 closeout commit, fetched artifacts, diff, tests, doctor and firewall.
- PROMOTE-D-FORMALIZED-20260807T135107Z: Promoted Module D from DESIGN to FORMALIZED at MINIMAL_SPINE
- PROMOTE-D-IMPLEMENTED-20260807T135107Z: Promoted Module D from FORMALIZED to IMPLEMENTED at MINIMAL_SPINE
- PROMOTE-D-VERIFIED-20260807T135107Z: Promoted Module D from IMPLEMENTED to VERIFIED at MINIMAL_SPINE
- PROMOTE-D-PHYSICALLY_EXECUTED-20260807T135108Z: Promoted Module D from VERIFIED to PHYSICALLY_EXECUTED at MINIMAL_SPINE
- PROMOTE-D-INDEPENDENTLY_REPRODUCED-20260807T135108Z: Promoted Module D from PHYSICALLY_EXECUTED to INDEPENDENTLY_REPRODUCED at MINIMAL_SPINE
- PROMOTE-D-FROZEN-20260807T135108Z: Promoted Module D from INDEPENDENTLY_REPRODUCED to FROZEN at MINIMAL_SPINE
- ADVANCE-D-130-20260807T135108Z: Marked D-130 PASS and activated E-140

## Recent failures

- SRC-010-FIREWALL-TOKEN-BOUNDARY: The mechanical scanner matched DESI inside design and public_data inside a NONE declaration key.
- SRC-010-RUN-ID-STATE-DRIFT: Generated timestamped run workspace existed but current_run and RUN_INDEX were not retained by the startup commit; verifier now resolves and registers the sole governed SRC-010 workspace.
- AUTH-020-FIREWALL-PROTOCOL-WORDING: The mechanical firewall scanner matched protocol wording inside AUTHORITY_SOURCE_TRACE.json even though no external target values were used. The trace wording was normalized without changing sources, definitions, claims, or gates.
- XWALK-030-MISSING-PROVENANCE-AND-MD: The prebuilt crosswalk lacked required source hashes and evidence states, and its Markdown deliverable was absent. Provenance and review structure were added without changing original dispositions.
- REC-040-FIREWALL-AUDIT-WORDING: The mechanical scanner matched external-comparison names and protocol wording in temporary discovery and audit records. Temporary discovery artifacts were removed after incorporation and audit wording normalized without changing source hashes, classifications, gates, or claim scope.
- REC-040-DISCOVERY-ORDERING: The temporary discovery record was removed before a later replay attempted to consume it. The record is now reconstructed from all exact remote refs before recovery and removed only after incorporation.
- REC-040-VERIFIED-SHA-RACE: Concurrent successful replays caused formal transition bookkeeping to record an earlier valid evidence SHA instead of the final clean replay SHA. Provenance was corrected to the final verified commit without changing run evidence, classifications, gates, result, or next-child authorization.
- E-140-20260807T144032Z: Frozen rate-source audit found no lawful target-blind provenance-bound E nuclear rate law; physical E execution blocked.

## Resume commands

```bash
python tools/rfc.py doctor
python tools/rfc.py next
```
