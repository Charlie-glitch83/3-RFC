from __future__ import annotations

from typing import Any

import numpy as np
from scipy.linalg import expm

from .utils import complex_json, matrix_psd_audit, require_finite


def run_linear_transfer(cfg: dict[str, Any]) -> dict[str, Any]:
    generator = require_finite("generator", cfg["generator"])
    times = require_finite("times", cfg["times"])
    x0 = require_finite("initial_state", cfg["initial_state"])
    if generator.ndim != 2 or generator.shape[0] != generator.shape[1]:
        raise ValueError("generator must be square")
    if x0.ndim != 1 or x0.shape[0] != generator.shape[0]:
        raise ValueError("initial_state dimension mismatch")
    if times.ndim != 1 or len(times) < 1 or np.min(times) < 0.0:
        raise ValueError("times must be a nonempty nonnegative vector")
    cov0 = require_finite("initial_covariance", cfg.get("initial_covariance", np.eye(len(x0))))
    if cov0.shape != generator.shape:
        raise ValueError("initial_covariance dimension mismatch")

    tolerance = float(cfg.get("tolerance", 1e-10))
    initial_covariance_audit = matrix_psd_audit(cov0, tolerance)
    if not initial_covariance_audit["symmetric"] or not initial_covariance_audit["positive_semidefinite"]:
        return {"success": False, "classification": "LINEAR_TRANSFER_REJECTED", "error": "initial covariance failed symmetry/PSD audit", "initial_covariance_audit": initial_covariance_audit}

    states: list[list[float]] = []
    covs: list[list[list[float]]] = []
    ops: list[list[list[float]]] = []
    output_audits: list[dict[str, Any]] = []
    for time in times:
        op = expm(generator * float(time))
        cov = op @ cov0 @ op.T
        ops.append(op.tolist())
        states.append((op @ x0).tolist())
        covs.append(cov.tolist())
        output_audits.append(matrix_psd_audit(cov, tolerance))

    # Use two arbitrary supplied nonnegative times to test the semigroup law.
    if len(times) >= 2:
        t1, t2 = float(times[0]), float(times[1])
    else:
        t1, t2 = float(times[0]) / 2.0, float(times[0]) / 2.0
    semigroup_error = float(np.linalg.norm(expm(generator * (t1 + t2)) - expm(generator * t2) @ expm(generator * t1)))
    all_covariances_psd = all(x["symmetric"] and x["positive_semidefinite"] for x in output_audits)
    pass_flags = {
        "semigroup": semigroup_error <= tolerance,
        "covariance_preserved": all_covariances_psd,
        "finite_outputs": bool(np.all(np.isfinite(np.asarray(states))) and np.all(np.isfinite(np.asarray(covs)))),
    }
    return {
        "success": bool(all(pass_flags.values())),
        "classification": "LINEAR_TRANSFER_EXECUTION",
        "operators": ops,
        "states": states,
        "covariances": covs,
        "initial_covariance_audit": initial_covariance_audit,
        "output_covariance_audits": output_audits,
        "semigroup_error": semigroup_error,
        "tolerance": tolerance,
        "generator_eigenvalues": complex_json(np.linalg.eigvals(generator)),
        "pass_flags": pass_flags,
    }
