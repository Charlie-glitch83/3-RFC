#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Execute every provenance-bound local solver config in an active run")
    parser.add_argument("--run", required=True)
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()
    run = Path(args.run).resolve()
    config_dir = run / "solver_configs"
    output_root = run / "solver_outputs"
    if not run.is_dir() or not config_dir.is_dir():
        raise SystemExit("run or solver_configs directory is missing")
    configs = sorted(config_dir.glob("*.json"))
    if not configs:
        raise SystemExit("no materialized solver configurations found")
    if args.clean and output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    rows = []
    for config in configs:
        try:
            doc = json.loads(config.read_text())
        except Exception as exc:
            rows.append({"config": config.name, "success": False, "error": f"JSON error: {exc}"})
            continue
        if doc.get("classification") != "PROVENANCE_BOUND_EXECUTION_CONFIG":
            rows.append({"config": config.name, "success": False, "error": "configuration was not created by the provenance materializer"})
            continue
        solver = doc.get("solver", "unknown")
        destination = output_root / config.stem
        command = [sys.executable, str(ROOT / "tools/run_configured_solver.py"), "--config", str(config), "--output-dir", str(destination)]
        completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        manifest_path = destination / "manifest.json"
        manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
        rows.append({
            "config": config.name,
            "solver": solver,
            "returncode": completed.returncode,
            "success": bool(manifest.get("success", False)) and completed.returncode == 0,
            "classification": manifest.get("classification"),
            "manifest": str(manifest_path),
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
        })
    summary = {
        "classification": "MODULE_LOCAL_EXECUTION_PIPELINE",
        "run": str(run),
        "configuration_count": len(configs),
        "overall": "PASS" if rows and all(row.get("success") for row in rows) else "FAIL",
        "results": rows,
        "warning": "Local solver success is necessary but does not replace source admission, Wolfram gates, convergence matrices, restart/replay, independent reconstruction, or module closeout."
    }
    (output_root / "SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return 0 if summary["overall"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
