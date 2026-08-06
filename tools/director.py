#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "STATE.json"
QUEUE = ROOT / "WORK_QUEUE.json"
CALLS = ROOT / "config/WOLFRAM_CALLS.json"
CATALOG = ROOT / "recipes/CATALOG.json"
BINDINGS = ROOT / "config/EXECUTION_BINDINGS.json"
WORK_UNIT_PACKS = ROOT / "config/WORK_UNIT_PACKS.json"
PACKET = ROOT / "work_packets/ACTIVE_WORK_PACKET.md"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def active_item() -> dict[str, Any]:
    state = load(STATE)
    items = load(QUEUE)["items"]
    matches = [x for x in items if x["id"] == state["active_work_unit"]]
    if len(matches) != 1:
        raise RuntimeError("active work unit does not resolve uniquely")
    return matches[0]


def module_recipe(module: str) -> dict[str, Any] | None:
    path = ROOT / "recipes" / module / "recipe.json"
    return load(path) if path.exists() else None


def work_unit_pack(work_unit: str) -> dict[str, Any] | None:
    if not WORK_UNIT_PACKS.exists():
        return None
    registry = load(WORK_UNIT_PACKS).get("work_units", {})
    entry = registry.get(work_unit)
    if not entry:
        return None
    recipe_path = ROOT / entry["recipe"]
    work_order_path = ROOT / entry["work_order"]
    if not recipe_path.is_file() or not work_order_path.is_file():
        return None
    return {
        "registry": entry,
        "recipe": load(recipe_path),
        "recipe_path": recipe_path,
        "work_order_path": work_order_path,
    }


def wolfram_calls() -> dict[str, dict[str, Any]]:
    calls = load(CALLS)["calls"]
    return {x["call_id"]: x for x in calls}


def execution_bindings(module: str | None = None) -> dict[str, Any]:
    modules = load(BINDINGS)["modules"]
    if module is None:
        return modules
    return modules.get(module, {"bindings": []})


def run_cmd(args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=check)


