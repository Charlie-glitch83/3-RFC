# Module F — Wolfram and Independent Verification

## Scope

This file records representative exact and numerical checks for the implemented Module F construction in:

- `science/POST_NUCLEAR_PLASMA.md`
- `proofs/POST_NUCLEAR_PERSISTENCE.md`

These checks verify finite algebraic and implementation consequences. They do not establish measured plasma/atomic precision, public recombination-code agreement, or empirical truth.

## 1. Conservative finite evolution

For the representative column-conservative generator

```wl
Q = {{-2,1,1},{1,-2,1},{1,1,-2}};
```

Wolfram returned:

```text
Total / column-conservation residual: {0,0,0}
Eigenvalues: {(-17-Sqrt[109])/2, (-17+Sqrt[109])/2, 0}
```

The zero mode is the normalization mode and the nonstationary modes are negative in the tested example.

## 2. Relational Gauss law

For an oriented incidence matrix `B`, positive edge response `C`, and `L=B^T C B`, Wolfram verified in a connected neutral example:

```text
Total charge = 0
L . PseudoInverse[L] . rho - rho = {0,0,0}
mean potential = 0
```

This supports the finite claim that a globally neutral charge vector lies in the image of the connected graph Laplacian and has a unique mean-zero pseudoinverse solution.

## 3. Pairwise exchange reciprocity

For a two-sector exchange matrix with paired source and destination entries, Wolfram returned zero total exchange. This checks the algebraic identity

```text
Q_(u->s) + Q_(s->u) = 0
```

for the representative closed pair.

## 4. Damped collective mode

For the representative plasma block

```wl
A = {{0,1},{-wp^2,-nu}};
```

Wolfram returned

```text
{(-nu-Sqrt[nu^2-4 wp^2])/2,
 (-nu+Sqrt[nu^2-4 wp^2])/2}
```

with negative real part for `nu>0`, supporting the stated damping classification. This is a representative stability check, not a measured plasma-frequency calculation.

## 5. Positive transport form

For a negative fast generator on the nonstationary subspace, Wolfram and the independent check verified

```text
-D = J^T L_fast^+ J <= 0
```

or equivalently the Module F convention

```text
D_F = -J^T L_fast^+ J >= 0.
```

## 6. Atomic candidate spectrum and promotion

For the representative two-state candidate Hamiltonian

```wl
Hatom = {{0,g},{g,del}};
```

Wolfram returned

```text
{(del-Sqrt[del^2+4 g^2])/2,
 (del+Sqrt[del^2+4 g^2])/2}
```

and verified `U^T U = I` for the tested rectangular promotion isometry. This checks self-adjoint spectral splitting and no-loss embedding algebra only.

## 7. Positive extinction and entropy-production identities

Wolfram reduced a representative extinction expression to

```text
kappa - kappa*x
```

which is nonnegative for `kappa>=0` and `0<=x<=1`.

For positive paired route currents `r1,r2`, it returned

```text
(r1-r2) Log[r1/r2] >= 0
```

under the positive-domain assumptions, supporting the detailed-balance entropy-production sign used by the reduced route system.

## 8. Covariance propagation

The representative Lyapunov form

```text
SigmaDot = J Sigma + Sigma J^T + Q,
Q >= 0
```

was evaluated with stable `J` and positive-semidefinite inputs. The independent implementation retained positive-semidefinite covariance over the tested step.

## 9. Independent implementation

A separate Python implementation using NumPy and SciPy returned:

```text
MODULE_F_INDEPENDENT_CHECK: PASS
markov_positivity_normalization=PASS
restart_semigroup_identity=PASS
graph_gauss_law=PASS
exchange_reciprocity=PASS
plasma_mode_stability=PASS
positive_transport=PASS
atomic_isometry=PASS
covariance_psd_step=PASS
```

The checks used:

- a three-state conservative generator and matrix exponential;
- split-and-restart versus direct semigroup evolution;
- a weighted three-node graph Laplacian and pseudoinverse;
- paired sector-energy exchange;
- a damped two-dimensional collective-mode block;
- a fast-generator pseudoinverse transport form;
- a rectangular atomic promotion isometry;
- one covariance Lyapunov step.

## 10. What these checks establish

They support the finite claims that the representative constructions possess:

- normalization-preserving positive evolution;
- restart consistency for autonomous subintervals;
- connected neutral graph Gauss-law solvability;
- paired exchange reciprocity;
- damped collective modes under positive damping;
- nonnegative generated transport;
- isometric atomic promotion;
- positive-semidefinite covariance propagation in the tested realization.

## 11. What these checks do not establish

They do not establish:

- empirical plasma or atomic coefficients;
- continuum kinetic or QED precision;
- measured opacity;
- a public recombination history;
- a visibility function or last-scattering surface;
- convergence of every future full-scale implementation;
- empirical agreement.

The exact assumptions, branch conditions, finite support, truncation, and claim boundaries in the science and proof files remain controlling.