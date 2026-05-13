# Annual Leave / Leave Management Evaluation Runbook

This runbook documents the current Minerva evaluation foundation for Annual Leave / Leave Management. It is intended for regression checks and readiness review after retrieval-plan, benchmark, synthesis, or formal corpus changes.

The workflow is diagnostic-only. It does not mutate corpus records, change database schema, ingest operational JSON, call a live LLM, connect Code Evidence Index to answer generation, add endpoints or UI, or change workforce-platform.

## Purpose

Annual Leave / Leave Management evaluation checks whether Minerva can retrieve and synthesize enough formal evidence to answer product-domain questions about the broader annual-leave management slice.

The evaluation covers:

- LeaveType, LeaveTypeRule, LeaveTypeKind and Rule Cockpit configuration;
- accrual basis, interpreter truth, no-fallback posture and LeaveLedger accrual minutes;
- TAKEN leave posting, public holiday treatment and DeductsOnPublicHoliday behavior;
- valuation basis, ordinary rate, PayRun snapshot and liability evidence;
- PayRun leave orchestration, admin/readiness relationships and processing caveats;
- Worker Story leave evidence, Leave and Accrual Outcome, ledger evidence and valuation basis;
- outstanding hardening, including Leave Source Model, FIFO lot consumption, revaluation and production hardening.

Annual Leave / Leave Management evaluation is not proof of runtime leave truth. It evaluates Minerva retrieval and answer quality over formal knowledge evidence. Minerva explains Annual Leave but does not calculate leave, post LeaveLedger rows, approve leave, value leave, mutate leave balances, finalise PayRuns, or decide operational readiness.

## Domain Retrieval Coverage

The Annual Leave / Leave Management retrieval plan is `ANNUAL_LEAVE_MANAGEMENT` in `app/services/domain_retrieval_plan_service.py`. It splits the broad question, "How is Annual Leave managed in the system?", into deterministic evidence groups:

- `configuration`: configuration and rule setup;
- `accrual`: accrual basis and ledger posting;
- `taken`: TAKEN leave and deduction rules;
- `valuation`: valuation and ordinary-rate evidence;
- `payrun`: PayRun leave orchestration;
- `worker_story`: Worker Story leave evidence;
- `outstanding`: outstanding hardening and future work.

The plan decides what evidence to search for. It does not calculate leave, infer missing source truth, post ledger rows, run leave processing, mutate payroll history, or treat missing corpus evidence as implemented product truth.

## Difference From Adjacent Domains

Leave Accrual / Processing is narrower and deeper than the Annual Leave overview. It evaluates detailed accrual source truth, applicability, CalcInterpreterLine/current-effective payroll output, LeaveLedger movement evidence, valuation hard-fail posture, processing sequencing and finalisation readiness. It is not a substitute for the broad Annual Leave / Leave Management overview.

Leave Source Model evaluates source truth and applicability boundaries: rule content versus applicability, contact versus appointment scope, source dimensions, precedence and no-entitlement versus missing-output distinctions. It does not replace Annual Leave overview coverage of configuration, accrual, TAKEN leave, valuation, PayRun orchestration, Worker Story evidence and outstanding hardening together.

Leave Requests / Leave Workflow evaluates request lifecycle, status transitions, approval/rejection/reopen behavior, idempotency, overlap/shortfall handling and request-driven ledger/payroll relationships. It is workflow-focused and does not substitute for Annual Leave management readiness.

Public Holidays evaluates public-holiday source/calendar evidence, worksite/state applicability, payroll treatment and leave interaction. It covers DeductsOnPublicHoliday where relevant, but it does not replace Annual Leave overview evaluation.

Adjacent domain runbooks, corpus coverage diagnostics and answer gap reports must not be counted as Annual Leave / Leave Management diagnostic or gap tooling.

## Commands

Run commands from the repository root.

### Full Pytest Suite

```powershell
.\.venv\Scripts\python.exe -m pytest --basetemp .\.pytest_tmp
```

This is the main regression gate. It should pass before treating any benchmark output as meaningful.

### Annual Leave Rich-Answer Benchmark

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.annual_leave.json
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.annual_leave.json --verbose --allow-failures
```

The rich-answer benchmark currently includes the broad Annual Leave / Leave Management question and checks answer sections, expected answer terms, expected source terms and forbidden answer patterns.

### Annual Leave Golden Questions

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\golden_questions.annual_leave.json
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\golden_questions.annual_leave.json --verbose
```

The golden-question manifest covers Annual Leave management, accrual, TAKEN posting, public holiday handling, valuation, Worker Story explanation, rule UI configuration and outstanding work.

### Annual Leave Corpus Seed Helpers

```powershell
.\.venv\Scripts\python.exe scripts\scan_leave_corpus_candidates.py --help
.\.venv\Scripts\python.exe scripts\build_leave_manifest_from_candidates.py --help
```

