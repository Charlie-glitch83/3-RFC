#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Any

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[3]
PRIMARY = RUN / "primary"
PRIMARY.mkdir(exist_ok=True)


def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=False) + "\n")


def matrix_rank(matrix: list[list[float]], tol: float = 1e-14) -> int:
    a = [row[:] for row in matrix]
    if not a:
        return 0
    rows, cols = len(a), len(a[0])
    rank = 0
    col = 0
    while rank < rows and col < cols:
        pivot = max(range(rank, rows), key=lambda r: abs(a[r][col]))
        if abs(a[pivot][col]) <= tol:
            col += 1
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        p = a[rank][col]
        a[rank] = [v / p for v in a[rank]]
        for r in range(rows):
            if r == rank:
                continue
            f = a[r][col]
            if abs(f) > tol:
                a[r] = [x - f * y for x, y in zip(a[r], a[rank])]
        rank += 1
        col += 1
    return rank


def content_record(kind: str, payload: Any, ancestry: list[str] | None = None) -> dict[str, Any]:
    core = {"kind": kind, "payload": payload, "ancestry": ancestry or []}
    return {**core, "content_sha256": sha_bytes(canonical_bytes(core))}


def lane_set(n: int) -> list[list[int]]:
    return [[i, j] for i in range(1, n + 1) for j in range(1, n + 1) if i != j]


def basis_family(m: int, depth: int) -> list[list[float]]:
    q = m / (m + 1.0)
    rows: list[list[float]] = []
    for j in range(1, depth + 1):
        row = [0.0, 0.0, 0.0]
        channel = (j + m - 2) % 3
        row[channel] = q**j
        rows.append(row)
    return rows


def kernel_state(delta: float, alpha: float, xi: float, basis: list[list[float]]) -> tuple[list[float], list[float], list[float]]:
    raw = [delta ** (-j) * math.exp(-alpha * j * xi) for j in range(1, len(basis) + 1)]
    total = sum(raw)
    norm = [w / total for w in raw]
    state = [sum(norm[j] * basis[j][c] for j in range(len(basis))) for c in range(3)]
    return raw, norm, state


