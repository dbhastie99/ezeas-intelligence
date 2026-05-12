# Leave Source Model Evaluation Runbook

This runbook documents the repeatable Minerva evaluation workflow for Leave Source Model. It is intended for regression checks and corpus-readiness diagnostics after retrieval-plan, benchmark, synthesis, or formal corpus changes.

The workflow is diagnostic-only. It does not mutate corpus records, change database schema, ingest operational JSON, call a live LLM, or connect Code Evidence Index to answer generation.

## Purpose

Leave Source Model evaluation checks whether Minerva can retrieve and synthesize enough formal evidence to answer product-domain questions about governed leave applicability and leave source truth. It focuses on the difference between applicability and rule content, LeaveTypeRule limitations, contact versus appointment scope, source dimensions and precedence, no entitlement versus missing leave output, leave accrual and leave request/payment effects as consumers of applicability decisions, Worker Story leave chapters, Command Centre honesty, Finalisation Readiness, and outstanding hardening.

The evaluation answers four practical questions:

- Does the full test suite still pass?
- Does the broad Leave Source Model benchmark still pass?
- Do the 9 focused follow-up benchmark questions still pass?
- Does the currently indexed formal corpus contain enough evidence for each Leave Source Model evidence group?

Leave Source Model evaluation is not proof of runtime Leave Source Model truth. It evaluates Minerva retrieval and answer quality over formal knowledge evidence. Minerva does not calculate leave applicability. The evaluation is also not proof that Leave Source Model is fully implemented, LeaveTypeRule alone is final applicability truth, every active LeaveTypeRule means every worker should have leave output, or missing leave output is always wrong.

## Domain Retrieval Coverage

The Leave Source Model domain retrieval plan is a deterministic evidence-gathering plan for leave source-truth and applicability questions. It splits broad and focused questions into targeted evidence groups and retrieves formal corpus chunks for each group.

The plan covers:

- purpose and operator meaning;
- applicability versus rule content;
- LeaveTypeRule limitations;
- contact versus appointment scope;
- source dimensions and precedence;
- leave accrual connection;
- leave request and payment effects connection;
- Worker Story connection;
- Command Centre and Finalisation Readiness connection;
- readiness and missing output detection;
- outstanding hardening.

The plan decides what evidence to search for. It does not calculate leave applicability, complete the Leave Source Model, infer final applicability truth from LeaveTypeRule alone, decide that every active LeaveTypeRule requires worker leave output, treat missing leave output as always wrong, mutate payroll or leave history, prove runtime Leave Source Model truth, or infer missing implementation status. If evidence is weak or missing, Minerva should report the corpus limitation instead of inventing a product claim.

## Difference From Other Evaluations

Annual Leave overview evaluation checks the broader leave-management slice: configuration, accrual, TAKEN leave, valuation, PayRun orchestration, Worker Story leave evidence, and outstanding leave hardening. Leave Source Model is narrower and deeper around applicability/source truth behind leave readiness and entitlement applicability.

Leave Accrual / Processing evaluation checks detailed accrual, payroll output, LeaveLedger, valuation, request/payment sequencing and processing readiness. Leave Source Model does not evaluate accrual quantity or ledger posting; it evaluates the source decision that accrual and request/payment effects should consume.

Worker Story evaluation checks the broader explanation surface for worker-level payroll outcomes. Leave Source Model only checks Worker Story where leave chapters need to explain source/applicability decisions, no-entitlement outcomes, missing-output warnings or leave output.

Payroll Bases & Totals evaluation checks governed payroll basis evidence, current-effective truth, bucket readiness and stale PayrollBucketResult caveats. Leave Source Model does not evaluate basis totals; it may only explain where basis-related context is not a substitute for leave applicability truth.

PayRun Admin Queue evaluation checks the operator action workbench. Leave Source Model does not evaluate the full queue; it checks whether leave readiness and missing-output warnings can be grounded in applicability/source evidence.

Movement Review evaluation checks payroll reasonableness and review evidence. Leave Source Model does not treat movement variance as leave applicability truth.

Comparison / Remediation evaluation checks governed comparison evidence and policy-driven assessment. Leave Source Model is not comparison/remediation, although missing applicability evidence can affect later review or remediation interpretation.

Tax / PAYG evaluation checks governed withholding evidence and status-honest tax explanation. Leave Source Model preserves a similar boundary: Minerva does not calculate leave applicability.

Deductions / Obligations evaluation checks governed deduction and recovery evidence. Leave Source Model does not evaluate deduction applicability, affordability, priority, obligations or negative net pay.

Retro / Replay evaluation checks governed historical correction and evidence replay. Leave Source Model does not prove retro/replay capability or dependency detection; it may only describe source/applicability evidence that future replay could need.

