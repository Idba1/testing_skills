#!/usr/bin/env python3
"""Audit *declared* test type coverage against explicitly supplied requirement IDs.

A match of IDs/kinds is not evidence of meaningful test execution or semantic coverage.
"""
import argparse
import csv
import json
from pathlib import Path

KINDS = {"positive", "negative", "boundary"}


def _read_csv(path, required):
    with Path(path).open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames is None or not required.issubset(set(reader.fieldnames)):
            raise ValueError(f"{path}: required columns: {', '.join(sorted(required))}")
        return [{key: (val or "").strip() for key, val in row.items() if key is not None}
                for row in reader]


def audit(requirements, tests):
    if not requirements:
        raise ValueError("at least one requirement is needed")
    req_index = {}
    for r in requirements:
        rid = r["requirement_id"]
        if not rid or not r["requirement_text"] or rid in req_index:
            raise ValueError("requirements need unique non-empty IDs and descriptions")
        kinds = {v.strip().lower() for v in r["required_kinds"].split("|") if v.strip()}
        if not kinds or not kinds.issubset(KINDS):
            raise ValueError(f"{rid}: required_kinds must be chosen from {sorted(KINDS)}")
        req_index[rid] = {"requirement_id": rid, "required_kinds": kinds, "found_kinds": set(), "test_ids": []}
    orphan_tests, unlinked_tests, seen_tests = [], [], set()
    for t in tests:
        tid = t["test_id"]
        if not tid or tid in seen_tests or not t["expected_result"]:
            raise ValueError("test IDs must be unique/non-empty and expected_result is required")
        seen_tests.add(tid)
        kind = t["kind"].lower()
        if kind not in KINDS:
            raise ValueError(f"test {tid}: unknown kind '{kind}'")
        rid = t["requirement_id"]
        if not rid:
            unlinked_tests.append(tid)
        elif rid not in req_index:
            orphan_tests.append({"test_id": tid, "unknown_requirement_id": rid})
        else:
            req_index[rid]["found_kinds"].add(kind)
            req_index[rid]["test_ids"].append(tid)
    entries, totals = [], {"covered": 0, "partial": 0, "uncovered": 0}
    for row in req_index.values():
        missing = row["required_kinds"] - row["found_kinds"]
        status = "covered" if not missing else "partial" if row["found_kinds"] else "uncovered"
        totals[status] += 1
        entries.append({"requirement_id": row["requirement_id"], "status": status,
                        "required_kinds": sorted(row["required_kinds"]),
                        "found_kinds": sorted(row["found_kinds"]),
                        "missing_kinds": sorted(missing), "linked_test_ids": sorted(row["test_ids"])})
    return {"audit_type": "declared_test_type_presence", "summary": {"total_requirements": len(entries), **totals,
            "orphan_test_count": len(orphan_tests), "unlinked_test_count": len(unlinked_tests)},
            "requirements": entries, "orphan_tests": orphan_tests, "unlinked_tests": unlinked_tests,
            "limitation": "Declared test type presence is not semantic coverage, test execution, or effectiveness. Human review of scenarios, boundaries and assertions is required."}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--requirements", required=True, type=Path)
    p.add_argument("--tests", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    a = p.parse_args(argv)
    try:
        result = audit(_read_csv(a.requirements, {"requirement_id", "requirement_text", "required_kinds"}),
                       _read_csv(a.tests, {"test_id", "requirement_id", "kind", "expected_result"}))
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except (ValueError, OSError) as exc:
        p.exit(2, f"Input error: {exc}\n")
    print(f"Wrote {a.output}")


if __name__ == "__main__":
    main()
