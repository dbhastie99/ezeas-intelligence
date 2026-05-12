# Rosters / Patterns / Scheduling Evaluation Runbook

This runbook documents the repeatable Minerva evaluation workflow for Rosters / Patterns / Scheduling. It is intended for regression checks and corpus-readiness diagnostics after retrieval-plan, benchmark, synthesis, diagnostic tooling, or formal corpus changes.

The workflow is diagnostic-only. It does not mutate corpus records, change database schema, ingest operational JSON, call a live LLM, read source-code content as Minerva evidence, or connect Code Evidence Index to answer generation. It also provides no Code Evidence answer integration and is not proof of runtime operational truth.

## Purpose

Rosters / Patterns / Scheduling is the Minerva product-domain explaining governed roster, pattern and schedule evidence; expected work context; Pattern / PatternDay / EmployeeAppointmentPattern configuration; appointment/worksite applicability; ordinary-hours and leave-basis context; ObjectTime/source-truth boundaries; Worker Story and payroll evidence relationships; and Admin Queue / Worker Attention / Finalisation Readiness relationships.

The evaluation answers four practical questions:

- Does the full test suite still pass?
- Does the Rosters / Patterns / Scheduling broad and focused rich-answer benchmark still pass?
- Do roster/pattern/scheduling-framed questions still route to the Rosters / Patterns / Scheduling domain while overlapping domains keep ownership?
- Does the currently indexed formal corpus contain enough evidence for each Rosters / Patterns / Scheduling evidence group?

Rosters / Patterns / Scheduling evaluation is not proof of runtime roster, pattern or scheduling implementation. It evaluates Minerva retrieval and answer quality over formal knowledge evidence. Minerva explains Rosters / Patterns / Scheduling. Minerva does not create rosters, change worker schedules, mutate Pattern, PatternDay or EmployeeAppointmentPattern truth, mutate ObjectTime, calculate payroll, decide entitlements, calculate leave, approve leave, determine finalisation readiness, finalise PayRuns, or mutate operational workforce/payroll/leave truth.

Explicit Minerva boundary:

- Minerva explains Rosters / Patterns / Scheduling.
- Minerva does not create rosters.
- Minerva does not change worker schedules.
- Minerva does not mutate Pattern, PatternDay or EmployeeAppointmentPattern truth.
- Minerva does not mutate ObjectTime.
- Minerva does not calculate payroll.
- Minerva does not decide entitlements.
- Minerva does not calculate leave.
- Minerva does not approve leave.
- Minerva does not determine finalisation readiness.
- Minerva does not finalise PayRuns.
- Minerva does not mutate operational workforce/payroll/leave truth.

## Domain Retrieval Coverage

The Rosters / Patterns / Scheduling domain retrieval plan is a deterministic evidence-gathering plan for questions about governed expected-time, work-pattern and scheduling evidence. It splits broad and focused questions into targeted evidence groups and retrieves formal corpus chunks for each group.

The v0.3 corpus coverage diagnostic covers:

- `roster_pattern_source_and_configuration`;
- `appointment_worksite_and_applicability_context`;
- `ordinary_hours_leave_basis_and_public_holiday_context`;
- `payroll_interpretation_and_worker_story_relationship`;
- `admin_queue_finalisation_and_readiness_relationship`;
- `minerva_boundaries_and_non_mutation_guardrails`.

The domain covers roster/pattern source data, Pattern, PatternDay, EmployeeAppointmentPattern, roster schedule configuration, expected work context, EmployeeAppointment / WorksitePosition / Worksite assignment context, state and public holiday context, ordinary-hours expectations, leave basis minutes, schedule/pattern relationship, public holiday and leave interaction, deferred roster-based basis hardening, ObjectTime/source-truth boundaries, expected schedule versus actual worked time, Worker Story, Decision Story, Payroll Output, Admin Queue, Worker Attention, Finalisation Readiness and Minerva non-mutation guardrails.

The plan decides what evidence to search for. It does not create rosters, change worker schedules, mutate Pattern, PatternDay or EmployeeAppointmentPattern truth, mutate ObjectTime, calculate payroll, decide entitlements, calculate leave, approve leave, determine finalisation readiness, finalise PayRuns, prove operational correctness, or mutate workforce/payroll/leave truth. If evidence is weak or missing, Minerva should report the corpus limitation instead of inventing a product claim.

## Difference From Other Evaluations

ObjectTime / Source Truth evaluation owns actual source time rows, source truth and actual worked-time evidence. Rosters / Patterns / Scheduling can compare expected schedule with ObjectTime, but expected schedule must not be collapsed into actual worked time.

