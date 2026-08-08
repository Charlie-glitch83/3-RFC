#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,shutil
from pathlib import Path

COMMIT='b0f21d023f64ce9c70fd4755dfdbb7357b9f7a10'
REPO='Charlie-glitch83/2-RFC'
SELECTED=[
'architecture/2RFC_DETAILED_SCIENTIFIC_GAP_TO_LIBRARY_REPAIR_PLAN.md','architecture/2RFC_MANUSCRIPT_SOURCE_TRACEABILITY_RULES.md','architecture/2RFC_WOLFRAM_INTEGRATION_RULES.md',
'modules/B/MODULE_B_DETAILED_SCIENTIFIC_REPAIR_PLAN.md','modules/B/MODULE_B_MANUSCRIPT_SOURCE_TRACEABILITY.md','modules/B/MODULE_B_WOLFRAM_INTEGRATION_REVISION.md','modules/B/MODULE_B_WOLFRAM_VERIFICATION.md','modules/B/MODULE_B_TO_C_SCIENTIFIC_HANDOFF.md',
'modules/C/MODULE_C_DETAILED_SCIENTIFIC_REPAIR_PLAN.md','modules/C/MODULE_C_MANUSCRIPT_SOURCE_TRACEABILITY.md','modules/C/MODULE_C_WOLFRAM_INTEGRATION_REVISION.md','modules/C/MODULE_C_WOLFRAM_VERIFICATION.md','modules/C/MODULE_C_TO_D_SCIENTIFIC_HANDOFF.md',
'modules/D/MODULE_D_DETAILED_SCIENTIFIC_REPAIR_PLAN.md','modules/D/MODULE_D_MANUSCRIPT_SOURCE_TRACEABILITY.md','modules/D/MODULE_D_WOLFRAM_INTEGRATION_REVISION.md','modules/D/MODULE_D_WOLFRAM_VERIFICATION.md','modules/D/MODULE_D_TO_E_SCIENTIFIC_HANDOFF.md',
'modules/E/MODULE_E_DETAILED_SCIENTIFIC_REPAIR_PLAN.md','modules/E/MODULE_E_MANUSCRIPT_SOURCE_TRACEABILITY.md','modules/E/MODULE_E_WOLFRAM_INTEGRATION_REVISION.md','modules/E/MODULE_E_WOLFRAM_VERIFICATION.md','modules/E/MODULE_E_TO_F_SCIENTIFIC_HANDOFF.md',
'modules/F/MODULE_F_DETAILED_SCIENTIFIC_REPAIR_PLAN.md','modules/F/MODULE_F_MANUSCRIPT_SOURCE_TRACEABILITY.md','modules/F/MODULE_F_WOLFRAM_INTEGRATION_REVISION.md','modules/F/MODULE_F_WOLFRAM_VERIFICATION.md','modules/F/MODULE_F_TO_G_SCIENTIFIC_HANDOFF.md',
'modules/G/MODULE_G_DETAILED_SCIENTIFIC_REPAIR_PLAN.md','modules/G/MODULE_G_MANUSCRIPT_SOURCE_TRACEABILITY.md','modules/G/MODULE_G_WOLFRAM_INTEGRATION_REVISION.md','modules/G/MODULE_G_WOLFRAM_VERIFICATION.md','modules/G/MODULE_G_TO_H_UNIT_SCIENTIFIC_HANDOFF.md',
'proofs/GENESIS_REALIZATION.md','proofs/MICROSCOPIC_CONSTITUTION.md','proofs/THERMAL_EVOLUTION.md','proofs/PRIMORDIAL_NUCLEOSYNTHESIS.md','proofs/POST_NUCLEAR_PERSISTENCE.md','proofs/NONEQUILIBRIUM_RECOMBINATION.md',
'science/PHYSICAL_REALIZATION.md','science/MICROSCOPIC_PHYSICS.md','science/THERMAL_EVOLUTION.md','science/PRIMORDIAL_NUCLEOSYNTHESIS.md','science/POST_NUCLEAR_PLASMA.md','science/NONEQUILIBRIUM_RECOMBINATION.md']

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def flatten(x):
    if isinstance(x,dict):
        if all(k in x for k in ('repository','commit','path','sha256')): yield x
        for v in x.values(): yield from flatten(v)
    elif isinstance(x,list):
        for v in x: yield from flatten(v)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--source-root',required=True); a=ap.parse_args()
    root=Path(__file__).resolve().parents[1]; src=Path(a.source_root).resolve(); cross=json.loads((root/'recovery/LINEAGE_CROSSWALK.json').read_text())
    records={(r['repository'],r['commit'],r['path']):r for r in flatten(cross)}
    dest=root/'recovery/admitted/2-RFC'/COMMIT; out=[]
    for rel in SELECTED:
        key=(REPO,COMMIT,rel)
        if key not in records: raise SystemExit(f'HARD STOP: crosswalk lacks {rel}')
        r=records[key]; sp=src/rel
        if not sp.is_file(): raise SystemExit(f'HARD STOP: source missing {rel}')
        h=sha(sp)
        if h!=r['sha256']: raise SystemExit(f'HARD STOP: hash mismatch {rel}: {h} != {r["sha256"]}')
        dp=dest/rel; dp.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(sp,dp)
        if sha(dp)!=h: raise SystemExit(f'HARD STOP: copied hash mismatch {rel}')
        out.append({'repository':REPO,'commit':COMMIT,'path':rel,'sha256':h,'bytes':sp.stat().st_size,'classification':'REPLAY_REQUIRED','prior_crosswalk_classification':r.get('classification'),'scientific_role':'Candidate formal derivation/handoff/verification design for exact parent-bound replay; prior PASS/status is not inherited.'})
    manifest={'schema_version':'1.0','object_id':'BG_REPLAY_CANDIDATE_MANIFEST','status':'RECOVERED_EXACT_BYTES_PENDING_SEQUENTIAL_REPLAY','source_repository':REPO,'source_commit':COMMIT,'authority_rule':'P29, revised N-body, P30, exact current parents and live 3-RFC module specs/recipes control. Recovered B-G objects are REPLAY_REQUIRED candidates only; no old PASS or empirical identification is inherited.','objects':out}
    mp=root/'recovery/BG_REPLAY_CANDIDATE_MANIFEST.json'; mp.write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'status':'PASS','objects':len(out),'manifest':str(mp.relative_to(root))},indent=2))
if __name__=='__main__': main()
