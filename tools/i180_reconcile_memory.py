#!/usr/bin/env python3
"""Reconcile machine/human memory after the governed I-180 scientific supersession."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = "audit/I180_SCIENTIFIC_SUPERSESSION_20260810.json"
SPEC = "modules/I/repair/I180_CORRECTED_DERIVATION_SPEC.json"
VERIFY = "modules/I/repair/REPAIR_VERIFICATION.json"


def now():
    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, obj):
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def reconcile_claims():
    p = ROOT / "CLAIMS_LEDGER.json"
    data = json.loads(p.read_text())
    for c in data.get("claims", []):
        if c.get("claim_id") == "I-180-FINITE-RELATIONAL-BACKGROUND":
            # Preserve the evidence state that the historical run actually reached;
            # supersession changes present authority, not the historical evidence record.
            c["supported"] = False
            c["current_authority"] = False
            c["supersession"] = {
                "reason": "Pre-execution uniqueness/branch-completeness was not established and numerical physical-background evidence was implementation-only.",
                "audit": AUDIT,
                "replacement_claim_id": "I-180-CORRECTED-RESPONSE-GEOMETRY-FRONTIER"
            }
    replacement = {
        "claim_id": "I-180-CORRECTED-RESPONSE-GEOMETRY-FRONTIER",
        "text": "At the repaired Module-I frontier, exact G/B ancestry supports a corrected finite-relational response-geometry candidate law family: the weighted Dirichlet/Laplacian operator on the constant-mode quotient is retained as the primary geometry state; its Green response yields a lossless effective-resistance readout; its nonzero spectrum yields principal response lengths and a derived volumetric geometric-mean scale while retaining anisotropy and unresolved lawful branch coordinates.",
        "owner": "I",
        "evidence_state": "DESIGN",
        "fidelity": "UNSTARTED",
        "supported": True,
        "current_authority": True,
        "evidence": [SPEC, VERIFY, AUDIT],
        "strongest_unsupported_claim": "No unique process-to-edge realization, unique continuum/SI spacetime metric, unique scalar expansion history on nonhomothetic branches, physical H(z), empirical cosmology, or physically executed I branch is established until exact parent bindings and branch witnesses close the remaining I frontier.",
        "recorded_utc": now(),
        "work_unit": "I-180",
        "authority_scope": "CORRECTED_PRE_EXECUTION_DERIVATION_ONLY"
    }
    claims = data.setdefault("claims", [])
    if not any(c.get("claim_id") == replacement["claim_id"] for c in claims):
        claims.append(replacement)
    else:
        for i, c in enumerate(claims):
            if c.get("claim_id") == replacement["claim_id"]:
                claims[i] = replacement
    write_json(p, data)


def append_jsonl(path: Path, entry, key: str, value: str):
    existing = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    for line in existing:
        try:
            if json.loads(line).get(key) == value:
                return
        except Exception:
            pass
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def reconcile_logs():
    append_jsonl(
        ROOT / "memory" / "DECISION_LOG.jsonl",
        {
            "decision_id": "RESET-I-180-SCIENTIFIC-FRONTIER-20260810",
            "timestamp_utc": now(),
            "work_unit": "I-180",
            "decision": "Supersede I-180/HI-190/J current authority and restore I-180 as the sole active frontier while preserving historical evidence in git.",
            "reason": "I-180 overclaimed metric/scale uniqueness and physical execution; repaired derivation preserves the full response operator, lawful branch multiplicity, anisotropy, and exact-parent execution gate.",
            "evidence": [AUDIT, SPEC, VERIFY]
        },
        "decision_id", "RESET-I-180-SCIENTIFIC-FRONTIER-20260810"
    )
    append_jsonl(
        ROOT / "memory" / "FAILURE_LOG.jsonl",
        {
            "failure_id": "I-180-PREMATURE-GEOMETRY-UNIQUENESS-AND-PHYSICAL-PROMOTION-20260810",
            "timestamp_utc": now(),
            "work_unit": "I-180",
            "category": "SCIENTIFIC_DERIVATION_AND_EVIDENCE_STATE_OVERCLAIM",
            "description": "The prior I-180 froze effective resistance and a pseudodeterminant scalar summary without proving universal metric/scale uniqueness or complete functional branching, and promoted implementation-only numerical background evidence through PHYSICALLY_EXECUTED.",
            "repair_scope": "Reset current authority to I; retain weighted response operator as primary geometry; reclassify resistance as a lossless response readout and pdet as volumetric summary; keep physical execution blocked until exact G/B branch binding.",
            "evidence": [AUDIT, SPEC, VERIFY]
        },
        "failure_id", "I-180-PREMATURE-GEOMETRY-UNIQUENESS-AND-PHYSICAL-PROMOTION-20260810"
    )


def write_frontier():
    state = json.loads((ROOT / "STATE.json").read_text())
    queue = json.loads((ROOT / "WORK_QUEUE.json").read_text())
    active = [x for x in queue.get("items", []) if x.get("status") == "ACTIVE"]
    out = {
        "schema_version": "1.0",
        "status": "CURRENT_SCIENTIFIC_FRONTIER",
        "timestamp_utc": now(),
        "active_work_unit": state.get("active_work_unit"),
        "current_module": state.get("current_module"),
        "current_run": state.get("current_run"),
        "active_queue_items": [x.get("id") for x in active],
        "last_valid_frozen_parent_chain": "A through HU at their existing verified/frozen scopes",
        "frontier_reason": "Module I requires corrected branch-complete geometry/expansion derivation and exact-parent physical binding before HI/J can resume.",
        "supersession_audit": AUDIT,
        "corrected_derivation": SPEC,
        "semantic_verification": VERIFY,
        "downstream_status": {"HI": "BLOCKED_PENDING_REPAIRED_I", "J": "BLOCKED_PENDING_REPAIRED_I_AND_HI_REPLAY"}
    }
    write_json(ROOT / "audit" / "PHYSICAL_FRONTIER_CURRENT.json", out)


def write_context():
    state = json.loads((ROOT / "STATE.json").read_text())
    queue = json.loads((ROOT / "WORK_QUEUE.json").read_text())
    active = next(x for x in queue.get("items", []) if x.get("status") == "ACTIVE")
    mods = state.get("modules", {})
    lines = [
        "# Current Context", "", f"Generated: {now()}", "", "## Project truth", "",
        f"- Status: `{state.get('project_status')}`",
        f"- Generation mode: `{state.get('generation_mode')}`",
        f"- Active work unit: `{state.get('active_work_unit')}` — {active.get('title')}",
        f"- Current module: `{state.get('current_module')}`",
        "- Scientific authority: A through HU remain frozen at their verified scopes; I is the sole active frontier.",
        "", "## Strongest supported claim", "",
        "The corrected pre-execution I derivation preserves the full gauge-reduced weighted response operator, treats effective resistance only as a lossless Green-response readout, treats the pseudodeterminant expression only as a volumetric geometric-mean response scale, retains anisotropic principal response lengths/rates, and preserves unresolved lawful branch coordinates instead of selecting them arbitrarily.",
        "", "## Strongest unsupported claim", "",
        "No physically executed repaired I branch, unique process-to-edge realization, unique continuum/SI spacetime metric, unique scalar expansion history on nonhomothetic branches, physical H(z), empirical agreement, repaired HI instantiation, or J covariance/spectrum state is currently established.",
        "", "## Immediate objective", "", active.get("objective", "Close the repaired Module I scientific frontier."),
        "", "## Mandatory repair gates", "",
        "- Derive or preserve the complete ancestry-compatible process-to-edge branch family.",
        "- Bind actual parent-generated G event/process objects; manufactured ODEs are implementation tests only.",
        "- Retain full response spectrum unless homothety/isotropy is internally proved.",
        "- Do not promote I to PHYSICALLY_EXECUTED without actual parent-bound execution.",
        "- Keep HI and J blocked until repaired I is frozen and HI is replayed.",
        "", "## Module states", ""
    ]
    for name in ("A","B","C","D","E","F","G","HU","I","HI","J","K","L","M","KLM","N","O","P","Q"):
        m = mods.get(name, {})
        lines.append(f"- {name}: `{m.get('evidence_state','?')}` / `{m.get('fidelity','?')}`")
    lines += ["", "## Repair evidence", "", f"- `{AUDIT}`", f"- `{SPEC}`", f"- `{VERIFY}`", "", "## Resume commands", "", "```bash", "python tools/rfc.py doctor", "python tools/rfc.py next", "```", ""]
    (ROOT / "memory" / "CURRENT_CONTEXT.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    reconcile_claims()
    reconcile_logs()
    write_frontier()
    write_context()


if __name__ == "__main__":
    main()
