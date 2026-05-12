# Movement Review Evaluation Runbook

This runbook documents the repeatable Minerva evaluation workflow for Movement Review. It is intended for regression checks and corpus-readiness diagnostics after retrieval-plan, benchmark, synthesis, or formal corpus changes.

The workflow is diagnostic-only. It does not mutate corpus records, change database schema, ingest operational JSON, call a live LLM, or connect Code Evidence Index to answer generation.

## Purpose

Movement Review evaluation checks whether Minerva can retrieve and synthesize enough formal evidence to answer product-domain questions about payroll reasonableness and review evidence.

The evaluation answers four practical questions:

- Does the full test suite still pass?
- Does the broad Movement Review benchmark still pass?
- Do the focused follow-up benchmark questions still pass?
- Does the currently indexed formal corpus contain enough evidence for each Movement Review evidence group?

Movement Review evaluation is not proof of runtime PayRun truth. It evaluates Minerva retrieval and answer quality over formal knowledge evidence. It is also not proof that Movement Review calculates payroll; deterministic Ezeas services remain calculation truth.

## Domain Retrieval Coverage

The Movement Review domain retrieval plan is a deterministic evidence-gathering plan for questions about payroll reasonableness, variance and review-worthy movement. It splits broad and focused questions into targeted evidence groups and retrieves formal corpus chunks for each group.

The plan covers:

- purpose and operator meaning;
- reasonableness, not automatic error;
- worker and organisation lenses;
- variance and comparable periods;
- Payroll Bases & Totals connection;
- Worker Story connection;
- Admin Queue connection;
- current-effective truth;
- trend-only and threshold treatment;
- filters and return context;
- outstanding hardening.

The plan decides what evidence to search for. It does not calculate payroll, does not prove runtime PayRun truth, and does not infer missing implementation status. If evidence is weak or missing, Minerva should report the corpus limitation instead of inventing a product claim.

## Difference From Other Evaluations

Annual Leave evaluation checks a leave-management product slice: configuration, accrual, TAKEN leave, valuation, PayRun orchestration, Worker Story leave evidence, and outstanding leave hardening.

Worker Story evaluation checks a broader explanation and evidence slice around how payroll outcomes are shown to an operator or worker. It focuses on source truth, calculated payroll output, decision/rate evidence, current-effective truth, and related review/admin surfaces.

Payroll Bases & Totals evaluation checks a governed payroll basis evidence slice. It preserves the distinction between basis evidence and reporting or analytics totals, checks current-effective truth and stale PayrollBucketResult caveats, and verifies relationship evidence for Worker Story and Movement Review.

PayRun Admin Queue evaluation checks the operator action workbench for blockers, warnings, ready actions, worker attention, dirty contacts, finalisation readiness, Assurance Snapshot, review navigation and outstanding hardening.

Movement Review evaluation checks payroll reasonableness and review evidence. It preserves the doctrine that variance is not automatic proof of error and that not every movement creates a fix action. It also checks organisation and worker lenses, comparable period evidence, trend-only / rolling / YTD treatment, and relationships to Payroll Bases & Totals, Worker Story and PayRun Admin Queue.

All five evaluations use deterministic retrieval and benchmark checks. Worker Story, Payroll Bases & Totals, PayRun Admin Queue, and Movement Review additionally have corpus coverage diagnostics and answer gap reports that classify evidence readiness group by group.

## Commands

Run commands from the repository root.

### Full Pytest Suite

```powershell
.\.venv\Scripts\python.exe -m pytest --basetemp .\.pytest_tmp
```

This is the main regression gate. It should pass before treating any benchmark or diagnostic output as meaningful.

### Movement Review Benchmark

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.movement_review.json
```

The benchmark includes the broad question, "What is Movement Review and what does it show?", plus focused follow-up questions about review-worthy movement, organisation and worker lenses, comparable periods and variance, Payroll Bases & Totals, Worker Story, PayRun Admin Queue / Assurance Snapshot, and rolling / YTD / trend-only metrics.

### Corpus Coverage Diagnostic

```powershell
.\.venv\Scripts\python.exe scripts\scan_movement_review_corpus_coverage.py
.\.venv\Scripts\python.exe scripts\scan_movement_review_corpus_coverage.py --json --output .\artifacts\eval\movement_review_corpus_coverage.json
```

The diagnostic reads the already indexed formal corpus and reports coverage for each Movement Review evidence group. It does not ingest files, mutate corpus records, call a live LLM, or change schema.

### Answer Gap Report

```powershell
.\.venv\Scripts\python.exe scripts\build_movement_review_answer_gap_report.py --coverage-report .\artifacts\eval\movement_review_corpus_coverage.json
.\.venv\Scripts\python.exe scripts\build_movement_review_answer_gap_report.py --coverage-report .\artifacts\eval\movement_review_corpus_coverage.json --json --output .\artifacts\eval\movement_review_answer_gap_report.json
```

The gap report consumes the coverage diagnostic JSON and recommends the next action for each evidence group.

## Interpreting Benchmark Results

Benchmark results are deterministic regression checks over the loaded Minerva corpus.

- `PASS` means the question met its configured retrieval and answer checks.
- `FAIL` means at least one expected source, source phrase, answer phrase, section, or forbidden-pattern check did not pass.

A failure does not automatically mean answer synthesis is wrong. Common causes are:

- the loaded corpus does not contain enough formal evidence;
- retrieval terms do not find the relevant formal evidence;
- synthesis found evidence but did not express the expected Movement Review wording;
- the benchmark expectation no longer matches the intended product-domain wording.

Investigate failures from the returned source references, failed checks, coverage diagnostic, and answer gap report before changing code.

## Interpreting Coverage Status

The coverage diagnostic classifies each Movement Review evidence group:

- `STRONG`: multiple relevant chunks or documents were found. The corpus likely has enough retrievable evidence for the group.
- `WEAK`: some relevant evidence was found, but coverage is thin. Answers may be incomplete or overly dependent on one source.
- `MISSING`: no useful evidence was found for the group. Minerva should treat that part of the answer as corpus-limited.

Coverage status is about available formal corpus evidence, not runtime PayRun truth. A `MISSING` group may mean the product concept exists but the indexed formal evidence is not loaded or not discoverable yet.

## Interpreting Gap Report Status

The answer gap report summarizes whether Movement Review answers are ready enough to keep, refine, or defer.

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
- not proof of runtime PayRun truth;
- not proof that Movement Review calculates payroll;
- not proof that variance means payroll is wrong;
- not proof that every movement creates a fix action.

Movement Review evaluation must continue to use the indexed formal knowledge corpus. It must not read or ingest source-code content as Minerva answer evidence, and it must not connect Code Evidence Index to answer generation.
