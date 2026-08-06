from __future__ import annotations

from typing import Any

import numpy as np

from .utils import require_finite


def run_fourier_field(cfg: dict[str, Any]) -> dict[str, Any]:
    """Generate a one-dimensional real finite-volume Gaussian field from frozen mode power."""
    power = require_finite("power_spectrum", cfg["power_spectrum"])
    if power.ndim != 1 or len(power) < 2 or np.min(power) < 0.0:
        raise ValueError("power_spectrum must be a nonnegative rfft-mode vector")
    seed = int(cfg["seed"])
    n = int(cfg.get("grid_size", 2 * (len(power) - 1)))
    if n < 2 or len(power) != n // 2 + 1:
        raise ValueError("power_spectrum length must equal grid_size//2+1")
    rng = np.random.default_rng(seed)
    coefficients = np.zeros(len(power), dtype=np.complex128)
    coefficients[0] = rng.normal(scale=np.sqrt(power[0]))
    nyquist = n % 2 == 0
    stop = len(power) - 1 if nyquist else len(power)
    if stop > 1:
        scale = np.sqrt(power[1:stop] / 2.0)
        coefficients[1:stop] = scale * (rng.normal(size=stop - 1) + 1j * rng.normal(size=stop - 1))
    if nyquist:
        coefficients[-1] = rng.normal(scale=np.sqrt(power[-1]))
    field = np.fft.irfft(coefficients, n=n, norm="ortho")
    reconstructed = np.fft.rfft(field, norm="ortho")
    reconstruction_error = float(np.max(np.abs(reconstructed - coefficients)))
    estimated_power = (np.abs(coefficients) ** 2).tolist()
    tolerance = float(cfg.get("reconstruction_tolerance", 1e-10))
    return {
        "success": reconstruction_error <= tolerance and bool(np.all(np.isfinite(field))),
        "classification": "FINITE_VOLUME_GAUSSIAN_FIELD_REALIZATION",
        "seed": seed,
        "grid_size": n,
        "field": field.tolist(),
        "fourier_coefficients": [{"real": float(z.real), "imag": float(z.imag)} for z in coefficients],
        "input_power_spectrum": power.tolist(),
        "realized_mode_power": estimated_power,
        "reconstruction_error": reconstruction_error,
        "reconstruction_tolerance": tolerance,
        "field_mean": float(np.mean(field)),
        "field_variance": float(np.var(field)),
    }
