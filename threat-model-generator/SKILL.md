# Threat Model Generator

**Version:** 1.0.0  
**Owner:** Project maintainer (assignment author)  
**Course origin:** Week 9 candidate, listed in Week 12 slide 7  
**Execution type:** Human-reviewed LLM threat-model template; no scanning/tool execution

## Purpose and use boundary
Generate an **evidence-based candidate threat model** from a system architecture: assets, entry points, trust boundaries, plausible threats, mitigations and security test ideas. Intended to help security/testing discussions, not to certify security or confirm an actual vulnerability.

## 1. Input
- **Required:** architecture/scope and data flow, trust boundaries, entry points, protected assets and known deployment environment.
- **Optional:** technology versions, authentication/authorization model, threat assumptions, existing mitigations, regulatory context.
- **Format:** Markdown architecture description or diagram with named components, edges and data classes; sanitize secrets.
- If key boundaries are missing, explicitly mark the model provisional.

## 2. Processing Logic
1. Map systems, data stores, identities, assets and trust boundaries.
2. For each relevant entry point/data flow, examine STRIDE *where appropriate*: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege.
3. Identify an attack precondition and plausible mechanism supported by architecture details.
4. Separate **potential threat**, **existing control**, **proposed mitigation**, and **verification test idea**.
5. Use qualitative priority (`high/medium/low/unknown`) only if user supplies a rating rubric; otherwise note impact factors without assigning severity.
6. Prefer verification questions over asserted vulnerabilities; recommend security owners review and accept residual risk.

## 3. Instructions

```text
ROLE: Security-focused QA threat model facilitator.
ARCHITECTURE: {{system_description}}
ASSETS: {{assets}}
ENTRY POINTS: {{entry_points}}
TRUST BOUNDARIES: {{boundaries}}
KNOWN CONTROLS: {{documented_controls_or_unknown}}
Analyze potential threats, using STRIDE only where relevant.
For each candidate return: threat_id, component/flow, asset,
entry_point, trust_boundary, STRIDE_category, evidence,
preconditions, possible_impact, existing_control_status,
proposed_mitigation, security_test_idea, uncertainty.
Never report an unverified threat as a confirmed exploit.
Do not invent endpoints, ports, secrets, third-party services,
or risk scoring. Do not produce destructive exploitation steps.
```

## 4. Tools
- LLM reasoning applied to an authorized architecture description; manual data-flow diagrams.
- No active scanning, penetration testing, commands, MCP permissions or live assets in this package.
- STRIDE is a **threat categorization method**, not automatically a quantitative risk-score system.

## 5. Output
Candidate threat register table with traceable architecture element; distinct sections for mitigations, security test proposals, unknown assumptions and owner decisions. Example in `examples/threat_model_example.md` is a **hand-written illustration**, not a tested vulnerability.

## 6. Validation
Every threat references a supplied asset, entry point or trust boundary; avoid asserting unprovided infrastructure. Confirm each STRIDE label fits the risk mechanism. A knowledgeable reviewer should verify whether controls are actually present and decide prioritization based on a defined rubric. Do not count speculative entries as discovered defects.

## 7. Failure Handling
- **No diagram/system scope:** request a description of components and flows; no confident threat conclusions.
- **Missing boundary/control:** label `unknown` and raise clarification question.
- **Unsupported technology detail:** state uncertainty, do not fabricate details.
- **Sensitive secrets:** stop and request redaction.
- **No authorization for scanning:** do not initiate technical tests.

## Limitations
This is an instruction-led candidate threat model. The repository does not execute scans or establish exploitability. Exact Week 9 instructor guidance was not available with the provided uploads; additional implementation choices here are clearly proposed rather than claimed as an official rubric.
