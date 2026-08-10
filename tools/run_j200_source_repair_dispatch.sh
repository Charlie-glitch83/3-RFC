#!/usr/bin/env bash
set -euo pipefail
EXPECT='34c69b08165bf738d460053dc08d833932b8c370'
OLD='J-200-20260809T225756Z'
test "$(git rev-parse HEAD)" = "$EXPECT"
python -m pip install --disable-pip-version-check -r requirements-lock.txt
OLD_R="modules/J/runs/$OLD"
cat > "$OLD_R/CLOSEOUT.md" <<'EOF'
# J-200 Superseded Pre-Execution Freeze Closeout

## Result
FAIL before primary physical execution.

## Finding
The frozen source scope admitted HI and P29 but omitted canonical P30, despite repository recovery evidence requiring exact HI + P29 + P30 before J freezes its derivation surface. P30 explicitly leaves the physical primordial spectrum, amplitude, index, transfer function, and matter power spectrum pending; it is a required negative authority boundary and cannot be silently omitted.

The J-WL-001 failures were implementation-only Wolfram compatibility defects. They remain preserved and do not alter J science. No physical covariance, physical spectrum, phase-selected field, or K-ready handoff was produced by this superseded run.

## Strongest supported claim
The exact HI parent and repository manufactured J checks remain valid inputs to a new correctly sourced J run.

## Strongest unsupported claim
No realized physical primordial covariance, physical primordial spectrum, finite-volume field, or J-to-K handoff is claimed from this run.

## Required action
Close this run FAIL, keep J-200 active, generate a new governed run, admit exact HI + canonical P29 + canonical P30 before freezing, and derive J only from those exact sources and repository-authorized internal derivations.
EOF
python tools/rfc.py close-run --run-id "$OLD" --result FAIL --closeout "$OLD_R/CLOSEOUT.md"
rm -f .github/workflows/j200-live-runner.yml
bash tools/start_work.sh
RUN="$(python - <<'PY'
import json
s=json.load(open('STATE.json'))
assert s['active_work_unit']=='J-200' and s['current_module']=='J',s
assert s['current_run'] and s['current_run']!='J-200-20260809T225756Z',s
print(s['current_run'])
PY
)"
R="modules/J/runs/$RUN"
python - "$RUN" <<'PY'
import hashlib,json,sys
from datetime import datetime,timezone
from pathlib import Path
run=sys.argv[1]; R=Path('modules/J/runs')/run
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def row(p,classification):
    q=Path(p); return {'path':str(q),'sha256':sha(q),'bytes':q.stat().st_size,'classification':classification}
