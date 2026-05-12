# Contacts / Employee Appointments Evaluation Runbook

This runbook documents the repeatable Minerva evaluation workflow for Contacts / Employee Appointments. It is intended for regression checks and corpus-readiness diagnostics after retrieval-plan, benchmark, synthesis, diagnostic tooling, or formal corpus changes.

The workflow is diagnostic-only. It does not mutate corpus records, change database schema, ingest operational JSON, call a live LLM, read source-code content as Minerva evidence, or connect Code Evidence Index to answer generation.

## Purpose

Contacts / Employee Appointments evaluation checks whether Minerva can retrieve and synthesize enough formal evidence to answer product-domain questions about Contact identity, EmployeeAppointment employment assignment, appointment-specific context, worker readiness and related cross-domain evidence.

The evaluation answers four practical questions:

- Does the full test suite still pass?
- Does the broad Contacts / Employee Appointments benchmark still pass?
- Do the 10 focused follow-up benchmark questions still pass?
- Does the currently indexed formal corpus contain enough evidence for each Contacts / Employee Appointments evidence group?

Contacts / Employee Appointments evaluation is not proof of runtime Contacts / Employee Appointments truth. It evaluates Minerva retrieval and answer quality over formal knowledge evidence. It is not proof that Contacts / Employee Appointments calculate payroll, that Contact alone is always enough where appointment-specific truth matters, that duplicate full appointments are the correct comparator-classification model, that contact history/readiness surfaces are complete, that dirty-contact propagation is complete, or that Minerva mutates contact or appointment data.

## Domain Retrieval Coverage

The Contacts / Employee Appointments domain retrieval plan is a deterministic evidence-gathering plan for questions about worker identity context and employment assignment context. It splits broad and focused questions into targeted evidence groups and retrieves formal corpus chunks for each group.

The plan covers:

- purpose and operator meaning;
- Contact identity and worker context;
- EmployeeAppointment as employment assignment;
- appointment scope and PayRun admission;
- award classification and position context;
- worksite, state and runtime location;
- ObjectTime / Source Truth connection;
- leave source and leave accrual connection;
- Worker Story and Contact history connection;
- worker readiness across tax, bank, deduction and payment context;
- dirty contact and reprocessing;
- comparison and classification lenses;
- outstanding hardening.

The plan decides what evidence to search for. It does not calculate payroll, prove runtime contact or appointment data, mark contacts dirty, reprocess workers, mutate Contact or EmployeeAppointment records, or replace deterministic Ezeas services. If evidence is weak or missing, Minerva should report the corpus limitation instead of inventing a product claim.

## Difference From Other Evaluations

ObjectTime / Source Truth evaluation checks governed source evidence, source-row inclusion, SourceTruth versus WorkedHours, provenance, corrections and reprocessing. Contacts / Employee Appointments can depend on ObjectTime / Source Truth for source-truth connection and worker inclusion context, but it owns the Contact versus EmployeeAppointment framing and should not treat ObjectTime as appointment identity truth by itself.

Imports / Actuals evaluation checks imported timesheets, imported payroll actuals, source-system mappings and imported actuals as an external outcome lane. Contacts / Employee Appointments may need imported position or classification context, but it does not own import validation or imported actuals truth.

Worker Story evaluation checks the explanation surface for worker-level payroll outcomes and evidence history. Contacts / Employee Appointments checks the worker identity, Contact history and appointment context that Worker Story may need to present.

Leave Source Model evaluation checks leave applicability dimensions, contact versus appointment scope and source precedence. Contacts / Employee Appointments checks how Contact and EmployeeAppointment scope connect to leave source/accrual questions, but it does not decide leave applicability.

Leave Accrual / Processing evaluation checks leave source truth, processed payroll output, LeaveLedger, TAKEN leave valuation and current-effective leave output. Contacts / Employee Appointments can explain the contact/appointment context feeding leave source/accrual, but it does not calculate leave.

PayRun Admin Queue evaluation checks the operator action workbench for blockers, warnings, ready actions, Worker Attention, dirty contacts and finalisation readiness. Contacts / Employee Appointments can explain dirty contact and reprocessing meaning, but ordinary PayRun Admin Queue dirty-contact questions remain owned by PayRun Admin Queue.

Payroll Bases & Totals evaluation checks governed payroll basis evidence, bucket definitions, current-effective truth and rebuild readiness. Contacts / Employee Appointments may explain appointment-specific context such as award, position or worksite, but it does not own payroll basis calculation truth.

Comparison / Remediation evaluation checks comparison lanes, variance, remediation and comparator policy. Contacts / Employee Appointments checks why classification lenses are preferred over duplicate full appointments for comparator classification context, but it does not own remediation generation.

