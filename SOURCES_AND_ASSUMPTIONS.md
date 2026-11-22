# Source Authority, Scope and Academic Integrity

## Provided source materials
1. `GenAI_Testing_Week10.pptx (1).pdf` — *Evaluating & Safeguarding GenAI Outputs*. Nine-dimension list: PDF page 3 / slide 6. Risk-based evaluation: PDF page 12 / slide 15.
2. `GenAI_Testing_Week11.pptx (1).pdf` — *AI Agents & the Model Context Protocol*. Permission boundaries: PDF page 11 / slide 12; unsafe agent actions and human approval: PDF pages 12–13.
3. `GenAI_Testing_Week12.pptx.pdf` — *Reusable Skills, LLM-Powered Test Infrastructure & LLMOps*. Specification: PDF page 5 / slide 6; candidate skills: PDF page 6 / slide 7; worked auditor: PDF page 8 / slide 9.
4. `generative_ai_software_testing_assignment_working_brief.pdf` — student-prepared working guide. **Not** an official instructor-issued assignment.
5. `Pasted text.txt` — user's project master prompt; stage flow, project quality requirements, no invented facts and original work expectations.

These source files were provided in the conversation and are referenced, but **not copied into the project ZIP**. The implementation code and skill documents in this repository are newly written.

## Verified by course materials
- Exactly seven *candidate skill titles* appear in Week 12.
- Seven components are displayed on Week 12's "Six-Part Skill Specification" slide, despite its inconsistent title: Input, Processing logic, Instructions, Tools, Output, Validation, Failure handling.
- The exact nine evaluation dimension names and risk-tier depth appear in Week 10.
- Evidence, validation, human review, permission limits and versioning are important course themes.

## Pending instructor verification
- Whether all seven candidate skills are *mandatory*, or whether a subset is permitted.
- Whether actual Python scripts are required, and how many.
- Whether there is an official assignment rubric, grading weights, report template or live demo requirement.
- Whether the final submission should be a GitHub URL, archive, report PDF, video or other format; deadline and repository naming.
- Whether additional Week 5–9 specific rules override the suggested implementation choices here; those lecture PDFs were not provided.

## Proposed implementation choices, not official grading rules
- Integer range probe JSON format and chosen probe distance.
- Three declared test categories (`positive`, `negative`, `boundary`) for the deterministic CSV coverage helper; the conceptual skill's broader audit still checks other applicable scenarios.
- The workload equation/JSON fields and estimation warnings.
- The evaluation record statuses (`pass`, `concern`, `not_checked`) and `structural_status` field.
- Illustrative prompt templates, fictional scenario examples and sample directory structure.

## Integrity and evaluation boundaries
- Generated example JSON outputs are real script executions against **fictional sample inputs**.
- Markdown examples for LLM-only skills were authored as illustrations and are **not** presented as actual LLM runs or externally validated findings.
- Unit tests verify Python helpers only. No SUT was contacted; no AI model, MCP server, code-host pipeline or vulnerability scanner was executed.
- Numeric evaluation scoring has not been invented because no numeric rubric was present.
- A passing test suite does not prove semantic test coverage, security, or correctness of user requirements.
