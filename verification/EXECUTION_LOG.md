# Actual Execution Evidence

## Regression verification on Windows

On 2026-11-22, Python 3.13.2 on Windows ran `python -B verification/run_tests.py`. The original suite passed all 24 tests. With the eight new tests and before the fixes, the runner reported nine failing assertions and four errors, including subtests. A first rerun after the fixes had two failing workload subtests because their fixtures overflowed concurrency before reaching the intended metric. After isolating each calculation in its fixture, the final run passed all 32 tests.

The in-memory syntax check compiled 10 Python files successfully.

```powershell
python -B -c "import pathlib; files = sorted(pathlib.Path('.').glob('**/*.py')); [compile(p.read_bytes(), str(p), 'exec') for p in files]; print(f'Compiled {len(files)} Python files')"
```

The sample verification invoked the following commands from repository root via Python subprocesses. Here `<temp>` represents the temporary directory created for the run.

```text
python -B test-case-generator/scripts/boundary_helper.py --input test-case-generator/examples/boundaries.json --output <temp>/generated_boundary_cases.json
python -B coverage-gap-auditor/scripts/coverage_audit.py --requirements coverage-gap-auditor/examples/requirements.csv --tests coverage-gap-auditor/examples/tests.csv --output <temp>/coverage_report.json
python -B workload-model-builder/scripts/workload_model.py --input workload-model-builder/examples/workload.json --output <temp>/workload_report.json
python -B nine-dimension-output-evaluator/scripts/evaluation_validator.py --input nine-dimension-output-evaluator/examples/evaluation_input.json --output <temp>/evaluation_report.json
```

All four exited 0 and each parsed report equaled its checked-in sample. The same commands were repeated with the substitutions below and `bad-` prefixed to each output filename. All four exited 2, printed the expected input error to stderr, and created no report.

| Replaced argument | Invalid input | Observed diagnostic |
|---|---|---|
| Boundary `--input <temp>/boundaries.json` | Requirement R1 with bounds 1 and 2, both exclusive | `R1: no integer can satisfy the declared interval` |
| Coverage `--tests <temp>/tests.csv` | Missing final field on line 2 | `CSV line 2 has the wrong number of fields` |
| Workload `--input <temp>/workload.json` | Arrivals per minute and mean duration both `1e308` | `mean_concurrent_sessions exceeds the supported numeric range` |
| Evaluation `--input <temp>/evaluation_input.json` | Risk level set to `[]` | `risk_level must be low, medium, high, or critical` |

## Original baseline verification on Linux

**Execution date:** 2026-11-22 (conversation date)  
**Environment in execution sandbox:** Python 3.13.5, Linux 6.18.57  
**Dependencies:** Python standard library; no external service or system-under-test.

## Tests actually run

From repository root:

```bash
python verification/run_tests.py
```

**Observed:** `Ran 24 tests` and `OK` (24 passed, 0 failures, 0 errors). The full captured console output is in `verification/unit_tests_capture.txt`. Test modules exercise input validation, missing/duplicate identifiers, boundary inclusivity, unlinked/orphan tests, workload calculation and evaluation risk-tier record checks.

Python syntax compilation was also run successfully:

```bash
python -m compileall -q test-case-generator/scripts coverage-gap-auditor/scripts workload-model-builder/scripts nine-dimension-output-evaluator/scripts verification/run_tests.py
```

## Script demonstrations actually run

Run each from repository root (the JSON files already contain the actual saved results):

```bash
python test-case-generator/scripts/boundary_helper.py --input test-case-generator/examples/boundaries.json --output test-case-generator/examples/generated_boundary_cases.json
python coverage-gap-auditor/scripts/coverage_audit.py --requirements coverage-gap-auditor/examples/requirements.csv --tests coverage-gap-auditor/examples/tests.csv --output coverage-gap-auditor/examples/coverage_report.json
python workload-model-builder/scripts/workload_model.py --input workload-model-builder/examples/workload.json --output workload-model-builder/examples/workload_report.json
python nine-dimension-output-evaluator/scripts/evaluation_validator.py --input nine-dimension-output-evaluator/examples/evaluation_input.json --output nine-dimension-output-evaluator/examples/evaluation_report.json
```

| Script | Observed result | Meaning |
|---|---|---|
| Boundary helper | 2 integer requirements, example REG-01 values 17/18/19/64/65/66 | Numeric range probes only; no real form executed |
| Coverage auditor | 1 covered / 1 partial / 1 uncovered; 1 orphan + 1 unlinked test | Declared test-kind presence only; not semantic test adequacy |
| Workload builder | 360.0 mean concurrent sessions, 720 estimated requests/minute | Steady-state estimate from synthetic user assumptions, not a measured benchmark |
| Evaluation record validator | `incomplete`, concerns Bias, Completeness, Traceability; incomplete checks Correctness, Hallucination, Security | Expected: a review record deliberately has unverified evidence |

## Negative command-line cases actually run

Four deliberately invalid inputs were supplied separately to the four command-line scripts. **All four returned exit code 2** and a descriptive input error. Captured details: `verification/negative_cli_capture.txt`. These failures were expected and demonstrate validation; they are not examples of a successful analysis of invalid data.

## Not tested / no claim made

- No external LLM or agent was invoked, so there are no real LLM-generated demonstration outputs.
- The three instruction-only skills have hand-authored illustrations only.
- No UI, API, Selenium suite, security scanner or live performance test was executed.
- No GitHub Actions workflow or hosted CI pipeline was executed.
- No instructor rubric compliance or submission portal acceptance was verified.
- Script unit tests do not validate actual source requirement quality or human evaluator independence.

## Reproducibility / review protocol

Re-run the commands and inspect output files; verify the sample inputs remain unchanged. For real-model trials, preserve model ID/version, prompt version, input hash, date, produced artifact, review record, observed failures, and corrections in an added evidence file. Have an authorized human review any external action or production-affecting decision.
