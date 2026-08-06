# Module P — Blind Empirical Comparison

**Objective:** Ingest public evidence only after O, apply preregistered observation operators/statistics, and classify survival, tension, or falsification without retuning.

**Parents:** O

**Children:** none

**N-body mode:** `RELATIONAL_GRAMMAR_ACTIVE`

## Required outputs

- version-locked public datasets
- preregistered statistics
- covariance/selection/window treatment
- multi-probe residuals and likelihoods
- baseline comparators
- tension/falsifier ledger
- blind validation report

## Mandatory gates

- O hash unchanged
- no target deletion
- no covariance inflation
- no branch/seed/tolerance changes
- reproducible independent comparison

## Forbidden shortcuts

- feeding residuals back to generation
- post-hoc statistic selection
- calling internal closure validation

## Claim boundary

Empirical survival, tension, or falsification of the frozen universe at tested scope.

## Working rule

Create run workspaces only with `python tools/rfc.py new-run P`. State is held centrally in `STATE.json`.
