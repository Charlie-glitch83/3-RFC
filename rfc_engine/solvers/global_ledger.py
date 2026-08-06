from __future__ import annotations

from typing import Any

import numpy as np


def run_global_ledger(cfg: dict[str, Any]) -> dict[str, Any]:
    """Audit cross-sector conservation and unique ownership without filling missing values."""
    quantities = list(cfg["quantities"])
    sectors = list(cfg["sectors"])
    initial = np.asarray(cfg["initial_ledger"], dtype=float)
    final = np.asarray(cfg["final_ledger"], dtype=float)
    if initial.shape != (len(sectors), len(quantities)) or final.shape != initial.shape:
        raise ValueError("ledger matrices must be sector x quantity")
    if not np.all(np.isfinite(initial)) or not np.all(np.isfinite(final)):
        raise ValueError("ledger contains non-finite values")

    transfers = np.zeros_like(initial)
    transfer_records: list[dict[str, Any]] = []
    for rec in cfg.get("transfers", []):
        source = sectors.index(rec["source"])
        target = sectors.index(rec["target"])
        quantity = quantities.index(rec["quantity"])
        amount = float(rec["amount"])
        if source == target or amount < 0.0:
            raise ValueError("transfers require distinct sectors and nonnegative amount")
        transfers[source, quantity] -= amount
        transfers[target, quantity] += amount
        transfer_records.append(dict(rec))

    predicted = initial + transfers
    residual = final - predicted
    global_before = np.sum(initial, axis=0)
    global_after = np.sum(final, axis=0)
    tolerance = float(cfg.get("tolerance", 1e-10))
    owners = cfg.get("owners", {})
    ownership_complete = set(owners) == set(quantities) and all(owner in sectors for owner in owners.values())
    pass_flags = {
        "transfer_pairing": bool(np.max(np.abs(np.sum(transfers, axis=0))) <= tolerance),
        "local_closure": bool(np.max(np.abs(residual)) <= tolerance),
        "global_conservation": bool(np.max(np.abs(global_after - global_before)) <= tolerance),
        "ownership_complete": bool(ownership_complete),
    }
    return {
        "success": bool(all(pass_flags.values())),
        "classification": "GLOBAL_CONSERVATION_LEDGER_AUDIT",
        "quantities": quantities,
        "sectors": sectors,
        "predicted_final": predicted.tolist(),
        "declared_final": final.tolist(),
        "local_residual": residual.tolist(),
        "global_before": global_before.tolist(),
        "global_after": global_after.tolist(),
        "owners": owners,
        "transfers": transfer_records,
        "pass_flags": pass_flags,
    }
