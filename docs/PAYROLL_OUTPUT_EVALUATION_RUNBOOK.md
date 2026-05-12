# Payroll Output Evaluation Runbook

This runbook documents the repeatable Minerva evaluation workflow for Payroll Output. It is intended for regression checks and corpus-readiness diagnostics after retrieval-plan, benchmark, synthesis, diagnostic tooling, or formal corpus changes.

The workflow is diagnostic-only. It does not mutate corpus records, change database schema, ingest operational JSON, call a live LLM, read source-code content as Minerva evidence, or connect Code Evidence Index to answer generation. It also provides no Code Evidence answer integration.

## Purpose

Payroll Output evaluation checks whether Minerva can retrieve and synthesize enough formal evidence to answer product-domain questions about calculated payroll results, current-effective worker and PayRun output, payroll lines or output lines, PayRun Output, Run Output, Process Period Output, worker-level output, PayRun totals, and downstream relationships to Worker Story, Gross-to-Net, Decision Story, RateSource / Rate Story, Payroll Bases & Totals, Finalisation Readiness and Payment Execution / Remittance.

The evaluation answers four practical questions:

- Does the full test suite still pass?
- Does the broad Payroll Output benchmark still pass?
- Do the focused follow-up benchmark questions still pass?
- Does the currently indexed formal corpus contain enough evidence for each Payroll Output evidence group?

Payroll Output evaluation is not proof of runtime Payroll Output implementation. It evaluates Minerva retrieval and answer quality over formal knowledge evidence. It is not proof that Minerva calculates payroll output, changes payroll output lines, finalises PayRuns, approves payroll output, selects treatments, selects rates, generates payment files or mutates payroll truth. It is also not proof that Payroll Output alone proves payroll correctness or that Run Output and Process Period Output are the same lens.

## Domain Retrieval Coverage

The Payroll Output domain retrieval plan is a deterministic evidence-gathering plan for questions about calculated payroll output evidence and output lenses. It splits broad and focused questions into targeted evidence groups and retrieves formal corpus chunks for each group.

The plan covers:

- Payroll Output purpose and operator meaning;
- calculated payroll lines and output lines;
- current-effective payroll output truth;
- Run Output versus Process Period Output;
- PayRun Output and selected run/subrun lenses;
- worker-level output and Worker Story relationship;
- PayRun totals and line totals;
- Decision Story and Rate Story relationship for why a line exists and why a selected rate or amount was used;
- Gross-to-Net relationship for gross earnings, taxable basis, deductions, obligations and net pay;
- Payroll Bases & Totals relationship for governed basis evidence;
- Finalisation Readiness and Payment Execution / Remittance relationship;
- outstanding hardening.

The plan decides what evidence to search for. It does not calculate payroll output, change output lines, finalise PayRuns, approve output, select treatments, select rates, generate payment files, prove payroll correctness, or mutate payroll truth. If evidence is weak or missing, Minerva should report the corpus limitation instead of inventing a product claim.

## Difference From Other Evaluations

Gross-to-Net evaluation owns the outcome explanation from gross earnings through taxable basis, PAYG, deductions, obligations and net pay. Payroll Output owns calculated output evidence and output lenses that Gross-to-Net consumes.

Worker Story evaluation owns broader worker-level narrative, evidence chapters, line proof and audit context. Payroll Output can provide the current-effective worker output evidence that Worker Story renders, but Worker Story remains the broader explanation surface.

Decision Story evaluation owns why a payroll line, treatment or entitlement exists. Payroll Output can show the calculated line, while Decision Story explains the treatment-selection evidence behind that line.

RateSource / Rate Story evaluation owns why a selected rate, RateSource or rate amount was used. Payroll Output can include a line amount or selected rate reference, but Rate Story owns rate evidence and RateSource explanation.

Payroll Bases & Totals evaluation owns governed basis evidence, bucket membership, taxable/superable/payroll tax/WIC/ordinary/worked-hours basis evidence and total/basis readiness. Payroll Output owns calculated pay/result evidence; output totals and basis evidence are related but distinct.

Finalisation Readiness evaluation owns readiness gates, blockers, warnings, current-effective output checks and finalisation safety. Payroll Output can be one input to readiness, but it does not determine readiness or finalise PayRuns.

Payment Execution / Remittance evaluation owns payment files, payment destinations, bank allocation, third-party remittance and payment execution readiness. Payroll Output may feed finalised/gross-to-net/payment-ready outcomes downstream, but it does not generate payment files.

