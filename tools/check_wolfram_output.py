#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def token(field: str, value: str) -> re.Pattern[str]:
    return re.compile(rf'["\\]?{re.escape(field)}["\\]?\s*->\s*{value}\b')


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply the frozen manufactured Wolfram-output gate")
    parser.add_argument("--call", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--json-output")
    args = parser.parse_args()
    expectations = json.loads((ROOT / "config/WOLFRAM_EXPECTATIONS.json").read_text())["calls"]
    if args.call not in expectations:
        raise SystemExit(f"unknown call: {args.call}")
    text = Path(args.output).read_text(encoding="utf-8")
    rule = expectations[args.call]
    failures: list[str] = []
    for field in rule.get("required_true", []):
        if not token(field, "True").search(text):
            failures.append(f"{field} is not True")
    for field in rule.get("required_false", []):
        if not token(field, "False").search(text):
            failures.append(f"{field} is not False")
    for value in rule.get("required_contains", []):
        if value not in text:
            failures.append(f"missing required text: {value}")
    for field in rule.get("manual_review", []):
        if field not in text:
            failures.append(f"manual-review field missing: {field}")
    result = {
        "call_id": args.call,
        "classification": "WOLFRAM_MANUFACTURED_GATE",
        "status": "PASS_WITH_MANUAL_INTERPRETATION" if not failures else "FAIL",
        "failures": failures,
        "manual_review_fields": rule.get("manual_review", []),
        "decision_rule": rule["decision"],
        "warning": "A manufactured symbolic gate never promotes a module to PHYSICALLY_EXECUTED. Parent-bound substitutions and module gates remain mandatory."
    }
    rendered = json.dumps(result, indent=2) + "\n"
    if args.json_output:
        Path(args.json_output).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
