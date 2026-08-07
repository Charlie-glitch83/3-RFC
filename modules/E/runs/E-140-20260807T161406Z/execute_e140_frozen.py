#!/usr/bin/env python3
import hashlib
import itertools
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

from rfc_engine.solvers.reaction_network import ReactionNetwork

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
SPEC_PATH = RUN / "FROZEN_DERIVATION_SPEC.json"
SOURCE_PATH = RUN / "SOURCE_REGISTER.json"
D_SPEC_PATH = ROOT / "modules/D/runs/D-130-20260807T053432Z/FROZEN_DERIVATION_SPEC.json"
D_UNC_PATH = ROOT / "modules/D/runs/D-130-20260807T053432Z/primary/UNCERTAINTY_COVARIANCE.json"


def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def linf(a, b):
    return float(np.max(np.abs(np.asarray(a, dtype=float) - np.asarray(b, dtype=float))))


spec = json.loads(SPEC_PATH.read_text())
source = json.loads(SOURCE_PATH.read_text())
dspec = json.loads(D_SPEC_PATH.read_text())
dunc = json.loads(D_UNC_PATH.read_text())

if spec.get("status") != "FROZEN_BEFORE_PRIMARY_EXECUTION":
    raise SystemExit("HARD STOP: E frozen derivation is not execution-authorized")
if spec["exact_parent"]["sha256"] != "199b89ccbdea06714a5539c5d3baf53cd332e5b65922676c6c8d37cc7c824af8":
    raise SystemExit("HARD STOP: D->E parent hash changed")
if source.get("public_data_declaration") != "NONE":
    raise SystemExit("HARD STOP: generation firewall declaration changed")

sg = spec["species_and_graph"]
rate = spec["rate_law"]
clock = spec["clock_and_interval"]
branches = spec["parent_to_E_interface"]["branch_family"]

species = sg["species"]
S = np.asarray(sg["stoichiometry"], dtype=float)
baryon = np.asarray(sg["baryon"], dtype=float)
charge = np.asarray(sg["charge"], dtype=float)
kf = float(rate["kf"])
kr = float(rate["kr"])
g = kf
energy = np.asarray(spec["intrinsic_energy_ledger"]["energy_vector"], dtype=float)
t0, tend = map(float, clock["t_span"])
base_step = float(clock["max_step"])
rtol = 1e-9
atol = 1e-12

# Frozen rate/source identities.
d_g = float(dspec["transport_derivation"]["gap_g_C"])
d_a = float(dspec["transport_derivation"]["edge_rate_a"])
rate_source_checks = {
    "kf_equals_parent_g_C": abs(kf - d_g) <= 1e-12,
    "kr_equals_parent_edge_rate_a": abs(kr - d_a) <= 1e-12,
    "g_C_equals_3a": abs(kf - 3.0 * kr) <= 1e-12,
    "public_data_declaration_none": source.get("public_data_declaration") == "NONE",
}
rate_source_pass = all(rate_source_checks.values())


def build_network(local_kf, local_kr, routes=1, stoich=None):
    if stoich is None:
        if routes == 1:
            matrix = S.copy()
            expressions = ["kf*n*p", "kr*d"]
        else:
            columns = []
            expressions = []
            for _ in range(routes):
                columns.append([-1.0, -1.0, 1.0])
                expressions.append(f"(kf/{routes})*n*p")
            for _ in range(routes):
                columns.append([1.0, 1.0, -1.0])
                expressions.append(f"(kr/{routes})*d")
            matrix = np.asarray(columns, dtype=float).T
    else:
        matrix = np.asarray(stoich, dtype=float)
        expressions = ["kf*n*p", "kr*d"]
    inv = {
        "baryon": baryon.tolist(),
        "charge": charge.tolist(),
        "intrinsic_energy": energy.tolist(),
    }
    return ReactionNetwork(species, matrix, expressions, {"kf": local_kf, "kr": local_kr}, inv), matrix


def integrate(y0, local_kf=kf, local_kr=kr, max_step=base_step, method="BDF", routes=1, start=t0, stop=tend):
    net, matrix = build_network(local_kf, local_kr, routes=routes)
    rate_fn = net._rate_function()
    sol = solve_ivp(
        lambda t, y: matrix @ rate_fn(y),
        (start, stop),
        np.asarray(y0, dtype=float),
        method=method,
        rtol=rtol if method == "BDF" else 1e-12,
        atol=atol if method == "BDF" else 1e-14,
        max_step=max_step,
        dense_output=True,
    )
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol


