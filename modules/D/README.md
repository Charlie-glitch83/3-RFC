# Module D — Nonequilibrium Thermal and Phase History

**Objective:** Evolve the microscopic state through nonequilibrium thermodynamics, transport, phase changes, entropy production, and clock/frame-consistent expansion.

**Parents:** C

**Children:** E

**N-body mode:** `RELATIONAL_GRAMMAR_ACTIVE`

## Required outputs

- temperature and distribution histories
- phase/event ledger
- transport and collision operators
- entropy and conservation ledger
- uncertainty/covariance
- H_D_to_E

## Mandatory gates

- positive distributions
- energy/charge conservation
- event ordering
- stiff-solver convergence
- restart and independent reconstruction

## Forbidden shortcuts

- using a standard thermal history as initial data
- fitting transition temperatures to observations

## Claim boundary

Generated RFC thermal history, not yet primordial abundances.

## Working rule

Create run workspaces only with `python tools/rfc.py new-run D`. State is held centrally in `STATE.json`.
