# Imports / Actuals Evaluation Runbook

This runbook documents the repeatable Minerva evaluation workflow for Imports / Actuals. It is intended for regression checks and corpus-readiness diagnostics after retrieval-plan, benchmark, synthesis, diagnostic tooling, or formal corpus changes.

The workflow is diagnostic-only. It does not mutate corpus records, change database schema, ingest operational JSON, call a live LLM, or connect Code Evidence Index to answer generation.

## Purpose

Imports / Actuals evaluation checks whether Minerva can retrieve and synthesize enough formal evidence to answer product-domain questions about governed imported evidence and external outcome truth. It focuses on imported timesheets, imported payroll actuals, source-system mapping, actuals as an external outcome lane, ObjectTime/source truth, comparison/remediation connections, reconciliation, Movement Review, Worker Story, Admin Queue, evidence provenance and audit.

The evaluation answers four practical questions:

- Does the full test suite still pass?
- Does the broad Imports / Actuals benchmark still pass?
- Do the 10 focused follow-up benchmark questions still pass?
- Does the currently indexed formal corpus contain enough evidence for each Imports / Actuals evidence group?

Imported actuals are external outcome truth, not calculated interpreter truth. Imported timesheets can become source truth only after validation and mapping. Imports / Actuals evaluation is not proof of runtime import/actuals truth, not proof that imported source data is automatically correct, not proof that actuals lane, comparison-line, or import mapping models are fully implemented, not proof that unmapped actuals can be silently ignored, and not proof that Minerva validates imports or mutates mappings.

## Domain Retrieval Coverage

The Imports / Actuals domain retrieval plan is a deterministic evidence-gathering plan for questions about imported external evidence and actuals outcome truth. It splits broad and focused questions into targeted evidence groups and retrieves formal corpus chunks for each group.

The plan covers:

- purpose and operator meaning;
- imported timesheet source truth;
- imported payroll actuals lane;
- source-system mapping and validation;
- pay code / RateType mapping;
- position/classification mapping;
- ObjectTime/source truth connection;
- Comparison / Remediation connection;
- reconciliation and Movement Review connection;
- Worker Story and Admin Queue connection;
- evidence provenance and audit;
- outstanding hardening.

The plan decides what evidence to search for. It does not validate imports, mutate mappings, prove imported source data is correct, convert imported actuals into calculated interpreter output, silently ignore unmapped actuals, prove runtime comparison-line truth, or take ownership of Comparison / Remediation policy. If evidence is weak or missing, Minerva should report the corpus limitation instead of inventing a product claim.

## Difference From Other Evaluations

Annual Leave evaluation checks leave configuration, accrual, TAKEN leave, valuation, PayRun orchestration, Worker Story leave evidence, and outstanding leave hardening. Imports / Actuals does not evaluate leave balances or leave valuation; it evaluates imported external source and outcome evidence.

Worker Story evaluation checks the broader explanation surface for worker-level payroll outcomes. Imports / Actuals only checks Worker Story where import provenance, mapping issues, unmapped actuals, missing classifications and review actions should be surfaced.

Payroll Bases & Totals evaluation checks governed payroll basis evidence, current-effective truth, bucket readiness and stale PayrollBucketResult caveats. Imports / Actuals may supply imported source or actuals evidence that later informs comparison or review, but it does not evaluate governed payroll bucket totals.

PayRun Admin Queue evaluation checks the operator action workbench for blockers, warnings and ready actions. Imports / Actuals may create mapping or validation issues for Admin Queue surfacing, but it does not evaluate the full Admin Queue workflow.

Movement Review evaluation checks payroll reasonableness, variance and review-worthy movement. Imports / Actuals supplies imported actuals and source evidence that Movement Review can use to explain variance or review outcomes; imported source data is still not automatically correct.

Comparison / Remediation evaluation checks governed comparison evidence, comparison policy, lanes, variance and remediation. Imports / Actuals supplies external actuals lane evidence and mapping/provenance inputs. Comparison / Remediation keeps ownership of comparison-lane adjudication, comparator policy, variance generation and remediation decisions.

Tax / PAYG evaluation checks governed withholding evidence and status-honest tax explanation. Imports / Actuals is not tax calculation or withholding evidence; it may preserve imported external outcome evidence that must not be treated as calculated tax truth.

Deductions / Obligations evaluation checks governed deduction, obligation and recovery evidence. Imports / Actuals is not worker deduction or obligation recovery; it explains imported source rows, mappings and actuals evidence.

Retro / Replay evaluation checks governed historical correction and evidence replay. Imports / Actuals does not prove retro/replay capability, although imported source rows and actuals provenance can matter for later historical explanation.

Payment Execution / Remittance evaluation checks governed downstream payment and remittance evidence. Imports / Actuals does not execute payments or remittances; it explains imported source and actuals evidence that may be reconciled against outcomes.

Leave Accrual / Processing evaluation checks detailed leave accrual, payroll output, LeaveLedger, valuation, request/payment sequencing and processing readiness. Imports / Actuals does not calculate leave accrual; imported timesheets may become source truth for work evidence only after validation and mapping.

