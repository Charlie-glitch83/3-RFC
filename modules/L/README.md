# Module L — Baryonic and Stellar Universe

**Objective:** Execute hydro/MHD, radiation, thermochemistry, turbulence, collapse, generated stellar birth, stellar/binary populations, feedback, remnants, accretion, cosmic rays, and radiation sources.

**Primary parents:** K

**Causal recurrence returns:** KLM

**Children:** M, KLM, N

**N-body mode:** `DIRECT_MANY_BODY_ACTIVE`

## Required outputs

- gas/MHD/radiation state
- cloud/core/collapse witnesses
- generated stellar birth measure
- stellar/binary/population histories
- feedback/remnant/accretion state
- L_to_M and L_to_K returns

## Mandatory gates

- mass/momentum/energy/species conservation
- resolution and subgrid convergence
- feedback ownership
- uncertainty/covariance
- replay locality
- independent implementation

## Forbidden shortcuts

- imported IMF as unexplained primitive
- calibrating star formation to public scaling laws
- promoting the old representative first pass to physical L without exact parent execution

## Claim boundary

Physically executed RFC baryonic and stellar state.

## Working rule

Create run workspaces only with `python tools/rfc.py new-run L`. State is held centrally in `STATE.json`.
