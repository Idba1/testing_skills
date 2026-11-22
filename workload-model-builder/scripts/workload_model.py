#!/usr/bin/env python3
"""Compute an illustrative steady-state workload estimate from explicit assumptions."""
import argparse
import json
import math
from pathlib import Path


def _number(obj, key, *, positive=True, whole=False):
    value = obj.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{key} must be a finite number")
    if positive and value <= 0:
        raise ValueError(f"{key} must be > 0")
    if not positive and value < 0:
        raise ValueError(f"{key} must be >= 0")
    if whole and not float(value).is_integer():
        raise ValueError(f"{key} must be a whole number")
    return value


def build(data):
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
    concurrency = arrivals / 60 * duration  # Little's Law: L = lambda * W
    warnings = []
    if concurrency > population:
        warnings.append("Estimated mean concurrency exceeds declared user population; review assumptions/repeat sessions.")
    return {"scenario": title, "assumptions": data, "derived": {
        "session_arrivals_per_second": round(arrivals / 60, 4),
        "mean_concurrent_sessions": round(concurrency, 2),
        "requests_per_minute": round(arrivals * requests, 2),
        "session_starts_in_peak_window": round(arrivals * peak_minutes, 2)},
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