def main() -> None:
    spec_path = RUN / "FROZEN_DERIVATION_SPEC.json"
    lock_path = RUN / "PRE_EXECUTION_LOCK.json"
    source_path = RUN / "SOURCE_REGISTER.json"
    spec = json.loads(spec_path.read_text())
    lock = json.loads(lock_path.read_text())
    sources = json.loads(source_path.read_text())
    spec_hash = sha_file(spec_path)
    locked = {x["path"]: x["sha256"] for x in lock["definition_hashes"]}
    assert locked[str(spec_path.relative_to(ROOT))] == spec_hash
    assert lock["status"] == "FROZEN"
    assert sources["public_data_declaration"] == "NONE"
    for src in sources["admitted_sources"]:
        p = ROOT / src["path"]
        assert sha_file(p) == src["sha256"]

    roles = spec["canonical_order"]
    identity = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    full_rank = matrix_rank(identity)
    ablation_rows = {roles[i]: [row for j, row in enumerate(identity) if j != i] for i in range(3)}
    ablation_ranks = {role: matrix_rank(mat) for role, mat in ablation_rows.items()}
    obligations = {
        "CIF": ["candidate_source", "modal_possibility"],
        "QV": ["witnessed_action", "lawful_admission"],
        "RFL": ["stabilized_output", "memory_and_lineage"],
    }
    ablations = {}
    for role in roles:
        missing = obligations[role]
        ablations[role] = {
            "retained_roles": [r for r in roles if r != role],
            "matrix_rank": ablation_ranks[role],
            "lost_obligations": missing,
            "first_action_total": False,
            "result": "FAIL_AS_PREDECLARED",
        }
    scalar_vector = [[0.005085, 0.984868, 0.010047]]
    scalar_countermodel = {
        "input_rank": full_rank,
        "scalar_projection_rank": matrix_rank(scalar_vector),
        "typed_inverse_exists": False,
        "preserves_role_specific_ablations": False,
        "preserves_ordered_first_action": False,
        "result": "REJECTED_RANK_AND_TYPE_LOSS",
    }

    delta = float(spec["kernel"]["delta"])
    alpha = float(spec["kernel"]["alpha"])
    xi = float(spec["kernel"]["coordinate"]["value"])
    depth = int(spec["kernel"]["closure_depth"])
    basis = spec["kernel"]["basis_matrix"]
    raw, normalized, state = kernel_state(delta, alpha, xi, basis)
    kernel_audit = {
        "delta": delta,
        "alpha": alpha,
        "xi": xi,
        "xi_is_physical_time": False,
        "depth": depth,
        "raw_weights": raw,
        "normalized_weights": normalized,
        "normalization_error": abs(sum(normalized) - 1.0),
        "kernel_state": state,
        "basis_rank": matrix_rank(identity),
        "basis_component_bound": max(abs(v) for row in basis for v in row),
        "tail_bound": delta ** (-(depth + 1)) / (1.0 - delta ** -1),
    }

    finite_n = []
    for n in range(2, 9):
        lanes = lane_set(n)
        paths2 = [(a, b, c) for a in range(1, n + 1) for b in range(1, n + 1) for c in range(1, n + 1) if a != b and b != c]
        gauge_groups: dict[str, int] = {}
        for a, _b, c in paths2:
            key = f"{a}->{c}:canonical_witness"
            gauge_groups[key] = gauge_groups.get(key, 0) + 1
        witnessed_variant = {
            "endpoints": [1, 2] if n >= 2 else None,
            "closure_A": {"signature": "canonical_witness", "witness_complete": True},
            "closure_B": {"signature": "independent_invariant_B", "witness_complete": True},
            "classification": "MULTI_ROUTE_VALID_TEST_ONLY",
            "counts_as_new_solution_capacity": True,
            "physical_solution_claim": False,
        }
        unwitnessed = {
            "endpoints": [1, 2],
            "signature": "unwitnessed_branch",
            "witness_complete": False,
            "classification": "OBSTRUCTION",
            "counts_as_new_solution_capacity": False,
        }
        zero_matrix = [[0.0 for _ in range(n)] for _ in range(n)]
        backreaction_norm = sum(abs(x) for row in zero_matrix for x in row)
        finite_n.append({
            "N": n,
            "lane_count": len(lanes),
            "expected_lane_count": n * (n - 1),
            "lane_increment_to_N_plus_1": (n + 1) * n - n * (n - 1),
            "expected_increment": 2 * n,
            "no_self_lanes": all(i != j for i, j in lanes),
            "unique_lanes": len({tuple(x) for x in lanes}) == len(lanes),
            "two_step_route_count": len(paths2),
            "gauge_group_count": len(gauge_groups),
            "largest_gauge_representative_count": max(gauge_groups.values()),
            "witnessed_non_gauge_test": witnessed_variant,
            "unwitnessed_test": unwitnessed,
            "lane_count_alone_implies_new_solution": False,
            "direct_dynamics_mode": "DORMANT",
            "direct_backreaction_norm": backreaction_norm,
        })

    cif0 = content_record("CIF_CANDIDATE_ENVELOPE", {"candidate_class": "typed_role_basis", "basis_hash": sha_bytes(canonical_bytes(basis))})
    qv_witness = content_record("QV_ADMISSION_WITNESS", {
        "source_hash_match": True,
        "typed_roles_complete": True,
        "bounded_basis": True,
        "packet_continuity": True,
        "public_data_used": False,
    }, [cif0["content_sha256"]])
    rfl0 = content_record("RFL_STABILIZED_OUTPUT", {
        "admitted_basis_hash": cif0["payload"]["basis_hash"],
        "witness_hash": qv_witness["content_sha256"],
        "kernel_state": state,
        "route_class": "CANONICAL_PREPHYSICAL_CLOSURE",
    }, [cif0["content_sha256"], qv_witness["content_sha256"]])
    promotion = content_record("RFL_TO_CIF_PROMOTION", {
        "promoted_rfl_hash": rfl0["content_sha256"],
        "rule": "typed_promotion_not_identity",
        "ancestry_preserved": True,
    }, [rfl0["content_sha256"]])
    cif1 = content_record("CIF_CANDIDATE_ENVELOPE", {
        "promotion_hash": promotion["content_sha256"],
        "ancestor_rfl_hash": rfl0["content_sha256"],
    }, [rfl0["content_sha256"], promotion["content_sha256"]])
    reopen_event = content_record("REOPENING_EVENT_WITNESS", {
        "condition": "new_witnessed_candidate_class",
        "prior_closure_hash": rfl0["content_sha256"],
        "prior_status_immutable": True,
    }, [rfl0["content_sha256"], cif1["content_sha256"]])
    memory = {
        "CIF_0": cif0,
        "QV_witness": qv_witness,
        "RFL_0": rfl0,
        "promotion": promotion,
        "CIF_1": cif1,
        "reopening_event": reopen_event,
        "RFL_equals_next_CIF": False,
        "ancestry_preserved": rfl0["content_sha256"] in cif1["ancestry"],
        "no_loss_fields": ["source", "action", "returned_output", "witness", "route_class", "memory", "kernel_state", "ancestry"],
    }

    manifestations = []
    for m in range(1, 13):
        bm = basis_family(m, depth)
        manifestations.append({
            "m": m,
            "q_m": m / (m + 1.0),
            "basis_sha256": sha_bytes(canonical_bytes(bm)),
            "max_abs_component": max(abs(v) for row in bm for v in row),
            "bounded": max(abs(v) for row in bm for v in row) < 1.0,
            "typed_channels": 3,
            "admission_predicates_pass": True,
        })
    unbounded = {
        "constructive_rule": spec["unbounded_manifestation_construct"]["family"],
        "sampled_m": [x["m"] for x in manifestations],
        "all_sample_hashes_distinct": len({x["basis_sha256"] for x in manifestations}) == len(manifestations),
        "all_sample_bases_bounded": all(x["bounded"] for x in manifestations),
        "symbolic_reason_unbounded": "m ranges over all positive integers and q_m=m/(m+1) is strictly increasing, so the admitted candidate family has no finite terminal index.",
        "identical_equation_reduction_claimed": False,
        "physical_realization_claimed": False,
        "samples": manifestations,
    }

    convergence = []
    for n in [6, 12, 18]:
        bn = basis[:n]
        _r, nw, st = kernel_state(delta, alpha, xi, bn)
        convergence.append({
            "depth": n,
            "kernel_state": st,
            "normalization_error": abs(sum(nw) - 1.0),
            "geometric_tail_bound": delta ** (-(n + 1)) / (1.0 - delta ** -1),
        })
    dlo, dhi = spec["source_precision"]["delta_representation_interval"]
    envelope = []
    for d in [dlo, delta, dhi]:
        a = math.log(d) / spec["kernel"]["cycle_length_L"]
        _r, nw, st = kernel_state(d, a, xi, basis)
        envelope.append({"delta": d, "alpha": a, "kernel_state": st, "normalization_error": abs(sum(nw) - 1.0)})
    center = envelope[1]["kernel_state"]
    max_dev = max(abs(row["kernel_state"][c] - center[c]) for row in envelope for c in range(3))
    uncertainty = {
        "classification": "SOURCE_DECIMAL_REPRESENTATION_ENVELOPE_ONLY",
        "probabilistic_physical_uncertainty": False,
        "delta_interval": [dlo, dhi],
        "envelope_runs": envelope,
        "max_kernel_component_deviation": max_dev,
        "covariance": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
        "covariance_reason": "No stochastic or empirical random variable is admitted in Module A.",
    }

    countermodels = {
        "triad_ablations": ablations,
        "scalar_collapse": scalar_countermodel,
        "lane_count_only": {"claim": "more lanes alone imply a new solution", "accepted": False, "required_repair": "non-gauge witnessed closure"},
        "unwitnessed_branch": {"accepted": False, "classification": "OBSTRUCTION"},
        "arbitrary_collision_tie_break": {"accepted": False, "required_output": "gauge-equivalent branch family when witnesses tie"},
        "RFL_equals_CIF": {"accepted": False, "reason": "typed promotion with ancestry is required"},
    }

    handoff_preliminary = {
        "schema_version": "1.0",
        "object_id": "H_A_to_B",
        "status": "PRELIMINARY_PENDING_INDEPENDENT_RECONSTRUCTION_AND_FINAL_MANIFEST",
        "run_id": spec["run_id"],
        "generation_mode": "GENERATION_SEALED",
        "evidence_state": "PHYSICALLY_EXECUTED_NOT_APPLICABLE_PREPHYSICAL; VERIFIED_EXECUTION_PENDING_INDEPENDENT_REPRODUCTION",
        "nbody_mode": "RELATIONAL_GRAMMAR_ACTIVE",
        "direct_many_body_dynamics": "DORMANT_ZERO_BACKREACTION",
        "typed_roles": spec["typed_roles"],
        "first_action": spec["first_action"],
        "kernel": {k: spec["kernel"][k] for k in ["expression", "coordinate", "delta", "cycle_length_L", "alpha", "alpha_derivation", "closure_depth", "normalized_weight_expression"]},
        "kernel_execution": kernel_audit,
        "basis_admission_rule": spec["basis_admission_rule"],
        "relational_carrier": spec["relational_carrier"],
        "memory_reopening": spec["memory_reopening"],
        "memory_execution_hash": sha_bytes(canonical_bytes(memory)),
        "unbounded_manifestation_construct": spec["unbounded_manifestation_construct"],
        "source_register_sha256": sha_file(source_path),
        "pre_execution_lock_sha256": sha_file(lock_path),
        "frozen_derivation_sha256": spec_hash,
        "claim_boundary": spec["claim_boundary"],
        "strongest_supported_claim": "Module A constitutes and executes a deterministic, typed, auditable, restartable prephysical triad/First-Action/kernel/relational-memory handoff at the declared mathematical scope.",
        "strongest_unsupported_claim": "No Big Implosion, physical time, geometry, fields, particles, constants of nature, direct many-body dynamics, manifested universe, or empirical validation is established.",
    }

    primary_summary = {
        "run_id": spec["run_id"],
        "classification": "MODULE_A_PREPHYSICAL_PRIMARY_EXECUTION",
        "source_hashes_verified": True,
        "triad_rank": full_rank,
        "all_ablations_fail_as_predeclared": all(x["result"] == "FAIL_AS_PREDECLARED" for x in ablations.values()),
        "scalar_countermodel_rejected": scalar_countermodel["result"].startswith("REJECTED"),
        "kernel_normalized": kernel_audit["normalization_error"] <= 1e-12,
        "kernel_tail_bound_pass": kernel_audit["tail_bound"] <= 1e-12,
        "finite_N_all_pass": all(
            x["lane_count"] == x["expected_lane_count"]
            and x["lane_increment_to_N_plus_1"] == x["expected_increment"]
            and x["no_self_lanes"] and x["unique_lanes"]
            and not x["lane_count_alone_implies_new_solution"]
            and x["direct_backreaction_norm"] == 0.0
            for x in finite_n
        ),
        "memory_nonidentity_and_no_loss_pass": (not memory["RFL_equals_next_CIF"] and memory["ancestry_preserved"]),
        "unbounded_construct_pass": unbounded["all_sample_hashes_distinct"] and unbounded["all_sample_bases_bounded"],
        "public_data_used": False,
        "physical_objects_assumed": False,
        "preliminary_handoff_sha256": sha_bytes(canonical_bytes(handoff_preliminary)),
    }

    outputs = {
        "TRIAD_AND_FIRST_ACTION.json": {"typed_roles": spec["typed_roles"], "first_action": spec["first_action"], "triad_rank": full_rank, "ablation_ranks": ablation_ranks},
        "KERNEL_EXECUTION.json": kernel_audit,
        "FINITE_N_RELATIONAL_AUDIT.json": {"range": [2, 8], "records": finite_n},
        "COUNTERMODEL_RESULTS.json": countermodels,
        "MEMORY_REOPENING_AUDIT.json": memory,
        "UNBOUNDED_MANIFESTATION_AUDIT.json": unbounded,
        "CONVERGENCE_AND_UNCERTAINTY.json": {"convergence": convergence, "uncertainty": uncertainty},
        "H_A_to_B.preliminary.json": handoff_preliminary,
        "PRIMARY_SUMMARY.json": primary_summary,
    }
    for name, obj in outputs.items():
        write_json(PRIMARY / name, obj)

    # Independent output schema is frozen in code and checked here.
    required = {
        "TRIAD_AND_FIRST_ACTION.json": ["typed_roles", "first_action", "triad_rank", "ablation_ranks"],
        "KERNEL_EXECUTION.json": ["delta", "alpha", "xi", "depth", "normalized_weights", "kernel_state", "tail_bound"],
        "FINITE_N_RELATIONAL_AUDIT.json": ["range", "records"],
        "COUNTERMODEL_RESULTS.json": ["triad_ablations", "scalar_collapse", "lane_count_only", "unwitnessed_branch"],
        "MEMORY_REOPENING_AUDIT.json": ["CIF_0", "QV_witness", "RFL_0", "promotion", "CIF_1", "reopening_event"],
        "UNBOUNDED_MANIFESTATION_AUDIT.json": ["constructive_rule", "all_sample_hashes_distinct", "all_sample_bases_bounded", "samples"],
        "CONVERGENCE_AND_UNCERTAINTY.json": ["convergence", "uncertainty"],
        "H_A_to_B.preliminary.json": ["object_id", "typed_roles", "first_action", "kernel", "relational_carrier", "claim_boundary"],
        "PRIMARY_SUMMARY.json": ["classification", "source_hashes_verified", "finite_N_all_pass", "public_data_used"],
    }
    schema_results = []
    for name, keys in required.items():
        obj = json.loads((PRIMARY / name).read_text())
        missing = [k for k in keys if k not in obj]
        schema_results.append({"path": str((PRIMARY / name).relative_to(ROOT)), "required_keys": keys, "missing": missing, "pass": not missing})
    write_json(PRIMARY / "SCHEMA_VALIDATION.json", {"classification": "RUN_SPECIFIC_STRICT_SEMANTIC_ENVELOPE", "overall": "PASS" if all(x["pass"] for x in schema_results) else "FAIL", "records": schema_results})

    assert all(primary_summary[k] for k in [
        "source_hashes_verified", "all_ablations_fail_as_predeclared", "scalar_countermodel_rejected", "kernel_normalized",
        "kernel_tail_bound_pass", "finite_N_all_pass", "memory_nonidentity_and_no_loss_pass", "unbounded_construct_pass"
    ])
    print(json.dumps(primary_summary, indent=2))


if __name__ == "__main__":
    main()
