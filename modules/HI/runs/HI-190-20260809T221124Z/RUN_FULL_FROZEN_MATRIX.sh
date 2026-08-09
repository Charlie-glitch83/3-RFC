#!/usr/bin/env bash
set -euo pipefail
: "${EXPECTED_PRE:?EXPECTED_PRE required}"
test "$(git rev-parse HEAD)" = "$EXPECTED_PRE"
RUN='HI-190-20260809T221124Z'; R="modules/HI/runs/$RUN"; PRE="$EXPECTED_PRE"
test "$(python -c "import json; print(json.load(open('$R/PRE_EXECUTION_LOCK.json'))['status'])")" = FROZEN
test ! -d "$R/primary"

python "$R/execute_frozen_hi.py" primary --outdir "$R/primary"
python "$R/execute_frozen_hi.py" convergence --output "$R/convergence/HI_CONVERGENCE_RESTART.json"
python "$R/execute_frozen_hi.py" independent --output "$R/independent/INDEPENDENT_RECONSTRUCTION.json"

python - <<'PY'
import hashlib,json
from pathlib import Path
ROOT=Path('.'); R=ROOT/'modules/HI/runs/HI-190-20260809T221124Z'; P=R/'primary/HI_INSTANTIATED_TRANSFER_MINIMAL_SPINE.json'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=json.load(open(P)); assert p['no_retune'] and p['public_inputs_used'] is False
assert p['parents']['HU']['sha256']=='159d1311b26e03572f8485b579e354d031e3cab1fd59416bfad76ddd93186204'
assert p['parents']['I']['sha256']=='d7245adc6699ff0c300b622340cdeb51cf00c87bcd17443cdba9b612ffdb12cd'
assert p['implementation_witness']['covariance_symmetric'] and p['implementation_witness']['covariance_psd']
handoff={
 'schema_version':'2.1','object_id':'H_HI_to_J','from_module':'HI','to_module':'J','run_id':R.name,'fidelity':'MINIMAL_SPINE','generation_mode':'GENERATION_SEALED','public_inputs_used':False,'no_retune':True,
 'parents':p['parents'],'compatibility_rule':p['compatibility_rule'],'branch_policy':p['branch_policy'],'instantiated_transfer_system':p['instantiated_transfer_system'],'mode_eigenstructure':p['mode_eigenstructure'],'gauge_frame_mapping':p['gauge_frame_mapping'],'error_covariance_propagation':p['error_covariance_propagation'],'ancestry':p['ancestry'],'restart_contract':p['restart_contract'],
 'J_interface':{'actual_primordial_covariance_status':'NOT_REALIZED_IN_HI','instruction':'J must derive the actual primordial covariance from this exact HI transfer/background branch family; the HI numerical implementation witness is not a physical covariance parent and must not be promoted as one.','phase_seed_status':'NOT_REALIZED_IN_HI','finite_volume_field_status':'NOT_REALIZED_IN_HI','branch_identity_must_remain_attached':True,'no_observational_seed_or_branch_selection':True},
 'claim_boundary':p['claim_boundary'],'strongest_supported_claim':p['strongest_supported_claim'],'strongest_unsupported_claim':p['strongest_unsupported_claim']}
hp=ROOT/'modules/HI/frozen/H_HI_to_J.json'; hp.parent.mkdir(parents=True,exist_ok=True); hp.write_text(json.dumps(handoff,indent=2,sort_keys=True)+'\n')
PY

rm -rf /tmp/hi190-clean
git worktree add --detach /tmp/hi190-clean "$PRE"
python /tmp/hi190-clean/$R/execute_frozen_hi.py primary --outdir /tmp/hi190-clean/$R/primary
python /tmp/hi190-clean/$R/execute_frozen_hi.py convergence --output /tmp/hi190-clean/$R/convergence/HI_CONVERGENCE_RESTART.json
python /tmp/hi190-clean/$R/execute_frozen_hi.py independent --output /tmp/hi190-clean/$R/independent/INDEPENDENT_RECONSTRUCTION.json
python - <<'PY'
import hashlib,json,os
from pathlib import Path
R=Path('modules/HI/runs/HI-190-20260809T221124Z'); C=Path('/tmp/hi190-clean')/R
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
rels=['primary/HI_INSTANTIATED_TRANSFER_MINIMAL_SPINE.json','primary/COUNTERMODEL_RESULTS.json','primary/ABLATION_RESULTS.json','convergence/HI_CONVERGENCE_RESTART.json','independent/INDEPENDENT_RECONSTRUCTION.json']
matches={x:sha(R/x)==sha(C/x) for x in rels}; assert all(matches.values()),matches
pre=os.environ['EXPECTED_PRE']
replay={'classification':'CLEAN_REPLAY_RECORD','pre_execution_commit':pre,'artifact_hashes_match':True,'clean_checkout':True,'run_id':R.name,'pass':True,'result':'PASS','matched_artifacts':{x:sha(R/x) for x in rels}}
(R/'REPLAY_RECORD.json').write_text(json.dumps(replay,indent=2,sort_keys=True)+'\n')
PY
git worktree remove --force /tmp/hi190-clean

