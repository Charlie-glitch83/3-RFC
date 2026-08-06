# Module G — Nonequilibrium Recombination and Last-Scattering State

**Objective:** Generate recombination, visibility, opacity, and radiation-surface histories from the physical plasma state.

**Parents:** F

**Children:** HU, I

**N-body mode:** `RELATIONAL_GRAMMAR_ACTIVE`

## Required outputs

- ionization/recombination histories
- visibility and optical-depth functions
- radiation surface
- covariance and restart
- H_G_to_HU
- H_G_to_I

## Mandatory gates

- rate and opacity lineage
- normalization and positivity
- stiff convergence
- independent reconstruction

## Forbidden shortcuts

- using public CMB targets to choose recombination parameters
- declaring a readiness score a CMB surface

## Claim boundary

Generated RFC last-scattering state, not observed CMB agreement.

## Working rule

Create run workspaces only with `python tools/rfc.py new-run G`. State is held centrally in `STATE.json`.
