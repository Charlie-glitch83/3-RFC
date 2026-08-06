# Failure and Repair Policy

## Rule

```text
preserve evidence of failure != preserve failed mechanism or outcome
```

Every failure record states:

- exact run and artifact hashes;
- failed gate;
- whether the failure is scientific, implementation, numerical, source, or infrastructure;
- earliest affected object;
- whether a correction changes frozen science;
- required replay scope;
- strongest claim still supported.

## Implementation-only correction

May change implementation details only. It may not change definitions, source objects, equations, coefficients, tests, expected outcomes, tolerances, gates, falsifiers, or claim scope. Rerun the full frozen matrix.

## Scientific revision

Creates a new versioned run with a new frozen pre-execution specification. The failed run remains immutable.

## No curve-fitting repair

A correction selected because it moves toward a known public value is not admitted as a generative repair.
