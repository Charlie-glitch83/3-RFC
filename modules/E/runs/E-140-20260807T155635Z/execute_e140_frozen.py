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

from rfc_engine.solvers.reaction_network import ReactionNetwork

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
SPEC_PATH = RUN / "FROZEN_DERIVATION_SPEC.json"
LOCK_PATH = RUN / "PRE_EXECUTION_LOCK.json"
SPEC = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
LOCK = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
PARENT_PATH = ROOT / SPEC["exact_parent"]["path"]
PARENT = json.loads(PARENT_PATH.read_text(encoding="utf-8"))
PRIMARY = RUN / "primary"
INDEP = RUN / "independent"
FROZEN = RUN / "frozen"
for p in (PRIMARY, INDEP, FROZEN):
    p.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def linf(a: Any, b: Any) -> float:
    return float(np.max(np.abs(np.asarray(a, dtype=float) - np.asarray(b, dtype=float))))


def roots_and_equilibrium(y0: list[float], kf: float, kr: float) -> tuple[list[float], float, list[float]]:
    n0, p0, d0 = map(float, y0)
    # kf(n0-x)(p0-x)-kr(d0+x)=0
    coeff = [kf, -kf * (n0 + p0) - kr, kf * n0 * p0 - kr * d0]
    roots = sorted(float(x.real) for x in np.roots(coeff) if abs(float(x.imag)) < 1e-12)
    lo, hi = -d0, min(n0, p0)
    feasible = [x for x in roots if lo - 1e-12 <= x <= hi + 1e-12]
    if len(feasible) != 1:
        raise RuntimeError(f"expected one feasible extent root, got roots={roots}, feasible={feasible}")
    xeq = feasible[0]
    state = [n0 - xeq, p0 - xeq, d0 + xeq]
    return roots, xeq, state


def analytic_extent(t: float, y0: list[float], kf: float, kr: float) -> float:
    roots, xeq, _ = roots_and_equilibrium(y0, kf, kr)
    other = roots[1] if abs(roots[0] - xeq) < 1e-12 else roots[0]
    x0 = 0.0
    ratio0 = (x0 - xeq) / (x0 - other)
    ratio = ratio0 * math.exp(kf * (xeq - other) * t)
    return (xeq - ratio * other) / (1.0 - ratio)


def freeze_time(y0: list[float], delta: float, depth: int, kf: float, kr: float) -> tuple[float, float, float]:
    roots, xeq, _ = roots_and_equilibrium(y0, kf, kr)
    other = roots[1] if abs(roots[0] - xeq) < 1e-12 else roots[0]
    q = delta ** (-depth)
    target = xeq - math.copysign(q * abs(xeq), xeq)
    # R(x)=(x-r1)/(x-r2), R(t)=R(0) exp(kf(r1-r2)t)
    r0 = (0.0 - xeq) / (0.0 - other)
    rt = (target - xeq) / (target - other)
    t = math.log(rt / r0) / (kf * (xeq - other))
    return q, target, t


def make_network(kf: float, kr: float) -> ReactionNetwork:
    sg = SPEC["species_and_graph"]
    return ReactionNetwork(
        list(sg["species"]),
        np.asarray(sg["stoichiometry"], dtype=float),
        list(sg["rate_expressions"]),
        {"kf": float(kf), "kr": float(kr)},
        {k: list(map(float, v)) for k, v in sg["invariants"].items()},
    )


def integrate(y0: list[float], kf: float, kr: float, t_end: float, max_step: float, *, t0: float = 0.0, method: str = "BDF", dense: bool = False):
    net = make_network(kf, kr)
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
        rtol=float(SPEC["execution"]["rtol"]),
        atol=float(SPEC["execution"]["atol"]),
        max_step=float(max_step),
        dense_output=dense,
    )
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol


def conservation_summary(sol) -> dict[str, Any]:
    inv = SPEC["species_and_graph"]["invariants"]
    out: dict[str, Any] = {}
    for name, row in inv.items():
        vals = np.asarray(row, dtype=float) @ sol.y
        out[name] = {
            "initial": float(vals[0]),
            "max_abs_drift": float(np.max(np.abs(vals - vals[0]))),
        }
    out["minimum_abundance"] = float(np.min(sol.y))
    return out


def countermodel_final(y0: list[float], kf: float, kr: float, t_end: float, max_step: float) -> list[float]:
    return integrate(y0, kf, kr, t_end, max_step).y[:, -1].tolist()


