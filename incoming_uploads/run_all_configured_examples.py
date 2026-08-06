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
    parser = argparse.ArgumentParser(description="Run every manufactured configured-solver example")
    parser.add_argument("--output-root", default="configured_runs/results")
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()
    output_root = (ROOT / args.output_root).resolve() if not Path(args.output_root).is_absolute() else Path(args.output_root)
    if args.clean and output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    rows = []
    for config in sorted((ROOT / "configured_runs/examples").glob("*.json")):
        destination = output_root / config.stem
        command = [sys.executable, str(ROOT / "tools/run_configured_solver.py"), "--config", str(config), "--output-dir", str(destination)]
        completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        manifest_path = destination / "manifest.json"
        manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {"success": False, "classification": "NO_MANIFEST"}
        rows.append({
            "example": config.name,
            "returncode": completed.returncode,
            "success": bool(manifest.get("success", False)),
            "classification": manifest.get("classification"),
            "manifest": str(manifest_path.relative_to(ROOT)) if manifest_path.exists() and manifest_path.is_relative_to(ROOT) else str(manifest_path),
            "stderr": completed.stderr.strip(),
        })
    summary = {
        "classification": "MANUFACTURED_CONFIGURED_SOLVER_MATRIX",
        "overall": "PASS" if all(row["success"] and row["returncode"] == 0 for row in rows) else "FAIL",
        "example_count": len(rows),
        "results": rows,
    }
    (output_root / "SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return 0 if summary["overall"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
