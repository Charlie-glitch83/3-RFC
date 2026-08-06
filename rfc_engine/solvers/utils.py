from __future__ import annotations

import math
from typing import Any

import numpy as np


PLACEHOLDER_PREFIXES = ("__BIND_", "__DERIVE_", "__FILL_", "<BIND", "<DERIVE")


def unresolved_placeholders(obj: Any, path: str = "$") -> list[str]:
    """Return paths containing intentionally unresolved execution bindings."""
    found: list[str] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            found.extend(unresolved_placeholders(value, f"{path}.{key}"))
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            found.extend(unresolved_placeholders(value, f"{path}[{index}]"))
    elif isinstance(obj, str) and obj.strip().startswith(PLACEHOLDER_PREFIXES):
        found.append(path)
    return found


def require_finite(name: str, array: Any) -> np.ndarray:
    value = np.asarray(array, dtype=float)
    if not np.all(np.isfinite(value)):
        raise ValueError(f"{name} contains non-finite values")
    return value


def complex_json(values: Any, tolerance: float = 1e-14) -> list[Any]:
    """Serialize real/complex eigenvalues without losing imaginary parts."""
    flat = np.asarray(values).reshape(-1)
    out: list[Any] = []
    for item in flat:
        z = complex(item)
        if abs(z.imag) <= tolerance:
            out.append(float(z.real))
        else:
            out.append({"real": float(z.real), "imag": float(z.imag)})
    return out


def relative_error(final: float, initial: float) -> float:
    scale = max(abs(initial), np.finfo(float).tiny)
    return float(abs(final - initial) / scale)


def matrix_psd_audit(matrix: Any, tolerance: float = 1e-12) -> dict[str, Any]:
    c = require_finite("matrix", matrix)
    if c.ndim != 2 or c.shape[0] != c.shape[1]:
        raise ValueError("matrix must be square")
    sym = (c + c.T) / 2.0
    symmetry_error = float(np.linalg.norm(c - c.T, ord=np.inf))
    eig = np.linalg.eigvalsh(sym)
    return {
        "shape": list(c.shape),
        "symmetry_error": symmetry_error,
        "symmetric": bool(symmetry_error <= tolerance),
        "eigenvalues": eig.tolist(),
        "minimum_eigenvalue": float(np.min(eig)),
        "positive_semidefinite": bool(np.min(eig) >= -tolerance),
        "positive_definite": bool(np.min(eig) > tolerance),
        "tolerance": float(tolerance),
    }


def within(value: float, tolerance: float) -> bool:
    return bool(math.isfinite(value) and abs(value) <= tolerance)
