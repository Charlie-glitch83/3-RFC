#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SHA = re.compile(r"^[0-9a-f]{64}$")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def set_path(obj: Any, path: str, value: Any) -> None:
    parts = path.split(".")
    current = obj
    for part in parts[:-1]:
        if not isinstance(current, dict) or part not in current:
            raise ValueError(f"binding path does not exist: {path}")
        current = current[part]
    if not isinstance(current, dict) or parts[-1] not in current:
        raise ValueError(f"binding path does not exist: {path}")
    current[parts[-1]] = value


def unresolved(obj: Any) -> bool:
    if isinstance(obj, dict):
        return any(unresolved(value) for value in obj.values())
    if isinstance(obj, list):
        return any(unresolved(value) for value in obj)
    return isinstance(obj, str) and obj.startswith("__BIND_")


def validate_provenance(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    kind = record.get("origin_kind")
    if kind not in {"ADMITTED_SOURCE", "EXACT_PARENT_ARTIFACT", "INTERNAL_DERIVATION", "PREREGISTERED_MODULE_P_SOURCE"}:
        errors.append("origin_kind is invalid")
    origin_path = record.get("origin_path")
    origin_hash = record.get("origin_sha256")
    if not isinstance(origin_path, str) or not origin_path:
        errors.append("origin_path is required")
    if not isinstance(origin_hash, str) or not SHA.fullmatch(origin_hash):
        errors.append("origin_sha256 must be a lowercase SHA-256")
    elif origin_path:
        path = Path(origin_path)
        if not path.is_absolute():
            path = ROOT / path
        if not path.is_file():
            errors.append(f"origin file does not exist: {origin_path}")
        elif digest(path) != origin_hash:
            errors.append(f"origin hash mismatch: {origin_path}")
    if kind == "INTERNAL_DERIVATION" and not record.get("derivation_object"):
        errors.append("INTERNAL_DERIVATION requires derivation_object")
    if kind == "PREREGISTERED_MODULE_P_SOURCE" and record.get("module") != "P":
        errors.append("public comparison bindings are legal only for Module P")
    if record.get("value") is None:
        errors.append("value is required")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Materialize a provenance-complete solver configuration")
    parser.add_argument("--template", required=True)
    parser.add_argument("--binding-sheet", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    template_path = Path(args.template).resolve()
    sheet_path = Path(args.binding_sheet).resolve()
    output_path = Path(args.output).resolve()
    config = load(template_path)
    sheet = load(sheet_path)
    if sheet.get("template_sha256") != digest(template_path):
        raise SystemExit("binding sheet template SHA-256 does not match the template")
    records = sheet.get("bindings", [])
    errors: list[str] = []
    seen: set[str] = set()
    for record in records:
        path = record.get("path")
        if not isinstance(path, str) or not path:
            errors.append("binding path is required")
            continue
        if path in seen:
            errors.append(f"duplicate binding path: {path}")
        seen.add(path)
        local = validate_provenance(record)
        errors.extend([f"{path}: {error}" for error in local])
        if not local:
            try:
                set_path(config, path, record["value"])
            except ValueError as exc:
                errors.append(str(exc))
    expected = set(sheet.get("expected_binding_paths", []))
    if seen != expected:
        errors.append(f"binding path set differs from expected paths: missing={sorted(expected-seen)} extra={sorted(seen-expected)}")
    if unresolved(config):
        errors.append("materialized configuration still contains unresolved binding tokens")
    if errors:
        print(json.dumps({"status": "FAIL", "errors": errors}, indent=2))
        return 1
    config["classification"] = "PROVENANCE_BOUND_EXECUTION_CONFIG"
    config["binding_manifest"] = {
        "template_path": str(template_path),
        "template_sha256": digest(template_path),
        "binding_sheet_path": str(sheet_path),
        "binding_sheet_sha256": digest(sheet_path),
        "bindings": [{key: value for key, value in record.items() if key != "placeholder"} for record in records],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "output": str(output_path), "sha256": digest(output_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
