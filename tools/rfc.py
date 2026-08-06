#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "STATE.json"
QUEUE_PATH = ROOT / "WORK_QUEUE.json"

EVIDENCE_ORDER = [
    "DESIGN", "FORMALIZED", "IMPLEMENTED", "VERIFIED", "PHYSICALLY_EXECUTED",
    "ENSEMBLE_VERIFIED", "INDEPENDENTLY_REPRODUCED", "FROZEN", "BLIND_VALIDATED", "PREDICTIVE_LOCK"
]
VALID_EXTRA_STATES = {"BLOCKED", "FAIL_REQUIRES_ANALYSIS", "FALSIFIED_AT_SCOPE"}
FIDELITY_ORDER = ["UNSTARTED", "TOY", "MANUFACTURED", "REPRESENTATIVE", "MINIMAL_SPINE", "PRODUCTION", "HYPER_REALISTIC", "GOLD_STANDARD"]
EVIDENCE_TRANSITIONS = {
    "DESIGN": {"FORMALIZED"},
    "FORMALIZED": {"IMPLEMENTED", "VERIFIED"},
    "IMPLEMENTED": {"VERIFIED"},
    "VERIFIED": {"PHYSICALLY_EXECUTED", "INDEPENDENTLY_REPRODUCED", "FROZEN"},
    "PHYSICALLY_EXECUTED": {"ENSEMBLE_VERIFIED", "INDEPENDENTLY_REPRODUCED", "FROZEN"},
    "ENSEMBLE_VERIFIED": {"INDEPENDENTLY_REPRODUCED", "FROZEN"},
    "INDEPENDENTLY_REPRODUCED": {"FROZEN"},
    "FROZEN": {"FROZEN", "BLIND_VALIDATED", "PREDICTIVE_LOCK"},
    "BLIND_VALIDATED": {"BLIND_VALIDATED", "PREDICTIVE_LOCK"},
    "PREDICTIVE_LOCK": {"PREDICTIVE_LOCK"}
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def tree_entries(path: Path) -> list[dict[str, Any]]:
    if path.is_file():
        return [{"path": str(path.relative_to(ROOT)), "sha256": sha256_file(path), "bytes": path.stat().st_size}]
    entries = []
    for p in sorted(path.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT)
        if any(part in {".git", "__pycache__", "runtime_cache", "scratch"} for part in rel.parts):
            continue
        entries.append({"path": str(rel), "sha256": sha256_file(p), "bytes": p.stat().st_size})
    return entries


def sha256_tree(path: Path) -> str:
    h = hashlib.sha256()
    for item in tree_entries(path):
        h.update(item["path"].encode())
        h.update(b"\0")
        h.update(item["sha256"].encode())
        h.update(b"\n")
    return h.hexdigest()


def active_item() -> dict[str, Any]:
    state = load_json(STATE_PATH)
    if state.get("active_work_unit") == "COMPLETE":
        return {"id": "COMPLETE", "title": "Work queue complete", "module": "FINAL", "objective": "All queued work units have passed.", "steps": [], "deliverables": [], "gates": [], "commit_message": ""}
    queue = load_json(QUEUE_PATH)["items"]
    matches = [x for x in queue if x["id"] == state["active_work_unit"]]
    if len(matches) != 1:
        raise RuntimeError("STATE active_work_unit does not resolve to exactly one queue item")
    return matches[0]


def validate_repository() -> list[str]:
    errors: list[str] = []
    required = [
        "README.md", "AGENTS.md", "STATE.json", "WORK_QUEUE.json", "CLAIMS_LEDGER.json",
        "config/project.json", "config/module_graph.json", "config/module_evidence_requirements.json", "tools/rfc.py", "memory/CURRENT_CONTEXT.md"
    ]
    for rel in required:
        if not (ROOT / rel).exists():
            errors.append(f"missing required file: {rel}")

    try:
        state = load_json(STATE_PATH)
        queue_doc = load_json(QUEUE_PATH)
        graph = load_json(ROOT / "config/module_graph.json")
        project = load_json(ROOT / "config/project.json")
    except Exception as exc:
        return errors + [f"JSON load failure: {exc}"]

    if project.get("canonical_terms") != {
        "CIF": "Cosmic Infinite Field", "QV": "Quantum Vacuum", "RFL": "Recursive Fractal Lattice", "first_action": "QV(CIF) -> RFL"
    }:
        errors.append("canonical terminology drift in config/project.json")

    items = queue_doc.get("items", [])
    active = [x for x in items if x.get("status") == "ACTIVE"]
    if state.get("active_work_unit") == "COMPLETE":
        if active:
            errors.append("queue is COMPLETE but still has an ACTIVE item")
        if any(x.get("status") != "PASS" for x in items):
            errors.append("queue is COMPLETE but not every item is PASS")
    else:
        if len(active) != 1:
            errors.append(f"queue must have exactly one ACTIVE item, found {len(active)}")
        elif active[0].get("id") != state.get("active_work_unit"):
            errors.append("queue ACTIVE item does not match STATE active_work_unit")

    ids = {x.get("id") for x in items}
    if len(ids) != len(items):
        errors.append("duplicate work-unit IDs")
    for item in items:
        for dep in item.get("depends_on", []):
            if dep not in ids:
                errors.append(f"unknown dependency {dep} for {item.get('id')}")
    dep_map = {x.get("id"): set(x.get("depends_on", [])) for x in items}
    expected_dependencies = {
        "HI-190": {"HU-170", "I-180"},
        "HR-255": {"N-250"},
        "O-260": {"HR-255"},
        "P-270": {"O-260"},
        "Q-280": {"O-260"},
        "FINAL-290": {"P-270", "Q-280"}
    }
    for task_id, deps in expected_dependencies.items():
        if dep_map.get(task_id) != deps:
            errors.append(f"protected dependency drift for {task_id}: {dep_map.get(task_id)}")

    module_order = graph.get("module_order", [])
    if set(module_order) != set(state.get("modules", {})):
        errors.append("STATE module set differs from module_graph")
    for mod, status in state.get("modules", {}).items():
        ev = status.get("evidence_state")
        if ev not in EVIDENCE_ORDER and ev not in VALID_EXTRA_STATES:
            errors.append(f"invalid evidence state {ev} for module {mod}")
        history = status.get("evidence_history", [])
        if not history or history[0].get("state") != "DESIGN" or history[-1].get("state") != ev:
            errors.append(f"invalid evidence history for module {mod}")
        if not (ROOT / "modules" / mod / "spec.json").exists():
            errors.append(f"missing module spec: {mod}")

    if state.get("generation_mode") == "PUBLIC_COMPARISON_OPEN" and not state.get("frozen_universe_hash"):
        errors.append("public comparison cannot open without frozen universe hash")
    if state.get("public_comparison_open") and state.get("generation_mode") != "PUBLIC_COMPARISON_OPEN":
        errors.append("public_comparison_open inconsistent with generation_mode")

    # Verify registered sources and artifacts.
    for reg_path, key in [(ROOT / "memory/SOURCE_REGISTRY.json", "sources"), (ROOT / "memory/ARTIFACT_REGISTRY.json", "artifacts")]:
        try:
            reg = load_json(reg_path)
            for rec in reg.get(key, []):
                p = ROOT / rec.get("frozen_path", rec.get("path", ""))
                if not p.exists():
                    errors.append(f"registered object missing: {p.relative_to(ROOT) if p.is_absolute() else p}")
                elif p.is_file() and sha256_file(p) != rec.get("sha256"):
                    errors.append(f"registered hash mismatch: {p.relative_to(ROOT)}")
                elif p.is_dir() and sha256_tree(p) != rec.get("sha256"):
                    errors.append(f"registered tree hash mismatch: {p.relative_to(ROOT)}")
        except Exception as exc:
            errors.append(f"registry validation failure {reg_path.name}: {exc}")

    # Claim evidence must be recognized.
    try:
        claims = load_json(ROOT / "CLAIMS_LEDGER.json").get("claims", [])
        for claim in claims:
            ev = claim.get("evidence_state")
            if ev not in EVIDENCE_ORDER and ev not in VALID_EXTRA_STATES:
                errors.append(f"claim {claim.get('claim_id')} has invalid evidence state {ev}")
    except Exception as exc:
        errors.append(f"claims ledger failure: {exc}")

    return errors


def cmd_doctor(_: argparse.Namespace) -> int:
    errors = validate_repository()
    if errors:
        print("3-RFC DOCTOR: FAIL")
        for e in errors:
            print(f"- {e}")
        return 1
    print("3-RFC DOCTOR: PASS")
    state = load_json(STATE_PATH)
    print(f"Active work unit: {state['active_work_unit']}")
    print(f"Generation mode: {state['generation_mode']}")
    return 0


def cmd_status(_: argparse.Namespace) -> int:
    state = load_json(STATE_PATH)
    item = active_item()
    print(json.dumps({
        "project_status": state["project_status"], "active_work_unit": item["id"], "title": item["title"],
        "module": item["module"], "generation_mode": state["generation_mode"],
        "strongest_supported_claim": state["strongest_supported_claim"],
        "strongest_unsupported_claim": state["strongest_unsupported_claim"],
        "last_verified_commit": state.get("last_verified_commit")
    }, indent=2))
    return 0


def cmd_next(_: argparse.Namespace) -> int:
    item = active_item()
    print(f"ACTIVE: {item['id']} — {item['title']}")
    print(f"MODULE: {item['module']}")
    print(f"OBJECTIVE: {item['objective']}")
    print("\nSTEPS:")
    for i, x in enumerate(item.get("steps", []), 1):
        print(f"  {i}. {x}")
    print("\nDELIVERABLES:")
    for x in item.get("deliverables", []):
        print(f"  - {x}")
    print("\nMANDATORY GATES:")
    for x in item.get("gates", []):
        print(f"  - {x}")
    print(f"\nCOMMIT MESSAGE: {item.get('commit_message', '')}")
    return 0


def read_jsonl(path: Path, limit: int = 8) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            rows.append({"raw": line})
    return rows[-limit:]


def cmd_context(_: argparse.Namespace) -> int:
    state = load_json(STATE_PATH)
    item = active_item()
    runs = load_json(ROOT / "memory/RUN_INDEX.json").get("runs", [])[-8:]
    decisions = read_jsonl(ROOT / "memory/DECISION_LOG.jsonl")
    failures = read_jsonl(ROOT / "memory/FAILURE_LOG.jsonl")
    sources = load_json(ROOT / "memory/SOURCE_REGISTRY.json").get("sources", [])
    artifacts = load_json(ROOT / "memory/ARTIFACT_REGISTRY.json").get("artifacts", [])

    lines = [
        "# Current Context", "", f"Generated: {now()}", "", "## Project truth", "",
        f"- Status: `{state['project_status']}`", f"- Generation mode: `{state['generation_mode']}`",
        f"- Active work unit: `{item['id']}` — {item['title']}", f"- Current module: `{item['module']}`",
        f"- Last verified commit: `{state.get('last_verified_commit')}`", "",
        "## Strongest supported claim", "", state["strongest_supported_claim"], "",
        "## Strongest unsupported claim", "", state["strongest_unsupported_claim"], "",
        "## Immediate objective", "", item["objective"], "", "## Required deliverables", ""
    ]
    lines += [f"- {x}" for x in item.get("deliverables", [])]
    lines += ["", "## Mandatory gates", ""] + [f"- {x}" for x in item.get("gates", [])]
    lines += ["", "## Module states", ""]
    for m, rec in state["modules"].items():
        lines.append(f"- {m}: `{rec['evidence_state']}` / `{rec['fidelity']}`")
    lines += ["", f"## Memory counts", "", f"- admitted sources: {len(sources)}", f"- frozen artifacts: {len(artifacts)}", f"- indexed runs: {len(load_json(ROOT / 'memory/RUN_INDEX.json').get('runs', []))}"]
    if runs:
        lines += ["", "## Recent runs", ""] + [f"- {r.get('run_id')}: {r.get('status')} ({r.get('module')})" for r in runs]
    if decisions:
        lines += ["", "## Recent decisions", ""] + [f"- {d.get('decision_id', '')}: {d.get('decision', d.get('raw', ''))}" for d in decisions]
    if failures:
        lines += ["", "## Recent failures", ""] + [f"- {f.get('failure_id', '')}: {f.get('description', f.get('raw', ''))}" for f in failures]
    lines += ["", "## Resume commands", "", "```bash", "python tools/rfc.py doctor", "python tools/rfc.py next", "```", ""]
    out = ROOT / "memory/CURRENT_CONTEXT.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(out.relative_to(ROOT))
    return 0


def copy_template(name: str, dest: Path) -> None:
    shutil.copy2(ROOT / "templates" / name, dest)


def cmd_new_run(args: argparse.Namespace) -> int:
    state = load_json(STATE_PATH)
    if state.get("current_run"):
        print(f"an active run already exists: {state['current_run']}", file=sys.stderr)
        return 2
    item = active_item()
    if item["module"] not in {args.module, "REPO", "SOURCES", "THEORY", "RECOVERY", "AUDIT", "FINAL"}:
        print(f"active work unit belongs to {item['module']}; requested {args.module}", file=sys.stderr)
        return 2
    run_id = args.run_id or f"{item['id']}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    if args.module in load_json(ROOT / "config/module_graph.json")["module_order"]:
        dest = ROOT / "modules" / args.module / "runs" / run_id
    else:
        dest = ROOT / "runs" / run_id
    if dest.exists():
        print(f"run already exists: {dest.relative_to(ROOT)}", file=sys.stderr)
        return 2
    dest.mkdir(parents=True)
    for name in [
        "RUN_PLAN.md", "SOURCE_REGISTER.json", "PRE_EXECUTION_LOCK.json", "ENVIRONMENT.json",
        "CHECKPOINT_RECORD.json", "GENERATED_OUTPUT_MANIFEST.json", "REPLAY_RECORD.json",
        "GATE_RESULTS.json", "INDEPENDENT_VERIFICATION.md", "CLOSEOUT.md"
    ]:
        copy_template(name, dest / name)
    (dest / "FAILURES.jsonl").write_text("", encoding="utf-8")
    save_json(dest / "run.json", {
        "run_id": run_id, "module": args.module, "task_id": item["id"], "status": "CREATED", "created_utc": now(),
        "parent_hashes": [], "generation_mode": load_json(STATE_PATH)["generation_mode"], "workspace": str(dest.relative_to(ROOT))
    })
    idx = load_json(ROOT / "memory/RUN_INDEX.json")
    idx["runs"].append({"run_id": run_id, "module": args.module, "task_id": item["id"], "status": "CREATED", "path": str(dest.relative_to(ROOT)), "created_utc": now()})
    save_json(ROOT / "memory/RUN_INDEX.json", idx)
    state = load_json(STATE_PATH)
    state["current_run"] = run_id
    if args.module in state["modules"]:
        state["modules"][args.module]["active_run"] = run_id
    state["last_updated_utc"] = now()
    save_json(STATE_PATH, state)
    print(dest.relative_to(ROOT))
    return 0


def cmd_admit_source(args: argparse.Namespace) -> int:
    src = Path(args.path).resolve()
    if not src.exists() or not src.is_file():
        print("source file not found", file=sys.stderr)
        return 2
    digest = sha256_file(src)
    dest_dir = ROOT / "sources/frozen" / digest
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    if not dest.exists():
        shutil.copy2(src, dest)
    record = {
        "label": args.label or src.name, "sha256": digest, "bytes": src.stat().st_size,
        "classification": args.classification, "origin": str(src), "frozen_path": str(dest.relative_to(ROOT)),
        "admitted_utc": now(), "admitted_by_work_unit": load_json(STATE_PATH)["active_work_unit"]
    }
    reg = load_json(ROOT / "memory/SOURCE_REGISTRY.json")
    if not any(x.get("sha256") == digest and x.get("label") == record["label"] for x in reg["sources"]):
        reg["sources"].append(record)
        save_json(ROOT / "memory/SOURCE_REGISTRY.json", reg)
    manifest = load_json(ROOT / "sources/SOURCE_MANIFEST.json")
    manifest["status"] = "IN_PROGRESS"
    if not any(x.get("sha256") == digest for x in manifest["sources"]):
        manifest["sources"].append(record)
    save_json(ROOT / "sources/SOURCE_MANIFEST.json", manifest)
    print(json.dumps(record, indent=2))
    return 0


def cmd_freeze(args: argparse.Namespace) -> int:
    p = (ROOT / args.path).resolve() if not Path(args.path).is_absolute() else Path(args.path).resolve()
    if not p.exists() or ROOT not in p.parents and p != ROOT:
        print("path must exist inside repository", file=sys.stderr)
        return 2
    digest = sha256_file(p) if p.is_file() else sha256_tree(p)
    rec = {"path": str(p.relative_to(ROOT)), "sha256": digest, "kind": args.kind, "created_utc": now(), "work_unit": load_json(STATE_PATH)["active_work_unit"]}
    reg = load_json(ROOT / "memory/ARTIFACT_REGISTRY.json")
    if not any(x.get("path") == rec["path"] and x.get("sha256") == digest for x in reg["artifacts"]):
        reg["artifacts"].append(rec)
        save_json(ROOT / "memory/ARTIFACT_REGISTRY.json", reg)
    print(json.dumps(rec, indent=2))
    return 0


def cmd_hash_tree(args: argparse.Namespace) -> int:
    p = (ROOT / args.path).resolve()
    entries = tree_entries(p)
    obj = {"root": str(p.relative_to(ROOT)), "sha256": sha256_tree(p), "created_utc": now(), "entries": entries}
    out = ROOT / args.output if args.output else None
    if out:
        save_json(out, obj)
        print(out.relative_to(ROOT))
    else:
        print(json.dumps(obj, indent=2))
    return 0


def cmd_firewall_scan(_: argparse.Namespace) -> int:
    roots = [ROOT / "runs", ROOT / "modules", ROOT / "generation", ROOT / "proofs", ROOT / "universes"]
    url_re = re.compile(r"https?://", re.I)
    suspicious = re.compile(r"(planck|desi|pantheon|sh0es|best[-_ ]?fit|posterior|likelihood|public[_ -]?data)", re.I)
    allowed_docs = {
        "README.md", "spec.json", "WORK_ORDER.md", "RUN_PLAN.md",
        "FROZEN_WORK_UNIT_RECIPE.json", "FROZEN_RECIPE.json", "REQUIRED_GATES.json",
        "WOLFRAM_SEQUENCE.md", "MODEL_PROMPT.md", "WORK_MODEL_PROMPT.md",
    }
    findings = []
    for base in roots:
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if not p.is_file() or any(x in p.parts for x in ["runtime_cache", "scratch"]):
                continue
            # Protocol/spec prose may mention forbidden concepts; executable/source registers are the important scan targets.
            if p.name in allowed_docs or "templates" in p.parts:
                continue
            if p.suffix.lower() not in {".py", ".json", ".yaml", ".yml", ".toml", ".txt", ".csv", ".md", ".wl"}:
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if url_re.search(text) or suspicious.search(text):
                findings.append(str(p.relative_to(ROOT)))
    declarations = load_json(ROOT / "generation/PUBLIC_DATA_DECLARATIONS.json").get("declared_public_inputs", [])
    if findings and not declarations:
        print("FIREWALL SCAN: REVIEW REQUIRED")
        for f in sorted(set(findings)):
            print(f"- {f}")
        print("This mechanical scan is not proof of contamination. Review and document each finding.")
        return 1
    print("FIREWALL SCAN: PASS (mechanical guardrail only)")
    return 0


def cmd_advance(args: argparse.Namespace) -> int:
    state = load_json(STATE_PATH)
    queue_doc = load_json(QUEUE_PATH)
    items = queue_doc["items"]
    current = next((x for x in items if x["id"] == state["active_work_unit"]), None)
    if not current or current["id"] != args.task:
        print("task is not the active work unit", file=sys.stderr)
        return 2
    evidence = (ROOT / args.evidence).resolve()
    if not evidence.exists() or ROOT not in evidence.parents:
        print("evidence file must exist inside repository", file=sys.stderr)
        return 2

    if args.result == "PASS":
        text = evidence.read_text(encoding="utf-8", errors="ignore") if evidence.is_file() else ""
        if len(text.strip()) < 120:
            print("PASS evidence is too short to be a completed closeout", file=sys.stderr)
            return 2
        if "Complete only after" in text or "Complete only" in text:
            print("PASS evidence still contains an incomplete placeholder", file=sys.stderr)
            return 2
        if current["id"] == "BOOT-000":
            sha = state.get("last_verified_commit")
            if not sha or sha not in text:
                print("BOOT-000 closeout must contain the recorded verified commit SHA", file=sys.stderr)
                return 2
        elif current["module"] in load_json(ROOT / "config/module_graph.json")["module_order"]:
            required_markers = ["Strongest supported claim", "Strongest unsupported claim", "Result"]
            missing = [m for m in required_markers if m not in text]
            if missing:
                print(f"module closeout missing markers: {missing}", file=sys.stderr)
                return 2

    if args.result == "PASS":
        module_order = load_json(ROOT / "config/module_graph.json")["module_order"]
        run_index = load_json(ROOT / "memory/RUN_INDEX.json").get("runs", [])
        if current["module"] in module_order:
            mod = current["module"]
            if state.get("current_run"):
                print("close the active run before advancing the module", file=sys.stderr)
                return 2
            passed_runs = [r for r in run_index if r.get("module") == mod and r.get("task_id") == current["id"] and r.get("status") == "PASS"]
            if not passed_runs:
                print("module advance requires at least one closed PASS run for the active work unit", file=sys.stderr)
                return 2
            rec = state["modules"][mod]
            required_state = current.get("required_evidence_state")
            required_fidelity = current.get("required_fidelity")
            if required_state and (rec.get("evidence_state") not in EVIDENCE_ORDER or EVIDENCE_ORDER.index(rec["evidence_state"]) < EVIDENCE_ORDER.index(required_state)):
                print(f"Module {mod} must reach {required_state} before advance", file=sys.stderr)
                return 2
            if required_fidelity and (rec.get("fidelity") not in FIDELITY_ORDER or FIDELITY_ORDER.index(rec["fidelity"]) < FIDELITY_ORDER.index(required_fidelity)):
                print(f"Module {mod} must reach fidelity {required_fidelity} before advance", file=sys.stderr)
                return 2
            req_path = ROOT / "config/module_evidence_requirements.json"
            if req_path.exists():
                req = load_json(req_path).get("modules", {}).get(mod, {})
                visited = {h.get("state") for h in rec.get("evidence_history", [])}
                missing_states = [x for x in req.get("must_visit", []) if x not in visited]
                if missing_states:
                    print(f"Module {mod} evidence history is missing required states: {missing_states}", file=sys.stderr)
                    return 2
        elif current["id"] in {"HR-255", "FINAL-290"}:
            if state.get("current_run"):
                print("close the active run before advancing", file=sys.stderr)
                return 2
            passed_runs = [r for r in run_index if r.get("task_id") == current["id"] and r.get("status") == "PASS"]
            if not passed_runs:
                print(f"{current['id']} requires a closed PASS run", file=sys.stderr)
                return 2
            if current["id"] == "HR-255":
                required_modules = [m for m in module_order if m not in {"O", "P", "Q"}]
                for mod in required_modules:
                    rec = state["modules"][mod]
                    if rec.get("evidence_state") not in EVIDENCE_ORDER or EVIDENCE_ORDER.index(rec["evidence_state"]) < EVIDENCE_ORDER.index("FROZEN"):
                        print(f"HR-255 requires Module {mod} FROZEN", file=sys.stderr)
                        return 2
                    if rec.get("fidelity") not in FIDELITY_ORDER or FIDELITY_ORDER.index(rec["fidelity"]) < FIDELITY_ORDER.index("HYPER_REALISTIC"):
                        print(f"HR-255 requires Module {mod} HYPER_REALISTIC", file=sys.stderr)
                        return 2

    if args.result == "FAIL":
        fail = {"failure_id": f"{args.task}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}", "run_id": state.get("current_run"), "gate": "work_unit", "category": "UNCLASSIFIED", "description": args.note or f"{args.task} failed", "earliest_affected_object": args.task, "changes_frozen_science": False, "required_replay_scope": args.task, "strongest_claim_remaining": state["strongest_supported_claim"], "timestamp_utc": now()}
        with (ROOT / "memory/FAILURE_LOG.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(fail, ensure_ascii=False) + "\n")
        current["status"] = "ACTIVE"
        state["project_status"] = "FAIL_REQUIRES_ANALYSIS"
        state["last_updated_utc"] = now()
        save_json(QUEUE_PATH, queue_doc)
        save_json(STATE_PATH, state)
        cmd_context(argparse.Namespace())
        print("failure recorded; task remains active")
        return 0

    # PASS: dependencies must already pass.
    statuses = {x["id"]: x["status"] for x in items}
    unmet = [d for d in current.get("depends_on", []) if statuses.get(d) != "PASS"]
    if unmet:
        print(f"cannot pass; unmet dependencies: {unmet}", file=sys.stderr)
        return 2
    current["status"] = "PASS"
    candidates = [x for x in items if x["status"] == "BLOCKED" and all(statuses.get(d) == "PASS" or d == current["id"] for d in x.get("depends_on", []))]
    # Recompute with current marked pass.
    statuses[current["id"]] = "PASS"
    candidates = [x for x in items if x["status"] == "BLOCKED" and all(statuses.get(d) == "PASS" for d in x.get("depends_on", []))]
    if len(candidates) > 1:
        # Keep queue deterministic by file order; only first becomes active.
        next_item = candidates[0]
    elif candidates:
        next_item = candidates[0]
    else:
        next_item = None
    if next_item:
        next_item["status"] = "ACTIVE"
        state["active_work_unit"] = next_item["id"]
        state["current_module"] = next_item["module"]
        state["project_status"] = "ACTIVE"
    else:
        state["active_work_unit"] = "COMPLETE"
        state["current_module"] = "FINAL"
        state["project_status"] = "QUEUE_COMPLETE"
    state["current_run"] = None
    state["last_updated_utc"] = now()
    decision = {"decision_id": f"ADVANCE-{args.task}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}", "timestamp_utc": now(), "work_unit": args.task, "decision": f"Marked {args.task} PASS and activated {state['active_work_unit']}", "basis": [str(evidence.relative_to(ROOT))], "alternatives_rejected": [], "changes_science": False, "required_replay": "none", "commit_sha": state.get("last_verified_commit") or ""}
    with (ROOT / "memory/DECISION_LOG.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(decision, ensure_ascii=False) + "\n")
    save_json(QUEUE_PATH, queue_doc)
    save_json(STATE_PATH, state)
    cmd_context(argparse.Namespace())
    print(f"advanced to {state['active_work_unit']}")
    return 0


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def cmd_new_proof(args: argparse.Namespace) -> int:
    slug = slugify(args.slug)
    dest = ROOT / "proofs" / slug
    if dest.exists():
        print("proof lane exists", file=sys.stderr)
        return 2
    dest.mkdir(parents=True)
    shutil.copy2(ROOT / "templates/PROOF_PLAN.md", dest / "PROOF_PLAN.md")
    shutil.copy2(ROOT / "templates/SOURCE_REGISTER.json", dest / "SOURCE_REGISTER.json")
    shutil.copy2(ROOT / "templates/GATE_RESULTS.json", dest / "GATE_RESULTS.json")
    shutil.copy2(ROOT / "templates/INDEPENDENT_VERIFICATION.md", dest / "INDEPENDENT_VERIFICATION.md")
    shutil.copy2(ROOT / "templates/CLOSEOUT.md", dest / "CLOSEOUT.md")
    save_json(dest / "proof.json", {"proof_id": slug, "title": args.title, "status": "DESIGN", "canonical_integration": False, "created_utc": now()})
    print(dest.relative_to(ROOT))
    return 0


def cmd_new_universe(args: argparse.Namespace) -> int:
    slug = slugify(args.slug)
    dest = ROOT / "universes" / slug
    if dest.exists():
        print("universe lane exists", file=sys.stderr)
        return 2
    dest.mkdir(parents=True)
    save_json(dest / "STATE.json", {"universe_id": slug, "title": args.title, "status": "DESIGN", "source_universe": None, "generation_mode": "GENERATION_SEALED", "modules": {m: "DESIGN" for m in load_json(ROOT / "config/module_graph.json")["module_order"]}, "created_utc": now()})
    (dest / "README.md").write_text(f"# {args.title}\n\nIsolated universe lane. It is not canonical until an authorized work unit admits it.\n", encoding="utf-8")
    print(dest.relative_to(ROOT))
    return 0



def find_run(run_id: str) -> tuple[dict[str, Any], Path, dict[str, Any]]:
    index = load_json(ROOT / "memory/RUN_INDEX.json")
    matches = [r for r in index.get("runs", []) if r.get("run_id") == run_id]
    if len(matches) != 1:
        raise RuntimeError(f"run {run_id} does not resolve uniquely")
    rec = matches[0]
    path = ROOT / rec["path"]
    return rec, path, index


def cmd_close_run(args: argparse.Namespace) -> int:
    try:
        rec, path, index = find_run(args.run_id)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if not path.exists():
        print("run workspace missing", file=sys.stderr)
        return 2
    closeout = (ROOT / args.closeout).resolve()
    if not closeout.exists() or path not in closeout.parents and closeout != path / "CLOSEOUT.md":
        print("closeout must exist inside the run workspace", file=sys.stderr)
        return 2
    if args.result == "PASS":
        gate_path = path / "GATE_RESULTS.json"
        iv_path = path / "INDEPENDENT_VERIFICATION.md"
        if not gate_path.exists() or load_json(gate_path).get("overall") != "PASS":
            print("PASS requires GATE_RESULTS.json overall PASS", file=sys.stderr)
            return 2
        if not iv_path.exists() or len(iv_path.read_text(encoding="utf-8", errors="ignore").strip()) < 120:
            print("PASS requires substantive independent verification", file=sys.stderr)
            return 2
        run_module = load_json(path / "run.json").get("module")
        if run_module in set(load_json(ROOT / "config/module_graph.json")["module_order"]) | {"UNIVERSE", "FINAL"}:
            pre = load_json(path / "PRE_EXECUTION_LOCK.json")
            env = load_json(path / "ENVIRONMENT.json")
            out_manifest = load_json(path / "GENERATED_OUTPUT_MANIFEST.json")
            replay = load_json(path / "REPLAY_RECORD.json")
            source_register = load_json(path / "SOURCE_REGISTER.json")
            if pre.get("status") != "FROZEN":
                print("PASS requires PRE_EXECUTION_LOCK.json status FROZEN", file=sys.stderr)
                return 2
            if env.get("status") != "FINAL" or not env.get("hidden_defaults_audited"):
                print("PASS requires FINAL environment with hidden defaults audited", file=sys.stderr)
                return 2
            if out_manifest.get("status") != "FINAL" or not out_manifest.get("outputs"):
                print("PASS requires FINAL nonempty generated-output manifest", file=sys.stderr)
                return 2
            if replay.get("result") != "PASS" or not replay.get("clean_checkout") or not replay.get("artifact_hashes_match"):
                print("PASS requires clean replay with matching artifact hashes", file=sys.stderr)
                return 2
            if source_register.get("public_data_declaration") not in {"NONE", "MODULE_P_PUBLIC_COMPARISON"}:
                print("invalid public-data declaration in source register", file=sys.stderr)
                return 2
        text = closeout.read_text(encoding="utf-8", errors="ignore")
        for marker in ["Result", "Strongest supported claim", "Strongest unsupported claim"]:
            if marker not in text:
                print(f"closeout missing marker: {marker}", file=sys.stderr)
                return 2
    run_json_path = path / "run.json"
    run_json = load_json(run_json_path)
    run_json["status"] = args.result
    run_json["closed_utc"] = now()
    run_json["closeout"] = str(closeout.relative_to(ROOT))
    save_json(run_json_path, run_json)
    tree_digest = sha256_tree(path)
    rec.update({"status": args.result, "closed_utc": run_json["closed_utc"], "tree_sha256": tree_digest, "closeout": run_json["closeout"]})
    save_json(ROOT / "memory/RUN_INDEX.json", index)
    artifact = {"path": str(path.relative_to(ROOT)), "sha256": tree_digest, "kind": "RUN_BUNDLE", "created_utc": now(), "work_unit": run_json.get("task_id"), "run_id": args.run_id}
    registry = load_json(ROOT / "memory/ARTIFACT_REGISTRY.json")
    registry["artifacts"] = [x for x in registry.get("artifacts", []) if not (x.get("kind") == "RUN_BUNDLE" and x.get("run_id") == args.run_id)]
    registry["artifacts"].append(artifact)
    save_json(ROOT / "memory/ARTIFACT_REGISTRY.json", registry)
    state = load_json(STATE_PATH)
    if state.get("current_run") == args.run_id:
        state["current_run"] = None
    mod = run_json.get("module")
    if mod in state.get("modules", {}):
        state["modules"][mod]["active_run"] = None
        state["modules"][mod].setdefault("completed_runs", []).append(args.run_id)
    state["last_updated_utc"] = now()
    save_json(STATE_PATH, state)
    print(json.dumps(artifact, indent=2))
    return 0


def cmd_promote_module(args: argparse.Namespace) -> int:
    state = load_json(STATE_PATH)
    if args.module not in state.get("modules", {}):
        print("unknown module", file=sys.stderr)
        return 2
    item = active_item()
    if item["module"] not in {args.module, "UNIVERSE", "FINAL"}:
        print(f"active work unit {item['id']} does not authorize promotion of {args.module}", file=sys.stderr)
        return 2
    if args.to not in EVIDENCE_ORDER:
        print("target must be an ordered evidence state", file=sys.stderr)
        return 2
    evidence = (ROOT / args.evidence).resolve()
    if not evidence.exists() or ROOT not in evidence.parents:
        print("evidence must exist inside repository", file=sys.stderr)
        return 2
    current = state["modules"][args.module]["evidence_state"]
    if current in VALID_EXTRA_STATES:
        print("module is in exception state; resolve it before promotion", file=sys.stderr)
        return 2
    if args.to != current and args.to not in EVIDENCE_TRANSITIONS.get(current, set()):
        print(f"illegal evidence transition {current} -> {args.to}", file=sys.stderr)
        return 2
    if args.fidelity not in FIDELITY_ORDER:
        print("invalid fidelity", file=sys.stderr)
        return 2
    rec = state["modules"][args.module]
    rec["evidence_state"] = args.to
    rec["fidelity"] = args.fidelity
    rec.setdefault("promotion_evidence", []).append(str(evidence.relative_to(ROOT)))
    rec.setdefault("evidence_history", []).append({"state": args.to, "fidelity": args.fidelity, "evidence": str(evidence.relative_to(ROOT)), "timestamp_utc": now(), "work_unit": item["id"]})
    rec["last_promoted_utc"] = now()
    state["last_updated_utc"] = now()
    save_json(STATE_PATH, state)
    decision = {"decision_id": f"PROMOTE-{args.module}-{args.to}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}", "timestamp_utc": now(), "work_unit": item["id"], "decision": f"Promoted Module {args.module} from {current} to {args.to} at {args.fidelity}", "basis": [str(evidence.relative_to(ROOT))], "alternatives_rejected": [], "changes_science": False, "required_replay": "none", "commit_sha": state.get("last_verified_commit") or ""}
    with (ROOT / "memory/DECISION_LOG.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(decision, ensure_ascii=False) + "\n")
    print(json.dumps(decision, indent=2))
    return 0


def cmd_record_claim(args: argparse.Namespace) -> int:
    path = (ROOT / args.file).resolve()
    if not path.exists() or ROOT not in path.parents:
        print("claim record must exist inside repository", file=sys.stderr)
        return 2
    claim = load_json(path)
    required = ["claim_id", "text", "owner", "evidence_state", "fidelity", "supported", "evidence"]
    missing = [k for k in required if k not in claim]
    if missing:
        print(f"claim record missing: {missing}", file=sys.stderr)
        return 2
    if claim["evidence_state"] not in EVIDENCE_ORDER and claim["evidence_state"] not in VALID_EXTRA_STATES:
        print("invalid claim evidence state", file=sys.stderr)
        return 2
    ledger = load_json(ROOT / "CLAIMS_LEDGER.json")
    if any(x.get("claim_id") == claim["claim_id"] for x in ledger.get("claims", [])):
        print("claim_id already exists", file=sys.stderr)
        return 2
    claim["recorded_utc"] = now()
    claim["work_unit"] = load_json(STATE_PATH)["active_work_unit"]
    ledger.setdefault("claims", []).append(claim)
    save_json(ROOT / "CLAIMS_LEDGER.json", ledger)
    print(json.dumps(claim, indent=2))
    return 0


def cmd_context_pack(args: argparse.Namespace) -> int:
    cmd_context(argparse.Namespace())
    state = load_json(STATE_PATH)
    item = active_item()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = ROOT / (args.output or f"memory/context_packs/3RFC_CONTEXT_{item['id']}_{stamp}.zip")
    out.parent.mkdir(parents=True, exist_ok=True)
    candidates = [
        ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "STATE.json", ROOT / "WORK_QUEUE.json",
        ROOT / "CLAIMS_LEDGER.json", ROOT / "memory/CURRENT_CONTEXT.md", ROOT / "memory/SOURCE_REGISTRY.json",
        ROOT / "memory/ARTIFACT_REGISTRY.json", ROOT / "memory/RUN_INDEX.json", ROOT / "memory/DECISION_LOG.jsonl",
        ROOT / "memory/FAILURE_LOG.jsonl", ROOT / "config/project.json", ROOT / "config/module_graph.json", ROOT / "config/module_evidence_requirements.json",
        ROOT / "docs/00_SCIENTIFIC_CONSTITUTION.md", ROOT / "docs/01_WORK_MODEL_OPERATING_MANUAL.md"
    ]
    if item["module"] in state.get("modules", {}):
        candidates += [ROOT / "modules" / item["module"] / "README.md", ROOT / "modules" / item["module"] / "spec.json"]
    if state.get("current_run"):
        try:
            _, run_path, _ = find_run(state["current_run"])
            candidates.append(run_path)
        except RuntimeError:
            pass
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in candidates:
            if not p.exists():
                continue
            if p.is_file():
                zf.write(p, p.relative_to(ROOT))
            else:
                for child in sorted(p.rglob("*")):
                    if child.is_file():
                        zf.write(child, child.relative_to(ROOT))
    print(out.relative_to(ROOT))
    return 0


def cmd_verify_bundle(_: argparse.Namespace) -> int:
    manifest_path = ROOT / "BUNDLE_MANIFEST.json"
    if not manifest_path.exists():
        print("BUNDLE_MANIFEST.json missing", file=sys.stderr)
        return 2
    manifest = load_json(manifest_path)
    errors = []
    for rec in manifest.get("files", []):
        path = ROOT / rec["path"]
        if not path.exists():
            errors.append(f"missing: {rec['path']}")
        elif sha256_file(path) != rec["sha256"]:
            errors.append(f"hash mismatch: {rec['path']}")
    if errors:
        print("BUNDLE VERIFICATION: FAIL")
        for e in errors:
            print(f"- {e}")
        return 1
    print(f"BUNDLE VERIFICATION: PASS ({len(manifest.get('files', []))} files)")
    return 0


def cmd_record_commit(args: argparse.Namespace) -> int:
    if not re.fullmatch(r"[0-9a-fA-F]{7,64}", args.sha):
        print("commit SHA must be 7-64 hexadecimal characters", file=sys.stderr)
        return 2
    state = load_json(STATE_PATH)
    state["last_verified_commit"] = args.sha.lower()
    state["last_verified_branch"] = args.branch
    state["last_updated_utc"] = now()
    save_json(STATE_PATH, state)
    rec = {
        "decision_id": f"COMMIT-{args.sha[:12]}", "timestamp_utc": now(),
        "work_unit": state["active_work_unit"], "decision": args.note or "Verified GitHub commit and diff",
        "basis": [f"commit:{args.sha.lower()}", f"branch:{args.branch}"], "alternatives_rejected": [],
        "changes_science": False, "required_replay": "none", "commit_sha": args.sha.lower()
    }
    with (ROOT / "memory/DECISION_LOG.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(json.dumps(rec, indent=2))
    return 0


def cmd_admit_seed(_: argparse.Namespace) -> int:
    state = load_json(STATE_PATH)
    if state.get("active_work_unit") != "SRC-010":
        print("admit-seed is authorized only while SRC-010 is active", file=sys.stderr)
        return 2
    manifest = load_json(ROOT / "source_seed/SOURCE_SEED_MANIFEST.json")
    admitted = 0
    for rec in sorted(manifest.get("files", []), key=lambda x: (x.get("reading_order", 999), x["filename"])):
        src = ROOT / "source_seed" / rec["filename"]
        digest = sha256_file(src)
        if digest != rec["sha256"]:
            print(f"seed hash mismatch: {rec['filename']}", file=sys.stderr)
            return 1
        ns = argparse.Namespace(path=str(src), classification=rec["default_classification"], label=rec.get("role") or src.name)
        code = cmd_admit_source(ns)
        if code:
            return code
        admitted += 1
    source_manifest = load_json(ROOT / "sources/SOURCE_MANIFEST.json")
    source_manifest["status"] = "ADMITTED_FROM_SEED_PENDING_INDEPENDENT_RECONSTRUCTION"
    source_manifest["manifest_sha256"] = hashlib.sha256(json.dumps(source_manifest.get("sources", []), sort_keys=True).encode()).hexdigest()
    save_json(ROOT / "sources/SOURCE_MANIFEST.json", source_manifest)
    state = load_json(STATE_PATH)
    state["source_state"] = "SEED_ADMITTED_PENDING_INDEPENDENT_RECONSTRUCTION"
    state["canonical_source_manifest"] = "sources/SOURCE_MANIFEST.json"
    state["last_updated_utc"] = now()
    save_json(STATE_PATH, state)
    print(f"admitted {admitted} seed files")
    return 0

def main() -> int:
    p = argparse.ArgumentParser(description="3-RFC repository control")
    sub = p.add_subparsers(dest="cmd", required=True)

    for name, func in [("doctor", cmd_doctor), ("status", cmd_status), ("next", cmd_next), ("context", cmd_context), ("firewall-scan", cmd_firewall_scan), ("verify-bundle", cmd_verify_bundle), ("admit-seed", cmd_admit_seed)]:
        sp = sub.add_parser(name)
        sp.set_defaults(func=func)

    sp = sub.add_parser("record-commit")
    sp.add_argument("sha")
    sp.add_argument("--branch", required=True)
    sp.add_argument("--note")
    sp.set_defaults(func=cmd_record_commit)

    sp = sub.add_parser("close-run")
    sp.add_argument("--run-id", required=True)
    sp.add_argument("--result", choices=["PASS", "FAIL", "BLOCKED"], required=True)
    sp.add_argument("--closeout", required=True)
    sp.set_defaults(func=cmd_close_run)

    sp = sub.add_parser("promote-module")
    sp.add_argument("module")
    sp.add_argument("--to", required=True)
    sp.add_argument("--fidelity", required=True)
    sp.add_argument("--evidence", required=True)
    sp.set_defaults(func=cmd_promote_module)

    sp = sub.add_parser("record-claim")
    sp.add_argument("--file", required=True)
    sp.set_defaults(func=cmd_record_claim)

    sp = sub.add_parser("context-pack")
    sp.add_argument("--output")
    sp.set_defaults(func=cmd_context_pack)

    sp = sub.add_parser("new-run")
    sp.add_argument("module")
    sp.add_argument("--run-id")
    sp.set_defaults(func=cmd_new_run)

    sp = sub.add_parser("admit-source")
    sp.add_argument("path")
    sp.add_argument("--classification", required=True)
    sp.add_argument("--label")
    sp.set_defaults(func=cmd_admit_source)

    sp = sub.add_parser("freeze")
    sp.add_argument("path")
    sp.add_argument("--kind", required=True)
    sp.set_defaults(func=cmd_freeze)

    sp = sub.add_parser("hash-tree")
    sp.add_argument("path")
    sp.add_argument("--output")
    sp.set_defaults(func=cmd_hash_tree)

    sp = sub.add_parser("advance")
    sp.add_argument("--task", required=True)
    sp.add_argument("--result", choices=["PASS", "FAIL"], required=True)
    sp.add_argument("--evidence", required=True)
    sp.add_argument("--note")
    sp.set_defaults(func=cmd_advance)

    sp = sub.add_parser("new-proof")
    sp.add_argument("slug")
    sp.add_argument("--title", required=True)
    sp.set_defaults(func=cmd_new_proof)

    sp = sub.add_parser("new-universe")
    sp.add_argument("slug")
    sp.add_argument("--title", required=True)
    sp.set_defaults(func=cmd_new_universe)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
