#!/usr/bin/env python3
"""Check the structure/completeness of human-authored nine-dimension evaluations.

Does not score or validate truthfulness of evidence. Advisory; never approves artifacts.
"""
import argparse
import json
from pathlib import Path

DIMENSIONS = ("Correctness", "Completeness", "Relevance", "Consistency", "Hallucination",
              "Bias", "Security", "Maintainability", "Traceability")
REQUIRED = {"low": (), "medium": ("Correctness", "Completeness", "Traceability"),
            "high": DIMENSIONS, "critical": DIMENSIONS}
STATES = ("pass", "concern", "not_checked")


def validate(data):
    """Validate core fields and report missing or incomplete review evidence."""
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    artifact = data.get("artifact_id")
    risk = data.get("risk_level")
    evaluations = data.get("evaluations")
    if not isinstance(artifact, str) or not artifact.strip():
        raise ValueError("artifact_id must be a non-empty string")
    if not isinstance(risk, str) or risk not in REQUIRED:
        raise ValueError("risk_level must be low, medium, high, or critical")
    if not isinstance(evaluations, dict):
        raise ValueError("evaluations must be an object")
    if set(evaluations) - set(DIMENSIONS):
        raise ValueError("unknown dimensions; names must match Week 10 exactly")
    incomplete, concerns = [], []
    required = list(REQUIRED[risk])
    missing = [d for d in required if d not in evaluations]
    for dim, check in evaluations.items():
        if not isinstance(check, dict) or check.get("status") not in STATES:
            raise ValueError(f"{dim}: expected status pass, concern, or not_checked")
        if check["status"] == "concern":
            concerns.append(dim)
        if check["status"] == "not_checked" or not isinstance(check.get("evidence"), str) or not check["evidence"].strip():
            incomplete.append(dim)
    sanity_ok = True
    if risk == "low":
        sanity = data.get("sanity_check")
        sanity_ok = (isinstance(sanity, dict) and sanity.get("status") in ("pass", "concern")
                     and isinstance(sanity.get("evidence"), str) and bool(sanity["evidence"].strip()))
    reviewer = data.get("independent_human_review")
    reviewer_recorded = (isinstance(reviewer, dict)
        and isinstance(reviewer.get("reviewer"), str) and bool(reviewer["reviewer"].strip())
        and reviewer.get("decision") in ("approved", "changes_requested")
        and reviewer.get("independent_attested") is True
        and isinstance(reviewer.get("notes"), str) and bool(reviewer["notes"].strip()))
    review_missing = risk == "critical" and not reviewer_recorded
    complete = not missing and not incomplete and sanity_ok and not review_missing
    return {"artifact_id": artifact, "risk_level": risk, "required_dimensions": required,
            "missing_dimensions": missing, "incomplete_dimension_evidence": sorted(incomplete),
            "concern_dimensions": sorted(concerns), "sanity_check_recorded": sanity_ok if risk == "low" else None,
            "independent_human_review_recorded": reviewer_recorded if risk == "critical" else None,
            "structural_status": "complete" if complete else "incomplete",
            "advisory": "Structural completeness is not output correctness or approval. Human evidence checks are essential; recorded reviewer independence is self-attested, not verified."}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    a = p.parse_args(argv)
    try:
        report = validate(json.loads(a.input.read_text(encoding="utf-8")))
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        p.exit(2, f"Input error: {exc}\n")
    print(f"Wrote {a.output}")


if __name__ == "__main__":
    main()
