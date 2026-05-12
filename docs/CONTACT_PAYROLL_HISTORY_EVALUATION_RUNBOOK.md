# Contact Payroll History Evaluation Runbook

This runbook documents the repeatable Minerva evaluation workflow for Contact Payroll History. It is intended for regression checks and corpus-readiness diagnostics after retrieval-plan, benchmark, synthesis, diagnostic tooling, or formal corpus changes.

The workflow is diagnostic-only. It does not mutate corpus records, change database schema, ingest operational JSON, call a live LLM, read source-code content as Minerva evidence, or connect Code Evidence Index to answer generation. It also provides no Code Evidence answer integration.

## Purpose

Contact Payroll History evaluation checks whether Minerva can retrieve and synthesize enough formal evidence to answer product-domain questions about contact/worker-level payroll history, PayRun participation, current and historical payroll output, Gross-to-Net history, deductions and obligations, tax/payment readiness, leave/accrual evidence, Worker Story links, Movement Review and PayRun Admin Queue context, and Retro / Replay correction context.

The evaluation answers four practical questions:

- Does the full test suite still pass?
- Does the broad Contact Payroll History benchmark still pass?
- Do the focused follow-up benchmark questions still pass?
- Does the currently indexed formal corpus contain enough evidence for each Contact Payroll History evidence group?

Contact Payroll History evaluation is not proof of runtime Contact Payroll History implementation. It evaluates Minerva retrieval and answer quality over formal knowledge evidence. It is not proof that Minerva calculates payroll history, changes historical payroll records, corrects payroll outcomes, performs retro/replay, approves payroll changes, finalises PayRuns or mutates payroll truth. It is also not proof that Contact Payroll History alone proves payroll correctness or that historical evidence should overwrite finalised truth.

## Domain Retrieval Coverage

The Contact Payroll History domain retrieval plan is a deterministic evidence-gathering plan for questions about historical payroll evidence at the contact or worker lens. It splits broad and focused questions into targeted evidence groups and retrieves formal corpus chunks for each group.

The plan covers:

- Contact Payroll History purpose and operator meaning;
- contact identity and PayRun participation;
- contact/worker-level payroll history across process periods and PayRuns;
- current and historical payroll output;
- Gross-to-Net history;
- deductions and obligations, including negative net pay history;
- tax/payment readiness history, including payment allocation and bank/payment destination context where formal evidence supports it;
- leave/accrual evidence over time;
- Worker Story relationship for worker-level evidence explanation;
- Movement Review and PayRun Admin Queue relationship for review context and action/workbench context;
- Retro / Replay and correction context;
- outstanding hardening.

The plan decides what evidence to search for. It does not calculate payroll history, change historical records, correct payroll outcomes, perform retro/replay, approve payroll changes, finalise PayRuns, prove payroll correctness, or mutate payroll truth. If evidence is weak or missing, Minerva should report the corpus limitation instead of inventing a product claim.

## Difference From Other Evaluations

Contacts / Employee Appointments evaluation owns contact identity, EmployeeAppointment context, worker context, employment assignment, PayRun admission, worksite/state/runtime location and appointment-related source truth. Contact Payroll History may use contact identity as a lens, but it owns historical payroll evidence for that contact or worker.

Payroll Output evaluation owns calculated output evidence, current-effective output truth, Run Output and Process Period Output lenses, payroll lines and output totals. Contact Payroll History consumes output evidence historically and at contact/worker level; it does not replace Payroll Output.

Gross-to-Net evaluation owns the outcome explanation from gross earnings through taxable basis, PAYG, deductions, obligations and net pay. Contact Payroll History can show Gross-to-Net history, but Gross-to-Net owns the current outcome explanation surface.

Worker Story evaluation owns the broader worker-level narrative, evidence chapters, line proof and audit context. Contact Payroll History is the historical/contact lens, while Worker Story remains the worker-level evidence explanation.

Deductions / Obligations evaluation owns deduction templates, worker deduction instructions, reducing-balance obligations, recovery, skipped/partial deductions and obligation ledgers. Contact Payroll History can show deduction and obligation history without owning deduction policy.

Tax / PAYG evaluation owns PAYG withholding evidence, TaxStory, taxable basis alignment, worker tax declarations and tax provider/service boundaries. Contact Payroll History can show tax/PAYG history and tax readiness evidence, but it does not withhold tax.

Payment Execution / Remittance evaluation owns payment files, payment destinations, bank allocation, third-party remittance and payment execution readiness. Contact Payroll History can show payment allocation and payment readiness history, but readiness is not payment file generation.

Retro / Replay evaluation owns retro, replay, correction pathways, attributed-period versus paid-period treatment and dependency detection. Contact Payroll History can provide historical payroll evidence and correction context, but it does not perform retro/replay or corrections.

