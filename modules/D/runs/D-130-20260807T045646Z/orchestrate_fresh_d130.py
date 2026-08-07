#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
os.chdir(ROOT)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2) + "\n")


def run(cmd: list[str], *, capture_path: Path | None = None) -> subprocess.CompletedProcess:
    proc = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if capture_path is not None:
        capture_path.write_text(proc.stdout)
    else:
        print(proc.stdout, end="")
    if proc.returncode != 0:
        raise SystemExit(f"command failed ({proc.returncode}): {' '.join(cmd)}\n{proc.stdout}")
    return proc


def current_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


state = json.loads((ROOT / "STATE.json").read_text())
lock = json.loads((RUN / "PRE_EXECUTION_LOCK.json").read_text())
spec = json.loads((RUN / "FROZEN_DERIVATION_SPEC.json").read_text())
parent_path = ROOT / "modules/C/frozen/H_C_to_D.json"
parent = json.loads(parent_path.read_text())
assert state["active_work_unit"] == "D-130"
assert state["current_run"] == "D-130-20260807T045646Z"
assert lock["status"] == "FROZEN"
assert spec["status"] == "FROZEN_PRE_EXECUTION"
assert lock["numerical_controls"] == spec["numerical_controls"]
assert sha(parent_path) == lock["parent_hashes"][0]["sha256"]

# Freeze implementation bytes before primary numerical execution.
impl_lock = {
    "schema_version": "1.0",
    "run_id": "D-130-20260807T045646Z",
    "status": "FROZEN_BEFORE_PRIMARY_EXECUTION",
    "frozen_utc": datetime.now(timezone.utc).isoformat(),
    "source_commit": current_head(),
    "pre_execution_lock_sha256": sha(RUN / "PRE_EXECUTION_LOCK.json"),
    "derivation_spec_sha256": sha(RUN / "FROZEN_DERIVATION_SPEC.json"),
    "primary_implementation": {"path": str((RUN / "primary/execute_d130.py").relative_to(ROOT)), "sha256": sha(RUN / "primary/execute_d130.py")},
    "independent_implementation": {"path": str((RUN / "independent/independent_reconstruct_d130.py").relative_to(ROOT)), "sha256": sha(RUN / "independent/independent_reconstruct_d130.py")},
    "orchestrator": {"path": str(Path(__file__).resolve().relative_to(ROOT)), "sha256": sha(Path(__file__).resolve())},
    "allowed_corrections": lock["allowed_implementation_only_corrections"],
}
write_json(RUN / "IMPLEMENTATION_LOCK.json", impl_lock)

# start_work.sh already copied these governed files. Verify rather than overwrite them.
canonical_template = ROOT / "configured_runs/templates/D_transport.template.json"
local_template = RUN / "solver_templates/D_transport.template.json"
local_sheet = RUN / "binding_sheets/D_transport.bindings.json"
assert local_template.is_file() and local_sheet.is_file()
assert sha(local_template) == sha(canonical_template)
sheet = json.loads(local_sheet.read_text())
assert sheet["template_sha256"] == sha(local_template)

