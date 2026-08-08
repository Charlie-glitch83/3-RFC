#!/usr/bin/env bash
set -euo pipefail
RID=$(python - <<'PY'
import json
print(json.load(open('STATE.json')).get('current_run') or '')
PY
)
if [ -n "$RID" ]; then
  python - "$RID" <<'PY'
import json,sys
from pathlib import Path
rid=sys.argv[1]; R=Path('modules/C/runs')/rid
rec=json.load(open(R/'run.json'))
if rec.get('module')!='C' or rec.get('task_id')!='C-125' or rec.get('status')!='CREATED':
    raise SystemExit(f'HARD STOP: refusing to supersede nonblank current run {rec}')
(R/'CLOSEOUT.md').write_text(f'''# {rid} Startup-Shell Closeout

**BLOCKED BEFORE SCIENTIFIC EXECUTION.**

This run was created by the generic C-125 startup path before the superseding-lineage controller reopened Module C at PRODUCTION fidelity. It contains no primary C science and is preserved as a startup-shell attempt. The repaired lineage closes this shell, reopens C from exact `H_B_to_C_v2`, and creates a fresh governed PRODUCTION run.
''',encoding='utf-8')
PY
  python tools/rfc.py close-run --run-id "$RID" --result BLOCKED --closeout "modules/C/runs/$RID/CLOSEOUT.md"
fi
bash tools/run_c125_repair_dispatch.sh
