from __future__ import annotations

from typing import Any

import numpy as np

from .utils import matrix_psd_audit


def audit_covariance(c: np.ndarray, tol: float = 1e-12) -> dict[str, Any]:
    return matrix_psd_audit(c, tol)


def run_covariance(cfg: dict[str, Any]) -> dict[str, Any]:
    c = np.asarray(cfg["covariance"], dtype=float)
    tolerance = float(cfg.get("tolerance", 1e-12))
    audit = audit_covariance(c, tolerance)
    if not audit["symmetric"]:
        return {"success": False, "classification": "COVARIANCE_REJECTED", "audit": audit, "error": "covariance is not symmetric; do not silently symmetrize it"}
    if not audit["positive_semidefinite"]:
        return {"success": False, "classification": "COVARIANCE_REJECTED", "audit": audit, "error": "covariance is not PSD; do not silently project it"}

    seed = int(cfg["seed"])
    count = int(cfg.get("sample_count", 10000))
    if count < 2:
        raise ValueError("sample_count must be at least 2")
    rng = np.random.default_rng(seed)
    vals, vecs = np.linalg.eigh(c)
    factor = vecs @ np.diag(np.sqrt(np.clip(vals, 0.0, None)))
    samples = rng.standard_normal((count, c.shape[0])) @ factor.T
    sample_cov = np.cov(samples, rowvar=False)
    max_error = float(np.max(np.abs(sample_cov - c)))
    sample_tolerance = float(cfg.get("sample_covariance_tolerance", max(0.05, 8.0 / np.sqrt(count))))
    pass_flags = {
        "symmetric": audit["symmetric"],
        "positive_semidefinite": audit["positive_semidefinite"],
        "sample_reconstruction": max_error <= sample_tolerance,
    }
    return {
        "success": bool(all(pass_flags.values())),
        "classification": "COVARIANCE_SAMPLE_EXECUTION",
        "audit": audit,
        "seed": seed,
        "sample_count": count,
        "sample_covariance": sample_cov.tolist(),
        "max_abs_sample_error": max_error,
        "sample_covariance_tolerance": sample_tolerance,
        "pass_flags": pass_flags,
    }
