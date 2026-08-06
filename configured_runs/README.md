# Configured execution layer

This directory contains two deliberately separate classes of configuration.

## `examples/`

Manufactured implementation checks. They prove that the reusable engines run, preserve their declared invariants, and emit content-addressed outputs. They are not RFC physical results and cannot close a module.

Run every example:

```bash
python tools/run_all_configured_examples.py
```

## `templates/`

Unbound execution templates for the actual A–Q lineage. Every string beginning with `__BIND_` is a hard stop. A template becomes executable only after a work model:

1. derives or recovers the object from exact admitted sources and exact successful parent outputs;
2. records the source path and SHA-256 in the run source register;
3. freezes the value, units, dimensions, expected result, tolerance, and falsifier in the pre-execution lock;
4. replaces all binding tokens;
5. executes `tools/run_configured_solver.py` without changing the frozen science.

The runner refuses unresolved templates. Module P is the only template permitted to use `MODULE_P_PUBLIC_COMPARISON` mode.
