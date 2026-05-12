# Finalisation Readiness Evaluation Runbook

This runbook documents the repeatable Minerva evaluation workflow for Finalisation Readiness. It is intended for regression checks and corpus-readiness diagnostics after retrieval-plan, benchmark, synthesis, or formal corpus changes.

The workflow is diagnostic-only. It does not mutate corpus records, change database schema, ingest operational JSON, call a live LLM, or connect Code Evidence Index to answer generation.

## Purpose

Finalisation Readiness evaluation checks whether Minerva can retrieve and synthesize enough formal evidence to answer product-domain questions about the governed readiness and assurance gate for PayRun finalisation. It focuses on blockers, warnings and green readiness, current-effective payroll output, Worker Attention, PayRun Admin Queue, Payroll Bases readiness, leave readiness, tax/deduction/payment readiness, payment execution and bank readiness, finalised outcome truth, warning acknowledgement and audit evidence, Worker Story, review surfaces, and outstanding hardening.

The evaluation answers four practical questions:

- Does the full test suite still pass?
- Does the broad Finalisation Readiness benchmark still pass?
- Do the 11 focused follow-up benchmark questions still pass?
- Does the currently indexed formal corpus contain enough evidence for each Finalisation Readiness evidence group?

Finalisation Readiness evaluation is not proof of runtime finalisation readiness truth. It evaluates Minerva retrieval and answer quality over formal knowledge evidence. Minerva does not determine readiness, and Finalisation Readiness does not calculate payroll. Amber warnings must not be silent or ignored. The evaluation is also not proof that amber warnings can be ignored, green readiness means no review-worthy movement exists, payment execution readiness equals gross-to-net readiness, or warning acknowledgement/finalisation policy is complete.

## Domain Retrieval Coverage

The Finalisation Readiness domain retrieval plan is a deterministic evidence-gathering plan for finalisation readiness questions. It splits broad and focused questions into targeted evidence groups and retrieves formal corpus chunks for each group.

The plan covers:

- purpose and operator meaning;
- blockers, warnings and green readiness;
- current-effective payroll output;
- Worker Attention and PayRun Admin Queue;
- Payroll Bases readiness;
- leave readiness;
- tax, deduction and payment readiness;
- payment execution and bank readiness;
- finalised outcome truth;
- warning acknowledgement and audit evidence;
- Worker Story and review surfaces;
- outstanding hardening.

The plan decides what evidence to search for. It does not determine readiness, calculate payroll, acknowledge warnings, finalise PayRuns, prove payment execution readiness, mutate payroll history, prove runtime finalisation readiness truth, or infer missing implementation status. If evidence is weak or missing, Minerva should report the corpus limitation instead of inventing a product claim.

## Difference From Other Evaluations

Annual Leave overview evaluation checks the broader leave-management slice. Finalisation Readiness only checks leave where missing leave output or leave valuation basis affects finalisation readiness evidence.

Worker Story evaluation checks a broader explanation slice for worker-level payroll outcomes. Finalisation Readiness only checks Worker Story where it must explain readiness evidence, blockers, warnings, and worker-specific issues.

Payroll Bases & Totals evaluation checks governed payroll basis evidence, current-effective truth, bucket readiness and stale PayrollBucketResult caveats. Finalisation Readiness checks Payroll Bases readiness only where unresolved or stale basis evidence can affect finalisation.

PayRun Admin Queue evaluation checks the operator action workbench. Finalisation Readiness uses Admin Queue and Worker Attention as readiness surfaces, but it is the governed finalisation gate rather than the whole queue experience.

Movement Review evaluation checks payroll reasonableness and review evidence. It preserves the doctrine that variance is not automatic proof of error. Finalisation Readiness does not treat movement variance as readiness truth by itself.

Comparison / Remediation evaluation checks governed comparison evidence and policy-driven assessment. Finalisation Readiness is not comparison/remediation, although unresolved comparison evidence may become a readiness concern where policy requires review.

Tax / PAYG evaluation checks governed withholding evidence and status-honest tax explanation. Finalisation Readiness only checks tax readiness as one readiness dimension and does not imply Minerva calculates tax.

Deductions / Obligations evaluation checks governed deduction and recovery evidence. Finalisation Readiness only checks deduction readiness, negative net pay and related payment readiness where they affect finalisation or downstream execution.

Retro / Replay evaluation checks governed historical correction and evidence replay. Finalisation Readiness does not prove retro/replay capability or dependency detection; it may only surface readiness issues from stale or superseded output.

Payment Execution / Remittance evaluation checks governed downstream payment and remittance evidence. Finalisation Readiness preserves that payment execution readiness is different from gross-to-net readiness.

