# Codex Prompt - Minerva Historical Runtime Implementation Test Matrix v0.1

Mode: Documentation/control/test hardening only.

Create and execute the Minerva historical runtime implementation test matrix v0.1.

This slice converts the verified historical runtime implementation design pack into concrete planned test cases for retrieval gating, answer-use enforcement, answer-mode enforcement, citation/provenance enforcement, refusal behaviour, conflict/supersession handling, and audit/logging before any implementation code is introduced.

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

- `docs/evaluation/historical_knowledge/HISTORICAL_RUNTIME_IMPLEMENTATION_TEST_MATRIX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_RUNTIME_IMPLEMENTATION_SCENARIO_FIXTURES.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_RUNTIME_IMPLEMENTATION_EXPECTED_OUTCOMES.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_RUNTIME_IMPLEMENTATION_NO_RUNTIME_ASSERTIONS.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_RUNTIME_IMPLEMENTATION_BLOCKER_MODEL.md`

Update the historical knowledge control index, runtime implementation design pack, retrieval gate design, answer synthesis gate design, citation/refusal gate design, audit/logging design, runtime implementation test matrix plan, chat pilot implementation entry criteria, and `tests/test_domain_baseline_capture_batch.py`.

Verification:

- `python -m pytest tests/test_domain_baseline_capture_batch.py -q`
- `git diff --check`
- clean `.pytest_tmp` if present.

Expected result: Minerva moves from runtime implementation design into runtime implementation test-matrix readiness, remains pre-runtime and pre-chat, and estimated progress toward a narrow safe internal chat pilot is about 88%.