# Fill the exact run-local binding sheet from frozen parent/derivation objects only.
controls = lock["numerical_controls"]
spec_path = RUN / "FROZEN_DERIVATION_SPEC.json"
lock_path = RUN / "PRE_EXECUTION_LOCK.json"
values = {
    "model.state_names": (["p1", "p2", "p3"], spec_path, "INTERNAL_DERIVATION", "D_NORMALIZED_TRANSPORT_STATE", "dimensionless labels", "3-state simplex"),
    "model.parameters": ({}, spec_path, "INTERNAL_DERIVATION", "D_NO_FREE_RATE_AFTER_INTRINSIC_NORMALIZATION", "dimensionless", "none"),
    "model.rhs_expressions": (["-2*p1/3+p2/3+p3/3", "p1/3-2*p2/3+p3/3", "p1/3+p2/3-2*p3/3"], spec_path, "INTERNAL_DERIVATION", "D_SELECTED_NORMALIZED_BRANCH", "population per intrinsic-clock unit", "dimensionless"),
    "model.initial_state": (parent["prethermal_state"]["node_populations"], parent_path, "EXACT_PARENT_ARTIFACT", "H_C_to_D_PRETHERMAL_STATE", "dimensionless probability", "3"),
    "model.t_span": (controls["execution_interval"], lock_path, "INTERNAL_DERIVATION", "D_FROZEN_INTRINSIC_INTERVAL", "intrinsic clock s", "dimensionless"),
    "model.max_step": (controls["primary_max_step"], lock_path, "INTERNAL_DERIVATION", "D_FROZEN_PRIMARY_MAX_STEP", "intrinsic clock s", "dimensionless"),
    "model.linear_invariants": ({"Q_total": [1, 1, 1]}, spec_path, "INTERNAL_DERIVATION", "D_TOTAL_CHARGE_INVARIANT", "dimensionless", "linear invariant"),
    "model.invariant_tolerance": (controls["invariant_tolerance"], lock_path, "INTERNAL_DERIVATION", "D_FROZEN_INVARIANT_TOLERANCE", "dimensionless", "absolute"),
    "model.positivity_tolerance": (controls["positivity_tolerance"], lock_path, "INTERNAL_DERIVATION", "D_FROZEN_POSITIVITY_TOLERANCE", "dimensionless probability", "absolute"),
}
seen = set()
for rec in sheet["bindings"]:
    key = rec["path"]
    value, origin, kind, dobj, units, dims = values[key]
    rec.update(
        value=value,
        origin_kind=kind,
        origin_path=str(origin.relative_to(ROOT)),
        origin_sha256=sha(origin),
        module="D",
        derivation_object=dobj,
        units=units,
        dimensions=dims,
        justification="Exact frozen parent or pre-execution derivation only; no observed targets or post-hoc values.",
    )
    seen.add(key)
assert seen == set(sheet["expected_binding_paths"])
write_json(local_sheet, sheet)

config_path = RUN / "solver_configs/D_transport.json"
run([
    sys.executable, "tools/materialize_solver_config.py",
    "--template", str(local_template.relative_to(ROOT)),
    "--binding-sheet", str(local_sheet.relative_to(ROOT)),
    "--output", str(config_path.relative_to(ROOT)),
], capture_path=RUN / "MATERIALIZE_SOLVER_CONFIG.txt")

# Exact configured engine, then repository local-phase checks.
solver_out = RUN / "solver_outputs/transport"
run([sys.executable, "tools/run_configured_solver.py", "--config", str(config_path.relative_to(ROOT)), "--output-dir", str(solver_out.relative_to(ROOT))], capture_path=RUN / "CONFIGURED_TRANSPORT_EXECUTION.txt")
run(["bash", "tools/finish_local_phase.sh", "D", str(RUN.relative_to(ROOT))], capture_path=RUN / "FINISH_LOCAL_PHASE.txt")

# Actual parent-driven diagnostic and independent reconstruction.
run([sys.executable, str((RUN / "primary/execute_d130.py").relative_to(ROOT))], capture_path=RUN / "primary/EXECUTION_STDOUT.txt")
run([sys.executable, str((RUN / "independent/independent_reconstruct_d130.py").relative_to(ROOT))], capture_path=RUN / "independent/EXECUTION_STDOUT.txt")