def summarize(sol, y0, local_kf=kf, local_kr=kr):
    b = baryon @ sol.y
    q = charge @ sol.y
    e = energy @ sol.y
    flow = local_kf * sol.y[0] * sol.y[1] - local_kr * sol.y[2]
    threshold = abs(float(flow[0])) / math.e
    indices = np.where(np.abs(flow) <= threshold)[0]
    freeze_index = int(indices[0]) if len(indices) else None
    return {
        "initial_state": list(map(float, y0)),
        "t": sol.t.tolist(),
        "y": sol.y.tolist(),
        "final_state": sol.y[:, -1].tolist(),
        "minimum_abundance": float(np.min(sol.y)),
        "max_baryon_drift": float(np.max(np.abs(b - b[0]))),
        "max_charge_drift": float(np.max(np.abs(q - q[0]))),
        "max_intrinsic_energy_drift": float(np.max(np.abs(e - e[0]))),
        "initial_net_flow": float(flow[0]),
        "final_net_flow": float(flow[-1]),
        "freezeout_threshold_abs_flow": threshold,
        "freezeout_event_found": freeze_index is not None,
        "freezeout_event_tau_E": float(sol.t[freeze_index]) if freeze_index is not None else None,
        "freezeout_event_state": sol.y[:, freeze_index].tolist() if freeze_index is not None else None,
    }


primary_records = []
convergence_records = []
route_records = []
restart_records = []
withheld_records = []
independent_records = []
branch_finals = []

for br in branches:
    y0 = list(map(float, br["initial_state"]))
    sol = integrate(y0)
    summary = summarize(sol, y0)
    summary.update({"branch_id": br["branch_id"], "assignment": br["assignment"]})
    primary_records.append(summary)
    branch_finals.append(summary["final_state"])

    step_finals = []
    for step in clock["convergence_steps"]:
        step_sol = integrate(y0, max_step=float(step))
        step_finals.append(step_sol.y[:, -1].tolist())
    conv_err = linf(step_finals[-2], step_finals[-1])
    convergence_records.append({
        "branch_id": br["branch_id"],
        "max_steps": list(map(float, clock["convergence_steps"])),
        "final_states": step_finals,
        "finest_pair_linf": conv_err,
        "pass": conv_err <= 1e-8,
    })

    route_finals = []
    for routes in (1, 2, 4):
        route_sol = integrate(y0, routes=routes)
        route_finals.append(route_sol.y[:, -1].tolist())
    route_err = max(linf(route_finals[0], route_finals[1]), linf(route_finals[0], route_finals[2]))
    route_records.append({
        "branch_id": br["branch_id"],
        "route_counts": [1, 2, 4],
        "final_states": route_finals,
        "max_linf_vs_single_route": route_err,
        "pass": route_err <= 1e-8,
    })

    midpoint = 0.5 * (t0 + tend)
    ymid = sol.sol(midpoint)
    restarted = integrate(ymid, start=midpoint, stop=tend)
    restart_err = linf(summary["final_state"], restarted.y[:, -1])
    restart_records.append({
        "branch_id": br["branch_id"],
        "checkpoint_tau_E": midpoint,
        "checkpoint_state": ymid.tolist(),
        "restart_final_state": restarted.y[:, -1].tolist(),
        "linf": restart_err,
        "pass": restart_err <= 1e-8,
    })

    forward_withheld = integrate(y0, local_kf=0.0, local_kr=kr).y[:, -1]
    reverse_withheld = integrate(y0, local_kf=kf, local_kr=0.0).y[:, -1]
    f_diff = linf(summary["final_state"], forward_withheld)
    r_diff = linf(summary["final_state"], reverse_withheld)
    withheld_records.append({
        "branch_id": br["branch_id"],
        "forward_withheld_final": forward_withheld.tolist(),
        "reverse_withheld_final": reverse_withheld.tolist(),
        "forward_withheld_linf": f_diff,
        "reverse_withheld_linf": r_diff,
        "pass": f_diff > 1e-6 and r_diff > 1e-6,
    })

    n0, p0, d0 = y0
    reduced = solve_ivp(
        lambda t, x: [kf * (n0 - x[0]) * (p0 - x[0]) - kr * (d0 + x[0])],
        (t0, tend),
        [0.0],
        method="DOP853",
        rtol=1e-12,
        atol=1e-14,
        max_step=base_step / 2.0,
    )
    if not reduced.success:
        raise RuntimeError(reduced.message)
    extent = float(reduced.y[0, -1])
    independent_final = [n0 - extent, p0 - extent, d0 + extent]
    indep_err = linf(summary["final_state"], independent_final)
    independent_records.append({
        "branch_id": br["branch_id"],
        "final_extent": extent,
        "final_state": independent_final,
        "linf_vs_primary": indep_err,
        "pass": indep_err <= 1e-8,
    })

