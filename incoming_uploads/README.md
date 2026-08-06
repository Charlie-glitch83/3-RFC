# Module K — Nonlinear Relational Gravity, Structures, Metric, and Lightcones

**Objective:** Evolve the realized fields into nonlinear structure while preserving relativistic/metric, route, event, branch, conservation, lightcone, and lensing truth.

**Primary parents:** J

**Causal recurrence returns:** KLM

**Children:** L, KLM, N

**N-body mode:** `DIRECT_MANY_BODY_ACTIVE`

## Required outputs

- particle/field nonlinear state
- halos and structures
- metric and Weyl products
- lightcones
- ray/Jacobi/lensing products
- merger/event trees
- return interface to L and KLM

## Mandatory gates

- force/field accuracy
- constraint closure
- mass-energy conservation
- resolution/volume convergence
- restart/replay
- independent critical implementation

## Forbidden shortcuts

- gravity-only toy labeled hyper-realistic
- dropping metric/lightcone truth
- tuning initial phases

## Claim boundary

Nonlinear RFC gravitational universe at stated fidelity.

## Working rule

Create run workspaces only with `python tools/rfc.py new-run K`. State is held centrally in `STATE.json`.