def recipe_errors() -> list[str]:
    errors: list[str] = []
    graph = load(ROOT / "config/module_graph.json")["module_order"]
    catalog = load(CATALOG)["modules"]
    calls = wolfram_calls()
    seen: set[str] = set()
    for mod in graph:
        if mod not in catalog:
            errors.append(f"missing recipe catalog entry for {mod}")
            continue
        rpath = ROOT / catalog[mod]["recipe"]
        wpath = ROOT / catalog[mod]["work_order"]
        if not rpath.exists():
            errors.append(f"missing recipe file for {mod}")
            continue
        if not wpath.exists():
            errors.append(f"missing work order for {mod}")
        rec = load(rpath)
        if rec.get("module") != mod:
            errors.append(f"recipe module mismatch for {mod}")
        if rec.get("parents") != load(ROOT / "modules" / mod / "spec.json").get("parents", []):
            errors.append(f"recipe parent mismatch for {mod}")
        for cid in rec.get("wolfram_calls", []):
            if cid in seen:
                errors.append(f"duplicate Wolfram call id {cid}")
            seen.add(cid)
            if cid not in calls:
                errors.append(f"unregistered Wolfram call {cid}")
                continue
            cpath = ROOT / calls[cid]["code_path"]
            if not cpath.exists():
                errors.append(f"missing Wolfram code {cpath.relative_to(ROOT)}")
            else:
                text = cpath.read_text(encoding="utf-8")
                if "ToString[result, InputForm]" not in text:
                    errors.append(f"Wolfram call is not self-reporting InputForm Association: {cid}")
    if set(seen) != set(calls):
        missing = sorted(set(calls) - seen)
        if missing:
            errors.append(f"registered calls not referenced by recipes: {missing}")
    binding_modules = execution_bindings()
    if set(binding_modules) != set(graph):
        errors.append("execution-binding module set differs from module graph")
    queue_items = load(QUEUE)["items"]
    expected_packs = {item["id"] for item in queue_items if module_recipe(item["module"]) is None}
    registered_packs = set(load(WORK_UNIT_PACKS).get("work_units", {})) if WORK_UNIT_PACKS.exists() else set()
    if expected_packs != registered_packs:
        errors.append(f"work-unit pack set drift: expected {sorted(expected_packs)}, registered {sorted(registered_packs)}")
    for work_id in sorted(expected_packs):
        pack = work_unit_pack(work_id)
        if not pack:
            errors.append(f"missing or unreadable work-unit pack for {work_id}")
            continue
        rec = pack["recipe"]
        if rec.get("work_unit") != work_id:
            errors.append(f"work-unit recipe id mismatch for {work_id}")
        if not rec.get("exact_sequence"):
            errors.append(f"work-unit recipe has no exact sequence for {work_id}")
        if not rec.get("componentwise_gates"):
            errors.append(f"work-unit recipe has no componentwise gates for {work_id}")
        if work_id == "HR-255":
            matrix = ROOT / "work_units/HR-255/EXECUTION_MATRIX.json"
            prompt = ROOT / "work_units/HR-255/WORK_MODEL_PROMPT.md"
            if not matrix.is_file() or not prompt.is_file():
                errors.append("HR-255 execution matrix or work-model prompt is missing")
            elif len(load(matrix).get("rows", [])) < 20:
                errors.append("HR-255 execution matrix has fewer than 20 mandatory rows")
    for mod in graph:
        recipe = module_recipe(mod) or {}
        registered = binding_modules.get(mod, {}).get("bindings", [])
        if recipe.get("solver_bindings") != registered:
            errors.append(f"recipe execution bindings drift for {mod}")
        seen_solvers: set[str] = set()
        for binding in registered:
            solver = binding.get("solver")
            if solver in seen_solvers:
                errors.append(f"duplicate solver binding {solver} in {mod}")
            seen_solvers.add(solver)
            template = ROOT / binding.get("template", "")
            sheet = ROOT / binding.get("binding_sheet", "")
            if not template.is_file():
                errors.append(f"missing solver template for {mod}: {template}")
            else:
                template_doc = load(template)
                if template_doc.get("classification") != "UNBOUND_EXECUTION_TEMPLATE":
                    errors.append(f"solver template classification drift for {mod}/{solver}")
            if not sheet.is_file():
                errors.append(f"missing binding sheet for {mod}/{solver}: {sheet}")
            elif template.is_file() and load(sheet).get("template_sha256") != sha256(template):
                errors.append(f"binding sheet template hash drift for {mod}/{solver}")
    return errors


def cmd_doctor(_: argparse.Namespace) -> int:
    errors = recipe_errors()
    base = run_cmd([sys.executable, "tools/rfc.py", "doctor"], check=False)
    if base.returncode:
        errors.append("base rfc doctor failed:\n" + base.stdout + base.stderr)
    ref = run_cmd([sys.executable, "tools/run_reference_checks.py", "--module", "ALL"], check=False)
    if ref.returncode:
        errors.append("manufactured reference matrix failed:\n" + ref.stdout + ref.stderr)
    if errors:
        print("3-RFC EXECUTION DIRECTOR: FAIL")
        for e in errors:
            print(f"- {e}")
        return 1
    print("3-RFC EXECUTION DIRECTOR: PASS")
    print(f"Recipe packs: {len(load(CATALOG)['modules'])}")
    print(f"Wolfram calls: {len(load(CALLS)['calls'])}")
    print(f"Local solver templates: {sum(len(x['bindings']) for x in execution_bindings().values())}")
    print(f"Administrative work-unit packs: {len(load(WORK_UNIT_PACKS)['work_units'])}")
    print(f"Active work unit: {active_item()['id']}")
    return 0


def cmd_active(_: argparse.Namespace) -> int:
    item = active_item()
    recipe = module_recipe(item["module"])
    pack = work_unit_pack(item["id"])
    recipe_path = f"recipes/{item['module']}/recipe.json" if recipe else (str(pack["recipe_path"].relative_to(ROOT)) if pack else None)
    out = {
        "work_unit": item["id"],
        "title": item["title"],
        "module": item["module"],
        "objective": item["objective"],
        "recipe": recipe_path,
        "current_run": load(STATE).get("current_run"),
        "next_command": "python tools/director.py prepare-active",
    }
    print(json.dumps(out, indent=2))
    return 0


