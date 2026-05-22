# Codex Prompt Artefact - Minerva Role-Scoped Code Evidence Foundation v0.1

Date: 2026-05-21

Repository: `ezeas-intelligence`

Objective: implement the Minerva Role-Scoped Code Evidence Foundation v0.1 as a read-only, deterministic, role-scoped code evidence foundation.

## Scope

Create:

- `docs/knowledge/minerva_code_evidence_role_model_v0_1_source_response.md`
- `docs/knowledge/minerva_code_evidence_role_model_v0_1.md`
- `docs/evaluation/minerva_code_evidence_role_model_v0_1/ANSWER_EVALUATION_BASELINE.md`
- `docs/evaluation/minerva_code_evidence_role_model_v0_1/CODE_EVIDENCE_SAMPLE_INDEX.json`
- `app/services/code_evidence_inventory_service.py`
- `app/services/code_evidence_answer_policy_service.py`
- `tests/test_minerva_code_evidence_role_model_knowledge.py`
- `tests/test_code_evidence_inventory_service.py`
- `tests/test_code_evidence_answer_policy_service.py`

## Product Decision

Code evidence has two uses:

- Developer technical mode for authorised implementation questions.
- Payroll and operational confirmation mode where code evidence strengthens confidence without exposing raw internals by default.

Code evidence is confirmation/supporting evidence. It is not payroll calculation authority and code cannot prove runtime availability by itself.

## Role Mapping

- DEVELOPER -> TECHNICAL_DISCLOSURE.
- PAYROLL_ADMINISTRATOR -> IMPLEMENTATION_CONFIRMATION.
- PAYROLL_USER -> BACKGROUND_CONFIDENCE_ONLY.
- CUSTOMER_ADMINISTRATOR -> IMPLEMENTATION_CONFIRMATION, customer-safe.
- WORKER -> NO_CODE_EVIDENCE.

## Target Registry

Active targets:

- ezeas-intelligence.
- workforce-platform.
- award-configurator-v1.

Registered optional/deferred target:

- ezeas-analytics.

Analytics is strategically important for future interactive visualisation, interpretation, and narrative explanation. Full analytics indexing is optional or deferred in v0.1 by default.

## Evidence Boundary

Code evidence can prove file, service, class, function, route, schema, UI reference, test, prompt artefact, and knowledge document existence.

Code evidence cannot prove DB migration applied, runtime enablement, production availability, customer access, live object state, payroll correctness, payment, finalisation, tenant safety, permissions, or deployed configuration.

## Non-Goals And Attestation

- No database migrations.
- No DB connection.
- No live LLM calls.
- No chat exposure.
- No Workforce Platform runtime integration.
- No UI work.
- No code execution.
- No repo mutation outside ezeas-intelligence.
- No operational payroll evidence ingestion.
- No vector database.
- No embeddings.
- No production/customer exposure.
- No raw code dumps.
- No secrets indexing.
- Raw code snippets disabled by default.

## Golden Questions

1. Why does Minerva need code evidence?
2. What are the two main uses of code evidence?
3. How is developer technical use different from payroll-manager confirmation use?
4. What can code evidence prove?
5. What can code evidence not prove?
6. Why is code evidence not payroll calculation authority?
7. How should a developer answer expose code evidence?
8. How should a payroll administrator answer use code evidence?
9. How should a payroll user answer use code evidence?
10. How should a worker answer use code evidence?
11. What are the code evidence disclosure modes?
12. How are roles mapped to disclosure modes?
13. Why should Analytics be included as a future code evidence target?
14. Why should Analytics full indexing be optional or deferred in v0.1?
15. How should Minerva handle doctrine/code conflicts?
16. How should Minerva handle code evidence without implementation-state documentation?
17. Why do tests provide stronger evidence than code existence alone?
18. What must Minerva never infer from code evidence alone?
19. What repositories are active code evidence targets in v0.1?
20. What remains out of scope for the Code Evidence foundation?

## Verification Commands

```powershell
C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/test_minerva_code_evidence_role_model_knowledge.py tests/test_code_evidence_inventory_service.py tests/test_code_evidence_answer_policy_service.py
C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/test_worker_story_baseline_capture_pilot.py tests/test_completed_domain_baseline_decision_ledger.py
git diff --check
git status --short
```
