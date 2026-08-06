#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 2 ]; then
  echo "usage: $0 <MODULE> <RUN_DIR>" >&2
  exit 2
fi
MODULE="$1"
RUN_DIR="$2"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
python tools/run_reference_checks.py --module "$MODULE" --output "$RUN_DIR/reference_checks.json"
python tools/run_module_pipeline.py --run "$RUN_DIR"
python -m unittest discover -s tests -v
python tools/director.py doctor
printf '\nLocal phase passed. Wolfram outputs, convergence/restart/replay, independent reconstruction, final gates, claim ledger, and verified GitHub commit are still required.\n'
