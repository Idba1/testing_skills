# Illustrative output — hand-authored, NOT an executed AI run

Input: `examples/requirements.md`

| Finding ID | Requirement | Verbatim excerpt | Category (proposed) | Testing impact | Clarification question | Proposal / uncertainty |
|---|---|---|---|---|---|---|
| AMB-01 | AUTH-01 | "quickly" | Vague qualifier | Timing assertion cannot be written | What maximum response time applies after the lockout condition is met? | **Unverified:** ask for measurable limit |
| AMB-02 | AUTH-01 | "many failed logins" | Missing measurable rule | Attempt-count boundary undefined in this requirement | Is the intended count five as in AUTH-02? Are attempts counted per account or per device? | Proposed link to AUTH-02; **not approved** |
| AMB-03 | AUTH-03 | "always unlock accounts immediately" | Scope / potential conflict | Cannot define exceptions to lockout | Can admin unlock accounts subject to fraud holds or other restrictions? | **No exceptions invented** |

## Unresolved stakeholder decisions
Confirm the timing limit, counting scope and the meaning of "always." No rule is finalized in this illustration.

## Validation notes
All snippets appear verbatim in the example source. No timing, count policy or administrative exception has been invented beyond the quoted source; AUTH-02's five attempts is referenced as a question, not propagated as an approved interpretation of AUTH-01.
