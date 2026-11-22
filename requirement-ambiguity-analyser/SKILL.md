# Requirement Ambiguity Analyser

**Version:** 1.0.0  
**Owner:** Project maintainer (assignment author)  
**Course origin:** Week 5 candidate, listed in Week 12 slide 7  
**Execution type:** Reusable AI instruction skill; no script

## Purpose and use boundary
Inspect source requirements for vague, missing, contradictory, or difficult-to-verify statements; present *evidence-linked clarification requests*. Intended for testers and analysts during requirement refinement. Do not use it to approve requirements, invent product rules, or decide business policy without a stakeholder.

## 1. Input
- **Required:** verbatim requirement statement(s) with stable identifiers and source/version information.
- **Optional:** acceptance criteria, glossary, known constraints, stakeholder notes, intended users, and domain context.
- **Format:** Markdown/text or a numbered requirement list; redact private data before submission.
- **Example:** `AUTH-01: The system must lock users quickly after many failed logins.`
- If source text is not identified, mark findings as pending traceability rather than assigning fake IDs.

## 2. Processing Logic
1. Identify each requirement and preserve its exact wording.
2. Flag (proposed working taxonomy): vague qualifiers, missing measurable rules, conflicting statements, and untestable/unsupported conditions. Categories are a design choice; Week 12 does not prescribe their labels.
3. Quote the *minimum* source excerpt for each finding and explain its test impact.
4. Check whether additional context resolves the issue; do not mistake an unfamiliar domain term for an error without evidence.
5. Produce a specific clarification question for the stakeholder and, where possible, a conditional rewrite explicitly marked **proposal—not approved requirement**.
6. Mark unresolved findings and request approval for business-rule decisions.

## 3. Instructions
Use this prompt with the supplied material:

```text
ROLE: You are a software requirements QA analyst.
INPUT REQUIREMENTS: {{numbered_source_requirements}}
OPTIONAL CONTEXT: {{verified_domain_context_or_none}}
TASK: Identify vague wording, incomplete constraints, conflicts, and untestable conditions.
For each finding include requirement_id, verbatim_excerpt, category,
why_it_blocks_a_reliable_test, clarification_question, and optional_proposed_rewrite.
Do not invent thresholds, lockout counts, timing limits, error strings, or acceptance rules.
Treat every proposed rewrite as a hypothesis until stakeholder confirmation.
If evidence is unavailable, state 'Unverified' instead of guessing.
Return findings as a Markdown table, followed by unresolved questions.
```

## 4. Tools
- An LLM for interpretation of plain-text requirements; no tool invocation is inherently required.
- Optional read-only requirements-repository lookup *if* access exists and is authorized.
- No code or external service is implemented by this repository for this skill.

## 5. Output
A Markdown table with: `finding_id | requirement_id | source_excerpt | category | impact | question | proposed_rewrite | confidence_or_uncertainty`.
Add `Unresolved stakeholder decisions` and `No-findings note` if relevant. See `examples/example_findings.md` (a **hand-authored illustration**, not a model execution result).

## 6. Validation
Every finding must reference an existing input ID and exact excerpt; there must be no fabricated number or policy. Questions should allow a decision-maker to clarify the rule. Validate any proposed rewrite against the provided source and label assumptions. Have a domain reviewer approve changed requirements; never infer approval from a fluent output.

## 7. Failure Handling
- **No requirements / missing text:** stop and request the original statements.
- **Unnumbered requirements:** ask for canonical IDs; temporary line labels are permissible only when explicitly marked temporary.
- **Contradiction unresolved:** present both statements and request the owner to reconcile them.
- **Unclear domain term:** ask for glossary/context instead of assigning an arbitrary meaning.
- **Tool unavailable:** analyze only available source text and disclose the missing context.
- **Sensitive content:** redact or decline unsafe distribution of credentials/PII.

## Limitations and evidence
This skill does not perform AI inference automatically in the provided ZIP. The example is a documented demonstration template; a live run would need an authorized LLM and recorded reviewer feedback. Version prompts with source and model details when running in production (Week 12 slides 10–11).