Leave Accrual / Processing evaluation checks detailed leave accrual and leave processing evidence. Finalisation Readiness only consumes leave readiness evidence; it does not calculate leave or prove leave-processing UI/runs are complete.

All evaluations use deterministic retrieval and benchmark checks. Worker Story, Payroll Bases & Totals, PayRun Admin Queue, Movement Review, Comparison / Remediation, Tax / PAYG, Deductions / Obligations, Retro / Replay, Payment Execution / Remittance, Leave Accrual / Processing, and Finalisation Readiness additionally have corpus coverage diagnostics and answer gap reports that classify evidence readiness group by group.

## Commands

Run commands from the repository root.

### Full Pytest Suite

```powershell
.\.venv\Scripts\python.exe -m pytest --basetemp .\.pytest_tmp
```

This is the main regression gate. It should pass before treating any benchmark or diagnostic output as meaningful.

### Finalisation Readiness Benchmark

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.finalisation_readiness.json
```

The benchmark includes the broad question, "How should Finalisation Readiness work in Ezeas?", plus focused follow-up questions about Minerva not determining readiness, blockers/warnings/green readiness, current-effective payroll output, Worker Attention, PayRun Admin Queue, Payroll Bases readiness, leave readiness, tax/deduction/payment readiness, payment execution readiness versus gross-to-net readiness, finalised outcome truth, warning acknowledgement, audit evidence, Worker Story, and review surfaces.

### Corpus Coverage Diagnostic

```powershell
.\.venv\Scripts\python.exe scripts\scan_finalisation_readiness_corpus_coverage.py
.\.venv\Scripts\python.exe scripts\scan_finalisation_readiness_corpus_coverage.py --json --output .\artifacts\eval\finalisation_readiness_corpus_coverage.json
```

The diagnostic reads the already indexed formal corpus and reports coverage for each Finalisation Readiness evidence group. It does not ingest files, mutate corpus records, call a live LLM, or change schema.

### Answer Gap Report

```powershell
.\.venv\Scripts\python.exe scripts\build_finalisation_readiness_answer_gap_report.py --coverage-report .\artifacts\eval\finalisation_readiness_corpus_coverage.json
.\.venv\Scripts\python.exe scripts\build_finalisation_readiness_answer_gap_report.py --coverage-report .\artifacts\eval\finalisation_readiness_corpus_coverage.json --json --output .\artifacts\eval\finalisation_readiness_answer_gap_report.json
```

The gap report consumes the coverage diagnostic JSON and recommends the next action for each evidence group.

## Interpreting Benchmark Results

Benchmark results are deterministic regression checks over the loaded Minerva corpus.

- `PASS` means the question met its configured retrieval and answer checks.
- `FAIL` means at least one expected source, source phrase, answer phrase, section, or forbidden-pattern check did not pass.

A failure does not automatically mean answer synthesis is wrong. Common causes are:

- the loaded corpus does not contain enough formal evidence;
- retrieval terms do not find the relevant formal evidence;
- synthesis found evidence but did not express the expected Finalisation Readiness wording;
- the benchmark expectation no longer matches the intended product-domain wording.

Investigate failures from the returned source references, failed checks, coverage diagnostic, and answer gap report before changing code.

## Interpreting Coverage Status

The coverage diagnostic classifies each Finalisation Readiness evidence group:

- `STRONG`: multiple relevant chunks or documents were found. The corpus likely has enough retrievable evidence for the group.
- `WEAK`: some relevant evidence was found, but coverage is thin. Answers may be incomplete or overly dependent on one source.
- `MISSING`: no useful evidence was found for the group. Minerva should treat that part of the answer as corpus-limited.

Coverage status is about available formal corpus evidence, not runtime finalisation readiness truth. A `MISSING` group may mean the product concept exists but the indexed formal evidence is not loaded or not discoverable yet.

## Interpreting Gap Report Status

The answer gap report summarizes whether Finalisation Readiness answers are ready enough to keep, refine, or defer.

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
- not proof of runtime finalisation readiness truth;
- not proof that Minerva determines readiness;
- not proof that finalisation readiness calculates payroll;
- not proof that amber warnings can be ignored;
- not proof that green readiness means no review-worthy movement exists;
- not proof that payment execution readiness equals gross-to-net readiness;
- not proof that warning acknowledgement/finalisation policy is complete.

Finalisation Readiness evaluation must continue to use the indexed formal knowledge corpus. It must not read or ingest source-code content as Minerva answer evidence, and it must not connect Code Evidence Index to answer generation.
