# Module E — Primordial Nuclear Network

**Objective:** Execute a source-owned reaction network to generate primordial isotope abundances and their full uncertainty state.

**Parents:** D

**Children:** F

**N-body mode:** `RELATIONAL_GRAMMAR_ACTIVE`

## Required outputs

- reaction graph and rates with source lineage
- abundance trajectories
- isotope covariance
- conservation and positivity ledger
- freeze-out/event witnesses
- H_E_to_F

## Mandatory gates

- baryon/charge/energy accounting
- network convergence
- rate-source audit
- no scalar-channel collapse
- withheld reaction and independent implementation checks

## Forbidden shortcuts

- targeting public abundances
- inheriting the old Li7 failure
- using fitted abundance corrections

## Claim boundary

Internally generated primordial nuclear state; observations remain sealed.

## Working rule

Create run workspaces only with `python tools/rfc.py new-run E`. State is held centrally in `STATE.json`.
