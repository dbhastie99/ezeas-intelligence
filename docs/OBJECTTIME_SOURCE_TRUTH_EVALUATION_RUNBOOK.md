# ObjectTime / Source Truth Evaluation Runbook

This runbook documents the repeatable Minerva evaluation workflow for ObjectTime / Source Truth. It is intended for regression checks and corpus-readiness diagnostics after retrieval-plan, benchmark, synthesis, diagnostic tooling, or formal corpus changes.

The workflow is diagnostic-only. It does not mutate corpus records, change database schema, ingest operational JSON, call a live LLM, or connect Code Evidence Index to answer generation.

## Purpose

ObjectTime / Source Truth evaluation checks whether Minerva can retrieve and synthesize enough formal evidence to answer product-domain questions about governed source evidence, source-row inclusion and PayRun inclusion context. It focuses on ObjectTime as source evidence, SourceTruth, WorkedHours boundaries, imported and generated source rows, current-effective payroll output, Worker Story, Payroll Bases, Leave Accrual, Comparison / Remediation, Movement Review, Retro / Replay, corrections, dirty contacts, reprocessing, provenance and audit.

The evaluation answers four practical questions:

- Does the full test suite still pass?
- Does the broad ObjectTime / Source Truth benchmark still pass?
- Do the 11 focused follow-up benchmark questions still pass?
- Does the currently indexed formal corpus contain enough evidence for each ObjectTime / Source Truth evidence group?

ObjectTime is source evidence, not payroll calculation truth by itself. ObjectTime / Source Truth can explain why a worker or source row belongs in a PayRun, but raw span hours are not user-facing worked hours. SourceTruth versus WorkedHours must stay explicit. This evaluation is not proof of runtime ObjectTime/source-truth truth, not proof that ObjectTime alone is final payroll calculation truth, not proof that imported source data is automatically valid, not proof that dependency detection and dirty-contact propagation are complete, and not proof that Minerva mutates source truth or reprocesses workers.

## Domain Retrieval Coverage

The ObjectTime / Source Truth domain retrieval plan is a deterministic evidence-gathering plan for questions about source evidence, inclusion and provenance. It splits broad and focused questions into targeted evidence groups and retrieves formal corpus chunks for each group.

The plan covers:

- purpose and operator meaning;
- ObjectTime as source evidence;
- PayRun inclusion and source truth;
- imported and generated source rows;
- SourceTruth versus WorkedHours;
- current-effective output connection;
- Worker Story connection;
- Payroll Bases and Leave Accrual connection;
- Comparison, Movement Review and Retro / Replay connection;
- corrections, dirty contacts and reprocessing;
- evidence provenance and audit;
- outstanding hardening.

The plan decides what evidence to search for. It does not calculate payroll, treat raw ObjectTime span hours as user-facing worked hours, merge SourceTruth and WorkedHours, validate imported source data, prove dependency detection is complete, mark contacts dirty, reprocess workers, or mutate source truth. If evidence is weak or missing, Minerva should report the corpus limitation instead of inventing a product claim.

## Difference From Other Evaluations

Imports / Actuals evaluation checks imported timesheets, imported payroll actuals, source-system mappings and imported actuals as an external outcome lane. ObjectTime / Source Truth is lower-level source evidence and inclusion context. Imports / Actuals may feed ObjectTime/source truth, but it also owns import mapping and imported actuals behavior.

Worker Story evaluation checks the broader explanation surface for worker-level payroll outcomes. ObjectTime / Source Truth only checks the Source Truth and inclusion foundation that Worker Story should present before calculated payroll outcome.

Payroll Bases & Totals evaluation checks governed payroll basis evidence, bucket definitions, current-effective truth and rebuild readiness. ObjectTime / Source Truth explains source evidence behind inclusion; Payroll Bases should consume governed processed payroll or bucket evidence, not raw source span duration.

Leave Accrual / Processing evaluation checks leave source truth, applicability, processed payroll output, LeaveLedger and leave valuation. ObjectTime / Source Truth can explain work/time source evidence, but Leave Accrual should consume governed processed/bucket evidence rather than raw ObjectTime span hours.

Movement Review evaluation checks reasonableness, variance and review-worthy movement. ObjectTime / Source Truth supplies source truth and provenance that Movement Review may need to explain why a change or variance exists.

Retro / Replay evaluation checks governed historical correction and evidence replay. ObjectTime / Source Truth supplies source truth, correction history and current-effective versus historical distinctions that replay may depend on; it does not prove replay or dependency detection is complete.

Comparison / Remediation evaluation checks comparison lanes, policies, variance and remediation. ObjectTime / Source Truth can support source evidence and inclusion provenance that comparisons depend on, but it does not own comparison policy or remediation generation.

