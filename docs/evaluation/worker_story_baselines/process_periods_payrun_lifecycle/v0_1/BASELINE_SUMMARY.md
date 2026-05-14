# Process Periods / PayRun Lifecycle Baseline Summary

Slice name: Process Periods / PayRun Lifecycle Baseline Recapture Result Update v0.1

Domain: Process Periods / PayRun Lifecycle

Source runbook: `docs/PROCESS_PERIOD_PAYRUN_LIFECYCLE_EVALUATION_RUNBOOK.md`

Source decision ledger: `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`

Baseline policy: `docs/evaluation/worker_story_baselines/BASELINE_CAPTURE_POLICY.md`

This pack records manually captured PowerShell evaluation output for Process Periods / PayRun Lifecycle. It is diagnostic-only and not operational truth. Captured evidence exists, but promotion is withheld because the benchmark failed 6 of 13 cases and the answer gap report status is `NEEDS_REFINEMENT`.

## Execution Context

Recaptured on 2026-05-14 from `C:\Projects\ezeas-intelligence`.

DB readiness was confirmed in normal PowerShell before capture.

- Readiness status: `READY`
- Ready: yes.
- Configuration source: `.env:MINERVA_DATABASE_URL`
- Selected ODBC driver: `ODBC Driver 17 for SQL Server`
- Required tables checked: `KnowledgeDocument`, `KnowledgeChunk`
- Missing tables: none.
- Read-only guardrails remained in place.

Codex did not rerun DB-backed commands for this update. The manually captured PowerShell outputs are the source truth for this baseline result.

## Commands

| Area | Command | Completed In v0.1 | Captured Result Summary |
|---|---|---:|---|
| DB readiness check | `scripts\check_worker_story_baseline_db_readiness.py` | yes | `READY`; ready: yes. |
| Process Periods / PayRun Lifecycle benchmark | `python scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.process_period_payrun_lifecycle.json` | yes | 13 total, 7 passed, 6 failed; audit/chat rows created: false. |
| Corpus coverage diagnostic | `python scripts\scan_process_period_payrun_lifecycle_corpus_coverage.py` | yes | 13 groups; 10 STRONG, 3 WEAK, 0 MISSING. |
| Corpus coverage diagnostic JSON | `python scripts\scan_process_period_payrun_lifecycle_corpus_coverage.py --json --output .\artifacts\eval\process_period_payrun_lifecycle_corpus_coverage.json` | yes | Generated transient JSON; committed: no. |
| Answer gap report | `python scripts\build_process_period_payrun_lifecycle_answer_gap_report.py --coverage-report .\artifacts\eval\process_period_payrun_lifecycle_corpus_coverage.json` | yes | `NEEDS_REFINEMENT`; 10 LOW/KEEP groups and 3 MEDIUM refinement groups. |
| Answer gap report JSON | `python scripts\build_process_period_payrun_lifecycle_answer_gap_report.py --coverage-report .\artifacts\eval\process_period_payrun_lifecycle_corpus_coverage.json --json --output .\artifacts\eval\process_period_payrun_lifecycle_answer_gap_report.json` | yes | Generated transient JSON; committed: no. |

## Recaptured Result

- Result status: `RECAPTURED_REQUIRES_REFINEMENT`
- Baseline promotion: withheld.
- Benchmark result: 13 total, 7 passed, 6 failed.
- Corpus coverage result: 13 groups; `STRONG`: 10, `WEAK`: 3, `MISSING`: 0.
- Answer gap report: `NEEDS_REFINEMENT`.
- Generated artefact committed: no.
- Live LLM calls: no.
- Corpus mutation: no.
- Operational JSON ingestion: no.
- Code Evidence answer integration: no.
- Final ledger status remains `BASELINE_REQUIRED`.
- This recaptured result does not count as `BASELINE_ALREADY_EXISTS`.

The failures are answer-synthesis and retrieval-term issues, not corpus absence issues, because coverage is 10 STRONG, 3 WEAK and 0 MISSING.

## Failed Benchmark Cases

