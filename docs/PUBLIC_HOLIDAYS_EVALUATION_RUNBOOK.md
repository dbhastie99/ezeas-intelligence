# Public Holidays Evaluation Runbook

This runbook documents the repeatable Minerva evaluation workflow for Public Holidays. It is intended for regression checks and corpus-readiness diagnostics after retrieval-plan, benchmark, synthesis, diagnostic tooling, or formal corpus changes.

The workflow is diagnostic-only. It does not mutate corpus records, change database schema, ingest operational JSON, call a live LLM, read source-code content as Minerva evidence, or connect Code Evidence Index to answer generation. It also provides no Code Evidence answer integration and is not proof of runtime operational truth.

## Purpose

Public Holidays is the Minerva product-domain explaining governed public holiday source/calendar evidence, PublicHolidayGroup context, worksite/state applicability, payroll treatment relationship, leave interaction, Worker Story evidence, Admin Queue / Worker Attention and Finalisation Readiness relationships.

The evaluation answers four practical questions:

- Does the full test suite still pass?
- Does the Public Holidays broad and focused rich-answer benchmark still pass?
- Do Public Holiday-framed questions still route to the Public Holidays domain while overlapping domains keep ownership?
- Does the currently indexed formal corpus contain enough evidence for each Public Holidays evidence group?

Public Holidays evaluation is not proof of runtime Public Holiday implementation. It evaluates Minerva retrieval and answer quality over formal knowledge evidence. Minerva explains Public Holiday handling. Minerva does not calculate public holiday entitlements, decide payroll treatment, post payroll output, approve leave, calculate leave, post LeaveLedger rows, change leave balances, change PublicHolidayGroup configuration, mutate Worksite, EmployeeAppointment, PayRun, LeaveRequest or payroll truth, determine finalisation readiness, or finalise PayRuns.

Explicit Minerva boundary:

- Minerva explains Public Holiday handling.
- Minerva does not calculate public holiday entitlements.
- Minerva does not decide payroll treatment.
- Minerva does not post payroll output.
- Minerva does not approve leave.
- Minerva does not calculate leave.
- Minerva does not post LeaveLedger rows.
- Minerva does not change leave balances.
- Minerva does not change PublicHolidayGroup configuration.
- Minerva does not mutate Worksite, EmployeeAppointment, PayRun, LeaveRequest or payroll truth.
- Minerva does not determine finalisation readiness.
- Minerva does not finalise PayRuns.

## Domain Retrieval Coverage

The Public Holidays domain retrieval plan is a deterministic evidence-gathering plan for questions about governed public holiday handling. It splits broad and focused questions into targeted evidence groups and retrieves formal corpus chunks for each group.

The v0.3 corpus coverage diagnostic covers:

- `public_holiday_source_and_calendar`;
- `worksite_state_and_applicability_context`;
- `payroll_treatment_and_decision_story`;
- `leave_interaction_and_deducts_on_public_holiday`;
- `worker_story_admin_queue_and_finalisation`;
- `minerva_boundaries_and_non_mutation_guardrails`.

The domain covers PublicHoliday and PublicHolidayGroup source/calendar evidence, observed days and overrides where supported, Worksite / WorksitePosition / EmployeeAppointment worksite/state context, deterministic payroll treatment and Decision Story relationship, Payroll Output relationship, DeductsOnPublicHoliday and Leave Requests / LeaveLedger interaction, Worker Story payroll evidence, PayRun Admin Queue / Worker Attention surfacing, Finalisation Readiness relationships, and Minerva non-mutation guardrails.

The plan decides what evidence to search for. It does not calculate public holiday entitlements, decide payroll treatment, post payroll output, approve leave, calculate leave, post LeaveLedger rows, change leave balances, change PublicHolidayGroup configuration, mutate Worksite or EmployeeAppointment truth, mutate PayRun or LeaveRequest truth, determine finalisation readiness, finalise PayRuns, prove operational correctness, or mutate payroll truth. If evidence is weak or missing, Minerva should report the corpus limitation instead of inventing a product claim.

## Difference From Other Evaluations

Leave Requests / Leave Workflow evaluation owns leave approval, leave request lifecycle, shortfall, reopening, approval and leave workflow questions. Public Holidays can explain how public holidays affect leave requests or LeaveLedger relationships, but it does not own the broad leave request workflow.

Leave Accrual / Processing evaluation owns deterministic leave accrual calculation and LeaveLedger accrual processing. Public Holidays can explain DeductsOnPublicHoliday and leave interaction where supported, but it does not calculate leave.

Leave Source Model evaluation owns general leave applicability/source-model questions. Public Holidays can explain public-holiday worksite/state applicability context, but it does not replace Leave Source Model.

Payroll Output evaluation owns generic payroll output/current-effective output questions. Public Holidays can explain how public holiday evidence relates to payroll output, but it does not post payroll output.

Decision Story evaluation owns generic treatment/entitlement explanation questions. Public Holidays can connect public holiday treatment to Decision Story, but it does not decide treatment.

Worker Story evaluation owns broad worker-level evidence narrative. Public Holidays can appear in Worker Story and payroll evidence, but it does not replace Worker Story.

Finalisation Readiness and Worker Attention / Issue Resolution own generic readiness gates, blockers, warnings and fix-link questions. Public Holidays can explain missing public holiday configuration or location context as readiness evidence where supported, but it does not determine or finalise readiness.

On-costs / Employer Liabilities owns broad employer liability/on-cost questions. Public Holidays can explain a public-holiday-specific relationship to state/location context and liabilities where formal evidence supports it, but it does not own the broad on-costs domain.