# Execute the symmetry quotient representative through the same physical law.
central_y0 = list(map(float, spec["parent_to_E_interface"]["central_symmetry_quotient_initial_state"]))
central_sol = integrate(central_y0)
central_record = summarize(central_sol, central_y0)

# Countermodels: branch scalar collapse and explicit conservation break.
initial_charges = [float(br["initial_charge"]) for br in branches]
final_charges = [float(charge @ np.asarray(rec["final_state"])) for rec in primary_records]
branch_charge_span = max(initial_charges) - min(initial_charges)
central_final = np.asarray(central_record["final_state"])
branch_mean_final = np.mean(np.asarray(branch_finals), axis=0)
scalar_collapse_difference = linf(central_final, branch_mean_final)
scalar_collapse_rejected = branch_charge_span > 1e-6 and scalar_collapse_difference > 1e-8
S_bad = S.copy()
S_bad[1, 0] = -0.9
b_bad = baryon @ S_bad
q_bad = charge @ S_bad
charge_break_rejected = bool(np.max(np.abs(b_bad)) > 1e-12 or np.max(np.abs(q_bad)) > 1e-12)
countermodels = {
    "scalar_collapse": {
        "branch_initial_charge_span": branch_charge_span,
        "branch_final_charges": final_charges,
        "central_quotient_final": central_final.tolist(),
        "branch_mean_final": branch_mean_final.tolist(),
        "central_vs_branch_mean_linf": scalar_collapse_difference,
        "rejected": scalar_collapse_rejected,
    },
    "charge_break": {
        "perturbed_stoichiometry": S_bad.tolist(),
        "baryon_nullspace_residual": b_bad.tolist(),
        "charge_nullspace_residual": q_bad.tolist(),
        "rejected": charge_break_rejected,
    },
    "withheld_channels": withheld_records,
    "public_or_historical_target_used": False,
}

# Inherited delta-envelope x six symmetry branches.
envelope_records = []
envelope_finals = []
for member in dunc["decimal_envelope_replays"]:
    delta = float(member["delta"])
    gg = float(member["g_C"])
    aa = gg / 3.0
    if abs(aa - 1.0 / (delta + 2.0)) > 1e-12:
        raise SystemExit("HARD STOP: inherited delta envelope violates a=1/(delta+2)")
    parent = list(map(float, member["final_at_one_gap_efold"]))
    local_end = 1.0 / aa
    local_step = local_end / 128.0
    for n_idx, p_idx in itertools.permutations(range(3), 2):
        r_idx = next(i for i in range(3) if i not in (n_idx, p_idx))
        y0 = [parent[n_idx] + 0.5 * parent[r_idx], parent[p_idx] + 0.5 * parent[r_idx], 0.0]
        # Inline local integration because the interval and rates are envelope-specific.
        net, matrix = build_network(gg, aa, routes=1)
        fn = net._rate_function()
        sol = solve_ivp(
            lambda t, y: matrix @ fn(y),
            (0.0, local_end),
            np.asarray(y0, dtype=float),
            method="BDF",
            rtol=rtol,
            atol=atol,
            max_step=local_step,
        )
        if not sol.success:
            raise RuntimeError(sol.message)
        final = sol.y[:, -1].tolist()
        envelope_finals.append(final)
        envelope_records.append({
            "delta": delta,
            "branch_id": f"N{n_idx}_P{p_idx}_R{r_idx}",
            "g_C": gg,
            "a": aa,
            "t_end": local_end,
            "initial_state": y0,
            "final_state": final,
            "minimum_abundance": float(np.min(sol.y)),
        })

branch_arr = np.asarray(branch_finals, dtype=float)
env_arr = np.asarray(envelope_finals, dtype=float)
branch_cov = np.cov(branch_arr, rowvar=False, ddof=1)
env_cov = np.cov(env_arr, rowvar=False, ddof=1)