These helper scripts support candidate formal-document review and manifest creation for targeted Annual Leave corpus supplementation. They are not Annual Leave corpus coverage diagnostics and are not answer gap reports.

### Annual Leave Corpus Coverage Diagnostic

```powershell
.\.venv\Scripts\python.exe scripts\scan_annual_leave_corpus_coverage.py
.\.venv\Scripts\python.exe scripts\scan_annual_leave_corpus_coverage.py --json --output .\artifacts\eval\annual_leave_corpus_coverage.json
```

The Annual Leave / Leave Management corpus coverage diagnostic classifies the canonical `ANNUAL_LEAVE_MANAGEMENT` evidence groups as `STRONG`, `WEAK`, or `MISSING`. It is read-only: it does not mutate corpus records, ingest operational JSON, call a live LLM, run migrations, connect Code Evidence Index to answer generation, or change endpoints/UI/workforce-platform.

The diagnostic must remain distinct from adjacent leave-domain diagnostics. Do not use `scan_leave_accrual_processing_corpus_coverage.py`, `scan_leave_source_model_corpus_coverage.py`, `scan_leave_requests_workflow_corpus_coverage.py`, or `scan_public_holidays_corpus_coverage.py` as substitutes.

Implemented assets:

- `app/services/annual_leave_corpus_coverage_service.py`;
- `scripts/scan_annual_leave_corpus_coverage.py`;
- tests for Annual Leave corpus coverage diagnostics.

### Annual Leave Answer Gap Report

```powershell
.\.venv\Scripts\python.exe scripts\build_annual_leave_answer_gap_report.py --coverage-report .\artifacts\eval\annual_leave_corpus_coverage.json
.\.venv\Scripts\python.exe scripts\build_annual_leave_answer_gap_report.py --coverage-report .\artifacts\eval\annual_leave_corpus_coverage.json --json --output .\artifacts\eval\annual_leave_answer_gap_report.json
```

The Annual Leave / Leave Management answer gap report consumes the saved corpus coverage JSON and maps `STRONG`, `WEAK`, and `MISSING` coverage to diagnostic answer-quality actions. It is read-only: it does not mutate corpus records, ingest operational JSON, call a live LLM, run migrations, connect Code Evidence Index to answer generation, or change endpoints/UI/workforce-platform.

Implemented assets:

- `app/services/annual_leave_answer_gap_report_service.py`;
- `scripts/build_annual_leave_answer_gap_report.py`;
- tests for Annual Leave answer gap reporting.

Do not use adjacent leave-domain answer gap reports as substitutes.

## Interpreting Benchmark Results

Benchmark results are deterministic regression checks over the loaded Minerva corpus.

- `PASS` means the question met its configured retrieval and answer checks.
- `FAIL` means at least one expected source, source phrase, answer phrase, answer section, or forbidden-pattern check did not pass.

A failure does not automatically mean answer synthesis is wrong. Common causes are:

- the loaded formal corpus does not contain enough Annual Leave evidence;
- retrieval terms do not find relevant formal evidence;
- synthesis found evidence but did not express the expected Annual Leave wording;
- the benchmark expectation no longer matches the intended product-domain wording.

Benchmark failures can now be triaged with the domain-specific corpus coverage diagnostic and answer gap report before any baseline capture decision. Do not claim runtime leave truth from benchmark, corpus coverage, or answer-gap output.

## Current Readiness

Annual Leave / Leave Management has:

- a deterministic retrieval plan;
- a rich-answer benchmark manifest;
- a golden-question manifest;
- README references;
- seed-corpus checklist and candidate-manifest helper scripts;
- this v0.4 evaluation runbook foundation.
- Annual Leave-specific corpus coverage diagnostic tooling.
- Annual Leave-specific answer gap report tooling.

Annual Leave / Leave Management now has the v0.4 runbook foundation, corpus coverage diagnostic tooling, answer gap report tooling, and a checked-in v0.1 baseline pack under `docs/evaluation/worker_story_baselines/annual_leave/v0_1/`. Generated JSON reports remain transient evaluation artefacts unless explicitly versioned as part of a baseline pack.

## Guardrails

This workflow must remain:

- diagnostic-only;
- Minerva explains Annual Leave but does not calculate leave;
- no corpus mutation;
- no live LLM calls;
- no database schema change;
- no operational JSON ingestion;
- no Code Evidence answer integration;
- no Code Evidence Index answer integration;
- no endpoint or UI changes;
- no workforce-platform changes;
- not proof of runtime operational truth;
- not proof that Minerva posts LeaveLedger rows;
- not proof that Minerva approves leave;
- not proof that Minerva values leave;
- not proof that Minerva changes leave balances;
- not proof that Minerva determines or finalises readiness.

Do not weaken benchmark expectations, fabricate coverage or gap results, run Annual Leave baseline capture, or create an Annual Leave baseline pack from this diagnostic-only tooling slice.