## Commands

Run commands from the repository root.

### Full Pytest Suite

```powershell
.\.venv\Scripts\python.exe -m pytest --basetemp .\.pytest_tmp
```

This is the main regression gate. It should pass before treating any benchmark or diagnostic output as meaningful.

### Public Holidays Benchmark

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.public_holidays.json
```

The benchmark includes the broad question, "How are Public Holidays handled in the platform?", plus focused follow-up questions about worker applicability, payroll treatment, leave request and LeaveLedger posting interaction, Worker Story and payroll evidence, missing configuration or location context, and employer liabilities or on-cost relationships.

### Focused Contract And Routing Tests

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_public_holidays_corpus_coverage.py tests\test_public_holidays_answer_gap_report.py tests\test_domain_retrieval_plans.py tests\test_rich_answer_contract.py --basetemp .\.pytest_tmp
```

Use this when touching Public Holidays benchmark, routing, diagnostic, answer gap report or documentation behavior.

### Corpus Coverage Diagnostic

Human-readable mode:

```powershell
.\.venv\Scripts\python.exe scripts\scan_public_holidays_corpus_coverage.py
```

JSON mode:

```powershell
.\.venv\Scripts\python.exe scripts\scan_public_holidays_corpus_coverage.py --json
```

Write diagnostic JSON to a file:

```powershell
.\.venv\Scripts\python.exe scripts\scan_public_holidays_corpus_coverage.py --json --output .\artifacts\eval\public_holidays_corpus_coverage.json
```

The diagnostic reads the already indexed formal corpus and reports coverage for each Public Holidays evidence group. It does not ingest files, mutate corpus records, call a live LLM, ingest operational JSON, connect Code Evidence to answer generation, or change schema.

### Answer Gap Report

Human-readable mode:

```powershell
.\.venv\Scripts\python.exe scripts\build_public_holidays_answer_gap_report.py --coverage-report .\artifacts\eval\public_holidays_corpus_coverage.json
```

JSON mode:

```powershell
.\.venv\Scripts\python.exe scripts\build_public_holidays_answer_gap_report.py --coverage-report .\artifacts\eval\public_holidays_corpus_coverage.json --json
```

Write answer gap report JSON to a file:

```powershell
.\.venv\Scripts\python.exe scripts\build_public_holidays_answer_gap_report.py --coverage-report .\artifacts\eval\public_holidays_corpus_coverage.json --json --output .\artifacts\eval\public_holidays_answer_gap_report.json
```

The gap report consumes the coverage diagnostic JSON and recommends the next action for each evidence group.

## Interpreting Benchmark Results

Benchmark results are deterministic regression checks over the loaded Minerva corpus.

- `PASS` means the question met its configured retrieval and answer checks.
- `FAIL` means at least one expected source, source phrase, answer phrase, section, answer mode, routing, or forbidden-pattern check did not pass.

A failure does not automatically mean answer synthesis is wrong. Common causes are:

- the loaded corpus does not contain enough formal evidence;
- retrieval terms do not find the relevant formal evidence;
- synthesis found evidence but did not express the expected Public Holidays wording;
- another domain owns the question and the routing expectation needs review;
- the benchmark expectation no longer matches the intended product-domain wording.

Investigate failures from the returned source references, failed checks, coverage diagnostic, and answer gap report before changing code.

## Interpreting Coverage Status

The coverage diagnostic classifies each Public Holidays evidence group:

- `STRONG`: multiple relevant chunks or documents were found. The corpus likely has enough retrievable evidence for the group.
- `WEAK`: some relevant evidence was found, but coverage is thin. Answers may be incomplete or overly dependent on one source.
- `MISSING`: no useful evidence was found for the group. Minerva should treat that part of the answer as corpus-limited.

Coverage status is about available formal corpus evidence, not runtime Public Holiday implementation or operational payroll/leave truth. A `MISSING` group may mean the product concept exists but the indexed formal evidence is not loaded or not discoverable yet.

## Interpreting Gap Report Status

The answer gap report summarizes whether Public Holidays answers are ready enough to keep, refine, or defer.

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
- Improve synthesis when coverage is `STRONG` but benchmark or human review shows the answer is incomplete, too broad, or missing required Public Holidays guardrails.
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
- not proof of runtime Public Holiday implementation;
- not proof of runtime operational truth;
- diagnostics do not mutate corpus;
- diagnostics do not call a live LLM;
- diagnostics do not ingest operational JSON;
- diagnostics do not connect Code Evidence to answer generation;
- diagnostics do not prove runtime operational truth;
- diagnostics do not calculate public holiday entitlements;
- diagnostics do not decide payroll treatment;
- diagnostics do not approve or calculate leave;
- diagnostics do not post LeaveLedger rows;
- diagnostics do not mutate Worksite/PublicHolidayGroup/EmployeeAppointment/PayRun/LeaveRequest truth;
- diagnostics do not determine or finalise readiness.

Diagnostics do not calculate, decide, approve, post, mutate, determine readiness or finalise anything. Minerva does not calculate public holiday entitlements, decide payroll treatment, post payroll output, approve leave, calculate leave, post LeaveLedger rows, change leave balances, change PublicHolidayGroup configuration, mutate Worksite, EmployeeAppointment, PayRun, LeaveRequest or payroll truth, determine finalisation readiness or finalise PayRuns. Public Holidays evaluation must continue to use the indexed formal knowledge corpus. It must not read or ingest source-code content as Minerva answer evidence, and it must not connect Code Evidence Index to answer generation.