Movement Review evaluation owns variance, review-worthy movement, reasonableness, comparable periods and worker/organisation review lenses. Contact Payroll History can provide historical context for review, but it is not the variance/reasonableness surface.

PayRun Admin Queue evaluation owns the action/workbench surface for blockers, warnings, ready actions, dirty contact/reprocessing actions and finalisation readiness. Contact Payroll History can link to queue context, but Admin Queue owns what needs action now.

All evaluations use deterministic retrieval and benchmark checks. Contact Payroll History additionally has corpus coverage diagnostics and an answer gap report that classify evidence readiness group by group.

## Commands

Run commands from the repository root.

### Full Pytest Suite

```powershell
.\.venv\Scripts\python.exe -m pytest --basetemp .\.pytest_tmp
```

This is the main regression gate. It should pass before treating any benchmark or diagnostic output as meaningful.

### Contact Payroll History Benchmark

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.contact_payroll_history.json
```

The benchmark includes the broad question, "What is Contact Payroll History in the platform?", plus focused follow-up questions about PayRun participation, current and historical payroll output, deductions/obligations/negative net pay, tax/payment readiness, leave/accrual/Worker Story relationships, and retro/replay/correction context.

### Corpus Coverage Diagnostic

```powershell
.\.venv\Scripts\python.exe scripts\scan_contact_payroll_history_corpus_coverage.py
.\.venv\Scripts\python.exe scripts\scan_contact_payroll_history_corpus_coverage.py --json --output .\artifacts\eval\contact_payroll_history_corpus_coverage.json
```

The diagnostic reads the already indexed formal corpus and reports coverage for each Contact Payroll History evidence group. It does not ingest files, mutate corpus records, call a live LLM, ingest operational JSON, connect Code Evidence to answer generation, or change schema.

### Answer Gap Report

```powershell
.\.venv\Scripts\python.exe scripts\build_contact_payroll_history_answer_gap_report.py --coverage-report .\artifacts\eval\contact_payroll_history_corpus_coverage.json
.\.venv\Scripts\python.exe scripts\build_contact_payroll_history_answer_gap_report.py --coverage-report .\artifacts\eval\contact_payroll_history_corpus_coverage.json --json --output .\artifacts\eval\contact_payroll_history_answer_gap_report.json
```

The gap report consumes the coverage diagnostic JSON and recommends the next action for each evidence group.

## Interpreting Benchmark Results

Benchmark results are deterministic regression checks over the loaded Minerva corpus.

- `PASS` means the question met its configured retrieval and answer checks.
- `FAIL` means at least one expected source, source phrase, answer phrase, section, or forbidden-pattern check did not pass.

A failure does not automatically mean answer synthesis is wrong. Common causes are:

- the loaded corpus does not contain enough formal evidence;
- retrieval terms do not find the relevant formal evidence;
- synthesis found evidence but did not express the expected Contact Payroll History wording;
- another domain owns the question and the routing expectation needs review;
- the benchmark expectation no longer matches the intended product-domain wording.

Investigate failures from the returned source references, failed checks, coverage diagnostic, and answer gap report before changing code.

## Interpreting Coverage Status

The coverage diagnostic classifies each Contact Payroll History evidence group:

- `STRONG`: multiple relevant chunks or documents were found. The corpus likely has enough retrievable evidence for the group.
- `WEAK`: some relevant evidence was found, but coverage is thin. Answers may be incomplete or overly dependent on one source.
- `MISSING`: no useful evidence was found for the group. Minerva should treat that part of the answer as corpus-limited.

Coverage status is about available formal corpus evidence, not runtime Contact Payroll History implementation or operational payroll truth. A `MISSING` group may mean the product concept exists but the indexed formal evidence is not loaded or not discoverable yet.

## Interpreting Gap Report Status

The answer gap report summarizes whether Contact Payroll History answers are ready enough to keep, refine, or defer.

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
- not proof of runtime Contact Payroll History implementation;
- not proof that Minerva calculates payroll history;
- not proof that Minerva changes historical payroll records;
- not proof that Minerva corrects payroll outcomes;
- not proof that Minerva performs retro/replay;
- not proof that Minerva approves payroll changes;
- not proof that Minerva finalises PayRuns;
- not proof that Contact Payroll History alone proves payroll correctness;
- not proof that historical evidence should overwrite finalised truth;
- not proof that Minerva mutates payroll truth.

Minerva does not calculate payroll history, change historical records, correct payroll outcomes, perform retro/replay, approve payroll changes, finalise PayRuns or mutate payroll truth. Contact Payroll History evaluation must continue to use the indexed formal knowledge corpus. It must not read or ingest source-code content as Minerva answer evidence, and it must not connect Code Evidence Index to answer generation.
