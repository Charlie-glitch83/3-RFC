#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
I_RUN = "I-180-20260810T134326Z"
G_RUN = "G-160-20260809T025252Z"
AUDIT_REL = "audit/G160_I_CHILD_INTERFACE_DEFECT_20260810.json"
CLAIM_REL = "audit/G160_I_CHILD_INTERFACE_REPAIR_CLAIM.json"
MARKER = "## Superseding I-child interface repair"
NEW_G_BINDINGS = [
    "i_route_registry",
    "i_route_resolved_process_activity",
    "i_route_to_relational_ancestry",
    "i_aggregate_no_loss_reconstruction",
    "i_geometry_child_packet",
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()

