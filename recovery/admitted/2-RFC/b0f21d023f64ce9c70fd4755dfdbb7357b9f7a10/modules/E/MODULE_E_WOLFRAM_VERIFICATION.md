# Module E Wolfram and Independent Verification

## Scope

This file records algebraic and finite-realization checks for Module E. It does not convert software output into empirical nuclear truth.

## Exact stoichiometric checks

A representative internally declared light-nuclide network was encoded over

```text
n, p, D, T, He3, He4, Li6, Li7, Be7, gamma
```

with twelve forward route families covering radiative capture, exchange, Li/Be conversion, and Li7 destruction.

For the stoichiometric matrix `N`, Wolfram returned

```text
A . N  = {0,...,0}
Z . N  = {0,...,0}
Nn . N = {0,...,0}
rank(N) = 7
```

where `A`, `Z`, and `Nn=A-Z` are baryon, proton/charge, and neutron ledgers. Thus the representative strong/electromagnetic route set closes all three ledgers exactly.

## Binding/Q-value identity

For reactant and product masses written as

```text
M = Z mp + N mn - B
```

and a route conserving proton and neutron counts, symbolic simplification gives

```text
Q = sum(B_products) - sum(B_reactants)
```

so mass differences, thresholds, and binding release are one registry identity rather than independent inputs.

## Detailed balance and entropy production

For positive forward and reverse currents `Jf,Jb`, Wolfram verified

```text
(Jf-Jb) (Log[Jf]-Log[Jb]) >= 0
```

which is the pairwise entropy-production term used by the generated reversible network.

## Positive normalized finite process

For the representative generator

```text
Q = {{-3,1,0},{3,-3,2},{0,2,-2}}
```

Wolfram verified:

```text
column sums = {0,0,0}
Exp[Q].{1,0,0}
 = {0.187793249261720..., 0.443695277416497..., 0.368511473321782...}
sum = 1
minimum component > 0
nonstationary eigenvalues = {-5.414213562..., -2.585786437..., 0}
```

This checks a positive normalized relaxation example with one stationary mode.

## Independent implementation

An independent SciPy/NumPy implementation checked:

```text
MODULE_E_INDEPENDENT_CHECK: PASS
stoichiometric_A_Z_N_conservation=PASS
markov_positivity_normalization=PASS
restart_identity=PASS
detailed_balance_entropy=PASS
sensitivity_frechet_check=PASS
rank=7
p1=[0.18779325, 0.44369528, 0.36851147]
```

The sensitivity check compared a centered finite difference of `exp(Q+epsilon E)` with the matrix-exponential Frechet derivative.

## Interpretation boundary

These checks support:

- exact conservation algebra;
- consistency of binding and reaction Q values;
- reversible entropy-production sign;
- positivity and normalization of a finite generator;
- restart identity;
- tangent/sensitivity implementation.

They do not establish:

- measured isotope masses or bindings;
- measured cross sections or lifetimes;
- observed primordial abundances;
- public BBN-code agreement;
- continuum nuclear-field-theory precision.

The physical Module E claim remains conditional on the frozen RFC parent, the generated finite operators, declared branches, and explicit refinement bounds.