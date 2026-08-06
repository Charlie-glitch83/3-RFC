from __future__ import annotations

from typing import Any

import numpy as np

from .utils import require_finite, relative_error


def graph_laplacian(node_count: int, weighted_edges: list[list[float]]) -> np.ndarray:
    laplacian = np.zeros((node_count, node_count), dtype=float)
    for rec in weighted_edges:
        if len(rec) != 3:
            raise ValueError("each edge must be [i, j, weight]")
        i, j, weight = int(rec[0]), int(rec[1]), float(rec[2])
        if i == j or not (0 <= i < node_count and 0 <= j < node_count):
            raise ValueError("invalid graph edge")
        if weight <= 0.0:
            raise ValueError("edge weights must be positive")
        laplacian[i, i] += weight
        laplacian[j, j] += weight
        laplacian[i, j] -= weight
        laplacian[j, i] -= weight
    return laplacian


def run_big_implosion(cfg: dict[str, Any]) -> dict[str, Any]:
    """Execute the frozen compression operator Q=(I+L/(delta-1))^-1.

    This is a reusable implementation of the operator form. A physical Module B
    closeout must additionally justify the graph, state, units, sector map, and
    event interpretation from the exact Module A parent.
    """
    delta = float(cfg["delta"])
    if delta <= 1.0:
        raise ValueError("delta must exceed 1")
    node_count = int(cfg["node_count"])
    if node_count < 2:
        raise ValueError("node_count must be at least 2")
    state = require_finite("initial_state", cfg["initial_state"])
    if state.ndim == 1:
        state = state[:, None]
    if state.ndim != 2 or state.shape[0] != node_count:
        raise ValueError("initial_state must have node_count rows")

    laplacian = graph_laplacian(node_count, cfg["weighted_edges"])
    identity = np.eye(node_count)
    operator = np.linalg.inv(identity + laplacian / (delta - 1.0))
    manifested = operator @ state
    reopened = np.linalg.solve(operator, manifested)

    ones = np.ones((node_count, 1))
    projector = identity - ones @ ones.T / node_count
    before_nontrivial = projector @ state
    after_nontrivial = projector @ manifested
    norm_before = float(np.linalg.norm(before_nontrivial))
    norm_after = float(np.linalg.norm(after_nontrivial))
    compression_ratio = float(norm_after / norm_before) if norm_before > 0.0 else 0.0
    mean_before = np.mean(state, axis=0)
    mean_after = np.mean(manifested, axis=0)
    reopening_error = float(np.linalg.norm(reopened - state))
    conserved_mode_error = float(np.linalg.norm(mean_after - mean_before))
    eig_l = np.linalg.eigvalsh(laplacian)
    eig_q = np.linalg.eigvalsh(operator)

    tolerance = float(cfg.get("tolerance", 1e-11))
    strict_margin = float(cfg.get("strict_compression_margin", 1e-12))
    pass_flags = {
        "symmetric_laplacian": bool(np.linalg.norm(laplacian - laplacian.T) <= tolerance),
        "positive_semidefinite_laplacian": bool(np.min(eig_l) >= -tolerance),
        "conserved_constant_mode": conserved_mode_error <= tolerance,
        "strict_nontrivial_compression": bool(norm_before <= tolerance or norm_after < norm_before - strict_margin),
        "reopening": reopening_error <= tolerance,
        "operator_eigenvalues_in_unit_interval": bool(np.min(eig_q) > 0.0 and np.max(eig_q) <= 1.0 + tolerance),
        "no_pre_event_clock_imported": cfg.get("pre_event_clock") is None,
    }

    sector_result = None
    if "sector_projection" in cfg:
        projection = require_finite("sector_projection", cfg["sector_projection"])
        if projection.ndim != 2 or projection.shape[1] != node_count:
            raise ValueError("sector_projection must have node_count columns")
        sectors = projection @ manifested
        reconstructed = projection.T @ sectors
        sector_result = {
            "values": sectors.tolist(),
            "projection_shape": list(projection.shape),
            "reconstruction_error": float(np.linalg.norm(reconstructed - manifested)),
        }

    return {
        "success": bool(all(pass_flags.values())),
        "classification": "BIG_IMPLOSION_OPERATOR_EXECUTION",
        "laplacian": laplacian.tolist(),
        "operator": operator.tolist(),
        "operator_eigenvalues": eig_q.tolist(),
        "initial_state": state.tolist(),
        "manifested_state": manifested.tolist(),
        "reopened_state": reopened.tolist(),
        "nontrivial_norm_before": norm_before,
        "nontrivial_norm_after": norm_after,
        "compression_ratio": compression_ratio,
        "reopening_error": reopening_error,
        "conserved_mode_error": conserved_mode_error,
        "total_relative_change": relative_error(float(np.sum(manifested)), float(np.sum(state))),
        "sector_result": sector_result,
        "pass_flags": pass_flags,
    }
