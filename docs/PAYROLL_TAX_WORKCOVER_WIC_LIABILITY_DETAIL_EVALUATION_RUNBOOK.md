# Payroll Tax / WorkCover / WIC Liability Detail Evaluation Runbook

This runbook documents the repeatable Minerva evaluation workflow for Payroll Tax / WorkCover / WIC Liability Detail. It is intended for regression checks and corpus-readiness diagnostics after retrieval-plan, benchmark, synthesis, diagnostic tooling, or formal corpus changes.

The workflow is diagnostic-only. It does not mutate corpus records, change database schema, ingest operational JSON, call a live LLM, read source-code content as Minerva evidence, or connect Code Evidence Index to answer generation. It also provides no Code Evidence answer integration and is not proof of runtime operational truth.

## Purpose

Payroll Tax / WorkCover / WIC Liability Detail is the Minerva product-domain explaining employer-side statutory/liability evidence for payroll tax, WorkCover and WIC; jurisdiction/worksite/state context; governed payroll basis membership; liability rate/source evidence; relationship to Payroll Bases, Payroll Output, Worker Story, Gross-to-Net boundaries and Finalisation Readiness.

The evaluation answers four practical questions:

- Does the full test suite still pass?
- Does the Payroll Tax / WorkCover / WIC Liability Detail broad and focused rich-answer benchmark still pass?
- Do payroll-tax/workcover/wic-liability-framed questions still route to the Payroll Tax / WorkCover / WIC Liability Detail domain while overlapping domains keep ownership?
- Does the currently indexed formal corpus contain enough evidence for each Payroll Tax / WorkCover / WIC Liability Detail evidence group?

Payroll Tax / WorkCover / WIC Liability Detail evaluation is not proof of runtime liability calculation, statutory lodgement, payroll output or finalisation behavior. It evaluates Minerva retrieval and answer quality over formal knowledge evidence. Minerva explains Payroll Tax / WorkCover / WIC liability evidence. Minerva does not calculate payroll tax, calculate WorkCover or WIC liability, lodge or remit statutory returns, decide statutory liability, change employer-liability configuration, change Worksite / State / jurisdiction truth, calculate payroll, mutate payroll output, determine finalisation readiness, finalise PayRuns, or mutate operational workforce/payroll/liability truth.

Explicit Minerva boundary:

- Minerva explains Payroll Tax / WorkCover / WIC liability evidence.
- Minerva does not calculate payroll tax.
- Minerva does not calculate WorkCover or WIC liability.
- Minerva does not lodge or remit statutory returns.
- Minerva does not decide statutory liability.
- Minerva does not change employer-liability configuration.
- Minerva does not change Worksite / State / jurisdiction truth.
- Minerva does not calculate payroll.
- Minerva does not mutate payroll output.
- Minerva does not determine finalisation readiness.
- Minerva does not finalise PayRuns.
- Minerva does not mutate operational workforce/payroll/liability truth.

## Domain Retrieval Coverage

The Payroll Tax / WorkCover / WIC Liability Detail domain retrieval plan is a deterministic evidence-gathering plan for questions about employer-side payroll tax, WorkCover, WIC and workers-compensation-style liability detail. It splits broad and focused questions into targeted evidence groups and retrieves formal corpus chunks for each group.

The v0.3 corpus coverage diagnostic covers:

- `liability_scope_and_employer_side_boundary`;
- `jurisdiction_worksite_and_state_context`;
- `governed_basis_membership_and_payroll_bases`;
- `rates_sources_and_liability_evidence`;
- `worker_story_output_and_finalisation_relationship`;
- `minerva_boundaries_and_non_mutation_guardrails`.

The domain covers employer-side liability boundaries, PAYG and worker net pay separation, Worksite.StateId, WorksitePosition, EmployeeAppointment, runtime location and ObjectTime location context where supported, governed basis membership, payroll bucket evidence, taxable wages, liability wages, included or excluded RateTypes and AwardRateTypes, Payroll Bases & Totals, RateSource and date-effective liability-rate evidence, account/state/award scoping, demo fallback versus production truth, Worker Story, Payroll Output, Gross-to-Net boundaries, employer liability lines, audit evidence, Finalisation Readiness, Admin Queue, Worker Attention, NEEDS_CONFIGURATION-style concepts and Minerva non-mutation guardrails.

