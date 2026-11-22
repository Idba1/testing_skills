#!/usr/bin/env python3
"""Generate candidate integer-boundary values from explicitly supplied limits.

This only checks declared numeric range membership, not system behaviour.
"""
import argparse
import json
from pathlib import Path


def _int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    return value


def generate(data):
    """Return sorted probes and their membership for each declared interval."""
    if not isinstance(data, dict) or not isinstance(data.get("requirements"), list) or not data["requirements"]:
        raise ValueError("'requirements' must be a non-empty list")
    items = []
    seen_ids = set()
    for requirement in data["requirements"]:
        if not isinstance(requirement, dict):
            raise ValueError("each requirement must be an object")
        rid = requirement.get("id")
        if not isinstance(rid, str) or not rid.strip() or rid in seen_ids:
            raise ValueError("each requirement needs a unique non-empty string id")
        seen_ids.add(rid)
        lo = _int(requirement.get("minimum"), f"{rid}.minimum")
        hi = _int(requirement.get("maximum"), f"{rid}.maximum")
        step = _int(requirement.get("step", 1), f"{rid}.step")
        if step <= 0 or lo > hi:
            raise ValueError(f"{rid}: step must be positive and minimum <= maximum")
        li = requirement.get("min_inclusive")
        ui = requirement.get("max_inclusive")
        if not isinstance(li, bool) or not isinstance(ui, bool):
            raise ValueError(f"{rid}: min_inclusive/max_inclusive must be booleans")
        first_allowed = lo if li else lo + 1
        last_allowed = hi if ui else hi - 1
        if first_allowed > last_allowed:
            raise ValueError(f"{rid}: no integer can satisfy the declared interval")
        # Step is a *probe distance*, not a claim that valid values are spaced this way.
        probes = sorted(set((lo - step, lo, lo + step, hi - step, hi, hi + step)))
        candidates = []
        for value in probes:
            within = first_allowed <= value <= last_allowed
            candidates.append({"value": value, "range_expected": "within_range" if within else "outside_range"})
        items.append({"requirement_id": rid, "declared_interval": {
            "minimum": lo, "maximum": hi, "min_inclusive": li, "max_inclusive": ui,
            "probe_distance": step}, "candidate_values": candidates})
    return {"analysis_type": "integer_range_probes", "requirements": items,
            "limitation": "Range membership only; actual acceptance, other constraints and expected UI/API responses require requirement review."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        report = generate(data)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        parser.exit(2, f"Input error: {exc}\n")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
