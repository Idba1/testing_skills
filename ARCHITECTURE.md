# Stage 2 — Skill Architecture

**Document version:** 1.0.0 | **Status:** Implemented baseline, pending instructor scope confirmation

## Design approach
A reusable AI skill is more than a saved prompt: it has explicit inputs, processing, instructions, optional tools, outputs, validation and failure handling. This architecture follows the seven rows in Week 12 slide 6 (the slide title says "Six-Part" but the displayed table has **seven** components). Course candidates follow Week 12 slide 7; the final evaluation dimensions follow Week 10 slide 6. Since the actual instructor assignment sheet/rubric was not uploaded, these are **course-grounded candidates**, not a confirmed compulsory submission list.

| Skill | Testing problem | Required input | Core processing | Output | Implemented tool | Output validation |
|---|---|---|---|---|---|---|
| Requirement Ambiguity Analyser | Unclear/conflicting requirements | Numbered source requirements | Classify issues; quote source; ask clarification | Evidence-linked ambiguity findings | None (instruction-based) | Every finding anchored to exact source; no fabricated rule |
| Test Case Generator with Coverage Constraints | Traceable scenario design | Requirement IDs, criteria, coverage constraints | Positive/negative/boundary/equivalence scenarios and open questions | Test case table; numeric probe candidates | `boundary_helper.py` (integer ranges only) | Range membership checks + human verification of test oracles |
| Coverage Gap Auditor | Missing coverage in existing suite | Numbered criteria, existing test records | Compare declared test categories to required kinds; separate semantic review | Structural gap report + review questions | `coverage_audit.py` (CSV) | IDs, counts, missing kinds, orphans; semantic audit remains manual |
| Automation Code Reviewer | Fragile/weak test automation | Code, language, framework, test intent | Assertions, selectors, waits, dependencies, maintainability, security | Line-specific review findings | None (instruction-based) | Exact code evidence, version-aware remediation; optional authorized execution |
| Workload Model Builder | Inconsistent performance load assumptions | Population, arrivals, duration, requests/session, think time, peak window | Unit validation; Little's Law; caveats | Estimates and assumptions report | `workload_model.py` (JSON) | Arithmetic/unit checks, assumption review; not a load test |
| Threat Model Generator | Overlooked security exposure in design | Assets, components, entry points, trust boundaries | Candidate STRIDE threats + control unknowns + test ideas | Proposed threat register | None (instruction-based) | Every threat maps to described architecture, human security review |
| Nine-Dimension Output Evaluator | Unsafe/unverifiable AI-generated QA output | Artifact, source evidence, risk level, evaluation entries | Risk-based depth, exact Week 10 dimensions, evidence | Advisory evaluation + completeness report | `evaluation_validator.py` (JSON) | Required dimensions/reviewer record present; human evaluates truth |

## Responsibility separation

1. **Instruction-based skill** = template for a human or authorized LLM to perform contextual analysis. The ZIP does not call an LLM API; sample reports for these skills are explicitly *hand-authored illustrations*.
2. **Deterministic Python script** = narrow, repeatable calculation/format check. Its generated sample JSONs were produced by actually executing the script and are part of the ZIP.
3. **Validation** = mechanical checks first; human judgment for semantics, risk, sign-off and stakeholder decisions. Script output must not be equated with correctness or release approval (Week 10 slide 18 and Week 12 slide 12).
4. **Data protection** = no live production calls, no stored API keys, no secrets, no autonomous write access, no offensive scanning, no third-party dependencies.

## Trace of sources to design
- **Week 10, PDF p. 3 (slide 6):** exact nine dimensions: Correctness, Completeness, Relevance, Consistency, Hallucination, Bias, Security, Maintainability, Traceability.
- **Week 10, PDF p. 12 (slide 15):** risk-based depth: low sanity; medium correctness/completeness/traceability; high nine; critical nine + independent human review.
- **Week 10, PDF p. 15 (slide 18):** AI generation → automated checks → human review → stakeholder confirmation → approved artifact.
- **Week 11, PDF pp. 11–13 (slides 12–14):** tool permission boundaries, wrong-target/prompt injection risks and approval gates.
- **Week 12, PDF pp. 4–8 (slides 5–9):** reusable skill differences, specification, seven candidate skills and coverage auditor exemplar.
- **Week 12, PDF pp. 9–14 (slides 10–15):** prompt versioning, advisory CI/AI checks, LLMOps and monitoring.
- **Working brief, PDF pp. 2–4:** student-proposed repository/testing and submission checks, explicitly **not an official instructor handout**.

## Intentional non-implementations
- No LLM client, MCP server or hosted agent: out of scope without user-approved service, credential, permissions and model version.
- No automatic acceptance or release gate based on probabilistic judgment.
- No invented numeric score/weights for the nine-dimension framework.
- No performance workload generation against a live server.
- No real source-code static analyzer or vulnerability scanner.
- No fabricated runtime execution logs for manually illustrated skills.

## Architecture approval status
The user requested completion after the earlier Stage 1 review; this is the implemented proposed architecture. Instructor-specific mandatory scope and submission details remain to be checked before final upload.
