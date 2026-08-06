#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from rfc_engine.reference_checks import run, run_all

p=argparse.ArgumentParser()
p.add_argument('--module',default='ALL')
p.add_argument('--output')
a=p.parse_args()
res=run_all() if a.module=='ALL' else run(a.module)
text=json.dumps(res,indent=2,ensure_ascii=False)+'\n'
if a.output:
    out=ROOT/a.output if not Path(a.output).is_absolute() else Path(a.output)
    out.parent.mkdir(parents=True,exist_ok=True); out.write_text(text,encoding='utf-8')
print(text,end='')
raise SystemExit(0 if res.get('overall')=='PASS' else 1)
