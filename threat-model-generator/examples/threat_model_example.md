# Illustrative candidate threat register — NOT a confirmed vulnerability scan

Source: `system_description.md`, a fictional architecture. STRIDE labels are used as categories, **not** as a risk scoring system.

| ID | Flow / asset | STRIDE category | Preconditions | Candidate threat | Potential impact | Known control status | Proposed mitigation / test idea | Uncertainty |
|---|---|---|---|---|---|---|---|---|
| TM-01 | Internet client → API; appointment ownership | Elevation of privilege | User can submit a request referring to an appointment not owned by them | Cross-account data access if object-level authorization is absent | Exposure of another user's appointments | **Unknown** | Verify server-side ownership enforcement using authorized test accounts in isolated test environment | No API routes or current checks provided |
| TM-02 | Internet client → API; booking availability | Denial of service | Excessive unauthenticated/automated requests possible | Resource exhaustion if traffic controls are insufficient | Reduced service availability | **Unknown** | Discuss sensible traffic budgets and validate rate controls in approved staging | No observed traffic or rate-limit values |
| TM-03 | API → database; appointment integrity | Tampering | An attacker gains unauthorized write capability | Appointment data modified without authorization | Wrong booking data or account attribution | **Unknown** | Review least privilege and application authorization; write non-destructive tests | No permissions evidence or exploit confirmation |

## Stakeholder review needed
Confirm actual authorization rules, access controls and approved test environments. No penetration test or scanner was executed. All entries are hypothetical risk scenarios.