Annual Leave, PayRun Admin Queue, Tax / PAYG, Deductions / Obligations, Payment Execution / Remittance, Finalisation Readiness, Leave Source Model, On-costs / Employer Liabilities, and Award Build / Award Evidence evaluate separate product domains. ObjectTime / Source Truth may connect to several of them through source evidence, inclusion and provenance, but it should not be treated as their runtime calculation truth.

All evaluations use deterministic retrieval and benchmark checks. Worker Story, Payroll Bases & Totals, PayRun Admin Queue, Movement Review, Comparison / Remediation, Tax / PAYG, Deductions / Obligations, Retro / Replay, Payment Execution / Remittance, Leave Accrual / Processing, Finalisation Readiness, Leave Source Model, On-costs / Employer Liabilities, Award Build / Award Evidence, Imports / Actuals, and ObjectTime / Source Truth additionally have corpus coverage diagnostics and answer gap reports that classify evidence readiness group by group.

## Commands

Run commands from the repository root.

### Full Pytest Suite

```powershell
.\.venv\Scripts\python.exe -m pytest --basetemp .\.pytest_tmp
```

This is the main regression gate. It should pass before treating any benchmark or diagnostic output as meaningful.

### ObjectTime / Source Truth Benchmark

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.objecttime_source_truth.json
```

The benchmark includes the broad question, "What is ObjectTime / Source Truth and why does it matter?", plus focused follow-up questions about ObjectTime as source evidence, PayRun inclusion, SourceTruth versus WorkedHours, raw span hours, imported and generated source rows, current-effective payroll output, Worker Story, Payroll Bases and Leave Accrual, Comparison / Movement Review / Retro / Replay, corrections and dirty contacts, and evidence provenance and audit.

### Corpus Coverage Diagnostic

```powershell
.\.venv\Scripts\python.exe scripts\scan_objecttime_source_truth_corpus_coverage.py
.\.venv\Scripts\python.exe scripts\scan_objecttime_source_truth_corpus_coverage.py --json --output .\artifacts\eval\objecttime_source_truth_corpus_coverage.json
```

The diagnostic reads the already indexed formal corpus and reports coverage for each ObjectTime / Source Truth evidence group. It does not ingest files, mutate corpus records, call a live LLM, or change schema.

### Answer Gap Report

```powershell
.\.venv\Scripts\python.exe scripts\build_objecttime_source_truth_answer_gap_report.py --coverage-report .\artifacts\eval\objecttime_source_truth_corpus_coverage.json
.\.venv\Scripts\python.exe scripts\build_objecttime_source_truth_answer_gap_report.py --coverage-report .\artifacts\eval\objecttime_source_truth_corpus_coverage.json --json --output .\artifacts\eval\objecttime_source_truth_answer_gap_report.json
```

The gap report consumes the coverage diagnostic JSON and recommends the next action for each evidence group.

## Interpreting Benchmark Results

Benchmark results are deterministic regression checks over the loaded Minerva corpus.

- `PASS` means the question met its configured retrieval and answer checks.
- `FAIL` means at least one expected source, source phrase, answer phrase, section, or forbidden-pattern check did not pass.

A failure does not automatically mean answer synthesis is wrong. Common causes are:

- the loaded corpus does not contain enough formal evidence;
- retrieval terms do not find the relevant formal evidence;
- synthesis found evidence but did not express the expected ObjectTime / Source Truth wording;
- the benchmark expectation no longer matches the intended product-domain wording.

Investigate failures from the returned source references, failed checks, coverage diagnostic, and answer gap report before changing code.

## Interpreting Coverage Status

The coverage diagnostic classifies each ObjectTime / Source Truth evidence group:

- `STRONG`: multiple relevant chunks or documents were found. The corpus likely has enough retrievable evidence for the group.
- `WEAK`: some relevant evidence was found, but coverage is thin. Answers may be incomplete or overly dependent on one source.
- `MISSING`: no useful evidence was found for the group. Minerva should treat that part of the answer as corpus-limited.

Coverage status is about available formal corpus evidence, not runtime ObjectTime/source-truth truth. A `MISSING` group may mean the product concept exists but the indexed formal evidence is not loaded or not discoverable yet.

## Interpreting Gap Report Status

The answer gap report summarizes whether ObjectTime / Source Truth answers are ready enough to keep, refine, or defer.

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
- not proof of runtime ObjectTime/source-truth truth;
- not proof that ObjectTime alone is final payroll calculation truth;
- not proof that raw span hours are worked hours;
- not proof that SourceTruth and WorkedHours are the same;
- not proof that imported source data is automatically valid;
- not proof that dependency detection and dirty-contact propagation are complete;
- not proof that Minerva mutates source truth or reprocesses workers.

ObjectTime / Source Truth evaluation must continue to use the indexed formal knowledge corpus. It must not read or ingest source-code content as Minerva answer evidence, and it must not connect Code Evidence Index to answer generation.
