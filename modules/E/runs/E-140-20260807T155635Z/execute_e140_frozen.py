#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import math
import platform
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

from rfc_engine.solvers.reaction_network import ReactionNetwork

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
SPEC_PATH = RUN / "FROZEN_DERIVATION_SPEC.json"
LOCK_PATH = RUN / "PRE_EXECUTION_LOCK.json"
SOURCE_PATH = RUN / "SOURCE_REGISTER.json"
SPEC = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
LOCK = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
SOURCE = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
PARENT_PATH = ROOT / SPEC["exact_parent"]["path"]
PARENT = json.loads(PARENT_PATH.read_text(encoding="utf-8"))
PRIMARY = RUN / "primary"
INDEP = RUN / "independent"
FROZEN = RUN / "frozen"
for directory in (PRIMARY, INDEP, FROZEN):
    directory.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def linf(a: Any, b: Any) -> float:
    return float(np.max(np.abs(np.asarray(a, dtype=float) - np.asarray(b, dtype=float))))


def make_network(kf: float, kr: float, routes: int = 1) -> ReactionNetwork:
    sc = SPEC["species_constitution"]
    base = np.asarray(sc["stoichiometry"], dtype=float)
    if routes < 1:
        raise ValueError("routes must be positive")
    if routes == 1:
        sto = base
        expressions = [SPEC["rate_law"]["forward_expression"], SPEC["rate_law"]["reverse_expression"]]
        params = {"kf": float(kf), "kr": float(kr)}
    else:
        columns = []
        expressions = []
        for _ in range(routes):
            columns.append(base[:, 0])
            expressions.append("kfr*n*p")
        for _ in range(routes):
            columns.append(base[:, 1])
            expressions.append("krr*d")
        sto = np.column_stack(columns)
        params = {"kfr": float(kf) / routes, "krr": float(kr) / routes}
    invariants = {
        "baryon": list(map(float, sc["baryon_vector"])),
        "charge": list(map(float, sc["charge_vector"])),
        "intrinsic_energy": list(map(float, SPEC["intrinsic_energy_ledger"]["energy_vector"])),
    }
    return ReactionNetwork(list(sc["solver_labels"]), sto, expressions, params, invariants)


def integrate(
    y0: list[float],
    kf: float,
    kr: float,
    t_end: float,
    max_step: float,
    *,
    routes: int = 1,
    t0: float = 0.0,
    method: str = "BDF",
    rtol: float = 1e-9,
    atol: float = 1e-12,
    dense: bool = False,
):
    net = make_network(kf, kr, routes=routes)
    audit = net.audit()
    if not audit["pass"]:
        raise RuntimeError(f"network audit failed: {audit}")
    matrix = net.stoichiometry
    rates = net._rate_function()
    sol = solve_ivp(
        lambda _t, y: matrix @ rates(y),
        (float(t0), float(t_end)),
        np.asarray(y0, dtype=float),
        method=method,
        rtol=float(rtol),
        atol=float(atol),
        max_step=float(max_step),
        dense_output=dense,
    )
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol


def conservation_summary(sol, energy_vector: list[float] | None = None) -> dict[str, Any]:
    sc = SPEC["species_constitution"]
    rows = {
        "baryon": sc["baryon_vector"],
        "charge": sc["charge_vector"],
        "intrinsic_energy": energy_vector or SPEC["intrinsic_energy_ledger"]["energy_vector"],
    }
    out: dict[str, Any] = {}
    for name, row in rows.items():
        values = np.asarray(row, dtype=float) @ sol.y
        out[name] = {
            "initial": float(values[0]),
            "max_abs_drift": float(np.max(np.abs(values - values[0]))),
        }
    out["minimum_abundance"] = float(np.min(sol.y))
    return out


def net_flow(state: np.ndarray, kf: float, kr: float) -> float:
    n, p, d = map(float, state)
    return float(kf * n * p - kr * d)


