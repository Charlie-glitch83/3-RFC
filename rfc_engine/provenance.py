from __future__ import annotations
import hashlib, json
from pathlib import Path
from typing import Any


def canonical_json_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, obj: Any) -> str:
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding='utf-8')
    return sha256_file(path)


def tree_manifest(root: Path) -> dict[str, Any]:
    files=[]
    for p in sorted(root.rglob('*')):
        if p.is_file() and p.name not in {'MANIFEST.json'} and '__pycache__' not in p.parts:
            files.append({'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':sha256_file(p)})
    digest=sha256_bytes(canonical_json_bytes(files))
    return {'root':str(root),'sha256':digest,'files':files}
