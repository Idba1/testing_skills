# Test Case Generator with Coverage Constraints

**Version:** 1.0.0  
**Owner:** Project maintainer (assignment author)  
**Course origin:** Week 6 candidate, listed in Week 12 slide 7  
**Execution type:** LLM-driven test design + optional deterministic Python boundary probe

## Purpose and use boundary
Generate **candidate** test cases tied to explicitly provided requirements and named coverage constraints. Suitable for feature design review; not a replacement for actually running tests, resolving unclear requirements, or inventing test oracles.

## 1. Input
- **Required:** requirement IDs and acceptance criteria, plus explicitly stated coverage kinds and constraints.
- **Optional:** supported platform, test data limitations, known interfaces, risk, domain and workflow background.
- **Format:** numbered Markdown text; optional JSON input for numeric helper (see `examples/boundaries.json`).
- **Example requirement:** `REG-01: age must be between 18 and 65 inclusive.`
- **Do not assume:** status codes, error messages, numeric boundaries, or validation rules not supported by source text.

## 2. Processing Logic
1. Extract requirement references and known conditions; flag open questions rather than guessing.
2. Derive positive, negative, boundary, equivalence partition, and edge scenarios as *applicable*.
3. For each test identify preconditions, input/action, expected behavior based on the source, category and requirement reference.
4. Apply supplied coverage constraints; if not satisfiable, report gaps instead of silently relaxing them.
5. Deduplicate overlapping tests while preserving traceability and rationale.
6. Only for explicitly **integer range** requirements, optionally run `scripts/boundary_helper.py` to create candidate probe values near each declared bound.
7. Human review validates actual oracle and business requirements before cases are executable.

## 3. Instructions

```text
ROLE: QA test designer. REQUIREMENTS: {{numbered_requirements}}
COVERAGE CONSTRAINTS: {{required_scenario_types_and_limits}}
CONTEXT: {{approved_context}}
Generate a Markdown test case table:
case_id, requirement_id, category, preconditions, input_or_steps,
expected_result, requirement_evidence, uncertainty.
Use positive/negative/boundary/equivalence scenarios only when appropriate.
Every expected result must be backed by a supplied requirement or clearly marked
'Needs clarification'. Never invent API responses, validation text or policy.
Report requested coverage constraints that cannot be met.
Do not claim generated cases were executed.
```

## 4. Tools
- LLM for interpretation, test design and reviewing scenario combinations (not packaged as an API client).
- **Implemented helper:** `scripts/boundary_helper.py` (Python standard library only). Example:

```bash
python test-case-generator/scripts/boundary_helper.py \
  --input test-case-generator/examples/boundaries.json \
  --output test-case-generator/examples/generated_boundary_cases.json
```

The JSON schema requires `requirements` as a non-empty list of unique IDs with `minimum`, `maximum` (integers), Boolean `min_inclusive`/`max_inclusive`, optional positive integer `step` (probe distance). It returns `range_expected: within_range|outside_range`; **not real application pass/fail**.

## 5. Output
A traceable test case table with `test_id | requirement_id | type | preconditions | action/data | source-backed expected result | evidence | unresolved issues`; and optional range-probe JSON. See the Markdown illustration and actual generated JSON in `examples/`.

## 6. Validation
All test cases must have a requirement reference; positive, negative and boundary constraints should be checked *where explicitly applicable*. Each expected result must have a source or an unresolved marker. Probe values must honor inclusive/exclusive range flags. Cross-check duplicates and avoid invented rules; have a tester approve cases before execution. Run unit tests for the helper.

## 7. Failure Handling
- **Missing requirements:** request source; do not fill a template with invented details.
- **Ambiguous business rule:** create a clarification item; leave expected outcome pending.
- **Invalid range, missing booleans, duplicate IDs, bad JSON:** helper exits non-zero with an input error.
- **Unsupported decimal/text boundary:** helper handles integers only; handle manually or implement a reviewed extension.
- **Unsatisfied coverage constraint:** report it explicitly.
- **LLM or tool failure:** retain source input, report failure and generate no unverified result.

## Limitations
The helper checks numeric membership under stated bounds only; it does not execute an SUT, know other business constraints, or prove requirement/test coverage. Example test cases are illustrative until an LLM run and human validation are recorded.
