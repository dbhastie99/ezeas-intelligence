# On-costs / Employer Liabilities Evaluation Runbook

This runbook documents the repeatable Minerva evaluation workflow for On-costs / Employer Liabilities. It is intended for regression checks and corpus-readiness diagnostics after retrieval-plan, benchmark, synthesis, diagnostic tooling, or formal corpus changes.

The workflow is diagnostic-only. It does not mutate corpus records, change database schema, ingest operational JSON, call a live LLM, or connect Code Evidence Index to answer generation.

## Purpose

On-costs / Employer Liabilities evaluation checks whether Minerva can retrieve and synthesize enough formal evidence to answer product-domain questions about governed employer liability evidence. It focuses on employer-side liabilities, not worker pay; deterministic services and governed configuration, not Minerva calculation; RateSource and date-effective rates; AwardRateType and RateType defaults or overrides; governed basis membership; super, payroll tax and WorkCover / WIC liability differences; state/worksite/runtime location resolution; PayRun Output, Worker Story, Payroll Bases & Totals, Finalisation Readiness, account-wide fallback demo behavior, production truth, and outstanding hardening.

The evaluation answers four practical questions:

- Does the full test suite still pass?
- Does the broad On-costs / Employer Liabilities benchmark still pass?
- Do the 11 focused follow-up benchmark questions still pass?
- Does the currently indexed formal corpus contain enough evidence for each On-costs / Employer Liabilities evidence group?

On-costs / Employer Liabilities evaluation is not proof of runtime on-cost / employer liability truth. It evaluates Minerva retrieval and answer quality over formal knowledge evidence. Employer liability is not worker pay, and on-costs are not worker net pay. Minerva does not calculate on-costs; it explains evidence and status. The evaluation is also not proof that demo account-wide fallback is production truth, runtime state/worksite/location resolution is complete, all on-cost AwardRateTypes/RateSources are automatically seeded, or raw flags are final runtime basis truth where governed basis membership is required.

## Domain Retrieval Coverage

The On-costs / Employer Liabilities domain retrieval plan is a deterministic evidence-gathering plan for questions about governed employer liability evidence. It splits broad and focused questions into targeted evidence groups and retrieves formal corpus chunks for each group.

The plan covers:

- purpose and operator meaning;
- employer liability not worker pay;
- RateSource and date-effective rates;
- AwardRateType and RateType settings;
- governed basis membership;
- super, payroll tax and WorkCover / WIC;
- state, worksite and runtime location resolution;
- PayRun Output and Worker Story connection;
- Payroll Bases & Totals connection;
- Finalisation Readiness connection;
- demo fallback versus production truth;
- outstanding hardening.

The plan decides what evidence to search for. It does not calculate on-costs, create employer liability outcomes, prove runtime payroll or employer liability truth, convert employer liability evidence into worker net pay, validate demo fallback as production truth, prove state/worksite resolution is complete, prove all on-cost configuration is seeded, or infer missing implementation status. If evidence is weak or missing, Minerva should report the corpus limitation instead of inventing a product claim.

## Difference From Other Evaluations

Annual Leave evaluation checks a leave-management product slice: configuration, accrual, TAKEN leave, valuation, PayRun orchestration, Worker Story leave evidence, and outstanding leave hardening. On-costs / Employer Liabilities does not evaluate leave balances or leave valuation; it evaluates employer-side liability evidence.

Worker Story evaluation checks the broader explanation surface for worker-level payroll outcomes. On-costs / Employer Liabilities only checks Worker Story where worker-payable lines must be distinguished from employer liability lines and on-cost evidence.

Payroll Bases & Totals evaluation checks governed payroll basis evidence, current-effective truth, bucket readiness and stale PayrollBucketResult caveats. On-costs / Employer Liabilities consumes or references Payroll Bases & Totals where governed basis evidence, basis membership or basis totals are needed for liability evidence; it does not replace the Payroll Bases evaluation.

PayRun Admin Queue evaluation checks the operator action workbench for blockers, warnings and ready actions. On-costs / Employer Liabilities may affect readiness or surfaced issues, but it does not evaluate the full Admin Queue workflow.

Movement Review evaluation checks payroll reasonableness, variance and review-worthy movement. On-costs / Employer Liabilities does not treat movement variance as employer liability calculation truth.

Comparison / Remediation evaluation checks governed comparison evidence and policy-driven assessment. On-costs / Employer Liabilities is not comparison/remediation, although liability evidence may need to remain separate from worker-pay remediation lines.

Tax / PAYG evaluation checks governed withholding evidence and status-honest tax explanation. On-costs / Employer Liabilities preserves a similar boundary: deterministic services and governed configuration produce outcomes, and Minerva does not calculate on-costs.

Deductions / Obligations evaluation checks governed deduction, obligation and recovery evidence. On-costs / Employer Liabilities is not worker deduction or obligation recovery; it explains employer-side liability evidence.

Retro / Replay evaluation checks governed historical correction and evidence replay. On-costs / Employer Liabilities does not prove retro/replay capability, but date-effective RateSource and liability configuration can matter for future replay or historical explanation.

Payment Execution / Remittance evaluation checks governed downstream payment and remittance evidence. On-costs / Employer Liabilities does not execute payment files or remittances; it may explain employer liability evidence that remains separate from worker net pay and payment execution.

