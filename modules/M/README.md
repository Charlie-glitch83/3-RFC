# Module M — Stellar/Explosive Nucleosynthesis, Chemistry, Dust, Cooling, and Opacity

**Objective:** Generate element/isotope production, chemical enrichment, dust, cooling, opacity, and composition-dependent returns from the executed stellar history.

**Primary parents:** L

**Causal recurrence returns:** KLM

**Children:** KLM, N

**N-body mode:** `RELATIONAL_GRAMMAR_ACTIVE`

## Required outputs

- stellar/explosive yields with provenance
- element/isotope histories
- galactic/cosmic chemical evolution
- dust and molecular state
- cooling/opacity returns
- M_to_K and M_to_L interfaces

## Mandatory gates

- nuclear/species conservation
- yield source/derivation audit
- network convergence
- return causality and earliest-change replay
- independent reconstruction

## Forbidden shortcuts

- fitting yields to solar abundances
- using public abundance patterns during generation
- dropping covariance

## Claim boundary

Generated RFC chemical and composition state.

## Working rule

Create run workspaces only with `python tools/rfc.py new-run M`. State is held centrally in `STATE.json`.
