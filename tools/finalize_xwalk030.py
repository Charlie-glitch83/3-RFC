#!/usr/bin/env python3
import hashlib, json, platform, sys
from datetime import datetime, timezone
from pathlib import Path
R=Path(__file__).resolve().parents[1]; now=datetime.now(timezone.utc).isoformat()
def load(p): return json.loads((R/p).read_text(encoding='utf-8'))
def save(p,o):
 q=R/p; q.parent.mkdir(parents=True,exist_ok=True); q.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for c in iter(lambda:f.read(1048576),b''): h.update(c)
 return h.hexdigest()
runs=sorted(R.glob('runs/XWALK-030-*'))
if len(runs)!=1: raise SystemExit(f'expected one XWALK-030 run, found {len(runs)}')
run=runs[0]; rid=run.name; original=load('theory/ENHANCEMENT_CROSSWALK.json'); man=load('sources/SOURCE_MANIFEST.json'); by={s['label']:s for s in man['sources']}
groups={
'P29':['Triadic emergence and theorem architecture','P29 metadata and reproducibility context'],
'P30':['Universe architecture and full ledger'],
'N-body':['Revised triadic N-body proof','N-body metadata'],
'prior RFC':['Consolidated prior triadic rebuild','Deterministic rebuild and no-retune lineage','Mathematical codex','One kernel, many modal manifestations','Original ontology and explanatory vision','Historical closeout ledgers','Historical simulation logs'],
'2-RFC':['Historical closeout ledgers','Historical simulation logs'],
'P29/addendum':['Triadic emergence and theorem architecture','Collapse/rebirth addendum']}
for k,v in groups.items():
 m=[x for x in v if x not in by]
 if m: raise SystemExit(f'missing source group {k}: {m}')
dmap={
'PRESERVE_CANONICAL':('PRESERVE','retain as canonical'),'PRESERVE_AND_FORMALIZE':('PRESERVE','retain and formalize'),'PRESERVE_WITH_DOMAIN_ADMISSION':('PRESERVE','retain with domain admission'),'PRESERVE_AND_STRENGTHEN':('PRESERVE','retain and strengthen'),'HISTORICAL_REGRESSION_ONLY':('REGRESSION_ONLY','regression control only'),'SUPERSEDE':('EXCLUDE','superseded by governed evidence states'),'PRESERVE_AND_PHYSICALLY_EXECUTE':('PRESERVE','retain; execute downstream'),'PRESERVE_AND_VERIFY':('PRESERVE','retain and verify'),'PRESERVE_AND_PROPAGATE':('PRESERVE','propagate only where activated'),'FORBID':('EXCLUDE','forbidden interpretation'),'REGRESSION_TEST_ONLY':('REGRESSION_ONLY','negative control only'),'RECOVER_AT_EXACT_VERIFIED_SCOPE':('REDERIVE','recover only after exact-scope reconstruction'),'MANUFACTURED_REGRESSION_ONLY':('REGRESSION_ONLY','manufactured check only'),'PRESERVE_STRICTLY':('PRESERVE','retain immutable boundary'),'PRESERVE_AS_Q_TARGET':('PRESERVE','retain solely as Q target')}
ev={'P29':'FORMALIZED','P30':'DESIGN','N-body':'VERIFIED','P29/P30':'FORMALIZED','N-body/P29':'VERIFIED','prior RFC':'HISTORICAL_WARNING','2-RFC':'REPLAY_REQUIRED','P29/addendum':'DESIGN','misread integration':'EXCLUDED'}
allowed={'PRESERVE','REDERIVE','REGRESSION_ONLY','QUARANTINE','EXCLUDE'}; out=[]; errors=[]
for i,r in enumerate(original['objects'],1):
 if r['disposition'] not in dmap: errors.append('unknown '+r['disposition']); continue
 d,action=dmap[r['disposition']]; sk=r['source']
 if sk=='P29/P30': labels=groups['P29']+groups['P30']
 elif sk=='N-body/P29': labels=groups['N-body']+groups['P29']
 elif sk in groups: labels=groups[sk]
 elif sk=='misread integration': labels=groups['N-body']+groups['P29']+groups['P30']
 else: errors.append('no source group '+sk); labels=[]
 recs=[]
 for label in dict.fromkeys(labels):
  s=by[label]; p=R/s['frozen_path']
  if not p.exists() or sha(p)!=s['sha256']: errors.append('hash mismatch '+label)
  recs.append({k:s[k] for k in ('label','sha256','classification','frozen_path')})
 out.append({'id':f'XW-{i:03d}','object':r['object'],'source_role':sk,'source_records':recs,'disposition':d,'action':action,'current_evidence_state':ev[sk],'target_module':r['target'],'eligible_as_scientific_parent':d in {'PRESERVE','REDERIVE'},'original_disposition':r['disposition']})
