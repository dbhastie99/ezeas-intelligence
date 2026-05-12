# Decision Story Evaluation Runbook

This runbook documents the repeatable Minerva evaluation workflow for Decision Story. It is intended for regression checks and corpus-readiness diagnostics after retrieval-plan, benchmark, synthesis, diagnostic tooling, or formal corpus changes.

The workflow is diagnostic-only. It does not mutate corpus records, change database schema, ingest operational JSON, call a live LLM, read source-code content as Minerva evidence, or connect Code Evidence Index to answer generation. It also provides no Code Evidence answer integration.

## Purpose

Decision Story evaluation checks whether Minerva can retrieve and synthesize enough formal evidence to answer product-domain questions about why a payroll treatment, entitlement, payroll line, rule outcome, allowance, penalty, overtime, shift, public holiday, break treatment, special condition or other calculated payroll decision exists.

The evaluation answers four practical questions:

- Does the full test suite still pass?
- Does the broad Decision Story benchmark still pass?
- Do the focused follow-up benchmark questions still pass?
- Does the currently indexed formal corpus contain enough evidence for each Decision Story evidence group?

Decision Story evaluation is not proof of runtime Decision Story implementation. It evaluates Minerva retrieval and answer quality over formal knowledge evidence. It is not proof that Minerva selects treatments, decides entitlements, interprets awards at runtime, calculates payroll, changes decision evidence, validates payroll correctness or mutates payroll truth. It is also not proof that DecisionEvidenceIndex alone proves the full award-source chain or that Decision Story is the same as Rate Story.

## Domain Retrieval Coverage

The Decision Story domain retrieval plan is a deterministic evidence-gathering plan for questions about why a payroll treatment or line exists. It splits broad and focused questions into targeted evidence groups and retrieves formal corpus chunks for each group.

The plan covers:

- Decision Story purpose and operator meaning;
- treatment or entitlement selection;
- why a payroll line exists;
- DecisionEvidenceIndex / Decision Evidence Index;
- award rule evidence, configured rule evidence and runtime facts;
- award/source evidence where available;
- allowance, penalty, overtime and shift decision evidence;
- break treatment, missed break, public holiday treatment, special conditions and minimum engagement where supported by corpus evidence;
- Decision Story versus Rate Story boundaries;
- Worker Story relationship and payroll line explanation;
- payroll output and Gross-to-Net relationship;
- outstanding hardening.

The plan decides what evidence to search for. It does not select treatments, decide entitlements, interpret awards at runtime, calculate payroll, change decision evidence, validate payroll correctness, prove the full award-source chain, or mutate payroll truth. If evidence is weak or missing, Minerva should report the corpus limitation instead of inventing a product claim.

## Difference From Other Evaluations

RateSource / Rate Story evaluation owns why a selected rate, RateSource or rate amount was used. Decision Story owns why the treatment or payroll line exists. Decision Story is not the same as Rate Story, and RateSource evidence alone does not prove entitlement.

Worker Story evaluation owns broader worker-level evidence, narrative context, calculated payroll outcome, line proof and audit story. Decision Story can appear inside Worker Story for a payroll line, but Worker Story remains the broader worker explanation surface.

Award Build / Award Evidence evaluation owns award source documents, pay guides, award-build configuration, DecisionEvidenceIndex creation context, RateSourceEvidenceIndex and durable award evidence. Decision Story can explain runtime decision evidence selected from those sources, but it does not own award-build source-document coverage or runtime award interpretation.

Gross-to-Net evaluation owns the payroll outcome explanation from gross earnings to net pay. Decision Story can explain why a line or treatment exists, but Gross-to-Net consumes payroll output amounts and outcomes and does not treat Decision Story as net-pay calculation authority.

Payroll Bases & Totals evaluation owns basis evidence, bucket membership and total/basis readiness. Decision Story may explain why a payroll line exists, but basis evidence remains owned by Payroll Bases & Totals.

Leave Accrual / Processing evaluation owns leave calculation, leave processing, leave source/applicability, leave valuation, LeaveLedger and leave readiness evidence. Decision Story can explain a decision surface where formal evidence supports it, but leave calculation and processing remain owned by Leave Accrual / Processing.

