# Verification Matrix

| Skill | Normal scenario | Missing / malformed input | Edge case | Nature of evidence |
|---|---|---|---|---|
| Requirement Ambiguity Analyser | Fictional vague login requirement | Missing requirement IDs handled by instructions | Contradictory policies require stakeholder | **Hand-authored** sample only; no live LLM evaluation |
| Test Case Generator | Integer inclusive range probes | Reject missing/Boolean bound, duplicate IDs | Exclusive limits, equal inclusive bounds, custom distance | **Automated tests + actual JSON execution** for helper; case table hand-authored |
| Coverage Gap Auditor | Covered/partial/uncovered rows | Reject unknown test kinds, empty criteria and malformed CSV | Orphan references and unlinked tests | **Automated tests + actual JSON execution** of structural auditor |
| Automation Code Reviewer | Intentional bad Selenium-style test example | Missing framework/source requires questions | Hardcoded credentials, false assertions, fixed sleep | **Hand-authored** code review, no runtime or LLM execution |
| Workload Model Builder | Synthetic workload and formula | Reject missing, zero, Boolean, infinity | Population warning and invalid think time | **Automated tests + actual JSON execution** |
| Threat Model Generator | Fictional architecture and plausible threat paths | Unknown controls recorded | No claim of tested exploitability | **Hand-authored** threat register, no active scanner |
| Nine-Dimension Output Evaluator | High-risk record completeness checks | Reject wrong labels/status; missing dimension flagged | Low sanity, medium 3, critical review record | **Automated tests + actual JSON execution** for structure only |

**Clarifications:** The unit tests verify script behavior, not model-generated answers, business rule approval or system-under-test behavior. Hand-authored examples are intentionally not represented as run results.
