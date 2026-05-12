# Gross-to-Net Evaluation Runbook

This runbook documents the repeatable Minerva evaluation workflow for Gross-to-Net. It is intended for regression checks and corpus-readiness diagnostics after retrieval-plan, benchmark, synthesis, diagnostic tooling, or formal corpus changes.

The workflow is diagnostic-only. It does not mutate corpus records, change database schema, ingest operational JSON, call a live LLM, read source-code content as Minerva evidence, or connect Code Evidence Index to answer generation. It also provides no Code Evidence answer integration.

## Purpose

Gross-to-Net evaluation checks whether Minerva can retrieve and synthesize enough formal evidence to answer product-domain questions about the payroll outcome calculation and explanation surface that connects gross earnings, taxable basis, PAYG / withholding, deductions, obligations, negative net pay, net pay, payment allocation, Worker Story, current-effective payroll output and finalised payroll outcome evidence.

The evaluation answers four practical questions:

- Does the full test suite still pass?
- Does the broad Gross-to-Net benchmark still pass?
- Do the focused follow-up benchmark questions still pass?
- Does the currently indexed formal corpus contain enough evidence for each Gross-to-Net evidence group?

Gross-to-Net evaluation is not proof of runtime Gross-to-Net implementation. It evaluates Minerva retrieval and answer quality over formal knowledge evidence. It is not proof that Minerva calculates gross-to-net, withholds tax, applies deductions, approves or resolves negative net pay, generates payment files, finalises PayRuns or mutates payroll truth. It is also not proof that Gross-to-Net alone proves payroll correctness.

## Domain Retrieval Coverage

The Gross-to-Net domain retrieval plan is a deterministic evidence-gathering plan for questions about payroll outcome explanation from gross earnings to net pay. It splits broad and focused questions into targeted evidence groups and retrieves formal corpus chunks for each group.

The plan covers:

- Gross-to-Net purpose and operator meaning;
- gross earnings and payroll output evidence;
- taxable basis, taxable earnings, PAYG and withholding context;
- TaxStory or tax evidence where supported by corpus evidence;
- deductions, obligations, reducing-balance recovery and deduction application effects;
- negative net pay, carry-forward, recovery, obligation conversion, write-off and out-of-pay treatment where supported by corpus evidence;
- net pay, worker net pay, payment allocation and payment execution readiness boundaries;
- Worker Story relationship and calculated payroll outcome explanation;
- finalisation and payment execution relationship;
- current-effective payroll output truth, stale output and superseded output;
- outstanding hardening.

The plan decides what evidence to search for. It does not calculate gross-to-net, withhold tax, apply deductions, approve negative net pay, generate payments, finalise PayRuns, mutate payroll truth, prove runtime payroll correctness, or replace deterministic Ezeas services. If evidence is weak or missing, Minerva should report the corpus limitation instead of inventing a product claim.

## Difference From Other Evaluations

Tax / PAYG evaluation owns governed withholding evidence, taxable basis alignment, worker tax declarations, TaxStory, PaymentDate where tax context matters and deterministic tax provider/service boundaries. Gross-to-Net can explain how PAYG / withholding affects net pay, but it does not calculate withholding and does not replace Tax / PAYG ownership.

Deductions / Obligations evaluation owns deduction applicability, affordability, priority, PayRunDeductionApplication memory, obligations, reducing-balance recovery, carry-forward, unmet deduction story and write-off policy. Gross-to-Net can explain how deductions and obligations affect net pay, but it does not apply deductions or decide obligation treatment.

Payment Execution / Remittance evaluation owns payment files, payment destinations, bank allocation, third-party remittance, remittance reconciliation and payment execution readiness. Gross-to-Net can explain net pay and payment allocation readiness, but payment execution and Gross-to-Net are not the same surface.

Worker Attention / Issue Resolution evaluation owns worker-level blockers, warnings, readiness gaps and deterministic fix links. Gross-to-Net can explain that negative net pay, payment allocation, deductions, tax or current-effective output issues may surface through Worker Attention, but it does not resolve issues or clear blockers.

Payroll Bases & Totals evaluation owns basis evidence, bucket membership, gross/ordinary/superable/taxable basis evidence and basis readiness. Gross-to-Net can consume or refer to taxable basis and Payroll Bases relationship, but basis evidence remains owned by Payroll Bases & Totals.

Worker Story evaluation owns worker evidence, narrative context, calculated payroll outcome, line proof, amounts, deductions, net pay and audit story. Gross-to-Net should be explainable through Worker Story, but Worker Story remains the broader worker evidence surface.

