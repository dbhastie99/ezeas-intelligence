# Payment Execution / Remittance Evaluation Runbook

This runbook documents the repeatable Minerva evaluation workflow for Payment Execution / Remittance. It is intended for regression checks and corpus-readiness diagnostics after retrieval-plan, benchmark, synthesis, or formal corpus changes.

The workflow is diagnostic-only. It does not mutate corpus records, change database schema, ingest operational JSON, call a live LLM, or connect Code Evidence Index to answer generation.

## Purpose

Payment Execution / Remittance evaluation checks whether Minerva can retrieve and synthesize enough formal evidence to answer product-domain questions about governed downstream payment/remittance action, finalised gross-to-net source evidence, worker net pay, bank allocation, payment destination readiness, negative net pay handling, obligations, deduction and third-party remittance, Generate Bank File, Period Close, remittance batching, remittance reconciliation, Worker Attention, PayRun Admin Queue, Worker Story, audit evidence, and outstanding hardening.

The evaluation answers four practical questions:

- Does the full test suite still pass?
- Does the broad Payment Execution / Remittance benchmark still pass?
- Do the focused follow-up benchmark questions still pass?
- Does the currently indexed formal corpus contain enough evidence for each Payment Execution / Remittance evidence group?

Payment Execution / Remittance evaluation is not proof of runtime payment execution/remittance truth. It evaluates Minerva retrieval and answer quality over formal knowledge evidence. It is also not proof that payment execution/remittance is complete, gross-to-net readiness equals payment execution readiness, missing bank/payment destination invalidates gross-to-net, bank file generation is implemented, remittance reconciliation/payment close is complete, negative net pay handling is solved, or obligation write-off financial consequences are implemented.

## Domain Retrieval Coverage

The Payment Execution / Remittance domain retrieval plan is a deterministic evidence-gathering plan for questions about governed payment execution and remittance evidence. It splits broad and focused questions into targeted evidence groups and retrieves formal corpus chunks for each group.

The plan covers:

- purpose and operator meaning;
- finalised gross-to-net source evidence;
- worker net pay and bank allocation;
- payment destination readiness;
- negative net pay and obligation interaction;
- deduction and third-party remittance;
- payment file generation and Period Close;
- remittance batching and reconciliation;
- Worker Attention and Admin Queue connection;
- Worker Story and audit evidence;
- outstanding hardening.

The plan decides what evidence to search for. It does not calculate payroll, execute payments, generate live bank files, remit deductions, reconcile remittance batches, close periods, mutate finalised outcomes, prove runtime payment execution/remittance truth, or infer missing implementation status. If evidence is weak or missing, Minerva should report the corpus limitation instead of inventing a product claim.

## Difference From Other Evaluations

Annual Leave evaluation checks a leave-management product slice: configuration, accrual, TAKEN leave, valuation, PayRun orchestration, Worker Story leave evidence, and outstanding leave hardening.

Worker Story evaluation checks a broader explanation and evidence slice around how payroll outcomes are shown to an operator or worker. It focuses on source truth, calculated payroll output, decision/rate evidence, current-effective truth, and related review/admin surfaces.

Payroll Bases & Totals evaluation checks a governed payroll basis evidence slice. It preserves the distinction between basis evidence and reporting or analytics totals, checks current-effective truth and stale PayrollBucketResult caveats, and verifies relationship evidence for Worker Story and Movement Review.

PayRun Admin Queue evaluation checks the operator action workbench for blockers, warnings, ready actions, worker attention, dirty contacts, finalisation readiness, Assurance Snapshot, review navigation and outstanding hardening. It preserves the distinction between Admin Queue and Command Centre, and it preserves the rule that queue cleanliness is not assurance.

Movement Review evaluation checks payroll reasonableness and review evidence. It preserves the doctrine that variance is not automatic proof of error and that not every movement creates a fix action. It also checks organisation and worker lenses, comparable period evidence, trend-only / rolling / YTD treatment, and relationships to Payroll Bases & Totals, Worker Story and PayRun Admin Queue.

Comparison / Remediation evaluation checks governed comparison evidence and policy-driven assessment. It preserves the three-lane model of primary calculated, comparator calculated and actual imported evidence; protects the primary ObjectTime -> EmployeeAppointment -> AwardPositionClass path as operational payroll truth; treats actuals as external outcome truth; requires comparison evidence before variance; and requires governed comparator classification mapping.

Tax / PAYG evaluation checks governed withholding evidence and status-honest tax explanation. It preserves the boundary that deterministic services and tax providers remain the calculation path, that Minerva does not calculate tax, that TaxStory should explain the withholding evidence path, that taxable basis must be governed, and that unsupported frequencies must be explicit rather than silently calculated.

Deductions / Obligations evaluation checks governed gross-to-net deduction and future recovery evidence. It preserves the boundary that deductions are governed application outcomes, not automatic raw net-pay subtraction; that the deduction template chain is LibraryDeductionTemplate -> AccountDeductionTemplate -> ContactPayrollDeduction -> PayRunDeductionApplication; that PayRunDeductionApplication is event/outcome memory; that applicability before affordability matters; that obligations are durable balance-bearing recovery records; and that negative net pay is a governed policy outcome.

