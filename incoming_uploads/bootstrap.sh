#!/usr/bin/env sh
set -eu
python tools/rfc.py verify-bundle
python tools/rfc.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan
python tools/rfc.py context
python tools/rfc.py next