def admin_instructions(item: dict[str, Any]) -> list[str]:
    tid = item["id"]
    if tid == "BOOT-000":
        return [
            "Run `python tools/director.py doctor` and `python -m unittest discover -s tests -v`.",
            "Copy this repository scaffold to the root of Charlie-glitch83/3-RFC.",
            "Commit with the queue-prescribed message.",
            "Verify the exact GitHub commit SHA, changed-file list, fetched README, and branch diff.",
            "Record the verified SHA with `python tools/rfc.py record-commit <SHA> --branch <BRANCH> --note \"Verified scaffold commit and diff\"`.",
            "Complete `runs/BOOT-000/CLOSEOUT.md`, then advance BOOT-000 only after the visible GitHub verification passes.",
        ]
    if tid == "SRC-010":
        return [
            "Run `python tools/rfc.py admit-seed`.",
            "Independently recompute every frozen source SHA-256 and compare it with `sources/SOURCE_MANIFEST.json`.",
            "Confirm P29, P30, N-body proof, and N-body metadata are present as exact bytes.",
            "Do not promote source summaries or deep-soak reports to canonical scientific parents.",
        ]
    if tid == "AUTH-020":
        return [
            "Use the already prepared `theory/SCIENTIFIC_CONSTITUTION.md`, `theory/TERMINOLOGY_LOCK.json`, and `theory/CLAIM_MAP.json` as the candidate outputs.",
            "Trace every material statement to the exact admitted P29/P30/N-body source bytes.",
            "Run a terminology search proving that no active file silently redefines CIF or QV.",
            "Record any source disagreement instead of rewriting it silently.",
        ]
    if tid == "XWALK-030":
        return [
            "Use `theory/ENHANCEMENT_CROSSWALK.json` as the prebuilt crosswalk.",
            "Add exact source hashes and line/object references after admission.",
            "Independently check that valid parent architecture is preserved, failed outcomes are regression-only, and N-body is not over-universalized.",
        ]
    if tid == "REC-040":
        return [
            "Use `recovery/CANDIDATE_ASSET_DISPOSITION.json` as the candidate list.",
            "Fetch each candidate from Charlie-glitch83/2-RFC by exact commit and path through the connected GitHub integration.",
            "Replay before admission. Copy only verified exact objects into a content-addressed recovery directory.",
            "Treat the repaired Module L first pass only at its declared verified scope; do not call it physical L without exact K parent execution.",
        ]
    if tid == "FRONTIER-050":
        return [
            "Use `audit/PHYSICAL_FRONTIER_SEED.json` as the prefilled audit skeleton.",
            "Replace every unverified statement with exact artifact hashes, run records, solver/restart evidence, covariance, and independent-reconstruction evidence.",
            "Select the earliest exact missing parent. Authorize one child only.",
        ]
    return item.get("steps", [])


def find_current_run_path() -> Path | None:
    state = load(STATE)
    rid = state.get("current_run")
    if not rid:
        return None
    idx = load(ROOT / "memory/RUN_INDEX.json").get("runs", [])
    matches = [ROOT / x["path"] for x in idx if x.get("run_id") == rid]
    return matches[0] if len(matches) == 1 else None


def create_run_if_needed(item: dict[str, Any], create: bool) -> Path | None:
    state = load(STATE)
    existing = find_current_run_path()
    if existing:
        return existing
    if not create or item["id"] == "BOOT-000":
        return ROOT / "runs" / "BOOT-000" if item["id"] == "BOOT-000" else None
    cp = run_cmd([sys.executable, "tools/rfc.py", "new-run", item["module"]], check=False)
    if cp.returncode:
        raise RuntimeError(cp.stdout + cp.stderr)
    rel = cp.stdout.strip().splitlines()[-1]
    return ROOT / rel


