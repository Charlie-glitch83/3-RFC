# Execution-Ready Autopilot

The work model is an operator, not a project architect.

At the beginning of every session run:

```bash
python tools/director.py doctor
python tools/director.py active
python tools/director.py prepare-active
```

Then open the single generated file:

```text
work_packets/ACTIVE_WORK_PACKET.md
```

Perform the commands in that file in order. Do not substitute a different equation, calculation, test, tool, threshold, or artifact name because it seems easier.

For every Wolfram call:

```bash
python tools/director.py wolfram-show --call <CALL_ID>
```

Submit the exact displayed code to the connected Wolfram Language evaluator. Save the returned output verbatim:

```bash
python tools/director.py wolfram-record --run <RUN_ID> --call <CALL_ID> --output <OUTPUT_FILE>
```

For every local manufactured check:

```bash
python tools/run_reference_checks.py --module <MODULE> --output <RUN_DIR>/reference_checks.json
```

Manufactured checks prove that the implementation and invariants work on known cases. They do not replace the module's actual parent-driven derivation and execution.

A work model must stop and record `BLOCKED_UNDERDETERMINED` when the admitted premises fail to select a unique object and no lawful branch-family execution is specified. It must never fill the gap with a remembered standard value.
