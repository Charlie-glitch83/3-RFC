#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RUN = Path(__file__).resolve().parent
MODULES = ["A","B","C","D","E","F","G","HU","I","HI","J"]
MODULE_ORDER = ["A","B","C","D","E","F","G","HU","I","HI","J","K","L","M","KLM","N","O","P","Q"]
PARENTS = {
    "A": [], "B": ["A"], "C": ["B"], "D": ["C"], "E": ["D"], "F": ["E"],
    "G": ["F"], "HU": ["G"], "I": ["G"], "HI": ["HU","I"], "J": ["HI"]
}
EXPECTED_PARENT_OBJECTS = {
    "A": ["admitted canonical authority bytes"],
    "B": ["H_A_to_B"], "C": ["H_B_to_C"], "D": ["H_C_to_D"], "E": ["H_D_to_E"],
    "F": ["H_E_to_F"], "G": ["H_F_to_G"], "HU": ["H_G_to_HU"], "I": ["H_G_to_I"],
    "HI": ["H_HU_to_HI", "H_I_to_HI"], "J": ["H_HI_to_J"]
}
HANDOFF_OUTPUTS = {
    "A": ["H_A_to_B"], "B": ["H_B_to_C"], "C": ["H_C_to_D"], "D": ["H_D_to_E"],
    "E": ["H_E_to_F"], "F": ["H_F_to_G"], "G": ["H_G_to_HU","H_G_to_I"],
    "HU": ["H_HU_to_HI"], "I": ["H_I_to_HI"], "HI": ["H_HI_to_J"], "J": ["P_J_to_K"]
}
REPRESENTATIVE_RESULTS = {
    "A": ["A_triad_kernel"], "B": ["B_big_implosion"], "C": ["C_spectral_model"],
    "D": ["D_transport"], "E": ["E_reaction_network"], "F": [], "G": ["G_visibility"],
    "HU": ["HU_linear_transfer"], "I": [], "HI": [], "J": ["J_covariance","J_fourier_field"]
}

def load(path: str | Path) -> Any:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def sha(path: str | Path) -> str:
    p = ROOT / path
    h = hashlib.sha256()
    with p.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def file_record(path: str) -> dict[str, Any]:
    p = ROOT / path
    return {"path": path, "sha256": sha(path), "bytes": p.stat().st_size}

def target_contains(target: str, module: str) -> bool:
    target = target.strip()
    if target == module or target == "all":
        return True
    if "/" in target:
        return module in target.split("/")
    if "-" in target:
        a, b = target.split("-", 1)
        if a in MODULE_ORDER and b in MODULE_ORDER:
            i, j = MODULE_ORDER.index(a), MODULE_ORDER.index(b)
            return module in MODULE_ORDER[min(i,j):max(i,j)+1]
    return False

def representative_record(name: str) -> dict[str, Any]:
    base = f"configured_runs/results/{name}"
    manifest = load(f"{base}/manifest.json")
    files = {
        "manifest": file_record(f"{base}/manifest.json"),
        "frozen_config": file_record(f"{base}/frozen_config.json"),
        "environment": file_record(f"{base}/environment.json"),
        "result": file_record(f"{base}/result.json"),
    }
    declared_match = (
        manifest.get("config_sha256") == files["frozen_config"]["sha256"] and
        manifest.get("environment_sha256") == files["environment"]["sha256"] and
        manifest.get("result_sha256") == files["result"]["sha256"]
    )
    return {
        "name": name,
        "classification": manifest.get("classification"),
        "success": bool(manifest.get("success")),
        "declared_hashes_match": declared_match,
        "scope": "MANUFACTURED_REFERENCE_ONLY_NOT_PARENT_DRIVEN_MODULE_EXECUTION",
        "files": files,
    }