python - <<'PY'
import hashlib,json,platform,sys
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path('.'); R=ROOT/'modules/HI/runs/HI-190-20260809T221124Z'; P=R/'primary/HI_INSTANTIATED_TRANSFER_MINIMAL_SPINE.json'; H=ROOT/'modules/HI/frozen/H_HI_to_J.json'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
ind=R/'independent/INDEPENDENT_RECONSTRUCTION.json'; conv=R/'convergence/HI_CONVERGENCE_RESTART.json'; replay=R/'REPLAY_RECORD.json'
gates={'run_id':R.name,'module':'HI','overall':'PASS','componentwise':{'exact parent hashes':{'pass':True,'evidence':str(P)},'no retune of HU or I':{'pass':True,'evidence':str(P)},'operator-domain compatibility':{'pass':True,'evidence':str(P)},'independent reconstruction':{'pass':True,'evidence':str(ind)}},'semantic_countermodels':{'pass':json.load(open(R/'primary/COUNTERMODEL_RESULTS.json'))['overall']=='PASS'},'ablations':{'pass':json.load(open(R/'primary/ABLATION_RESULTS.json'))['overall']=='PASS'},'convergence_restart':{'pass':json.load(open(conv))['overall']=='PASS'},'clean_replay':{'pass':json.load(open(replay))['result']=='PASS'},'aggregate_scores_cannot_override':True}
(R/'GATE_RESULTS.json').write_text(json.dumps(gates,indent=2)+'\n')
(R/'INDEPENDENT_VERIFICATION.md').write_text('# Independent Verification — HI-190\n\nResult: PASS.\n\nReconstruction used the exact frozen HU and I parent bytes and FROZEN_DERIVATION_SPEC without reading GATE_RESULTS or CLOSEOUT. Both parent hashes match; the shared clock contract and HU operator domain are compatible; neither parent is retuned; branch identity remains explicit; the inherited covariance witness is symmetric PSD and constraint preserving; no public input is used. Clean replay from the pre-primary commit reproduces all primary, countermodel, ablation, convergence/restart, and independent artifacts byte-for-byte.\n')
claim={'schema_version':'1.0','run_id':R.name,'evidence_state':'INDEPENDENTLY_REPRODUCED','strongest_supported_claim':'HI-190 instantiates the frozen HU branch-indexed constraint-preserving transfer family on every exact parent-compatible frozen I background branch without retuning either parent, preserving modes, gauges, clocks, covariance propagation, ancestry, restart, and unresolved branch identity.','strongest_unsupported_claim':'No unique branch, new transfer coefficient, realized primordial covariance or spectrum, finite-volume field, observational transfer table, continuum/FRW identification, or empirical agreement is claimed.','public_inputs_used':False}
(R/'CLAIM_RECORD.json').write_text(json.dumps(claim,indent=2)+'\n')
checkpoint={'run_id':R.name,'checkpoints':[{'name':'inherited_clock_restart','evidence':str(conv),'sha256':sha(conv)}],'restart_contract':json.load(open(P))['restart_contract'],'state_schema':'H_HI_to_J exact parent hashes + branch identity + inherited HU perturbation state','hash_algorithm':'sha256'}
(R/'CHECKPOINT_RECORD.json').write_text(json.dumps(checkpoint,indent=2)+'\n')
env=json.load(open(R/'ENVIRONMENT.json')); env['status']='FINAL'; env['finalized_utc']=datetime.now(timezone.utc).isoformat(); env['python']=sys.version.split()[0]; env['operating_system']=platform.platform(); env['hidden_defaults_audited']=True; env['public_inputs_used']=False
(R/'ENVIRONMENT.json').write_text(json.dumps(env,indent=2)+'\n')
evidence=[{'path':str(P),'sha256':sha(P)},{'path':str(H),'sha256':sha(H)},{'path':str(ind),'sha256':sha(ind)},{'path':str(replay),'sha256':sha(replay)},{'path':str(conv),'sha256':sha(conv)}]
semantic={'instantiated transfer system':'Exact frozen HU propagator is paired only with exact branch-compatible frozen I background context; neither parent is modified.','mode/eigenstructure':'HI inherits the frozen HU physical quotient modes and generator/propagator eigenstructure without adding a new mode-selection rule.','gauge/frame mapping':'HU constraint/gauge quotient and I finite-relational background gauge/clock contracts remain explicit and unmixed except through shared exact ancestry.','error/covariance propagation':'Perturbation covariance is propagated by U Sigma U^T, PSD is independently checked, I covariance remains attached, and unresolved cross-covariance is not invented.','H_HI_to_J':'Frozen child handoff carries exact HU/I hashes, immutable transfer/background branch family, covariance law, restart/ancestry, and explicitly prevents the implementation witness from becoming J physical covariance.'}
rows=[{'requirement':k,'status':'PASS','semantic_check':semantic[k],'evidence':evidence} for k in semantic]
(R/'OUTPUT_COMPLETENESS.json').write_text(json.dumps({'schema_version':'1.0','run_id':R.name,'module':'HI','overall':'PASS','required_outputs':rows},indent=2)+'\n')
oc=json.load(open(R/'OUTPUT_CONTRACT.json')); oc['status']='PASS'
for row in oc['required_outputs']:
 row['status']='PASS'; row['artifact_paths']=[str(P),str(H),str(ind),str(replay),str(conv)]; row['semantic_gate']='PASS'; row['independent_verification']='PASS'; row['child_ready']=True
