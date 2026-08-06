# Module KLM — Causal K–L–M Recurrence and Classification

**Objective:** Replay causal backreaction among gravity, baryons/stars, and chemistry until the system reaches a lawfully classified state without forcing convergence.

**Parents:** K, L, M

**Children:** K, L, M, N

**N-body mode:** `DIRECT_MANY_BODY_ACTIVE`

## Required outputs

- iteration history
- causal return witnesses
- earliest affected checkpoints
- conservation/covariance updates
- restart/replay
- classification: fixed point, finite cycle, attractor, branch family, obstruction, or nonconvergence
- certified K*, L*, M* or certified alternative

## Mandatory gates

- no target-driven stopping
- componentwise convergence metrics
- return ownership
- clean replay
- independent implementation
- preserved failed attempts

## Forbidden shortcuts

- promoting reduced dimensionless F0 to physical recurrence
- forcing a fixed point
- ignoring nonconvergent lawful behavior

## Claim boundary

Physical coupled-universe classification at executed fidelity.

## Working rule

Create run workspaces only with `python tools/rfc.py new-run KLM`. State is held centrally in `STATE.json`.