Finalisation Readiness evaluation checks the governed readiness gate for PayRun finalisation. Imports / Actuals may feed readiness through unresolved mapping, validation or actuals evidence, but it does not determine finalisation readiness.

Leave Source Model evaluation checks governed leave applicability and source truth. Imports / Actuals also cares about source truth, but for imported source rows, imported timesheets, ObjectTime/source truth and external actuals evidence rather than leave applicability.

On-costs / Employer Liabilities evaluation checks employer-side liability evidence, super, payroll tax, WorkCover / WIC, governed bases and state/worksite/runtime location resolution. Imports / Actuals is external imported evidence and actuals outcome truth, not employer liability calculation evidence.

Award Build / Award Evidence evaluation checks upstream award/pay guide interpretation, RateType/AwardRateType creation, RateSource evidence, DecisionEvidenceIndex and RateSourceEvidenceIndex. Imports / Actuals consumes or maps external source-system evidence; it does not build award configuration or prove award evidence completeness.

All evaluations use deterministic retrieval and benchmark checks. Worker Story, Payroll Bases & Totals, PayRun Admin Queue, Movement Review, Comparison / Remediation, Tax / PAYG, Deductions / Obligations, Retro / Replay, Payment Execution / Remittance, Leave Accrual / Processing, Finalisation Readiness, Leave Source Model, On-costs / Employer Liabilities, Award Build / Award Evidence, and Imports / Actuals additionally have corpus coverage diagnostics and answer gap reports that classify evidence readiness group by group.

## Commands

Run commands from the repository root.

### Full Pytest Suite

```powershell
.\.venv\Scripts\python.exe -m pytest --basetemp .\.pytest_tmp
```

This is the main regression gate. It should pass before treating any benchmark or diagnostic output as meaningful.

### Imports / Actuals Benchmark

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.imports_actuals.json
```

The benchmark includes the broad question, "How should Imports and Actuals work in Ezeas?", plus focused follow-up questions about imported actuals as external outcome truth, imported timesheets and source truth, source-system mapping, pay code / RateType mapping, position/classification mapping, ObjectTime/source truth, Comparison / Remediation relationships, reconciliation and Movement Review, Worker Story and Admin Queue surfacing, and evidence provenance and audit.

### Corpus Coverage Diagnostic

```powershell
.\.venv\Scripts\python.exe scripts\scan_imports_actuals_corpus_coverage.py
.\.venv\Scripts\python.exe scripts\scan_imports_actuals_corpus_coverage.py --json --output .\artifacts\eval\imports_actuals_corpus_coverage.json
```

The diagnostic reads the already indexed formal corpus and reports coverage for each Imports / Actuals evidence group. It does not ingest files, mutate corpus records, call a live LLM, or change schema.

### Answer Gap Report

```powershell
.\.venv\Scripts\python.exe scripts\build_imports_actuals_answer_gap_report.py --coverage-report .\artifacts\eval\imports_actuals_corpus_coverage.json
.\.venv\Scripts\python.exe scripts\build_imports_actuals_answer_gap_report.py --coverage-report .\artifacts\eval\imports_actuals_corpus_coverage.json --json --output .\artifacts\eval\imports_actuals_answer_gap_report.json
```

The gap report consumes the coverage diagnostic JSON and recommends the next action for each evidence group.

## Interpreting Benchmark Results

Benchmark results are deterministic regression checks over the loaded Minerva corpus.

- `PASS` means the question met its configured retrieval and answer checks.
- `FAIL` means at least one expected source, source phrase, answer phrase, section, or forbidden-pattern check did not pass.

A failure does not automatically mean answer synthesis is wrong. Common causes are:

- the loaded corpus does not contain enough formal evidence;
- retrieval terms do not find the relevant formal evidence;
- synthesis found evidence but did not express the expected Imports / Actuals wording;
- the benchmark expectation no longer matches the intended product-domain wording.

Investigate failures from the returned source references, failed checks, coverage diagnostic, and answer gap report before changing code.

## Interpreting Coverage Status

The coverage diagnostic classifies each Imports / Actuals evidence group:

- `STRONG`: multiple relevant chunks or documents were found. The corpus likely has enough retrievable evidence for the group.
- `WEAK`: some relevant evidence was found, but coverage is thin. Answers may be incomplete or overly dependent on one source.
- `MISSING`: no useful evidence was found for the group. Minerva should treat that part of the answer as corpus-limited.

Coverage status is about available formal corpus evidence, not runtime import/actuals truth. A `MISSING` group may mean the product concept exists but the indexed formal evidence is not loaded or not discoverable yet.

## Interpreting Gap Report Status

The answer gap report summarizes whether Imports / Actuals answers are ready enough to keep, refine, or defer.

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
- not proof of runtime import/actuals truth;
- not proof that imported actuals are calculated interpreter truth;
- not proof that imported source data is automatically correct;
- not proof that actuals lane, comparison-line, or import mapping models are fully implemented;
- not proof that unmapped actuals can be silently ignored;
- not proof that Minerva validates imports or mutates mappings.

Imports / Actuals evaluation must continue to use the indexed formal knowledge corpus. It must not read or ingest source-code content as Minerva answer evidence, and it must not connect Code Evidence Index to answer generation.
