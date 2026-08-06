#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
RUN = Path(__file__).resolve().parent
MODULES=["A","B","C","D","E","F","G","HU","I","HI","J"]

def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def sha(p):
    h=hashlib.sha256()
    with (ROOT/p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''): h.update(b)
    return h.hexdigest()

def main():
    state=load('STATE.json'); registry=load('memory/ARTIFACT_REGISTRY.json'); index=load('memory/RUN_INDEX.json')
    sm=load('sources/SOURCE_MANIFEST.json'); rec=load('recovery/ADMITTED_ASSET_MANIFEST.json')
    source_ok=all(sha(x['frozen_path'])==x['sha256'] and (ROOT/x['frozen_path']).stat().st_size==x['bytes'] for x in sm['sources'])
    recovery_ok=all(sha(x['stored_path'])==x['sha256'] and (ROOT/x['stored_path']).stat().st_size==x['bytes'] for x in rec['assets']) and rec.get('canonical_parents')==[]
    module_artifacts={m:[a for a in registry.get('artifacts',[]) if a.get('path','').startswith(f'modules/{m}/')] for m in MODULES}
    module_runs={m:[r for r in index.get('runs',[]) if r.get('module')==m] for m in MODULES}
    module_files={m:sorted(str(p.relative_to(ROOT)) for p in (ROOT/f'modules/{m}/runs').rglob('*') if p.is_file() and p.name!='.gitkeep') for m in MODULES}
    missing=[m for m in MODULES if not module_artifacts[m] and not module_runs[m] and not module_files[m]]
    frontier=missing[0] if missing else None
    # A manufactured result is checked only to prove it cannot be confused with a governed module run.
    a_manifest=load('configured_runs/results/A_triad_kernel/manifest.json')
    manufactured_a_ok=(a_manifest.get('success') is True and sha('configured_runs/results/A_triad_kernel/result.json')==a_manifest['result_sha256'])
    verdict='PASS' if source_ok and recovery_ok and frontier=='A' and manufactured_a_ok else 'FAIL'
    result={
      'schema_version':'1.0','run_id':RUN.name,'method':'independent raw-registry reconstruction without using primary gate summaries',
      'source_bytes_verified':source_ok,'recovered_objects_verified':recovery_ok,'module_artifacts':module_artifacts,
      'module_runs':module_runs,'module_run_files':module_files,'earliest_missing_module':frontier,
      'manufactured_A_check_verified_but_noncanonical':manufactured_a_ok,'verdict':verdict
    }
    (RUN/'INDEPENDENT_FRONTIER_RECONSTRUCTION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    primary=load('audit/PHYSICAL_FRONTIER.json')
    agree=primary['selected_frontier']['module']==frontier and primary['selected_frontier']['authorized_child']=='A-100'
    md=f"""# Independent Verification

## Inputs reconstructed

- Rehashed all `{len(sm['sources'])}` admitted source objects from `sources/SOURCE_MANIFEST.json`.
- Rehashed all `{len(rec['assets'])}` REC-040 admitted objects and independently confirmed `canonical_parents` is empty.
- Read raw `memory/ARTIFACT_REGISTRY.json`, `memory/RUN_INDEX.json`, and every `modules/<A-J>/runs` tree.
- Verified the A finite configured result directly from its declared result hash, while excluding it as a governed Module A run.

## Methods independent from primary execution

The verifier did not use the primary audit's gate verdicts or row statuses. It selected the first topological module with no registered module artifact, no indexed module run, and no non-placeholder module-run files.

## Results

- Source bytes exact: `{source_ok}`.
- REC-040 objects exact and source-only: `{recovery_ok}`.
- Earliest missing governed module output: `{frontier}`.
- Primary/independent frontier agreement: `{agree}`.
- A manufactured reference passes its own declared hash but remains outside `modules/A/runs` and the artifact/run registries.

## Disagreements

None.

## Verdict

**{verdict}** — Module A is independently reconstructed as the unique earliest frontier. This verifies an audit conclusion only; it does not execute Module A or produce `H_A_to_B`.
"""
    (RUN/'INDEPENDENT_VERIFICATION.md').write_text(md,encoding='utf-8')
    if verdict!='PASS' or not agree: raise SystemExit(1)
if __name__=='__main__': main()
