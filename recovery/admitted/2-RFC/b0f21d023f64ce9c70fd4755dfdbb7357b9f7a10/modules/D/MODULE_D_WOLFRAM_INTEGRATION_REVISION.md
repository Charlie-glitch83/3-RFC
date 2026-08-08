# Module D — Wolfram Integration Revision

Binding revision to `MODULE_D_DETAILED_SCIENTIFIC_REPAIR_PLAN.md`; governed by `architecture/2RFC_WOLFRAM_INTEGRATION_RULES.md`.

## Authorized work

Use Wolfram to formulate and solve the nonequilibrium thermal system:

- Boltzmann, quantum-kinetic, fluid, and moment equations;
- collision integrals, conserved null spaces, and detailed balance;
- finite-temperature masses, rates, potentials, and phase-transition conditions derived from the Module C laws;
- stiffness, asymptotic regimes, freeze-out, annihilation, entropy redistribution, neutrino transport, and visible-dark exchange;
- asymmetry activation, washout, survival, and sensitivity;
- event detection for transition and decoupling surfaces;
- Jacobians, sparse structure, covariance, and adjoint sensitivities.

## Required methods

Use symbolic reduction before numerics, stiff solvers with arbitrary precision when needed, positivity-preserving variables, residual checks, conserved-charge monitors, and independent equilibrium and asymptotic limits.

## Forbidden use

Wolfram may not import a standard thermal timeline, fitted reaction history, public freeze-out temperature, or conventional cosmological normalization as a generative input.

## Completion addition

Every transition, decoupling, and freeze-out exported to Module E must be reproducible from the frozen equations, with solver-convergence, conservation, branch, and uncertainty evidence.