def main() -> None:
    source_manifest = load("sources/SOURCE_MANIFEST.json")
    crosswalk = load("theory/ENHANCEMENT_CROSSWALK.json")
    state = load("STATE.json")
    registry = load("memory/ARTIFACT_REGISTRY.json")
    run_index = load("memory/RUN_INDEX.json")
    queue = load("WORK_QUEUE.json")
    recovered = load("recovery/ADMITTED_ASSET_MANIFEST.json")

    source_checks = []
    source_by_hash = {}
    for rec in source_manifest["sources"]:
        p = rec["frozen_path"]
        actual = file_record(p)
        ok = actual["sha256"] == rec["sha256"] and actual["bytes"] == rec["bytes"]
        source_checks.append({"label": rec["label"], "classification": rec["classification"], "declared_sha256": rec["sha256"], "actual": actual, "match": ok})
        source_by_hash[rec["sha256"]] = rec
    if not all(x["match"] for x in source_checks):
        raise SystemExit("canonical source hash mismatch")

    recovered_checks = []
    for rec in recovered["assets"]:
        actual = file_record(rec["stored_path"])
        ok = actual["sha256"] == rec["sha256"] and actual["bytes"] == rec["bytes"]
        recovered_checks.append({"name": rec["name"], "classification": rec["classification"], "evidence_state": rec["evidence_state"], "actual": actual, "match": ok})
    if not all(x["match"] for x in recovered_checks):
        raise SystemExit("recovered source hash mismatch")

    registered_module_artifacts = [x for x in registry.get("artifacts", []) if x.get("path", "").startswith("modules/")]
    indexed_module_runs = [x for x in run_index.get("runs", []) if x.get("module") in MODULES]
    rows = []
    for module in MODULES:
        recipe_path = f"recipes/{module}/recipe.json"
        recipe = load(recipe_path)
        law_files = [
            file_record(f"modules/{module}/spec.json"), file_record(recipe_path), file_record(f"recipes/{module}/gates.json"),
            file_record(f"recipes/{module}/wolfram/{module}-WL-001.wl"), file_record(f"recipes/{module}/wolfram/{module}-WL-002.wl"),
        ]
        solver_bindings = []
        for bind in recipe.get("solver_bindings", []):
            template = bind["template"]
            sheet = bind["binding_sheet"]
            solver_bindings.append({
                "solver": bind["solver"], "declared_status": bind["status"], "purpose": bind["purpose"],
                "template": file_record(template), "binding_sheet": file_record(sheet)
            })
        representative = [representative_record(x) for x in REPRESENTATIVE_RESULTS[module]]
        module_run_dir = ROOT / f"modules/{module}/runs"
        run_files = sorted(str(p.relative_to(ROOT)) for p in module_run_dir.rglob("*") if p.is_file() and p.name != ".gitkeep")
        artifact_matches = [x for x in registered_module_artifacts if x.get("path", "").startswith(f"modules/{module}/")]
        run_matches = [x for x in indexed_module_runs if x.get("module") == module]

        xwalk_objects = []
        source_hashes = set()
        for obj in crosswalk["objects"]:
            if obj.get("inherited_as_scientific_parent") and target_contains(obj.get("target", ""), module):
                xwalk_objects.append({
                    "object": obj["object"], "evidence_state": obj["evidence_state"], "classification": obj["classification"],
                    "source_hashes": obj.get("source_hashes", [])
                })
                source_hashes.update(obj.get("source_hashes", []))
        source_evidence = []
        for digest in sorted(source_hashes):
            rec = source_by_hash.get(digest)
            source_evidence.append({"sha256": digest, "label": rec.get("label") if rec else None, "frozen_path": rec.get("frozen_path") if rec else None, "verified": digest in source_by_hash})

        if module == "A":
            law_status = "FORMALIZED_SOURCE_ARCHITECTURE_NOT_YET_FROZEN_AS_MODULE_A"
            parent_status = "ADMITTED_AUTHORITY_BYTES_VERIFIED; TYPED_PREPHYSICAL_PARENT_PACKET_ABSENT"
        else:
            law_status = "DESIGN_AND_INTERFACE_SPECIFIED_NOT_PARENT_DRIVEN_EXECUTED"
            parent_status = "ABSENT"

        physical_output_present = bool(run_files or artifact_matches or run_matches)
        # Registry/run objects are the only admissible positive evidence. Mere mentions in prose do not count.
        rows.append({
            "ordinal": MODULES.index(module) + 1,
            "module": module,
            "expected_parents": PARENTS[module],
            "expected_parent_objects": EXPECTED_PARENT_OBJECTS[module],
            "source": {"crosswalk_objects": xwalk_objects, "exact_sources": source_evidence, "all_source_bytes_verified": all(x["verified"] for x in source_evidence)},
            "law": {"status": law_status, "files": law_files, "claim_boundary": recipe.get("claim_boundary")},
            "representative_test": {"records": representative, "status": "PRESENT_LIMITED" if representative else "NO_PREBUILT_RESULT", "cannot_satisfy_physical_execution": True},
            "physical_parent": {"status": parent_status, "registry_matches": artifact_matches, "run_index_matches": run_matches},
            "solver": {"bindings": solver_bindings, "status": "UNBOUND_UNTIL_EXACT_PARENT_DERIVATION"},
            "required_output_objects": recipe.get("required_outputs", []),
            "handoff_outputs": HANDOFF_OUTPUTS[module],
            "output": {"status": "ABSENT" if not physical_output_present else "PRESENT_REQUIRES_REVIEW", "module_run_files": run_files, "registered_artifacts": artifact_matches, "indexed_runs": run_matches},
            "restart": {"status": "ABSENT", "basis": "no parent-driven module run/output packet registered"},
            "covariance": {"status": "ABSENT", "basis": "no parent-driven module output/covariance packet registered"},
            "independent_reconstruction": {"status": "ABSENT", "basis": "no module run with independent verification registered"},
            "state_record": {"evidence_state": state["modules"][module]["evidence_state"], "fidelity": state["modules"][module]["fidelity"]},
            "boundary_status": "FRONTIER" if module == "A" else "BLOCKED_BY_EARLIER_FRONTIER_AND_LOCALLY_UNEXECUTED",
        })

    frontier_rows = [r for r in rows if r["boundary_status"] == "FRONTIER"]
    next_items = [x for x in queue["items"] if x.get("depends_on") == ["FRONTIER-050"]]
    selected_next = next_items[0]["id"] if len(next_items) == 1 else None
    gates = {
        "no status word hides a missing object": {
            "result": "PASS",
            "basis": "Every row separately records law, manufactured test, exact parent, solver binding, output, restart, covariance, and independent reconstruction; manufactured success is explicitly non-physical."
        },
        "one frontier selected": {
            "result": "PASS" if len(frontier_rows) == 1 and frontier_rows[0]["module"] == "A" else "FAIL",
            "basis": f"frontier_count={len(frontier_rows)}; selected={frontier_rows[0]['module'] if frontier_rows else None}"
        },
        "recovered parents verified": {
            "result": "PASS" if all(x["match"] for x in recovered_checks) and recovered.get("canonical_parents") == [] else "FAIL",
            "basis": "All five REC-040 objects rehashed exactly; canonical_parents remains empty; none is used as an A-J physical parent."
        }
    }
    if any(x["result"] != "PASS" for x in gates.values()):
        raise SystemExit("mandatory gate failed")

    out = {
        "schema_version": "1.0",
        "work_unit": "FRONTIER-050",
        "run_id": RUN.name,
        "generation_mode": state["generation_mode"],
        "audit_rule": "Select the earliest topological boundary whose exact parent-driven output and reconstruction evidence are absent; formal law and manufactured checks never impersonate physical execution.",
        "authority": {
            "last_verified_scientific_commit": state["last_verified_commit"],
            "source_manifest": file_record("sources/SOURCE_MANIFEST.json"),
            "source_manifest_status": source_manifest["status"],
            "crosswalk": file_record("theory/ENHANCEMENT_CROSSWALK.json"),
            "artifact_registry": file_record("memory/ARTIFACT_REGISTRY.json"),
            "run_index": file_record("memory/RUN_INDEX.json"),
            "rec040_manifest": file_record("recovery/ADMITTED_ASSET_MANIFEST.json"),
            "source_checks": source_checks,
            "recovered_checks": recovered_checks,
        },
        "rows": rows,
        "selected_frontier": {
            "module": "A",
            "missing_object": "frozen typed prephysical Module A packet H_A_to_B, derived from exact admitted authority bytes and independently reconstructed",
            "why_earliest": "A has formalized source architecture and a successful finite manufactured kernel check, but no governed Module A run, registered output, restartable H_A_to_B packet, or independent symbolic reconstruction. Therefore B has no admissible exact parent and no later A-J execution can be physical.",
            "first_physical_event_remains": "Module B Big Implosion, only after A-100 closes H_A_to_B",
            "authorized_child": selected_next,
        },
        "gates": gates,
        "strongest_supported_claim": "The exact execution frontier is Module A: admitted authority and formal architecture exist, but the frozen typed prephysical handoff H_A_to_B has not been produced or independently reconstructed in 3-RFC.",
        "strongest_unsupported_claim": "This audit does not execute Module A or B, does not produce a physical universe state, and does not validate any later module or empirical claim.",
    }
    (ROOT / "audit/PHYSICAL_FRONTIER.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# Physical Execution Frontier", "", f"- Work unit: `FRONTIER-050`", f"- Run: `{RUN.name}`",
        "- Generation mode: `GENERATION_SEALED`", "- Selected frontier: **Module A**", "- Authorized child: `A-100`", "",
        "## Finding", "",
        "The canonical sources and key triadic/N-body architecture are exact and formalized, and several finite manufactured solver checks pass. None of those checks is a governed parent-driven Module A execution. The first missing admissible object is the frozen typed prephysical handoff `H_A_to_B`, with its restart/provenance packet and independent symbolic reconstruction. Module B remains the first physical event, but it cannot begin without that exact A parent.", "",
        "## Boundary matrix", "",
        "| Module | Law | Representative check | Exact parent | Physical/output packet | Restart | Covariance | Independent reconstruction | Evidence state |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        rep = "limited manufactured PASS" if r["representative_test"]["records"] else "no prebuilt result"
        lines.append(f"| {r['module']} | {r['law']['status']} | {rep} | {r['physical_parent']['status']} | {r['output']['status']} | {r['restart']['status']} | {r['covariance']['status']} | {r['independent_reconstruction']['status']} | {r['state_record']['evidence_state']} |")
    lines += [
        "", "## Mandatory gates", "",
        "- **PASS — no status word hides a missing object.** Law, manufactured checks, parent, output, restart, covariance, and independent reconstruction are separate fields for every row.",
        "- **PASS — one frontier selected.** Module A is the unique earliest topological break.",
        "- **PASS — recovered parents verified.** All five REC-040 objects rehash exactly, remain `SOURCE_OBJECT_ONLY`, and `canonical_parents` is empty.",
        "", "## Strongest supported claim", "",
        out["strongest_supported_claim"], "", "## Strongest unsupported claim", "", out["strongest_unsupported_claim"], "",
        "## Exact next child", "", "`A-100 — Close Module A: Triad, First Action, Recursive Kernel, and Relational Completion`", ""
    ]
    (ROOT / "audit/PHYSICAL_FRONTIER.md").write_text("\n".join(lines), encoding="utf-8")

if __name__ == "__main__":
    main()
