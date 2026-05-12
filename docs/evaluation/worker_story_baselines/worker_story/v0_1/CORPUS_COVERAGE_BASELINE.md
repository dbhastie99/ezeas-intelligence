# Worker Story Corpus Coverage Baseline

This file records the Worker Story corpus coverage baseline execution result for comparison control. It is diagnostic-only and not operational truth.

## Commands Executed

Human-readable mode:

```powershell
.\.venv\Scripts\python.exe scripts/scan_worker_story_corpus_coverage.py
```

JSON mode with output file:

```powershell
.\.venv\Scripts\python.exe scripts/scan_worker_story_corpus_coverage.py --json --output reports/worker_story_corpus_coverage.json
```

Captured on 2026-05-12 from `C:\Projects\ezeas-intelligence`.

## Evidence Group Coverage Summary

Domain: Worker Story / Worker Calculation Story

Indexed corpus: 5 active documents, 4583 chunks.

| Evidence Group | Captured Coverage Status |
|---|---|
| `worker_story_purpose` | STRONG |
| `source_truth_and_inclusion` | STRONG |
| `interpreted_worked_hours` | STRONG |
| `calculated_payroll_outcome` | STRONG |
| `decision_story_and_rate_story` | STRONG |
| `leave_and_accrual_outcome` | STRONG |
| `payroll_bases_and_totals` | STRONG |
| `movement_review_and_admin_queue` | STRONG |
| `current_effective_truth` | STRONG |
| `outstanding_hardening` | STRONG |

## Coverage Counts

Result status: `COMPLETED`

- `STRONG`: 10
- `WEAK`: 0
- `MISSING`: 0

Evidence groups with weak or missing coverage: none.

Generated artefact committed: no. `reports/worker_story_corpus_coverage.json` was generated locally and summarized in this curated markdown baseline.

Live LLM calls: no.

Corpus mutation: no.

## Status Interpretation

- `STRONG`: multiple relevant chunks or documents were found and the group is likely well supported by indexed formal evidence.
- `WEAK`: some relevant formal evidence was found, but coverage is thin or narrow.
- `MISSING`: no useful formal-corpus support was found for the group.

Coverage status is about available indexed formal corpus evidence. It is not operational truth and does not prove whether the platform runtime implements the behavior.

## Diagnostic Interpretation

The corpus support signal is strong for the current Worker Story evidence groups. The remaining failed benchmark should be treated as synthesis/routing/answer-mode drift unless later evidence contradicts this baseline; it should not be treated as a formal corpus gap.

## Diagnostic-Only Guardrails

This corpus coverage baseline:

- does not mutate corpus;
- does not change routing;
- does not change answer generation;
- does not call live LLM;
- does not ingest operational JSON;
- does not connect Code Evidence;
- does not connect Code Evidence to answer generation;
- does not prove runtime platform truth;
- does not prove payroll/runtime truth.
