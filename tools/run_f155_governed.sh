#!/usr/bin/env bash
set -euo pipefail
RUN_ID='F-155-20260808T165152Z'
R="modules/F/runs/$RUN_ID"
BRANCH='agent/frontier-050-execution'
python -m pip install --disable-pip-version-check -r requirements-lock.txt
python - <<'PY'
import json
s=json.load(open('STATE.json'))
assert s['active_work_unit']=='F-155' and s['current_module']=='F' and s['current_run']=='F-155-20260808T165152Z',s
assert s['modules']['E']['evidence_state']=='FROZEN' and s['modules']['E']['fidelity']=='PRODUCTION',s['modules']['E']
PY
python tools/rfc.py reopen-module F --fidelity PRODUCTION --evidence recovery/BG_SUPERSEDING_LINEAGE_PACKET.md
python tools/f155_parent_bound.py prepare --run "$R"
python tools/director.py wolfram-show --call F-WL-001 >/tmp/F-WL-001-displayed.txt
python tools/director.py wolfram-show --call F-WL-002 >/tmp/F-WL-002-displayed.txt
python tools/director.py wolfram-record --run "$RUN_ID" --call F-WL-001 --output "$R/scratch/wolfram_external/F-WL-001.txt"
python tools/director.py wolfram-record --run "$RUN_ID" --call F-WL-002 --output "$R/scratch/wolfram_external/F-WL-002.txt"
python tools/run_reference_checks.py --module F --output "$R/reference_checks.json"
python tools/materialize_solver_config.py --template "$R/solver_templates/F_reaction_network.template.json" --binding-sheet "$R/binding_sheets/F_reaction_network.bindings.json" --output "$R/solver_configs/F_reaction_network.json"
python tools/materialize_solver_config.py --template "$R/solver_templates/F_transport.template.json" --binding-sheet "$R/binding_sheets/F_transport.bindings.json" --output "$R/solver_configs/F_transport.json"

git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
git add "$R" STATE.json memory/DECISION_LOG.jsonl
git commit -m 'Freeze F-155 pre-execution state'
git push origin HEAD:"$BRANCH"
PRE_SHA="$(git rev-parse HEAD)"

run_convergence () {
  local BASE="$1"
  python - "$BASE" <<'PY'
import json,sys
from pathlib import Path
r=Path(sys.argv[1]); d=json.loads((r/'FROZEN_DERIVATION_SPEC.json').read_text()); tau=d['implementation_checks']['reaction']['t_span'][1]
for div in [64,128,256,512]:
  for name,nested in [('F_reaction_network.json',False),('F_transport.json',True)]:
    c=json.loads((r/'solver_configs'/name).read_text())
    if nested: c['model']['max_step']=tau/div
    else: c['max_step']=tau/div
    p=r/'convergence'/str(div)/'configs'/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(c,indent=2)+'\n')
PY
  for DIV in 64 128 256 512; do
    python tools/run_configured_solver.py --config "$BASE/convergence/$DIV/configs/F_reaction_network.json" --output-dir "$BASE/convergence/$DIV/outputs/F_reaction_network"
    python tools/run_configured_solver.py --config "$BASE/convergence/$DIV/configs/F_transport.json" --output-dir "$BASE/convergence/$DIV/outputs/F_transport"
  done
  python - "$BASE" <<'PY'
import json,sys
from pathlib import Path
import numpy as np
r=Path(sys.argv[1]); tol=1e-8; rows={}
for solver in ['F_reaction_network','F_transport']:
  vals={d:np.array(json.loads((r/'convergence'/str(d)/'outputs'/solver/'result.json').read_text())['final'],float) for d in [64,128,256,512]}
  ref=vals[512]; diffs={str(d):float(np.max(np.abs(v-ref))) for d,v in vals.items()}; rows[solver]={'linf_vs_512':diffs,'tolerance':tol,'pass':max(diffs.values())<=tol}
