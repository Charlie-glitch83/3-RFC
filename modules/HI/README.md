# Module HI — Transfer Operator Instantiation

**Objective:** Instantiate the frozen universal transfer operator on the realized background without changing either parent's law.

**Parents:** HU, I

**Children:** J

**N-body mode:** `RELATIONAL_GRAMMAR_ACTIVE`

## Required outputs

- instantiated transfer system
- mode/eigenstructure
- gauge/frame mapping
- error/covariance propagation
- H_HI_to_J

## Mandatory gates

- exact parent hashes
- no retune of HU or I
- operator-domain compatibility
- independent reconstruction

## Forbidden shortcuts

- refitting transfer coefficients after seeing spectra

## Claim boundary

RFC linear transfer realization.

## Working rule

Create run workspaces only with `python tools/rfc.py new-run HI`. State is held centrally in `STATE.json`.
