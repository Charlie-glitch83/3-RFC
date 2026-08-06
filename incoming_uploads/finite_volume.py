from __future__ import annotations

from typing import Any

import numpy as np

from .utils import require_finite


def run_periodic_conservative(cfg: dict[str, Any]) -> dict[str, Any]:
    state = require_finite("state", cfg["state"])
    flux = require_finite("interface_flux", cfg["interface_flux"])
    dt = float(cfg["dt"])
    dx = float(cfg.get("dx", 1.0))
    if state.ndim != 1 or state.shape != flux.shape:
        raise ValueError("state and interface_flux must be equal one-dimensional arrays")
    if dt <= 0.0 or dx <= 0.0:
        raise ValueError("dt and dx must be positive")
    updated = state - (dt / dx) * (np.roll(flux, -1) - flux)
    conservation_error = float(abs(np.sum(updated) - np.sum(state)))
    conservation_tolerance = float(cfg.get("conservation_tolerance", 1e-12))
    positivity_required = bool(cfg.get("positivity_required", False))
    positivity_tolerance = float(cfg.get("positivity_tolerance", 1e-12))
    pass_flags = {
        "finite_state": bool(np.all(np.isfinite(updated))),
        "periodic_conservation": conservation_error <= conservation_tolerance,
        "positivity": bool((not positivity_required) or np.min(updated) >= -positivity_tolerance),
    }
    return {
        "success": bool(all(pass_flags.values())),
        "classification": "PERIODIC_FINITE_VOLUME_UPDATE",
        "updated_state": updated.tolist(),
        "sum_before": float(np.sum(state)),
        "sum_after": float(np.sum(updated)),
        "conservation_error": conservation_error,
        "conservation_tolerance": conservation_tolerance,
        "minimum_state": float(np.min(updated)),
        "pass_flags": pass_flags,
    }
