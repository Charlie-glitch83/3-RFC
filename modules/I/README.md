# Module I — Realized Background Geometry and Expansion

**Objective:** Generate the universe's realized geometry, expansion, clocks, horizons, and distance structure from the accumulated physical state.

**Parents:** G

**Children:** HI

**N-body mode:** `RELATIONAL_GRAMMAR_ACTIVE`

## Required outputs

- metric/background state
- expansion and clock histories
- horizons and distances
- constraint and conservation ledgers
- covariance
- H_I_to_HI

## Mandatory gates

- equation/constraint derivation
- gauge/frame consistency
- no observed expansion history used as target
- numerical convergence and independent reconstruction

## Forbidden shortcuts

- inserting LambdaCDM best-fit parameters
- calling a standard background RFC-derived without proof

## Claim boundary

Realized RFC background geometry.

## Working rule

Create run workspaces only with `python tools/rfc.py new-run I`. State is held centrally in `STATE.json`.