# True clean-checkout replay at the exact frozen implementation source commit.
source_commit = impl_lock["source_commit"]
with tempfile.TemporaryDirectory(prefix="d130-clean-replay-") as td:
    replay_root = Path(td) / "repo"
    run(["git", "worktree", "add", "--detach", str(replay_root), source_commit])
    try:
        rel_run = RUN.relative_to(ROOT)
        subprocess.run([sys.executable, str(rel_run / "primary/execute_d130.py")], cwd=replay_root, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        subprocess.run([sys.executable, str(rel_run / "independent/independent_reconstruct_d130.py")], cwd=replay_root, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        pairs = [
            "primary/DISTRIBUTION_HISTORY.json",
            "primary/PRIMARY_DIAGNOSTICS.json",
            "independent/INDEPENDENT_RECONSTRUCTION.json",
        ]
        checks = []
        for rel in pairs:
            live = RUN / rel
            replay = replay_root / rel_run / rel
            checks.append({"path": rel, "live_sha256": sha(live), "replay_sha256": sha(replay), "exact_match": sha(live) == sha(replay)})
        replay_record = {
            "source_commit": source_commit,
            "clean_checkout": True,
            "primary_command": f"python {rel_run}/primary/execute_d130.py",
            "independent_command": f"python {rel_run}/independent/independent_reconstruct_d130.py",
            "checks": checks,
            "pass": all(x["exact_match"] for x in checks),
        }
        write_json(RUN / "REPLAY_RECORD.json", replay_record)
        assert replay_record["pass"]
    finally:
        subprocess.run(["git", "worktree", "remove", "--force", str(replay_root)], cwd=ROOT, check=False)

primary_diag = json.loads((RUN / "primary/PRIMARY_DIAGNOSTICS.json").read_text())
ledger = json.loads((RUN / "primary/ENTROPY_CONSERVATION_LEDGER.json").read_text())
phase = json.loads((RUN / "primary/PHASE_EVENT_LEDGER.json").read_text())
indep = json.loads((RUN / "independent/INDEPENDENT_RECONSTRUCTION.json").read_text())
replay = json.loads((RUN / "REPLAY_RECORD.json").read_text())
solver = json.loads((solver_out / "result.json").read_text())

positive_pass = bool(primary_diag["checks"]["positive_distributions"] and solver["pass_flags"]["positivity"])
conv_pass = bool(primary_diag["checks"]["dyadic_convergence"] and primary_diag["checks"]["analytic_orbit"])
restart_indep_pass = bool(primary_diag["checks"]["restart"] and indep["diagnostic_pass"] and replay["pass"])
assert positive_pass and conv_pass and restart_indep_pass
assert ledger["charge_conservation_status"] == "PASS"
assert phase["events"] == [] and phase["observed_or_public_target_values_used"] is False

gates = {
    "run_id": "D-130-20260807T045646Z",
    "overall": "BLOCKED",
    "component_gates": {
        "positive distributions": {"status": "PASS", "normalized_score": 1.0},
        "energy/charge conservation": {
            "status": "BLOCKED_PHYSICAL_ENERGY_NOT_DERIVED",
            "charge_status": ledger["charge_conservation_status"],
            "physical_energy_status": ledger["physical_energy_conservation_status"],
            "normalized_score": None,
        },
        "event ordering": {"status": "PASS_NO_EVENT_WITNESS", "events": [], "observed_targets_used": False, "normalized_score": 1.0},
        "stiff-solver convergence": {"status": "PASS", "normalized_score": 1.0, "scope": "BDF convergence of normalized intrinsic branch; no physical stiffness scale claimed"},
        "restart and independent reconstruction": {"status": "PASS", "normalized_score": 1.0},
    },
    "blocking_object": {
        "status": "BLOCKED",
        "name": "PHYSICAL_THERMAL_HISTORY",
        "reason": "Exact C parent provides no dimensionful energy/temperature map, physical clock, metric expansion state, or parent-derived phase order parameter/threshold. Full D claim would exceed evidence.",
    },
    "generation_inputs": "FROZEN_PARENT_AND_INTERNAL_DERIVATION_ONLY",
}
write_json(RUN / "GATE_RESULTS.json", gates)

(RUN / "INDEPENDENT_VERIFICATION.md").write_text("""# Independent verification — D-130

## Result

**PASS for the normalized dimensionless transport diagnostic; BLOCKED for full physical Module D.**

The independent implementation reconstructed the exact C projector and analytic orbit from `H_C_to_D` and `FROZEN_DERIVATION_SPEC.json` before reading the primary trajectory. It independently verified normalization, positivity, entropy direction, dimensionless excitation decay, and the analytic final state within the frozen tolerance. The clean-checkout replay reproduced the selected primary and independent artifacts byte-for-byte.

The same independent inspection confirms that the exact parent provides no dimensionful energy scale or thermodynamic temperature map, no physical clock or metric expansion state, and no phase order parameter/threshold. Therefore this verification does not support a Kelvin-temperature history, physical expansion chronology, phase-transition chronology, or D-to-E physical handoff.
""")

write_json(RUN / "H_D_to_E_BLOCKED.json", {
    "schema_version": "1.0",
    "object_id": "H_D_to_E_BLOCKED",
    "from_module": "D",
    "to_module": "E",
    "run_id": "D-130-20260807T045646Z",
    "status": "BLOCKED_NO_PHYSICAL_HANDOFF",
    "supported_object": "normalized dimensionless parent-driven transport diagnostic",
    "missing_required_objects": [
        "dimensionful energy/temperature map",
        "physical clock or lawful time map",
        "metric/expansion state required by D objective",
        "parent-derived phase order parameter and threshold",
    ],
    "generation_inputs": "FROZEN_PARENT_AND_INTERNAL_DERIVATION_ONLY",
    "claim_boundary": "No primordial-abundance parent is released; Module E remains blocked.",
})

(RUN / "CLOSEOUT.md").write_text("""# Module D closeout — physical thermal-history obstruction

## Result

`BLOCKED` at the physical thermal-history layer after successful execution of the lawful normalized dimensionless transport diagnostic.

## Strongest supported claim

The exact frozen C parent and inherited O(2) symmetry support the nontrivial linear conservative positivity-preserving relaxation family `dp/dtau=-kappa P_perp p` up to intrinsic clock reparameterization. The normalized branch `dp/ds=-P_perp p` was executed with the frozen BDF controls, remained positive, conserved total carrier charge, matched the analytic orbit, increased Shannon entropy, decreased the inherited dimensionless excitation functional, passed the frozen dyadic convergence matrix, passed midpoint restart, executed the preregistered structural countermodels/ablations, reproduced independently, and replayed from a clean checkout. The nonlinear conservative O(2)-equivariant family remains underdetermined rather than silently discarded.

## Blocking scientific object

The exact C parent contains no dimensionful energy scale, thermodynamic temperature map, physical clock, metric/expansion state, or parent-derived phase order parameter/threshold. Physical energy conservation therefore cannot be tested as a D quantity, no Kelvin-temperature history can be generated, and no physical phase chronology exists to hand to Module E. Importing standard cosmological values or formulas would violate the generation firewall and the frozen claim boundary.

## Strongest unsupported claim

No complete generated RFC physical thermal history, Kelvin-temperature trajectory, physical expansion history, phase-transition chronology, primordial isotope initial conditions, empirical correspondence, or valid `H_D_to_E` physical handoff has been established.

## Generation firewall

Only the exact frozen parent, frozen repository authorities, and internal derivations were used. No observational target or remembered best-fit value entered generation.

## Advancement

Do not advance to Module E. Preserve `H_D_to_E_BLOCKED.json` and resolve the missing physical scale/clock/thermodynamic/event objects through a new lawfully frozen D derivation if possible.
""")

# Required end-of-session checks before closeout transition.
run([sys.executable, "tools/director.py", "doctor"], capture_path=RUN / "FINAL_DOCTOR.txt")
run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], capture_path=RUN / "UNIT_TESTS.txt")
run([sys.executable, "tools/rfc.py", "firewall-scan"], capture_path=RUN / "FIREWALL_SCAN.txt")
run([sys.executable, "tools/rfc.py", "context"], capture_path=RUN / "CONTEXT_REFRESH.txt")

