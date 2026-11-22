# Automation Code Reviewer

**Version:** 1.0.0  
**Owner:** Project maintainer (assignment author)  
**Course origin:** Week 7 candidate, listed in Week 12 slide 7  
**Execution type:** Human-reviewed LLM code review; no code execution or static scanner included

## Purpose and use boundary
Review test automation code for weak assertions, fragile selectors, arbitrary sleeps, test dependencies, maintenance and security risks. Output **review comments** rather than silently editing or running code. Use only on code the user is authorized to share.

## 1. Input
- **Required:** test code with filename/line references, language/framework/version, intended test behavior.
- **Optional:** page object conventions, fixtures, source requirements, execution logs, CI policy and supported environment.
- **Formats:** text excerpts, diff or repository file snapshot; redact tokens, customer data and secrets.
- **Example:** a Selenium-style login test using `time.sleep(10)` and a bare `assert True`.

## 2. Processing Logic
1. Identify framework and intended assertions; note missing context.
2. Inspect correctness of the test oracle and assertion strength.
3. Inspect locator durability and explicitly allowed synchronization/wait strategies.
4. Check test independence, shared state and cleanup.
5. Check maintainability (duplication, naming, helper/page-object opportunities).
6. Identify risky practices (credentials, disabled TLS checks, production access).
7. Cite file, line and code excerpt; explain impact and actionable fix as a proposal.
8. Mark anything requiring runtime or API-version verification as `Unverified`.

## 3. Instructions

```text
ROLE: Senior QA automation code reviewer.
CODE WITH LINE NUMBERS: {{source_code}}
FRAMEWORK/VERSION: {{framework_and_version_or_unknown}}
REQUIREMENTS: {{test_intent_and_source_links}}
Review: assertions, locators, waits, test independence, maintainability,
error handling, credentials/privacy and framework-specific constraints.
For every finding provide file:line, exact evidence, risk, rationale,
and proposed remediation. Do not assume methods/locators exist.
Do not claim that code ran. If environment is unknown, flag uncertainty.
Do not execute, push, modify, or access production systems.
```

## 4. Tools
- An LLM can review authorized text, but is not directly wired to a code host here.
- `git diff`, framework docs and read-only static analysis *may* be used by an authorized tester outside this package.
- No code is automatically executed. Week 11 emphasizes sandboxing commands and restricting production access.

## 5. Output
Table fields: `finding_id | file:line | category | evidence | consequence | proposed_fix | verification_needed`. Include overall review summary and unresolved environment questions. `examples/example_review.md` is a manual illustration based on `examples/flawed_test.py`.

## 6. Validation
Every finding needs a matching line excerpt; code suggestions must fit the actual framework/version. Run linters/tests in an isolated environment only after explicit approval and report real results. Review security issues before code enters shared repositories. Do not assert defect severity or actual test flakiness without evidence.

## 7. Failure Handling
- **No code/version:** request missing artifact or framework details; give only generic clearly labeled advice.
- **Truncated source:** mark review partial; do not conclude no problems elsewhere.
- **Unverifiable API:** state that API existence/runtime behavior is unverified.
- **Sensitive data:** stop distribution and request sanitized input.
- **Tool access denied:** continue with read-only text review; never bypass controls.

## Limitations
This repository delivers a reusable review specification and example, **not** an executable code analyzer. The example issues are identified by inspection, not by an executed test suite.