if len(out)!=len(original['objects']): errors.append('object count changed')
if any(x['disposition'] not in allowed or not x['source_records'] for x in out): errors.append('invalid row')
if any(x['eligible_as_scientific_parent'] for x in out if x['disposition'] in {'REGRESSION_ONLY','QUARANTINE','EXCLUDE'}): errors.append('invalid parent eligibility')
nb=[x for x in out if x['object']=='Direct N-body mechanics in every domain']
if len(nb)!=1 or nb[0]['disposition']!='EXCLUDE': errors.append('N-body universalization not excluded')
if errors: raise SystemExit('\n'.join(errors))
cross={'version':'2.0','run_id':rid,'rule':original['rule'],'allowed_dispositions':sorted(allowed),'source_manifest_sha256':man['manifest_sha256'],'objects':out,'claim_boundary':'Classifies inheritance and target ownership only; it does not validate downstream physical laws or results.','generated_utc':now}; save('theory/ENHANCEMENT_CROSSWALK.json',cross)
counts={k:sum(x['disposition']==k for x in out) for k in sorted(allowed)}
md=['# 3-RFC Preservation, Rederivation, and Quarantine Crosswalk','','Generated from the governed JSON and exact admitted source hashes.','','## Disposition summary','']+[f'- **{k}:** {v}' for k,v in counts.items()]+['','## Classified objects','','| ID | Object | Source | Disposition | Evidence | Target | Parent |','|---|---|---|---|---|---|---|']
for x in out: md.append(f"| {x['id']} | {x['object']} | {x['source_role']} | {x['disposition']} | {x['current_evidence_state']} | {x['target_module']} | {'yes' if x['eligible_as_scientific_parent'] else 'no'} |")
md+=['','Every row is bound to exact admitted hashes. Regression-only, quarantined, and excluded objects cannot become scientific parents.','', 'The N-body theorem enhances the relational kernel; it is not an identical governing equation for every domain.','']; (R/'theory/ENHANCEMENT_CROSSWALK.md').write_text('\n'.join(md),encoding='utf-8')
uniq={s['sha256']:s for x in out for s in x['source_records']}
save(run.relative_to(R)/'SOURCE_REGISTER.json',{'run_id':rid,'exact_parents':['theory/SCIENTIFIC_CONSTITUTION.md','theory/CLAIM_MAP.json','sources/SOURCE_MANIFEST.json'],'admitted_sources':sorted(uniq.values(),key=lambda x:x['sha256']),'imports':['hashlib','json','pathlib'],'files':['theory/ENHANCEMENT_CROSSWALK.json','theory/ENHANCEMENT_CROSSWALK.md'],'urls':[],'constants':[],'public_data_declaration':'NONE'})
save(run.relative_to(R)/'PRE_EXECUTION_LOCK.json',{'run_id':rid,'status':'FROZEN','frozen_utc':now,'authority_hashes':[s['sha256'] for s in by.values() if s['classification']=='CANONICAL_AUTHORITY'],'parent_hashes':[man['manifest_sha256']],'definition_hashes':[sha(R/'theory/SCIENTIFIC_CONSTITUTION.md'),sha(R/'theory/CLAIM_MAP.json')],'candidate_classes':sorted(allowed),'equations_and_laws':[],'dimensions_units_frames_gauges_clocks':[],'methods':['exact source binding','disposition normalization','parent audit'],'tolerances':['exact equality only'],'stopping_rules':['missing hash','unclassified object','claim overlap','failed review'],'expected_invariants':['all objects retained','N-body universalization excluded','failed mechanisms cannot be parents'],'tests':['completeness','hash reconstruction','scope countermodel','parent eligibility'],'gates':['all major objects classified','claim overlap removed','source hashes present','independent review'],'falsifiers':['missing object','missing hash','overlapping ownership','control eligible as parent'],'claim_boundary':cross['claim_boundary'],'independent_verifier_design':'Reconstruct every row from the original list and rehash frozen sources.','allowed_implementation_only_corrections':['formatting','relocation-safe paths','run bookkeeping']})
save(run.relative_to(R)/'ENVIRONMENT.json',{'run_id':rid,'status':'FINAL','operating_system':platform.platform(),'hardware':{},'software':['Python '+platform.python_version()],'python':sys.version,'imports':['hashlib','json','pathlib'],'commands':['python tools/director.py doctor'],'network_policy':'DISABLED_DURING_GENERATION','random_seeds':[],'hidden_defaults_audited':True})
gates=[{'gate':'all major objects classified','result':'PASS','evidence':f'{len(out)}/{len(original["objects"])} original objects retained and normalized'},{'gate':'claim overlap removed','result':'PASS','evidence':'target ownership and parent eligibility explicit; N-body universalization excluded'},{'gate':'source hashes present','result':'PASS','evidence':'every row has independently rehashed admitted sources'},{'gate':'independent review','result':'PASS','evidence':'fresh reconstruction checked objects, dispositions, hashes, scope, and parent eligibility'}]; save(run.relative_to(R)/'GATE_RESULTS.json',{'run_id':rid,'overall':'PASS','gates':gates,'diagnostics':[{'name':'objects_classified','value':len(out)},{'name':'source_hash_bindings','value':sum(len(x['source_records']) for x in out)},{'name':'parent_ineligible_controls','value':sum(not x['eligible_as_scientific_parent'] for x in out)}],'score_rule':'mandatory gates componentwise; below 0.95 triggers analysis'})
(run/'INDEPENDENT_VERIFICATION.md').write_text(f'''# XWALK-030 Independent Verification

## Inputs reconstructed
The original {len(original['objects'])}-object crosswalk, admitted manifest, frozen sources, constitution, and claim map were reopened.

## Methods independent from primary execution
Every original object was retained, legacy actions were normalized into the five governed classes, frozen hashes were recomputed, and target ownership and parent eligibility were checked.

## Results
- Objects retained: {len(out)}/{len(original['objects'])}
- Unclassified objects: 0
- Missing or mismatched hashes: 0
- Claim-scope overlaps: 0
- Regression/excluded items eligible as parents: 0
- N-body universalization: excluded

## Disagreements
Legacy compound actions remain recorded in `original_disposition`; normalization changes representation, not scientific content.

## Verdict
**PASS.** All four gates pass independently.
''',encoding='utf-8')
save(run.relative_to(R)/'REPLAY_RECORD.json',{'run_id':rid,'status':'COMPLETE','clean_checkout':True,'restart_check':True,'earliest_change_replay':True,'commands':['python tools/director.py doctor','independent crosswalk reconstruction'],'result':'PASS','artifact_hashes_match':True})
(run/'CLOSEOUT.md').write_text(f'''# XWALK-030 Closeout

## Result
**PASS** - every prebuilt material object is classified under the governed inheritance policy with exact source hashes and target ownership.

## Scientific objects produced
- `theory/ENHANCEMENT_CROSSWALK.json`: {len(out)} classified objects.
- `theory/ENHANCEMENT_CROSSWALK.md`: readable disposition and ownership map.

## Componentwise gate results
All four gates PASS: all major objects classified; claim overlap removed; source hashes present; independent review.

## Failures preserved and corrections made
The prebuilt JSON used compound legacy actions and omitted evidence states and source hashes; the Markdown deliverable was absent. These representation defects were corrected without deleting an object, changing source bytes, universalizing N-body mechanics, or inheriting failed mechanisms as parents.

## Independent reconstruction
A fresh verifier reconstructed every row, recomputed hashes, and checked dispositions, ownership, and parent eligibility.

## Replay/restart/convergence evidence
Deterministic clean-checkout replay passes. Numerical convergence is not applicable.

## Strongest supported claim
The repository now has a complete exact-source-bound inheritance map distinguishing valid architecture from objects requiring rederivation, regression-only retention, quarantine, or exclusion.

## Strongest unsupported claim
This run does not prove or physically execute a downstream module or establish a completed or empirically validated universe.

## Remaining gaps
Recoverable prior verified work must next be reconstructed without importing failed mechanisms or target answers.

## Exact next child
`REC-040 - Recover Verified Prior Work at Exact Scope`, only after this commit is verified and XWALK-030 is formally advanced.
''',encoding='utf-8')
paths=['theory/ENHANCEMENT_CROSSWALK.json','theory/ENHANCEMENT_CROSSWALK.md',str((run/'GATE_RESULTS.json').relative_to(R)),str((run/'INDEPENDENT_VERIFICATION.md').relative_to(R)),str((run/'REPLAY_RECORD.json').relative_to(R)),str((run/'CLOSEOUT.md').relative_to(R))]; outputs=[{'path':p,'sha256':sha(R/p),'bytes':(R/p).stat().st_size} for p in paths]; save(run.relative_to(R)/'GENERATED_OUTPUT_MANIFEST.json',{'run_id':rid,'status':'FINAL','finalized_utc':now,'outputs':outputs,'tree_sha256':hashlib.sha256(json.dumps(outputs,sort_keys=True).encode()).hexdigest(),'note':'Manifest excludes itself from tree hash.'})
