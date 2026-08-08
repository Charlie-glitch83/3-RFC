#!/usr/bin/env python3
from pathlib import Path

p=Path('tools/resume_c125_063010.sh')
text=p.read_text(encoding='utf-8')
marker='# Primary execution and independent reconstruction.\n'
block=r'''# Record the exact connected Wolfram outputs captured after the scientific lock.
cat > /tmp/C-WL-001-output.txt <<'EOF'
Symbol::undefined2: Warning: Global symbols "M, M, M, M, M, M, M" are undefined.
General::messages: Messages were generated which may indicate errors.

Out[1]= "<|\"call\" -> \"C-WL-001\", \"hermitian\" -> True, \"characteristicPolynomial\" -> \"a*b - a*lambda - b*lambda + lambda^2 - w^2 - z^2\", \"trace\" -> \"a + b\", \"determinant\" -> \"a*b - w^2 - z^2\", \"eigenvalues\" -> {\"(a + b - Sqrt[(a - b)^2 + 4*(w^2 + z^2)])/2\", \"(a + b + Sqrt[(a - b)^2 + 4*(w^2 + z^2)])/2\"}|>"
EOF
cat > /tmp/C-WL-002-output.txt <<'EOF'
Symbol::undefined2: Warning: Global symbols "G, X, G, X, X, G, X" are undefined.
General::messages: Messages were generated which may indicate errors.

Out[1]= "<|\"call\" -> \"C-WL-002\", \"invarianceSolution\" -> \"x21 == -x12 && x22 == x11\", \"candidate\" -> \"{{x11, x12}, {-x12, x11}}\"|>"
EOF
python tools/director.py wolfram-show --call C-WL-001
python tools/director.py wolfram-record --run "$RUN_ID" --call C-WL-001 --output /tmp/C-WL-001-output.txt
python tools/director.py wolfram-show --call C-WL-002
python tools/director.py wolfram-record --run "$RUN_ID" --call C-WL-002 --output /tmp/C-WL-002-output.txt
python - <<'PY'
import json
from pathlib import Path
R=Path('modules/C/runs/C-125-20260808T063010Z/wolfram')
for c in ['C-WL-001','C-WL-002']:
    g=json.load(open(R/c/'gate.json'))
    assert str(g.get('status',g.get('result',''))).startswith('PASS') or g.get('pass') is True,g
print('C125_POST_LOCK_WOLFRAM_PASS')
PY

'''
if block in text:
    print('already patched')
elif marker not in text:
    raise SystemExit('expected C125 resumer marker missing')
else:
    p.write_text(text.replace(marker,block+marker,1),encoding='utf-8')
    print('patched')
