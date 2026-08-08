# Module B Wolfram Verification

## Scope

This record verifies exact and representative finite-relational consequences of the authorized Module B equations. Wolfram is used as an independent symbolic/numerical engine, not as a physical source.

## Exact representative branch

For

```text
W = {{0,2,0},{1,0,3},{0,1,0}}
delta = 5/2
x- = {3,-1,2}
```

Wolfram returned

```text
L = {{3,-3,0},{-3,7,-4},{0,-4,4}}
Qimp = {{41,22,16},{22,33,24},{16,24,39}}/79
x+ = {133,81,102}/79
```

and verified:

- `Qimp . {1,1,1} = {1,1,1}`;
- all nonconstant eigenvalues lie strictly between zero and one;
- `(I + ell_delta L) x+ = x-` exactly;
- the variational gradient vanishes at `x+`;
- the Hessian eigenvalues are positive;
- local continuity residual is exactly zero;
- total carrier change is exactly zero;
- nonconstant carrier energy decreases;
- the compression progress `chi` is positive;
- effective-resistance distances are finite and positive on distinct vertices.

## Four-sector projectors

On the doubled state and doubled directed-current carrier, Wolfram verified exactly:

```text
sum_a P_a = I
P_a^2 = P_a
P_a P_b = 0  for a != b
```

This establishes completeness, idempotence, and mutual orthogonality of the four genesis projectors at the declared algebraic scope.

## Clock

For

```text
q(u) = exp(-alpha u)/delta
Srec(u) = -log(1-q) - q log(q)/(1-q)
```

Wolfram derived

```text
dSrec/du = -alpha delta exp(alpha u) (alpha u + log delta)
            /(delta exp(alpha u)-1)^2
```

which is strictly negative for `alpha>0`, `delta>1`, and `u>=0`. It also verified `Srec -> 0` as `u -> infinity`, so the logarithmic intrinsic clock is strictly increasing and unbounded.

## Relic and tail checks

Wolfram verified:

- `Gcomp = Log[I + ell_delta L]` has one zero constant-mode eigenvalue and positive nonconstant eigenvalues;
- `Exp[-tau Gcomp]` forms the expected semigroup;
- covariance transformed by `Qimp Sigma Qimp^T` remains positive semidefinite in the representative arbitrary-precision example;
- the route-even tail vanishes for reciprocal directed weights;
- the route-odd and route-even pair seeds separate net flux from nonreciprocal directed content.

## Limitations

These calculations verify the algebra and representative branch behavior. They do not prove:

- mature Lorentzian spacetime;
- a continuum stress-energy tensor;
- unique SI scales;
- particle, photon, dark-matter, or dark-energy identities;
- empirical realization in nature.

Those claims remain outside Module B.