def render_packet(item: dict[str, Any], run_path: Path | None) -> str:
    lines = [
        f"# ACTIVE WORK PACKET — {item['id']}", "",
        "**This is the only authorized work. Execute it in order.**", "",
        f"- Module: `{item['module']}`", f"- Objective: {item['objective']}",
        f"- Run workspace: `{run_path.relative_to(ROOT) if run_path else 'not yet created'}`", "",
        "## Exact sequence", "",
    ]
    recipe = module_recipe(item["module"])
    if recipe:
        lines += [
            f"1. Read `recipes/{item['module']}/WORK_ORDER.md` and `recipes/{item['module']}/recipe.json`.",
            "2. Verify all exact parent hashes and fill the run source register.",
            "3. Freeze the pre-execution lock before primary execution.",
            "4. Run these Wolfram calls exactly and record their complete outputs:", "",
        ]
        for cid in recipe["wolfram_calls"]:
            lines.append(f"   - `python tools/director.py wolfram-show --call {cid}`")
        run_label = str(run_path.relative_to(ROOT)) if run_path else "<RUN_DIR>"
        lines += ["", f"5. Run `python tools/run_reference_checks.py --module {item['module']} --output {run_label}/reference_checks.json`.",
                  "6. Bind and run the prebuilt local engines listed below. Every `__BIND_` token is a hard stop:", ""]
        for binding in recipe.get("solver_bindings", []):
            lines.append(f"   - `{binding['copy_command'].replace('<RUN_DIR>', run_label)}`")
            lines.append(f"   - fill `{binding['binding_sheet']}` after it is copied into the run; every value requires an origin SHA-256")
            lines.append(f"   - `{binding['materialize_command'].replace('<RUN_DIR>', run_label)}`")
            lines.append(f"   - `{binding['run_command'].replace('<RUN_DIR>', run_label)}`")
        lines += ["", "7. Execute any remaining parent-driven domain code named in the recipe. Manufactured checks and generic engines do not replace the physical result.",
                  "8. Run countermodels, ablations, convergence, restart, replay, uncertainty/covariance, and independent reconstruction.",
                  "9. Finalize manifests only after outputs stop changing. State strongest supported and unsupported claims.",
                  "10. Commit and verify the exact GitHub SHA/diff before advancing."]
    else:
        pack = work_unit_pack(item["id"])
        if pack:
            pack_recipe = pack["recipe"]
            lines += [
                f"1. Read `{pack['work_order_path'].relative_to(ROOT)}` and `{pack['recipe_path'].relative_to(ROOT)}`.",
                "2. Execute the frozen sequence below without redesigning it:",
                "",
            ]
            for index, step in enumerate(pack_recipe.get("exact_sequence", []), 1):
                lines.append(f"   {index}. {step}")
            if pack_recipe.get("exact_commands"):
                lines += ["", "3. Run the exact commands:", ""]
                for command in pack_recipe["exact_commands"]:
                    lines.append(f"   - `{command}`")
            if item["id"] == "HR-255":
                lines += [
                    "",
                    "4. Execute every row in `work_units/HR-255/EXECUTION_MATRIX.json`; no row may be skipped or converted into prose.",
                    "5. Use `work_units/HR-255/WORK_MODEL_PROMPT.md` as the operator prompt for every HR subrun.",
                ]
        else:
            for i, step in enumerate(admin_instructions(item), 1):
                lines.append(f"{i}. {step}")
    pack_for_fields = work_unit_pack(item["id"])
    field_source = pack_for_fields["recipe"] if pack_for_fields else item
    deliverables = field_source.get("deliverables", item.get("deliverables", []))
    gates = field_source.get("componentwise_gates", item.get("gates", []))
    commit_message = field_source.get("commit_message", item.get("commit_message", ""))
    lines += ["", "## Required deliverables", ""] + [f"- {x}" for x in deliverables]
    lines += ["", "## Componentwise gates", ""] + [f"- {x}" for x in gates]
    lines += ["", "## Commit message", "", f"`{commit_message}`", ""]
    return "\n".join(lines)


