from __future__ import annotations

from pathlib import Path
from typing import Any

from rfc_engine.provenance import tree_manifest


def run_freeze_packet(cfg: dict[str, Any]) -> dict[str, Any]:
    """Content-address a completed universe directory without mutating it."""
    root = Path(cfg["root"]).resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError("freeze root must be an existing directory")
    manifest = tree_manifest(root)
    required = set(cfg.get("required_relative_paths", []))
    present = {x["path"] for x in manifest["files"]}
    missing = sorted(required - present)
    return {
        "success": not missing and bool(manifest["files"]),
        "classification": "CONTENT_ADDRESSED_UNIVERSE_FREEZE",
        "universe_hash": manifest["sha256"],
        "file_count": len(manifest["files"]),
        "total_bytes": sum(x["bytes"] for x in manifest["files"]),
        "missing_required_paths": missing,
        "manifest": manifest,
    }
