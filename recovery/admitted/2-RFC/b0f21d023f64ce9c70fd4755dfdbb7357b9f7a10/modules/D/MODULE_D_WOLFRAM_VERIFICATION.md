# Module D Wolfram Verification

## Scope

Wolfram was used only to verify exact algebraic consequences of the completed finite-relational Module D equations. It supplied no cosmological model, measured constant, particle table, transition temperature, baryon ratio, neutrino history, abundance, or public target.

## Exact checks

### 1. Markov-generator conservation

For the representative three-state route generator

\[
Q=\begin{pmatrix}
-a&b&0\\
a&-(b+c)&d\\
0&c&-d
\end{pmatrix},
\qquad a,b,c,d>0,
\]

Wolfram verified that every column sum is exactly zero.

For the normalized stationary state

\[
\pi=\frac{(bd,ad,ac)}{bd+ad+ac},
\]

Wolfram returned

```text
Q.pi = {0,0,0}
Total[pi] = 1
```

For `{a,b,c,d}={2,3,5,7}`, the eigenvalues are

\[
0,
\quad
\frac{-17+\sqrt{109}}2,
\quad
\frac{-17-\sqrt{109}}2,
\]

so the nonstationary spectrum has strictly negative real part.

### 2. Positive normalized propagator

For the same exact branch, Wolfram evaluated \(e^{Qt}\) and verified at \(t=1\):

```text
column sums = {1,1,1}
minimum propagator entry = 0.2112318899... > 0
```

This independently confirms normalization and positivity for the representative classical restriction.

### 3. Detailed-balance entropy term

Wolfram reduced the elementary entropy-production term to

\[
(x-y)\log(x/y)\ge0
\]

for positive forward and reverse currents. This follows analytically because \(\log\) is strictly increasing.

### 4. Lindblad trace preservation

For a two-level dephasing jump with

\[
\dot\rho=\gamma(\sigma_z\rho\sigma_z-\rho),
\]

Wolfram returned

```text
Tr[dot rho] = 0
```

and the off-diagonal terms decay as \(-2\gamma\rho_{12}\) and \(-2\gamma\rho_{21}\).

### 5. Gibbs energy monotonicity

For a two-level spectrum \(\{0,\epsilon\}\), Wolfram derived

\[
E(\beta)=\frac{\epsilon}{1+e^{\beta\epsilon}},
\]

\[
\frac{dE}{d\beta}
=-\frac{\epsilon^2}{4}\operatorname{sech}^2(\beta\epsilon/2)<0
\]

for \(\epsilon>0\). Thus the moment-matching inverse temperature is unique wherever the target energy lies strictly inside the spectral interval.

### 6. Two-state relaxation gap

For

\[
Q_2=\begin{pmatrix}-a&b\\a&-b\end{pmatrix},
\]

the eigenvalues are

\[
0,
\qquad -(a+b).
\]

Therefore the intrinsic relaxation gap used by the Module D freeze-out construction is exactly \(a+b\) in this representative route pair.

## Independent implementation

A separate SciPy/NumPy implementation reproduced:

```text
MODULE_D_INDEPENDENT_CHECK: PASS
markov_normalization_positivity=PASS
relative_entropy_monotonicity=PASS
charge_energy_no_loss=PASS
lindblad_trace_positivity=PASS
gibbs_temperature_uniqueness=PASS
freezeout_gap=a+b
```

For the representative initial state \((1,0,0)\), it obtained

```text
p(1) = {0.48583430, 0.30293381, 0.21123189}
KL(initial || pi) = 0.7621400520...
KL(t=2 || pi) = 1.094646866e-6
```

The relative entropy decreased monotonically over the sampled interval.

## Independent analytic checks

The load-bearing results do not depend on Wolfram:

- zero column sums imply probability conservation;
- nonnegative off-diagonal rates generate a positive stochastic semigroup;
- Lindblad form is trace preserving and completely positive;
- exact commuting charges are conserved by cyclicity of trace;
- detailed-balance entropy production is nonnegative term by term;
- Gibbs energy obeys \(dE/d\beta=-\operatorname{Var}(H)\le0\);
- a two-state rate generator has relaxation gap equal to the sum of its forward and reverse rates.

## Interpretation boundary

These checks verify algebra and representative finite realizations. They do not establish measured thermal history, empirical transition temperatures, observed baryon asymmetry, public neutrino values, continuum kinetic precision, primordial abundances, or empirical truth. The scientific derivation and boundaries are stated in `science/THERMAL_EVOLUTION.md` and `proofs/THERMAL_EVOLUTION.md`.