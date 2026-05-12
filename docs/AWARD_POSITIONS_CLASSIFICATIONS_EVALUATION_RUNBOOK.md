# Award Positions / Classifications Evaluation Runbook

This runbook documents the repeatable Minerva evaluation workflow for Award Positions / Classifications. It is intended for regression checks and corpus-readiness diagnostics after retrieval-plan, benchmark, synthesis, diagnostic tooling, or formal corpus changes.

The workflow is diagnostic-only. It does not mutate corpus records, change database schema, ingest operational JSON, call a live LLM, read source-code content as Minerva evidence, or connect Code Evidence Index to answer generation. It also provides no Code Evidence answer integration and is not proof of runtime operational truth.

## Purpose

Award Positions / Classifications is the Minerva product-domain explaining governed award position/classification evidence; AwardPosition and AwardPositionClass source/build evidence; EmployeeAppointment / WorksitePosition / Position assignment context; classification relationship to RateSource, Rate Story, Decision Story and Payroll Output; comparison/remediation classification lenses; Worker Story / Admin Queue / Worker Attention / Finalisation Readiness relationships.

The evaluation answers four practical questions:

- Does the full test suite still pass?
- Does the Award Positions / Classifications broad and focused rich-answer benchmark still pass?
- Do award-position/classification-framed questions still route to the Award Positions / Classifications domain while overlapping domains keep ownership?
- Does the currently indexed formal corpus contain enough evidence for each Award Positions / Classifications evidence group?

Award Positions / Classifications evaluation is not proof of runtime award classification implementation. It evaluates Minerva retrieval and answer quality over formal knowledge evidence. Minerva explains Award Positions / Classifications. Minerva does not classify workers, change EmployeeAppointment, WorksitePosition, Position or AwardPositionClass records, select award classes at runtime, interpret awards at runtime, calculate payroll, decide entitlements, mutate payroll output, determine finalisation readiness, finalise PayRuns, or mutate operational workforce/payroll/award truth.

Explicit Minerva boundary:

- Minerva explains Award Positions / Classifications.
- Minerva does not classify workers.
- Minerva does not change EmployeeAppointment, WorksitePosition, Position or AwardPositionClass records.
- Minerva does not select award classes at runtime.
- Minerva does not interpret awards at runtime.
- Minerva does not calculate payroll.
- Minerva does not decide entitlements.
- Minerva does not mutate payroll output.
- Minerva does not determine finalisation readiness.
- Minerva does not finalise PayRuns.
- Minerva does not mutate operational workforce/payroll/award truth.

## Domain Retrieval Coverage

The Award Positions / Classifications domain retrieval plan is a deterministic evidence-gathering plan for questions about governed award position, award class, employment classification and assignment-context evidence. It splits broad and focused questions into targeted evidence groups and retrieves formal corpus chunks for each group.

The v0.3 corpus coverage diagnostic covers:

- `award_position_classification_source_and_build`;
- `appointment_position_and_worksite_assignment`;
- `payroll_interpretation_rate_and_decision_story`;
- `comparison_remediation_and_classification_lenses`;
- `worker_story_admin_queue_and_readiness_relationship`;
- `minerva_boundaries_and_non_mutation_guardrails`.

The domain covers award build extraction/configuration, AwardPosition, AwardPositionClass, PositionClass, classification levels, position groups, pay guide and class evidence, EmployeeAppointment / WorksitePosition / Position / Worksite assignment context, classification context for RateSource, Rate Story, Decision Story, Payroll Output and calculated line evidence, comparator classification, imported classification mapping, classification lenses, primary appointment class boundaries, Worker Story, Admin Queue, Worker Attention, Finalisation Readiness, NEEDS_CONFIGURATION-style concepts and Minerva non-mutation guardrails.

