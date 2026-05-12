# Leave Requests / Leave Workflow Evaluation Runbook

This runbook documents the repeatable Minerva evaluation workflow for Leave Requests / Leave Workflow. It is intended for regression checks and corpus-readiness diagnostics after retrieval-plan, benchmark, synthesis, diagnostic tooling, or formal corpus changes.

The workflow is diagnostic-only. It does not mutate corpus records, change database schema, ingest operational JSON, call a live LLM, read source-code content as Minerva evidence, or connect Code Evidence Index to answer generation. It also provides no Code Evidence answer integration and does not prove runtime operational truth.

## Purpose

Leave Requests / Leave Workflow evaluation checks whether Minerva can retrieve and synthesize enough formal evidence to answer product-domain questions about the governed workflow for creating, submitting, reviewing, approving, rejecting, reopening, valuing, posting and explaining leave requests.

The evaluation answers four practical questions:

- Does the full test suite still pass?
- Does the broad Leave Requests / Leave Workflow benchmark still pass?
- Do the focused follow-up benchmark questions still pass?
- Does the currently indexed formal corpus contain enough evidence for each Leave Requests / Leave Workflow evidence group?

Leave Requests / Leave Workflow evaluation is not proof of runtime Leave Request implementation. It evaluates Minerva retrieval and answer quality over formal knowledge evidence. Minerva explains Leave Requests / Leave Workflow. Minerva does not approve leave, calculate leave, post LeaveLedger rows, change leave balances, reopen leave requests, resolve shortfalls, finalise PayRuns or mutate operational leave/payroll truth.

Explicit Minerva boundary:

- Minerva does not approve leave.
- Minerva does not calculate leave.
- Minerva does not post LeaveLedger rows.
- Minerva does not change leave balances.
- Minerva does not reopen leave requests.
- Minerva does not resolve shortfalls.
- Minerva does not finalise PayRuns.
- Minerva does not mutate operational leave/payroll truth.

## Domain Retrieval Coverage

The Leave Requests / Leave Workflow domain retrieval plan is a deterministic evidence-gathering plan for questions about governed employee leave request workflow evidence. It splits broad and focused questions into targeted evidence groups and retrieves formal corpus chunks for each group.

The v0.3 corpus coverage diagnostic covers:

- `request_lifecycle_and_status_transitions`;
- `preview_overlap_and_shortfall_handling`;
- `taken_leave_valuation_and_hard_fail`;
- `leaveledger_posting_and_balance_effects`;
- `leave_source_and_applicability_relationship`;
- `worker_story_payrun_and_finalisation_relationship`;
- `idempotency_reopen_and_approval_governance`;
- `minerva_boundaries_and_non_mutation_guardrails`.

The domain covers request lifecycle, draft/submission/review/approval/rejection/reopen transitions, preview, overlap and shortfall handling, TAKEN leave valuation, LeaveLedger posting, leave balance effects, Leave Source Model and applicability caveats, Worker Story, PayRun and finalisation readiness relationships, idempotency and approval governance, and Minerva non-mutation guardrails.

The plan decides what evidence to search for. It does not approve leave, calculate leave, value leave, post LeaveLedger rows, change leave balances, reopen requests, resolve shortfalls, finalise PayRuns, prove operational correctness, or mutate leave/payroll truth. If evidence is weak or missing, Minerva should report the corpus limitation instead of inventing a product claim.

## Difference From Other Evaluations

Leave Accrual / Processing evaluation owns deterministic leave accrual, processing, leave valuation basis and payroll/leave output behavior. Leave Requests / Leave Workflow can explain request payment effects and workflow links, but it does not calculate leave.

Leave Source Model evaluation owns governed leave applicability and source-truth caveats. Leave Requests / Leave Workflow must preserve the Leave Source Model caveat and must not treat LeaveTypeRule alone as final leave applicability truth.

Payroll Output evaluation owns calculated payroll output, output lines and current-effective output truth. Leave Requests / Leave Workflow may connect leave requests to payroll output effects, but Leave Requests alone does not prove payroll correctness.

Worker Story evaluation owns worker-level evidence narrative and Leave and Accrual Outcome explanation. Leave Requests / Leave Workflow can link to Worker Story, but it does not replace the worker evidence surface.

Finalisation Readiness evaluation owns readiness gates, blockers, warnings and PayRun finalisation safety. Leave Requests / Leave Workflow can explain leave readiness relationships, but it does not finalise PayRuns.

Contact Payroll History evaluation owns historical contact/worker payroll evidence. Leave Requests / Leave Workflow can connect to historical leave/payroll evidence where supported, but it does not rewrite history.

Deductions / Obligations and Gross-to-Net own explicit net-pay, deduction, obligation and payroll outcome explanation contexts. Leave Requests / Leave Workflow must not collapse request workflow evidence into deduction or net-pay ownership.

All evaluations use deterministic retrieval and benchmark checks. Leave Requests / Leave Workflow additionally has corpus coverage diagnostics and an answer gap report that classify evidence readiness group by group.

## Commands

Run commands from the repository root.

### Full Pytest Suite

```powershell
.\.venv\Scripts\python.exe -m pytest --basetemp .\.pytest_tmp
```

This is the main regression gate. It should pass before treating any benchmark or diagnostic output as meaningful.

