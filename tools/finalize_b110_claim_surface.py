#!/usr/bin/env python3
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
STATE=ROOT/'STATE.json'
SUPPORTED='Module B now provides a frozen, source-addressed, physically executed, independently reproduced and cleanly replayed first physical RFC state H_B_to_C at MINIMAL_SPINE fidelity: the exact frozen A prephysical modal state undergoes the source-locked Big Implosion counting-Laplacian crossing into a conserved, strictly compressed, exactly reopenable relational state with intrinsic event-order origin and typed pregeometry.'
UNSUPPORTED='No microscopic particle/field sector model, metric spacetime geometry, calibrated physical duration, dimensional physical constants, late-time cosmology, empirical agreement, manifested completed universe, or later-module physics has yet been established.'
VERIFIED_COMMIT='36084b7dac69139e37e6c69dcc7779da4c050a1e'

def main():
    state=json.loads(STATE.read_text(encoding='utf-8'))
    b=state['modules']['B']
    if state.get('active_work_unit')!='C-120' or state.get('current_module')!='C':
        raise SystemExit('HARD STOP: expected C-120 to be sole active child after B closeout')
    if b.get('evidence_state')!='FROZEN' or b.get('fidelity')!='MINIMAL_SPINE' or 'B-110-20260807T002248Z' not in b.get('completed_runs',[]):
        raise SystemExit('HARD STOP: Module B closeout state is not frozen/minimal-spine/completed')
    state['strongest_supported_claim']=SUPPORTED
    state['strongest_unsupported_claim']=UNSUPPORTED
    state['last_verified_commit']=VERIFIED_COMMIT
    state['last_verified_branch']='agent/frontier-050-execution'
    state['last_updated_utc']=datetime.now(timezone.utc).isoformat()
    STATE.write_text(json.dumps(state,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'status':'PASS','updated':'STATE.json claim surface only','verified_commit':VERIFIED_COMMIT,'active_work_unit':state['active_work_unit']},indent=2))

if __name__=='__main__': main()