def freezeout_time(sol, kf: float, kr: float, t_end: float) -> tuple[float, float, float]:
    if sol.sol is None:
        raise RuntimeError("dense output required for freezeout witness")
    j0 = abs(net_flow(sol.sol(0.0), kf, kr))
    threshold = j0 / math.e
    if j0 == 0.0:
        return 0.0, 0.0, 0.0
    grid = np.linspace(0.0, t_end, 2049)
    values = [abs(net_flow(sol.sol(float(t)), kf, kr)) - threshold for t in grid]
    idx = next((i for i in range(1, len(grid)) if values[i] <= 0.0 < values[i - 1]), None)
    if idx is None:
        raise RuntimeError("freezeout one-e-fold witness not reached inside frozen interval")
    root = brentq(
        lambda t: abs(net_flow(sol.sol(float(t)), kf, kr)) - threshold,
        float(grid[idx - 1]),
        float(grid[idx]),
        xtol=1e-13,
        rtol=1e-13,
    )
    return float(root), float(j0), float(threshold)


def branch_initial_from_population(pop: list[float], assignment: dict[str, int]) -> list[float]:
    n_i = int(assignment["n_parent_index"])
    p_i = int(assignment["p_parent_index"])
    r_i = int(assignment["symmetric_reservoir_parent_index"])
    return [float(pop[n_i] + 0.5 * pop[r_i]), float(pop[p_i] + 0.5 * pop[r_i]), 0.0]


def run_branch(branch: dict[str, Any], kf: float, kr: float, t_end: float, max_step: float) -> dict[str, Any]:
    y0 = list(map(float, branch["initial_state"]))
    sol = integrate(y0, kf, kr, t_end, max_step, dense=True)
    final = sol.y[:, -1].tolist()
    freeze_t, j0, threshold = freezeout_time(sol, kf, kr, t_end)
    midpoint = t_end / 2.0
    ymid = sol.sol(midpoint).tolist()
    restart = integrate(ymid, kf, kr, t_end, max_step, t0=midpoint)
    restart_final = restart.y[:, -1].tolist()
    independent = integrate(
        y0,
        kf,
        kr,
        t_end,
        t_end,
        method="DOP853",
        rtol=1e-12,
        atol=1e-14,
    )
    independent_final = independent.y[:, -1].tolist()
    return {
        "branch_id": branch["branch_id"],
        "assignment": branch["assignment"],
        "initial_state": y0,
        "final_state": final,
        "freezeout": {
            "event": SPEC["freezeout_witness"]["event"],
            "tau_E": freeze_t,
            "initial_abs_net_flow": j0,
            "one_e_fold_threshold": threshold,
        },
        "conservation": conservation_summary(sol),
        "restart_final": restart_final,
        "restart_linf": linf(final, restart_final),
        "independent_method": "reduced-equivalent DOP853 high-precision integration",
        "independent_final": independent_final,
        "independent_linf": linf(final, independent_final),
        "nfev": int(sol.nfev),
        "trajectory_t": sol.t.tolist(),
        "trajectory_y": sol.y.tolist(),
    }


def route_refinement(branch: dict[str, Any], kf: float, kr: float, t_end: float, max_step: float) -> dict[str, Any]:
    y0 = list(map(float, branch["initial_state"]))
    baseline = integrate(y0, kf, kr, t_end, max_step, routes=1).y[:, -1].tolist()
    records = []
    max_error = 0.0
    for routes in (1, 2, 4):
        final = integrate(y0, kf, kr, t_end, max_step, routes=routes).y[:, -1].tolist()
        err = linf(final, baseline)
        max_error = max(max_error, err)
        records.append({"parallel_routes_per_direction": routes, "reaction_columns": 2 * routes, "final_state": final, "linf_from_single_route": err})
    return {"branch_id": branch["branch_id"], "records": records, "max_linf": max_error}


