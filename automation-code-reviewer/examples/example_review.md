# Illustrative review — hand-authored, not a tool execution

Source: `flawed_test.py` (intentionally flawed fictional example).

| Finding | Source | Category | Evidence | Why it matters | Proposed remediation | Verification needed |
|---|---|---|---|---|---|---|
| ACR-01 | lines 8–10 | Locator durability | Absolute `/html/body/...` XPath | Page layout changes may break selectors | Prefer stable semantic locator or a vetted page-object abstraction | Actual DOM and framework version needed |
| ACR-02 | line 11 | Wait strategy | `time.sleep(10)` | Arbitrary fixed wait can be slow or flaky | Wait for a relevant observable state with an appropriate framework API | Confirm the login success condition |
| ACR-03 | line 12 | Assertion quality | `assert True` | Assertion never verifies login outcome | Assert a requirement-backed indicator of authentication | Need source requirement and app behavior |
| ACR-04 | line 9 | Credential hygiene | Hardcoded example value in test | A hardcoded secret-like value is an unsafe pattern to propagate | Use dummy fixtures or a managed test secret source as policy permits | Confirm whether this is non-sensitive fixture data |

**Limitations:** These are code-inspection findings, not outcomes from running Selenium. URL `example.invalid` is deliberately nonfunctional. The example password is fictitious; no real credential or real service is involved.
