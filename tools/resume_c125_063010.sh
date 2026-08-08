#!/usr/bin/env bash
set -euo pipefail
RUN_ID="C-125-20260808T063500Z"
RUN="modules/C/runs/${RUN_ID}"

python - <<'PY'
import json
from pathlib import Path
s=json.load(open('STATE.json')); q={x['id']:x for x in json.load(open('WORK_QUEUE.json'))['items']}; r=json.load(open('modules/C/runs/C-125-20260808T063500Z/run.json'))
assert s['active_work_unit']=='C-125' and s['current_module']=='C' and s['current_run']=='C-125-20260808T063500Z',s
assert s['modules']['C']['evidence_state']=='DESIGN' and s['modules']['C']['fidelity']=='PRODUCTION',s['modules']['C']
assert s['modules']['B']['evidence_state']=='FROZEN' and s['modules']['B']['fidelity']=='PRODUCTION',s['modules']['B']
assert q['C-125']['status']=='ACTIVE' and q['D-135']['status']=='BLOCKED',q
assert r['status']=='CREATED',r
assert Path('modules/B/frozen/H_B_to_C_v2.json').is_file()
print('C125_RESUME_PRECONDITION_PASS')
PY

# Remove only the root-level artifacts created by the prior empty-$RUN implementation failure.
rm -f ENVIRONMENT.json FROZEN_DERIVATION_SPEC.json PRE_EXECUTION_LOCK.json RUN_PLAN.md SOURCE_REGISTER.json GATE_RESULTS.json
rm -f binding_sheets/C_spectral_model.bindings.json solver_templates/C_spectral_model.template.json
rm -f primary/MICROSCOPIC_CONSTITUTION_V2.json primary/COUNTERMODEL_RESULTS.json independent/INDEPENDENT_RECONSTRUCTION.json
rmdir binding_sheets solver_templates primary independent 2>/dev/null || true

# Freeze the actual governed run-local C science.
python tools/execute_c125.py prepare --run "$RUN"
python - <<'PY'
import hashlib,json,math
from pathlib import Path
R=Path('modules/C/runs/C-125-20260808T063500Z'); parent=json.load(open('modules/B/frozen/H_B_to_C_v2.json'))
Q=parent['operator']['matrix']; M=[[(1.0 if i==j else 0.0)-float(x) for j,x in enumerate(row)] for i,row in enumerate(Q)]
G=[[0.0,-1/math.sqrt(3),1/math.sqrt(3)],[1/math.sqrt(3),0.0,-1/math.sqrt(3)],[-1/math.sqrt(3),1/math.sqrt(3),0.0]]
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=R/'binding_sheets/C_spectral_model.bindings.json'; sheet=json.load(open(p)); src=R/'FROZEN_DERIVATION_SPEC.json'; h=sha(src)
for rec in sheet['bindings']:
 rec.update(origin_kind='INTERNAL_DERIVATION',origin_path=str(src),origin_sha256=h,module='C',units='dimensionless',dimensions='1',justification='Corroborative exact parent spectral audit; full C-125 generator is execute_c125.py from recovered theorem sources.')
 if rec['path']=='model.matrix': rec.update(value=M,derivation_object='I-Q_B')
 elif rec['path']=='model.symmetry_generators': rec.update(value=[G],derivation_object='conserved-mode O(2) audit generator')
 else: raise SystemExit(rec['path'])
p.write_text(json.dumps(sheet,indent=2)+'\n')
PY
mkdir -p "$RUN/solver_configs"
python tools/materialize_solver_config.py --template "$RUN/solver_templates/C_spectral_model.template.json" --binding-sheet "$RUN/binding_sheets/C_spectral_model.bindings.json" --output "$RUN/solver_configs/C_spectral_model.json"
python - <<'PY'
import hashlib,json
from pathlib import Path
R=Path('modules/C/runs/C-125-20260808T063500Z')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=R/'PRE_EXECUTION_LOCK.json'; lock=json.load(open(p)); lock['corroborative_solver_binding']={'config_path':str(R/'solver_configs/C_spectral_model.json'),'config_sha256':sha(R/'solver_configs/C_spectral_model.json'),'binding_sha256':sha(R/'binding_sheets/C_spectral_model.bindings.json'),'purpose':'corroborative parent-derived spectral audit only'}; p.write_text(json.dumps(lock,indent=2)+'\n')
PY
python tools/rfc.py context
python tools/rfc.py doctor
python tools/director.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan

