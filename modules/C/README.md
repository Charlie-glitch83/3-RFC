# Module C — Microscopic Constitution

**Objective:** Derive and execute the microscopic field, particle, interaction, mass, mixing, and prethermal population content from the first physical state.

**Parents:** B

**Children:** D

**N-body mode:** `RELATIONAL_GRAMMAR_ACTIVE`

## Required outputs

- typed fields and excitations
- interaction and symmetry structure
- mass/mixing generation or lawful branch family
- charge and conservation ownership
- prethermal populations and covariance
- H_C_to_D

## Mandatory gates

- units and dimensions
- symmetry/constraint closure
- positivity/unitarity or declared alternative
- no Standard Model label without derivation or correspondence theorem
- independent symbolic and numerical checks

## Forbidden shortcuts

- importing measured masses/couplings
- assigning familiar particles by resemblance
- hiding undetermined coefficients

## Claim boundary

RFC microscopic constitution at the executed scope; empirical identity remains for Module P.

## Working rule

Create run workspaces only with `python tools/rfc.py new-run C`. State is held centrally in `STATE.json`.
