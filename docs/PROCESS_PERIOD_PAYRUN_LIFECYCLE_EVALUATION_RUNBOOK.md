# Process Periods / PayRun Lifecycle Evaluation Runbook

This runbook documents the repeatable Minerva evaluation workflow for Process Periods / PayRun Lifecycle. It is intended for regression checks and corpus-readiness diagnostics after retrieval-plan, benchmark, synthesis, diagnostic tooling, or formal corpus changes.

The workflow is diagnostic-only. It does not mutate corpus records, change database schema, ingest operational JSON, call a live LLM, read source-code content as Minerva evidence, or connect Code Evidence Index to answer generation.

## Purpose

Process Periods / PayRun Lifecycle evaluation checks whether Minerva can retrieve and synthesize enough formal evidence to answer product-domain questions about governed payroll-period context, payment-event lifecycle evidence, period states, PayRun creation/admission, run types, PayRunContact state, current-effective output, finalisation readiness, payment execution and review surfaces.

The evaluation answers four practical questions:

- Does the full test suite still pass?
- Does the broad Process Periods / PayRun Lifecycle benchmark still pass?
- Do the 12 focused follow-up benchmark questions still pass?
- Does the currently indexed formal corpus contain enough evidence for each Process Periods / PayRun Lifecycle evidence group?

Process Periods / PayRun Lifecycle evaluation is not proof of runtime ProcessPeriod / PayRun lifecycle truth. It evaluates Minerva retrieval and answer quality over formal knowledge evidence. It is not proof that ProcessPeriod calculates payroll, that open means safe to finalise, that closed-period truth can be silently changed, that regular, supplementary and retro PayRuns are interchangeable, that PaymentDate derivation is hardcoded, or that payment execution / period close is complete.

## Domain Retrieval Coverage

The Process Periods / PayRun Lifecycle domain retrieval plan is a deterministic evidence-gathering plan for questions about payroll-period governance and PayRun payment/processing event lifecycle. It splits broad and focused questions into targeted evidence groups and retrieves formal corpus chunks for each group.

The plan covers:

- purpose and operator meaning;
- ProcessPeriod and ProcessPeriodGroup context;
- open, not-open and closed lifecycle;
- closed dominates open;
- close rolls forward;
- PaymentDate and calendar/payment policy;
- PayRun creation and worker admission inside a ProcessPeriod;
- RunType and RunPurpose as separate dimensions;
- regular, supplementary and retro PayRuns, plus termination, reversal and adjustment run concepts;
- PayRunContact lifecycle and worker participation state;
- admission is not processing;
- current-effective output and finalisation readiness;
- payment execution and period close;
- Worker Story, Admin Queue and Movement Review connections;
- outstanding hardening.

The plan decides what evidence to search for. It does not calculate payroll, prove runtime period state, mutate ProcessPeriod or PayRun records, finalise PayRuns, execute payments, close periods, or replace deterministic Ezeas services. If evidence is weak or missing, Minerva should report the corpus limitation instead of inventing a product claim.

## Difference From Other Evaluations

Tax / PAYG evaluation owns withholding evidence, TaxStory, taxable basis, worker tax declarations and tax-context ProcessPeriod PaymentDate questions. Process Periods / PayRun Lifecycle can explain why PaymentDate belongs in governed period/payment context, but it must not steal Tax / PAYG ownership where the question is primarily about tax calculation or withholding.

Retro / Replay evaluation owns governed historical correction, attributed-period truth, paid-period truth, current-effective versus historical truth, finalised outcome memory and replay governance. Process Periods / PayRun Lifecycle can explain regular, supplementary and retro PayRuns as different lifecycle concepts, but retro-framed period/replay questions remain owned by Retro / Replay.

Finalisation Readiness evaluation owns readiness gates, blockers, warnings, warning acknowledgement and whether a PayRun can be finalised safely. Process Periods / PayRun Lifecycle can explain how current-effective output, PayRun state and period context feed finalisation readiness, but finalisation-framed readiness questions remain owned by Finalisation Readiness.

Payment Execution / Remittance evaluation owns bank files, payment allocation, worker net pay, third-party remittance, remittance reconciliation and payment execution readiness. Process Periods / PayRun Lifecycle can explain payment execution and period close as downstream governed outcomes, but it does not own payment file generation or remittance truth.

ObjectTime / Source Truth evaluation checks governed source evidence, source-row inclusion, SourceTruth versus WorkedHours and provenance. Process Periods / PayRun Lifecycle can explain PayRun creation/admission and worker inclusion at lifecycle level, but ObjectTime / Source Truth owns source-row evidence and inclusion provenance.

Contacts / Employee Appointments evaluation checks Contact identity, EmployeeAppointment assignment, worker readiness and appointment-specific context. Process Periods / PayRun Lifecycle may consume worker/admission context, but Contact versus EmployeeAppointment ownership stays with Contacts / Employee Appointments.

Worker Story, PayRun Admin Queue and Movement Review evaluations own their explanation, action-workbench and review-surface concerns. Process Periods / PayRun Lifecycle explains how those surfaces connect to worker participation, readiness and review implications, but it does not replace their domain-specific evaluations.

