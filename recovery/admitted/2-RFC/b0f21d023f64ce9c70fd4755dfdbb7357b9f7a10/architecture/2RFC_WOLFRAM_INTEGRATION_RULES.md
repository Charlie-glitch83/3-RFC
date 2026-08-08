# 2-RFC Wolfram Integration Rules

## Scientific role

The Wolfram plugin is an authorized computational instrument for the A–Q repair and implementation chain.

It may be used to:

- manipulate source-derived equations symbolically;
- prove algebraic, combinatorial, spectral, variational, conservation, limit, and asymptotic consequences;
- solve or approximate declared ODE, PDE, DAE, integral, eigenvalue, optimization, graph, and stochastic systems;
- perform arbitrary-precision and interval-aware numerical work;
- propagate uncertainty, covariance, sensitivities, and Jacobians;
- test independent formulations, limiting cases, branches, and falsifiers;
- build observation operators and statistical comparisons inside Module P;
- analyze terminal dynamics, singularities, asymptotes, and cycle maps inside Module Q.

It is not a scientific source for RFC.

## Source and no-retune firewall

Every Wolfram input must come from:

- the active module’s sealed parent packet;
- the valid scientific sources named by that module plan;
- equations or transformations derived transparently from those sources;
- public evidence only inside Module P and only under its frozen dataset-role rules.

Wolfram may not supply:

- missing RFC laws;
- hidden constants or conventional best-fit parameters;
- public-data-derived targets for Modules A–O or Q;
- branch selection based on empirical success;
- post-hoc amplitude rescaling, curve fitting, or parameter repair;
- a familiar external cosmology substituted for an unresolved RFC equation;
- a physical interpretation that is not already derived by the module.

`WolframAlpha`, curated formulas, entity data, and named scientific models may be used only as explicitly declared benchmark, dimensional, or comparison objects. They may not enter generation unless the module already authorizes that exact object as an interface law.

## Required computational record

Every load-bearing Wolfram result must retain:

```text
module and claim identity
parent-state identity
exact input equations
assumptions and domains
units and conventions
branch conditions
Wolfram Language code or natural-language query
exact output where available
numerical output and precision
error or residual bounds
uncertainty and covariance contribution
independent-check method
scientific interpretation
scope and unresolved conditions
```

Assumptions must be explicit. Hidden assumptions introduced by broad simplification are forbidden.

## Exact-first and precision rules

Use exact integers, rationals, algebraic numbers, and symbolic parameters whenever the problem permits.

Numerical work must declare:

- working precision;
- accuracy and precision goals;
- solver method where material;
- domain and event handling;
- stiffness or conditioning diagnostics;
- convergence under precision, tolerance, resolution, and formulation changes;
- interval, residual, or backward-error bounds when load bearing.

Machine precision alone may not establish a theorem-level identity or a near-singular terminal result.

## Independent verification

Wolfram is an independent derivation and verification engine, but it cannot be the sole witness for every mandatory claim.

At least one materially independent check is required for load-bearing results, chosen from:

- analytic derivation;
- a second Wolfram formulation using different mathematics;
- an independent numerical implementation;
- exact limiting-case recovery;
- conservation or invariant closure;
- manufactured solutions;
- direct-versus-transfer, local-versus-global, or finite-versus-continuum overlap.

Agreement must cover the scientific object actually claimed—not only one favorable scalar.

## Disagreement and failure rule

When Wolfram disagrees with the source derivation, another implementation, a conservation law, or a required limit:

1. stop the affected claim;
2. localize the disagreement to equation, assumption, branch, representation, precision, or implementation;
3. preserve all competing outputs and uncertainty;
4. do not tune the physical model to force agreement;
5. classify the result as obstructed, unresolved, or failed until the discrepancy is closed.

For Module P, every mandatory normalized component below `0.95` remains a failure. Wolfram-derived averages or global likelihoods may not hide that failure.

## Connector division of labor

- `WolframLanguageEvaluator`: primary exact, symbolic, numerical, asymptotic, graph, optimization, and statistical engine.
- `WolframAlpha`: benchmark facts, standard-unit transformations, and explicitly authorized external reference calculations; never the generative RFC source.
- `WolframContext`: capability and documentation orientation; never physical evidence.

These rules are scientifically binding on every Module A–Q Wolfram revision.