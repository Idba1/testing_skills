# Workload Model Builder

**Version:** 1.0.0  
**Owner:** Project maintainer (assignment author)  
**Course origin:** Week 9 candidate, listed in Week 12 slide 7  
**Execution type:** Parameterized design prompt + implemented deterministic workload calculator

## Purpose and use boundary
Turn explicit traffic assumptions into a transparent, approximate performance-test workload. Useful before writing load-tool scripts. Not a load test, capacity measurement, SLA forecast or measured performance result.

## 1. Input
- **Required:** `scenario` (non-empty text), `population_users` (positive whole number), `peak_session_arrivals_per_minute`, `mean_session_duration_seconds`, `mean_requests_per_session`, `peak_window_minutes` (all positive finite numbers), `mean_think_time_seconds` (finite non-negative number).
- **Optional for design review:** peak shape, pacing strategy, transaction weights, geographic mix, target latency/SLAs, system constraints.
- **Format:** JSON for calculator; optional numbered background statements for AI review.
- **Example:** see `examples/workload.json` (synthetic assumptions, not measured traffic).

## 2. Processing Logic
1. Confirm units and source of all assumptions; explicitly label estimates versus observed values.
2. Compute arrival rate per second from peak starts per minute.
3. Estimate steady-state **mean concurrent sessions** with Little's Law: `L = λW` where λ = session arrivals per second and W = mean session duration in seconds.
4. Approximate requests/minute as session starts/minute × average requests/session.
5. Compute peak-window session **starts** without interpreting them as unique users.
6. Report think time separately; it is assumed to be *already included* in total mean session duration.
7. Flag when estimated concurrency exceeds stated user population; recommend checking assumptions rather than silently capping.
8. Define a proposed load profile and measurements only when source context allows; treat ramp-up, burst and SLAs as unprovided until confirmed.

## 3. Instructions

```text
ROLE: Performance test planner.
TRAFFIC ASSUMPTIONS WITH UNITS: {{provided_assumptions}}
ASSUMPTION SOURCES: {{measured_or_estimated}}
Describe traffic shape, session mix, arrival rate, think time, mean session
length and peak usage. Compute only quantities supported by supplied values.
Write all equations, units and assumptions; distinguish steady-state mean
concurrency from peak maximum concurrency. Never invent response times,
measured capacity, SLAs or failure thresholds. Request missing inputs.
Output a workload table, calculations, suggested load phases (marked
proposed), risk notes and verification questions.
```

## 4. Tools
`python workload-model-builder/scripts/workload_model.py --input workload-model-builder/examples/workload.json --output workload-model-builder/examples/workload_report.json`

The helper is standard-library-only, produces JSON, and deliberately does **not** contact a target service. Performance tools (JMeter/k6/etc.) are not installed or run by the repository.

## 5. Output
JSON with `assumptions`, `derived`, `formula`, `warnings`, and `limitations`. Include a separate proposed workload profile only after a tester agrees the shape and targets. Actual example calculation is in `examples/workload_report.json`.

## 6. Validation
Verify physical units, positive finite inputs and mean concurrency arithmetic. Compare assumptions to real telemetry before treating estimates as representative. Human approval is needed for load intensity or SLA values. Tests cover nominal calculation, invalid inputs, think-time inconsistency and population mismatch.

## 7. Failure Handling
- **Unknown rate/duration:** request the missing parameter, no fabricated fallback.
- **Zero/negative/NaN/infinite values, noninteger population, invalid JSON:** stop with descriptive error.
- **Think time larger than total session time:** stop for clarification.
- **Population mismatch:** emit a warning; do not silently modify assumptions.
- **Tool unavailable:** provide formula only; do not claim calculations were executed.

## Limitations
Little's Law estimate assumes a sufficiently stable observation interval and mean quantities; it does not capture bursts, percentiles, network bottlenecks, transaction weighting or actual server performance. Synthetic results are planning illustrations, not empirical results.
