# QA Testing Skills — Generative AI for Software Testing

**Original educational project | Version 1.0.0 | Python 3.9+ (standard library only)**

A collection of seven *course-grounded candidate* reusable AI software testing skills. Each skill has `SKILL.md` with **Input, Processing Logic, Instructions, Tools, Output, Validation, Failure Handling**. Four of the seven also include narrow deterministic Python helpers, examples and unit tests.

> **Academic scope warning:** The Week 10–12 lecture slides substantiate the candidate skills and framework, but the original **official assignment instructions, grading rubric and submission format were not provided**. The supplied "Assignment Working Brief" itself says it is student-prepared and unofficial. Confirm required scope with the instructor before submission. The package is a working implementation, not a claim of official grading compliance.

## Skill library

| Skill | Folder | Available implementation |
|---|---|---|
| Requirement Ambiguity Analyser | `requirement-ambiguity-analyser/` | Reusable LLM instructions + hand-authored illustration |
| Test Case Generator with Coverage Constraints | `test-case-generator/` | LLM instructions + *integer range probe* script + tests |
| Coverage Gap Auditor | `coverage-gap-auditor/` | LLM semantic audit instructions + *CSV structural gap* script + tests |
| Automation Code Reviewer | `automation-code-reviewer/` | Reusable LLM instructions + code review illustration |
| Workload Model Builder | `workload-model-builder/` | LLM planning instructions + *calculation* script + tests |
| Threat Model Generator | `threat-model-generator/` | Reusable LLM instructions + candidate register illustration |
| Nine-Dimension Output Evaluator | `nine-dimension-output-evaluator/` | LLM/human evidence rubric + *record schema* script + tests |

## Repository layout

```text
qa-testing-skills/
├── README.md
├── ARCHITECTURE.md
├── SOURCES_AND_ASSUMPTIONS.md
├── SUBMISSION_CHECKLIST.md
├── verification/
│   ├── run_tests.py
│   ├── TEST_MATRIX.md
│   └── EXECUTION_LOG.md
├── requirement-ambiguity-analyser/
│   ├── SKILL.md
│   └── examples/
├── test-case-generator/
│   ├── SKILL.md
│   ├── scripts/boundary_helper.py
│   ├── tests/test_boundary_helper.py
│   └── examples/
├── coverage-gap-auditor/
│   ├── SKILL.md
│   ├── scripts/coverage_audit.py
│   ├── tests/test_coverage_audit.py
│   └── examples/
├── automation-code-reviewer/
│   ├── SKILL.md
│   └── examples/
├── workload-model-builder/
│   ├── SKILL.md
│   ├── scripts/workload_model.py
│   ├── tests/test_workload_model.py
│   └── examples/
├── threat-model-generator/
│   ├── SKILL.md
│   └── examples/
└── nine-dimension-output-evaluator/
    ├── SKILL.md
    ├── scripts/evaluation_validator.py
    ├── tests/test_evaluation_validator.py
    └── examples/
```

## Prerequisites
Python 3.9 or later, no third-party packages or LLM credentials. Developed for a command-line environment and compatible with Windows, Linux and macOS. An LLM service is needed only if you choose to manually *run* the instruction-based skills; no LLM API is provided or silently called.

## Setup and usage

1. Extract the ZIP and open a terminal *inside the `qa-testing-skills` folder*.
2. Read `ARCHITECTURE.md` for design decisions.
3. Open the `SKILL.md` for the task you want to perform. Fill the prompt template with original numbered requirements/context and review the output manually.
4. Run the appropriate deterministic helper where useful. The commands below work from repository root:

```bash
python test-case-generator/scripts/boundary_helper.py --input test-case-generator/examples/boundaries.json --output test-case-generator/examples/generated_boundary_cases.json
python coverage-gap-auditor/scripts/coverage_audit.py --requirements coverage-gap-auditor/examples/requirements.csv --tests coverage-gap-auditor/examples/tests.csv --output coverage-gap-auditor/examples/coverage_report.json
python workload-model-builder/scripts/workload_model.py --input workload-model-builder/examples/workload.json --output workload-model-builder/examples/workload_report.json
python nine-dimension-output-evaluator/scripts/evaluation_validator.py --input nine-dimension-output-evaluator/examples/evaluation_input.json --output nine-dimension-output-evaluator/examples/evaluation_report.json
```

On Windows, `py` may replace `python` if configured. The scripts use no absolute paths, real credentials, network requests or external dependencies.

## Run tests

```bash
python verification/run_tests.py
```

Test source in each implemented skill's `tests/` directory. Actual test and example execution evidence: `verification/EXECUTION_LOG.md`; test coverage details: `verification/TEST_MATRIX.md`. A script's non-zero exit on invalid input is intentional failure handling.

## Example scenario and actual results

- The range helper derives probes (17, 18, 19, 64, 65, 66) for declared inclusive age limits [18,65]; it reports only range membership.
- The CSV coverage helper reports, for **synthetic data only**, 1 covered, 1 partial, 1 uncovered requirement; 1 orphan and 1 unlinked test. This is *declared test-type presence*, not semantic coverage.
- The synthetic steady-state workload helper computes 360 mean concurrent sessions from 120 session starts/min and 180 s duration; **not** measured peak load.
- The evaluation record helper deliberately reports `incomplete` for a fictional high-risk record because some evidence has not been checked. This is **appropriate behavior**, not a failed script.

## Limitations and safe-use policy

- `SKILL.md` is a reusable design specification, not an automatically deployable agent or MCP server.
- No claim that LLM-only examples were executed; no real system-under-test was exercised.
- No autonomous blocking of merges based on AI judgments; critical issues require human review.
- Do not send credentials/PII to unauthorized models or run generated commands against production.
- Keep model and prompt versions, inputs and review outcomes with future actual LLM-run evidence (Week 12 prompt versioning and monitoring).
- The Week 10 nine evaluation dimensions are kept verbatim; numerical scoring weights were **not** specified, so none are made up.

## Suggested demonstration to instructor

Explain the architecture in `ARCHITECTURE.md`, show one `SKILL.md` (e.g., Coverage Gap Auditor), run `python verification/run_tests.py`, run the CSV coverage example, show its orphan/unlinked results, and explain why the structural coverage claim needs a tester's semantic review. Then show `SOURCES_AND_ASSUMPTIONS.md` to distinguish verified lecture guidance from your proposed implementation.

## Future improvements (not implemented)

- Authorized read-only repository and requirement-tool integrations; versioned prompts/model reference cases.
- Semantic test scenario audits with evidence and explicit human approval.
- More boundary types and richer coverage metrics once justified by requirements.
- A secure CI pipeline for **mechanical** checks; optional advisory AI review without autonomous release gates.

## Source attribution
Original design based on provided course Week 10/11/12 lecture materials; attribution by page/slide in `SOURCES_AND_ASSUMPTIONS.md`. Project scripts, prompt templates and examples are written independently. Example scenarios are fictitious.