The plan decides what evidence to search for. It does not classify workers, change EmployeeAppointment, WorksitePosition, Position or AwardPositionClass records, select award classes at runtime, interpret awards at runtime, calculate payroll, decide entitlements, mutate payroll output, determine finalisation readiness, finalise PayRuns, prove operational correctness, or mutate workforce/payroll/award truth. If evidence is weak or missing, Minerva should report the corpus limitation instead of inventing a product claim.

## Difference From Other Evaluations

Award Build / Award Evidence evaluation owns award build/source evidence questions that are not specifically classification-framed. Award Positions / Classifications can explain AwardPosition and AwardPositionClass source/build evidence, but it does not replace the broader award build evidence domain.

Contacts / Employee Appointments evaluation owns generic contact, appointment and work assignment questions. Award Positions / Classifications can explain how EmployeeAppointment, WorksitePosition, Position and Worksite connect to classification evidence when the question is classification-framed.

RateSource / Rate Story, Decision Story and Payroll Output own generic rate, treatment explanation and payroll output questions. Award Positions / Classifications can explain classification context for those surfaces, but it does not own generic rate selection, treatment explanation or output-line questions.

Comparison / Remediation owns broad comparison and remediation questions. Award Positions / Classifications can explain comparator classification, imported classification mapping and classification lenses, while preserving that comparator classes do not automatically replace the primary appointment class.

Rosters / Patterns / Scheduling, ObjectTime / Source Truth, Worker Story, Finalisation Readiness, Worker Attention / Issue Resolution and Imports / Actuals keep ownership of their generic domains. Award Positions / Classifications can explain relationships to those surfaces only when the question is award-position/classification-framed.

## Commands

Run commands from the repository root.

### Full Pytest Suite

```powershell
.\.venv\Scripts\python.exe -m pytest --basetemp .\.pytest_tmp
```

This is the main regression gate. It should pass before treating any benchmark or diagnostic output as meaningful.

### Award Positions / Classifications Benchmark

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.award_positions_classifications.json
```

The benchmark includes the broad question, "How do Award Positions and Classifications work in the platform?", plus focused follow-up questions about award evidence creation, EmployeeAppointment connection, RateSource / Rate Story / Payroll Output, Decision Story, comparison/remediation classification lenses, and missing or unresolved classification evidence.

### Focused Contract And Routing Tests

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_award_positions_classifications_corpus_coverage.py tests\test_award_positions_classifications_answer_gap_report.py tests\test_domain_retrieval_plans.py tests\test_rich_answer_contract.py --basetemp .\.pytest_tmp
```

Use this when touching Award Positions / Classifications benchmark, routing, diagnostic, answer gap report or documentation behavior.

### Corpus Coverage Diagnostic

Human-readable mode:

```powershell
.\.venv\Scripts\python.exe scripts\scan_award_positions_classifications_corpus_coverage.py
```

JSON mode:

```powershell
.\.venv\Scripts\python.exe scripts\scan_award_positions_classifications_corpus_coverage.py --json
```

Write diagnostic JSON to a file:

```powershell
.\.venv\Scripts\python.exe scripts\scan_award_positions_classifications_corpus_coverage.py --json --output .\artifacts\eval\award_positions_classifications_corpus_coverage.json
```

The diagnostic reads the already indexed formal corpus and reports coverage for each Award Positions / Classifications evidence group. It does not ingest files, mutate corpus records, call a live LLM, ingest operational JSON, connect Code Evidence to answer generation, or change schema.

### Answer Gap Report

Human-readable mode:

```powershell
.\.venv\Scripts\python.exe scripts\build_award_positions_classifications_answer_gap_report.py --coverage-report .\artifacts\eval\award_positions_classifications_corpus_coverage.json
```

JSON mode:

```powershell
.\.venv\Scripts\python.exe scripts\build_award_positions_classifications_answer_gap_report.py --coverage-report .\artifacts\eval\award_positions_classifications_corpus_coverage.json --json
```

Write answer gap report JSON to a file:

```powershell
.\.venv\Scripts\python.exe scripts\build_award_positions_classifications_answer_gap_report.py --coverage-report .\artifacts\eval\award_positions_classifications_corpus_coverage.json --json --output .\artifacts\eval\award_positions_classifications_answer_gap_report.json
```

