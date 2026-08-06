from __future__ import annotations

from typing import Any

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp


def run_transport(cfg: dict[str, Any]) -> dict[str, Any]:
    names = list(cfg["state_names"])
    if len(names) != len(set(names)) or not names:
        raise ValueError("state_names must be nonempty and unique")
    params = {key: float(value) for key, value in cfg.get("parameters", {}).items()}
    symbols = sp.symbols(names)
    parameter_symbols = {key: sp.Symbol(key) for key in params}
    local = {symbol.name: symbol for symbol in symbols} | parameter_symbols | {"t": sp.Symbol("t")}
    expressions = [sp.sympify(text, locals=local) for text in cfg["rhs_expressions"]]
    if len(expressions) != len(names):
        raise ValueError("one rhs expression is required per state")
    fn = sp.lambdify([local["t"], *symbols, *parameter_symbols.values()], expressions, "numpy")
    parameter_values = [params[key] for key in parameter_symbols]

    def rhs(time: float, state: np.ndarray) -> np.ndarray:
        return np.asarray(fn(float(time), *[float(x) for x in state], *parameter_values), dtype=float).reshape(-1)

    initial = np.asarray(cfg["initial_state"], dtype=float)
    if initial.shape != (len(names),) or not np.all(np.isfinite(initial)):
        raise ValueError("initial_state is invalid")
    t_span = tuple(map(float, cfg["t_span"]))
    if len(t_span) != 2 or t_span[1] <= t_span[0]:
        raise ValueError("t_span must increase")
    solution = solve_ivp(
        rhs,
        t_span,
        initial,
        method=cfg.get("method", "BDF"),
        rtol=float(cfg.get("rtol", 1e-9)),
        atol=float(cfg.get("atol", 1e-12)),
        max_step=float(cfg.get("max_step", np.inf)),
    )

    invariant_tolerance = float(cfg.get("invariant_tolerance", 1e-8))
    invariants: dict[str, Any] = {}
    invariant_pass = True
    for name, row in cfg.get("linear_invariants", {}).items():
        vector = np.asarray(row, dtype=float)
        if vector.shape != initial.shape:
            raise ValueError(f"linear invariant {name} has wrong shape")
        values = vector @ solution.y
        drift = float(np.max(np.abs(values - values[0])))
        invariants[name] = {"initial": float(values[0]), "max_abs_drift": drift, "tolerance": invariant_tolerance, "pass": drift <= invariant_tolerance}
        invariant_pass = invariant_pass and drift <= invariant_tolerance

    positivity_required = bool(cfg.get("positivity_required", False))
    positivity_tolerance = float(cfg.get("positivity_tolerance", 1e-10))
    minimum = float(np.min(solution.y))
    pass_flags = {
        "integrator": bool(solution.success),
        "finite_state": bool(np.all(np.isfinite(solution.y))),
        "linear_invariants": bool(invariant_pass),
        "positivity": bool((not positivity_required) or minimum >= -positivity_tolerance),
    }
    return {
        "success": bool(all(pass_flags.values())),
        "classification": "TRANSPORT_ODE_EXECUTION",
        "message": solution.message,
        "state_names": names,
        "t": solution.t.tolist(),
        "y": solution.y.tolist(),
        "final": solution.y[:, -1].tolist(),
        "minimum_state": minimum,
        "invariants": invariants,
        "nfev": int(solution.nfev),
        "pass_flags": pass_flags,
    }
