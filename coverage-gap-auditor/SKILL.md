# Coverage Gap Auditor

**Version:** 1.0.0  
**Owner:** Project maintainer (assignment author)  
**Course origin:** Week 6 candidate, listed in Week 12 slides 7 and 9  
**Execution type:** Read-only deterministic coverage inventory + optional human/LLM semantic audit

## Purpose and use boundary
Compare requirements/acceptance criteria to an existing suite and identify **covered, partially covered, uncovered** elements with evidence. *Do not generate new test cases* in this skill; recommendations may identify missing types or scenarios without writing them. Match the Week 12 worked specification (slide 9).

## 1. Input
- **Required:** source requirements with stable IDs, named coverage constraints, and existing test records with their linked requirement IDs.
- **Optional:** boundary specifications, decision tables, code-execution evidence, justified exclusions and test history.
- **CSV schema:** `requirements.csv`: `requirement_id,requirement_text,required_kinds` (`positive|negative|boundary` separated by `|`). `tests.csv`: `test_id,requirement_id,kind,expected_result`. Files must contain headers and non-empty IDs/descriptions (except test references may be blank to flag unlinked rows).

## 2. Processing Logic
1. Validate stable IDs, schema and declared coverage kinds.
2. Map each test's declared kind to its referenced requirement.
3. Flag orphan IDs and tests missing a requirement reference.
4. Classify each requirement by **declared test-kind presence**: covered (all requested kinds present), partial (some), uncovered (none).
5. A human/LLM must separately review requirement semantics, boundary completeness, condition combinations and scope creep; the CSV script does **not** infer these from titles or links.
6. Output gaps grouped by test kind and requirement; never write replacement tests.

## 3. Instructions

```text
ROLE: QA coverage auditor. INPUT: {{numbered_acceptance_criteria}}
EXISTING SUITE: {{test_cases_with_requirement_links}}
CHECKS: requirement coverage; boundary completeness;
condition combinations; scope creep.
Report only gaps in a table: criterion_id, check_type, observed_evidence,
missing_or_partial_area, severity_if_evidenced, question_or_next_review.
Do NOT generate or rewrite test cases. Do not invent acceptance criteria.
If criteria are absent or unnumbered, request them before auditing.
Distinguish 'declared kind present' from meaningful coverage and execution.
```

## 4. Tools
- **Implemented script:** `scripts/coverage_audit.py` with Python standard library CSV/JSON.
- Example command from repository root:

```bash
python coverage-gap-auditor/scripts/coverage_audit.py \
  --requirements coverage-gap-auditor/examples/requirements.csv \
  --tests coverage-gap-auditor/examples/tests.csv \
  --output coverage-gap-auditor/examples/coverage_report.json
```

- Optional AI semantic review is *not implemented* as an external LLM client. It remains an advisory human-reviewed task.

## 5. Output
JSON `summary`, per-requirement `status`, `required_kinds`, `found_kinds`, `missing_kinds`, linked IDs, `orphan_tests`, `unlinked_tests` and a limitations disclosure. The actual sample is `examples/coverage_report.json`. For semantic review use a gap-list table with source excerpts.

## 6. Validation
Every result references existing input IDs; category names match expected types; no unknown requirement is treated as covered. Verify `covered + partial + uncovered = total`. Spot-check that linked cases genuinely test the scenario and assertion; especially inspect boundaries and combinations before approving conclusions.

## 7. Failure Handling
- **Missing required CSV columns, duplicate column names, incorrect row widths, or CSV parser errors:** stop with a clear input error. Use an explicit empty field for a blank test requirement reference.
- **Duplicate IDs, empty requirement text/test expected result, invalid kind:** stop with clear input error.
- **Orphan or blank test requirement ID:** report separately; do not hide/drop silently.
- **Unnumbered/missing criteria:** ask for IDs; do not infer acceptance criteria.
- **Unavailable LLM or uncertain semantics:** deliver only structural results and label the gap.

## Limitations
`covered` means **declared type presence**, not real executable completeness, correctness, or successful test runs. Do not use this as an autonomous release gate. Matches Week 12 preference for advisory AI judgment (slide 12).
