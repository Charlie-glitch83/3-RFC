from __future__ import annotations

from typing import Any

import hashlib
import numpy as np

from .utils import matrix_psd_audit, require_finite


def run_gaussian_comparison(cfg: dict[str, Any]) -> dict[str, Any]:
    prediction = require_finite("prediction", cfg["prediction"])
    frozen_hash = hashlib.sha256(prediction.tobytes()).hexdigest()
    data = require_finite("data", cfg["data"])
    covariance = require_finite("covariance", cfg["covariance"])
    if prediction.ndim != 1 or prediction.shape != data.shape:
        raise ValueError("prediction/data shape mismatch")
    if covariance.shape != (len(prediction), len(prediction)):
        raise ValueError("covariance shape mismatch")
    tolerance = float(cfg.get("covariance_tolerance", 1e-12))
    audit = matrix_psd_audit(covariance, tolerance)
    if not audit["symmetric"] or not audit["positive_definite"]:
        return {"success": False, "classification": "PUBLIC_COMPARISON_REJECTED", "error": "covariance must be symmetric positive definite", "covariance_audit": audit}
    residual = data - prediction
    chi_square = float(residual @ np.linalg.solve(covariance, residual))
    unchanged = hashlib.sha256(prediction.tobytes()).hexdigest() == frozen_hash
    return {
        "success": bool(unchanged),
        "classification": "READ_ONLY_GAUSSIAN_COMPARISON",
        "chi_square": chi_square,
        "degrees_of_freedom": int(len(prediction)),
        "residual": residual.tolist(),
        "prediction_hash": frozen_hash,
        "prediction_unchanged": unchanged,
        "covariance_audit": audit,
    }