Retro / Replay evaluation checks governed historical correction and evidence replay. It preserves the boundary that attributed-period truth and paid-period truth stay distinct, finalised outcomes are historical payment truth, current-effective truth is not historical/finalised truth, source/config changes should create dependency detection or dirty replay candidates rather than hidden recalculation, retro PayRuns and supplementary PayRuns are not the same, and Movement Review variance does not automatically prove retro error.

Payment Execution / Remittance evaluation checks governed downstream payment and remittance evidence. It preserves the boundary that payment execution is not payroll calculation truth, that finalised gross-to-net/payment outcome is consumed rather than recalculated, that gross-to-net readiness is not payment execution readiness, that missing payment destination can block payment execution without invalidating gross-to-net, that Generate Bank File and Period Close are governed execution rather than generic export, and that remittance reconciliation, payment close, negative net pay handling and obligation write-off financial consequences remain status-honest.

All ten evaluations use deterministic retrieval and benchmark checks. Worker Story, Payroll Bases & Totals, PayRun Admin Queue, Movement Review, Comparison / Remediation, Tax / PAYG, Deductions / Obligations, Retro / Replay, and Payment Execution / Remittance additionally have corpus coverage diagnostics and answer gap reports that classify evidence readiness group by group.

## Commands

Run commands from the repository root.

### Full Pytest Suite

```powershell
.\.venv\Scripts\python.exe -m pytest --basetemp .\.pytest_tmp
```

This is the main regression gate. It should pass before treating any benchmark or diagnostic output as meaningful.

### Payment Execution / Remittance Benchmark

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.payment_execution_remittance.json
```

The benchmark includes the broad question, "How should Payment Execution and Remittance work in Ezeas?", plus focused follow-up questions about payment execution versus payroll calculation, finalised gross-to-net source evidence, worker net pay and bank allocation, missing payment destinations, negative net pay and obligations, deduction and third-party remittance, Generate Bank File / Period Close, remittance batching and reconciliation, and Worker Attention / Admin Queue / Worker Story relationships.

### Corpus Coverage Diagnostic

```powershell
.\.venv\Scripts\python.exe scripts\scan_payment_execution_remittance_corpus_coverage.py
.\.venv\Scripts\python.exe scripts\scan_payment_execution_remittance_corpus_coverage.py --json --output .\artifacts\eval\payment_execution_remittance_corpus_coverage.json
```

The diagnostic reads the already indexed formal corpus and reports coverage for each Payment Execution / Remittance evidence group. It does not ingest files, mutate corpus records, call a live LLM, or change schema.

### Answer Gap Report

```powershell
.\.venv\Scripts\python.exe scripts\build_payment_execution_remittance_answer_gap_report.py --coverage-report .\artifacts\eval\payment_execution_remittance_corpus_coverage.json
.\.venv\Scripts\python.exe scripts\build_payment_execution_remittance_answer_gap_report.py --coverage-report .\artifacts\eval\payment_execution_remittance_corpus_coverage.json --json --output .\artifacts\eval\payment_execution_remittance_answer_gap_report.json
```

The gap report consumes the coverage diagnostic JSON and recommends the next action for each evidence group.

## Interpreting Benchmark Results

Benchmark results are deterministic regression checks over the loaded Minerva corpus.

- `PASS` means the question met its configured retrieval and answer checks.
- `FAIL` means at least one expected source, source phrase, answer phrase, section, or forbidden-pattern check did not pass.

A failure does not automatically mean answer synthesis is wrong. Common causes are:

- the loaded corpus does not contain enough formal evidence;
- retrieval terms do not find the relevant formal evidence;
- synthesis found evidence but did not express the expected Payment Execution / Remittance wording;
- the benchmark expectation no longer matches the intended product-domain wording.

Investigate failures from the returned source references, failed checks, coverage diagnostic, and answer gap report before changing code.

## Interpreting Coverage Status

The coverage diagnostic classifies each Payment Execution / Remittance evidence group:

- `STRONG`: multiple relevant chunks or documents were found. The corpus likely has enough retrievable evidence for the group.
- `WEAK`: some relevant evidence was found, but coverage is thin. Answers may be incomplete or overly dependent on one source.
- `MISSING`: no useful evidence was found for the group. Minerva should treat that part of the answer as corpus-limited.

Coverage status is about available formal corpus evidence, not runtime payment execution/remittance truth. A `MISSING` group may mean the product concept exists but the indexed formal evidence is not loaded or not discoverable yet.

## Interpreting Gap Report Status

The answer gap report summarizes whether Payment Execution / Remittance answers are ready enough to keep, refine, or defer.

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
- not proof of runtime payment execution/remittance truth;
- not proof that payment execution/remittance is complete;
- not proof that gross-to-net readiness equals payment execution readiness;
- not proof that missing bank/payment destination invalidates gross-to-net;
- not proof that bank file generation is implemented;
- not proof that remittance reconciliation/payment close is complete;
- not proof that negative net pay handling is solved;
- not proof that obligation write-off financial consequences are implemented.

Payment Execution / Remittance evaluation must continue to use the indexed formal knowledge corpus. It must not read or ingest source-code content as Minerva answer evidence, and it must not connect Code Evidence Index to answer generation.
