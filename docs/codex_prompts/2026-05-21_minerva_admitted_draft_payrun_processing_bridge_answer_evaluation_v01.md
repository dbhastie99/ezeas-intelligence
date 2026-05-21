# Prompt Artefact: Minerva Admitted Draft PayRun Processing Bridge Answer Evaluation v0.1

Date: 2026-05-21

Repository: ezeas-intelligence

Slice: Admitted Draft PayRun Processing Bridge Answer Evaluation v0.1

Boundary: evaluation-only, no runtime changes, no workforce-platform changes, no database migrations, no live LLM calls, no external service calls, no production chat exposure, no endpoint/UI changes, no corpus mutation except controlled local evaluation artefacts, no payroll calculation logic, and no Minerva payroll decisioning.

## Objective

Implement deterministic evaluation / answer-behaviour coverage proving that Minerva can answer the Admitted Draft PayRun Processing Bridge golden questions safely and accurately from the preserved knowledge pack.

The source-response blocker has been resolved and committed.

Existing committed source authority:
`docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1_source_response.md`

Existing committed structured knowledge pack:
`docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1.md`

The structured pack was built from the reconstructed canonical source response. The source-response file is authoritative. The structured document is navigational and answer-oriented.

## Runtime And Scope Boundary

This slice must not implement runtime retrieval changes unless an existing test-only harness already supports this safely.

The Workforce Platform runtime bridge may be running separately, but this Minerva slice must not claim that runtime implementation exists unless evidence already exists inside ezeas-intelligence and is explicitly in scope.

Minerva should answer this domain as doctrine/design/current intended bridge behaviour, not as completed runtime execution unless later implementation evidence is ingested.

## Core Doctrine To Preserve

source change -> impact assessment -> action register -> PayRunActionDecision -> admission authority -> PayRun / PayRunContact resolved or created where authorised -> deterministic draft PayRunContact processing -> calculated draft payroll output -> evidence/story -> readiness update

Required answer boundaries:

- admission is not processing;
- PayRunActionDecision remains the authority source;
- the bridge must not decide inclusion independently;
- the bridge must not create PayRuns or PayRunContacts unless authorised;
- processing must use deterministic Workforce Platform services;
- Minerva must not calculate payroll outcomes;
- the bridge must reuse existing deterministic processing paths;
- if the existing processing path is unsafe or unclear, the bridge must stop with a blocker;
- the bridge processes only draft/unfinalised/unfrozen PayRuns;
- finalised, paid, frozen, payment-batch-generated or bank-file-generated PayRuns must not be silently mutated;
- ProcessPeriod.LifecycleStatusCode is payroll-control truth;
- IsOpen/IsClosed alone is insufficient;
- ObjectTime payroll impact is worker-period scoped;
- idempotency is required;
- evidence/story continuity is required;
- readiness is an operator/control consequence, not a substitute for calculation.

## Strict Non-Goals

- no workforce-platform changes;
- no runtime bridge implementation;
- no database migrations;
- no live LLM calls;
- no external service calls;
- no production chat exposure;
- no endpoint/UI changes;
- no corpus mutation unless existing repo convention explicitly treats local fixture/evaluation docs as controlled test artefacts;
- no payroll calculation logic;
- no Minerva payroll decisioning;
- no finalisation;
- no payment;
- no bank file;
- no payment batch;
- no retro execution;
- no manual adjustment execution;
- no broad automation ladder;
- no parallel payroll processor.

## Expected Implementation

Follow existing ezeas-intelligence conventions for benchmark/evaluation/golden-question tests. Inspect nearby patterns, especially:

- `tests/test_worker_story_baseline_capture_pilot.py`
- `tests/test_completed_domain_baseline_decision_ledger.py`
- `tests/test_rich_answer_contract.py`
- tests or fixtures that evaluate deterministic answer guidance
- `docs/evaluation/`
- `docs/knowledge/payroll/`

Add:

1. `docs/evaluation/admitted_draft_payrun_processing_bridge_v0_1/ANSWER_EVALUATION_BASELINE.md`
2. `tests/test_admitted_draft_payrun_processing_bridge_answer_evaluation.py`

The evaluation baseline should include domain name, source-response path, structured knowledge path, evaluation status, all 20 golden questions, expected answer themes for each question, prohibited answer claims where relevant, required caveats where implementation/runtime state must not be overstated, answer-boundary summary, and no-runtime/no-live-LLM/no-DB/no-workforce-platform-change attestation.

## Golden Questions

Use the exact 20 golden questions from `docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1_source_response.md`:

