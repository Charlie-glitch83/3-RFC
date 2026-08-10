#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'STATE.json'
s=json.loads(p.read_text())
ts=datetime.now(timezone.utc).isoformat()
for mod in ('I','HI','J'):
    m=s.get('modules',{}).get(mod)
    if not isinstance(m,dict):
        continue
    m['evidence_history']=[{
        'state':'DESIGN',
        'fidelity':'UNSTARTED',
        'timestamp_utc':ts,
        'evidence':'audit/I180_SCIENTIFIC_SUPERSESSION_20260810.json',
        'work_unit':'I-180',
        'note':'Current-authority history reset after scientific supersession; historical evidence remains preserved in git and the supersession audit.'
    }]
p.write_text(json.dumps(s,indent=2)+'\n')