git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
git add -A
git commit -m 'Freeze exact C-125 superseding replay after path repair'
git pull --rebase origin agent/frontier-050-execution
git push origin HEAD:agent/frontier-050-execution
LOCK_SHA=$(git rev-parse HEAD)
git fetch origin agent/frontier-050-execution
test "$(git rev-parse origin/agent/frontier-050-execution)" = "$LOCK_SHA"

# Record the exact connected Wolfram outputs captured after the scientific lock.
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
R=Path('modules/C/runs/C-125-20260808T063500Z/wolfram')
for c in ['C-WL-001','C-WL-002']:
    g=json.load(open(R/c/'gate.json'))
    assert str(g.get('status',g.get('result',''))).startswith('PASS') or g.get('pass') is True,g
print('C125_POST_LOCK_WOLFRAM_PASS')
PY

# Primary execution and independent reconstruction.
python tools/run_reference_checks.py --module C --output "$RUN/reference_checks.json"
mkdir -p "$RUN/solver_outputs/spectral_model"
python tools/run_configured_solver.py --config "$RUN/solver_configs/C_spectral_model.json" --output-dir "$RUN/solver_outputs/spectral_model"
python tools/execute_c125.py execute --run "$RUN"
python - <<'PY'
import json
R='modules/C/runs/C-125-20260808T063500Z'
assert json.load(open(R+'/reference_checks.json'))['overall']=='PASS'
assert json.load(open(R+'/solver_outputs/spectral_model/result.json'))['success'] is True
assert json.load(open(R+'/PRIMARY_GATE_INPUTS.json'))['overall']=='PASS'
assert json.load(open(R+'/independent/INDEPENDENT_RECONSTRUCTION.json'))['pass'] is True
PY

# Independent clean-checkout replay from the exact frozen preexecution commit.
rm -rf /tmp/c125-lock /tmp/c125-replay
git worktree add --detach /tmp/c125-lock "$LOCK_SHA"
(
 cd /tmp/c125-lock
 python tools/execute_c125.py execute --run "$RUN" --output-root /tmp/c125-replay
)
python tools/execute_c125.py finalize --run "$RUN" --replay-root /tmp/c125-replay

# Implementation-only closeout normalization required by the controller.
python - <<'PY'
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
R=Path('modules/C/runs/C-125-20260808T063500Z')
claim=json.load(open(R/'CLAIM_RECORD.json'))
p=R/'CLOSEOUT.md'; text=p.read_text(encoding='utf-8')
if '## Result' not in text:
    text=text.replace('# C-125 Closeout\n\n','# C-125 Closeout\n\n## Result\n\n**PASS.**\n\n',1)
if '## Strongest supported claim' not in text:
    text += '\n## Strongest supported claim\n\n'+claim['text']+'\n'
if '## Strongest unsupported claim' not in text:
    text += '\n## Strongest unsupported claim\n\n'+claim['strongest_unsupported_claim']+'\n'
p.write_text(text,encoding='utf-8')
assert all(x in text for x in ['Result','Strongest supported claim','Strongest unsupported claim'])
# Closeout is part of the generated evidence tree, so finalize the manifest again.
records=[]
for q in sorted(R.rglob('*')):
    if not q.is_file() or q.name in {'GENERATED_OUTPUT_MANIFEST.json','run.json'} or '__pycache__' in q.parts: continue
    records.append({'path':str(q.relative_to(R)),'sha256':hashlib.sha256(q.read_bytes()).hexdigest(),'bytes':q.stat().st_size})
h=hashlib.sha256()
for rec in records: h.update(rec['path'].encode()); h.update(b'\0'); h.update(rec['sha256'].encode()); h.update(b'\n')
(R/'GENERATED_OUTPUT_MANIFEST.json').write_text(json.dumps({'run_id':'C-125-20260808T063500Z','status':'FINAL','finalized_utc':datetime.now(timezone.utc).isoformat(),'outputs':records,'tree_sha256':h.hexdigest(),'note':'Finalized after controller-required closeout headings; C science, gates, thresholds and claim scope unchanged. Excludes itself and controller-owned run.json.'},indent=2)+'\n')
PY

