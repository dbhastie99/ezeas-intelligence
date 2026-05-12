# Costing / GL Consequence Evidence Evaluation Runbook

This runbook documents the repeatable Minerva evaluation workflow for Costing / GL Consequence Evidence. It is intended for regression checks and corpus-readiness diagnostics after retrieval-plan, benchmark, synthesis, diagnostic tooling, or formal corpus changes.

The workflow is diagnostic-only. It does not mutate corpus records, change database schema, ingest operational JSON, call a live LLM, read source-code content as Minerva evidence, or connect Code Evidence Index to answer generation.

## Purpose

Costing / GL Consequence Evidence evaluation checks whether Minerva can retrieve and synthesize enough formal evidence to answer product-domain questions about downstream financial consequence evidence. It focuses on financial consequences that may flow from finalised payroll outcome truth, payment execution, employer liabilities / on-costs, deduction obligations, obligation write-off handling, remediation variance, leave valuation, negative net pay, audit story, financial evidence and deferred/final costing slice boundaries.

The evaluation answers four practical questions:

- Does the full test suite still pass?
- Does the broad Costing / GL Consequence Evidence benchmark still pass?
- Do the 10 focused follow-up benchmark questions still pass?
- Does the currently indexed formal corpus contain enough evidence for each Costing / GL Consequence Evidence evidence group?

Costing / GL Consequence Evidence evaluation is not proof of runtime costing/GL truth. It evaluates Minerva retrieval and answer quality over formal knowledge evidence. It is not proof that costing is implemented, that Minerva posts GL entries or calculates costing, that costing should block payroll payment/close performance, that obligation write-offs have no financial consequence, that remediation variance downstream treatment is complete, or that negative net pay financial treatment is solved.

## Domain Retrieval Coverage

The Costing / GL Consequence domain retrieval plan is a deterministic evidence-gathering plan for questions about downstream financial consequence evidence. It splits broad and focused questions into targeted evidence groups and retrieves formal corpus chunks for each group.

The plan covers:

- purpose and operator meaning;
- downstream financial consequence evidence, not payroll calculation truth;
- finalised payroll outcome truth and finalised gross-to-net/payment/liability source outcomes;
- Payment Execution / Remittance connection;
- employer liabilities / on-costs connection;
- deduction obligations, obligation write-off or writeoff consequences, forgiveness, balance reduction and material adjustment;
- Comparison / Remediation remediation variance and variance line downstream treatment;
- leave valuation and leave accrual connection;
- negative net pay and out-of-pay consequences;
- audit story and financial evidence, including source outcome, reason, treatment, amount, ledger status, costing status and deferred accounting design status;
- deferred/final costing slice boundary;
- outstanding hardening.

The plan decides what evidence to search for. It does not post GL entries, calculate costing, prove runtime accounting truth, execute payments, calculate payroll, calculate employer liabilities, calculate leave valuation, resolve remediation downstream treatment, mutate obligation balances, or replace deterministic Ezeas services. If evidence is weak or missing, Minerva should report the corpus limitation instead of inventing a product claim.

## Difference From Other Evaluations

Payment Execution / Remittance evaluation owns bank files, payment allocation, worker net pay, third-party remittance, remittance reconciliation and payment execution readiness. Costing / GL Consequence Evidence can explain that payment execution and remittance outcomes may create financial consequence evidence, but it does not execute payments or prove payment execution truth.

On-costs / Employer Liabilities evaluation owns governed employer liability evidence, RateSource/date-effective rates, AwardRateType settings, governed basis membership, super, payroll tax and WorkCover / WIC liability differences. Costing / GL Consequence Evidence can explain downstream costing or GL consequences from employer liabilities / on-costs, but it does not calculate those liabilities.

Deductions / Obligations evaluation owns deduction applicability, affordability, PayRunDeductionApplication, obligation balances, recoveries and obligation state. Costing / GL Consequence Evidence only evaluates whether deduction obligations, write-offs, forgiveness, balance reduction and material adjustment may have financial consequence treatment.

Comparison / Remediation evaluation owns comparison evidence before variance, remediation policy, comparator classification and variance-line assessment. Costing / GL Consequence Evidence can explain downstream treatment of remediation variance or variance line evidence, but it must not claim that remediation variance downstream treatment is complete unless formal evidence says so.

Leave Accrual / Processing evaluation owns leave accrual, TAKEN leave valuation, LeaveLedger movement, request/payment sequencing and leave readiness. Costing / GL Consequence Evidence can explain that leave valuation and accrual evidence may eventually flow to costing, but it does not calculate leave or prove leave valuation completeness.

Finalisation Readiness evaluation owns readiness gates, blockers, warnings, current-effective payroll output and finalisation safety. Costing / GL Consequence Evidence can consume finalised payroll outcome truth and explain downstream consequence evidence, but it must not make costing a payroll-processing blocker.