out={'classification':'F155_CONVERGENCE_MATRIX','solvers':rows,'pass':all(x['pass'] for x in rows.values())}
(r/'convergence/CONVERGENCE.json').write_text(json.dumps(out,indent=2)+'\n')
if not out['pass']: raise SystemExit('F155 convergence failed')
PY
}
patch_convergence_gate () {
  local BASE="$1"
  python - "$BASE" <<'PY'
import json,sys
from pathlib import Path
r=Path(sys.argv[1]); p=r/'PRIMARY_GATE_INPUTS.json'; g=json.loads(p.read_text()); c=json.loads((r/'convergence/CONVERGENCE.json').read_text())
g['componentwise']['convergence']={'pass':c['pass'],'evidence':'convergence/CONVERGENCE.json'}; p.write_text(json.dumps(g,indent=2)+'\n')
PY
}

bash tools/finish_local_phase.sh F "$R"
run_convergence "$R"
python tools/f155_parent_bound.py execute --run "$R"
patch_convergence_gate "$R"

rm -rf /tmp/f155-clean
git worktree add --detach /tmp/f155-clean "$PRE_SHA"
(
  cd /tmp/f155-clean
  R2="modules/F/runs/$RUN_ID"
  bash tools/finish_local_phase.sh F "$R2"
  run_convergence "$R2"
  python tools/f155_parent_bound.py execute --run "$R2"
  patch_convergence_gate "$R2"
)
python tools/f155_parent_bound.py finalize --run "$R" --replay-run "/tmp/f155-clean/$R" --pre-sha "$PRE_SHA"
python tools/scientific_completion_guard.py --run "$R"
python tools/rfc.py doctor
python tools/director.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan
python tools/rfc.py close-run --run-id "$RUN_ID" --result PASS --closeout "$R/CLOSEOUT.md"
python tools/rfc.py promote-module F --to FORMALIZED --fidelity PRODUCTION --evidence "$R/FROZEN_DERIVATION_SPEC.json"
python tools/rfc.py promote-module F --to IMPLEMENTED --fidelity PRODUCTION --evidence "$R/solver_outputs/F_transport/result.json"
python tools/rfc.py promote-module F --to VERIFIED --fidelity PRODUCTION --evidence "$R/GATE_RESULTS.json"
python tools/rfc.py promote-module F --to PHYSICALLY_EXECUTED --fidelity PRODUCTION --evidence "$R/primary/POST_NUCLEAR_PLASMA_V2.json"
python tools/rfc.py promote-module F --to INDEPENDENTLY_REPRODUCED --fidelity PRODUCTION --evidence "$R/independent/INDEPENDENT_RECONSTRUCTION.json"
python tools/rfc.py promote-module F --to FROZEN --fidelity PRODUCTION --evidence modules/F/frozen/H_F_to_G_v2.json
python tools/rfc.py freeze modules/F/frozen/H_F_to_G_v2.json --kind MODULE_HANDOFF
python tools/rfc.py record-claim --file "$R/CLAIM_RECORD.json"
python - <<'PY'
import json
from pathlib import Path
h=json.loads(Path('modules/F/frozen/H_F_to_G_v2.json').read_text()); p=Path('STATE.json'); s=json.loads(p.read_text())
s['strongest_supported_claim']=h['strongest_supported_claim']; s['strongest_unsupported_claim']=h['strongest_unsupported_claim']; s['repair_state']='F155_PRODUCTION_CLOSED_PENDING_VERIFIED_COMMIT_AND_CHILD_ADVANCE'; p.write_text(json.dumps(s,indent=2)+'\n')
PY
python tools/rfc.py context
python tools/rfc.py doctor
python tools/rfc.py firewall-scan
git add -A
git commit -m 'Close F-155 superseding F replay at verified scope'
git pull --rebase origin "$BRANCH"
git push origin HEAD:"$BRANCH"
printf 'F155_FINAL_COMMIT=%s\n' "$(git rev-parse HEAD)"