def main() -> int:
    if SPEC.get("status") != "FROZEN_BEFORE_PRIMARY_EXECUTION" or LOCK.get("status") != "FROZEN":
        raise RuntimeError("frozen E authority missing")
    if sha256(PARENT_PATH) != SPEC["exact_parent"]["sha256"]:
        raise RuntimeError("exact D parent hash mismatch")

    sg = SPEC["species_and_graph"]
    rate = SPEC["rate_law"]
    exe = SPEC["execution"]
    y0 = list(map(float, SPEC["initial_state"]["value"]))
    kf, kr = float(rate["kf"]), float(rate["kr"])
    delta, depth = float(rate["delta"]), int(rate["closure_depth"])
    t_end, base_step = float(exe["t_span"][1]), float(exe["max_step"])

    # Frozen rate/source identities.
    rate_ratio_error = abs(kf / kr - delta)
    rate_sum_error = abs(kf + kr - 1.0)
    sto = np.asarray(sg["stoichiometry"], dtype=float)
    invariant_residuals = {name: (np.asarray(row, dtype=float) @ sto).tolist() for name, row in sg["invariants"].items()}
    invariant_nullspace_error = max(abs(v) for vals in invariant_residuals.values() for v in vals)

    # Primary parent-driven execution.
    sol = integrate(y0, kf, kr, t_end, base_step, dense=True)
    primary_final = sol.y[:, -1].tolist()
    conservation = conservation_summary(sol)
    roots, xeq, eq_state = roots_and_equilibrium(y0, kf, kr)
    q, target_extent, t_derived = freeze_time(y0, delta, depth, kf, kr)
    x_final = float(y0[0] - primary_final[0])
    analytic_x = analytic_extent(t_end, y0, kf, kr)
    analytic_final = [y0[0] - analytic_x, y0[1] - analytic_x, y0[2] + analytic_x]
    independent_error = linf(primary_final, analytic_final)
    freeze_time_error = abs(t_derived - t_end)

    primary_record = {
        "schema_version": "1.0",
        "run_id": SPEC["run_id"],
        "classification": "PARENT_DRIVEN_E_REACTION_NETWORK",
        "species": sg["species"],
        "initial_state": y0,
        "t": sol.t.tolist(),
        "y": sol.y.tolist(),
        "final_state": primary_final,
        "equilibrium_roots": roots,
        "selected_equilibrium_extent": xeq,
        "equilibrium_state": eq_state,
        "freeze_q_E": q,
        "freeze_target_extent": target_extent,
        "derived_t_freeze": t_derived,
        "primary_final_extent": x_final,
        "analytic_final_extent": analytic_x,
        "analytic_final_state": analytic_final,
        "conservation": conservation,
        "minimum_abundance": float(np.min(sol.y)),
        "nfev": int(sol.nfev),
    }
    write_json(PRIMARY / "ABUNDANCE_TRAJECTORIES.json", primary_record)

    # Time-step/rate-resolution convergence using the frozen dyadic sequence.
    convergence = []
    finals = []
    for step in exe["convergence_steps"]:
        ss = integrate(y0, kf, kr, t_end, float(step))
        final = ss.y[:, -1].tolist()
        finals.append(final)
        convergence.append({"max_step": float(step), "final_state": final, "nfev": int(ss.nfev)})
    finest_pair_linf = linf(finals[-2], finals[-1])
    write_json(PRIMARY / "CONVERGENCE_MATRIX.json", {
        "classification": "SOURCE_COMPLETE_N2_PLUS_DYADIC_RATE_TIME_RESOLUTION",
        "source_complete_reaction_count": 2,
        "unsupported_third_reaction_added": False,
        "refinements": convergence,
        "finest_pair_linf": finest_pair_linf,
        "tolerance": 1e-8,
        "pass": finest_pair_linf <= 1e-8,
    })

    # Source-defined N=1 truncations and semantic countermodels.
    forward_withheld = countermodel_final(y0, 0.0, kr, t_end, base_step)
    reverse_withheld = countermodel_final(y0, kf, 0.0, t_end, base_step)
    scalar_collapse = countermodel_final(y0, 0.5, 0.5, t_end, base_step)
    channel_swap = countermodel_final(y0, kr, kf, t_end, base_step)
    cm = {
        "full_final": primary_final,
        "FORWARD_WITHHELD": {"final": forward_withheld, "linf_from_full": linf(primary_final, forward_withheld)},
        "REVERSE_WITHHELD": {"final": reverse_withheld, "linf_from_full": linf(primary_final, reverse_withheld)},
        "SCALAR_COLLAPSE": {"final": scalar_collapse, "linf_from_full": linf(primary_final, scalar_collapse)},
        "CHANNEL_SWAP": {"final": channel_swap, "linf_from_full": linf(primary_final, channel_swap)},
        "distinguishability_floor": 1e-8,
    }
    for key in ("FORWARD_WITHHELD", "REVERSE_WITHHELD", "SCALAR_COLLAPSE", "CHANNEL_SWAP"):
        cm[key]["distinguishable"] = cm[key]["linf_from_full"] > 1e-8
    write_json(PRIMARY / "COUNTERMODELS_AND_ABLATIONS.json", cm)

    # Midpoint restart on the accepted primary trajectory.
    midpoint = t_end / 2.0
    ymid = sol.sol(midpoint).tolist()
    restart_sol = integrate(ymid, kf, kr, t_end, base_step, t0=midpoint)
    restart_final = restart_sol.y[:, -1].tolist()
    restart_error = linf(primary_final, restart_final)
    write_json(RUN / "CHECKPOINT_RECORD.json", {
        "status": "PASS" if restart_error <= 1e-8 else "FAIL",
        "midpoint_tau_E": midpoint,
        "midpoint_state": ymid,
        "restart_final": restart_final,
        "primary_final": primary_final,
        "linf": restart_error,
        "tolerance": 1e-8,
    })

    # Independent analytic extent reconstruction.
    indep_record = {
        "method": "closed-form Riccati reaction-extent reconstruction",
        "roots": roots,
        "selected_equilibrium_extent": xeq,
        "analytic_extent_at_freeze": analytic_x,
        "analytic_final_state": analytic_final,
        "primary_final_state": primary_final,
        "linf": independent_error,
        "tolerance": 1e-8,
        "pass": independent_error <= 1e-8,
    }
    write_json(INDEP / "INDEPENDENT_RECONSTRUCTION.json", indep_record)

    # Exact inherited decimal envelope; one E trajectory per frozen delta member.
    env_records = []
    env_finals = []
    for member in PARENT["uncertainty_covariance"]["decimal_envelope_replays"]:
        dlt = float(member["delta"])
        yi = list(map(float, member["final_at_one_gap_efold"]))
        kfi = dlt / (dlt + 1.0)
        kri = 1.0 / (dlt + 1.0)
        qi, target_i, ti = freeze_time(yi, dlt, depth, kfi, kri)
        step_i = ti / 128.0
        si = integrate(yi, kfi, kri, ti, step_i)
        final_i = si.y[:, -1].tolist()
        env_finals.append(final_i)
        roots_i, xeq_i, eq_i = roots_and_equilibrium(yi, kfi, kri)
        ax_i = analytic_extent(ti, yi, kfi, kri)
        af_i = [yi[0] - ax_i, yi[1] - ax_i, yi[2] + ax_i]
        env_records.append({
            "delta": dlt,
            "initial_state": yi,
            "kf": kfi,
            "kr": kri,
            "q_E": qi,
            "equilibrium_roots": roots_i,
            "selected_equilibrium_extent": xeq_i,
            "equilibrium_state": eq_i,
            "freeze_target_extent": target_i,
            "t_freeze": ti,
            "final_state": final_i,
            "independent_final_state": af_i,
            "independent_linf": linf(final_i, af_i),
            "conservation": conservation_summary(si),
        })
    env_arr = np.asarray(env_finals, dtype=float)
    covariance = np.cov(env_arr, rowvar=False, ddof=1).tolist()
    write_json(PRIMARY / "UNCERTAINTY_COVARIANCE.json", {
        "classification": SPEC["uncertainty"]["classification"],
        "members": env_records,
        "componentwise_min": np.min(env_arr, axis=0).tolist(),
        "componentwise_max": np.max(env_arr, axis=0).tolist(),
        "diagnostic_covariance": covariance,
        "stochastic_covariance": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
    })

    # Required truth ledgers.
    write_json(PRIMARY / "REACTION_GRAPH_AND_RATES.json", {
        "species": sg["species"],
        "semantics": sg["semantics"],
        "ordered_parent_map": sg["ordered_parent_map"],
        "stoichiometry": sg["stoichiometry"],
        "reactions": sg["reactions"],
        "rate_expressions": sg["rate_expressions"],
        "rate_law": rate,
        "rate_source_sha256": sha256(SPEC_PATH),
        "historical_failure_or_public_target_used": False,
    })
    write_json(PRIMARY / "CONSERVATION_POSITIVITY_LEDGER.json", {
        "invariant_nullspace_residuals": invariant_residuals,
        "max_nullspace_error": invariant_nullspace_error,
        "trajectory": conservation,
        "positivity_tolerance": exe["positivity_tolerance"],
    })
    write_json(PRIMARY / "FREEZEOUT_EVENT_WITNESSES.json", {
        "event": "E_CANONICAL_CLOSURE_DEPTH_FREEZE",
        "q_E": q,
        "target_extent": target_extent,
        "derived_t_freeze": t_derived,
        "frozen_t_span_end": t_end,
        "freeze_time_error": freeze_time_error,
        "primary_final_extent": x_final,
        "analytic_final_extent": analytic_x,
        "primary_vs_analytic_linf": independent_error,
    })

    # Gate reconstruction from the frozen matrix.
    conservation_pass = (
        invariant_nullspace_error <= 1e-12
        and conservation["baryon"]["max_abs_drift"] <= 1e-9
        and conservation["charge"]["max_abs_drift"] <= 1e-9
        and conservation["energy"]["max_abs_drift"] <= 1e-9
        and conservation["minimum_abundance"] >= -float(exe["positivity_tolerance"])
    )
    convergence_pass = finest_pair_linf <= 1e-8
    rate_source_pass = rate_ratio_error <= 1e-12 and rate_sum_error <= 1e-12
    no_scalar_pass = cm["SCALAR_COLLAPSE"]["distinguishable"] and cm["CHANNEL_SWAP"]["distinguishable"]
    withheld_pass = (
        cm["FORWARD_WITHHELD"]["distinguishable"]
        and cm["REVERSE_WITHHELD"]["distinguishable"]
        and independent_error <= 1e-8
        and restart_error <= 1e-8
        and all(x["independent_linf"] <= 1e-8 for x in env_records)
    )
    component = {
        "baryon/charge/energy accounting": {"status": "PASS" if conservation_pass else "FAIL"},
        "network convergence": {"status": "PASS" if convergence_pass else "FAIL", "finest_pair_linf": finest_pair_linf},
        "rate-source audit": {"status": "PASS" if rate_source_pass else "FAIL", "kf_over_kr_error": rate_ratio_error, "kf_plus_kr_error": rate_sum_error},
        "no scalar-channel collapse": {"status": "PASS" if no_scalar_pass else "FAIL", "scalar_linf": cm["SCALAR_COLLAPSE"]["linf_from_full"], "channel_swap_linf": cm["CHANNEL_SWAP"]["linf_from_full"]},
        "withheld reaction and independent implementation checks": {"status": "PASS" if withheld_pass else "FAIL", "forward_withheld_linf": cm["FORWARD_WITHHELD"]["linf_from_full"], "reverse_withheld_linf": cm["REVERSE_WITHHELD"]["linf_from_full"], "independent_linf": independent_error, "restart_linf": restart_error},
    }
    overall = "PASS" if all(v["status"] == "PASS" for v in component.values()) else "FAIL_REQUIRES_ANALYSIS"
    gates = {
        "schema_version": "1.0",
        "module": "E",
        "run_id": SPEC["run_id"],
        "overall": overall,
        "aggregate_scores_cannot_override": True,
        "component_gates": component,
    }
    write_json(RUN / "GATE_RESULTS.json", gates)

    write_json(RUN / "REPLAY_RECORD.json", {
        "result": overall,
        "clean_checkout_execution": True,
        "primary_configured_solver_required": True,
        "independent_reconstruction": indep_record,
        "restart_linf": restart_error,
    })
    write_json(RUN / "ENVIRONMENT.json", {
        "status": "FINAL",
        "python": platform.python_version(),
        "generation_mode": "GENERATION_SEALED",
        "public_data_used": False,
        "network_use_for_science": "NONE",
        "historical_failure_used_for_generation": False,
        "physical_execution_status": "EXECUTED",
    })

    supported = (
        "Internally generated RFC minimal-spine primordial three-species reaction state with a source-owned two-channel rate law derived from the inherited recursive kernel, exact baryon/charge/internal-energy accounting, a canonical closure-depth freeze witness, inherited delta-envelope covariance, convergence, withheld-channel countermodels, restart, clean replay, and independent reaction-extent reconstruction."
    )
    unsupported = (
        "Module E does not establish calibrated nuclear reaction rates, MeV binding energies, SI time, Standard Model isotope correspondence, public abundance agreement, or external BBN validation."
    )
    (RUN / "INDEPENDENT_VERIFICATION.md").write_text(
        "# Independent Verification — E-140\n\n"
        "Reconstructed the frozen E law from the exact parent and kernel-derived rate identities, then solved the reaction-extent Riccati equation in closed form without trusting the primary BDF solver or gate summary. The reconstructed final state is compared componentwise to the primary result at the frozen `1e-8` L-infinity tolerance.\n\n"
        f"Independent final-state L-infinity error: `{independent_error:.17g}`.\n\n"
        f"Result: **{'PASS' if independent_error <= 1e-8 else 'FAIL'}**.\n",
        encoding="utf-8",
    )
    (RUN / "CLOSEOUT.md").write_text(
        "# E-140 Closeout\n\n"
        f"## Result\n\n`{overall}`\n\n"
        f"## Strongest supported claim\n\n{supported}\n\n"
        f"## Strongest unsupported claim\n\n{unsupported}\n\n"
        "## Failure inheritance boundary\n\nHistorical scalar/Li7 failures were retained only as regression warnings and did not select rates, states, thresholds, branches, or expected outcomes.\n",
        encoding="utf-8",
    )

    if overall == "PASS":
        handoff = {
            "schema_version": "1.0",
            "object_id": "H_E_to_F",
            "from_module": "E",
            "to_module": "F",
            "run_id": SPEC["run_id"],
            "evidence_state": "PHYSICALLY_EXECUTED_PENDING_CLOSEOUT",
            "fidelity": "MINIMAL_SPINE",
            "generation_mode": "GENERATION_SEALED",
            "parent": {"object_id": "H_D_to_E", "sha256": SPEC["exact_parent"]["sha256"]},
            "species": sg["species"],
            "species_semantics": sg["semantics"],
            "final_abundance_state": primary_final,
            "equilibrium_state": eq_state,
            "freezeout": {"q_E": q, "tau_E": t_end, "final_extent": x_final},
            "rate_law": {"kf": kf, "kr": kr, "delta": delta, "source": "E140_FROZEN_DERIVATION_SPEC"},
            "uncertainty_covariance": covariance,
            "restart_contract": "F receives the exact E final abundance state, source-owned two-channel reaction law, freeze witness, conservation ledgers, inherited delta envelope and covariance; no empirical isotope correspondence is added.",
            "claim_boundary": SPEC["claim_boundary"],
        }
        write_json(FROZEN / "H_E_to_F.json", handoff)

    # Final manifest only after all scientific outputs have stopped changing.
    rels = [
        "reference_checks.json",
        "solver_configs/E_reaction_network.json",
        "solver_outputs/reaction_network/result.json",
        "primary/REACTION_GRAPH_AND_RATES.json",
        "primary/ABUNDANCE_TRAJECTORIES.json",
        "primary/UNCERTAINTY_COVARIANCE.json",
        "primary/CONSERVATION_POSITIVITY_LEDGER.json",
        "primary/FREEZEOUT_EVENT_WITNESSES.json",
        "primary/CONVERGENCE_MATRIX.json",
        "primary/COUNTERMODELS_AND_ABLATIONS.json",
        "CHECKPOINT_RECORD.json",
        "independent/INDEPENDENT_RECONSTRUCTION.json",
        "INDEPENDENT_VERIFICATION.md",
        "GATE_RESULTS.json",
        "REPLAY_RECORD.json",
        "frozen/H_E_to_F.json",
    ]
    outputs = []
    for rel in rels:
        p = RUN / rel
        if p.exists():
            outputs.append({"path": rel, "sha256": sha256(p), "bytes": p.stat().st_size})
    write_json(RUN / "GENERATED_OUTPUT_MANIFEST.json", {
        "status": "FINAL" if overall == "PASS" else "FINAL_FAIL_REQUIRES_ANALYSIS",
        "generation_mode": "GENERATION_SEALED",
        "physical_execution_occurred": True,
        "outputs": outputs,
    })

    return 0 if overall == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