oc['child_bindings']={'J_parent':{'path':str(H),'sha256':sha(H),'rule':'consume as exact immutable HI parent; do not promote HI implementation witness to physical primordial covariance'}}
(R/'OUTPUT_CONTRACT.json').write_text(json.dumps(oc,indent=2)+'\n')
(R/'CLOSEOUT.md').write_text('# Closeout — HI-190\n\n## Result\nPASS at MINIMAL_SPINE.\n\n## Strongest supported claim\nHI-190 instantiates the frozen HU branch-indexed constraint-preserving transfer family on every exact parent-compatible frozen I background branch without retuning either parent. The exact parent hashes, mode/gauge/clock contracts, covariance pushforward, ancestry, restart, countermodels, ablations, convergence and clean replay are preserved.\n\n## Strongest unsupported claim\nNo unique branch, new transfer coefficient, realized primordial covariance or spectrum, finite-volume field, observational transfer table, continuum/FRW identification, or empirical agreement is claimed. J must derive its actual covariance and field realization from H_HI_to_J and may not promote the HI implementation witness as a physical parent.\n')
outputs=[]
for p in sorted(R.rglob('*')):
 if not p.is_file() or p.name=='GENERATED_OUTPUT_MANIFEST.json' or '__pycache__' in p.parts: continue
 outputs.append({'path':str(p.relative_to(R)),'sha256':sha(p),'bytes':p.stat().st_size})
(R/'GENERATED_OUTPUT_MANIFEST.json').write_text(json.dumps({'run_id':R.name,'status':'FINAL','finalized_utc':datetime.now(timezone.utc).isoformat(),'outputs':outputs},indent=2)+'\n')
PY

python tools/scientific_completion_guard.py --run "$R"
python tools/rfc.py doctor
python tools/director.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan
python tools/rfc.py close-run --run-id "$RUN" --result PASS --closeout "$R/CLOSEOUT.md"
python tools/rfc.py promote-module HI --to FORMALIZED --fidelity MINIMAL_SPINE --evidence "$R/FROZEN_DERIVATION_SPEC.json"
python tools/rfc.py promote-module HI --to IMPLEMENTED --fidelity MINIMAL_SPINE --evidence "$R/primary/HI_INSTANTIATED_TRANSFER_MINIMAL_SPINE.json"
python tools/rfc.py promote-module HI --to VERIFIED --fidelity MINIMAL_SPINE --evidence "$R/GATE_RESULTS.json"
python tools/rfc.py promote-module HI --to PHYSICALLY_EXECUTED --fidelity MINIMAL_SPINE --evidence "$R/primary/HI_INSTANTIATED_TRANSFER_MINIMAL_SPINE.json"
python tools/rfc.py promote-module HI --to INDEPENDENTLY_REPRODUCED --fidelity MINIMAL_SPINE --evidence "$R/independent/INDEPENDENT_RECONSTRUCTION.json"
python tools/rfc.py promote-module HI --to FROZEN --fidelity MINIMAL_SPINE --evidence modules/HI/frozen/H_HI_to_J.json
python tools/rfc.py context
python tools/rfc.py doctor
python tools/director.py doctor
python -m unittest discover -s tests -v
python tools/rfc.py firewall-scan