# Close blocked run; never advance D->E.
run([sys.executable, "tools/rfc.py", "close-run", "--run-id", "D-130-20260807T045646Z", "--result", "BLOCKED", "--closeout", str((RUN / "CLOSEOUT.md").relative_to(ROOT))], capture_path=RUN / "CLOSE_RUN.txt")

# Final environment and manifest are written only after all other run outputs stop changing.
write_json(RUN / "ENVIRONMENT_FINAL.json", {
    "python": sys.version,
    "platform": platform.platform(),
    "implementation": platform.python_implementation(),
    "random_seed": "NONE_DETERMINISTIC",
    "generation_network_inputs": "NONE",
    "finalized_utc": datetime.now(timezone.utc).isoformat(),
})
files=[]
for p in sorted(RUN.rglob("*")):
    if p.is_file() and "__pycache__" not in p.parts and p.name != "GENERATED_OUTPUT_MANIFEST.json":
        b=p.read_bytes()
        files.append({"path":str(p.relative_to(ROOT)),"sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b)})
canonical=json.dumps(files,sort_keys=True,separators=(",",":")).encode()
write_json(RUN / "GENERATED_OUTPUT_MANIFEST.json", {
    "run_id":"D-130-20260807T045646Z",
    "finalized_after_all_run_outputs_stopped":True,
    "files":files,
    "tree_sha256":hashlib.sha256(canonical).hexdigest(),
})

# Mechanical checks again after state transition; these do not mutate run outputs.
run([sys.executable, "tools/director.py", "doctor"])
run([sys.executable, "tools/rfc.py", "firewall-scan"])
print(json.dumps({"result":"BLOCKED_AT_PHYSICAL_THERMAL_HISTORY","run_id":"D-130-20260807T045646Z","advanced_to_E":False}, indent=2))