On-costs / Employer Liabilities evaluation checks employer liability evidence such as super, payroll tax, WorkCover / WIC, RateSource and state/worksite/runtime location resolution. Contacts / Employee Appointments can provide worksite/state/runtime location context, but it does not calculate on-costs or employer liabilities.

Award Build / Award Evidence, Tax / PAYG, Deductions / Obligations, Payment Execution / Remittance, Finalisation Readiness, Movement Review, Retro / Replay and other domain evaluations own their specific calculation, readiness, payment, correction, review or evidence concerns. Contacts / Employee Appointments may connect to them through worker identity, appointment context, worker readiness or classification evidence, but it should not be treated as their runtime truth.

All evaluations use deterministic retrieval and benchmark checks. Contacts / Employee Appointments additionally has corpus coverage diagnostics and an answer gap report that classify evidence readiness group by group.

## Commands

Run commands from the repository root.

### Full Pytest Suite

```powershell
.\.venv\Scripts\python.exe -m pytest --basetemp .\.pytest_tmp
```

This is the main regression gate. It should pass before treating any benchmark or diagnostic output as meaningful.

### Contacts / Employee Appointments Benchmark

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.contacts_employee_appointments.json
```

The benchmark includes the broad Contacts / Employee Appointments question plus 10 focused follow-up questions covering Contact versus EmployeeAppointment, PayRun admission, ObjectTime / Source Truth, AwardPositionClass and WorksitePosition, worksite/state/runtime location, leave source/accrual, Worker Story and Contact history, worker readiness, dirty contact and reprocessing, and classification lenses rather than duplicate full appointments.

### Corpus Coverage Diagnostic

```powershell
.\.venv\Scripts\python.exe scripts\scan_contacts_employee_appointments_corpus_coverage.py
.\.venv\Scripts\python.exe scripts\scan_contacts_employee_appointments_corpus_coverage.py --json --output .\artifacts\eval\contacts_employee_appointments_corpus_coverage.json
```

The diagnostic reads the already indexed formal corpus and reports coverage for each Contacts / Employee Appointments evidence group. It does not ingest files, mutate corpus records, call a live LLM, or change schema.

### Answer Gap Report

```powershell
.\.venv\Scripts\python.exe scripts\build_contacts_employee_appointments_answer_gap_report.py --coverage-report .\artifacts\eval\contacts_employee_appointments_corpus_coverage.json
.\.venv\Scripts\python.exe scripts\build_contacts_employee_appointments_answer_gap_report.py --coverage-report .\artifacts\eval\contacts_employee_appointments_corpus_coverage.json --json --output .\artifacts\eval\contacts_employee_appointments_answer_gap_report.json
```

The gap report consumes the coverage diagnostic JSON and recommends the next action for each evidence group.

## Interpreting Benchmark Results

Benchmark results are deterministic regression checks over the loaded Minerva corpus.

- `PASS` means the question met its configured retrieval and answer checks.
- `FAIL` means at least one expected source, source phrase, answer phrase, section, or forbidden-pattern check did not pass.

A failure does not automatically mean answer synthesis is wrong. Common causes are:

- the loaded corpus does not contain enough formal evidence;
- retrieval terms do not find the relevant formal evidence;
- synthesis found evidence but did not express the expected Contacts / Employee Appointments wording;
- another domain owns the question and the routing expectation needs review;
- the benchmark expectation no longer matches the intended product-domain wording.

Investigate failures from the returned source references, failed checks, coverage diagnostic, and answer gap report before changing code.

## Interpreting Coverage Status

The coverage diagnostic classifies each Contacts / Employee Appointments evidence group:

- `STRONG`: multiple relevant chunks or documents were found. The corpus likely has enough retrievable evidence for the group.
- `WEAK`: some relevant evidence was found, but coverage is thin. Answers may be incomplete or overly dependent on one source.
- `MISSING`: no useful evidence was found for the group. Minerva should treat that part of the answer as corpus-limited.

Coverage status is about available formal corpus evidence, not runtime Contact or EmployeeAppointment truth. A `MISSING` group may mean the product concept exists but the indexed formal evidence is not loaded or not discoverable yet.

## Interpreting Gap Report Status

The answer gap report summarizes whether Contacts / Employee Appointments answers are ready enough to keep, refine, or defer.

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
- not proof of runtime Contacts / Employee Appointments truth;
- not proof that Contacts / Employee Appointments calculate payroll;
- not proof that Contact alone is always enough where appointment-specific truth matters;
- not proof that duplicate full appointments are the correct comparator-classification model;
- not proof that contact history/readiness surfaces are complete;
- not proof that dirty-contact propagation is complete;
- not proof that Minerva mutates contact or appointment data.

Contacts / Employee Appointments evaluation must continue to use the indexed formal knowledge corpus. It must not read or ingest source-code content as Minerva answer evidence, and it must not connect Code Evidence Index to answer generation.
