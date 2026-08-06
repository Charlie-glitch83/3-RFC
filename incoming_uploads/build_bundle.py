#!/usr/bin/env python3
"""Build the integrity records and a reproducible 3-RFC ZIP archive."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "BUNDLE_MANIFEST.json"
CHECKSUMS = ROOT / "CHECKSUMS.sha256"
FIXED_ZIP_TIME = (2026, 8, 5, 0, 0, 0)
EXCLUDED_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".sha256"}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def is_included(path: Path, include_integrity: bool = True) -> bool:
    rel = path.relative_to(ROOT)
    if any(part in EXCLUDED_DIRS for part in rel.parts):
        return False
    if path.suffix in EXCLUDED_SUFFIXES:
        return False
    if path.name in {".DS_Store"}:
        return False
    if not include_integrity and path in {MANIFEST, CHECKSUMS}:
        return False
    return path.is_file()


def files(include_integrity: bool = True) -> list[Path]:
    return sorted(
        (path for path in ROOT.rglob("*") if is_included(path, include_integrity)),
        key=lambda path: path.relative_to(ROOT).as_posix(),
    )


def write_integrity() -> dict[str, object]:
    payload_files = files(include_integrity=False)
    manifest = {
        "schema_version": "1.0",
        "bundle_id": "3RFC_Execution_Ready_Universe_Builder_20260805",
        "generated_utc": json.loads((ROOT / "BUNDLE_INFO.json").read_text(encoding="utf-8"))["created_utc"],
        "rule": "Integrity records exclude BUNDLE_MANIFEST.json and CHECKSUMS.sha256 to avoid self-reference.",
        "files": [
            {
                "path": path.relative_to(ROOT).as_posix(),
                "size_bytes": path.stat().st_size,
                "sha256": digest(path),
            }
            for path in payload_files
        ],
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    checksum_files = [path for path in files(include_integrity=True) if path != CHECKSUMS]
    CHECKSUMS.write_text(
        "".join(f"{digest(path)}  {path.relative_to(ROOT).as_posix()}\n" for path in checksum_files),
        encoding="utf-8",
    )
    return manifest


def write_zip(output: Path) -> str:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files(include_integrity=True):
            rel = path.relative_to(ROOT).as_posix()
            info = zipfile.ZipInfo(rel, date_time=FIXED_ZIP_TIME)
            mode = path.stat().st_mode
            perms = 0o755 if mode & stat.S_IXUSR else 0o644
            info.external_attr = (perms & 0xFFFF) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return digest(output)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional reproducible ZIP output path")
    args = parser.parse_args()
    manifest = write_integrity()
    print(f"integrity files: {len(manifest['files'])}")
    if args.output:
        sha = write_zip(args.output.resolve())
        sha_path = Path(str(args.output.resolve()) + ".sha256")
        sha_path.write_text(f"{sha}  {args.output.name}\n", encoding="utf-8")
        print(args.output.resolve())
        print(sha)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
