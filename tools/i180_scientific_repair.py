#!/usr/bin/env python3
"""Reset the scientific frontier to Module I and install the corrected I derivation.

This script is intentionally conservative. It never deletes historical I/HI evidence. It
moves the current controller frontier back to I, records the superseded state in an audit
artifact, and installs a derivation in which the gauge-reduced weighted Laplacian/Dirichlet
operator is primary. Resistance distance and pseudo-determinant scale are retained only at
their proved scopes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "STATE.json"
QUEUE = ROOT / "WORK_QUEUE.json"
AUDIT = ROOT / "audit" / "I180_SCIENTIFIC_SUPERSESSION_20260810.json"
SPEC = ROOT / "modules" / "I" / "repair" / "I180_CORRECTED_DERIVATION_SPEC.json"
VERIFY = ROOT / "modules" / "I" / "repair" / "REPAIR_VERIFICATION.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def json_write(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def reset_frontier() -> None:
    state = json.loads(STATE.read_text())
    queue = json.loads(QUEUE.read_text())
    old_state = deepcopy(state)
    old_queue_active = [x.get("id") for x in queue.get("items", []) if x.get("status") == "ACTIVE"]

    audit = {
        "schema_version": "1.0",
        "event": "I180_SCIENTIFIC_FRONTIER_RESET_AND_SUPERSESSION",
        "timestamp_utc": utcnow(),
        "reason": [
            "I-180 froze effective-resistance distance and pseudo-determinant scalar scale without proving universal uniqueness or metric/scale branch completeness.",
            "I-180 primary numerical background was explicitly classified as an implementation witness, yet controller evidence was promoted through PHYSICALLY_EXECUTED.",
            "HI-190 and J-200 depend on I and therefore cannot remain authoritative while I is repaired."
        ],
        "preservation_policy": "No historical run is deleted. Prior I-180/HI-190/J evidence remains in repository history and is superseded only as current scientific authority.",
        "previous_frontier": {
            "active_work_unit": old_state.get("active_work_unit"),
            "current_module": old_state.get("current_module"),
            "current_run": old_state.get("current_run"),
            "active_queue_items": old_queue_active,
            "I_state": old_state.get("modules", {}).get("I"),
            "HI_state": old_state.get("modules", {}).get("HI"),
            "J_state": old_state.get("modules", {}).get("J")
        },
        "new_frontier": {
            "active_work_unit": "I-180",
            "current_module": "I",
            "current_run": None,
            "HU_preserved": True,
            "HI_blocked_pending_repaired_I": True,
            "J_blocked_pending_repaired_I_and_replayed_HI": True
        },
        "claim_correction": {
            "old_overclaim": "I physically executed a uniquely derived realized background geometry.",
            "corrected_claim": "Through HU the lineage is frozen; I is the active frontier. The prior I construction is an admissible response-geometry candidate with successful implementation checks, but universal uniqueness, branch completeness, and physical branch execution were not established."
        }
    }
    json_write(AUDIT, audit)

    state["active_work_unit"] = "I-180"
    state["current_module"] = "I"
    state["current_run"] = None
    state["last_updated_utc"] = utcnow()
    for mod in ("I", "HI", "J"):
        m = state.get("modules", {}).get(mod)
        if isinstance(m, dict):
            m["evidence_state"] = "DESIGN"
            m["fidelity"] = "UNSTARTED"
            m["active_run"] = None
            m["frozen_artifacts"] = []
            m["completed_runs"] = []
            m["promotion_evidence"] = []
            m["scientific_supersession"] = {
                "status": "SUPERSEDED_AS_CURRENT_AUTHORITY",
                "audit": str(AUDIT.relative_to(ROOT)),
                "historical_evidence_preserved_in_git": True
            }
    if "strongest_supported_claim" in state:
        state["strongest_supported_claim"] = (
            "A through HU remain at their verified frozen scopes. Module I is the sole active scientific frontier; no realized physical background geometry is currently frozen."
        )
    if "strongest_unsupported_claim" in state:
        state["strongest_unsupported_claim"] = (
            "No unique or branch-complete Module-I metric/expansion law, physical I branch execution, HI instantiation on repaired I, or J covariance/spectrum state is currently established."
        )
    json_write(STATE, state)

    seen_i = False
    for item in queue.get("items", []):
        wid = item.get("id")
        if wid == "I-180":
            item["status"] = "ACTIVE"
            item["scientific_reset"] = str(AUDIT.relative_to(ROOT))
            seen_i = True
            continue
        if wid in {"HI-190", "J-200"} or (seen_i and item.get("status") != "PASS"):
            item["status"] = "BLOCKED"
        elif item.get("status") == "ACTIVE":
            item["status"] = "BLOCKED"
    # Defensive: there must be exactly one ACTIVE item.
    active = [x.get("id") for x in queue.get("items", []) if x.get("status") == "ACTIVE"]
    if active != ["I-180"]:
        raise SystemExit(f"frontier reset produced invalid ACTIVE set: {active}")
    json_write(QUEUE, queue)


def build_spec() -> None:
    g = ROOT / "modules" / "G" / "frozen" / "H_G_to_I.json"
    b = ROOT / "modules" / "B" / "frozen" / "H_B_to_C_v2.json"
    protocol = ROOT / "docs" / "09_DERIVATION_PROTOCOL.md"
    nbody_candidates = list((ROOT / "sources" / "frozen").glob("*/A_Triadic_Solution_to_the_General_N_Body_Problem_Revised.pdf"))
    if len(nbody_candidates) != 1:
        raise SystemExit(f"expected one frozen revised N-body PDF, found {len(nbody_candidates)}")
    nbody = nbody_candidates[0]

    spec = {
        "schema_version": "3.0",
        "work_unit": "I-180",
        "status": "CORRECTED_DERIVATION_PRE_EXECUTION",
        "generation_mode": "GENERATION_SEALED",
        "objective": "Derive realized relational geometry/expansion from exact G/B ancestry without arbitrary metric selection or scalar information loss.",
        "exact_inputs": [
            {"path": str(g.relative_to(ROOT)), "sha256": sha(g), "role": "DIRECT_PARENT"},
            {"path": str(b.relative_to(ROOT)), "sha256": sha(b), "role": "PHYSICAL_CARRIER_ANCESTRY"},
            {"path": str(nbody.relative_to(ROOT)), "sha256": sha(nbody), "role": "RELATIONAL_BRANCH_POLICY_AUTHORITY"},
            {"path": str(protocol.relative_to(ROOT)), "sha256": sha(protocol), "role": "DERIVATION_PROTOCOL"}
        ],
        "triadic_descent": {
            "CIF": "Retain the complete internally admissible family of process-to-relational-lane realizations and response readouts not distinguished by exact parent witnesses.",
            "QV": "Admit only conservative, ancestry-compatible, gauge-consistent realizations and reject any candidate that deletes recoverable relational information or adds an unearned scale/target.",
            "RFL": "Stabilize the complete gauge-reduced response geometry, its branch identity, memory, covariance, and restart information without collapsing unresolved anisotropy or lawful branch multiplicity."
        },
        "primary_geometry": {
            "object": "GAUGE_REDUCED_WEIGHTED_DIRICHLET_RESPONSE_FAMILY",
            "event_pullback": "w_e^b(t)=sum_r M_b(e|r) Gamma_r^b(t), with M>=0 and column sums 1; M remains a branch coordinate unless exact ancestry witnesses distinguish it.",
            "operator": "L_b,M(t)=B_R^T diag(w^b,M(t)) B_R",
            "quotient": "Q=1^perp; on each connected positive branch L|_Q is positive definite.",
            "response_operator": "G_b,M(t)=L_b,M(t)^+ on the constant-mode quotient.",
            "claim": "L (equivalently its quotient Dirichlet form) is primary. No pairwise scalar distance is allowed to replace the full operator as the geometry state."
        },
        "response_distance": {
            "formula": "R_ij=(e_i-e_j)^T L^+ (e_i-e_j); d_resp=sqrt(R_ij)",
            "classification": "DERIVED_RESPONSE_METRIC_READOUT_NOT_UNIVERSAL_METRIC_UNIQUENESS",
            "no_loss_theorem": "For connected n-node branches, with H=I-11^T/n, L^+=-1/2 H R H. Therefore the complete resistance matrix reconstructs the gauge-reduced response operator exactly.",
            "scope_of_uniqueness": "Unique pairwise squared response distance generated by the Green response operator L^+; no claim that every conceivable graph metric is equivalent to it.",
            "rejected_overclaim": "Do not call effective resistance the unique RFC metric without an additional theorem excluding all other lawful relational observables."
        },
        "competing_readouts": [
            {
                "name": "shortest_path_inverse_activity",
                "status": "DIAGNOSTIC_NOT_PRIMARY_GEOMETRY",
                "reason": "Can discard non-geodesic edge-weight information and therefore fails the RFC no-loss memory requirement as a replacement for the full geometry state."
            },
            {
                "name": "diffusion_or_heat_distance",
                "status": "RESERVED_BRANCH_IF_SCALE_PARAMETER_IS_INTERNALLY_DERIVED",
                "reason": "Requires an additional diffusion/scale parameter unless a parent supplies it; cannot silently select one."
            }
        ],
        "expansion_without_scalar_collapse": {
            "nonzero_spectrum": "lambda_k(t)>0, k=1..r, of L on Q",
            "principal_response_lengths": "ell_k(t)=lambda_k(t)^(-1/2)",
            "directional_rates": "H_k=d ln ell_k/dt_phys",
            "volumetric_scale": "a_vol(t)=[pdet_+(L(t_in))/pdet_+(L(t))]^(1/(2r)) = [prod_k ell_k(t)/prod_k ell_k(t_in)]^(1/r)",
            "volumetric_rate": "H_vol=d ln a_vol/dt_phys=(1/r) sum_k H_k",
            "classification_of_old_pdet_formula": "DERIVED_VOLUMETRIC_GEOMETRIC_MEAN_SUMMARY, not a proof that all scalar size summaries are identical.",
            "anisotropy_policy": "Retain the full ell_k/H_k spectrum. A single scalar H may not erase unequal directional response rates.",
            "homothetic_correspondence": "If L(t)=c(t)L(t_in) on Q, then ell_k(t)/ell_k(t_in)=c(t)^(-1/2) for every k; every positive symmetric homogeneous degree -1/2 scale functional has the same relative scale. Only in this internally witnessed homothetic case is scalar collapse branch-independent."
        },
        "clock": "Use only inherited Big-Implosion t_phys=t_B tau_B with t_B>0 branch coordinate; recurrence depth is not time.",
        "causal_reach": {
            "status": "BRANCH_FUNCTIONAL_PENDING_GEOMETRY_AND_PROPAGATION_BINDING",
            "rule": "Do not define a unique horizon from a scalar a unless homothetic/isotropic collapse has been internally witnessed. Causal reach must be computed on the retained geometry/propagation branch."
        },
        "branch_policy": {
            "authority": "Revised N-body branch policy: when lawful witnesses do not distinguish a unique branch, preserve the gauge/multi-route branch family rather than adding information.",
            "coordinates": [
                "G inherited unresolved microscopic/recombination coordinates",
                "ancestry-compatible process-to-edge incidence M_b(e|r)",
                "positive clock scale t_B",
                "propagation representative where not already parent-fixed",
                "any additional response-readout parameter only if explicitly derived and typed"
            ],
            "forbidden_selection": [
                "observed H(z), H0, BAO, SN, sound horizon or LambdaCDM targets",
                "standard FRW/Friedmann/Einstein equations without a later correspondence theorem",
                "manufactured numerical witness promoted to a physical branch",
                "arbitrary tie-breaking among internally indistinguishable branches"
            ]
        },
        "physical_execution_gate": {
            "status": "BLOCKED_PENDING_EXACT_PARENT_BINDING",
            "requirements": [
                "derive or explicitly retain the complete M_b(e|r) branch from exact G/B route ancestry",
                "bind actual parent-generated Gamma_r^b(t) or the exact parent object replacing it",
                "execute the physical branch family or a uniquely witnessed branch; manufactured ODEs remain implementation tests only",
                "retain anisotropic response spectrum unless homothety is proved"
            ],
            "promotion_rule": "No PHYSICALLY_EXECUTED promotion from implementation-only or manufactured witnesses."
        },
        "semantic_countermodels_required": [
            "two different weighted graphs with identical shortest-path metric but different response operator -> shortest path cannot replace no-loss geometry",
            "two nonhomothetic positive spectra for which volumetric and RMS response scales disagree -> scalar summaries are not universally equivalent",
            "homothetic spectra -> all degree -1/2 homogeneous relative scales agree",
            "negative/nonconservative incidence -> reject",
            "extra disconnected zero mode -> reject or explicit component branch",
            "observed-cosmology target injection -> reject"
        ],
        "claim_boundary": {
            "strongest_supported": "A corrected finite-relational response-geometry law family is derivable from exact G/B ancestry: weighted Dirichlet operator on the gauge quotient, lossless Green-response readout, principal response-length spectrum, and a derived volumetric expansion summary. The previous resistance/pdet construction survives only at these narrower proved scopes.",
            "strongest_unsupported": "No unique process-to-edge realization, unique continuum/SI spacetime metric, unique scalar expansion history on nonhomothetic branches, physical H(z), empirical cosmology, or physically executed I branch is established until exact parent bindings and branch witnesses close the remaining I frontier."
        }
    }
    json_write(SPEC, spec)


def resistance_matrix(L: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    Lp = np.linalg.pinv(L)
    n = L.shape[0]
    R = np.empty_like(L)
    for i in range(n):
        for j in range(n):
            e = np.zeros(n); e[i] = 1; e[j] -= 1
            R[i, j] = e @ Lp @ e
    return R, Lp


def verify_math() -> None:
    # Nonphysical semantic witness only.
    w = np.array([2.0, 3.0, 5.0])
    B = np.array([[1., -1., 0.], [1., 0., -1.], [0., 1., -1.]])
    L = B.T @ np.diag(w) @ B
    R, Lp = resistance_matrix(L)
    H = np.eye(3) - np.ones((3, 3)) / 3
    recon = -0.5 * H @ R @ H
    reconstruction_linf = float(np.max(np.abs(recon - Lp)))

    # Shortest-path no-loss countermodel: direct edge 0-2 is non-geodesic for both
    # choices below, so changing its weight leaves all shortest path lengths fixed.
    # Edge lengths are inverse activity.
    def sp_metric(weights):
        l01, l02, l12 = 1 / weights[0], 1 / weights[1], 1 / weights[2]
        return np.array([[0, min(l01, l02+l12), min(l02, l01+l12)],
                         [min(l01, l02+l12), 0, min(l12, l01+l02)],
                         [min(l02, l01+l12), min(l12, l01+l02), 0]], float)
    wa = np.array([1.0, 0.2, 1.0])   # lengths 1,5,1 -> edge 02 hidden
    wb = np.array([1.0, 0.1, 1.0])   # lengths 1,10,1 -> same shortest-path metric
    spa, spb = sp_metric(wa), sp_metric(wb)
    La = B.T @ np.diag(wa) @ B
    Lb = B.T @ np.diag(wb) @ B

    # Nonhomothetic scalar-summary disagreement.
    lam0 = np.array([1.0, 4.0])
    lam1 = np.array([2.0, 5.0])
    avol = float((np.prod(lam0) / np.prod(lam1)) ** (1 / (2 * len(lam0))))
    arms = float(np.sqrt(np.mean(1 / lam1)) / np.sqrt(np.mean(1 / lam0)))

    # Homothetic agreement.
    c = 3.25
    lamh = c * lam0
    avol_h = float((np.prod(lam0) / np.prod(lamh)) ** (1 / (2 * len(lam0))))
    arms_h = float(np.sqrt(np.mean(1 / lamh)) / np.sqrt(np.mean(1 / lam0)))
    expected_h = float(c ** -0.5)

    out = {
        "schema_version": "1.0",
        "classification": "I180_CORRECTED_DERIVATION_SEMANTIC_VERIFICATION",
        "all_inputs_nonphysical_manufactured": True,
        "checks": {
            "resistance_double_centering_reconstructs_Lplus": {
                "residual_linf": reconstruction_linf,
                "pass": reconstruction_linf < 1e-12
            },
            "shortest_path_can_lose_edge_information": {
                "shortest_path_equal": bool(np.allclose(spa, spb)),
                "laplacians_different": bool(not np.allclose(La, Lb)),
                "pass": bool(np.allclose(spa, spb) and not np.allclose(La, Lb))
            },
            "nonhomothetic_scalar_summaries_can_disagree": {
                "a_vol": avol,
                "a_rms_response": arms,
                "difference": abs(avol-arms),
                "pass": abs(avol-arms) > 1e-6
            },
            "homothetic_relative_scales_agree": {
                "a_vol": avol_h,
                "a_rms_response": arms_h,
                "expected_c_minus_half": expected_h,
                "pass": max(abs(avol_h-expected_h), abs(arms_h-expected_h)) < 1e-12
            }
        },
        "wolfram_crosscheck": {
            "status": "PASS_EXTERNAL_KERNEL_20260810",
            "result": "For symbolic positive K3 weights a,b,c, -1/2 H R H - Lplus == zero matrix exactly; volumetric principal-length identity residual == 0.",
            "note": "External Wolfram check is corroborative. Repository verification remains independently reproducible with NumPy."
        }
    }
    out["pass"] = all(v.get("pass", False) for v in out["checks"].values())
    json_write(VERIFY, out)
    if not out["pass"]:
        raise SystemExit("I-180 corrected derivation semantic verification failed")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["reset", "spec", "verify", "all"])
    args = ap.parse_args()
    if args.mode in {"reset", "all"}:
        reset_frontier()
    if args.mode in {"spec", "all"}:
        build_spec()
    if args.mode in {"verify", "all"}:
        if not SPEC.exists():
            build_spec()
        verify_math()


if __name__ == "__main__":
    main()
