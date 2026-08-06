from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import sympy as sp
from numpy.typing import NDArray
from scipy.integrate import solve_ivp


@dataclass
class ReactionNetwork:
    species: list[str]
    stoichiometry: NDArray[np.float64]
    rate_expressions: list[str]
    parameters: dict[str, float]
    invariants: dict[str, list[float]]

    @classmethod
    def from_config(cls, cfg: dict[str, Any]) -> "ReactionNetwork":
        return cls(
            species=list(cfg["species"]),
            stoichiometry=np.asarray(cfg["stoichiometry"], dtype=float),
            rate_expressions=list(cfg["rate_expressions"]),
            parameters={key: float(value) for key, value in cfg.get("parameters", {}).items()},
            invariants={key: list(map(float, value)) for key, value in cfg.get("invariants", {}).items()},
        )

    def _rate_function(self):
        symbols = sp.symbols(self.species)
        parameter_symbols = {key: sp.Symbol(key) for key in self.parameters}
        local = {symbol.name: symbol for symbol in symbols} | parameter_symbols
        expressions = [sp.sympify(text, locals=local) for text in self.rate_expressions]
        fn = sp.lambdify([*symbols, *parameter_symbols.values()], expressions, "numpy")
        parameter_values = [self.parameters[key] for key in parameter_symbols]

        def rates(state: NDArray[np.float64]) -> NDArray[np.float64]:
            values = fn(*[float(x) for x in state], *parameter_values)
            return np.asarray(values, dtype=float).reshape(-1)

        return rates

    def audit(self) -> dict[str, Any]:
        species_count = len(self.species)
        matrix = self.stoichiometry
        errors: list[str] = []
        if len(self.species) != len(set(self.species)) or not self.species:
            errors.append("species names must be nonempty and unique")
        if matrix.ndim != 2 or matrix.shape[0] != species_count:
            errors.append("stoichiometry shape mismatch")
        elif matrix.shape[1] != len(self.rate_expressions):
            errors.append("reaction/rate count mismatch")
        invariant_residuals: dict[str, list[float]] = {}
        if not errors:
            for name, row in self.invariants.items():
                array = np.asarray(row, dtype=float)
                if array.shape != (species_count,):
                    errors.append(f"invariant {name} shape mismatch")
                    continue
                residual = array @ matrix
                invariant_residuals[name] = residual.tolist()
                if not np.allclose(residual, 0.0, atol=1e-12):
                    errors.append(f"invariant {name} not conserved by stoichiometry")
        return {"pass": not errors, "errors": errors, "invariant_residuals": invariant_residuals}

    def integrate(
        self,
        y0: list[float],
        t_span: list[float],
        rtol: float,
        atol: float,
        method: str = "BDF",
        max_step: float = np.inf,
        positivity_tolerance: float = 1e-9,
        invariant_tolerance: float = 1e-8,
    ) -> dict[str, Any]:
        audit = self.audit()
        if not audit["pass"]:
            raise ValueError(audit["errors"])
        initial = np.asarray(y0, dtype=float)
        if initial.shape != (len(self.species),) or np.min(initial) < 0.0:
            raise ValueError("initial abundance vector is invalid")
        rates = self._rate_function()
        matrix = self.stoichiometry

        def rhs(_time: float, state: np.ndarray) -> np.ndarray:
            return matrix @ rates(state)

        solution = solve_ivp(
            rhs,
            (float(t_span[0]), float(t_span[1])),
            initial,
            method=method,
            rtol=rtol,
            atol=atol,
            max_step=max_step,
        )
        invariants: dict[str, Any] = {}
        invariant_pass = True
        for name, row in self.invariants.items():
            values = np.asarray(row, dtype=float) @ solution.y
            drift = float(np.max(np.abs(values - values[0])))
            invariants[name] = {"initial": float(values[0]), "max_abs_drift": drift, "tolerance": invariant_tolerance, "pass": drift <= invariant_tolerance}
            invariant_pass = invariant_pass and drift <= invariant_tolerance
        minimum = float(np.min(solution.y))
        pass_flags = {
            "integrator": bool(solution.success),
            "finite_state": bool(np.all(np.isfinite(solution.y))),
            "positivity": minimum >= -positivity_tolerance,
            "invariants": invariant_pass,
        }
        return {
            "success": bool(all(pass_flags.values())),
            "classification": "REACTION_NETWORK_EXECUTION",
            "message": solution.message,
            "species": self.species,
            "t": solution.t.tolist(),
            "y": solution.y.tolist(),
            "final": solution.y[:, -1].tolist(),
            "minimum_abundance": minimum,
            "positivity_tolerance": positivity_tolerance,
            "invariants": invariants,
            "nfev": int(solution.nfev),
            "audit": audit,
            "pass_flags": pass_flags,
        }