PayRun Admin Queue evaluation owns the operator workbench for actions, blockers, warnings, dirty contact/reprocessing actions and readiness work. Payroll Output can explain calculated result evidence; Admin Queue owns what needs action now.

All evaluations use deterministic retrieval and benchmark checks. Payroll Output additionally has corpus coverage diagnostics and an answer gap report that classify evidence readiness group by group.

## Commands

Run commands from the repository root.

### Full Pytest Suite

```powershell
.\.venv\Scripts\python.exe -m pytest --basetemp .\.pytest_tmp
```

This is the main regression gate. It should pass before treating any benchmark or diagnostic output as meaningful.

### Payroll Output Benchmark

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.payroll_output.json
```

The benchmark includes the broad question, "What is Payroll Output in the platform?", plus focused follow-up questions about current-effective payroll output, Run Output versus Process Period Output, payroll line output and evidence, Gross-to-Net, Payroll Bases & Totals, and finalisation/payment execution relationships.

### Corpus Coverage Diagnostic

```powershell
.\.venv\Scripts\python.exe scripts\scan_payroll_output_corpus_coverage.py
.\.venv\Scripts\python.exe scripts\scan_payroll_output_corpus_coverage.py --json --output .\artifacts\eval\payroll_output_corpus_coverage.json
```

The diagnostic reads the already indexed formal corpus and reports coverage for each Payroll Output evidence group. It does not ingest files, mutate corpus records, call a live LLM, ingest operational JSON, connect Code Evidence to answer generation, or change schema.

### Answer Gap Report

```powershell
.\.venv\Scripts\python.exe scripts\build_payroll_output_answer_gap_report.py --coverage-report .\artifacts\eval\payroll_output_corpus_coverage.json
.\.venv\Scripts\python.exe scripts\build_payroll_output_answer_gap_report.py --coverage-report .\artifacts\eval\payroll_output_corpus_coverage.json --json --output .\artifacts\eval\payroll_output_answer_gap_report.json
```

The gap report consumes the coverage diagnostic JSON and recommends the next action for each evidence group.

## Interpreting Benchmark Results

Benchmark results are deterministic regression checks over the loaded Minerva corpus.

- `PASS` means the question met its configured retrieval and answer checks.
- `FAIL` means at least one expected source, source phrase, answer phrase, section, or forbidden-pattern check did not pass.

A failure does not automatically mean answer synthesis is wrong. Common causes are:

- the loaded corpus does not contain enough formal evidence;
- retrieval terms do not find the relevant formal evidence;
- synthesis found evidence but did not express the expected Payroll Output wording;
- another domain owns the question and the routing expectation needs review;
- the benchmark expectation no longer matches the intended product-domain wording.

Investigate failures from the returned source references, failed checks, coverage diagnostic, and answer gap report before changing code.

## Interpreting Coverage Status

The coverage diagnostic classifies each Payroll Output evidence group:

- `STRONG`: multiple relevant chunks or documents were found. The corpus likely has enough retrievable evidence for the group.
- `WEAK`: some relevant evidence was found, but coverage is thin. Answers may be incomplete or overly dependent on one source.
- `MISSING`: no useful evidence was found for the group. Minerva should treat that part of the answer as corpus-limited.

Coverage status is about available formal corpus evidence, not runtime Payroll Output implementation or operational payroll truth. A `MISSING` group may mean the product concept exists but the indexed formal evidence is not loaded or not discoverable yet.

## Interpreting Gap Report Status

The answer gap report summarizes whether Payroll Output answers are ready enough to keep, refine, or defer.

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
- not proof of runtime Payroll Output implementation;
- not proof that Minerva calculates payroll output;
- not proof that Minerva changes payroll output lines;
- not proof that Minerva finalises PayRuns;
- not proof that Minerva approves payroll output;
- not proof that Minerva selects treatments;
- not proof that Minerva selects rates;
- not proof that Minerva generates payment files;
- not proof that Payroll Output alone proves payroll correctness;
- not proof that Run Output and Process Period Output are the same lens;
- not proof that Minerva mutates payroll truth.

Minerva does not calculate payroll output, change output lines, finalise PayRuns, approve output, select treatments, select rates, generate payment files or mutate payroll truth. Payroll Output evaluation must continue to use the indexed formal knowledge corpus. It must not read or ingest source-code content as Minerva answer evidence, and it must not connect Code Evidence Index to answer generation.
