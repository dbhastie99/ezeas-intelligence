# RateSource / Rate Story Evaluation Runbook

This runbook documents the repeatable Minerva evaluation workflow for RateSource / Rate Story. It is intended for regression checks and corpus-readiness diagnostics after retrieval-plan, benchmark, synthesis, diagnostic tooling, or formal corpus changes.

The workflow is diagnostic-only. It does not mutate corpus records, change database schema, ingest operational JSON, call a live LLM, read source-code content as Minerva evidence, or connect Code Evidence Index to answer generation. It also provides no Code Evidence answer integration.

## Purpose

RateSource / Rate Story evaluation checks whether Minerva can retrieve and synthesize enough formal evidence to answer product-domain questions about selected rate evidence, rate amount evidence, date-effective rates, award/account/class scope, pay guide evidence, RateSourceEvidenceIndex, and the boundary between Rate Story and Decision Story.

The evaluation answers four practical questions:

- Does the full test suite still pass?
- Does the broad RateSource / Rate Story benchmark still pass?
- Do the focused follow-up benchmark questions still pass?
- Does the currently indexed formal corpus contain enough evidence for each RateSource / Rate Story evidence group?

RateSource / Rate Story evaluation is not proof of runtime RateSource implementation. It evaluates Minerva retrieval and answer quality over formal knowledge evidence. It is not proof that Minerva selects rates, calculates pay, interprets awards at runtime, changes RateSource records, validates payroll correctness or mutates payroll truth. It is also not proof that RateSource evidence alone proves entitlement, pay guide evidence alone proves treatment entitlement, or Rate Story is the same as Decision Story.

## Domain Retrieval Coverage

The RateSource / Rate Story domain retrieval plan is a deterministic evidence-gathering plan for questions about which rate was used, where the amount came from, and how rate evidence is represented. It splits broad and focused questions into targeted evidence groups and retrieves formal corpus chunks for each group.

The plan covers:

- RateSource / Rate Story purpose and operator meaning;
- RateSource selection and selected rate evidence;
- rate amount evidence and amount provenance;
- date-effective rates and effective date context;
- award/account/class scope, RateType and AwardRateType context;
- pay guide evidence, including source row, column, page or source text where supported by corpus evidence;
- RateSourceEvidenceIndex / Rate Source Evidence Index;
- Rate Story versus Decision Story boundaries;
- Worker Story relationship and payroll line explanation;
- payroll output and Gross-to-Net relationship;
- outstanding hardening.

The plan decides what evidence to search for. It does not select rates, calculate pay, interpret awards at runtime, change RateSource records, validate payroll correctness, prove entitlement, or mutate payroll truth. If evidence is weak or missing, Minerva should report the corpus limitation instead of inventing a product claim.

## Difference From Other Evaluations

Decision Story evaluation owns why a treatment or payroll line exists, including entitlement and treatment-selection logic. RateSource / Rate Story owns why a selected rate or rate amount was used. Rate Story is not the same as Decision Story, and RateSource evidence alone does not prove entitlement.

Worker Story evaluation owns broader worker-level evidence, narrative context, calculated payroll outcome, line proof and audit story. Rate Story can appear inside Worker Story for a payroll line, but Worker Story remains the broader worker explanation surface.

Award Build / Award Evidence evaluation owns award source documents, pay guides, award-build configuration, RateType / AwardRateType setup, DecisionEvidenceIndex and durable award evidence. RateSource / Rate Story can explain rate evidence selected from those sources, but it does not own award-build source-document coverage or runtime award interpretation.

Gross-to-Net evaluation owns the payroll outcome explanation from gross earnings to net pay. RateSource / Rate Story can explain the rate or amount evidence behind output lines, but Gross-to-Net uses output lines and amounts and does not treat Rate Story as calculation authority.

Payroll Bases & Totals evaluation owns basis evidence, bucket membership and total/basis readiness. RateSource / Rate Story may mention rate evidence that contributes to output lines, but basis evidence remains owned by Payroll Bases & Totals.

Tax / PAYG evaluation owns governed withholding evidence, tax basis alignment, worker tax declarations, TaxStory and deterministic tax provider/service boundaries. If RateSource appears inside a tax-framed question, Tax / PAYG keeps ownership.

On-costs / Employer Liabilities evaluation owns employer-liability rates, date-effective liability evidence, super, payroll tax and WorkCover / WIC contexts. If RateSource appears inside an employer-liability context, On-costs / Employer Liabilities keeps ownership.