def prefill_run(item: dict[str, Any], run_path: Path | None) -> None:
    if not run_path or not run_path.exists():
        return
    recipe = module_recipe(item["module"])
    pack = work_unit_pack(item["id"])
    if pack:
        shutil.copy2(pack["recipe_path"], run_path / "FROZEN_WORK_UNIT_RECIPE.json")
        shutil.copy2(pack["work_order_path"], run_path / "WORK_ORDER.md")
        if item["id"] == "HR-255":
            shutil.copy2(ROOT / "work_units/HR-255/EXECUTION_MATRIX.json", run_path / "EXECUTION_MATRIX.json")
            shutil.copy2(ROOT / "work_units/HR-255/WORK_MODEL_PROMPT.md", run_path / "WORK_MODEL_PROMPT.md")
        if not recipe:
            return
    if not recipe:
        return
    shutil.copy2(ROOT / "recipes" / item["module"] / "recipe.json", run_path / "FROZEN_RECIPE.json")
    shutil.copy2(ROOT / "recipes" / item["module"] / "WORK_ORDER.md", run_path / "WORK_ORDER.md")
    shutil.copy2(ROOT / "recipes" / item["module"] / "gates.json", run_path / "REQUIRED_GATES.json")
    wolfram_dir = run_path / "wolfram"
    wolfram_dir.mkdir(exist_ok=True)
    calls = wolfram_calls()
    wolfram_lines = [f"# Exact Wolfram sequence — {item['module']}", "", "Submit each `input.wl` verbatim to `WolframLanguageEvaluator`, save the complete response as `output.txt`, then run the shown record command.", ""]
    for call_id in recipe.get("wolfram_calls", []):
        call_dir = wolfram_dir / call_id
        call_dir.mkdir(exist_ok=True)
        shutil.copy2(ROOT / calls[call_id]["code_path"], call_dir / "input.wl")
        wolfram_lines += [f"## {call_id}", "", calls[call_id]["purpose"], "", "```bash", f"python tools/director.py wolfram-show --call {call_id}", f"python tools/director.py wolfram-record --run {load(STATE).get('current_run')} --call {call_id} --output {call_dir.relative_to(ROOT)}/output.txt", "```", ""]
    (run_path / "WOLFRAM_SEQUENCE.md").write_text("\n".join(wolfram_lines), encoding="utf-8")
    template_dir = run_path / "solver_templates"
    sheet_dir = run_path / "binding_sheets"
    config_dir = run_path / "solver_configs"
    template_dir.mkdir(exist_ok=True)
    sheet_dir.mkdir(exist_ok=True)
    config_dir.mkdir(exist_ok=True)
    for binding in recipe.get("solver_bindings", []):
        template_src = ROOT / binding["template"]
        sheet_src = ROOT / binding["binding_sheet"]
        template_dest = template_dir / template_src.name
        sheet_dest = sheet_dir / sheet_src.name
        if not template_dest.exists():
            shutil.copy2(template_src, template_dest)
        if not sheet_dest.exists():
            shutil.copy2(sheet_src, sheet_dest)
    save(run_path / "LOCAL_EXECUTION_BINDINGS.json", {"module": item["module"], "bindings": recipe.get("solver_bindings", [])})
    commands = ["#!/usr/bin/env bash", "set -euo pipefail", f"RUN_DIR='{run_path.relative_to(ROOT)}'", ""]
    commands += ["# Materialize each config only after filling its binding sheet."]
    for binding in recipe.get("solver_bindings", []):
        commands += [f"# {binding['purpose']}", binding["materialize_command"].replace("<RUN_DIR>", "${RUN_DIR}")]
    commands += ["", f'bash tools/finish_local_phase.sh {item["module"]} "${{RUN_DIR}}"', ""]
    run_script = run_path / "RUN_LOCAL_PHASE.sh"
    run_script.write_text("\n".join(commands), encoding="utf-8")
    run_script.chmod(0o755)
    plan = run_path / "RUN_PLAN.md"
    text = plan.read_text(encoding="utf-8") if plan.exists() else ""
    if "PRE-CHEWED MODULE PLAN" not in text:
        plan.write_text(
            f"# Run Plan — {item['id']}\n\nPRE-CHEWED MODULE PLAN\n\n"
            f"Objective: {recipe['objective']}\n\n"
            "The exact derivation obligations, calls, outputs, gates, and stop conditions are frozen in `FROZEN_RECIPE.json`, `WORK_ORDER.md`, and `REQUIRED_GATES.json`.\n\n"
            "Before execution, replace every placeholder in the source register, pre-execution lock, environment, expected outcomes, tolerances, falsifiers, and claim boundary with exact frozen values.\n",
            encoding="utf-8",
        )