Leave Accrual / Processing evaluation checks detailed leave accrual, payroll output, LeaveLedger, valuation, request/payment sequencing and processing readiness. On-costs / Employer Liabilities does not calculate leave accrual; it focuses on employer liabilities such as superannuation on-costs and their governed bases.

Finalisation Readiness evaluation checks the governed readiness gate for PayRun finalisation. On-costs / Employer Liabilities supplies evidence that Finalisation Readiness may need when unresolved basis or liability configuration should block, warn, or require review under policy.

Leave Source Model evaluation checks governed leave applicability and source truth. On-costs / Employer Liabilities may also need source and location resolution, but its scope is employer liability evidence rather than leave applicability.

All evaluations use deterministic retrieval and benchmark checks. Worker Story, Payroll Bases & Totals, PayRun Admin Queue, Movement Review, Comparison / Remediation, Tax / PAYG, Deductions / Obligations, Retro / Replay, Payment Execution / Remittance, Leave Accrual / Processing, Finalisation Readiness, Leave Source Model, and On-costs / Employer Liabilities additionally have corpus coverage diagnostics and answer gap reports that classify evidence readiness group by group.

## Commands

Run commands from the repository root.

### Full Pytest Suite

```powershell
.\.venv\Scripts\python.exe -m pytest --basetemp .\.pytest_tmp
```

This is the main regression gate. It should pass before treating any benchmark or diagnostic output as meaningful.

### On-costs / Employer Liabilities Benchmark

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.oncosts_employer_liabilities.json
```

The benchmark includes the broad question, "How should On-costs and Employer Liabilities work in Ezeas?", plus focused follow-up questions about not being worker pay, why Minerva does not calculate on-costs, RateSource/date-effective rates, AwardRateType and RateType settings, governed basis membership, super/payroll tax/WorkCover/WIC differences, state/worksite/runtime location resolution, PayRun Output and Worker Story, Payroll Bases & Totals, account-wide fallback demo behavior, and Finalisation Readiness.

### Corpus Coverage Diagnostic

```powershell
.\.venv\Scripts\python.exe scripts\scan_oncosts_employer_liabilities_corpus_coverage.py
.\.venv\Scripts\python.exe scripts\scan_oncosts_employer_liabilities_corpus_coverage.py --json --output .\artifacts\eval\oncosts_employer_liabilities_corpus_coverage.json
```

The diagnostic reads the already indexed formal corpus and reports coverage for each On-costs / Employer Liabilities evidence group. It does not ingest files, mutate corpus records, call a live LLM, or change schema.

### Answer Gap Report

```powershell
.\.venv\Scripts\python.exe scripts\build_oncosts_employer_liabilities_answer_gap_report.py --coverage-report .\artifacts\eval\oncosts_employer_liabilities_corpus_coverage.json
.\.venv\Scripts\python.exe scripts\build_oncosts_employer_liabilities_answer_gap_report.py --coverage-report .\artifacts\eval\oncosts_employer_liabilities_corpus_coverage.json --json --output .\artifacts\eval\oncosts_employer_liabilities_answer_gap_report.json
```

The gap report consumes the coverage diagnostic JSON and recommends the next action for each evidence group.

## Interpreting Benchmark Results

Benchmark results are deterministic regression checks over the loaded Minerva corpus.

- `PASS` means the question met its configured retrieval and answer checks.
- `FAIL` means at least one expected source, source phrase, answer phrase, section, or forbidden-pattern check did not pass.

A failure does not automatically mean answer synthesis is wrong. Common causes are:

- the loaded corpus does not contain enough formal evidence;
- retrieval terms do not find the relevant formal evidence;
- synthesis found evidence but did not express the expected On-costs / Employer Liabilities wording;
- the benchmark expectation no longer matches the intended product-domain wording.

Investigate failures from the returned source references, failed checks, coverage diagnostic, and answer gap report before changing code.

## Interpreting Coverage Status

The coverage diagnostic classifies each On-costs / Employer Liabilities evidence group:

- `STRONG`: multiple relevant chunks or documents were found. The corpus likely has enough retrievable evidence for the group.
- `WEAK`: some relevant evidence was found, but coverage is thin. Answers may be incomplete or overly dependent on one source.
- `MISSING`: no useful evidence was found for the group. Minerva should treat that part of the answer as corpus-limited.

Coverage status is about available formal corpus evidence, not runtime on-cost / employer liability truth. A `MISSING` group may mean the product concept exists but the indexed formal evidence is not loaded or not discoverable yet.

## Interpreting Gap Report Status

The answer gap report summarizes whether On-costs / Employer Liabilities answers are ready enough to keep, refine, or defer.

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
- not proof of runtime on-cost / employer liability truth;
- not proof that Minerva calculates on-costs;
- not proof that on-costs are worker net pay;
- not proof that demo account-wide fallback is production truth;
- not proof that runtime state/worksite/location resolution is complete;
- not proof that all on-cost AwardRateTypes/RateSources are automatically seeded;
- not proof that raw flags are final runtime basis truth where governed basis membership is required.

On-costs / Employer Liabilities evaluation must continue to use the indexed formal knowledge corpus. It must not read or ingest source-code content as Minerva answer evidence, and it must not connect Code Evidence Index to answer generation.