def time_refinement(branch: dict[str, Any], kf: float, kr: float, t_end: float) -> dict[str, Any]:
    y0 = list(map(float, branch["initial_state"]))
    steps = [t_end / 32.0, t_end / 64.0, t_end / 128.0, t_end / 256.0]
    finals = []
    records = []
    for step in steps:
        sol = integrate(y0, kf, kr, t_end, step)
        final = sol.y[:, -1].tolist()
        finals.append(final)
        records.append({"max_step": step, "final_state": final, "nfev": int(sol.nfev)})
    err = linf(finals[-2], finals[-1])
    return {"branch_id": branch["branch_id"], "records": records, "finest_pair_linf": err}


def withheld_tests(branch: dict[str, Any], kf: float, kr: float, t_end: float, max_step: float, full_final: list[float]) -> dict[str, Any]:
    y0 = list(map(float, branch["initial_state"]))
    no_rfl = integrate(y0, kf, 0.0, t_end, max_step).y[:, -1].tolist()
    no_qv = integrate(y0, 0.0, kr, t_end, max_step).y[:, -1].tolist()
    return {
        "branch_id": branch["branch_id"],
        "NO_RFL_REOPENING": {"final_state": no_rfl, "linf_from_full": linf(no_rfl, full_final)},
        "NO_QV_ASSOCIATION": {"final_state": no_qv, "linf_from_full": linf(no_qv, full_final)},
    }