conservation_pass = all(
    rec["minimum_abundance"] >= -1e-12
    and rec["max_baryon_drift"] <= 1e-9
    and rec["max_charge_drift"] <= 1e-9
    and rec["max_intrinsic_energy_drift"] <= 1e-9
    and rec["freezeout_event_found"]
    for rec in primary_records
)
convergence_pass = all(r["pass"] for r in convergence_records) and all(r["pass"] for r in route_records)
withheld_independent_pass = (
    all(r["pass"] for r in withheld_records)
    and all(r["pass"] for r in restart_records)
    and all(r["pass"] for r in independent_records)
)
no_scalar_pass = scalar_collapse_rejected and charge_break_rejected

component_gates = {
    "baryon/charge/energy accounting": conservation_pass,
    "network convergence": convergence_pass,
    "rate-source audit": rate_source_pass,
    "no scalar-channel collapse": no_scalar_pass,
    "withheld reaction and independent implementation checks": withheld_independent_pass,
}
overall = all(component_gates.values())

primary_dir = RUN / "primary"
dump(primary_dir / "REACTION_GRAPH_AND_RATES.json", {
    "species": species,
    "stoichiometry": S.tolist(),
    "rate_expressions": sg["rate_expressions"],
    "parameters": {"kf": kf, "kr": kr},
    "source_identity_checks": rate_source_checks,
    "generation_mode": "GENERATION_SEALED",
})
dump(primary_dir / "BRANCH_FAMILY_ABUNDANCE_TRAJECTORIES.json", {
    "branch_count": len(primary_records),
    "branches": primary_records,
    "central_symmetry_quotient": central_record,
})
dump(primary_dir / "CONSERVATION_POSITIVITY_LEDGER.json", {
    "branches": [{
        "branch_id": r["branch_id"],
        "minimum_abundance": r["minimum_abundance"],
        "max_baryon_drift": r["max_baryon_drift"],
        "max_charge_drift": r["max_charge_drift"],
        "max_intrinsic_energy_drift": r["max_intrinsic_energy_drift"],
    } for r in primary_records],
    "energy_vector": energy.tolist(),
    "pass": conservation_pass,
})
dump(primary_dir / "FREEZEOUT_EVENT_WITNESSES.json", {
    "definition": clock["freezeout_witness"],
    "branches": [{
        "branch_id": r["branch_id"],
        "initial_net_flow": r["initial_net_flow"],
        "threshold": r["freezeout_threshold_abs_flow"],
        "tau_E": r["freezeout_event_tau_E"],
        "state": r["freezeout_event_state"],
        "found": r["freezeout_event_found"],
    } for r in primary_records],
})
dump(primary_dir / "ISOTOPE_COVARIANCE.json", {
    "classification": "STRUCTURAL_BRANCH_COVARIANCE_NOT_STOCHASTIC",
    "branch_mean": np.mean(branch_arr, axis=0).tolist(),
    "branch_covariance": branch_cov.tolist(),
    "stochastic_covariance": np.zeros((3, 3)).tolist(),
})
dump(RUN / "UNCERTAINTY_COVARIANCE.json", {
    "classification": "BRANCH_PLUS_INHERITED_SOURCE_DECIMAL_ENVELOPE",
    "envelope_member_count": len(envelope_records),
    "envelope_replays": envelope_records,
    "combined_mean": np.mean(env_arr, axis=0).tolist(),
    "combined_covariance": env_cov.tolist(),
    "stochastic_covariance": np.zeros((3, 3)).tolist(),
})
dump(RUN / "CONVERGENCE_MATRIX.json", {
    "time_step_refinement": convergence_records,
    "exact_route_splitting": route_records,
    "pass": convergence_pass,
})
dump(RUN / "COUNTERMODELS_AND_ABLATIONS.json", {
    **countermodels,
    "pass": no_scalar_pass and all(r["pass"] for r in withheld_records),
})
dump(RUN / "CHECKPOINT_RECORD.json", {
    "checkpoint_kind": "MIDPOINT_RESTART",
    "branches": restart_records,
    "pass": all(r["pass"] for r in restart_records),
})
dump(RUN / "independent/INDEPENDENT_RECONSTRUCTION.json", {
    "method": "DOP853_REDUCED_ONE_DIMENSIONAL_REACTION_EXTENT",
    "branches": independent_records,
    "pass": all(r["pass"] for r in independent_records),
})

