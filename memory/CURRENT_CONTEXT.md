# Current Context

Generated: 2026-08-07T04:16:49.145626+00:00

## Project truth

- Status: `FAIL_REQUIRES_ANALYSIS`
- Generation mode: `GENERATION_SEALED`
- Active work unit: `E-140` — Close Module E: Primordial Nuclear Network
- Current module: `E`
- Last verified commit: `1813f323211236953b20b29d55e58d958c5ffabd`

## Strongest supported claim

The exact frozen C microscopic parent generates a positive, conserved, source-owned dimensionless nonequilibrium relaxation history under the normalized C projector, with monotonic Shannon entropy growth, an intrinsic collision-count clock, ordered internal relaxation events, a no-loss dimensionless disequilibrium-energy/RFL-memory ledger, converged BDF execution, restart, clean replay, and independent analytic reconstruction at MINIMAL_SPINE fidelity.

## Strongest unsupported claim

No source-owned physical nuclear species graph, reaction-rate law, nuclear energy ledger, primordial isotope abundance trajectory, isotope covariance, or freeze-out state has been derived. E is blocked at E_SOURCE_OWNED_NUCLEAR_SPECIES_AND_RATE_LAW; historical/proxy abundance-target results are not generative parents.

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
- frozen artifacts: 11
- indexed runs: 10

## Recent runs

- XWALK-030-20260806T130603Z: PASS (THEORY)
- REC-040-20260806T135256Z: PASS (RECOVERY)
- FRONTIER-050-20260806T142549Z: PASS (AUDIT)
- A-100-20260806T173458Z: PASS (A)
- B-110-20260807T002248Z: PASS (B)
- C-120-20260807T032543Z: PASS (C)
- D-130-20260807T035820Z: PASS (D)
- E-140-20260807T041433Z: BLOCKED (E)

## Recent decisions

- ADVANCE-C-120-20260807T034953Z: Marked C-120 PASS and activated D-130
- PROMOTE-D-FORMALIZED-20260807T040337Z: Promoted Module D from DESIGN to FORMALIZED at MINIMAL_SPINE
- PROMOTE-D-IMPLEMENTED-20260807T040337Z: Promoted Module D from FORMALIZED to IMPLEMENTED at MINIMAL_SPINE
- PROMOTE-D-VERIFIED-20260807T040337Z: Promoted Module D from IMPLEMENTED to VERIFIED at MINIMAL_SPINE
- PROMOTE-D-PHYSICALLY_EXECUTED-20260807T040337Z: Promoted Module D from VERIFIED to PHYSICALLY_EXECUTED at MINIMAL_SPINE
- PROMOTE-D-INDEPENDENTLY_REPRODUCED-20260807T040337Z: Promoted Module D from PHYSICALLY_EXECUTED to INDEPENDENTLY_REPRODUCED at MINIMAL_SPINE
- PROMOTE-D-FROZEN-20260807T040337Z: Promoted Module D from INDEPENDENTLY_REPRODUCED to FROZEN at MINIMAL_SPINE
- ADVANCE-D-130-20260807T040612Z: Marked D-130 PASS and activated E-140

## Recent failures

- SRC-010-FIREWALL-TOKEN-BOUNDARY: The mechanical scanner matched DESI inside design and public_data inside a NONE declaration key.
- SRC-010-RUN-ID-STATE-DRIFT: Generated timestamped run workspace existed but current_run and RUN_INDEX were not retained by the startup commit; verifier now resolves and registers the sole governed SRC-010 workspace.
- AUTH-020-FIREWALL-PROTOCOL-WORDING: The mechanical firewall scanner matched protocol wording inside AUTHORITY_SOURCE_TRACE.json even though no external target values were used. The trace wording was normalized without changing sources, definitions, claims, or gates.
- XWALK-030-MISSING-PROVENANCE-AND-MD: The prebuilt crosswalk lacked required source hashes and evidence states, and its Markdown deliverable was absent. Provenance and review structure were added without changing original dispositions.
- REC-040-FIREWALL-AUDIT-WORDING: The mechanical scanner matched external-comparison names and protocol wording in temporary discovery and audit records. Temporary discovery artifacts were removed after incorporation and audit wording normalized without changing source hashes, classifications, gates, or claim scope.
- REC-040-DISCOVERY-ORDERING: The temporary discovery record was removed before a later replay attempted to consume it. The record is now reconstructed from all exact remote refs before recovery and removed only after incorporation.
- REC-040-VERIFIED-SHA-RACE: Concurrent successful replays caused formal transition bookkeeping to record an earlier valid evidence SHA instead of the final clean replay SHA. Provenance was corrected to the final verified commit without changing run evidence, classifications, gates, result, or next-child authorization.
- E-140-20260807T041649Z: Frozen source/rate audit found no lawful target-blind physical nuclear species/reaction/rate object; E remains active and blocked for analysis.

## Resume commands

```bash
python tools/rfc.py doctor
python tools/rfc.py next
```
