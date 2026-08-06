#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
python tools/director.py doctor
python tools/rfc.py context
python tools/director.py active
python tools/director.py prepare-active --create-run
printf '\nOpen and execute exactly: work_packets/ACTIVE_WORK_PACKET.md\n'
