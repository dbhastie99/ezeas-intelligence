# ObjectTime / Source Truth Baseline Summary

Slice name: ObjectTime / Source Truth Baseline Capture v0.1

Domain: ObjectTime / Source Truth

Source runbook: `docs/OBJECTTIME_SOURCE_TRUTH_EVALUATION_RUNBOOK.md`

Source decision ledger: `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`

Baseline policy: `docs/evaluation/worker_story_baselines/BASELINE_CAPTURE_POLICY.md`

This blocked baseline pack is diagnostic-only and not operational truth. It records DB-readiness non-execution for ObjectTime / Source Truth and does not capture benchmark, corpus coverage or answer gap results.

## Execution Context

Attempted on 2026-05-14 from `C:\Projects\ezeas-intelligence`.

DB readiness returned `DATABASE_CONNECTION_FAILED`.

- Readiness command: `.\.venv\Scripts\python.exe scripts\check_worker_story_baseline_db_readiness.py`
- Ready: no.
- Required tables checked: `KnowledgeDocument`, `KnowledgeChunk`
- Missing tables: none.
- Configuration source reported: `.env:MINERVA_DATABASE_URL`
- Dialect/driver reported: `mssql/pyodbc`
- Selected ODBC driver reported: `ODBC Driver 18 for SQL Server`
- Error class: `pyodbc.OperationalError`
- Result status: `BLOCKED_DATABASE_CONNECTION`

Because readiness was not `READY`, ObjectTime / Source Truth benchmark, corpus coverage and answer gap commands were not run. No generated JSON reports were produced for this ObjectTime / Source Truth attempt.

## Commands

| Area | Command | Completed In v0.1 | Captured Result Summary |
|---|---|---:|---|
| DB readiness check | `.\.venv\Scripts\python.exe scripts\check_worker_story_baseline_db_readiness.py` | yes | `DATABASE_CONNECTION_FAILED`; ready: no. |
| ObjectTime / Source Truth benchmark | `.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.objecttime_source_truth.json` | no | Blocked by DB readiness. |
| Corpus coverage diagnostic | `.\.venv\Scripts\python.exe scripts\scan_objecttime_source_truth_corpus_coverage.py` | no | Blocked by DB readiness. |
| Corpus coverage diagnostic JSON | `.\.venv\Scripts\python.exe scripts\scan_objecttime_source_truth_corpus_coverage.py --json --output .\artifacts\eval\objecttime_source_truth_corpus_coverage.json` | no | Blocked by DB readiness; generated artefact committed: no. |
| Answer gap report | `.\.venv\Scripts\python.exe scripts\build_objecttime_source_truth_answer_gap_report.py --coverage-report .\artifacts\eval\objecttime_source_truth_corpus_coverage.json` | no | Blocked by DB readiness. |
| Answer gap report JSON | `.\.venv\Scripts\python.exe scripts\build_objecttime_source_truth_answer_gap_report.py --coverage-report .\artifacts\eval\objecttime_source_truth_corpus_coverage.json --json --output .\artifacts\eval\objecttime_source_truth_answer_gap_report.json` | no | Blocked by DB readiness; generated artefact committed: no. |

## Blocked Finding

- Readiness status: `DATABASE_CONNECTION_FAILED`.
- Result status: `BLOCKED_DATABASE_CONNECTION`.
- Baseline pack created: blocked pack only.
- Benchmark result: not run.
- Corpus coverage result: not run.
- Answer gap report: not run.
- Generated artefact committed: no.
- Live LLM calls: no.
- Corpus mutation: no.
- Operational JSON ingestion: no.
- Code Evidence answer integration: no.
- Final ledger status remains `BASELINE_REQUIRED`.
- This blocked pack does not count as `BASELINE_ALREADY_EXISTS`.

## Domain Boundary To Preserve

ObjectTime / Source Truth is source evidence and PayRun inclusion context. It is not merely a timesheet or shift domain, and it is not payroll calculation truth by itself.

The next captured run must preserve these boundaries:

- ObjectTime, ObjectTimeAttribute, ObjectTimeAssessment and ObjectTimeAssessmentResponse are ObjectTime-family source evidence surfaces.
- SourceTruth is not WorkedHours.
- Raw span hours are not user-facing payroll worked hours.
- Worked hours must come from interpreted payroll truth or governed payroll bucket results where supported.
- ObjectTime source changes can affect payroll causality, dirty state, finalised correction review and evidence preservation.
- Minerva baseline packs are diagnostic comparison controls, not operational payroll truth.

## Source-Change Status To Preserve

Current known source-change status is recorded here as a review guardrail only. It is not benchmark output.

ObjectTime-family guarded dry-run route wiring is complete for:

- `OBJECT_TIME`
- `OBJECT_TIME_ATTRIBUTE`
- `OBJECT_TIME_ASSESSMENT`
- `OBJECT_TIME_ASSESSMENT_RESPONSE`

Known workforce-platform source-change milestones to preserve:

- v5.41 dry-run adapter exists.
- v5.42 dry-run orchestrator exists.
- v5.43 rollout inventory exists.
- v5.44 ObjectTime dry-run probe exists.
- v5.45 ObjectTime route-adjacent contract probe exists.
- v5.46 ObjectTime request builder exists.
- v5.47 test-only route harness exists.
- v5.48 integration plan/readiness gate exists.
- v5.49 OBJECT_TIME guarded dry-run route wiring exists.
- v5.51 OBJECT_TIME edge hardening exists.
- v5.52 OBJECT_TIME_ATTRIBUTE guarded dry-run route wiring exists.
- v5.53 OBJECT_TIME_ASSESSMENT guarded dry-run route wiring exists.
- v5.54 OBJECT_TIME_ASSESSMENT_RESPONSE guarded dry-run route wiring exists.
- v5.55 ObjectTime-family guarded dry-run close-out exists.
- v5.56 source-change runtime intake readiness contract exists.

Do not overclaim v5.56. It is a readiness contract only. It is not runtime intake.

## Not Implemented

This pack does not implement or claim:

- runtime source-change hook or intake;
- dirty runtime from source-change hooks;
- Finalised correction intake creation from hooks;
- review request creation from hooks;
- correction execution;
- retro or replay execution;
- supplementary execution;
- adjustment execution;
- payment or remittance execution;
- finalisation mutation;
- production enablement.

## Guardrails

This blocked pack:

- does not mutate corpus;
- does not change routing;
- does not change answer generation;
- does not call live LLM;
- does not ingest operational JSON;
- does not connect Code Evidence;
- does not connect Code Evidence to answer generation;
- does not prove runtime platform truth;
- does not create payroll/runtime truth;
- does not create DB schema or migrations;
- does not add endpoints or UI;
- does not change workforce-platform;
- does not create v0.5 slices automatically.

## Recommended Next Slice

Fix SQL Server connectivity or credentials so the readiness check returns `READY` before running commands. Then rerun the ObjectTime / Source Truth benchmark, corpus coverage diagnostic and answer gap report before moving this domain to `BASELINE_ALREADY_EXISTS`.