def cmd_prepare(args: argparse.Namespace) -> int:
    item = active_item()
    run_path = create_run_if_needed(item, args.create_run)
    prefill_run(item, run_path)
    PACKET.parent.mkdir(parents=True, exist_ok=True)
    PACKET.write_text(render_packet(item, run_path), encoding="utf-8")
    print(PACKET.relative_to(ROOT))
    if run_path:
        print(f"run: {run_path.relative_to(ROOT)}")
    return 0


def cmd_wolfram_list(args: argparse.Namespace) -> int:
    calls = wolfram_calls()
    rows = [x for x in calls.values() if not args.module or x["module"] == args.module]
    for x in rows:
        print(f"{x['call_id']}\t{x['module']}\t{x['purpose']}\t{x['code_path']}")
    return 0


def cmd_wolfram_show(args: argparse.Namespace) -> int:
    calls = wolfram_calls()
    if args.call not in calls:
        print("unknown call", file=sys.stderr)
        return 2
    rec = calls[args.call]
    path = ROOT / rec["code_path"]
    print(f"(* CALL_ID: {args.call} *)")
    print(f"(* PURPOSE: {rec['purpose']} *)")
    print(path.read_text(encoding="utf-8"), end="")
    return 0


def cmd_wolfram_record(args: argparse.Namespace) -> int:
    calls = wolfram_calls()
    if args.call not in calls:
        print("unknown call", file=sys.stderr)
        return 2
    output = Path(args.output).resolve()
    if not output.exists() or not output.is_file():
        print("output file missing", file=sys.stderr)
        return 2
    idx = load(ROOT / "memory/RUN_INDEX.json").get("runs", [])
    matches = [ROOT / x["path"] for x in idx if x.get("run_id") == args.run]
    if len(matches) != 1:
        print("run id does not resolve uniquely", file=sys.stderr)
        return 2
    run_path = matches[0]
    rec = calls[args.call]
    dest = run_path / "wolfram" / args.call
    dest.mkdir(parents=True, exist_ok=True)
    code = ROOT / rec["code_path"]
    shutil.copy2(code, dest / "input.wl")
    shutil.copy2(output, dest / "output.txt")
    record = {
        "call_id": args.call,
        "module": rec["module"],
        "purpose": rec["purpose"],
        "tool": "WolframLanguageEvaluator",
        "timestamp_utc": now(),
        "input_sha256": sha256(dest / "input.wl"),
        "output_sha256": sha256(dest / "output.txt"),
        "public_knowledge_allowed": rec["public_knowledge_allowed"],
        "public_knowledge_used": False,
        "interpretation_required": True,
    }
    gate = run_cmd([sys.executable, "tools/check_wolfram_output.py", "--call", args.call, "--output", str(dest / "output.txt"), "--json-output", str(dest / "gate.json")], check=False)
    record["manufactured_gate_returncode"] = gate.returncode
    record["manufactured_gate_path"] = str((dest / "gate.json").relative_to(ROOT))
    save(dest / "record.json", record)
    print(json.dumps(record, indent=2))
    if gate.stdout:
        print(gate.stdout, end="")
    if gate.stderr:
        print(gate.stderr, file=sys.stderr, end="")
    return 0 if gate.returncode == 0 else 1


