# Codex Prompt - Minerva Historical Runtime Implementation Design Pack v0.1

Mode: Documentation/control/test hardening only.

Create and execute the Minerva historical runtime implementation design pack v0.1.

This slice defines future runtime design for a narrow, read-only Minerva historical chat pilot after chat pilot readiness control. It must create design documentation, interface-shape docs, blocker rules, test-planning docs, and tests only.

Required posture:

- no source content ingestion;
- no operational corpus mutation;
- no Code Evidence ingestion;
- no live LLM calls;
- no database writes;
- no schema migrations;
- no endpoint changes;
- no UI changes;
- no retrieval runtime implementation;
- no answer synthesis runtime implementation;
- no citation rendering runtime implementation;
- no chat exposure;
- no workforce-platform changes;
- no award-configurator-v1 changes;
- no ezeas-analytics changes;
- no current-truth promotion;
- no runtime answer-use permission activation;
- no runtime retrieval eligibility activation;
- no runtime answer-mode activation;
- no historical source may become answerable current truth in this slice.

Create:

- `docs/evaluation/historical_knowledge/HISTORICAL_RUNTIME_IMPLEMENTATION_DESIGN_PACK.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_RUNTIME_RETRIEVAL_GATE_DESIGN.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_RUNTIME_ANSWER_SYNTHESIS_GATE_DESIGN.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_RUNTIME_CITATION_REFUSAL_GATE_DESIGN.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_RUNTIME_AUDIT_LOGGING_DESIGN.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_RUNTIME_IMPLEMENTATION_TEST_MATRIX_PLAN.md`

Update the historical knowledge control index, chat pilot readiness checklist, go/no-go, implementation entry criteria, runtime gate plan, runtime gate chain requirements, dependency map, and `tests/test_domain_baseline_capture_batch.py`.

Verification:

- `python -m pytest tests/test_domain_baseline_capture_batch.py -q`
- `git diff --check`
- clean `.pytest_tmp` if present.

Expected result: Minerva moves from chat pilot readiness control into runtime implementation design, remains pre-runtime and pre-chat, and estimated progress toward a narrow safe internal chat pilot is about 85%.