Contacts / Employee Appointments evaluation owns appointment identity and employment assignment questions. Rosters / Patterns / Scheduling can explain how EmployeeAppointment, WorksitePosition and Worksite context affect schedule applicability, but it does not replace appointment identity ownership.

Public Holidays evaluation owns public holiday handling, calendars and DeductsOnPublicHoliday. Rosters / Patterns / Scheduling can explain state/public holiday context and leave interaction where supported, but it does not own Public Holidays.

Leave Accrual / Processing and Leave Source Model own leave accrual calculation and leave applicability/source-model questions. Rosters / Patterns / Scheduling can explain leave-basis context and ordinary-hours expectations, but it does not calculate leave.

Leave Requests / Leave Workflow owns leave request lifecycle, approval, shortfall and reopen questions. Rosters / Patterns / Scheduling can provide schedule context for leave questions where supported, but it does not approve or manage leave requests.

Payroll Output, Decision Story, Worker Story, Payroll Bases & Totals, Finalisation Readiness, Worker Attention / Issue Resolution and Process Periods / PayRun Lifecycle keep ownership of their generic domains. Rosters / Patterns / Scheduling can explain relationships to those surfaces only when the question is roster/pattern/scheduling-framed.

## Commands

Run commands from the repository root.

### Full Pytest Suite

```powershell
.\.venv\Scripts\python.exe -m pytest --basetemp .\.pytest_tmp
```

This is the main regression gate. It should pass before treating any benchmark or diagnostic output as meaningful.

### Rosters / Patterns / Scheduling Benchmark

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.rosters_patterns_scheduling.json
```

The benchmark includes the broad question, "How do Rosters, Patterns and Scheduling work in the platform?", plus focused follow-up questions about expected work context, EmployeeAppointment / Worksite relationships, ordinary hours and leave basis, ObjectTime/source-truth boundaries, Worker Story and payroll evidence, and missing roster or pattern configuration.

### Focused Contract And Routing Tests

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_rosters_patterns_scheduling_corpus_coverage.py tests\test_rosters_patterns_scheduling_answer_gap_report.py tests\test_domain_retrieval_plans.py tests\test_rich_answer_contract.py --basetemp .\.pytest_tmp
```

Use this when touching Rosters / Patterns / Scheduling benchmark, routing, diagnostic, answer gap report or documentation behavior.

### Corpus Coverage Diagnostic

Human-readable mode:

```powershell
.\.venv\Scripts\python.exe scripts\scan_rosters_patterns_scheduling_corpus_coverage.py
```

JSON mode:

```powershell
.\.venv\Scripts\python.exe scripts\scan_rosters_patterns_scheduling_corpus_coverage.py --json
```

Write diagnostic JSON to a file:

```powershell
.\.venv\Scripts\python.exe scripts\scan_rosters_patterns_scheduling_corpus_coverage.py --json --output .\artifacts\eval\rosters_patterns_scheduling_corpus_coverage.json
```

The diagnostic reads the already indexed formal corpus and reports coverage for each Rosters / Patterns / Scheduling evidence group. It does not ingest files, mutate corpus records, call a live LLM, ingest operational JSON, connect Code Evidence to answer generation, or change schema.

### Answer Gap Report

Human-readable mode:

```powershell
.\.venv\Scripts\python.exe scripts\build_rosters_patterns_scheduling_answer_gap_report.py --coverage-report .\artifacts\eval\rosters_patterns_scheduling_corpus_coverage.json
```

JSON mode:

```powershell
.\.venv\Scripts\python.exe scripts\build_rosters_patterns_scheduling_answer_gap_report.py --coverage-report .\artifacts\eval\rosters_patterns_scheduling_corpus_coverage.json --json
```

Write answer gap report JSON to a file:

```powershell
.\.venv\Scripts\python.exe scripts\build_rosters_patterns_scheduling_answer_gap_report.py --coverage-report .\artifacts\eval\rosters_patterns_scheduling_corpus_coverage.json --json --output .\artifacts\eval\rosters_patterns_scheduling_answer_gap_report.json
```

The gap report consumes the coverage diagnostic JSON and recommends the next action for each evidence group.

## Interpreting Benchmark Results

Benchmark results are deterministic regression checks over the loaded Minerva corpus.

- `PASS` means the question met its configured retrieval and answer checks.
- `FAIL` means at least one expected source, source phrase, answer phrase, section, answer mode, routing, or forbidden-pattern check did not pass.

