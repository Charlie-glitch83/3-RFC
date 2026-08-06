from __future__ import annotations

from typing import Any

import numpy as np

from .utils import require_finite, relative_error


def accelerations(x: np.ndarray, m: np.ndarray, softening: float, coupling: float) -> np.ndarray:
    n = len(m)
    a = np.zeros_like(x, dtype=float)
    for i in range(n):
        for j in range(i + 1, n):
            r = x[j] - x[i]
            inv = (float(r @ r) + softening**2) ** (-1.5)
            pair = coupling * r * inv
            a[i] += m[j] * pair
            a[j] -= m[i] * pair
    return a


def energy(x: np.ndarray, v: np.ndarray, m: np.ndarray, softening: float, coupling: float) -> float:
    kinetic = float(np.sum(0.5 * m[:, None] * v * v))
    potential = 0.0
    for i in range(len(m)):
        for j in range(i + 1, len(m)):
            potential -= coupling * m[i] * m[j] / np.sqrt(float(np.sum((x[j] - x[i]) ** 2)) + softening**2)
    return kinetic + potential


def run_nbody(cfg: dict[str, Any]) -> dict[str, Any]:
    x = require_finite("positions", cfg["positions"]).copy()
    v = require_finite("velocities", cfg["velocities"]).copy()
    m = require_finite("masses", cfg["masses"]).copy()
    if x.ndim != 2 or v.shape != x.shape or m.shape != (x.shape[0],):
        raise ValueError("positions, velocities, and masses have incompatible shapes")
    if np.min(m) <= 0.0:
        raise ValueError("masses must be positive")
    dt = float(cfg["dt"])
    steps = int(cfg["steps"])
    softening = float(cfg.get("softening", 0.0))
    if "coupling_constant" not in cfg:
        raise ValueError("coupling_constant must be explicit; implicit physical constants are forbidden")
    coupling = float(cfg["coupling_constant"])
    if dt <= 0.0 or steps < 1 or softening < 0.0 or coupling <= 0.0:
        raise ValueError("invalid integration parameter")
    stride = int(cfg.get("checkpoint_stride", max(1, steps // 20)))
    if stride < 1:
        raise ValueError("checkpoint_stride must be positive")

    e0 = energy(x, v, m, softening, coupling)
    p0 = np.sum(m[:, None] * v, axis=0)
    com0 = np.sum(m[:, None] * x, axis=0) / np.sum(m)
    checkpoints: list[dict[str, Any]] = []
    for step in range(steps):
        v += 0.5 * dt * accelerations(x, m, softening, coupling)
        x += dt * v
        v += 0.5 * dt * accelerations(x, m, softening, coupling)
        if (step + 1) % stride == 0 or step + 1 == steps:
            checkpoints.append({
                "step": step + 1,
                "time": (step + 1) * dt,
                "positions": x.tolist(),
                "velocities": v.tolist(),
                "energy": energy(x, v, m, softening, coupling),
            })

    e1 = energy(x, v, m, softening, coupling)
    p1 = np.sum(m[:, None] * v, axis=0)
    com1 = np.sum(m[:, None] * x, axis=0) / np.sum(m)
    energy_drift = relative_error(e1, e0)
    momentum_error = float(np.linalg.norm(p1 - p0))
    energy_tolerance = float(cfg.get("relative_energy_tolerance", 1e-4))
    momentum_tolerance = float(cfg.get("momentum_tolerance", 1e-10))
    pass_flags = {
        "finite_state": bool(np.all(np.isfinite(x)) and np.all(np.isfinite(v))),
        "energy_drift": energy_drift <= energy_tolerance,
        "momentum_conservation": momentum_error <= momentum_tolerance,
        "checkpoint_complete": bool(checkpoints and checkpoints[-1]["step"] == steps),
    }
    return {
        "success": bool(all(pass_flags.values())),
        "classification": "PAIRWISE_LEAPFROG_EXECUTION",
        "dimension": int(x.shape[1]),
        "body_count": int(x.shape[0]),
        "coupling_constant": coupling,
        "final_positions": x.tolist(),
        "final_velocities": v.tolist(),
        "initial_energy": e0,
        "final_energy": e1,
        "relative_energy_drift": energy_drift,
        "relative_energy_tolerance": energy_tolerance,
        "momentum_error": momentum_error,
        "momentum_tolerance": momentum_tolerance,
        "initial_center_of_mass": com0.tolist(),
        "final_center_of_mass": com1.tolist(),
        "checkpoints": checkpoints,
        "pass_flags": pass_flags,
    }
