# Provenance-complete solver binding

Never hand-edit an unbound template into an executable configuration without a binding record.

For each template, copy the matching file from `configured_runs/binding_sheets/` into the active run. Fill every record with:

- `value` — the exact JSON value to insert;
- `origin_kind` — `ADMITTED_SOURCE`, `EXACT_PARENT_ARTIFACT`, `INTERNAL_DERIVATION`, or, only in Module P, `PREREGISTERED_MODULE_P_SOURCE`;
- `origin_path` and `origin_sha256` — an existing immutable file and its verified hash;
- `derivation_object` — the theorem, equation, notebook, or program object that produced an internally derived value;
- units, dimensions, and a short justification.

Then materialize the solver configuration:

```bash
python tools/materialize_solver_config.py \
  --template configured_runs/templates/<TEMPLATE>.json \
  --binding-sheet <RUN_DIR>/binding_sheets/<SHEET>.json \
  --output <RUN_DIR>/solver_configs/<CONFIG>.json
```

The tool refuses a hash mismatch, nonexistent origin, missing value, invalid origin class, Module P leakage, duplicate path, or remaining `__BIND_` token.
