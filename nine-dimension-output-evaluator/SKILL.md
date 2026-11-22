# Nine-Dimension Output Evaluator

**Version:** 1.0.0  
**Owner:** Project maintainer (assignment author)  
**Course origin:** Week 10 slide 6 (PDF page 3); candidate listed Week 12 slide 7  
**Execution type:** Human/LLM evaluation specification + deterministic record-completeness validator

## Purpose and use boundary
Review AI-generated QA artifacts for the **exact nine course dimensions**, calibrating review depth to risk. This is an *evaluation and evidence checklist*, not automatic truth certification, a numerical scoring engine, or a release-approval mechanism.

## 1. Input
- **Required:** `artifact_id`, original AI output, source requirements/reference evidence, `risk_level` (`low|medium|high|critical`) and evaluation observations.
- **Optional:** artifact context, model/prompt version, independent review, test results, stakeholder decisions.
- **Helper JSON:** `artifact_id`, `risk_level`, `evaluations` keyed by exact names; each value has `status` (`pass|concern|not_checked`) and `evidence` (text). Low risk also requires a `sanity_check` record. Critical risk requires `independent_human_review` record: reviewer, independent_attested=true, decision, notes. This is **our implementation schema**, not an instructor-issued rubric.

## 2. Processing Logic
1. Determine cost of error and confirm risk level rather than deriving risk from format alone.
2. Apply course evaluation depth (Week 10 slide 15): **Low:** sanity check only; **Medium:** Correctness, Completeness, Traceability; **High:** all nine; **Critical:** all nine plus independent human review.
3. For each required dimension record evidence, concern, or not-checked state; verify every factual claim against primary sources.
4. Identify unverified data, privacy risk, bias, fabricated fields, traceability gaps and unsafe code patterns.
5. Present unresolved items without treating a clean-looking output as proof.
6. Optionally use the helper script to validate only the **presence and shape** of written evaluation evidence.
7. Release/acceptance and business-rule questions require accountable human stakeholders.

## 3. Instructions

```text
ROLE: Evidence-focused AI-output QA reviewer.
ARTIFACT: {{AI_generated_artifact}}
SOURCE: {{original_requirements_or_logs}}
RISK LEVEL: {{low_medium_high_critical_with_reason}}
Assess according to Week 10's exact dimensions in this spelling/order:
Correctness, Completeness, Relevance, Consistency, Hallucination, Bias,
Security, Maintainability, Traceability.
Use risk-tier depth: low sanity; medium correctness/completeness/traceability;
high all nine; critical all nine plus independent human review.
Per dimension provide status (pass/concern/not_checked), cited evidence,
what must be independently verified, and next review action.
Do not invent a numerical scoring rubric, relabel dimensions or mark
uncited claims as true. No AI-generated sign-off or release approval.
```

## 4. Tools
- Original sources, test logs and human review are the real basis for judgment.
- **Implemented helper:** `scripts/evaluation_validator.py` checks a prepared evaluation-record JSON for mandatory fields/dimensions and reviewer-record presence. It **does not** evaluate actual evidence truth or run an LLM.
- Run from root:

```bash
python nine-dimension-output-evaluator/scripts/evaluation_validator.py \
  --input nine-dimension-output-evaluator/examples/evaluation_input.json \
  --output nine-dimension-output-evaluator/examples/evaluation_report.json
```

## 5. Output
Evaluation table: `dimension | status | source/evidence | verification needed | remediation`; summary of concerns, missing evidence and reviewer decision where relevant. Helper JSON contains `structural_status`, required/missing dimensions, incomplete evidence, concerns and advisory. See examples (synthetic and **illustrative**, not an evaluation of a real system).

## 6. Validation
Use the exact nine names and the Week 10 risk-based selection. Check claims against source, execute generated code when authorized, inspect for security/privacy issues and human approval where appropriate. The helper validates structural fields only; `complete` means nothing about factual correctness, adequacy, independence of reviewer, or approval. **No official numeric weighting or score cutoffs were supplied**, so none are implemented.

## 7. Failure Handling
- **Missing artifact/source:** request it; do not pretend assessment was performed.
- **Risk level missing:** request classification; no silent default.
- **Unrecognized dimension/status or malformed JSON:** helper stops with a descriptive error.
- **Missing required check or empty/not-checked evidence:** helper returns `incomplete`, not artificial scores.
- **Critical reviewer absent or incomplete:** report an incomplete evaluation. The helper expects non-empty `reviewer` and `notes` strings, `independent_attested` set to JSON `true`, and `decision` set to `approved` or `changes_requested`. Reviewer independence is self-attested.
- **Safety concern:** flag for human response and avoid autonomous release decisions.

## Exact course evaluation dimensions
1. Correctness — technically and factually right?
2. Completeness — covers all relevant matters?
3. Relevance — addresses the actual requirement?
4. Consistency — internally and historically coherent?
5. Hallucination — unsupported facts/values/endpoints/rules?
6. Bias — unfair or unrepresentative assumptions?
7. Security — security or privacy exposure?
8. Maintainability — sustainable for the team?
9. Traceability — linked to the source requirement?

## Limitations
The program checks review record structure. Evidence assessment, scoring, approval, and independent human judgment remain outside the script. A `concern` can coexist with `structural_status: complete` because the latter is a formatting/completeness signal only.
