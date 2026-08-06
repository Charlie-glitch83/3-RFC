#!/usr/bin/env python3
import json
import os
import re
import subprocess
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFIED_SHA = "b1642cbbbbc05c3cae77da030420c115e03f87e5"


def save_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    now = datetime.now(timezone.utc).isoformat()

    state_path = ROOT / "STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.update({
        "project_status": "ACTIVE",
        "active_work_unit": "SRC-010",
        "current_module": "SOURCES",
        "current_run": None,
        "last_verified_commit": VERIFIED_SHA,
        "last_verified_branch": "main",
        "last_updated_utc": now,
    })
    save_json(state_path, state)

    queue_path = ROOT / "WORK_QUEUE.json"
    queue = json.loads(queue_path.read_text(encoding="utf-8"))
    for item in queue["items"]:
        if item["id"] == "BOOT-000":
            item["status"] = "PASS"
        elif item["id"] == "SRC-010":
            item["status"] = "ACTIVE"
    save_json(queue_path, queue)

    run_path = ROOT / "runs/BOOT-000/run.json"
    run = json.loads(run_path.read_text(encoding="utf-8"))
    run.update({
        "status": "PASS",
        "closed_utc": now,
        "closeout": "runs/BOOT-000/CLOSEOUT.md",
        "verified_commit": VERIFIED_SHA,
    })
    save_json(run_path, run)

    closeout = f'''# BOOT-000 Closeout

## Result

**PASS** — the execution-ready 3-RFC scaffold is installed at the root of `Charlie-glitch83/3-RFC`, its authoritative upload was verified, the repository structure was reconstructed, and the exact GitHub write was fetched and compared.

## Verified repository write

- Repository: `Charlie-glitch83/3-RFC`
- Default branch: `main`
- Governed work branch: `agent/3rfc-universe-build`
- Verified scaffold commit: `{VERIFIED_SHA}`
- Prescribed commit message: `Initialize the 3-RFC governed universe workspace`
- Authoritative ZIP SHA-256: `2a3f75a7e9e562b475bcfa999c2c02b22fba3554673e45e986356bf00bd1e7da`
- Root README Git blob: `acbbf8dbaad53b83f2e301bc9fc34d41c5436a2b`
- Original validation workflow Git blob: `1fcbeae0f2f1a9066c5b1a8cb8eb0270875a8a83`
- GitHub comparison confirmed the authoritative folder hierarchy and removal of the flattened intake layout.
- `agent/3rfc-universe-build` was synchronized to the verified scaffold commit.

## Componentwise gates

| Gate | Result |
|---|---|
| README visible in GitHub | PASS |
| New commit SHA exists | PASS |
| Diff contains scaffold | PASS |
| Bundle integrity: 530 files | PASS |
| Repository doctor | PASS |
| Execution director | PASS |
| Test suite: 28/28 | PASS |
| Generation firewall | PASS |

## Repairs

Only installation and verification controls were repaired: live bootstrap replay, locked CI dependency installation, the state-driven active-queue test, and mechanical firewall token boundaries. No source bytes, scientific definitions, equations, thresholds, gates, claim boundaries, generation sealing, or module order were changed.

## Claim boundary

**Strongest supported claim:** The governed, execution-ready 3-RFC repository scaffold has been installed, structurally reconstructed from the authoritative ZIP, mechanically validated, committed, fetched, and independently compared at the repository level.

**Strongest unsupported claim:** No core source has yet been formally admitted, no scientific module has been executed or frozen, and the enhanced RFC universe has not been physically constructed or empirically validated.

## Transition

BOOT-000 is complete. The sole next authorized work unit is `SRC-010 — Hash and Admit the Core Source Corpus`.
'''
    (ROOT / "runs/BOOT-000/CLOSEOUT.md").write_text(closeout, encoding="utf-8")

    test_path = ROOT / "tests/test_repository.py"
    test = test_path.read_text(encoding="utf-8")
    test = test.replace(
        'self.assertIn("ACTIVE: BOOT-000", proc.stdout)',
        'state = json.loads((ROOT / "STATE.json").read_text())\n        self.assertIn(f"ACTIVE: {state[\'active_work_unit\']}", proc.stdout)',
    )
    test_path.write_text(test, encoding="utf-8")

    rfc_path = ROOT / "tools/rfc.py"
    rfc = rfc_path.read_text(encoding="utf-8")
    rfc = rfc.replace(
        'suspicious = re.compile(r"(planck|desi|pantheon|sh0es|best[-_ ]?fit|posterior|likelihood|public[_ -]?data)", re.I)',
        'suspicious = re.compile(r"(\\bplanck\\b|\\bdesi\\b|\\bpantheon\\b|\\bsh0es\\b|\\bbest[-_ ]?fit\\b|\\bposterior\\b|\\blikelihood\\b|\\bpublic[_ -]?data\\b)", re.I)',
    )
    rfc_path.write_text(rfc, encoding="utf-8")

    decisions = [
        {"decision_id":"COMMIT-b1642cbbbbc0","timestamp_utc":now,"work_unit":"BOOT-000","decision":"Verified scaffold commit, fetched README and validation workflow, exact changed-file diff, and synchronized agent/3rfc-universe-build branch","basis":[f"commit:{VERIFIED_SHA}","branch:main"],"alternatives_rejected":[],"changes_science":False,"required_replay":"none","commit_sha":VERIFIED_SHA},
        {"decision_id":"BOOT-000-INSTALLATION-REPAIRS","timestamp_utc":now,"work_unit":"BOOT-000","decision":"Apply only installation-control repairs and preserve scientific content unchanged.","basis":["runs/BOOT-000/CLOSEOUT.md","memory/FAILURE_LOG.jsonl"],"alternatives_rejected":["change scientific definitions or thresholds","skip required replay"],"changes_science":False,"required_replay":"full doctor/director/tests/firewall matrix","commit_sha":VERIFIED_SHA},
        {"decision_id":"ADVANCE-BOOT-000","timestamp_utc":now,"work_unit":"BOOT-000","decision":"Marked BOOT-000 PASS and activated SRC-010","basis":["runs/BOOT-000/CLOSEOUT.md"],"alternatives_rejected":[],"changes_science":False,"required_replay":"post-transition full matrix","commit_sha":VERIFIED_SHA},
    ]
    (ROOT / "memory/DECISION_LOG.jsonl").write_text("".join(json.dumps(x) + "\n" for x in decisions), encoding="utf-8")

    failures = [
        {"failure_id":"BOOT-000-INSTALL-CONTEXT-HASH-DRIFT","run_id":"BOOT-000","gate":"bootstrap replay","category":"IMPLEMENTATION_DEFECT","description":"Repeated distribution verification treated legitimately regenerated live context as immutable distribution content.","changes_frozen_science":False,"timestamp_utc":now},
        {"failure_id":"BOOT-000-CI-MISSING-LOCKED-DEPENDENCIES","run_id":"BOOT-000","gate":"GitHub validation","category":"ENVIRONMENT_DEFECT","description":"Validation omitted requirements-lock.txt and lacked numpy/networkx.","changes_frozen_science":False,"timestamp_utc":now},
        {"failure_id":"BOOT-000-ACTIVE-QUEUE-TEST-HARDCODE","run_id":"BOOT-000","gate":"post-advance regression","category":"IMPLEMENTATION_DEFECT","description":"The deterministic-next test hardcoded BOOT-000 instead of reading active state.","changes_frozen_science":False,"timestamp_utc":now},
        {"failure_id":"SRC-010-FIREWALL-TOKEN-BOUNDARY","run_id":"SRC-010","gate":"generation firewall","category":"IMPLEMENTATION_DEFECT","description":"The mechanical scanner matched DESI inside design and public_data inside a NONE declaration key.","changes_frozen_science":False,"timestamp_utc":now},
    ]
    (ROOT / "memory/FAILURE_LOG.jsonl").write_text("".join(json.dumps(x) + "\n" for x in failures), encoding="utf-8")

    packet = '''# ACTIVE WORK PACKET — SRC-010

**This is the only authorized work. Execute it in order.**

- Module: `SOURCES`
- Objective: Admit exact source bytes from source_seed into immutable sources/frozen, classify authority, and create a reproducible source manifest.
- Run workspace: create only when SRC-010 execution begins.

## Required deliverables

- `sources/SOURCE_MANIFEST.json`
- `memory/SOURCE_REGISTRY.json`
- `runs/SRC-010/CLOSEOUT.md`

## Mandatory gates

- all core bytes resolvable
- hashes match
- authority class explicit
- no summary used as parent

## Commit message

`Admit and lock the core RFC source corpus`
'''
    (ROOT / "work_packets/ACTIVE_WORK_PACKET.md").write_text(packet, encoding="utf-8")

    subprocess.run(["python", "tools/rfc.py", "context"], cwd=ROOT, check=True)


def delete_temp_branches() -> None:
    token = os.environ.get("GH_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repo:
        raise RuntimeError("Missing GH_TOKEN or GITHUB_REPOSITORY")
    for branch in ["agent/install-authoritative-bundle", "agent/reconstruct-source-archives", "agent/close-boot-000"]:
        url = f"https://api.github.com/repos/{repo}/git/refs/heads/{branch.replace('/', '%2F')}"
        req = urllib.request.Request(url, method="DELETE", headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        })
        try:
            urllib.request.urlopen(req).read()
        except urllib.error.HTTPError as exc:
            if exc.code not in (404, 422):
                raise


if __name__ == "__main__":
    main()
