from __future__ import annotations

from typing import Any

import numpy as np
from scipy.integrate import cumulative_trapezoid

from .utils import require_finite


def run_visibility(cfg: dict[str, Any]) -> dict[str, Any]:
    """Construct a normalized visibility kernel from a frozen positive opacity rate."""
    time = require_finite("time", cfg["time"])
    rate = require_finite("opacity_rate", cfg["opacity_rate"])
    if time.ndim != 1 or rate.shape != time.shape or len(time) < 3:
        raise ValueError("time and opacity_rate must be equal one-dimensional arrays")
    if not np.all(np.diff(time) > 0.0):
        raise ValueError("time must be strictly increasing")
    if np.min(rate) < 0.0:
        raise ValueError("opacity_rate must be nonnegative")

    # Optical depth remaining to the terminal boundary.
    reverse_tau = cumulative_trapezoid(rate[::-1], time[::-1], initial=0.0)
    tau = -reverse_tau[::-1]
    visibility = rate * np.exp(-tau)
    norm = float(np.trapezoid(visibility, time))
    tolerance = float(cfg.get("normalization_tolerance", 5e-3))
    if norm <= 0.0 or not np.isfinite(norm):
        normalized = np.zeros_like(visibility)
    else:
        normalized = visibility / norm
    normalized_integral = float(np.trapezoid(normalized, time))
    peak_index = int(np.argmax(normalized))
    pass_flags = {
        "positive_rate": bool(np.min(rate) >= 0.0),
        "finite_tau": bool(np.all(np.isfinite(tau))),
        "normalized": bool(abs(normalized_integral - 1.0) <= tolerance),
    }
    return {
        "success": bool(all(pass_flags.values())),
        "classification": "VISIBILITY_KERNEL_EXECUTION",
        "time": time.tolist(),
        "optical_depth": tau.tolist(),
        "visibility": visibility.tolist(),
        "normalized_visibility": normalized.tolist(),
        "raw_integral": norm,
        "normalized_integral": normalized_integral,
        "peak_time": float(time[peak_index]),
        "peak_index": peak_index,
        "pass_flags": pass_flags,
    }