The gap report consumes the coverage diagnostic JSON and recommends the next action for each evidence group.

## Interpreting Benchmark Results

Benchmark results are deterministic regression checks over the loaded Minerva corpus.

- `PASS` means the question met its configured retrieval and answer checks.
- `FAIL` means at least one expected source, source phrase, answer phrase, section, answer mode, routing, or forbidden-pattern check did not pass.

A failure does not automatically mean answer synthesis is wrong. Common causes are:

- the loaded corpus does not contain enough formal evidence;
- retrieval terms do not find the relevant formal evidence;
- synthesis found evidence but did not express the expected Award Positions / Classifications wording;
- another domain owns the question and the routing expectation needs review;
- the benchmark expectation no longer matches the intended product-domain wording.

Investigate failures from the returned source references, failed checks, coverage diagnostic, and answer gap report before changing code.

## Interpreting Coverage Status

The coverage diagnostic classifies each Award Positions / Classifications evidence group:

- `STRONG`: multiple relevant chunks or documents were found. The corpus likely has enough retrievable evidence for the group.
- `WEAK`: some relevant evidence was found, but coverage is thin. Answers may be incomplete or overly dependent on one source.
- `MISSING`: no useful evidence was found for the group. Minerva should treat that part of the answer as corpus-limited.

Coverage status is about available formal corpus evidence, not runtime award classification, appointment, payroll or award truth. A `MISSING` group may mean the product concept exists but the indexed formal evidence is not loaded or not discoverable yet.

## Interpreting Gap Report Status

The answer gap report summarizes whether Award Positions / Classifications answers are ready enough to keep, refine, or defer.

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

## When To Improve What

- Improve retrieval terms when formal evidence exists but diagnostic coverage is `WEAK` because the scanner is not finding enough relevant corpus support.
- Improve synthesis when coverage is `STRONG` but benchmark or human review shows the answer is incomplete, too broad, or missing required Award Positions / Classifications guardrails.
- Add formal source evidence later when the group is genuinely `MISSING` from the indexed formal corpus.
- Keep existing behavior where coverage and answer quality are acceptable.
- Do not use operational JSON or Code Evidence as a shortcut for missing formal source evidence.

## Guardrails

This workflow must remain:

- diagnostic-only;
- no corpus mutation;
- no live LLM calls;
- no database schema change;
- no operational JSON ingestion;
- no Code Evidence answer integration;
- no Code Evidence Index answer integration;
- not proof of runtime award position/classification implementation;
- not proof of runtime operational truth;
- diagnostics do not mutate corpus;
- diagnostics do not call a live LLM;
- diagnostics do not ingest operational JSON;
- diagnostics do not connect Code Evidence to answer generation;
- diagnostics do not prove runtime operational truth;
- diagnostics do not classify workers;
- diagnostics do not change EmployeeAppointment, WorksitePosition, Position or AwardPositionClass records;
- diagnostics do not select award classes at runtime;
- diagnostics do not interpret awards at runtime;
- diagnostics do not calculate payroll;
- diagnostics do not decide entitlements;
- diagnostics do not mutate payroll output;
- diagnostics do not determine or finalise readiness;
- diagnostics do not mutate operational workforce/payroll/award truth.

Diagnostics do not classify, change, select, interpret, calculate, decide, mutate, determine readiness or finalise anything. Minerva does not classify workers, change EmployeeAppointment, WorksitePosition, Position or AwardPositionClass records, select award classes at runtime, interpret awards at runtime, calculate payroll, decide entitlements, mutate payroll output, determine finalisation readiness, finalise PayRuns or mutate operational workforce/payroll/award truth. Award Positions / Classifications evaluation must continue to use the indexed formal knowledge corpus. It must not read or ingest source-code content as Minerva answer evidence, and it must not connect Code Evidence Index to answer generation.
