#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "STATE.json"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def patch_once(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text(encoding="utf-8")
    if new in text:
        return
    if old not in text:
        raise SystemExit(f"HARD STOP: patch anchor missing for {label}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def patch_rfc() -> None:
    """Install the higher-fidelity output-contract and reopen controls used by the B-first replay."""
    p = ROOT / "tools/rfc.py"

    old = '''    for name in [\n        "RUN_PLAN.md", "SOURCE_REGISTER.json", "PRE_EXECUTION_LOCK.json", "ENVIRONMENT.json",\n        "CHECKPOINT_RECORD.json", "GENERATED_OUTPUT_MANIFEST.json", "OUTPUT_COMPLETENESS.json", "REPLAY_RECORD.json",\n        "GATE_RESULTS.json", "INDEPENDENT_VERIFICATION.md", "CLOSEOUT.md"\n    ]:\n        copy_template(name, dest / name)\n    (dest / "FAILURES.jsonl").write_text("", encoding="utf-8")\n'''
    new = '''    for name in [\n        "RUN_PLAN.md", "SOURCE_REGISTER.json", "PRE_EXECUTION_LOCK.json", "ENVIRONMENT.json",\n        "CHECKPOINT_RECORD.json", "GENERATED_OUTPUT_MANIFEST.json", "OUTPUT_COMPLETENESS.json", "REPLAY_RECORD.json",\n        "GATE_RESULTS.json", "INDEPENDENT_VERIFICATION.md", "CLOSEOUT.md"\n    ]:\n        copy_template(name, dest / name)\n    if args.module in load_json(ROOT / "config/module_graph.json")["module_order"]:\n        spec = load_json(ROOT / "modules" / args.module / "spec.json")\n        save_json(dest / "OUTPUT_CONTRACT.json", {\n            "schema_version": "1.0", "run_id": run_id, "module": args.module, "status": "DRAFT",\n            "required_outputs": [{"name": name, "status": "UNSATISFIED", "artifact_paths": [], "semantic_gate": "PENDING", "independent_verification": "PENDING", "child_ready": False} for name in spec.get("required_outputs", [])],\n            "child_bindings": {},\n            "note": "PASS requires every live module-spec output and configured child binding to be artifact-backed, semantically verified, independently verified, and child-ready."\n        })\n    (dest / "FAILURES.jsonl").write_text("", encoding="utf-8")\n'''
    patch_once(p, old, new, "new-run OUTPUT_CONTRACT")

    marker = '''def cmd_close_run(args: argparse.Namespace) -> int:\n'''
    helper = '''def validate_required_output_contract(path: Path, module: str) -> tuple[bool, list[str]]:\n    errors: list[str] = []\n    contract_path = path / "OUTPUT_CONTRACT.json"\n    if not contract_path.exists():\n        return False, ["OUTPUT_CONTRACT.json is missing"]\n    spec = load_json(ROOT / "modules" / module / "spec.json")\n    contract = load_json(contract_path)\n    if contract.get("status") != "PASS":\n        errors.append("OUTPUT_CONTRACT.json status must be PASS")\n    required = list(spec.get("required_outputs", []))\n    records = contract.get("required_outputs", [])\n    by_name = {r.get("name"): r for r in records if isinstance(r, dict) and r.get("name")}\n    if set(by_name) != set(required):\n        errors.append(f"output-contract names differ from live module spec: expected {required}, found {sorted(by_name)}")\n    for name in required:\n        rec = by_name.get(name)\n        if not rec:\n            continue\n        if rec.get("status") != "SATISFIED": errors.append(f"required output not SATISFIED: {name}")\n        if rec.get("semantic_gate") != "PASS": errors.append(f"required output semantic gate not PASS: {name}")\n        if rec.get("independent_verification") != "PASS": errors.append(f"required output independent verification not PASS: {name}")\n        if rec.get("child_ready") is not True: errors.append(f"required output not child-ready: {name}")\n        arts = rec.get("artifact_paths", [])\n        if not arts: errors.append(f"required output has no artifact evidence: {name}")\n        for rel in arts:\n            q = (ROOT / rel).resolve()\n            if not q.exists() or ROOT not in q.parents:\n                errors.append(f"required-output artifact missing/outside repository: {name}: {rel}")\n    cfg_path = ROOT / "config/required_output_contracts.json"\n    cfg = load_json(cfg_path) if cfg_path.exists() else {}\n    bindings = contract.get("child_bindings", {})\n    for req in cfg.get("modules", {}).get(module, {}).get("required_child_bindings", []):\n        key = req["name"]\n        rec = bindings.get(key)\n        if not isinstance(rec, dict):\n            errors.append(f"required child binding missing: {key}")\n            continue\n        if rec.get("status") != "SATISFIED": errors.append(f"required child binding not SATISFIED: {key}")\n        if rec.get("source_lineage") != "PASS": errors.append(f"required child binding source lineage not PASS: {key}")\n        if rec.get("independent_verification") != "PASS": errors.append(f"required child binding independent verification not PASS: {key}")\n        if not rec.get("artifact_paths"): errors.append(f"required child binding has no artifact evidence: {key}")\n        if not req.get("allow_derived_absence", False) and rec.get("derived_absence") is True:\n            errors.append(f"required child binding cannot be satisfied by absence: {key}")\n        if req.get("allow_derived_absence", False) and rec.get("derived_absence") is True and not rec.get("absence_proof_artifact"):\n            errors.append(f"derived absence lacks proof artifact: {key}")\n    return not errors, errors\n\n\n'''
    patch_once(p, marker, helper + marker, "required-output validator")

    old = '''        run_module = load_json(path / "run.json").get("module")\n        if run_module in set(load_json(ROOT / "config/module_graph.json")["module_order"]) | {"UNIVERSE", "FINAL"}:\n'''
    new = '''        run_module = load_json(path / "run.json").get("module")\n        module_order = set(load_json(ROOT / "config/module_graph.json")["module_order"])\n        if run_module in module_order:\n            output_ok, output_errors = validate_required_output_contract(path, run_module)\n            if not output_ok:\n                print("PASS requires a complete live required-output and child-readiness contract", file=sys.stderr)\n                for err in output_errors: print(f"- {err}", file=sys.stderr)\n                return 2\n        if run_module in module_order | {"UNIVERSE", "FINAL"}:\n'''
    patch_once(p, old, new, "close-run OUTPUT_CONTRACT enforcement")

    marker = '''def cmd_record_claim(args: argparse.Namespace) -> int:\n'''
    reopen = '''def cmd_reopen_module(args: argparse.Namespace) -> int:\n    state = load_json(STATE_PATH)\n    if args.module not in state.get("modules", {}):\n        print("unknown module", file=sys.stderr); return 2\n    item = active_item()\n    if item.get("module") != args.module:\n        print(f"active work unit {item.get('id')} does not authorize reopening {args.module}", file=sys.stderr); return 2\n    rec = state["modules"][args.module]\n    current = rec.get("evidence_state"); current_fidelity = rec.get("fidelity")\n    if current not in {"FROZEN", "BLOCKED"}:\n        print("only FROZEN/BLOCKED modules may be reopened", file=sys.stderr); return 2\n    if args.fidelity not in FIDELITY_ORDER or current_fidelity not in FIDELITY_ORDER:\n        print("invalid fidelity", file=sys.stderr); return 2\n    if current == "FROZEN" and FIDELITY_ORDER.index(args.fidelity) <= FIDELITY_ORDER.index(current_fidelity):\n        print("reopening a frozen module requires strictly higher fidelity", file=sys.stderr); return 2\n    evidence = (ROOT / args.evidence).resolve()\n    if not evidence.exists() or ROOT not in evidence.parents:\n        print("reopen evidence must exist inside repository", file=sys.stderr); return 2\n    previous = {"evidence_state": current, "fidelity": current_fidelity}\n    rec["evidence_state"] = "DESIGN"; rec["fidelity"] = args.fidelity; rec["active_run"] = None\n    rec["reopened_from"] = previous; rec["reopen_evidence"] = str(evidence.relative_to(ROOT))\n    rec.setdefault("evidence_history", []).append({"state": "DESIGN", "fidelity": args.fidelity, "evidence": str(evidence.relative_to(ROOT)), "timestamp_utc": now(), "work_unit": item["id"], "reopened_from": previous})\n    state["last_updated_utc"] = now(); save_json(STATE_PATH, state)\n    decision = {"decision_id": f"REOPEN-{args.module}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}", "timestamp_utc": now(), "work_unit": item["id"], "decision": f"Reopened Module {args.module} from {current}/{current_fidelity} at target fidelity {args.fidelity} for the authorized superseding lineage.", "basis": [str(evidence.relative_to(ROOT))], "alternatives_rejected": ["overwrite prior frozen evidence", "fabricate missing child bindings downstream"], "changes_science": False, "required_replay": item["id"], "commit_sha": state.get("last_verified_commit") or ""}\n    with (ROOT / "memory/DECISION_LOG.jsonl").open("a", encoding="utf-8") as f:\n        f.write(json.dumps(decision, ensure_ascii=False) + "\\n")\n    print(json.dumps(decision, indent=2)); return 0\n\n\n'''
    patch_once(p, marker, reopen + marker, "reopen-module command")

    old = '''    sp = sub.add_parser("close-run")\n'''
    new = '''    sp = sub.add_parser("reopen-module")\n    sp.add_argument("module")\n    sp.add_argument("--fidelity", required=True)\n    sp.add_argument("--evidence", required=True)\n    sp.set_defaults(func=cmd_reopen_module)\n\n    sp = sub.add_parser("close-run")\n'''
    patch_once(p, old, new, "reopen-module parser")


if __name__ == "__main__":
    patch_rfc()
