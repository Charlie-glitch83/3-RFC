from __future__ import annotations

from typing import Any

import numpy as np

from .utils import require_finite


def run_triad_kernel(cfg: dict[str, Any]) -> dict[str, Any]:
    """Construct the finite recursive carrier used to test Module A implementations.

    This engine does not choose the physical meaning of a modal basis. It executes
    the depth law and complete directed non-self relational carrier supplied in the
    frozen configuration.
    """
    delta = float(cfg["delta"])
    alpha = float(cfg["alpha"])
    time = float(cfg.get("time", 0.0))
    depth = int(cfg["depth"])
    constituents = list(cfg["constituents"])
    if delta <= 1.0:
        raise ValueError("delta must exceed 1")
    if alpha < 0.0 or time < 0.0 or depth < 1:
        raise ValueError("alpha/time/depth violate the frozen domain")
    if len(constituents) < 1 or len(set(constituents)) != len(constituents):
        raise ValueError("constituent identifiers must be nonempty and unique")

    j = np.arange(1, depth + 1, dtype=float)
    raw = np.power(delta, -j) * np.exp(-alpha * j * time)
    normalization = float(np.sum(raw))
    if not np.isfinite(normalization) or normalization <= 0.0:
        raise ValueError("recursive weights failed normalization")
    weights = raw / normalization

    lanes = [[source, target] for source in constituents for target in constituents if source != target]
    n = len(constituents)
    expected = n * (n - 1)
    next_increment = (n + 1) * n - expected

    basis = cfg.get("basis_matrix")
    kernel_state = None
    if basis is not None:
        b = require_finite("basis_matrix", basis)
        if b.ndim != 2 or b.shape[0] != depth:
            raise ValueError("basis_matrix must have one row per recursive depth")
        kernel_state = (weights @ b).tolist()

    tolerance = float(cfg.get("tolerance", 1e-12))
    normalization_error = float(abs(np.sum(weights) - 1.0))
    pass_flags = {
        "normalization": normalization_error <= tolerance,
        "no_self_lanes": all(a != b for a, b in lanes),
        "lane_count": len(lanes) == expected,
        "lane_uniqueness": len({tuple(x) for x in lanes}) == expected,
        "two_n_increment": next_increment == 2 * n,
    }
    return {
        "success": bool(all(pass_flags.values())),
        "classification": "FINITE_TRIAD_KERNEL_EXECUTION",
        "depth": depth,
        "raw_weights": raw.tolist(),
        "normalized_weights": weights.tolist(),
        "normalization_error": normalization_error,
        "constituents": constituents,
        "directed_lanes": lanes,
        "lane_count": len(lanes),
        "expected_lane_count": expected,
        "next_constituent_lane_increment": next_increment,
        "kernel_state": kernel_state,
        "pass_flags": pass_flags,
    }