Retro / Replay evaluation owns attributed-period truth, paid-period truth, current-effective versus historical truth, finalised outcome memory and governed replay. Costing / GL Consequence Evidence can explain downstream financial consequences from finalised or remediated outcomes, but it does not prove retro/replay implementation.

Payroll Bases & Totals, Tax / PAYG, Worker Story, PayRun Admin Queue, Movement Review, Imports / Actuals, ObjectTime / Source Truth, Contacts / Employee Appointments, Award Build / Award Evidence and other evaluations own their specific evidence and runtime boundaries. Costing / GL Consequence Evidence is downstream financial consequence evidence; it is not a generic replacement for those domains and not payroll calculation truth.

All evaluations use deterministic retrieval and benchmark checks. Costing / GL Consequence Evidence additionally has corpus coverage diagnostics and an answer gap report that classify evidence readiness group by group.

## Commands

Run commands from the repository root.

### Full Pytest Suite

```powershell
.\.venv\Scripts\python.exe -m pytest --basetemp .\.pytest_tmp
```

This is the main regression gate. It should pass before treating any benchmark or diagnostic output as meaningful.

### Costing / GL Consequence Evidence Benchmark

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.costing_gl_consequence.json
```

The benchmark includes the broad question, "How should Costing and GL Consequence Evidence work in Ezeas?", plus focused follow-up questions about downstream payroll-calculation boundaries, finalised payroll outcome truth, Payment Execution / Remittance, employer liabilities / on-costs, deduction obligations and write-offs, Comparison / Remediation variance lines, leave valuation and accrual, negative net pay and out-of-pay treatment, audit story and deferred/final costing slice boundaries.

### Corpus Coverage Diagnostic

```powershell
.\.venv\Scripts\python.exe scripts\scan_costing_gl_consequence_corpus_coverage.py
.\.venv\Scripts\python.exe scripts\scan_costing_gl_consequence_corpus_coverage.py --json --output .\artifacts\eval\costing_gl_consequence_corpus_coverage.json
```

The diagnostic reads the already indexed formal corpus and reports coverage for each Costing / GL Consequence Evidence evidence group. It does not ingest files, mutate corpus records, call a live LLM, or change schema.

### Answer Gap Report

```powershell
.\.venv\Scripts\python.exe scripts\build_costing_gl_consequence_answer_gap_report.py --coverage-report .\artifacts\eval\costing_gl_consequence_corpus_coverage.json
.\.venv\Scripts\python.exe scripts\build_costing_gl_consequence_answer_gap_report.py --coverage-report .\artifacts\eval\costing_gl_consequence_corpus_coverage.json --json --output .\artifacts\eval\costing_gl_consequence_answer_gap_report.json
```

The gap report consumes the coverage diagnostic JSON and recommends the next action for each evidence group.

## Interpreting Benchmark Results

Benchmark results are deterministic regression checks over the loaded Minerva corpus.

- `PASS` means the question met its configured retrieval and answer checks.
- `FAIL` means at least one expected source, source phrase, answer phrase, section, or forbidden-pattern check did not pass.

A failure does not automatically mean answer synthesis is wrong. Common causes are:

- the loaded corpus does not contain enough formal evidence;
- retrieval terms do not find the relevant formal evidence;
- synthesis found evidence but did not express the expected Costing / GL Consequence Evidence wording;
- another domain owns the question and the routing expectation needs review;
- the benchmark expectation no longer matches the intended product-domain wording.

Investigate failures from the returned source references, failed checks, coverage diagnostic, and answer gap report before changing code.

## Interpreting Coverage Status

The coverage diagnostic classifies each Costing / GL Consequence Evidence evidence group:

- `STRONG`: multiple relevant chunks or documents were found. The corpus likely has enough retrievable evidence for the group.
- `WEAK`: some relevant evidence was found, but coverage is thin. Answers may be incomplete or overly dependent on one source.
- `MISSING`: no useful evidence was found for the group. Minerva should treat that part of the answer as corpus-limited.

Coverage status is about available formal corpus evidence, not runtime costing/GL truth. A `MISSING` group may mean the product concept exists but the indexed formal evidence is not loaded or not discoverable yet.

## Interpreting Gap Report Status

The answer gap report summarizes whether Costing / GL Consequence Evidence answers are ready enough to keep, refine, or defer.

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
- not proof of runtime costing/GL truth;
- not proof that costing is implemented;
- not proof that Minerva posts GL entries or calculates costing;
- not proof that costing should block payroll payment/close performance;
- not proof that obligation write-offs have no financial consequence;
- not proof that remediation variance downstream treatment is complete;
- not proof that negative net pay financial treatment is solved.

Costing / GL Consequence Evidence evaluation must continue to use the indexed formal knowledge corpus. It must not read or ingest source-code content as Minerva answer evidence, and it must not connect Code Evidence Index to answer generation.
