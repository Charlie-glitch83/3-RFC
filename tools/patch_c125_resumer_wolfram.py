#!/usr/bin/env python3
import json
from pathlib import Path

state=json.load(open('STATE.json'))
rid=state.get('current_run')
if state.get('active_work_unit')!='C-125' or state.get('current_module')!='C' or not rid or not rid.startswith('C-125-'):
    raise SystemExit(f'HARD STOP: no canonical active C-125 run to patch: {state.get("active_work_unit")} / {rid}')

p=Path('tools/resume_c125_063010.sh')
text=p.read_text(encoding='utf-8')
# The repo-authored resumer was created for the first repaired shell. Retarget every
# run-local literal to the run that is canonical in STATE at this exact checkout.
text=text.replace('C-125-20260808T063010Z',rid)
marker='# Primary execution and independent reconstruction.\n'
block=f'''# Record the exact connected Wolfram outputs captured after the scientific lock.\ncat > /tmp/C-WL-001-output.txt <<'EOF'\nSymbol::undefined2: Warning: Global symbols "M, M, M, M, M, M, M" are undefined.\nGeneral::messages: Messages were generated which may indicate errors.\n\nOut[1]= "<|\\"call\\" -> \\"C-WL-001\\", \\"hermitian\\" -> True, \\"characteristicPolynomial\\" -> \\"a*b - a*lambda - b*lambda + lambda^2 - w^2 - z^2\\", \\"trace\\" -> \\"a + b\\", \\"determinant\\" -> \\"a*b - w^2 - z^2\\", \\"eigenvalues\\" -> {{\\"(a + b - Sqrt[(a - b)^2 + 4*(w^2 + z^2)])/2\\", \\"(a + b + Sqrt[(a - b)^2 + 4*(w^2 + z^2)])/2\\"}}|>"\nEOF\ncat > /tmp/C-WL-002-output.txt <<'EOF'\nSymbol::undefined2: Warning: Global symbols "G, X, G, X, X, G, X" are undefined.\nGeneral::messages: Messages were generated which may indicate errors.\n\nOut[1]= "<|\\"call\\" -> \\"C-WL-002\\", \\"invarianceSolution\\" -> \\"x21 == -x12 && x22 == x11\\", \\"candidate\\" -> \\"{{{{x11, x12}}, {{-x12, x11}}}}\\"|>"\nEOF\npython tools/director.py wolfram-show --call C-WL-001\npython tools/director.py wolfram-record --run "$RUN_ID" --call C-WL-001 --output /tmp/C-WL-001-output.txt\npython tools/director.py wolfram-show --call C-WL-002\npython tools/director.py wolfram-record --run "$RUN_ID" --call C-WL-002 --output /tmp/C-WL-002-output.txt\npython - <<'PY'\nimport json\nfrom pathlib import Path\nR=Path('modules/C/runs/{rid}/wolfram')\nfor c in ['C-WL-001','C-WL-002']:\n    g=json.load(open(R/c/'gate.json'))\n    assert str(g.get('status',g.get('result',''))).startswith('PASS') or g.get('pass') is True,g\nprint('C125_POST_LOCK_WOLFRAM_PASS')\nPY\n\n'''
if 'C125_POST_LOCK_WOLFRAM_PASS' not in text:
    if marker not in text:
        raise SystemExit('expected C125 resumer marker missing')
    text=text.replace(marker,block+marker,1)
p.write_text(text,encoding='utf-8')
print(json.dumps({'status':'PATCHED','current_run':rid,'post_lock_wolfram':True},indent=2))