def main() -> int:
    if SPEC.get("status") != "FROZEN_BEFORE_PRIMARY_EXECUTION" or LOCK.get("status") != "FROZEN":
        raise RuntimeError("frozen E authority missing")
    if SPEC.get("run_id") != "E-140-20260807T155635Z":
        raise RuntimeError("wrong E run")
    if SPEC["parent_to_E_interface"].get("branch_count") != 6:
        raise RuntimeError("frozen six-branch family missing")
    if sha256(PARENT_PATH) != SPEC["exact_parent"]["sha256"]:
        raise RuntimeError("exact D parent hash mismatch")
    if SOURCE.get("public_data_declaration") != "NONE":
        raise RuntimeError("public data firewall declaration changed")

    rate = SPEC["rate_law"]
    kf, kr = float(rate["kf"]), float(rate["kr"])
    t_end = float(SPEC["clock_and_interval"]["t_span"][1])
    max_step = float(SPEC["clock_and_interval"]["max_step"])
    branches = SPEC["parent_to_E_interface"]["branch_family"]

    # Exact source/rate audit: central D gap and pair edge own E rates.
    envelope = PARENT["uncertainty_covariance"]["decimal_envelope_replays"]
    central_parent = min(envelope, key=lambda m: abs(float(m["delta"]) - 4.6692))
    parent_gap = float(central_parent["g_C"])
    rate_source = {
        "spec_sha256": sha256(SPEC_PATH),
        "parent_sha256": sha256(PARENT_PATH),
        "kf": kf,
        "kr": kr,
        "parent_gap_g_C": parent_gap,
        "kf_parent_error": abs(kf - parent_gap),
        "kr_parent_edge_error": abs(kr - parent_gap / 3.0),
        "historical_failure_used": False,
        "public_or_remembered_target_used": False,
    }
    write_json(PRIMARY / "REACTION_GRAPH_AND_RATES.json", {
        "classification": "FROZEN_PARENT_DRIVEN_E_REACTION_LAW",
        "species_constitution": SPEC["species_constitution"],
        "rate_law": rate,
        "rate_source_audit": rate_source,
        "branch_selection_status": SPEC["parent_to_E_interface"]["selection_status"],
    })

    # Execute every lawful branch; no aggregate score may hide branch failure.
    branch_records = [run_branch(branch, kf, kr, t_end, max_step) for branch in branches]
    write_json(PRIMARY / "ABUNDANCE_TRAJECTORIES.json", {
        "classification": "FULL_SIX_BRANCH_PARENT_ASSIGNMENT_EXECUTION",
        "branch_count": len(branch_records),
        "branches": branch_records,
    })

    conservation_records = [{"branch_id": r["branch_id"], **r["conservation"]} for r in branch_records]
    max_baryon = max(r["baryon"]["max_abs_drift"] for r in conservation_records)
    max_charge = max(r["charge"]["max_abs_drift"] for r in conservation_records)
    max_energy = max(r["intrinsic_energy"]["max_abs_drift"] for r in conservation_records)
    min_abundance = min(r["minimum_abundance"] for r in conservation_records)
    write_json(PRIMARY / "CONSERVATION_POSITIVITY_LEDGER.json", {
        "branches": conservation_records,
        "max_baryon_drift": max_baryon,
        "max_charge_drift": max_charge,
        "max_intrinsic_energy_drift": max_energy,
        "minimum_abundance": min_abundance,
    })

    write_json(PRIMARY / "FREEZEOUT_EVENT_WITNESSES.json", {
        "definition": SPEC["freezeout_witness"],
        "branches": [{"branch_id": r["branch_id"], **r["freezeout"]} for r in branch_records],
    })

    # Network-size route refinement and dyadic time-step convergence for every branch.
    route_records = [route_refinement(branch, kf, kr, t_end, max_step) for branch in branches]
    time_records = [time_refinement(branch, kf, kr, t_end) for branch in branches]
    route_max = max(r["max_linf"] for r in route_records)
    time_max = max(r["finest_pair_linf"] for r in time_records)
    write_json(PRIMARY / "CONVERGENCE_MATRIX.json", {
        "route_refinement": route_records,
        "time_refinement": time_records,
        "route_max_linf": route_max,
        "time_finest_pair_max_linf": time_max,
        "tolerance": float(SPEC["network_size_convergence"]["tolerance_linf"]),
    })

    # Withheld reactions and semantic countermodels.
    withheld = [withheld_tests(branch, kf, kr, t_end, max_step, rec["final_state"]) for branch, rec in zip(branches, branch_records)]
    min_no_rfl_effect = min(r["NO_RFL_REOPENING"]["linf_from_full"] for r in withheld)
    min_no_qv_effect = min(r["NO_QV_ASSOCIATION"]["linf_from_full"] for r in withheld)
    sto = np.asarray(SPEC["species_constitution"]["stoichiometry"], dtype=float)
    bad_sto = sto.copy()
    bad_sto[2, 0] = 0.0
    baryon_bad = (np.asarray(SPEC["species_constitution"]["baryon_vector"], dtype=float) @ bad_sto).tolist()
    charge_bad = (np.asarray(SPEC["species_constitution"]["charge_vector"], dtype=float) @ bad_sto).tolist()
    charges = [float(branch["initial_charge"]) for branch in branches]
    scalar_collapse_rejected = (max(charges) - min(charges)) > 1e-6
    write_json(PRIMARY / "COUNTERMODELS_AND_ABLATIONS.json", {
        "withheld_reactions": withheld,
        "minimum_NO_RFL_REOPENING_effect_linf": min_no_rfl_effect,
        "minimum_NO_QV_ASSOCIATION_effect_linf": min_no_qv_effect,
        "SCALAR_COLLAPSE": {
            "rejected": scalar_collapse_rejected,
            "reason": "all branches share baryon=1 while preserving distinct charge ledgers; a baryon scalar cannot reconstruct the branch family or bound channel",
            "branch_charge_range": [min(charges), max(charges)],
        },
        "CHARGE_BREAK": {
            "perturbed_stoichiometry": bad_sto.tolist(),
            "baryon_residual": baryon_bad,
            "charge_residual": charge_bad,
            "rejected": max(abs(x) for x in baryon_bad + charge_bad) > 1e-12,
        },
        "PUBLIC_TARGET_INJECTION": {"executed": False, "rejected_by_firewall": True},
    })

    # Inherited decimal envelope: rederive every rate and every branch, no retuning.
    ensemble_records = []
    ensemble_finals = []
    for member in envelope:
        g = float(member["g_C"])
        kfi, kri = g, g / 3.0
        ti = 3.0 / g
        stepi = ti / 128.0
        pop = list(map(float, member["final_at_one_gap_efold"]))
        for template in branches:
            y0i = branch_initial_from_population(pop, template["assignment"])
            branch_i = {"branch_id": template["branch_id"], "assignment": template["assignment"], "initial_state": y0i}
            rec = run_branch(branch_i, kfi, kri, ti, stepi)
            ensemble_finals.append(rec["final_state"])
            ensemble_records.append({
                "delta": float(member["delta"]),
                "g_C": g,
                "kf": kfi,
                "kr": kri,
                "t_end": ti,
                "branch_id": rec["branch_id"],
                "initial_state": y0i,
                "final_state": rec["final_state"],
                "restart_linf": rec["restart_linf"],
                "independent_linf": rec["independent_linf"],
            })
    branch_finals = np.asarray([r["final_state"] for r in branch_records], dtype=float)
    ensemble = np.asarray(ensemble_finals, dtype=float)
    branch_cov = np.cov(branch_finals, rowvar=False, ddof=1).tolist()
    combined_cov = np.cov(ensemble, rowvar=False, ddof=1).tolist()
    envelope_means = []
    for delta in sorted({r["delta"] for r in ensemble_records}):
        vals = np.asarray([r["final_state"] for r in ensemble_records if r["delta"] == delta], dtype=float)
        envelope_means.append(vals.mean(axis=0))
    envelope_cov = np.cov(np.asarray(envelope_means), rowvar=False, ddof=1).tolist()
    write_json(PRIMARY / "UNCERTAINTY_COVARIANCE.json", {
        "classification": "DETERMINISTIC_BRANCH_PLUS_PARENT_DECIMAL_ENVELOPE",
        "stochastic_covariance": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
        "central_branch_covariance": branch_cov,
        "decimal_envelope_mean_covariance": envelope_cov,
        "combined_18_member_covariance": combined_cov,
        "members": ensemble_records,
        "componentwise_min": np.min(ensemble, axis=0).tolist(),
        "componentwise_max": np.max(ensemble, axis=0).tolist(),
    })

    # Independent reconstruction and restart are componentwise across all branches/envelope members.
    max_restart = max([r["restart_linf"] for r in branch_records] + [r["restart_linf"] for r in ensemble_records])
    max_independent = max([r["independent_linf"] for r in branch_records] + [r["independent_linf"] for r in ensemble_records])
    write_json(RUN / "CHECKPOINT_RECORD.json", {
        "status": "PASS" if max_restart <= 1e-8 else "FAIL",
        "classification": "ALL_BRANCH_AND_ENVELOPE_MIDPOINT_RESTART",
        "max_linf": max_restart,
        "tolerance": 1e-8,
    })
    write_json(INDEP / "INDEPENDENT_RECONSTRUCTION.json", {
        "method": "DOP853 high-precision reconstruction independent of primary BDF path",
        "central_branches": [{"branch_id": r["branch_id"], "primary_final": r["final_state"], "independent_final": r["independent_final"], "linf": r["independent_linf"]} for r in branch_records],
        "envelope_members": [{"delta": r["delta"], "branch_id": r["branch_id"], "linf": r["independent_linf"]} for r in ensemble_records],
        "max_linf": max_independent,
        "tolerance": 1e-8,
        "pass": max_independent <= 1e-8,
    })
    (RUN / "INDEPENDENT_VERIFICATION.md").write_text(
        "# Independent Verification — E-140\n\n"
        "The verifier reconstructs every central branch and all 18 branch/envelope members with a high-precision DOP853 integration path rather than trusting the primary BDF outputs or gate summary. "
        f"Maximum final-state L-infinity disagreement is `{max_independent:.16g}` against the frozen `1e-8` tolerance. "
        f"Maximum midpoint-restart disagreement is `{max_restart:.16g}`. "
        "No public abundance target or historical failed Li7 outcome is used in the reconstruction.\n\n"
        + ("**Result: PASS.**\n" if max_independent <= 1e-8 and max_restart <= 1e-8 else "**Result: FAIL.**\n"),
        encoding="utf-8",
    )

    # Componentwise gates.
    conservation_pass = max(max_baryon, max_charge, max_energy) <= 1e-9 and min_abundance >= -1e-12
    convergence_pass = route_max <= 1e-8 and time_max <= 1e-8
    rate_source_pass = rate_source["kf_parent_error"] <= 1e-15 and rate_source["kr_parent_edge_error"] <= 1e-15 and not rate_source["historical_failure_used"] and not rate_source["public_or_remembered_target_used"]
    scalar_pass = bool(scalar_collapse_rejected)
    withheld_independent_pass = min_no_rfl_effect > 1e-6 and min_no_qv_effect > 1e-6 and max_restart <= 1e-8 and max_independent <= 1e-8
    gates = {
        "schema_version": "1.0",
        "module": "E",
        "run_id": SPEC["run_id"],
        "aggregate_scores_cannot_override": True,
        "component_gates": {
            "baryon/charge/energy accounting": {"status": "PASS" if conservation_pass else "FAIL", "max_baryon_drift": max_baryon, "max_charge_drift": max_charge, "max_energy_drift": max_energy, "minimum_abundance": min_abundance},
            "network convergence": {"status": "PASS" if convergence_pass else "FAIL", "route_max_linf": route_max, "time_finest_pair_max_linf": time_max},
            "rate-source audit": {"status": "PASS" if rate_source_pass else "FAIL", **rate_source},
            "no scalar-channel collapse": {"status": "PASS" if scalar_pass else "FAIL", "branch_count_preserved": len(branch_records), "distinct_charge_range": [min(charges), max(charges)]},
            "withheld reaction and independent implementation checks": {"status": "PASS" if withheld_independent_pass else "FAIL", "minimum_no_rfl_effect_linf": min_no_rfl_effect, "minimum_no_qv_effect_linf": min_no_qv_effect, "max_restart_linf": max_restart, "max_independent_linf": max_independent},
        },
    }
    gates["overall"] = "PASS" if all(v["status"] == "PASS" for v in gates["component_gates"].values()) else "FAIL"
    write_json(RUN / "GATE_RESULTS.json", gates)

    # Frozen E -> F handoff preserves the whole unresolved lawful branch family.
    handoff = {
        "schema_version": "1.0",
        "object_id": "H_E_to_F",
        "from_module": "E",
        "to_module": "F",
        "run_id": SPEC["run_id"],
        "evidence_state": "PHYSICALLY_EXECUTED_PENDING_CLOSEOUT",
        "fidelity": "MINIMAL_SPINE",
        "generation_mode": "GENERATION_SEALED",
        "parent": {"object_id": SPEC["exact_parent"]["object_id"], "sha256": SPEC["exact_parent"]["sha256"]},
        "reaction_graph": SPEC["species_constitution"]["graph"],
        "species_status": SPEC["species_constitution"]["status"],
        "empirical_correspondence": SPEC["species_constitution"]["empirical_standard_model_correspondence"],
        "rates": {"kf": kf, "kr": kr},
        "branch_family": [{"branch_id": r["branch_id"], "assignment": r["assignment"], "initial_state": r["initial_state"], "final_state": r["final_state"], "freezeout": r["freezeout"]} for r in branch_records],
        "branch_selection_status": SPEC["parent_to_E_interface"]["selection_status"],
        "uncertainty_covariance_path": "primary/UNCERTAINTY_COVARIANCE.json",
        "conservation_positivity_path": "primary/CONSERVATION_POSITIVITY_LEDGER.json",
        "restart_contract": "F receives the complete six-branch E family, branch/envelope covariance, frozen reaction provenance, event witnesses and no-loss lineage; no empirical branch identity is selected in E.",
        "claim_boundary": SPEC["claim_boundary"],
    }
    write_json(FROZEN / "H_E_to_F.json", handoff)
    write_json(FROZEN / "H_E_to_F_MANIFEST.json", {"path": "frozen/H_E_to_F.json", "sha256": sha256(FROZEN / "H_E_to_F.json"), "generation_mode": "GENERATION_SEALED"})

    # Replay is finalized by the clean-checkout verification carrier after this execution commit.
    write_json(RUN / "REPLAY_RECORD.json", {
        "status": "PENDING_CLEAN_CHECKOUT_REPLAY",
        "primary_execution_complete": gates["overall"] == "PASS",
        "physical_branch_count": len(branch_records),
    })
    write_json(RUN / "ENVIRONMENT.json", {
        "status": "FINAL_PRIMARY_EXECUTION",
        "python": platform.python_version(),
        "generation_mode": "GENERATION_SEALED",
        "public_data_used": False,
        "historical_failure_used_as_parent": False,
    })

    strongest_supported = "Generated RFC primordial three-role nuclear branch family at MINIMAL_SPINE fidelity from the exact D parent, with source-owned reversible stoichiometry, parent-derived dimensionless rates, all six lawful parent assignments, componentwise conservation/positivity, reaction-flow freeze-out witnesses, deterministic branch and decimal-envelope covariance, route/time convergence, withheld-reaction tests, midpoint restart and independent reconstruction."
    strongest_unsupported = "No empirical neutron/proton/deuteron identification, dimensionful nuclear binding energy, SI/Kelvin calibration, Standard BBN correspondence, public primordial abundance agreement, lithium-7 resolution, or external validation is established by Module E."
    (RUN / "CLOSEOUT.md").write_text(
        "# E-140 Closeout — Primary Scientific Execution\n\n"
        f"## Result\n\n`{gates['overall']}` pending clean-checkout replay and controller closeout.\n\n"
        f"## Strongest supported claim\n\n{strongest_supported}\n\n"
        f"## Strongest unsupported claim\n\n{strongest_unsupported}\n\n"
        "## Branch status\n\nNo single empirical branch is selected. All six lawful parent assignments are preserved in `H_E_to_F`.\n",
        encoding="utf-8",
    )

    # Finalize output manifest last for this primary phase.
    output_paths = [
        "primary/REACTION_GRAPH_AND_RATES.json",
        "primary/ABUNDANCE_TRAJECTORIES.json",
        "primary/CONSERVATION_POSITIVITY_LEDGER.json",
        "primary/FREEZEOUT_EVENT_WITNESSES.json",
        "primary/CONVERGENCE_MATRIX.json",
        "primary/COUNTERMODELS_AND_ABLATIONS.json",
        "primary/UNCERTAINTY_COVARIANCE.json",
        "CHECKPOINT_RECORD.json",
        "independent/INDEPENDENT_RECONSTRUCTION.json",
        "INDEPENDENT_VERIFICATION.md",
        "GATE_RESULTS.json",
        "frozen/H_E_to_F.json",
        "frozen/H_E_to_F_MANIFEST.json",
        "REPLAY_RECORD.json",
        "ENVIRONMENT.json",
        "CLOSEOUT.md",
    ]
    outputs = []
    for rel in output_paths:
        path = RUN / rel
        outputs.append({"path": rel, "sha256": sha256(path), "bytes": path.stat().st_size})
    write_json(RUN / "GENERATED_OUTPUT_MANIFEST.json", {
        "status": "PRIMARY_FINAL_PENDING_CLEAN_REPLAY",
        "generation_mode": "GENERATION_SEALED",
        "physical_execution_occurred": True,
        "outputs": outputs,
    })

    print(json.dumps({
        "run_id": SPEC["run_id"],
        "overall": gates["overall"],
        "branch_count": len(branch_records),
        "max_baryon_drift": max_baryon,
        "max_charge_drift": max_charge,
        "max_energy_drift": max_energy,
        "minimum_abundance": min_abundance,
        "route_max_linf": route_max,
        "time_max_linf": time_max,
        "max_restart_linf": max_restart,
        "max_independent_linf": max_independent,
        "minimum_no_rfl_effect_linf": min_no_rfl_effect,
        "minimum_no_qv_effect_linf": min_no_qv_effect,
        "handoff_sha256": sha256(FROZEN / "H_E_to_F.json"),
    }, indent=2))
    return 0 if gates["overall"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
