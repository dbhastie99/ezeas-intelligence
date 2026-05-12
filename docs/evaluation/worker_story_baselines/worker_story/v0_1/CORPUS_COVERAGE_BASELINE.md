# Worker Story Corpus Coverage Baseline

This file records the Worker Story corpus coverage baseline shape for comparison control. It is diagnostic-only and not operational truth.

## Command

Human-readable mode:

```powershell
py scripts/scan_worker_story_corpus_coverage.py
```

JSON mode with output file:

```powershell
py scripts/scan_worker_story_corpus_coverage.py --json --output reports/worker_story_corpus_coverage.json
```

## Evidence Group Coverage Summary

The Worker Story coverage diagnostic is expected to report these evidence groups:

| Evidence Group | Baseline Capture State |
|---|---|
| `worker_story_purpose` | shape recorded; generated coverage not captured in v0.1 |
| `source_truth_and_inclusion` | shape recorded; generated coverage not captured in v0.1 |
| `interpreted_worked_hours` | shape recorded; generated coverage not captured in v0.1 |
| `calculated_payroll_outcome` | shape recorded; generated coverage not captured in v0.1 |
| `decision_story_and_rate_story` | shape recorded; generated coverage not captured in v0.1 |
| `leave_and_accrual_outcome` | shape recorded; generated coverage not captured in v0.1 |
| `payroll_bases_and_totals` | shape recorded; generated coverage not captured in v0.1 |
| `movement_review_and_admin_queue` | shape recorded; generated coverage not captured in v0.1 |
| `current_effective_truth` | shape recorded; generated coverage not captured in v0.1 |
| `outstanding_hardening` | shape recorded; generated coverage not captured in v0.1 |

## Status Interpretation

- `STRONG`: multiple relevant chunks or documents were found and the group is likely well supported by indexed formal evidence.
- `WEAK`: some relevant formal evidence was found, but coverage is thin or narrow.
- `MISSING`: no useful formal-corpus support was found for the group.

Coverage status is about available indexed formal corpus evidence. It is not operational truth and does not prove whether the platform runtime implements the behavior.

## Current Baseline Finding

The coverage diagnostic was not executed as a baseline-capture command in this v0.1 slice. This file defines the checked-in corpus coverage baseline capture shape and must be populated by a future rerun if generated coverage output is intentionally versioned.

No `STRONG`, `WEAK` or `MISSING` result is claimed by this file.

## Diagnostic-Only Guardrails

This corpus coverage baseline:

- does not mutate corpus;
- does not change routing;
- does not change answer generation;
- does not call live LLM;
- does not ingest operational JSON;
- does not connect Code Evidence;
- does not prove runtime platform truth;
- does not prove payroll/runtime truth.