### Leave Requests / Leave Workflow Benchmark

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.leave_requests_workflow.json
```

The benchmark includes the broad question, "What is Leave Requests / Leave Workflow in the platform?", plus focused follow-up questions about draft-to-approval lifecycle, preview/overlap/shortfall handling, TAKEN leave valuation, LeaveLedger posting and balance effects, Leave Source/applicability, and Worker Story/PayRun/finalisation readiness relationships.

### Focused Contract And Routing Tests

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_leave_requests_workflow_corpus_coverage.py tests\test_leave_requests_workflow_answer_gap_report.py tests\test_domain_retrieval_plans.py tests\test_rich_answer_contract.py --basetemp .\.pytest_tmp
```

Use this when touching Leave Requests / Leave Workflow benchmark, routing, diagnostic, answer gap report or documentation behavior.

### Corpus Coverage Diagnostic

Human-readable mode:

```powershell
.\.venv\Scripts\python.exe scripts\scan_leave_requests_workflow_corpus_coverage.py
```

JSON mode:

```powershell
.\.venv\Scripts\python.exe scripts\scan_leave_requests_workflow_corpus_coverage.py --json
```

Write diagnostic JSON to a file:

```powershell
.\.venv\Scripts\python.exe scripts\scan_leave_requests_workflow_corpus_coverage.py --json --output .\artifacts\eval\leave_requests_workflow_corpus_coverage.json
```

The diagnostic reads the already indexed formal corpus and reports coverage for each Leave Requests / Leave Workflow evidence group. It does not ingest files, mutate corpus records, call a live LLM, ingest operational JSON, connect Code Evidence to answer generation, or change schema.

### Answer Gap Report

Human-readable mode:

```powershell
.\.venv\Scripts\python.exe scripts\build_leave_requests_workflow_answer_gap_report.py --coverage-report .\artifacts\eval\leave_requests_workflow_corpus_coverage.json
```

JSON mode:

```powershell
.\.venv\Scripts\python.exe scripts\build_leave_requests_workflow_answer_gap_report.py --coverage-report .\artifacts\eval\leave_requests_workflow_corpus_coverage.json --json
```

Write answer gap report JSON to a file:

```powershell
.\.venv\Scripts\python.exe scripts\build_leave_requests_workflow_answer_gap_report.py --coverage-report .\artifacts\eval\leave_requests_workflow_corpus_coverage.json --json --output .\artifacts\eval\leave_requests_workflow_answer_gap_report.json
```

The gap report consumes the coverage diagnostic JSON and recommends the next action for each evidence group.

## Interpreting Benchmark Results

Benchmark results are deterministic regression checks over the loaded Minerva corpus.

- `PASS` means the question met its configured retrieval and answer checks.
- `FAIL` means at least one expected source, source phrase, answer phrase, section, answer mode, routing, or forbidden-pattern check did not pass.

A failure does not automatically mean answer synthesis is wrong. Common causes are:

- the loaded corpus does not contain enough formal evidence;
- retrieval terms do not find the relevant formal evidence;
- synthesis found evidence but did not express the expected Leave Requests / Leave Workflow wording;
- another domain owns the question and the routing expectation needs review;
- the benchmark expectation no longer matches the intended product-domain wording.

Investigate failures from the returned source references, failed checks, coverage diagnostic, and answer gap report before changing code.

## Interpreting Coverage Status

The coverage diagnostic classifies each Leave Requests / Leave Workflow evidence group:

- `STRONG`: multiple relevant chunks or documents were found. The corpus likely has enough retrievable evidence for the group.
- `WEAK`: some relevant evidence was found, but coverage is thin. Answers may be incomplete or overly dependent on one source.
- `MISSING`: no useful evidence was found for the group. Minerva should treat that part of the answer as corpus-limited.

Coverage status is about available formal corpus evidence, not runtime Leave Request implementation or operational leave/payroll truth. A `MISSING` group may mean the product concept exists but the indexed formal evidence is not loaded or not discoverable yet.

## Interpreting Gap Report Status

The answer gap report summarizes whether Leave Requests / Leave Workflow answers are ready enough to keep, refine, or defer.

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
- Improve synthesis when coverage is `STRONG` but benchmark or human review shows the answer is incomplete, too broad, or missing required Leave Requests / Leave Workflow guardrails.
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
- not proof of runtime Leave Request implementation;
- not proof of runtime operational truth;
- not proof that Minerva approves leave;
- not proof that Minerva calculates leave;
- not proof that Minerva posts LeaveLedger rows;
- not proof that Minerva changes leave balances;
- not proof that Minerva reopens leave requests;
- not proof that Minerva resolves shortfalls;
- not proof that Minerva finalises PayRuns;
- not proof that Minerva mutates operational leave/payroll truth.

Diagnostics do not approve, post, reopen, resolve or finalise anything. Minerva does not approve leave, calculate leave, post LeaveLedger rows, change leave balances, reopen leave requests, resolve shortfalls, finalise PayRuns or mutate operational leave/payroll truth. Leave Requests / Leave Workflow evaluation must continue to use the indexed formal knowledge corpus. It must not read or ingest source-code content as Minerva answer evidence, and it must not connect Code Evidence Index to answer generation.
