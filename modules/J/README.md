# Module J — Primordial Covariance, Linear Spectra, and Finite-Volume Fields

**Objective:** Generate the actual covariance, linear spectra, phases/seeds, and finite-volume field realization consumed by nonlinear gravity.

**Parents:** HI

**Children:** K

**N-body mode:** `RELATIONAL_GRAMMAR_ACTIVE`

## Required outputs

- positive-semidefinite covariance
- linear spectra and growth
- finite-volume fields
- phase/seed provenance
- promotion witnesses
- restartable P_J_to_K

## Mandatory gates

- covariance PSD
- reality/Hermitian conditions
- resolution and volume tests
- no public initial-condition file
- independent field reconstruction

## Forbidden shortcuts

- synthetic representative covariance as physical parent
- selecting seeds for observational agreement

## Claim boundary

One realized RFC linear universe and its uncertainty state.

## Working rule

Create run workspaces only with `python tools/rfc.py new-run J`. State is held centrally in `STATE.json`.