iv_text = "# Independent Verification — E-140\n\n"
iv_text += "The independent verifier reconstructed all six symmetry-equivalent parent-role branches from the frozen interface, reduced each reversible three-species system to one reaction extent, and integrated that scalar law with DOP853 at tighter tolerances. It did not trust the primary BDF gate summaries.\n\n"
iv_text += f"Maximum branchwise independent-vs-primary L-infinity error: {max(r['linf_vs_primary'] for r in independent_records):.16e}.\n\n"
iv_text += f"Independent reconstruction result: {'PASS' if all(r['pass'] for r in independent_records) else 'FAIL'}.\n"
(RUN / "INDEPENDENT_VERIFICATION.md").write_text(iv_text)

dump(RUN / "GATE_RESULTS.json", {
    "schema_version": "1.0",
    "module": "E",
    "run_id": spec["run_id"],
    "overall": "PASS" if overall else "FAIL_REQUIRES_ANALYSIS",
    "aggregate_scores_cannot_override": True,
    "component_gates": component_gates,
    "metrics": {
        "minimum_abundance": min(r["minimum_abundance"] for r in primary_records),
        "max_baryon_drift": max(r["max_baryon_drift"] for r in primary_records),
        "max_charge_drift": max(r["max_charge_drift"] for r in primary_records),
        "max_intrinsic_energy_drift": max(r["max_intrinsic_energy_drift"] for r in primary_records),
        "max_finest_step_linf": max(r["finest_pair_linf"] for r in convergence_records),
        "max_route_split_linf": max(r["max_linf_vs_single_route"] for r in route_records),
        "max_restart_linf": max(r["linf"] for r in restart_records),
        "max_independent_linf": max(r["linf_vs_primary"] for r in independent_records),
        "minimum_withheld_channel_effect": min(min(r["forward_withheld_linf"], r["reverse_withheld_linf"]) for r in withheld_records),
        "branch_charge_span": branch_charge_span,
        "scalar_collapse_linf": scalar_collapse_difference,
    },
    "physical_execution_occurred": True,
    "generation_mode": "GENERATION_SEALED",
})

handoff = {
    "schema_version": "1.0",
    "object_id": "H_E_to_F",
    "from_module": "E",
    "to_module": "F",
    "run_id": spec["run_id"],
    "evidence_state": "PHYSICALLY_EXECUTED_PENDING_CLOSEOUT",
    "fidelity": "MINIMAL_SPINE",
    "generation_mode": "GENERATION_SEALED",
    "parent": {"object_id": "H_D_to_E", "sha256": spec["exact_parent"]["sha256"]},
    "rate_law": {"kf": kf, "kr": kr, "source": "C/D parent-derived g_C and a"},
    "branch_family_final_states": [{"branch_id": r["branch_id"], "final_state": r["final_state"]} for r in primary_records],
    "central_symmetry_quotient_final_state": central_record["final_state"],
    "branch_mean_final_state": np.mean(branch_arr, axis=0).tolist(),
    "branch_covariance": branch_cov.tolist(),
    "combined_branch_decimal_covariance": env_cov.tolist(),
    "stochastic_covariance": np.zeros((3, 3)).tolist(),
    "freezeout_witnesses": [{"branch_id": r["branch_id"], "tau_E": r["freezeout_event_tau_E"]} for r in primary_records],
    "restart_contract": "F receives the exact six-branch primordial RFC abundance family, central symmetry quotient, branch/decimal covariance, conserved ledgers and freeze-out witness set; no observational abundances or calibrated nuclear constants are preloaded.",
    "claim_boundary": spec["claim_boundary"],
}
if overall:
    dump(RUN / "frozen/H_E_to_F.json", handoff)
    dump(RUN / "frozen/H_E_to_F_MANIFEST.json", {
        "object_id": "H_E_to_F_MANIFEST",
        "run_id": spec["run_id"],
        "sha256": sha(RUN / "frozen/H_E_to_F.json"),
        "bytes": (RUN / "frozen/H_E_to_F.json").stat().st_size,
        "fidelity": "MINIMAL_SPINE",
        "generation_mode": "GENERATION_SEALED",
    })

print(json.dumps({
    "overall": "PASS" if overall else "FAIL_REQUIRES_ANALYSIS",
    "component_gates": component_gates,
    "metrics": json.loads((RUN / "GATE_RESULTS.json").read_text())["metrics"],
}, indent=2))

if not overall:
    raise SystemExit(2)