Payroll Bases & Totals, Leave Source Model, Leave Accrual / Processing, Deductions / Obligations, On-costs / Employer Liabilities, Award Build / Award Evidence, Imports / Actuals, Comparison / Remediation and other domain evaluations own their specific evidence and calculation/readiness boundaries. Process Periods / PayRun Lifecycle supplies period/payment-event context; it is not their runtime calculation truth.

All evaluations use deterministic retrieval and benchmark checks. Process Periods / PayRun Lifecycle additionally has corpus coverage diagnostics and an answer gap report that classify evidence readiness group by group.

## Commands

Run commands from the repository root.

### Full Pytest Suite

```powershell
.\.venv\Scripts\python.exe -m pytest --basetemp .\.pytest_tmp
```

This is the main regression gate. It should pass before treating any benchmark or diagnostic output as meaningful.

### Process Periods / PayRun Lifecycle Benchmark

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.process_period_payrun_lifecycle.json
```

The benchmark includes the broad Process Periods / PayRun Lifecycle question plus 12 focused follow-up questions covering ProcessPeriod versus ProcessPeriodGroup, open / not-open / closed lifecycle, closed dominates open, close rolls forward, PaymentDate, PayRun creation and worker admission, RunType versus RunPurpose, regular / supplementary / retro PayRuns, PayRunContact, admission is not processing, current-effective output and connections to Finalisation Readiness, Payment Execution, Worker Story, Admin Queue and Movement Review.

### Corpus Coverage Diagnostic

```powershell
.\.venv\Scripts\python.exe scripts\scan_process_period_payrun_lifecycle_corpus_coverage.py
.\.venv\Scripts\python.exe scripts\scan_process_period_payrun_lifecycle_corpus_coverage.py --json --output .\artifacts\eval\process_period_payrun_lifecycle_corpus_coverage.json
```

The diagnostic reads the already indexed formal corpus and reports coverage for each Process Periods / PayRun Lifecycle evidence group. It does not ingest files, mutate corpus records, call a live LLM, or change schema.

### Answer Gap Report

```powershell
.\.venv\Scripts\python.exe scripts\build_process_period_payrun_lifecycle_answer_gap_report.py --coverage-report .\artifacts\eval\process_period_payrun_lifecycle_corpus_coverage.json
.\.venv\Scripts\python.exe scripts\build_process_period_payrun_lifecycle_answer_gap_report.py --coverage-report .\artifacts\eval\process_period_payrun_lifecycle_corpus_coverage.json --json --output .\artifacts\eval\process_period_payrun_lifecycle_answer_gap_report.json
```

The gap report consumes the coverage diagnostic JSON and recommends the next action for each evidence group.

## Interpreting Benchmark Results

Benchmark results are deterministic regression checks over the loaded Minerva corpus.

- `PASS` means the question met its configured retrieval and answer checks.
- `FAIL` means at least one expected source, source phrase, answer phrase, section, or forbidden-pattern check did not pass.

A failure does not automatically mean answer synthesis is wrong. Common causes are:

- the loaded corpus does not contain enough formal evidence;
- retrieval terms do not find the relevant formal evidence;
- synthesis found evidence but did not express the expected Process Periods / PayRun Lifecycle wording;
- another domain owns the question and the routing expectation needs review;
- the benchmark expectation no longer matches the intended product-domain wording.

Investigate failures from the returned source references, failed checks, coverage diagnostic, and answer gap report before changing code.

## Interpreting Coverage Status

The coverage diagnostic classifies each Process Periods / PayRun Lifecycle evidence group:

- `STRONG`: multiple relevant chunks or documents were found. The corpus likely has enough retrievable evidence for the group.
- `WEAK`: some relevant evidence was found, but coverage is thin. Answers may be incomplete or overly dependent on one source.
- `MISSING`: no useful evidence was found for the group. Minerva should treat that part of the answer as corpus-limited.

Coverage status is about available formal corpus evidence, not runtime ProcessPeriod / PayRun lifecycle truth. A `MISSING` group may mean the product concept exists but the indexed formal evidence is not loaded or not discoverable yet.

## Interpreting Gap Report Status

The answer gap report summarizes whether Process Periods / PayRun Lifecycle answers are ready enough to keep, refine, or defer.

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

## Guardrails

This workflow must remain:

- diagnostic-only;
- no corpus mutation;
- no live LLM calls;
- no database schema change;
- no operational JSON ingestion;
- no Code Evidence Index answer integration;
- not proof of runtime ProcessPeriod / PayRun lifecycle truth;
- not proof that ProcessPeriod calculates payroll;
- not proof that open means safe to finalise;
- not proof that closed-period truth can be silently changed;
- not proof that regular, supplementary and retro PayRuns are interchangeable;
- not proof that PaymentDate derivation is hardcoded;
- not proof that payment execution / period close is complete.

Process Periods / PayRun Lifecycle evaluation must continue to use the indexed formal knowledge corpus. It must not read or ingest source-code content as Minerva answer evidence, and it must not connect Code Evidence Index to answer generation.
