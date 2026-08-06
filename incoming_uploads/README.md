# 3-RFC execution tools

## One-command session start

```bash
bash tools/start_work.sh
```

This validates the repository, refreshes compact memory, resolves the only authorized work unit, creates/reuses its run workspace, copies exact Wolfram programs and provenance binding sheets, and writes `work_packets/ACTIVE_WORK_PACKET.md`.

## Director

```text
python tools/director.py doctor
python tools/director.py active
python tools/director.py prepare-active --create-run
python tools/director.py wolfram-list --module <MODULE>
python tools/director.py wolfram-show --call <CALL_ID>
python tools/director.py wolfram-record --run <RUN_ID> --call <CALL_ID> --output <FILE>
python tools/director.py solver-list --module <MODULE>
python tools/director.py solver-show --module <MODULE> --solver <SOLVER>
python tools/director.py solver-copy --module <MODULE> --solver <SOLVER> --destination <RUN_DIR>
```

## Provenance-bound numerical execution

```text
python tools/materialize_solver_config.py --template ... --binding-sheet ... --output ...
python tools/run_configured_solver.py --config ... --output-dir ...
python tools/run_module_pipeline.py --run <RUN_DIR>
bash tools/finish_local_phase.sh <MODULE> <RUN_DIR>
```

The materializer refuses missing origins, hash mismatches, unresolved values, and illegal public-data bindings. The local pipeline refuses hand-created configs that did not pass through the materializer.

## Manufactured validation

```text
python tools/run_reference_checks.py --module ALL
python tools/run_all_configured_examples.py --clean
python -m unittest discover -s tests -v
```

Manufactured PASS results prove implementation behavior only.

## Repository controller

Run `python tools/rfc.py --help`.

Core commands include `verify-bundle`, `doctor`, `context`, `context-pack`, `next`, `record-commit`, `admit-seed`, `admit-source`, `new-run`, `close-run`, `promote-module`, `record-claim`, `freeze`, `firewall-scan`, `advance`, `new-proof`, and `new-universe`.

Mechanical PASS results are guardrails, not scientific validation.

## Bundle integrity and reproducible packaging

```text
python tools/build_bundle.py
python tools/build_bundle.py --output ../3RFC_Execution_Ready_Universe_Builder_20260805.zip
python tools/rfc.py verify-bundle
```

The builder excludes runtime caches, writes a content manifest and checksum list, and uses fixed ZIP metadata so unchanged content produces the same archive bytes. `verify-bundle` is a pre-installation distribution check; after legitimate repository mutations, use Git, run manifests, artifact hashes, and replay rather than rechecking the original ZIP manifest.
