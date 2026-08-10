#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
I_RUN = "I-180-20260810T134326Z"
G_RUN = "G-160-20260809T025252Z"
AUDIT_REL = "audit/G160_I_CHILD_INTERFACE_DEFECT_20260810.json"
CLAIM_ID = "G-165-ROUTE-RESOLVED-I-CHILD-REPAIR-FRONTIER"
MARKER = "## Superseding I-child interface repair"
NEW_G_BINDINGS = [
    "i_route_registry",
    "i_route_resolved_process_activity",
    "i_route_to_relational_ancestry",
    "i_aggregate_no_loss_reconstruction",
    "i_geometry_child_packet",
]
NEW_G_OUTPUT = "route-resolved G process activity and I geometry-ready ancestry packet"
NEW_G_GATES = [
    "I route registry completeness",
    "route-resolved process activity provenance",
    "process-to-B-edge ancestry completeness or certified complete branch family",
    "aggregate opacity no-loss reconstruction",
    "manufactured witnesses cannot promote physical execution",
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def save(rel: str, obj) -> None:
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha(rel: str) -> str:
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


def ensure(cond: bool, msg: str) -> None:
    if not cond:
        raise RuntimeError(msg)


def add_unique(seq: list, value) -> None:
    if value not in seq:
        seq.append(value)


def prepare() -> None:
    state = load("STATE.json")
    ensure(state.get("active_work_unit") == "I-180", "repair requires I-180 active")
    ensure(state.get("current_run") == I_RUN, "repair requires the live corrected I run")
    ensure(state["modules"]["G"]["evidence_state"] == "FROZEN", "G must still be frozen before supersession")
    ensure(state["modules"]["G"]["fidelity"] == "MINIMAL_SPINE", "expected historical G fidelity MINIMAL_SPINE")

    old_contract = load(f"modules/G/runs/{G_RUN}/OUTPUT_CONTRACT.json")
    old_primary = load(f"modules/G/runs/{G_RUN}/primary/G_RECOMBINATION_LAST_SCATTERING_MINIMAL_SPINE.json")
    old_derivation = load(f"modules/G/runs/{G_RUN}/FROZEN_DERIVATION_SPEC.json")
    old_bindings = load(f"modules/G/runs/{G_RUN}/binding_sheets/G_recombination_network.bindings.json")
    global_bindings = load("configured_runs/binding_sheets/G_recombination_network.bindings.json")
    blocked1 = (ROOT / "modules/G/runs/G-160-20260808T021341Z/CLOSEOUT.md").read_text(encoding="utf-8")
    blocked2 = (ROOT / "modules/G/runs/G-160-20260808T051613Z/CLOSEOUT.md").read_text(encoding="utf-8")

    hgi = next(x for x in old_contract["required_outputs"] if x["name"] == "H_G_to_I")
    params = next(x for x in old_bindings["bindings"] if x["path"] == "model.parameters")
    ensure(old_contract["status"] == "PASS" and hgi.get("child_ready") is True, "historical G did not claim child readiness as expected")
    ensure(params.get("value") == {"kf": 1.0, "kr": 1.0}, "historical manufactured fixed-rate witness changed")
    ensure("implementation witness only" in params.get("justification", ""), "historical binding is not explicitly implementation-only")
    ensure(all(x.get("value") is None for x in global_bindings.get("bindings", [])), "global G binding sheet is not clean/unbound")
    ensure(old_primary.get("classification") == "PHYSICALLY_EXECUTED_FINITE_RELATIONAL_BRANCH_FAMILY", "historical physical classification changed")
    ensure(old_derivation.get("branch_family", {}).get("nonuniqueness_policy"), "historical G did not retain unresolved branch policy")
    ensure("not a scientific failure of Module G" in blocked1, "first preserved G blocker no longer states source-repair scope")
    ensure("B -> C -> D -> E -> F -> G" in blocked2, "second preserved G blocker no longer locks replay order")

    audit = {
        "schema_version": "1.0",
        "timestamp_utc": now(),
        "classification": "UPSTREAM_INTERFACE_AND_EVIDENCE_STATE_DEFECT",
        "result": "REPAIR_REQUIRED_AT_G_BEFORE_I_CAN_PHYSICALLY_EXECUTE",
        "generation_mode": "GENERATION_SEALED",
        "earliest_direct_defect": "G-160-20260809T025252Z",
        "preserved_valid_upstream_scope": "B through F remain frozen at their currently stated scopes; F supplies the route/extinction law and G owns its route-resolved execution.",
        "evidence": [
            {"path": f"modules/G/runs/{G_RUN}/OUTPUT_CONTRACT.json", "sha256": sha(f"modules/G/runs/{G_RUN}/OUTPUT_CONTRACT.json"), "finding": "H_G_to_I was marked SATISFIED and child_ready without I-specific route-level bindings."},
            {"path": f"modules/G/runs/{G_RUN}/binding_sheets/G_recombination_network.bindings.json", "sha256": sha(f"modules/G/runs/{G_RUN}/binding_sheets/G_recombination_network.bindings.json"), "finding": "The executed numerical witness used kf=kr=1.0 and labels those values implementation witness only."},
            {"path": f"modules/G/runs/{G_RUN}/primary/G_RECOMBINATION_LAST_SCATTERING_MINIMAL_SPINE.json", "sha256": sha(f"modules/G/runs/{G_RUN}/primary/G_RECOMBINATION_LAST_SCATTERING_MINIMAL_SPINE.json"), "finding": "The historical primary promoted the unresolved lawful branch family to PHYSICALLY_EXECUTED."},
            {"path": "configured_runs/binding_sheets/G_recombination_network.bindings.json", "sha256": sha("configured_runs/binding_sheets/G_recombination_network.bindings.json"), "finding": "The canonical global binding sheet remains fully unbound, so the historical fixed witness is not inherited by a new run."},
            {"path": "modules/G/runs/G-160-20260808T021341Z/CLOSEOUT.md", "sha256": sha("modules/G/runs/G-160-20260808T021341Z/CLOSEOUT.md"), "finding": "The preserved earlier blocker explicitly rejected treating missing child-critical science as a failure of G."},
            {"path": "modules/G/runs/G-160-20260808T051613Z/CLOSEOUT.md", "sha256": sha("modules/G/runs/G-160-20260808T051613Z/CLOSEOUT.md"), "finding": "The preserved replay blocker required the ordered superseding B through F parent reconstruction before G execution."},
            {"path": "recovery/BG_SUPERSEDING_LINEAGE_PACKET.md", "sha256": sha("recovery/BG_SUPERSEDING_LINEAGE_PACKET.md"), "finding": "A missing child-critical field is defined as an upstream/interface defect; G may not invent it."},
        ],
        "diagnosis": {
            "triad_falsified": False,
            "I_law_falsified": False,
            "F_parent_replay_required_now": False,
            "G_superseding_replay_required": True,
            "HU_replay_required_after_G": True,
            "reason": "The current I blocker is caused by a historical G closure contract that accepted aggregate manufactured evidence as sufficient for the geometry child. The first direct repair point is G, not I and not the triad."
        },
        "required_G_to_I_contract": {
            "route_registry": "stable branch-specific material route identifiers with exact source ancestry",
            "route_resolved_process_activity": "Gamma_r^b(t) or an exact branch-indexed replacement derived from the frozen parent rather than a manufactured constant-rate witness",
            "route_to_relational_ancestry": "exact process-to-B relational ancestry witness or a complete constrained branch family with no arbitrary tie-break",
            "aggregate_no_loss_reconstruction": "route-resolved activities reconstruct the parent aggregate interaction/opacity source within frozen tolerance",
            "geometry_child_packet": "artifact-backed child interface carrying clock, branch identity, covariance/restart, route activity and relational ancestry together"
        },
        "claim_boundary": "This audit diagnoses repository/evidence-state damage. It does not itself derive the missing G route realization or physically execute I."
    }
    save(AUDIT_REL, audit)

    cfg = load("config/required_output_contracts.json")
    greqs = cfg["modules"]["G"]["required_child_bindings"]
    existing = {x["name"] for x in greqs}
    for name in NEW_G_BINDINGS:
        if name not in existing:
            greqs.append({"name": name, "allow_derived_absence": False})
    save("config/required_output_contracts.json", cfg)

    spec = load("modules/G/spec.json")
    add_unique(spec.setdefault("required_outputs", []), NEW_G_OUTPUT)
    for gate in NEW_G_GATES:
        add_unique(spec.setdefault("gates", []), gate)
    add_unique(spec.setdefault("forbidden_shortcuts", []), "using a manufactured or implementation-only rate witness as physical route activity")
    spec["claim_boundary"] = "Generated RFC recombination/visibility plus route-resolved geometry-child state; no external comparison or unresolved branch is promoted as a unique physical realization."
    save("modules/G/spec.json", spec)

    recipe = load("recipes/G/recipe.json")
    add_unique(recipe.setdefault("derive_exactly", []), "route-resolved material process activity required by I")
    add_unique(recipe.setdefault("derive_exactly", []), "ancestry-preserving process-to-B relational crosswalk or complete lawful branch family")
    add_unique(recipe.setdefault("derive_exactly", []), "no-loss reconstruction from route-resolved activity back to aggregate opacity source")
    add_unique(recipe.setdefault("required_outputs", []), NEW_G_OUTPUT)
    for gate in NEW_G_GATES:
        add_unique(recipe.setdefault("mandatory_gates", []), gate)
    for stop in [
        "a manufactured/reference rate is used as physical G route activity",
        "H_G_to_I lacks route-resolved process activity",
        "H_G_to_I lacks ancestry sufficient to construct the I process-to-edge branch family",
        "route-resolved activity fails to reconstruct the aggregate G interaction source",
    ]:
        add_unique(recipe.setdefault("hard_stop_conditions", []), stop)
    recipe["claim_boundary"] = spec["claim_boundary"]
    save("recipes/G/recipe.json", recipe)

    gates = load("recipes/G/gates.json")
    names = {x["gate"] for x in gates.get("componentwise", [])}
    for name in NEW_G_GATES:
        if name not in names:
            gates.setdefault("componentwise", []).append({"gate": name, "required": "PASS"})
    save("recipes/G/gates.json", gates)

    wo = ROOT / "recipes/G/WORK_ORDER.md"
    text = wo.read_text(encoding="utf-8")
    if MARKER not in text:
        text += f"\n\n{MARKER}\n\n"
        text += "The historical G MINIMAL_SPINE run is preserved but cannot satisfy the repaired geometry-child contract. Before any physical-execution promotion, derive and artifact-bind: (1) a stable route registry; (2) branch-specific route-resolved process activity; (3) exact ancestry to the inherited B relational carrier or a complete lawful incidence branch family; (4) a no-loss reconstruction to the aggregate interaction/opacity source; and (5) a geometry-ready G→I packet.\n\n"
        text += "The canonical G binding sheets begin unbound. Manufactured reference checks and implementation witnesses remain useful tests but are forbidden as physical binding sources. If the admitted parents do not uniquely select route coordinates, preserve the full lawful branch family; if they do not provide enough information to execute it, stop with an upstream obstruction rather than assigning constants.\n"
        wo.write_text(text, encoding="utf-8")

    claims = load("CLAIMS_LEDGER.json")
    old = next(x for x in claims["claims"] if x.get("claim_id") == "G-160-MINIMAL-SPINE-RECOMBINATION-SURFACE")
    old["supported"] = False
    old["current_authority"] = False
    old["supersession"] = {
        "reason": "The historical G run used implementation-only fixed-rate bindings while its closure contract marked H_G_to_I child-ready without route-resolved activity or geometry-child ancestry.",
        "audit": AUDIT_REL,
        "replacement_claim_id": CLAIM_ID,
        "historical_evidence_preserved": True,
    }
    if not any(x.get("claim_id") == CLAIM_ID for x in claims["claims"]):
        claims["claims"].append({
            "claim_id": CLAIM_ID,
            "text": "The current G repair frontier preserves the frozen F parent and requires a superseding G execution that derives route-resolved process activity and an ancestry-complete geometry-child interface before I can resume physical execution.",
            "owner": "G",
            "evidence_state": "DESIGN",
            "fidelity": "PRODUCTION",
            "supported": True,
            "current_authority": True,
            "evidence": [AUDIT_REL, "recovery/BG_SUPERSEDING_LINEAGE_PACKET.md", "configured_runs/binding_sheets/G_recombination_network.bindings.json"],
            "strongest_unsupported_claim": "No repaired G physical route realization, superseding HU transfer, or repaired I physical geometry is established yet.",
            "recorded_utc": now(),
            "work_unit": "G-165",
        })
    save("CLAIMS_LEDGER.json", claims)

    r = ROOT / "modules/I/runs" / I_RUN
    defect = {
        "schema_version": "1.0",
        "run_id": I_RUN,
        "classification": "UPSTREAM_INTERFACE_DEFECT",
        "result": "BLOCKED_UPSTREAM_G_REPAIR_REQUIRED",
        "audit": AUDIT_REL,
        "I_science_changed": False,
        "I_frozen_preexecution_law_preserved": True,
        "physical_execution_performed": False,
        "required_replay": "G-165 then HU superseding replay then resume I-180 from a fresh exact G parent",
    }
    (r / "UPSTREAM_INTERFACE_DEFECT.json").write_text(json.dumps(defect, indent=2) + "\n", encoding="utf-8")
    (r / "CLOSEOUT.md").write_text(
        "# I-180 Corrected Run Closeout\n\n"
        "## Result\n\nBLOCKED_UPSTREAM_INTERFACE_DEFECT before physical primary execution.\n\n"
        "The corrected I response-geometry law and exact Wolfram manufactured gates are preserved. Parent binding exposed a historical G closure defect: the frozen G interface was marked child-ready for I although the executed numerical bindings were explicitly implementation-only and the packet did not export route-resolved process activity plus ancestry sufficient for the corrected I law.\n\n"
        "This is not recorded as a failure of the triad or of the corrected I law. The run is closed without solver materialization and will be replayed after the superseding G and HU parent chain is frozen.\n\n"
        "## Strongest supported claim\n\nThe corrected I finite-relational response-geometry law is FORMALIZED and its physical execution is correctly blocked by an upstream G interface/evidence-state defect.\n\n"
        "## Strongest unsupported claim\n\nNo repaired I physical geometry, unique process-to-edge realization, or physically executed expansion background is established.\n",
        encoding="utf-8",
    )
    print(json.dumps({"result": "PREPARED", "audit": AUDIT_REL, "new_G_bindings": NEW_G_BINDINGS}, indent=2))


def module_item(item_id: str, title: str, module: str, status: str, depends_on: list[str], objective: str, commit_message: str, fidelity: str = "PRODUCTION") -> dict:
    return {
        "id": item_id,
        "title": title,
        "module": module,
        "status": status,
        "depends_on": depends_on,
        "objective": objective,
        "steps": [
            "Read the live module spec, recipe, work order, exact parents, derivation protocol, execution protocol, and the supersession audit named by this work unit.",
            "Create the governed run through repository tooling; do not reuse a historical run directory as current authority.",
            "Freeze exact sources, parents, branch variables, candidate classes, methods, tolerances, gates, falsifiers and claim boundary before primary execution.",
            "Derive missing science from admitted parents and triadic laws. Preserve complete branch families or obstruction; do not promote manufactured/reference values.",
            "Execute only parent-bound physical objects and run component gates, convergence, restart, replay, countermodels, ablations, covariance and independent reconstruction.",
            "Finalize manifests after outputs stop changing, close with evidence-matched claims, commit, verify and allow only the next direct repair child.",
        ],
        "deliverables": [
            f"modules/{module}/runs/<RUN_ID>/RUN_PLAN.md",
            f"modules/{module}/runs/<RUN_ID>/SOURCE_REGISTER.json",
            f"modules/{module}/runs/<RUN_ID>/GATE_RESULTS.json",
            f"modules/{module}/runs/<RUN_ID>/INDEPENDENT_VERIFICATION.md",
            f"modules/{module}/runs/<RUN_ID>/CLOSEOUT.md",
            "versioned frozen child interface and artifact registry entries",
        ],
        "gates": NEW_G_GATES if module == "G" else [
            "exact superseding G parent hash",
            "tangent/transfer reconstruction from repaired G without trusting historical HU summaries",
            "covariance, restart and clean replay",
            "no downstream I/J object imported into HU",
        ],
        "commit_message": commit_message,
        "required_evidence_state": "FROZEN",
        "required_fidelity": fidelity,
    }


def route() -> None:
    state = load("STATE.json")
    ensure(state.get("current_run") is None, "I run must be closed before rerouting")
    ensure(state.get("active_work_unit") == "I-180", "I-180 must remain active until reroute")
    ensure(state["modules"]["I"]["evidence_state"] == "FORMALIZED", "I must be FORMALIZED before reroute")

    q = load("WORK_QUEUE.json")
    items = q["items"]
    ensure(not any(x["id"] in {"G-165", "HU-175"} for x in items), "repair work units already exist")
    i_idx = next(i for i, x in enumerate(items) if x["id"] == "I-180")
    i_item = items[i_idx]
    i_item["status"] = "BLOCKED"
    i_item["depends_on"] = ["G-165", "HU-175"]
    i_item["required_fidelity"] = "PRODUCTION"

    g_item = module_item(
        "G-165",
        "Repair Module G: Route-Resolved Recombination State and Geometry-Child Interface",
        "G",
        "ACTIVE",
        ["G-160"],
        "Supersede the historical G MINIMAL_SPINE physical-execution overclaim by deriving/executing a parent-bound route-resolved recombination state and a no-loss, ancestry-complete G→I interface from exact H_F_to_G_v2.",
        "Repair G route-resolved state and geometry child interface",
    )
    hu_item = module_item(
        "HU-175",
        "Replay Module HU Against the Superseding G State",
        "HU",
        "BLOCKED",
        ["G-165"],
        "Reconstruct and freeze the universal linear tangent/transfer object against the superseding G route-resolved state so HI cannot consume a stale G-era HU parent.",
        "Replay HU against repaired G state",
    )
    items[i_idx:i_idx] = [g_item, hu_item]

    hi = next((x for x in items if x.get("id") == "HI-190"), None)
    if hi:
        deps = [d for d in hi.get("depends_on", []) if d != "HU-170"]
        if "HU-175" not in deps:
            deps.insert(0, "HU-175")
        hi["depends_on"] = deps

    save("WORK_QUEUE.json", q)

    state["active_work_unit"] = "G-165"
    state["current_module"] = "G"
    state["current_run"] = None
    state["project_status"] = "ACTIVE"
    state["last_updated_utc"] = now()
    state["strongest_supported_claim"] = "The corrected I law is FORMALIZED, and an exact audit has located the first direct blocking repository defect at historical G-160: its implementation-only recombination witness was promoted to physical execution and its G→I packet was marked child-ready without route-resolved process activity and geometry-child ancestry."
    state["strongest_unsupported_claim"] = "No superseding G physical route realization, replayed HU transfer, repaired I physical geometry, repaired HI state or J state is established yet."
    save("STATE.json", state)

    frontier = load("audit/PHYSICAL_FRONTIER_CURRENT.json")
    frontier.update({
        "schema_version": frontier.get("schema_version", "1.0"),
        "status": "CURRENT_SCIENTIFIC_FRONTIER",
        "timestamp_utc": now(),
        "active_work_unit": "G-165",
        "current_module": "G",
        "current_run": None,
        "active_queue_items": ["G-165"],
        "last_valid_frozen_parent_chain": "A through F at current frozen scopes; historical G/HU are preserved but superseded for the repaired I lineage.",
        "frontier_reason": "Historical G-160 passed a weak HU/I child contract using implementation-only recombination bindings. G must be replayed at higher fidelity with route-resolved process activity and I ancestry before HU and I resume.",
        "supersession_audit": AUDIT_REL,
        "downstream_status": {
            "HU": "BLOCKED_PENDING_SUPERSEDING_G_REPLAY",
            "I": "FORMALIZED_BLOCKED_PENDING_G_AND_HU_REPAIR",
            "HI": "BLOCKED_PENDING_REPAIRED_G_HU_I",
            "J": "BLOCKED_PENDING_REPAIRED_HI",
        },
    })
    save("audit/PHYSICAL_FRONTIER_CURRENT.json", frontier)

    with (ROOT / "memory/FAILURE_LOG.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps({
            "failure_id": "G160-I-CHILD-INTERFACE-DEFECT-20260810",
            "run_id": G_RUN,
            "gate": "G_TO_I_CHILD_READINESS",
            "category": "EVIDENCE_STATE_AND_INTERFACE_DEFECT",
            "description": "Historical G-160 promoted implementation-only fixed-rate recombination evidence to PHYSICALLY_EXECUTED and marked H_G_to_I child-ready without route-resolved process activity or geometry-child ancestry.",
            "earliest_affected_object": "modules/G/frozen/H_G_to_I.json",
            "changes_frozen_science": False,
            "required_replay_scope": "G-165 -> HU-175 -> I-180",
            "strongest_claim_remaining": state["strongest_supported_claim"],
            "timestamp_utc": now(),
        }, ensure_ascii=False) + "\n")
    with (ROOT / "memory/DECISION_LOG.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps({
            "decision_id": "REROUTE-I180-TO-G165-20260810",
            "timestamp_utc": now(),
            "work_unit": "G-165",
            "decision": "Preserved the corrected I run at FORMALIZED scope and rerouted the active frontier to a superseding G replay, followed by HU replay, because the historical G→I child contract and physical-execution promotion were defective.",
            "basis": [AUDIT_REL, "recovery/BG_SUPERSEDING_LINEAGE_PACKET.md"],
            "alternatives_rejected": ["treat the missing I binding as a triad failure", "invent route activity in I", "reuse kf=kr=1 implementation witness as physical data", "overwrite historical G evidence"],
            "changes_science": False,
            "required_replay": "G-165 -> HU-175 -> I-180",
            "commit_sha": state.get("last_verified_commit") or "",
        }, ensure_ascii=False) + "\n")
    print(json.dumps({"result": "ROUTED", "active_work_unit": "G-165", "next_after_G": "HU-175", "then": "I-180"}, indent=2))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("phase", choices=["prepare", "route"])
    args = ap.parse_args()
    if args.phase == "prepare":
        prepare()
    else:
        route()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
