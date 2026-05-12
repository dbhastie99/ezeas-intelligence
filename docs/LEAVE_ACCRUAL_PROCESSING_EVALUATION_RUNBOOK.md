# Leave Accrual / Processing Evaluation Runbook

This runbook documents the repeatable Minerva evaluation workflow for Leave Accrual / Processing. It is intended for regression checks and corpus-readiness diagnostics after retrieval-plan, benchmark, synthesis, or formal corpus changes.

The workflow is diagnostic-only. It does not mutate corpus records, change database schema, ingest operational JSON, call a live LLM, or connect Code Evidence Index to answer generation.

## Purpose

Leave Accrual / Processing evaluation checks whether Minerva can retrieve and synthesize enough formal evidence to answer product-domain questions about detailed leave accrual and leave processing. It focuses on deterministic platform outcomes, leave source truth, applicability, accrual basis and quantity, CalcInterpreterLine/current-effective payroll output, LeaveType and LeaveTypeRule configuration, LeaveLedger movement evidence, leave valuation basis, TAKEN leave valuation hard-fail/no silent fallback posture, leave request payment effects, PayRun processing, finalisation readiness, Worker Story, Payroll Bases & Totals, and outstanding hardening.

The evaluation answers four practical questions:

- Does the full test suite still pass?
- Does the broad Leave Accrual / Processing benchmark still pass?
- Do the focused follow-up benchmark questions still pass?
- Does the currently indexed formal corpus contain enough evidence for each Leave Accrual / Processing evidence group?

Leave Accrual / Processing evaluation is not proof of runtime leave accrual/processing truth. It evaluates Minerva retrieval and answer quality over formal knowledge evidence. Minerva does not calculate leave. The evaluation is also not proof that the Leave Source Model is complete, all leave types are fully implemented, LeaveTypeRule alone is final applicability truth, TAKEN leave can post without valuation, or leave-processing UI/runs are complete.

## Domain Retrieval Coverage

The Leave Accrual / Processing domain retrieval plan is a deterministic evidence-gathering plan for detailed leave accrual and leave processing questions. It splits broad and focused questions into targeted evidence groups and retrieves formal corpus chunks for each group.

The plan covers:

- purpose and operator meaning;
- leave source truth and applicability;
- accrual basis and quantity;
- payroll output and CalcInterpreterLine/current-effective payroll output source evidence;
- LeaveType and LeaveTypeRule configuration;
- LeaveLedger accrual, payment and balance movement evidence;
- leave valuation basis;
- leave request payment effects;
- PayRun processing and finalisation readiness;
- Worker Story connection;
- Payroll Bases & Totals connection;
- outstanding hardening.

The plan decides what evidence to search for. It does not calculate leave, infer source truth that is not in the formal corpus, complete the Leave Source Model, post LeaveLedger rows, run leave processing, finalise PayRuns, mutate payroll history, prove runtime leave accrual/processing truth, or infer missing implementation status. If evidence is weak or missing, Minerva should report the corpus limitation instead of inventing a product claim.

## Difference From Other Evaluations

Annual Leave overview evaluation checks the broader leave-management slice: configuration, accrual, TAKEN leave, valuation, PayRun orchestration, Worker Story leave evidence, and outstanding leave hardening. Leave Accrual / Processing is narrower and deeper: it evaluates detailed accrual source truth, applicability, CalcInterpreterLine/current-effective payroll output, LeaveLedger movement evidence, valuation hard-fail posture, processing sequencing, and finalisation readiness.

Worker Story evaluation checks a broader explanation and evidence slice around how payroll outcomes are shown to an operator or worker. Leave Accrual / Processing only checks Worker Story where it must explain Leave and Accrual Outcome using server-owned leave output, ledger and valuation evidence.

Payroll Bases & Totals evaluation checks governed payroll basis evidence, current-effective truth, bucket readiness and stale PayrollBucketResult caveats. Leave Accrual / Processing only checks Payroll Bases & Totals where basis evidence, worked hours or leave basis quantities support leave accrual explanation.

PayRun Admin Queue evaluation checks the operator action workbench for blockers, warnings, ready actions, worker attention, dirty contacts, finalisation readiness, Assurance Snapshot, review navigation and outstanding hardening. Leave Accrual / Processing only checks PayRun processing and finalisation readiness for leave output, leave readiness and warning acknowledgement.

Movement Review evaluation checks payroll reasonableness and review evidence. It preserves the doctrine that variance is not automatic proof of error. Leave Accrual / Processing does not treat movement variance as leave accrual truth.

Comparison / Remediation evaluation checks governed comparison evidence and policy-driven assessment. It preserves the three-lane model of primary calculated, comparator calculated and actual imported evidence. Leave Accrual / Processing is not comparison or remediation evidence.

Tax / PAYG evaluation checks governed withholding evidence and status-honest tax explanation. It preserves the boundary that Minerva does not calculate tax. Leave Accrual / Processing preserves the parallel boundary that Minerva does not calculate leave.

