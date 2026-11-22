#!/usr/bin/env python3
"""Compute an illustrative steady-state workload estimate from explicit assumptions."""
import argparse
import json
import math
from pathlib import Path


def _is_finite(value):
    """Check whether a number fits in the finite float range."""
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def _number(obj, key, *, positive=True, whole=False):
    value = obj.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not _is_finite(value):
        raise ValueError(f"{key} must be a finite number within the supported numeric range")
    if positive and value <= 0:
        raise ValueError(f"{key} must be > 0")
    if not positive and value < 0:
        raise ValueError(f"{key} must be >= 0")
    if whole and not float(value).is_integer():
        raise ValueError(f"{key} must be a whole number")
    return value


def build(data):
    """Calculate and validate a steady-state estimate from workload assumptions."""
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    title = data.get("scenario")
    if not isinstance(title, str) or not title.strip():
        raise ValueError("scenario must be a non-empty string")
    population = _number(data, "population_users", whole=True)
    arrivals = _number(data, "peak_session_arrivals_per_minute")
    duration = _number(data, "mean_session_duration_seconds")
    requests = _number(data, "mean_requests_per_session")
    peak_minutes = _number(data, "peak_window_minutes")
    think_time = _number(data, "mean_think_time_seconds", positive=False)
    if think_time > duration:
        raise ValueError("mean_think_time_seconds cannot exceed mean_session_duration_seconds")
    arrivals_per_second = arrivals / 60
    concurrency = arrivals_per_second * duration  # Little's Law: L = lambda * W
    derived = {
        "session_arrivals_per_second": arrivals_per_second,
        "mean_concurrent_sessions": concurrency,
        "requests_per_minute": arrivals * requests,
        "session_starts_in_peak_window": arrivals * peak_minutes,
    }
    for name, value in derived.items():
        if not _is_finite(value):
            raise ValueError(f"{name} exceeds the supported numeric range")
    derived = {name: round(value, 4 if name == "session_arrivals_per_second" else 2)
               for name, value in derived.items()}
    warnings = []
    if concurrency > population:
        warnings.append("Estimated mean concurrency exceeds declared user population; review assumptions/repeat sessions.")
    return {"scenario": title, "assumptions": data, "derived": derived,
        "formula": "mean_concurrent_sessions = (peak_session_arrivals_per_minute / 60) * mean_session_duration_seconds",
        "warnings": warnings,
        "limitations": ["Steady-state mean estimate, NOT a capacity guarantee or percentile/maximum concurrency.",
            "Requests-per-minute assumes mean requests per session over arrivals; does not model bursts or time-varying behavior.",
            "Think time is reported as an assumption, not added again to session duration.",
            "Peak-window session starts are not unique users; population is a context/consistency check."]}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    a = p.parse_args(argv)
    try:
        result = build(json.loads(a.input.read_text(encoding="utf-8")))
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        p.exit(2, f"Input error: {exc}\n")
    print(f"Wrote {a.output}")


if __name__ == "__main__":
    main()