1. `process-period-payrun-lifecycle-rich-answer`
   - Question: How should Process Periods and PayRun Lifecycle work in Ezeas?
   - Missing expected terms include `Process Periods / PayRun Lifecycle`, `ProcessPeriod`, `ProcessPeriodGroup`, governed payroll-period context, payment-event lifecycle evidence, `PaymentDate`, PayRun creation, PayRun admission, `RunType`, `RunPurpose`, `PayRunContact`, current-effective payroll output, finalisation readiness, payment execution, period close, Worker Story, PayRun Admin Queue and Movement Review.
2. `process-period-closed-dominates-open`
   - Missing expected terms include `closed`, `dominates open`, `closed dominates open`, `ProcessPeriod`, period lifecycle and closed-period truth.
3. `process-period-close-rolls-forward`
   - Missing expected terms include `close rolls forward`, roll forward, period close, open next period, create next period and implemented.
4. `process-period-paymentdate`
   - Missing expected terms include `PaymentDate`, payment date, tax/PAYG, payment context, calendar policy, governed, derived and not hardcoded.
5. `process-period-payrun-creation-admission`
   - Missing expected terms include PayRun creation, PayRun admission, `ProcessPeriod`, process-period context, worker inclusion, payment event and admission is not processing.
   - No source snippet or matched phrase contained expected terms PayRun creation, PayRun admission or admission is not processing.
6. `process-period-admission-not-processing`
   - Missing expected terms include admission, processing, admission is not processing, worker inclusion, `PayRunContact` and processing state.

## Domain Boundary To Preserve

Process Periods / PayRun Lifecycle provides operational payroll context for pay period membership, payment date context, payroll frequency, PayRun state, worker inclusion, recalculation readiness, finalisation boundaries, payroll evidence snapshots, worker story context, reconciliation context, movement/change comparison context, tax/payment-date context where supported and batch/group period policy context where supported.

It is not merely a date range or run list domain. It is also not runtime ProcessPeriod, PayRun, payment execution or finalisation truth.

The next refinement slice must preserve these boundaries:

- `PaymentDate` belongs on `ProcessPeriod`.
- Default payment-date derivation policy belongs on `ProcessPeriodGroup` or an equivalent governed policy, not hardcoded logic.
- Payroll calendar and payroll-year definitions must be governed and configurable, not hardcoded.
- Pay frequency support must ultimately include `DAILY`, `WEEKLY`, `FORTNIGHTLY`, `MONTHLY` and `QUARTERLY` where relevant.
- Unsupported frequencies or incomplete provider coverage must be surfaced honestly.
- Dirty contact doctrine means payroll-impacting source or configuration changes make the current `PayRunContact` unsafe until reprocessed.
- Default dirty-contact response is full contact-level PayRun reprocessing unless selective recalculation is explicitly supported, tested and explainable.
- Finalised or protected PayRuns require correction or review pathways rather than ordinary mutation.
- Minerva baseline packs are diagnostic comparison controls, not operational payroll truth.

## Not Implemented

This pack does not implement or claim:

- no DB writes;
- no migrations;
- no corpus mutation;
- no operational JSON ingestion;
- no Code Evidence answer integration;
- no live LLM calls;
- no endpoint/UI/workforce-platform/runtime changes;
- no PayRun runtime changes;
- no ProcessPeriod runtime changes;
- no dirty runtime calls;
- no correction/review/payment/finalisation execution.

## Guardrails

This recaptured baseline result:

- does not mutate corpus;
- does not change routing;
- does not change answer generation;
- does not call live LLM;
- does not ingest operational JSON;
- does not connect Code Evidence;
- does not connect Code Evidence to answer generation;
- does not prove runtime ProcessPeriod or PayRun lifecycle truth;
- does not create payroll/runtime truth;
- does not create DB schema or migrations;
- does not add endpoints or UI;
- does not change workforce-platform;
- does not create v0.5 slices automatically.

## Recommended Next Slice

Refine Process Periods / PayRun Lifecycle retrieval terms for weak supporting groups before adding new corpus, and tighten answer synthesis for weak core groups while keeping status caveats. Promotion remains withheld until benchmark and answer-gap results satisfy the baseline promotion criteria.
