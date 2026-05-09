# Worker Story Evaluation Runbook

This runbook documents the repeatable Minerva evaluation workflow for Worker Story / Worker Calculation Story. It is intended for regression checks and corpus-readiness diagnostics after retrieval-plan, benchmark, or formal corpus changes.

The workflow is documentation-first and diagnostic-only. It does not change retrieval logic, answer synthesis, benchmark behavior, corpus contents, database schema, or Code Evidence Index integration.

## Purpose

Worker Story evaluation checks whether Minerva can retrieve and synthesize enough formal evidence to answer product-domain questions about Worker Story / Worker Calculation Story.

The evaluation answers three practical questions:

- Does the full test suite still pass?
- Does the Worker Story rich-answer benchmark still behave as expected?
- Does the currently indexed formal corpus contain enough evidence for each Worker Story evidence group?

Worker Story evaluation is not a live LLM quality review. It uses deterministic retrieval, deterministic benchmark checks, and the stub answer generator.

## Worker Story Domain Retrieval Coverage

The Worker Story domain retrieval plan is a deterministic evidence-gathering plan for Worker Story / Worker Calculation Story questions. It splits broad product-domain questions into targeted evidence groups and retrieves formal corpus chunks for each group.

The plan covers:

- Worker Story purpose;
- source truth and inclusion evidence;
- Interpreted Worked Hours;
- Calculated Payroll Outcome;
- Decision Story and Rate Story;
- Leave and Accrual Outcome;
- Payroll Bases & Totals;
- Movement Review and PayRun Admin Queue;
- current-effective truth;
- outstanding hardening and limitations.

The plan decides what evidence to search for. It does not hardcode an answer. If evidence is weak or missing, Minerva should report the corpus limitation instead of inventing a product claim.

## Difference From Annual Leave Evaluation

Annual Leave evaluation checks a leave-management product slice: configuration, accrual, TAKEN leave, valuation, PayRun orchestration, Worker Story leave evidence, and outstanding leave hardening.

Worker Story evaluation checks a broader explanation and evidence slice around how payroll outcomes are shown to an operator or worker. It focuses on source truth, calculated payroll output, decision/rate evidence, current-effective truth, and related review/admin surfaces.

Both evaluations use deterministic retrieval and benchmark checks. Worker Story additionally has a corpus coverage diagnostic and an answer gap report that classify evidence readiness group by group.

## Commands

Run commands from the repository root.

### Full Pytest Suite

```powershell
pytest
```

This is the main regression gate. It should pass before treating any benchmark or diagnostic output as meaningful.

### Worker Story Benchmark

```powershell
py scripts/run_golden_questions.py --manifest samples/eval/rich_answer_benchmark.worker_story.json --verbose --allow-failures
```

Use `--allow-failures` when tracking benchmark readiness against an incomplete formal corpus. Remove it only when the corpus and expected checks are intended to be fully passing.

### Annual Leave Benchmark Regression Check

```powershell
py scripts/run_golden_questions.py --manifest samples/eval/rich_answer_benchmark.annual_leave.json --verbose --allow-failures
```

This confirms Worker Story work has not regressed the existing Annual Leave rich-answer path.

### Worker Story Corpus Coverage Diagnostic

```powershell
py scripts/scan_worker_story_corpus_coverage.py
py scripts/scan_worker_story_corpus_coverage.py --json --output reports/worker_story_corpus_coverage.json
```

The diagnostic reads the already indexed formal corpus and reports coverage for each Worker Story evidence group. It does not ingest files or mutate corpus records.

### Worker Story Answer Gap Report

```powershell
py scripts/build_worker_story_answer_gap_report.py --coverage-report reports/worker_story_corpus_coverage.json
py scripts/build_worker_story_answer_gap_report.py --coverage-report reports/worker_story_corpus_coverage.json --json --output reports/worker_story_answer_gap_report.json
```

The gap report consumes the coverage diagnostic JSON and recommends the next action for each evidence group.

## Interpreting Benchmark Results

Benchmark results are deterministic regression checks over the loaded Minerva corpus.

- `PASS` means the question met its configured retrieval and answer checks.
- `FAIL` means at least one expected source, source phrase, or answer phrase was not found.

A failure does not automatically mean answer synthesis is wrong. Common causes are:

- the loaded corpus does not contain enough formal evidence;
- retrieval terms do not find the relevant formal evidence;
- synthesis found evidence but did not express the expected phrase;
- the benchmark expectation no longer matches the intended product wording.

Investigate failures from the top sources and failed checks before changing code.

## Interpreting Coverage Status

The coverage diagnostic classifies each Worker Story evidence group:

- `STRONG`: multiple relevant chunks or documents were found. The corpus likely has enough retrievable evidence for the group.
- `WEAK`: some relevant evidence was found, but coverage is thin. Answers may be incomplete or overly dependent on one source.
- `MISSING`: no useful evidence was found for the group. Minerva should treat that part of the answer as corpus-limited.

Coverage status is about available formal corpus evidence, not product truth. A `MISSING` group may mean the product exists but the indexed formal evidence is not loaded or not discoverable yet.

## Interpreting Gap Report Status

The answer gap report summarizes whether Worker Story answers are ready enough to keep, refine, or defer.

- `GOOD`: core evidence is strong enough for the current answer path.
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
- no live LLM calls;
- no corpus mutation;
- no database schema change;
- no Code Evidence Index answer integration;
- no source code content used as answer evidence.

Code Evidence Index v1.0 remains metadata-only and disconnected from answer generation. Worker Story evaluation must continue to use the indexed formal knowledge corpus, not source code content.
