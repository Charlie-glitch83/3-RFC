#!/usr/bin/env python3
from pathlib import Path

p=Path('tools/resume_c125_063010.sh')
text=p.read_text(encoding='utf-8')
old="assert json.load(open(R+'/GATE_RESULTS.json'))['overall']=='PASS'"
new="assert json.load(open(R+'/PRIMARY_GATE_INPUTS.json'))['overall']=='PASS'"
if new in text:
    print('already patched')
elif old not in text:
    raise SystemExit('expected C125 pre-finalization gate assertion missing')
else:
    p.write_text(text.replace(old,new,1),encoding='utf-8')
    print('patched C125 pre-finalization assertion')