Finalisation Readiness evaluation owns readiness gates, blockers, warnings, current-effective output and finalisation safety. Gross-to-Net can contribute readiness evidence, but it does not finalise PayRuns or prove finalisation readiness.

PayRun Admin Queue evaluation owns the operator workbench for what needs action now. Gross-to-Net issues may surface there, but Gross-to-Net is not the Admin Queue and does not mutate operational queue state.

All evaluations use deterministic retrieval and benchmark checks. Gross-to-Net additionally has corpus coverage diagnostics and an answer gap report that classify evidence readiness group by group.

## Commands

Run commands from the repository root.

### Full Pytest Suite

```powershell
.\.venv\Scripts\python.exe -m pytest --basetemp .\.pytest_tmp
```

This is the main regression gate. It should pass before treating any benchmark or diagnostic output as meaningful.

### Gross-to-Net Benchmark

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.gross_to_net.json
```

The benchmark includes the broad question, "What is Gross-to-Net in the platform?", plus focused follow-up questions about gross earnings to net pay flow, taxable basis and PAYG, deductions and obligations, negative net pay, current-effective payroll output and Worker Story.

### Corpus Coverage Diagnostic

```powershell
.\.venv\Scripts\python.exe scripts\scan_gross_to_net_corpus_coverage.py
.\.venv\Scripts\python.exe scripts\scan_gross_to_net_corpus_coverage.py --json --output .\artifacts\eval\gross_to_net_corpus_coverage.json
```

The diagnostic reads the already indexed formal corpus and reports coverage for each Gross-to-Net evidence group. It does not ingest files, mutate corpus records, call a live LLM, ingest operational JSON, connect Code Evidence to answer generation, or change schema.

### Answer Gap Report

```powershell
.\.venv\Scripts\python.exe scripts\build_gross_to_net_answer_gap_report.py --coverage-report .\artifacts\eval\gross_to_net_corpus_coverage.json
.\.venv\Scripts\python.exe scripts\build_gross_to_net_answer_gap_report.py --coverage-report .\artifacts\eval\gross_to_net_corpus_coverage.json --json --output .\artifacts\eval\gross_to_net_answer_gap_report.json
```

The gap report consumes the coverage diagnostic JSON and recommends the next action for each evidence group.

## Interpreting Benchmark Results

Benchmark results are deterministic regression checks over the loaded Minerva corpus.

- `PASS` means the question met its configured retrieval and answer checks.
- `FAIL` means at least one expected source, source phrase, answer phrase, section, or forbidden-pattern check did not pass.

A failure does not automatically mean answer synthesis is wrong. Common causes are:

- the loaded corpus does not contain enough formal evidence;
- retrieval terms do not find the relevant formal evidence;
- synthesis found evidence but did not express the expected Gross-to-Net wording;
- another domain owns the question and the routing expectation needs review;
- the benchmark expectation no longer matches the intended product-domain wording.

Investigate failures from the returned source references, failed checks, coverage diagnostic, and answer gap report before changing code.

## Interpreting Coverage Status

The coverage diagnostic classifies each Gross-to-Net evidence group:

- `STRONG`: multiple relevant chunks or documents were found. The corpus likely has enough retrievable evidence for the group.
- `WEAK`: some relevant evidence was found, but coverage is thin. Answers may be incomplete or overly dependent on one source.
- `MISSING`: no useful evidence was found for the group. Minerva should treat that part of the answer as corpus-limited.

Coverage status is about available formal corpus evidence, not runtime Gross-to-Net implementation or operational payroll truth. A `MISSING` group may mean the product concept exists but the indexed formal evidence is not loaded or not discoverable yet.

## Interpreting Gap Report Status

The answer gap report summarizes whether Gross-to-Net answers are ready enough to keep, refine, or defer.

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
- no Code Evidence answer integration;
- no Code Evidence Index answer integration;
- not proof of runtime Gross-to-Net implementation;
- not proof that Minerva calculates gross-to-net;
- not proof that Minerva withholds tax;
- not proof that Minerva applies deductions;
- not proof that Minerva approves or resolves negative net pay;
- not proof that Minerva generates payment files;
- not proof that Minerva finalises PayRuns;
- not proof that Gross-to-Net alone proves payroll correctness.

Minerva does not calculate, withhold, apply deductions, approve, resolve, generate payment files, finalise or mutate payroll truth. Gross-to-Net evaluation must continue to use the indexed formal knowledge corpus. It must not read or ingest source-code content as Minerva answer evidence, and it must not connect Code Evidence Index to answer generation.