Finalisation Readiness evaluation owns readiness gates, blockers, warnings, current-effective output and finalisation safety. Decision Story can contribute line-level explanation evidence, but it does not determine readiness or finalise PayRuns.

All evaluations use deterministic retrieval and benchmark checks. Decision Story additionally has corpus coverage diagnostics and an answer gap report that classify evidence readiness group by group.

## Commands

Run commands from the repository root.

### Full Pytest Suite

```powershell
.\.venv\Scripts\python.exe -m pytest --basetemp .\.pytest_tmp
```

This is the main regression gate. It should pass before treating any benchmark or diagnostic output as meaningful.

### Decision Story Benchmark

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.decision_story.json
```

The benchmark includes the broad question, "What is Decision Story in the platform?", plus focused follow-up questions about why a payroll line exists, DecisionEvidenceIndex, Decision Story versus Rate Story, allowance/penalty/overtime/shift decisions, break/public-holiday/special-condition decisions, and the Worker Story / Gross-to-Net relationship.

### Corpus Coverage Diagnostic

```powershell
.\.venv\Scripts\python.exe scripts\scan_decision_story_corpus_coverage.py
.\.venv\Scripts\python.exe scripts\scan_decision_story_corpus_coverage.py --json --output .\artifacts\eval\decision_story_corpus_coverage.json
```

The diagnostic reads the already indexed formal corpus and reports coverage for each Decision Story evidence group. It does not ingest files, mutate corpus records, call a live LLM, ingest operational JSON, connect Code Evidence to answer generation, or change schema.

### Answer Gap Report

```powershell
.\.venv\Scripts\python.exe scripts\build_decision_story_answer_gap_report.py --coverage-report .\artifacts\eval\decision_story_corpus_coverage.json
.\.venv\Scripts\python.exe scripts\build_decision_story_answer_gap_report.py --coverage-report .\artifacts\eval\decision_story_corpus_coverage.json --json --output .\artifacts\eval\decision_story_answer_gap_report.json
```

The gap report consumes the coverage diagnostic JSON and recommends the next action for each evidence group.

## Interpreting Benchmark Results

Benchmark results are deterministic regression checks over the loaded Minerva corpus.

- `PASS` means the question met its configured retrieval and answer checks.
- `FAIL` means at least one expected source, source phrase, answer phrase, section, or forbidden-pattern check did not pass.

A failure does not automatically mean answer synthesis is wrong. Common causes are:

- the loaded corpus does not contain enough formal evidence;
- retrieval terms do not find the relevant formal evidence;
- synthesis found evidence but did not express the expected Decision Story wording;
- another domain owns the question and the routing expectation needs review;
- the benchmark expectation no longer matches the intended product-domain wording.

Investigate failures from the returned source references, failed checks, coverage diagnostic, and answer gap report before changing code.

## Interpreting Coverage Status

The coverage diagnostic classifies each Decision Story evidence group:

- `STRONG`: multiple relevant chunks or documents were found. The corpus likely has enough retrievable evidence for the group.
- `WEAK`: some relevant evidence was found, but coverage is thin. Answers may be incomplete or overly dependent on one source.
- `MISSING`: no useful evidence was found for the group. Minerva should treat that part of the answer as corpus-limited.

Coverage status is about available formal corpus evidence, not runtime Decision Story implementation or operational payroll truth. A `MISSING` group may mean the product concept exists but the indexed formal evidence is not loaded or not discoverable yet.

## Interpreting Gap Report Status

The answer gap report summarizes whether Decision Story answers are ready enough to keep, refine, or defer.

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
- not proof of runtime Decision Story implementation;
- not proof that Minerva selects treatments;
- not proof that Minerva decides entitlements;
- not proof that Minerva interprets awards at runtime;
- not proof that Minerva calculates payroll;
- not proof that Minerva changes decision evidence;
- not proof that DecisionEvidenceIndex alone proves the full award-source chain;
- not proof that Decision Story is the same as Rate Story;
- not proof that Minerva validates payroll correctness or mutates payroll truth.

Minerva does not select treatments, decide entitlements, interpret awards at runtime, calculate payroll, change decision evidence, validate payroll correctness or mutate payroll truth. Decision Story evaluation must continue to use the indexed formal knowledge corpus. It must not read or ingest source-code content as Minerva answer evidence, and it must not connect Code Evidence Index to answer generation.
