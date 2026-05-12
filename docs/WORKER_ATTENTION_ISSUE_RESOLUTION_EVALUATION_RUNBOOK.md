# Worker Attention / Issue Resolution Evaluation Runbook

This runbook documents the repeatable Minerva evaluation workflow for Worker Attention / Issue Resolution. It is intended for regression checks and corpus-readiness diagnostics after retrieval-plan, benchmark, synthesis, diagnostic tooling, or formal corpus changes.

The workflow is diagnostic-only. It does not mutate corpus records, change database schema, ingest operational JSON, call a live LLM, read source-code content as Minerva evidence, or connect Code Evidence Index to answer generation.

## Purpose

Worker Attention / Issue Resolution evaluation checks whether Minerva can retrieve and synthesize enough formal evidence to answer product-domain questions about the worker-level issue and resolution surface for payroll-affecting blockers, warnings, readiness gaps and deterministic fix links.

The evaluation answers four practical questions:

- Does the full test suite still pass?
- Does the broad Worker Attention / Issue Resolution benchmark still pass?
- Do the focused follow-up benchmark questions still pass?
- Does the currently indexed formal corpus contain enough evidence for each Worker Attention / Issue Resolution evidence group?

Worker Attention / Issue Resolution evaluation is not proof of runtime Worker Attention implementation. It evaluates Minerva retrieval and answer quality over formal knowledge evidence. It is not proof that Minerva resolves issues, clears blockers, marks PayRunContact dirty, reprocesses workers, calculates payroll, approves, suppresses, finalises or mutates payroll truth. It is also not proof that Worker Attention proves payroll correctness, deterministic fix-link contracts are complete, or issue taxonomy or resolution workflow is complete.

## Domain Retrieval Coverage

The Worker Attention / Issue Resolution domain retrieval plan is a deterministic evidence-gathering plan for questions about worker-level issue modelling, readiness gaps and guided resolution surfaces. It splits broad and focused questions into targeted evidence groups and retrieves formal corpus chunks for each group.

The plan covers:

- Worker Attention purpose and operator meaning;
- WorkerIssue / worker issue model;
- IssueScope / issue scope, IssueClass / issue class, IssueType / issue type and IssueSeverity / severity;
- blockers, warnings and readiness gaps;
- deterministic fix link / deterministic fix links;
- resolution surface, in-context remediation and governed user action;
- dirty contact, PayRunContact dirty, PENDING dirty state and reprocessing signals;
- payment allocation readiness and payment execution readiness;
- tax readiness, deduction readiness and leave readiness;
- negative net pay, obligations, carry-forward, recovery and write-off pathways where supported by corpus evidence;
- Worker Story relationship;
- PayRun Admin Queue relationship;
- outstanding hardening.

The plan decides what evidence to search for. It does not resolve worker issues, clear blockers, mutate dirty state, reprocess workers, calculate payroll, approve, suppress, finalise or repair payroll truth. If evidence is weak or missing, Minerva should report the corpus limitation instead of inventing a product claim.

## Difference From Other Evaluations

PayRun Admin Queue evaluation owns the operator workbench for what needs action now, including blockers, warnings, ready actions and broader PayRun action workflow. Worker Attention / Issue Resolution owns the worker-level issue and resolution surface. The surfaces are related but not identical.

Worker Story evaluation owns worker evidence, narrative context and explanation of why a worker has a payroll outcome or issue. Worker Attention may expose an issue and resolution path; Worker Story explains evidence and context for that worker.

Contacts / Employee Appointments evaluation owns Contact identity, EmployeeAppointment context, appointment-specific worker readiness, contact history and worker context. Worker Attention can surface a dirty contact or worker readiness issue, but contact/appointment truth remains owned by Contacts / Employee Appointments.

Payment Execution / Remittance evaluation owns payment execution readiness, bank/payment allocation, remittance batching and reconciliation. Worker Attention can surface payment allocation readiness or payment destination blockers for a worker, but it does not execute payments.

Tax / PAYG evaluation owns governed withholding evidence, tax readiness, worker tax declarations and TaxStory. Worker Attention can surface tax readiness as a worker-level issue, but it does not calculate tax or own tax truth.

Deductions / Obligations evaluation owns deduction applicability, affordability, PayRunDeductionApplication, obligations, recovery, carry-forward and write-off policy. Worker Attention can surface deduction readiness, negative net pay or obligation issues, but it does not decide those obligations.

Leave Accrual / Processing evaluation owns leave accrual, TAKEN leave valuation, LeaveLedger and leave readiness evidence. Worker Attention can surface leave readiness as a worker-level issue, but it does not calculate leave or mutate leave outcomes.