The plan decides what evidence to search for. It does not calculate payroll tax, calculate WorkCover or WIC liability, lodge or remit statutory returns, decide statutory liability, change employer-liability configuration, change Worksite / State / jurisdiction truth, calculate payroll, mutate payroll output, determine finalisation readiness, finalise PayRuns, prove operational correctness, or mutate workforce/payroll/liability truth. If evidence is weak or missing, Minerva should report the corpus limitation instead of inventing a product claim.

## Difference From Other Evaluations

On-costs / Employer Liabilities owns broad on-cost and employer-liability questions that are not asking for payroll tax, WorkCover or WIC detail. Payroll Tax / WorkCover / WIC Liability Detail is narrower and explains statutory/liability evidence for those specific liability families.

Tax / PAYG owns worker PAYG, withholding and tax declaration questions. Payroll Tax / WorkCover / WIC Liability Detail can explain why payroll tax is employer-side liability evidence, but it does not own PAYG withholding.

Payroll Bases & Totals owns generic payroll basis and bucket evidence questions. Payroll Tax / WorkCover / WIC Liability Detail can explain how governed basis membership affects taxable wages or liability wages when the question is liability-framed.

RateSource / Rate Story owns generic rate selection and rate evidence questions. Payroll Tax / WorkCover / WIC Liability Detail can explain liability RateSource or date-effective liability-rate evidence when the question is payroll-tax/workcover/wic-framed.

Payment Execution / Remittance, Gross-to-Net, Payroll Output, Worker Story, Finalisation Readiness, Public Holidays, ObjectTime / Source Truth, Contacts / Employee Appointments and Award Positions / Classifications keep ownership of their generic domains. Payroll Tax / WorkCover / WIC Liability Detail can explain relationships to those surfaces only when the question is employer-liability-detail-framed.

## Commands

Run commands from the repository root.

### Full Pytest Suite

```powershell
.\.venv\Scripts\python.exe -m pytest --basetemp .\.pytest_tmp
```

This is the main regression gate. It should pass before treating any benchmark or diagnostic output as meaningful.

### Payroll Tax / WorkCover / WIC Liability Detail Benchmark

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.payroll_tax_workcover_wic_liability_detail.json
```

The benchmark includes the broad question, "How do Payroll Tax, WorkCover and WIC liabilities work in the platform?", plus focused follow-up questions about PAYG / worker net pay boundaries, state and worksite context, Payroll Bases and governed basis membership, liability rates / RateSource evidence, Worker Story / Payroll Output evidence, and missing configuration surfacing.

### Focused Contract And Routing Tests

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_payroll_tax_workcover_wic_liability_detail_corpus_coverage.py tests\test_payroll_tax_workcover_wic_liability_detail_answer_gap_report.py tests\test_domain_retrieval_plans.py tests\test_rich_answer_contract.py --basetemp .\.pytest_tmp
```

Use this when touching Payroll Tax / WorkCover / WIC Liability Detail benchmark, routing, diagnostic, answer gap report or documentation behavior.

### Corpus Coverage Diagnostic

Human-readable mode:

```powershell
.\.venv\Scripts\python.exe scripts\scan_payroll_tax_workcover_wic_liability_detail_corpus_coverage.py
```

JSON mode:

```powershell
.\.venv\Scripts\python.exe scripts\scan_payroll_tax_workcover_wic_liability_detail_corpus_coverage.py --json
```

Write diagnostic JSON to a file:

```powershell
.\.venv\Scripts\python.exe scripts\scan_payroll_tax_workcover_wic_liability_detail_corpus_coverage.py --json --output .\artifacts\eval\payroll_tax_workcover_wic_liability_detail_corpus_coverage.json
```

The diagnostic reads the already indexed formal corpus and reports coverage for each Payroll Tax / WorkCover / WIC Liability Detail evidence group. It does not ingest files, mutate corpus records, call a live LLM, ingest operational JSON, connect Code Evidence to answer generation, or change schema.

### Answer Gap Report

Human-readable mode:

```powershell
.\.venv\Scripts\python.exe scripts\build_payroll_tax_workcover_wic_liability_detail_answer_gap_report.py --coverage-report .\artifacts\eval\payroll_tax_workcover_wic_liability_detail_corpus_coverage.json
```

JSON mode:

```powershell
.\.venv\Scripts\python.exe scripts\build_payroll_tax_workcover_wic_liability_detail_answer_gap_report.py --coverage-report .\artifacts\eval\payroll_tax_workcover_wic_liability_detail_corpus_coverage.json --json
```

Write answer gap report JSON to a file:

```powershell
.\.venv\Scripts\python.exe scripts\build_payroll_tax_workcover_wic_liability_detail_answer_gap_report.py --coverage-report .\artifacts\eval\payroll_tax_workcover_wic_liability_detail_corpus_coverage.json --json --output .\artifacts\eval\payroll_tax_workcover_wic_liability_detail_answer_gap_report.json
```

The gap report consumes the coverage diagnostic JSON and recommends the next action for each evidence group.

## Interpreting Benchmark Results

Benchmark results are deterministic regression checks over the loaded Minerva corpus.

- `PASS` means the question met its configured retrieval and answer checks.
- `FAIL` means at least one expected source, source phrase, answer phrase, section, answer mode, routing, or forbidden-pattern check did not pass.

A failure does not automatically mean answer synthesis is wrong. Common causes are:

- the loaded corpus does not contain enough formal evidence;
- retrieval terms do not find the relevant formal evidence;
- synthesis found evidence but did not express the expected Payroll Tax / WorkCover / WIC Liability Detail wording;
- another domain owns the question and the routing expectation needs review;
- the benchmark expectation no longer matches the intended product-domain wording.

Investigate failures from the returned source references, failed checks, coverage diagnostic, and answer gap report before changing code.

## Interpreting Coverage Status

The coverage diagnostic classifies each Payroll Tax / WorkCover / WIC Liability Detail evidence group:

- `STRONG`: multiple relevant chunks or documents were found. The corpus likely has enough retrievable evidence for the group.
- `WEAK`: some relevant evidence was found, but coverage is thin. Answers may be incomplete or overly dependent on one source.
- `MISSING`: no useful evidence was found for the group. Minerva should treat that part of the answer as corpus-limited.

Coverage status is about available formal corpus evidence, not runtime payroll tax, WorkCover, WIC, payroll output, statutory lodgement or finalisation truth. A `MISSING` group may mean the product concept exists but the indexed formal evidence is not loaded or not discoverable yet.

## Interpreting Gap Report Status

The answer gap report summarizes whether Payroll Tax / WorkCover / WIC Liability Detail answers are ready enough to keep, refine, or defer.

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

## When To Improve What

- Improve retrieval terms when formal evidence exists but diagnostic coverage is `WEAK` because the scanner is not finding enough relevant corpus support.
- Improve synthesis when coverage is `STRONG` but benchmark or human review shows the answer is incomplete, too broad, or missing required Payroll Tax / WorkCover / WIC Liability Detail guardrails.
- Add formal source evidence later when the group is genuinely `MISSING` from the indexed formal corpus.
- Keep existing behavior where coverage and answer quality are acceptable.
- Do not use operational JSON or Code Evidence as a shortcut for missing formal source evidence.

## Guardrails

This workflow must remain:

- diagnostic-only;
- no corpus mutation;
- no live LLM calls;
- no database schema change;
- no operational JSON ingestion;
- no Code Evidence answer integration;
- no Code Evidence Index answer integration;
- not proof of runtime liability calculation or statutory lodgement;
- not proof of runtime operational truth;
- diagnostics do not mutate corpus;
- diagnostics do not call a live LLM;
- diagnostics do not ingest operational JSON;
- diagnostics do not connect Code Evidence to answer generation;
- diagnostics do not prove runtime operational truth;
- diagnostics do not calculate payroll tax;
- diagnostics do not calculate WorkCover or WIC liability;
- diagnostics do not lodge or remit statutory returns;
- diagnostics do not decide statutory liability;
- diagnostics do not change employer-liability configuration;
- diagnostics do not change Worksite / State / jurisdiction truth;
- diagnostics do not calculate payroll;
- diagnostics do not mutate payroll output;
- diagnostics do not determine or finalise readiness;
- diagnostics do not mutate operational workforce/payroll/liability truth.

Diagnostics do not calculate, lodge, remit, decide, change, mutate, determine readiness or finalise anything. Minerva does not calculate payroll tax, calculate WorkCover or WIC liability, lodge or remit statutory returns, decide statutory liability, change employer-liability configuration, change Worksite / State / jurisdiction truth, calculate payroll, mutate payroll output, determine finalisation readiness, finalise PayRuns or mutate operational workforce/payroll/liability truth. Payroll Tax / WorkCover / WIC Liability Detail evaluation must continue to use the indexed formal knowledge corpus. It must not read or ingest source-code content as Minerva answer evidence, and it must not connect Code Evidence Index to answer generation.