Payment Execution / Remittance evaluation checks governed downstream payment and remittance evidence. Leave Source Model does not prove bank file generation, remittance reconciliation, payment close or payment execution readiness.

Finalisation Readiness evaluation checks the governed readiness gate for PayRun finalisation. Leave Source Model supplies leave applicability/source evidence that Finalisation Readiness may consume when deciding whether missing leave output is a blocker, warning, no-entitlement outcome or corpus/runtime unknown.

All evaluations use deterministic retrieval and benchmark checks. Worker Story, Payroll Bases & Totals, PayRun Admin Queue, Movement Review, Comparison / Remediation, Tax / PAYG, Deductions / Obligations, Retro / Replay, Payment Execution / Remittance, Leave Accrual / Processing, Finalisation Readiness, and Leave Source Model additionally have corpus coverage diagnostics and answer gap reports that classify evidence readiness group by group.

## Commands

Run commands from the repository root.

### Full Pytest Suite

```powershell
.\.venv\Scripts\python.exe -m pytest --basetemp .\.pytest_tmp
```

This is the main regression gate. It should pass before treating any benchmark or diagnostic output as meaningful.

### Leave Source Model Benchmark

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.leave_source_model.json
```

The benchmark includes the broad question, "What is the Leave Source Model and why does it matter?", plus focused follow-up questions about LeaveTypeRule not being final applicability truth, applicability versus rule content, no entitlement versus missing leave output, contact versus appointment scope, source dimensions and precedence, leave accrual, leave request payment effects, Worker Story, Command Centre and Finalisation Readiness.

### Corpus Coverage Diagnostic

```powershell
.\.venv\Scripts\python.exe scripts\scan_leave_source_model_corpus_coverage.py
.\.venv\Scripts\python.exe scripts\scan_leave_source_model_corpus_coverage.py --json --output .\artifacts\eval\leave_source_model_corpus_coverage.json
```

The diagnostic reads the already indexed formal corpus and reports coverage for each Leave Source Model evidence group. It does not ingest files, mutate corpus records, call a live LLM, or change schema.

### Answer Gap Report

```powershell
.\.venv\Scripts\python.exe scripts\build_leave_source_model_answer_gap_report.py --coverage-report .\artifacts\eval\leave_source_model_corpus_coverage.json
.\.venv\Scripts\python.exe scripts\build_leave_source_model_answer_gap_report.py --coverage-report .\artifacts\eval\leave_source_model_corpus_coverage.json --json --output .\artifacts\eval\leave_source_model_answer_gap_report.json
```

The gap report consumes the coverage diagnostic JSON and recommends the next action for each evidence group.

## Interpreting Benchmark Results

Benchmark results are deterministic regression checks over the loaded Minerva corpus.

- `PASS` means the question met its configured retrieval and answer checks.
- `FAIL` means at least one expected source, source phrase, answer phrase, section, or forbidden-pattern check did not pass.

A failure does not automatically mean answer synthesis is wrong. Common causes are:

- the loaded corpus does not contain enough formal evidence;
- retrieval terms do not find the relevant formal evidence;
- synthesis found evidence but did not express the expected Leave Source Model wording;
- the benchmark expectation no longer matches the intended product-domain wording.

Investigate failures from the returned source references, failed checks, coverage diagnostic, and answer gap report before changing code.

## Interpreting Coverage Status

The coverage diagnostic classifies each Leave Source Model evidence group:

- `STRONG`: multiple relevant chunks or documents were found. The corpus likely has enough retrievable evidence for the group.
- `WEAK`: some relevant evidence was found, but coverage is thin. Answers may be incomplete or overly dependent on one source.
- `MISSING`: no useful evidence was found for the group. Minerva should treat that part of the answer as corpus-limited.

Coverage status is about available formal corpus evidence, not runtime Leave Source Model truth. A `MISSING` group may mean the product concept exists but the indexed formal evidence is not loaded or not discoverable yet.

## Interpreting Gap Report Status

The answer gap report summarizes whether Leave Source Model answers are ready enough to keep, refine, or defer.

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
- not proof of runtime Leave Source Model truth;
- not proof that Minerva calculates leave applicability;
- not proof that Leave Source Model is fully implemented;
- not proof that LeaveTypeRule alone is final applicability truth;
- not proof that every active LeaveTypeRule means every worker should have leave output;
- not proof that missing leave output is always wrong.

Leave Source Model evaluation must continue to use the indexed formal knowledge corpus. It must not read or ingest source-code content as Minerva answer evidence, and it must not connect Code Evidence Index to answer generation.
