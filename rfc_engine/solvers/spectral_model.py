from __future__ import annotations

from typing import Any

import numpy as np

from .utils import complex_json, require_finite


def run_spectral_model(cfg: dict[str, Any]) -> dict[str, Any]:
    """Audit a frozen real matrix candidate and its declared symmetry generators."""
    matrix = require_finite("matrix", cfg["matrix"])
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("matrix must be square")
    tolerance = float(cfg.get("tolerance", 1e-10))
    symmetry_error = float(np.linalg.norm(matrix - matrix.T))
    symmetric = symmetry_error <= tolerance
    if symmetric:
        values, vectors = np.linalg.eigh((matrix + matrix.T) / 2.0)
        reconstruction = vectors @ np.diag(values) @ vectors.T
        orthogonality_error = float(np.linalg.norm(vectors.T @ vectors - np.eye(len(values))))
    else:
        values, vectors = np.linalg.eig(matrix)
        reconstruction = vectors @ np.diag(values) @ np.linalg.inv(vectors)
        orthogonality_error = None
    reconstruction_error = float(np.linalg.norm(reconstruction - matrix))

    generator_audits: list[dict[str, Any]] = []
    for index, raw in enumerate(cfg.get("symmetry_generators", [])):
        generator = require_finite(f"symmetry_generator[{index}]", raw)
        if generator.shape != matrix.shape:
            raise ValueError("symmetry generator shape mismatch")
        commutator = matrix @ generator - generator @ matrix
        error = float(np.linalg.norm(commutator))
        generator_audits.append({"index": index, "commutator_error": error, "pass": error <= tolerance})

    required_symmetric = bool(cfg.get("require_symmetric", True))
    require_generator_invariance = bool(cfg.get("require_generator_invariance", True))
    pass_flags = {
        "finite": bool(np.all(np.isfinite(matrix))),
        "required_symmetry": bool((not required_symmetric) or symmetric),
        "reconstruction": reconstruction_error <= tolerance,
        "orthogonality": bool(orthogonality_error is None or orthogonality_error <= tolerance),
        "generator_invariance": bool((not require_generator_invariance) or all(x["pass"] for x in generator_audits)),
    }
    return {
        "success": bool(all(pass_flags.values())),
        "classification": "SPECTRAL_MODEL_AUDIT",
        "shape": list(matrix.shape),
        "symmetric": symmetric,
        "symmetry_error": symmetry_error,
        "eigenvalues": complex_json(values),
        "eigenvectors": np.real_if_close(vectors).tolist(),
        "reconstruction_error": reconstruction_error,
        "orthogonality_error": orthogonality_error,
        "symmetry_generator_audits": generator_audits,
        "pass_flags": pass_flags,
    }
