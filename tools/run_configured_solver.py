#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rfc_engine.provenance import sha256_file, write_json
from rfc_engine.solvers.big_implosion import run_big_implosion
from rfc_engine.solvers.covariance import run_covariance
from rfc_engine.solvers.finite_volume import run_periodic_conservative
from rfc_engine.solvers.fourier_field import run_fourier_field
from rfc_engine.solvers.freeze_packet import run_freeze_packet
from rfc_engine.solvers.global_ledger import run_global_ledger
from rfc_engine.solvers.linear_transfer import run_linear_transfer
from rfc_engine.solvers.nbody import run_nbody
from rfc_engine.solvers.observation import run_gaussian_comparison
from rfc_engine.solvers.ray_bundle import run_ray_bundle
from rfc_engine.solvers.reaction_network import ReactionNetwork
from rfc_engine.solvers.recurrence import run_affine_recurrence
from rfc_engine.solvers.spectral_model import run_spectral_model
from rfc_engine.solvers.synthetic_observation import run_synthetic_observation
from rfc_engine.solvers.transport import run_transport
from rfc_engine.solvers.triad_kernel import run_triad_kernel
from rfc_engine.solvers.utils import unresolved_placeholders
from rfc_engine.solvers.visibility import run_visibility


def execute(cfg: dict[str, Any]) -> dict[str, Any]:
    placeholders = unresolved_placeholders(cfg)
    if placeholders:
        raise ValueError(f"configuration contains unresolved bindings: {placeholders}")
    if cfg.get("generation_mode") not in {"GENERATION_SEALED", "MODULE_P_PUBLIC_COMPARISON"}:
        raise ValueError("config must declare generation_mode")
    solver = cfg["solver"]
    model = cfg.get("model", {})
    if solver == "triad_kernel":
        return run_triad_kernel(model)
    if solver == "big_implosion":
        return run_big_implosion(model)
    if solver == "spectral_model":
        return run_spectral_model(model)
    if solver == "reaction_network":
        network = ReactionNetwork.from_config(model)
        return network.integrate(
            cfg["initial_state"],
            cfg["t_span"],
            float(cfg.get("rtol", 1e-9)),
            float(cfg.get("atol", 1e-12)),
            cfg.get("method", "BDF"),
            float(cfg.get("max_step", float("inf"))),
            float(cfg.get("positivity_tolerance", 1e-9)),
            float(cfg.get("invariant_tolerance", 1e-8)),
        )
    if solver == "transport":
        return run_transport(model)
    if solver == "visibility":
        return run_visibility(model)
    if solver == "linear_transfer":
        return run_linear_transfer(model)
    if solver == "covariance":
        return run_covariance(model)
    if solver == "fourier_field":
        return run_fourier_field(model)
    if solver == "nbody":
        return run_nbody(model)
    if solver == "finite_volume":
        return run_periodic_conservative(model)
    if solver == "ray_bundle":
        return run_ray_bundle(model)
    if solver == "synthetic_observation":
        return run_synthetic_observation(model)
    if solver == "affine_recurrence":
        return run_affine_recurrence(model)
    if solver == "global_ledger":
        return run_global_ledger(model)
    if solver == "freeze_packet":
        return run_freeze_packet(model)
    if solver == "gaussian_comparison":
        if cfg["generation_mode"] != "MODULE_P_PUBLIC_COMPARISON":
            raise ValueError("gaussian comparison is permitted only in Module P mode")
        return run_gaussian_comparison(model)
    raise ValueError(f"unknown solver: {solver}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run an exact frozen solver configuration")
    parser.add_argument("--config", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    cfg_path = Path(args.config).resolve()
    out = Path(args.output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

    input_copy = out / "frozen_config.json"
    input_copy.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    started = datetime.now(timezone.utc).isoformat()
    try:
        result = execute(cfg)
    except Exception as exc:
        result = {
            "success": False,
            "classification": "CONFIGURATION_OR_EXECUTION_ERROR",
            "error_type": type(exc).__name__,
            "error": str(exc),
        }
    write_json(out / "result.json", result)
    environment = {
        "python": sys.version,
        "platform": platform.platform(),
        "implementation": platform.python_implementation(),
        "started_utc": started,
        "completed_utc": datetime.now(timezone.utc).isoformat(),
    }
    write_json(out / "environment.json", environment)
    manifest = {
        "solver": cfg.get("solver"),
        "generation_mode": cfg.get("generation_mode"),
        "config_sha256": sha256_file(input_copy),
        "result_sha256": sha256_file(out / "result.json"),
        "environment_sha256": sha256_file(out / "environment.json"),
        "success": bool(result.get("success", False)),
        "classification": result.get("classification", "CONFIGURED_EXECUTION_RESULT"),
    }
    write_json(out / "manifest.json", manifest)
    print(json.dumps(manifest, indent=2))
    return 0 if manifest["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
