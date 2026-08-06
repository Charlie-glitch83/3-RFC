# Module F — Post-Nuclear Plasma and Radiation Persistence

**Objective:** Carry isotope, plasma, radiation, neutrino, and transport states from nucleosynthesis into recombination without losing lineage or covariance.

**Parents:** E

**Children:** G

**N-body mode:** `RELATIONAL_GRAMMAR_ACTIVE`

## Required outputs

- plasma composition and ionization state
- radiation/neutrino persistence
- opacity and transport state
- source-transfer ownership
- H_F_to_G

## Mandatory gates

- charge neutrality where derived
- energy and particle accounting
- covariance positive semidefinite
- replay from E

## Forbidden shortcuts

- resetting to a textbook plasma
- dropping isotope or uncertainty channels

## Claim boundary

Post-nuclear RFC plasma state.

## Working rule

Create run workspaces only with `python tools/rfc.py new-run F`. State is held centrally in `STATE.json`.
