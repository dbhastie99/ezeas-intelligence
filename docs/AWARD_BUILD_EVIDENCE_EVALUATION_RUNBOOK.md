# Award Build / Award Evidence Evaluation Runbook

This runbook documents the repeatable Minerva evaluation workflow for Award Build / Award Evidence. It is intended for regression checks and corpus-readiness diagnostics after retrieval-plan, benchmark, synthesis, diagnostic tooling, or formal corpus changes.

The workflow is diagnostic-only. It does not mutate corpus records, change database schema, ingest operational JSON, call a live LLM, or connect Code Evidence Index to answer generation.

## Purpose

Award Build / Award Evidence evaluation checks whether Minerva can retrieve and synthesize enough formal evidence to answer product-domain questions about governed award configuration and evidence creation. It focuses on turning award documents and pay guides into traceable platform configuration and evidence, not runtime payroll calculation by Minerva.

The evaluation answers four practical questions:

- Does the full test suite still pass?
- Does the broad Award Build / Award Evidence benchmark still pass?
- Do the 11 focused follow-up benchmark questions still pass?
- Does the currently indexed formal corpus contain enough evidence for each Award Build / Award Evidence evidence group?

Award Build / Award Evidence is not runtime payroll calculation. Minerva does not interpret awards at runtime; it explains retrieved formal evidence and status. The evaluation is not proof of runtime award build truth, not proof that all awards/regimes are fully supported, not proof that Durable AwardEvidenceSet is complete, not proof that classification extraction is fully deterministic, not proof that every DecisionEvidenceIndex family has complete coverage, and not proof that rates may be hardcoded.

## Domain Retrieval Coverage

The Award Build / Award Evidence domain retrieval plan is a deterministic evidence-gathering plan for questions about governed award build evidence. It splits broad and focused questions into targeted evidence groups and retrieves formal corpus chunks for each group.

The plan covers:

- purpose and operator meaning;
- award documents and pay guides as source evidence;
- RateType and AwardRateType creation;
- RateSource and date-effective rate evidence;
- classification, position and class evidence;
- allowances, penalties and conditional rules;
- DecisionEvidenceIndex;
- RateSourceEvidenceIndex;
- Worker Story Decision Story and Rate Story connection;
- NEEDS_CONFIGURATION and build status;
- Durable AwardEvidenceSet;
- outstanding hardening.

The plan decides what evidence to search for. It does not interpret awards at runtime, calculate payroll, prove complete award/regime support, prove durable evidence storage is complete, prove classification extraction is fully deterministic, prove every decision family is covered, or replace RateSource with hardcoded rates. If evidence is weak or missing, Minerva should report the corpus limitation instead of inventing a product claim.

## Difference From Other Evaluations

Annual Leave evaluation checks leave configuration, accrual, TAKEN leave, valuation, PayRun orchestration, Worker Story leave evidence, and outstanding leave hardening. Award Build / Award Evidence is upstream of many payroll concepts; it evaluates award/pay guide source evidence and configuration creation rather than leave balances or leave valuation.

Worker Story evaluation checks the broader explanation surface for worker-level payroll outcomes. Award Build / Award Evidence only checks Worker Story where Decision Story and Rate Story should reuse award build/runtime evidence.

Payroll Bases & Totals evaluation checks governed payroll basis evidence, current-effective truth, bucket readiness and stale PayrollBucketResult caveats. Award Build / Award Evidence may create or evidence upstream rate and treatment configuration, but it does not evaluate payroll basis totals.

PayRun Admin Queue evaluation checks the operator action workbench for blockers, warnings and ready actions. Award Build / Award Evidence can produce NEEDS_CONFIGURATION status, but it does not evaluate the full Admin Queue workflow.

Movement Review evaluation checks payroll reasonableness, variance and review-worthy movement. Award Build / Award Evidence does not treat movement variance as proof of award interpretation or rate truth.

Comparison / Remediation evaluation checks governed comparison evidence and policy-driven assessment. Award Build / Award Evidence supplies source-backed configuration evidence that comparison or remediation may later rely on, but it is not a comparison workflow.

Tax / PAYG evaluation checks governed withholding evidence and status-honest tax explanation. Award Build / Award Evidence preserves a similar boundary: deterministic services and governed configuration produce outcomes, and Minerva does not calculate payroll.

Deductions / Obligations evaluation checks governed deduction, obligation and recovery evidence. Award Build / Award Evidence is not worker deduction or obligation recovery; it explains award/pay guide source evidence and award-scoped configuration.

Retro / Replay evaluation checks governed historical correction and evidence replay. Award Build / Award Evidence does not prove replay capability, although RateSource and date-effective rate evidence can matter for historical explanation.

Payment Execution / Remittance evaluation checks governed downstream payment and remittance evidence. Award Build / Award Evidence does not execute payments or remittances.

Leave Accrual / Processing evaluation checks detailed leave accrual, payroll output, LeaveLedger, valuation, request/payment sequencing and processing readiness. Award Build / Award Evidence does not calculate leave accrual; it focuses on award source material, rate/treatment setup and evidence.

