# Payroll Bases & Totals Evaluation Runbook

This runbook documents the repeatable Minerva evaluation workflow for Payroll Bases & Totals. It is intended for regression checks and corpus-readiness diagnostics after retrieval-plan, benchmark, synthesis, or formal corpus changes.

The workflow is diagnostic-only. It does not mutate corpus records, change database schema, ingest operational JSON, call a live LLM, or connect Code Evidence Index to answer generation.

## Purpose

Payroll Bases & Totals evaluation checks whether Minerva can retrieve and synthesize enough formal evidence to answer product-domain questions about governed payroll basis evidence.

The evaluation answers four practical questions:

- Does the full test suite still pass?
- Does the broad Payroll Bases & Totals benchmark still pass?
- Do the focused follow-up benchmark questions still pass?
- Does the currently indexed formal corpus contain enough evidence for each Payroll Bases & Totals evidence group?

Payroll Bases & Totals evaluation is not proof of runtime payroll truth. It evaluates Minerva retrieval and answer quality over formal knowledge evidence. Deterministic Ezeas services remain payroll truth.

## Domain Retrieval Coverage

The Payroll Bases & Totals domain retrieval plan is a deterministic evidence-gathering plan for questions about governed payroll basis evidence. It splits broad and focused questions into targeted evidence groups and retrieves formal corpus chunks for each group.

The plan covers:

- purpose and operator meaning;
- bucket definition and membership;
- worked hours and quantity;
- gross, ordinary, superable and taxable bases;
- current-effective truth;
- readiness and rebuild;
- Worker Story connection;
- Movement Review connection;
- outstanding hardening.

The plan decides what evidence to search for. It does not calculate payroll, does not prove payroll calculation truth, and does not infer missing implementation status. If evidence is weak or missing, Minerva should report the corpus limitation instead of inventing a product claim.

## Difference From Annual Leave And Worker Story Evaluation

Annual Leave evaluation checks a leave-management product slice: configuration, accrual, TAKEN leave, valuation, PayRun orchestration, Worker Story leave evidence, and outstanding leave hardening.

Worker Story evaluation checks a broader explanation and evidence slice around how payroll outcomes are shown to an operator or worker. It focuses on source truth, calculated payroll output, decision/rate evidence, current-effective truth, and related review/admin surfaces.

Payroll Bases & Totals evaluation checks a governed payroll basis evidence slice. It preserves the distinction between basis evidence and reporting or analytics totals, checks current-effective truth and stale PayrollBucketResult caveats, and verifies relationship evidence for Worker Story and Movement Review.

All three evaluations use deterministic retrieval and benchmark checks. Worker Story and Payroll Bases & Totals additionally have corpus coverage diagnostics and answer gap reports that classify evidence readiness group by group.

## Commands

Run commands from the repository root.

### Full Pytest Suite

```powershell
.\.venv\Scripts\python.exe -m pytest --basetemp .\.pytest_tmp
```

This is the main regression gate. It should pass before treating any benchmark or diagnostic output as meaningful.

### Payroll Bases & Totals Benchmark

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.payroll_bases_and_totals.json
```

The benchmark includes the broad question, "What are Payroll Bases & Totals and why do they matter?", plus focused follow-up questions about current-effective truth, reporting totals, bucket definitions and membership, stale PayrollBucketResult rows, and Worker Story / Movement Review relationships.

### Corpus Coverage Diagnostic

```powershell
.\.venv\Scripts\python.exe scripts\scan_payroll_bases_corpus_coverage.py
.\.venv\Scripts\python.exe scripts\scan_payroll_bases_corpus_coverage.py --json --output .\artifacts\eval\payroll_bases_corpus_coverage.json
```

The diagnostic reads the already indexed formal corpus and reports coverage for each Payroll Bases & Totals evidence group. It does not ingest files, mutate corpus records, call a live LLM, or change schema.

### Answer Gap Report

```powershell
.\.venv\Scripts\python.exe scripts\build_payroll_bases_answer_gap_report.py --coverage-report .\artifacts\eval\payroll_bases_corpus_coverage.json
.\.venv\Scripts\python.exe scripts\build_payroll_bases_answer_gap_report.py --coverage-report .\artifacts\eval\payroll_bases_corpus_coverage.json --json --output .\artifacts\eval\payroll_bases_answer_gap_report.json
```

The gap report consumes the coverage diagnostic JSON and recommends the next action for each evidence group.

## Interpreting Benchmark Results

Benchmark results are deterministic regression checks over the loaded Minerva corpus.

- `PASS` means the question met its configured retrieval and answer checks.
- `FAIL` means at least one expected source, source phrase, answer phrase, section, or forbidden-pattern check did not pass.

A failure does not automatically mean answer synthesis is wrong. Common causes are:

- the loaded corpus does not contain enough formal evidence;
- retrieval terms do not find the relevant formal evidence;
- synthesis found evidence but did not express the expected Payroll Bases wording;
- the benchmark expectation no longer matches the intended product-domain wording.

Investigate failures from the returned source references, failed checks, coverage diagnostic, and answer gap report before changing code.

## Interpreting Coverage Status

The coverage diagnostic classifies each Payroll Bases & Totals evidence group:

- `STRONG`: multiple relevant chunks or documents were found. The corpus likely has enough retrievable evidence for the group.
- `WEAK`: some relevant evidence was found, but coverage is thin. Answers may be incomplete or overly dependent on one source.
- `MISSING`: no useful evidence was found for the group. Minerva should treat that part of the answer as corpus-limited.

Coverage status is about available formal corpus evidence, not runtime payroll truth. A `MISSING` group may mean the product concept exists but the indexed formal evidence is not loaded or not discoverable yet.

## Interpreting Gap Report Status

The answer gap report summarizes whether Payroll Bases & Totals answers are ready enough to keep, refine, or defer.

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
- not proof of runtime payroll truth.

Payroll Bases & Totals evaluation must continue to use the indexed formal knowledge corpus. It must not read or ingest source-code content as Minerva answer evidence, and it must not connect Code Evidence Index to answer generation.
