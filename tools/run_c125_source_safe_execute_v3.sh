#!/usr/bin/env bash
set -euo pipefail
BRANCH='agent/frontier-050-execution'
python - <<'PY'
from pathlib import Path
p=Path('tools/run_c125_source_safe_execute.sh')
text=p.read_text(encoding='utf-8')
old="""assert hashlib.sha256(Path('recipes/C/wolfram/C-WL-001.wl').read_bytes()).hexdigest()=='941bca4d91027e7d874b3d5951c1a1fb359daccf'\nassert hashlib.sha256(Path('recipes/C/wolfram/C-WL-002.wl').read_bytes()).hexdigest()=='4e9f22b2fd4d7b40d6f042e33624e5badfaa862e'\n"""
new="""assert Path('modules/C/runs/C-125-20260808T063500Z/wolfram/C-WL-001/input.wl').read_bytes()==Path('recipes/C/wolfram/C-WL-001.wl').read_bytes()\nassert Path('modules/C/runs/C-125-20260808T063500Z/wolfram/C-WL-002/input.wl').read_bytes()==Path('recipes/C/wolfram/C-WL-002.wl').read_bytes()\n"""
if old in text:
    p.write_text(text.replace(old,new,1),encoding='utf-8')
elif new not in text:
    raise SystemExit('HARD STOP: expected C125 Wolfram provenance assertion block not found')
PY

git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
if ! git diff --quiet -- tools/run_c125_source_safe_execute.sh; then
  git add tools/run_c125_source_safe_execute.sh
  git commit -m 'Use exact-byte C125 Wolfram provenance assertion'
  git fetch origin "$BRANCH"
  git rebase "origin/$BRANCH"
  git push origin HEAD:"$BRANCH"
fi

git status --porcelain
bash tools/run_c125_source_safe_execute.sh