parent='modules/HI/frozen/H_HI_to_J.json'
p29='sources/frozen/cef6d68b05eb509e471c55a18b5fffedd9c411b44bc0d5bd0f6b5ee86bd8b53e/Presentation 29 revised  raw LaTeX.md'
p30='sources/frozen/4895c3777da3aa84da4ec2343419ffbc07502b3738602308a1f402862441eaf6/Presentation 30 raw LaTex.md'
blueprint='sources/frozen/2f3539d6493f87a407765a9f24d6cd61e825a36fe9217d2adfa075c070d27b6e/2RFC_Deep_Soak_and_Realization_Blueprint_20260805.md'
queue='sources/frozen/c3b22b3f6973cef75409162c406ac224b2d66aa8bb938a6f035d386384fab226/2RFC_Immediate_Execution_Queue_20260805.md'
authority=['recipes/J/recipe.json','recipes/J/WORK_ORDER.md','recipes/J/gates.json','modules/J/spec.json','docs/08_EVIDENCE_AND_CLAIM_STATES.md','docs/09_DERIVATION_PROTOCOL.md','docs/10_EXECUTION_PROTOCOL.md','theory/DERIVATION_ATLAS.md','config/WOLFRAM_EXPECTATIONS.json','config/required_output_contracts.json','MODEL_OPERATOR_PROMPT.md','requirements-lock.txt']
src={'schema_version':'2.1','run_id':run,'status':'FROZEN_BEFORE_PRIMARY_EXECUTION','generation_mode':'GENERATION_SEALED','exact_parents':[row(parent,'DIRECT_PARENT')],'admitted_sources':[row(p29,'CANONICAL_AUTHORITY'),row(p30,'CANONICAL_AUTHORITY'),row(blueprint,'ADMITTED_SOURCE'),row(queue,'ADMITTED_SOURCE')],'imports':['json','hashlib','pathlib','numpy','scipy'],'files':[row(p,'AUTHORITY') for p in authority],'urls':[],'constants':[],'public_data_declaration':'NONE','network_policy':'DISABLED_DURING_GENERATION'}
(R/'SOURCE_REGISTER.json').write_text(json.dumps(src,indent=2)+'\n')
par=json.loads(Path(parent).read_text())
deriv={'schema_version':'2.1','run_id':run,'status':'FROZEN_PRE_EXECUTION','module':'J','fidelity':'MINIMAL_SPINE','generation_mode':'GENERATION_SEALED','parent':row(parent,'DIRECT_PARENT'),
'source_laws':{'P29_recursive_kernel':'K_f(t)=sum_{j=1}^N delta^{-j} f_j(t) exp(-alpha j t); domain lanes alter the modal basis while preserving the frozen source packet.','P29_normalized_depth_weights':'p_j(t;n)=delta^{-j} exp(-alpha j t)/sum_{k=1}^n delta^{-k} exp(-alpha k t), positive and normalized.','P30_boundary':'physical P_R(k), n_s, A_s, alpha_s, r, physical T(k), and matter power spectrum are explicitly pending/not generated and may not be imported as solved parents.'},
'exact_HI_mode_law':par['mode_eigenstructure']['law'],'exact_HI_covariance_pushforward':par['error_covariance_propagation']['law'],
'derivation_rule':'Construct J only on the exact branch-indexed HI physical quotient. P29 recursive weights may define a PSD spectral covariance over an exact inherited J modal basis only when the exact branch supplies a finite ordered physical basis and a source-owned recursion-to-mode mapping. The branch covariance family is then Sigma_J=sum_j p_j |f_bj><f_bj| and is propagated only by the exact HI pushforward law. This rule does not manufacture a basis, dimension, physical amplitude, cross-covariance, clock identification, or branch selection. If a material ingredient is absent, preserve the family symbolically and stop BLOCKED_UNDERDETERMINED before numeric physical realization.',
'target_blind_seed_rule':'Only after a material covariance is lawfully fixed, derive the stochastic seed deterministically from SHA256(parent_sha256 || run_id || purpose_label); never search or retune it.',
'candidate_classes':['branch-indexed endogenous PSD covariance spectral operators on exact HI modes','complete lawful covariance branch family when ancestry remains nonunique','target-blind finite-volume realization only after material covariance is fixed'],
'forbidden_promotions':['manufactured J covariance to physical parent','P30 readiness markers/sigma8/proxy scores to physical spectrum','public or remembered primordial amplitudes','unowned zero cross-covariance','arbitrary finite basis dimension or mode ordering'],
'claim_boundary':'One realized RFC linear universe only if exact admitted ancestry supplies every material covariance and realization ingredient; otherwise close at the exact underdetermination obstruction.'}
(R/'FROZEN_DERIVATION_SPEC.json').write_text(json.dumps(deriv,indent=2)+'\n')
dh=sha(R/'FROZEN_DERIVATION_SPEC.json')
lock={'schema_version':'2.1','run_id':run,'status':'FROZEN','frozen_utc':datetime.now(timezone.utc).isoformat(),'frozen_before_primary_execution':True,'authority_hashes':[sha(p) for p in authority],'parent_hashes':[sha(parent)],'definition_hashes':[dh,sha(p29),sha(p30),sha(blueprint),sha(queue)],'candidate_classes':deriv['candidate_classes'],'equations_and_laws':[deriv['source_laws']['P29_recursive_kernel'],deriv['source_laws']['P29_normalized_depth_weights'],deriv['derivation_rule'],deriv['exact_HI_covariance_pushforward'],deriv['target_blind_seed_rule']],'dimensions_units_frames_gauges_clocks':['inherit exact HI branch identity','inherit HU quotient V_b=ker(C_b)/im(G_b)','inherit Big-Implosion clock family without identifying recursive depth as physical time','no imported FRW/k-grid/SI normalization','finite-volume grid remains implementation coordinate unless source-owned'],'methods':['exact source/parent hashing','J-WL-001 then J-WL-002 manufactured checks','J manufactured reference check','typed derivability audit against exact HI+P29+P30','provenance-bound covariance/fourier engines only if material bindings exist'],'tolerances':['covariance symmetry/PSD engine tolerance=1e-12','Fourier reconstruction tolerance=1e-10','no sample tolerance or convergence threshold may be invented before a lawful physical covariance is materialized'],'stopping_rules':['public initial-condition or target phase enters','manufactured covariance promoted','P30 pending proxy promoted','covariance non-PSD','unresolved __BIND token at attempted materialization','arbitrary mode dimension/basis/order','material covariance value absent from exact source/parent/hashed derivation','clean replay mismatch'],'expected_invariants':['exact parent hash unchanged','P29/P30 hashes unchanged','branch identity retained','no public input','manufactured checks remain implementation-only'],'tests':['J-WL-001','J-WL-002','manufactured J reference check','typed material-covariance derivability audit'],'gates':['covariance PSD','reality/Hermitian conditions','resolution and volume tests','no public initial-condition file','independent field reconstruction'],'falsifiers':['manufactured or public covariance enters physical generation','seed/branch shopping','invented mode dimension/order/amplitude'],'claim_boundary':deriv['claim_boundary'],'independent_verifier_design':'Re-hash exact HI, P29, and P30; independently verify whether a finite ordered physical mode basis, mode count, normalization/amplitude, and recursion-to-mode mapping are actually supplied. Refuse physical materialization if any are absent.','allowed_implementation_only_corrections':['syntax/path/serialization/evaluator-backend/solver plumbing only; preserve failure and rerun full frozen matrix; source set and derivation law are frozen science']}
(R/'PRE_EXECUTION_LOCK.json').write_text(json.dumps(lock,indent=2)+'\n')
env={'schema_version':'2.1','run_id':run,'status':'CAPTURED_PRE_EXECUTION','generation_mode':'GENERATION_SEALED','network_policy':'DISABLED_DURING_GENERATION','software':['python 3.11','numpy','scipy'],'imports':src['imports'],'hidden_defaults_audited':True,'public_inputs_used':False}
(R/'ENVIRONMENT.json').write_text(json.dumps(env,indent=2)+'\n')
print('NEW_RUN='+run); print('PARENT_SHA256='+sha(parent)); print('P29_SHA256='+sha(p29)); print('P30_SHA256='+sha(p30)); print('DERIVATION_SHA256='+dh)
PY
python tools/rfc.py doctor
python tools/director.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan
git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
git add -A
git commit -m 'Replace J-200 invalid freeze with correctly sourced run'
git pull --rebase origin agent/frontier-050-execution
git push origin HEAD:agent/frontier-050-execution
printf 'J200_SOURCE_REPAIR_COMMIT=%s\n' "$(git rev-parse HEAD)"