Finalisation Readiness evaluation owns readiness gates, blockers, warnings, current-effective output and finalisation safety. Worker Attention can supply worker-level blockers or warnings that contribute to readiness, but it does not determine finalisation or clear readiness state.

All evaluations use deterministic retrieval and benchmark checks. Worker Attention / Issue Resolution additionally has corpus coverage diagnostics and an answer gap report that classify evidence readiness group by group.

## Commands

Run commands from the repository root.

### Full Pytest Suite

```powershell
.\.venv\Scripts\python.exe -m pytest --basetemp .\.pytest_tmp
```

This is the main regression gate. It should pass before treating any benchmark or diagnostic output as meaningful.

### Worker Attention / Issue Resolution Benchmark

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.worker_attention_issue_resolution.json
```

The benchmark includes the broad question, "What is Worker Attention / Issue Resolution in the platform?", plus focused follow-up questions about the worker issue model, deterministic fix links and resolution surfaces, dirty contact and reprocessing, payment allocation and negative net pay, and Worker Attention relationships with Admin Queue and Worker Story.

### Corpus Coverage Diagnostic

```powershell
.\.venv\Scripts\python.exe scripts\scan_worker_attention_issue_resolution_corpus_coverage.py
.\.venv\Scripts\python.exe scripts\scan_worker_attention_issue_resolution_corpus_coverage.py --json --output .\artifacts\eval\worker_attention_issue_resolution_corpus_coverage.json
```

The diagnostic reads the already indexed formal corpus and reports coverage for each Worker Attention / Issue Resolution evidence group. It does not ingest files, mutate corpus records, call a live LLM, ingest operational JSON, connect Code Evidence to answer generation, or change schema.

### Answer Gap Report

```powershell
.\.venv\Scripts\python.exe scripts\build_worker_attention_issue_resolution_answer_gap_report.py --coverage-report .\artifacts\eval\worker_attention_issue_resolution_corpus_coverage.json
.\.venv\Scripts\python.exe scripts\build_worker_attention_issue_resolution_answer_gap_report.py --coverage-report .\artifacts\eval\worker_attention_issue_resolution_corpus_coverage.json --json --output .\artifacts\eval\worker_attention_issue_resolution_answer_gap_report.json
```

The gap report consumes the coverage diagnostic JSON and recommends the next action for each evidence group.

## Interpreting Benchmark Results

Benchmark results are deterministic regression checks over the loaded Minerva corpus.

- `PASS` means the question met its configured retrieval and answer checks.
- `FAIL` means at least one expected source, source phrase, answer phrase, section, or forbidden-pattern check did not pass.

A failure does not automatically mean answer synthesis is wrong. Common causes are:

- the loaded corpus does not contain enough formal evidence;
- retrieval terms do not find the relevant formal evidence;
- synthesis found evidence but did not express the expected Worker Attention / Issue Resolution wording;
- another domain owns the question and the routing expectation needs review;
- the benchmark expectation no longer matches the intended product-domain wording.

Investigate failures from the returned source references, failed checks, coverage diagnostic, and answer gap report before changing code.

## Interpreting Coverage Status

The coverage diagnostic classifies each Worker Attention / Issue Resolution evidence group:

- `STRONG`: multiple relevant chunks or documents were found. The corpus likely has enough retrievable evidence for the group.
- `WEAK`: some relevant evidence was found, but coverage is thin. Answers may be incomplete or overly dependent on one source.
- `MISSING`: no useful evidence was found for the group. Minerva should treat that part of the answer as corpus-limited.

Coverage status is about available formal corpus evidence, not runtime Worker Attention implementation or operational truth. A `MISSING` group may mean the product concept exists but the indexed formal evidence is not loaded or not discoverable yet.

## Interpreting Gap Report Status

The answer gap report summarizes whether Worker Attention / Issue Resolution answers are ready enough to keep, refine, or defer.

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
- not proof of runtime Worker Attention implementation;
- not proof that Minerva resolves issues;
- not proof that Minerva clears blockers;
- not proof that Minerva marks PayRunContact dirty;
- not proof that Minerva reprocesses workers;
- not proof that Worker Attention proves payroll correctness;
- not proof that deterministic fix-link contracts are complete;
- not proof that issue taxonomy or resolution workflow is complete.

Minerva does not resolve, clear, reprocess, calculate, approve, suppress, finalise or mutate payroll truth. Worker Attention / Issue Resolution evaluation must continue to use the indexed formal knowledge corpus. It must not read or ingest source-code content as Minerva answer evidence, and it must not connect Code Evidence Index to answer generation.