Payment Execution / Remittance evaluation owns payment files, payment destinations, remittance, bank allocation and payment execution readiness. RateSource / Rate Story does not generate payments and does not prove payment execution readiness.

All evaluations use deterministic retrieval and benchmark checks. RateSource / Rate Story additionally has corpus coverage diagnostics and an answer gap report that classify evidence readiness group by group.

## Commands

Run commands from the repository root.

### Full Pytest Suite

```powershell
.\.venv\Scripts\python.exe -m pytest --basetemp .\.pytest_tmp
```

This is the main regression gate. It should pass before treating any benchmark or diagnostic output as meaningful.

### RateSource / Rate Story Benchmark

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.rate_source_rate_story.json
```

The benchmark includes the broad question, "What is RateSource / Rate Story in the platform?", plus focused follow-up questions about RateSource selection, pay guide evidence, Rate Story versus Decision Story, date-effective and scoped rates, and the Worker Story / Gross-to-Net relationship.

### Corpus Coverage Diagnostic

```powershell
.\.venv\Scripts\python.exe scripts\scan_rate_source_rate_story_corpus_coverage.py
.\.venv\Scripts\python.exe scripts\scan_rate_source_rate_story_corpus_coverage.py --json --output .\artifacts\eval\rate_source_rate_story_corpus_coverage.json
```

The diagnostic reads the already indexed formal corpus and reports coverage for each RateSource / Rate Story evidence group. It does not ingest files, mutate corpus records, call a live LLM, ingest operational JSON, connect Code Evidence to answer generation, or change schema.

### Answer Gap Report

```powershell
.\.venv\Scripts\python.exe scripts\build_rate_source_rate_story_answer_gap_report.py --coverage-report .\artifacts\eval\rate_source_rate_story_corpus_coverage.json
.\.venv\Scripts\python.exe scripts\build_rate_source_rate_story_answer_gap_report.py --coverage-report .\artifacts\eval\rate_source_rate_story_corpus_coverage.json --json --output .\artifacts\eval\rate_source_rate_story_answer_gap_report.json
```

The gap report consumes the coverage diagnostic JSON and recommends the next action for each evidence group.

## Interpreting Benchmark Results

Benchmark results are deterministic regression checks over the loaded Minerva corpus.

- `PASS` means the question met its configured retrieval and answer checks.
- `FAIL` means at least one expected source, source phrase, answer phrase, section, or forbidden-pattern check did not pass.

A failure does not automatically mean answer synthesis is wrong. Common causes are:

- the loaded corpus does not contain enough formal evidence;
- retrieval terms do not find the relevant formal evidence;
- synthesis found evidence but did not express the expected RateSource / Rate Story wording;
- another domain owns the question and the routing expectation needs review;
- the benchmark expectation no longer matches the intended product-domain wording.

Investigate failures from the returned source references, failed checks, coverage diagnostic, and answer gap report before changing code.

## Interpreting Coverage Status

The coverage diagnostic classifies each RateSource / Rate Story evidence group:

- `STRONG`: multiple relevant chunks or documents were found. The corpus likely has enough retrievable evidence for the group.
- `WEAK`: some relevant evidence was found, but coverage is thin. Answers may be incomplete or overly dependent on one source.
- `MISSING`: no useful evidence was found for the group. Minerva should treat that part of the answer as corpus-limited.

Coverage status is about available formal corpus evidence, not runtime RateSource implementation or operational payroll truth. A `MISSING` group may mean the product concept exists but the indexed formal evidence is not loaded or not discoverable yet.

## Interpreting Gap Report Status

The answer gap report summarizes whether RateSource / Rate Story answers are ready enough to keep, refine, or defer.

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
- not proof of runtime RateSource implementation;
- not proof that Minerva selects rates;
- not proof that Minerva calculates pay;
- not proof that Minerva interprets awards at runtime;
- not proof that Minerva changes RateSource records;
- not proof that RateSource evidence alone proves entitlement;
- not proof that pay guide evidence alone proves treatment entitlement;
- not proof that Rate Story is the same as Decision Story;
- not proof that Minerva validates payroll correctness or mutates payroll truth.

Minerva does not select rates, calculate pay, interpret awards at runtime, change RateSource records, validate payroll correctness or mutate payroll truth. RateSource / Rate Story evaluation must continue to use the indexed formal knowledge corpus. It must not read or ingest source-code content as Minerva answer evidence, and it must not connect Code Evidence Index to answer generation.
