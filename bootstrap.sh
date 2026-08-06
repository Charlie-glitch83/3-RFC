#!/usr/bin/env sh
set -eu

# Distribution integrity is a one-time pre-mutation check. Once a Git HEAD
# exists, the live repository is governed by Git hashes, manifests, replay,
# and the test suite rather than by byte identity with the original ZIP.
if command -v git >/dev/null 2>&1 && git rev-parse --verify HEAD >/dev/null 2>&1; then
  echo "BUNDLE VERIFICATION: SKIPPED (live repository; use Git hashes, manifests, replay, and tests)"
else
  python tools/rfc.py verify-bundle
fi

python tools/rfc.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan
python tools/rfc.py context
python tools/rfc.py next