Deductions / Obligations evaluation checks governed gross-to-net deduction and future recovery evidence. Leave Accrual / Processing does not evaluate deduction affordability, priority, obligations, reducing-balance recovery or negative net pay policy.

Retro / Replay evaluation checks governed historical correction and evidence replay. Leave Accrual / Processing does not prove retro/replay capability, dependency detection, or governed historical bucket rebuilds.

Payment Execution / Remittance evaluation checks governed downstream payment and remittance evidence. Leave Accrual / Processing does not prove bank file generation, remittance reconciliation, payment close, or payment execution readiness.

All evaluations use deterministic retrieval and benchmark checks. Worker Story, Payroll Bases & Totals, PayRun Admin Queue, Movement Review, Comparison / Remediation, Tax / PAYG, Deductions / Obligations, Retro / Replay, Payment Execution / Remittance, and Leave Accrual / Processing additionally have corpus coverage diagnostics and answer gap reports that classify evidence readiness group by group.

## Commands

Run commands from the repository root.

### Full Pytest Suite

```powershell
.\.venv\Scripts\python.exe -m pytest --basetemp .\.pytest_tmp
```

This is the main regression gate. It should pass before treating any benchmark or diagnostic output as meaningful.

### Leave Accrual / Processing Benchmark

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.leave_accrual_processing.json
```

The benchmark includes the broad question, "How does leave accrue and get processed in Ezeas?", plus focused follow-up questions about Minerva not calculating leave accrual, source truth, CalcInterpreterLine/current-effective payroll output, LeaveType and LeaveTypeRule, applicability, LeaveLedger, TAKEN leave valuation hard-fail/no silent fallback, leave request payment effects, Worker Story, Payroll Bases & Totals, and PayRun finalisation readiness.

### Corpus Coverage Diagnostic

```powershell
.\.venv\Scripts\python.exe scripts\scan_leave_accrual_processing_corpus_coverage.py
.\.venv\Scripts\python.exe scripts\scan_leave_accrual_processing_corpus_coverage.py --json --output .\artifacts\eval\leave_accrual_processing_corpus_coverage.json
```

The diagnostic reads the already indexed formal corpus and reports coverage for each Leave Accrual / Processing evidence group. It does not ingest files, mutate corpus records, call a live LLM, or change schema.

### Answer Gap Report

```powershell
.\.venv\Scripts\python.exe scripts\build_leave_accrual_processing_answer_gap_report.py --coverage-report .\artifacts\eval\leave_accrual_processing_corpus_coverage.json
.\.venv\Scripts\python.exe scripts\build_leave_accrual_processing_answer_gap_report.py --coverage-report .\artifacts\eval\leave_accrual_processing_corpus_coverage.json --json --output .\artifacts\eval\leave_accrual_processing_answer_gap_report.json
```

The gap report consumes the coverage diagnostic JSON and recommends the next action for each evidence group.

## Interpreting Benchmark Results

Benchmark results are deterministic regression checks over the loaded Minerva corpus.

- `PASS` means the question met its configured retrieval and answer checks.
- `FAIL` means at least one expected source, source phrase, answer phrase, section, or forbidden-pattern check did not pass.

A failure does not automatically mean answer synthesis is wrong. Common causes are:

- the loaded corpus does not contain enough formal evidence;
- retrieval terms do not find the relevant formal evidence;
- synthesis found evidence but did not express the expected Leave Accrual / Processing wording;
- the benchmark expectation no longer matches the intended product-domain wording.

Investigate failures from the returned source references, failed checks, coverage diagnostic, and answer gap report before changing code.

## Interpreting Coverage Status

The coverage diagnostic classifies each Leave Accrual / Processing evidence group:

- `STRONG`: multiple relevant chunks or documents were found. The corpus likely has enough retrievable evidence for the group.
- `WEAK`: some relevant evidence was found, but coverage is thin. Answers may be incomplete or overly dependent on one source.
- `MISSING`: no useful evidence was found for the group. Minerva should treat that part of the answer as corpus-limited.

Coverage status is about available formal corpus evidence, not runtime leave accrual/processing truth. A `MISSING` group may mean the product concept exists but the indexed formal evidence is not loaded or not discoverable yet.

## Interpreting Gap Report Status

The answer gap report summarizes whether Leave Accrual / Processing answers are ready enough to keep, refine, or defer.

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
- not proof of runtime leave accrual/processing truth;
- not proof that Minerva calculates leave;
- not proof that the Leave Source Model is complete;
- not proof that all leave types are fully implemented;
- not proof that LeaveTypeRule alone is final applicability truth;
- not proof that TAKEN leave can post without valuation;
- not proof that leave-processing UI/runs are complete.

Leave Accrual / Processing evaluation must continue to use the indexed formal knowledge corpus. It must not read or ingest source-code content as Minerva answer evidence, and it must not connect Code Evidence Index to answer generation.
