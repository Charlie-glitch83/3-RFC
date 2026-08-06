from __future__ import annotations

from typing import Any

import numpy as np

from .utils import complex_json, require_finite


def run_affine_recurrence(cfg: dict[str, Any]) -> dict[str, Any]:
    matrix = require_finite("matrix", cfg["matrix"])
    offset = require_finite("offset", cfg["offset"])
    state = require_finite("initial_state", cfg["initial_state"]).copy()
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1] or offset.shape != state.shape or matrix.shape[0] != len(state):
        raise ValueError("recurrence dimensions are incompatible")
    max_iterations = int(cfg.get("max_iterations", 10000))
    tolerance = float(cfg.get("tolerance", 1e-10))
    max_period = int(cfg.get("max_period", 16))
    divergence_threshold = float(cfg.get("divergence_threshold", 1e12))
    allowed = set(cfg.get("allowed_classifications", ["FIXED_POINT", "FINITE_CYCLE", "ATTRACTOR_OR_UNRESOLVED", "DIVERGENT_OR_NONCONVERGENT"]))
    history = [state.copy()]
    classification = "ATTRACTOR_OR_UNRESOLVED"
    period: int | None = None
    residual = float("inf")
    for _ in range(max_iterations):
        state = matrix @ state + offset
        history.append(state.copy())
        if not np.all(np.isfinite(state)) or np.linalg.norm(state) > divergence_threshold:
            classification = "DIVERGENT_OR_NONCONVERGENT"
            break
        residual = float(np.linalg.norm(history[-1] - history[-2]))
        if residual <= tolerance:
            classification = "FIXED_POINT"
            period = 1
            break
        for candidate in range(2, min(max_period, len(history) // 2) + 1):
            checks = [np.linalg.norm(history[-index] - history[-index - candidate]) <= tolerance for index in range(1, candidate + 1)]
            if all(checks):
                classification = "FINITE_CYCLE"
                period = candidate
                break
        if period:
            break
    eigenvalues = np.linalg.eigvals(matrix)
    return {
        "success": classification in allowed,
        "classification": classification,
        "period": period,
        "iterations": len(history) - 1,
        "final_state": history[-1].tolist(),
        "last_step_residual": residual,
        "spectral_radius": float(np.max(np.abs(eigenvalues))),
        "eigenvalues": complex_json(eigenvalues),
        "history_tail": [entry.tolist() for entry in history[-min(20, len(history)):]],
        "allowed_classifications": sorted(allowed),
    }
