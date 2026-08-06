from __future__ import annotations

from typing import Any

import hashlib
import numpy as np

from .utils import matrix_psd_audit, require_finite


def run_synthetic_observation(cfg: dict[str, Any]) -> dict[str, Any]:
    """Apply a frozen observation operator to truth-level outputs.

    This belongs to generation only when the response/noise model was frozen
    without public target information. Public data are never consumed here.
    """
    truth = require_finite("truth", cfg["truth"])
    response = require_finite("response_matrix", cfg["response_matrix"])
    if truth.ndim != 1 or response.ndim != 2 or response.shape[1] != len(truth):
        raise ValueError("response_matrix dimension mismatch")
    noiseless = response @ truth
    observed = noiseless.copy()
    noise_record: dict[str, Any] | None = None
    if "noise_covariance" in cfg:
        covariance = require_finite("noise_covariance", cfg["noise_covariance"])
        if covariance.shape != (len(noiseless), len(noiseless)):
            raise ValueError("noise covariance dimension mismatch")
        tolerance = float(cfg.get("covariance_tolerance", 1e-12))
        audit = matrix_psd_audit(covariance, tolerance)
        if not audit["symmetric"] or not audit["positive_semidefinite"]:
            return {"success": False, "classification": "SYNTHETIC_OBSERVATION_REJECTED", "covariance_audit": audit}
        seed = int(cfg["noise_seed"])
        rng = np.random.default_rng(seed)
        values, vectors = np.linalg.eigh(covariance)
        factor = vectors @ np.diag(np.sqrt(np.clip(values, 0.0, None)))
        draw = factor @ rng.standard_normal(len(noiseless))
        observed = noiseless + draw
        noise_record = {"seed": seed, "draw": draw.tolist(), "covariance_audit": audit}
    truth_hash = hashlib.sha256(truth.tobytes()).hexdigest()
    response_hash = hashlib.sha256(response.tobytes()).hexdigest()
    return {
        "success": bool(np.all(np.isfinite(observed))),
        "classification": "SYNTHETIC_OBSERVATION_GENERATION",
        "truth_hash": truth_hash,
        "response_hash": response_hash,
        "noiseless_observable": noiseless.tolist(),
        "synthetic_observable": observed.tolist(),
        "noise": noise_record,
    }
