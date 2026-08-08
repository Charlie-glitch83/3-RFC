#!/usr/bin/env bash
set -euo pipefail

# Preserve any generic pre-repair C-125 startup shell before the superseding run.
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

This run was created by the generic C-125 startup path before the superseding-lineage controller reopened Module C at PRODUCTION fidelity. It contains no primary C science and is preserved as a startup-shell attempt. The repaired lineage closes this shell and proceeds from exact `H_B_to_C_v2` in a fresh governed PRODUCTION run.
''',encoding='utf-8')
PY
  python tools/rfc.py close-run --run-id "$RID" --result BLOCKED --closeout "modules/C/runs/$RID/CLOSEOUT.md"
fi

# Accept only the two lawful pre-primary states and normalize to DESIGN/PRODUCTION once.
MODE=$(python - <<'PY'
import json
from pathlib import Path
s=json.load(open('STATE.json')); q={x['id']:x for x in json.load(open('WORK_QUEUE.json'))['items']}
assert s['active_work_unit']=='C-125' and s['current_module']=='C' and s['current_run'] is None,s
assert s['modules']['B']['evidence_state']=='FROZEN' and s['modules']['B']['fidelity']=='PRODUCTION',s['modules']['B']
c=s['modules']['C']; pair=(c['evidence_state'],c['fidelity'])
assert pair in {('FROZEN','MINIMAL_SPINE'),('DESIGN','PRODUCTION')},c
assert q['C-125']['status']=='ACTIVE' and q['D-135']['status']=='BLOCKED',q
assert Path('modules/B/frozen/H_B_to_C_v2.json').is_file()
assert Path('recovery/BG_SUPERSEDING_LINEAGE_PACKET.md').is_file()
print('REOPEN' if pair==('FROZEN','MINIMAL_SPINE') else 'RESUME')
PY
)
if [ "$MODE" = "REOPEN" ]; then
  python tools/rfc.py reopen-module C --fidelity PRODUCTION --evidence recovery/BG_SUPERSEDING_LINEAGE_PACKET.md
fi
python - <<'PY'
import json
s=json.load(open('STATE.json')); c=s['modules']['C']
assert s['current_run'] is None,s
assert c['evidence_state']=='DESIGN' and c['fidelity']=='PRODUCTION',c
print('C125_NORMALIZED_TO_PRODUCTION')
PY

# Execute the unchanged frozen scientific sequence beginning at fresh-run creation.
awk 'BEGIN{emit=0} /^python tools\/rfc.py new-run C --run-id /{emit=1} emit{print}' tools/run_c125_repair_dispatch.sh | bash