A failure does not automatically mean answer synthesis is wrong. Common causes are:

- the loaded corpus does not contain enough formal evidence;
- retrieval terms do not find the relevant formal evidence;
- synthesis found evidence but did not express the expected Rosters / Patterns / Scheduling wording;
- another domain owns the question and the routing expectation needs review;
- the benchmark expectation no longer matches the intended product-domain wording.

Investigate failures from the returned source references, failed checks, coverage diagnostic, and answer gap report before changing code.

## Interpreting Coverage Status

The coverage diagnostic classifies each Rosters / Patterns / Scheduling evidence group:

- `STRONG`: multiple relevant chunks or documents were found. The corpus likely has enough retrievable evidence for the group.
- `WEAK`: some relevant evidence was found, but coverage is thin. Answers may be incomplete or overly dependent on one source.
- `MISSING`: no useful evidence was found for the group. Minerva should treat that part of the answer as corpus-limited.

Coverage status is about available formal corpus evidence, not runtime roster, pattern, scheduling, payroll or leave truth. A `MISSING` group may mean the product concept exists but the indexed formal evidence is not loaded or not discoverable yet.

## Interpreting Gap Report Status

The answer gap report summarizes whether Rosters / Patterns / Scheduling answers are ready enough to keep, refine, or defer.

- `GOOD`: evidence is strong enough for the current answer path.
- `NEEDS_REFINEMENT`: evidence exists but retrieval terms or synthesis may need refinement.
- `INSUFFICIENT_CORPUS`: important evidence is missing from the indexed formal corpus.

Use the per-group findings rather than only the overall status. A supporting group can need refinement while the core answer remains usable.

## Recommended Next Actions

The gap report may recommend:

- `KEEP`: leave the current retrieval and synthesis behavior unchanged for this group.
- `IMPROVE_RETRIEVAL_TERMS`: refine deterministic search terms or group targeting so existing corpus evidence is found more reliably.
- `IMPROVE_SYNTHESIS`: adjust answer synthesis so retrieved evidence is explained more clearly and completely.
- `ADD_FORMAL_SOURCE_EVIDENCE_LATER`: do not fix this in code yet; load or author formal source evidence in a later corpus slice.

Do not treat `ADD_FORMAL_SOURCE_EVIDENCE_LATER` as permission to ingest files during this runbook. It is a planning signal only.

## When To Improve What

- Improve retrieval terms when formal evidence exists but diagnostic coverage is `WEAK` because the scanner is not finding enough relevant corpus support.
- Improve synthesis when coverage is `STRONG` but benchmark or human review shows the answer is incomplete, too broad, or missing required Rosters / Patterns / Scheduling guardrails.
- Add formal source evidence later when the group is genuinely `MISSING` from the indexed formal corpus.
- Keep existing behavior where coverage and answer quality are acceptable.
- Do not use operational JSON or Code Evidence as a shortcut for missing formal source evidence.

## Guardrails

This workflow must remain:

- diagnostic-only;
- no corpus mutation;
- no live LLM calls;
- no database schema change;
- no operational JSON ingestion;
- no Code Evidence answer integration;
- no Code Evidence Index answer integration;
- not proof of runtime roster, pattern or scheduling implementation;
- not proof of runtime operational truth;
- diagnostics do not mutate corpus;
- diagnostics do not call a live LLM;
- diagnostics do not ingest operational JSON;
- diagnostics do not connect Code Evidence to answer generation;
- diagnostics do not prove runtime operational truth;
- diagnostics do not create rosters;
- diagnostics do not change worker schedules;
- diagnostics do not mutate Pattern, PatternDay or EmployeeAppointmentPattern truth;
- diagnostics do not mutate ObjectTime;
- diagnostics do not calculate payroll;
- diagnostics do not decide entitlements;
- diagnostics do not calculate or approve leave;
- diagnostics do not determine or finalise readiness;
- diagnostics do not mutate operational workforce/payroll/leave truth.

Diagnostics do not create, change, mutate, calculate, decide, approve, determine readiness or finalise anything. Minerva does not create rosters, change worker schedules, mutate Pattern, PatternDay or EmployeeAppointmentPattern truth, mutate ObjectTime, calculate payroll, decide entitlements, calculate leave, approve leave, determine finalisation readiness, finalise PayRuns or mutate operational workforce/payroll/leave truth. Rosters / Patterns / Scheduling evaluation must continue to use the indexed formal knowledge corpus. It must not read or ingest source-code content as Minerva answer evidence, and it must not connect Code Evidence Index to answer generation.