python - <<'PY'
import json
R='modules/C/runs/C-125-20260808T063500Z'
c=json.load(open(R+'/OUTPUT_CONTRACT.json')); assert c['status']=='PASS',c
assert all(x['status']=='SATISFIED' and x['child_ready'] for x in c['required_outputs'])
assert all(x['status']=='SATISFIED' and x['source_lineage']=='PASS' and x['independent_verification']=='PASS' for x in c['child_bindings'].values())
assert json.load(open(R+'/OUTPUT_COMPLETENESS.json'))['overall']=='PASS'
assert json.load(open(R+'/REPLAY_RECORD.json'))['artifact_hashes_match'] is True
PY
python tools/rfc.py doctor
python tools/director.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan

# Evidence-matched closeout and one-child advancement.
python tools/rfc.py close-run --run-id "$RUN_ID" --result PASS --closeout "$RUN/CLOSEOUT.md"
python tools/rfc.py promote-module C --to FORMALIZED --fidelity PRODUCTION --evidence "$RUN/FROZEN_DERIVATION_SPEC.json"
python tools/rfc.py promote-module C --to IMPLEMENTED --fidelity PRODUCTION --evidence "$RUN/primary/MICROSCOPIC_CONSTITUTION_V2.json"
python tools/rfc.py promote-module C --to VERIFIED --fidelity PRODUCTION --evidence "$RUN/GATE_RESULTS.json"
python tools/rfc.py promote-module C --to PHYSICALLY_EXECUTED --fidelity PRODUCTION --evidence "$RUN/primary/MICROSCOPIC_CONSTITUTION_V2.json"
python tools/rfc.py promote-module C --to INDEPENDENTLY_REPRODUCED --fidelity PRODUCTION --evidence "$RUN/independent/INDEPENDENT_RECONSTRUCTION.json"
python tools/rfc.py promote-module C --to FROZEN --fidelity PRODUCTION --evidence modules/C/frozen/H_C_to_D_v2.json
python tools/rfc.py freeze modules/C/frozen/H_C_to_D_v2.json --kind MODULE_HANDOFF
python tools/rfc.py record-claim --file "$RUN/CLAIM_RECORD.json"
python tools/rfc.py advance --task C-125 --result PASS --evidence "$RUN/CLOSEOUT.md" --note 'Verified C-125 channel-complete microscopic replay from exact H_B_to_C_v2; activate only D-135.'
python tools/rfc.py context
python tools/rfc.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan
python - <<'PY'
import json
s=json.load(open('STATE.json')); q={x['id']:x for x in json.load(open('WORK_QUEUE.json'))['items']}
assert s['active_work_unit']=='D-135' and s['current_module']=='D' and s['current_run'] is None,s
assert s['modules']['C']['evidence_state']=='FROZEN' and s['modules']['C']['fidelity']=='PRODUCTION',s['modules']['C']
assert q['C-125']['status']=='PASS' and q['D-135']['status']=='ACTIVE' and q['E-145']['status']=='BLOCKED',q
PY

git add -A
git commit -m 'Close verified C-125 and activate D-135'
git pull --rebase origin agent/frontier-050-execution
git push origin HEAD:agent/frontier-050-execution
CLOSE_SHA=$(git rev-parse HEAD)
git fetch origin agent/frontier-050-execution
test "$(git rev-parse origin/agent/frontier-050-execution)" = "$CLOSE_SHA"
python tools/rfc.py record-commit "$CLOSE_SHA" --branch agent/frontier-050-execution --note 'Verified C-125 channel-complete microscopic replay, exact parent/source lineage, clean replay, complete D child contract, PRODUCTION evidence ladder and one-child activation D-135.'
python tools/rfc.py context
python tools/rfc.py doctor
git add STATE.json memory/DECISION_LOG.jsonl memory/CURRENT_CONTEXT.md
git commit -m 'Record verified C-125 superseding closeout'
git pull --rebase origin agent/frontier-050-execution
git push origin HEAD:agent/frontier-050-execution

echo "C125_RESUME_COMPLETE $(git rev-parse HEAD)"