1. What is the Admitted Draft PayRun Processing Bridge?
2. Why is this bridge needed after PayRun admission?
3. What is the canonical governed path from source change to readiness update?
4. Why does PayRunActionDecision remain the authority source?
5. Can the bridge create a PayRun by itself?
6. Can the bridge create a PayRunContact by itself?
7. What guardrails protect finalised, frozen, paid, or payment-batch-generated PayRuns?
8. Why must the bridge use existing deterministic processing paths?
9. What should happen if the existing processing path is unsafe or unclear?
10. Why must Minerva not calculate payroll outcomes?
11. What is the difference between admission and processing?
12. Why is ObjectTime payroll impact worker-period scoped?
13. What idempotency risks does the bridge need to prevent?
14. What evidence should the bridge preserve?
15. How should readiness be updated after processing?
16. What may this slice implement?
17. What must this slice not implement?
18. Why is this a large but bounded slice?
19. How should Minerva explain admitted draft processing without overstating runtime behaviour?
20. How does this bridge preserve deterministic payroll authority?

## Expected Answer Themes

For each golden question, define concise expected answer themes.

Examples:

- Q1 should state the bridge is a controlled handoff from authorised admission into deterministic draft PayRunContact processing.
- Q4 should state PayRunActionDecision/admission authority controls inclusion and creation authority.
- Q5 and Q6 should clearly answer that the bridge cannot create PayRun/PayRunContact on its own authority.
- Q7 should name draft/unfinalised/unfrozen guardrails and protection of finalised/paid/frozen/payment-batch/bank-file states.
- Q8 and Q9 should state the bridge must reuse existing deterministic processing paths and stop with blocker if unsafe.
- Q10 should state Minerva is advisory/evidence intelligence only and must not calculate gross/net/tax/deductions/entitlements/payment/bank-file values.
- Q11 should distinguish admission from processing.
- Q12 should explain worker-period scope.
- Q13 should discuss duplicate PayRuns, PayRunContacts, admission records, result lines, readiness records, and evidence.
- Q14 should include source truth, action, decision, admission, target PayRun, PayRunContact, processing outcome, blockers, readiness consequence, and actions not taken.
- Q19 should require caveated doctrine/design phrasing and prohibit claiming runtime implementation unless evidence exists.
- Q20 should explain deterministic authority through governed admission, deterministic processing service reuse, guardrails, idempotency, evidence/story, and Minerva advisory boundary.

## Prohibited Answer Claims

The evaluation must explicitly prohibit claims such as:

- Minerva calculates payroll outcomes.
- The bridge finalises PayRuns.
- The bridge pays workers.
- The bridge creates bank files.
- The bridge can mutate finalised/paid/frozen PayRuns.
- Admission is the same as processing.
- PayRunActionDecision is optional.
- IsOpen/IsClosed alone is enough lifecycle truth.
- ObjectTime impact is only row-scoped.
- The bridge may invent a parallel payroll processor.
- The runtime bridge is implemented and live, unless implementation evidence is later ingested and tested.
- The structured knowledge document replaces the source response.

## Testing Requirements

The focused test should verify:

1. Source-response file exists.
2. Structured knowledge file exists.
3. Evaluation baseline file exists.
4. Evaluation baseline links to both source and structured knowledge files.
5. All 20 golden questions are present in the evaluation baseline.
6. Each golden question has expected answer guidance.
7. Evaluation baseline contains prohibited answer claims.
8. Evaluation baseline contains runtime-overstatement caveat.
9. Evaluation baseline contains no-runtime/no-live-LLM/no-DB/no-workforce-platform-change attestation.
10. Evaluation baseline includes Minerva advisory/no-payroll-calculation boundary.
11. Evaluation baseline includes finalised/frozen/paid/payment-batch guardrail.
12. Evaluation baseline includes ProcessPeriod.LifecycleStatusCode doctrine.
13. Evaluation baseline includes ObjectTime worker-period scope doctrine.
14. Evaluation baseline includes no-parallel-payroll-processor doctrine.
15. Mojibake markers are absent from the evaluation baseline.

Optional: if there is an existing deterministic answer-contract helper used in tests, add a small in-memory evaluator that checks candidate answer snippets for required/prohibited terms. Keep it test-only and deterministic.

Do not add live LLM calls.

## Verification Commands

Use:

1. `C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/test_admitted_draft_payrun_processing_bridge_source_response.py tests/test_admitted_draft_payrun_processing_bridge_knowledge_pack.py tests/test_admitted_draft_payrun_processing_bridge_answer_evaluation.py`
2. `C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/test_worker_story_baseline_capture_pilot.py tests/test_completed_domain_baseline_decision_ledger.py`
3. `git diff --check`
4. `git status --short`

Do not commit.