def cmd_solver_list(args: argparse.Namespace) -> int:
    modules = execution_bindings(args.module) if args.module else None
    if args.module:
        rows = modules.get("bindings", [])
        if not rows:
            print("unknown module or no bindings", file=sys.stderr)
            return 2
        for row in rows:
            print(f"{args.module}	{row['solver']}	{row['template']}	{row['purpose']}")
        return 0
    for module, rec in execution_bindings().items():
        for row in rec.get("bindings", []):
            print(f"{module}	{row['solver']}	{row['template']}	{row['purpose']}")
    return 0


def _select_binding(module: str, solver: str) -> dict[str, Any] | None:
    rows = [x for x in execution_bindings(module).get("bindings", []) if x.get("solver") == solver]
    return rows[0] if len(rows) == 1 else None


def cmd_solver_show(args: argparse.Namespace) -> int:
    binding = _select_binding(args.module, args.solver)
    if not binding:
        print("binding does not resolve uniquely", file=sys.stderr)
        return 2
    print((ROOT / binding["template"]).read_text(encoding="utf-8"), end="")
    return 0


def cmd_solver_copy(args: argparse.Namespace) -> int:
    binding = _select_binding(args.module, args.solver)
    if not binding:
        print("binding does not resolve uniquely", file=sys.stderr)
        return 2
    destination = Path(args.destination).resolve()
    template_dir = destination / "solver_templates"
    sheet_dir = destination / "binding_sheets"
    template_dir.mkdir(parents=True, exist_ok=True)
    sheet_dir.mkdir(parents=True, exist_ok=True)
    source = ROOT / binding["template"]
    sheet_source = ROOT / binding["binding_sheet"]
    target = template_dir / source.name
    sheet_target = sheet_dir / sheet_source.name
    existing = [path for path in (target, sheet_target) if path.exists()]
    if existing and not args.force:
        print(f"refusing to overwrite existing files: {[str(path) for path in existing]}", file=sys.stderr)
        return 2
    shutil.copy2(source, target)
    shutil.copy2(sheet_source, sheet_target)
    print(json.dumps({"template": str(target), "binding_sheet": str(sheet_target)}, indent=2))
    return 0


def cmd_recipe(args: argparse.Namespace) -> int:
    rec = module_recipe(args.module)
    if not rec:
        print("unknown module recipe", file=sys.stderr)
        return 2
    print(json.dumps(rec, indent=2))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="3-RFC execution director")
    sub = p.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("doctor"); sp.set_defaults(func=cmd_doctor)
    sp = sub.add_parser("active"); sp.set_defaults(func=cmd_active)
    sp = sub.add_parser("prepare-active"); sp.add_argument("--create-run", action="store_true"); sp.set_defaults(func=cmd_prepare)
    sp = sub.add_parser("wolfram-list"); sp.add_argument("--module"); sp.set_defaults(func=cmd_wolfram_list)
    sp = sub.add_parser("wolfram-show"); sp.add_argument("--call", required=True); sp.set_defaults(func=cmd_wolfram_show)
    sp = sub.add_parser("wolfram-record"); sp.add_argument("--run", required=True); sp.add_argument("--call", required=True); sp.add_argument("--output", required=True); sp.set_defaults(func=cmd_wolfram_record)
    sp = sub.add_parser("solver-list"); sp.add_argument("--module"); sp.set_defaults(func=cmd_solver_list)
    sp = sub.add_parser("solver-show"); sp.add_argument("--module", required=True); sp.add_argument("--solver", required=True); sp.set_defaults(func=cmd_solver_show)
    sp = sub.add_parser("solver-copy"); sp.add_argument("--module", required=True); sp.add_argument("--solver", required=True); sp.add_argument("--destination", required=True); sp.add_argument("--force", action="store_true"); sp.set_defaults(func=cmd_solver_copy)
    sp = sub.add_parser("recipe"); sp.add_argument("--module", required=True); sp.set_defaults(func=cmd_recipe)
    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