Finalisation Readiness evaluation checks the governed readiness gate for PayRun finalisation. Award Build / Award Evidence may feed readiness through missing configuration or evidence, but it does not determine finalisation readiness.

Leave Source Model evaluation checks governed leave applicability and source truth. Award Build / Award Evidence also uses source truth, but for award documents, pay guides, classification, RateType, AwardRateType, RateSource, DecisionEvidenceIndex and RateSourceEvidenceIndex.

On-costs / Employer Liabilities evaluation checks employer-side liability evidence, super, payroll tax, WorkCover / WIC, governed bases and state/worksite/runtime location resolution. Award Build / Award Evidence is upstream award configuration/evidence creation and does not evaluate employer liability calculation evidence.

All evaluations use deterministic retrieval and benchmark checks. Worker Story, Payroll Bases & Totals, PayRun Admin Queue, Movement Review, Comparison / Remediation, Tax / PAYG, Deductions / Obligations, Retro / Replay, Payment Execution / Remittance, Leave Accrual / Processing, Finalisation Readiness, Leave Source Model, On-costs / Employer Liabilities, and Award Build / Award Evidence additionally have corpus coverage diagnostics and answer gap reports that classify evidence readiness group by group.

## Commands

Run commands from the repository root.

### Full Pytest Suite

```powershell
.\.venv\Scripts\python.exe -m pytest --basetemp .\.pytest_tmp
```

This is the main regression gate. It should pass before treating any benchmark or diagnostic output as meaningful.

### Award Build / Award Evidence Benchmark

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.award_build_evidence.json
```

The benchmark includes the broad question, "How should Award Build and Award Evidence work in Ezeas?", plus focused follow-up questions about why it is not runtime payroll calculation, award documents and pay guides as source evidence, RateType and AwardRateType, RateSource and date-effective rate evidence, classification/position/class evidence, allowances and penalties, DecisionEvidenceIndex, RateSourceEvidenceIndex, Worker Story Decision Story and Rate Story, NEEDS_CONFIGURATION, and Durable AwardEvidenceSet hardening.

### Corpus Coverage Diagnostic

```powershell
.\.venv\Scripts\python.exe scripts\scan_award_build_evidence_corpus_coverage.py
.\.venv\Scripts\python.exe scripts\scan_award_build_evidence_corpus_coverage.py --json --output .\artifacts\eval\award_build_evidence_corpus_coverage.json
```

The diagnostic reads the already indexed formal corpus and reports coverage for each Award Build / Award Evidence evidence group. It does not ingest files, mutate corpus records, call a live LLM, or change schema.

### Answer Gap Report

```powershell
.\.venv\Scripts\python.exe scripts\build_award_build_evidence_answer_gap_report.py --coverage-report .\artifacts\eval\award_build_evidence_corpus_coverage.json
.\.venv\Scripts\python.exe scripts\build_award_build_evidence_answer_gap_report.py --coverage-report .\artifacts\eval\award_build_evidence_corpus_coverage.json --json --output .\artifacts\eval\award_build_evidence_answer_gap_report.json
```

The gap report consumes the coverage diagnostic JSON and recommends the next action for each evidence group.

## Interpreting Benchmark Results

Benchmark results are deterministic regression checks over the loaded Minerva corpus.

- `PASS` means the question met its configured retrieval and answer checks.
- `FAIL` means at least one expected source, source phrase, answer phrase, section, or forbidden-pattern check did not pass.

A failure does not automatically mean answer synthesis is wrong. Common causes are:

- the loaded corpus does not contain enough formal evidence;
- retrieval terms do not find the relevant formal evidence;
- synthesis found evidence but did not express the expected Award Build / Award Evidence wording;
- the benchmark expectation no longer matches the intended product-domain wording.

Investigate failures from the returned source references, failed checks, coverage diagnostic, and answer gap report before changing code.

## Interpreting Coverage Status

The coverage diagnostic classifies each Award Build / Award Evidence evidence group:

- `STRONG`: multiple relevant chunks or documents were found. The corpus likely has enough retrievable evidence for the group.
- `WEAK`: some relevant evidence was found, but coverage is thin. Answers may be incomplete or overly dependent on one source.
- `MISSING`: no useful evidence was found for the group. Minerva should treat that part of the answer as corpus-limited.

Coverage status is about available formal corpus evidence, not runtime award build truth. A `MISSING` group may mean the product concept exists but the indexed formal evidence is not loaded or not discoverable yet.

## Interpreting Gap Report Status

The answer gap report summarizes whether Award Build / Award Evidence answers are ready enough to keep, refine, or defer.

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
- not proof of runtime award build truth;
- not proof that Minerva interprets awards at runtime;
- not proof that all awards/regimes are fully supported;
- not proof that Durable AwardEvidenceSet is complete;
- not proof that classification extraction is fully deterministic;
- not proof that every DecisionEvidenceIndex family has complete coverage;
- not proof that rates may be hardcoded.

Award Build / Award Evidence evaluation must continue to use the indexed formal knowledge corpus. It must not read or ingest source-code content as Minerva answer evidence, and it must not connect Code Evidence Index to answer generation.
