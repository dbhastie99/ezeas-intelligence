# Minerva Historical Read-Only Chat Pilot Safety Test Pack v0.1 Prompt

Date: 16 May 2026

## Purpose

Create the durable control artefact and execute the Minerva historical read-only chat pilot safety test pack v0.1 slice.

## Slice

Minerva historical read-only chat pilot safety test pack v0.1.

## Context

The current Minerva historical knowledge model includes the governance chain, runtime implementation design, runtime implementation test matrix, read-only gated retrieval skeleton, retrieval skeleton contract hardening, answer synthesis enforcement skeleton, and citation/refusal enforcement skeleton.

Existing service files:

- `app/services/historical_read_only_gated_retrieval_skeleton_service.py`
- `app/services/historical_answer_synthesis_enforcement_skeleton_service.py`
- `app/services/historical_citation_refusal_enforcement_skeleton_service.py`

Important current truth:

- Historical sources are not answerable current truth by default.
- Current runtime-adjacent skeletons evaluate supplied in-memory metadata only.
- No live retrieval backend is used.
- No corpus/vector/database stores are queried.
- No live LLM is called.
- No chat is exposed.
- No final natural-language chat answer is generated.
- No endpoint/UI exists.
- This slice must not mutate operational corpus content or live evidence stores.

## Objective

Create the read-only chat pilot safety test pack for the Minerva historical skeleton chain. Prove, through documentation and tests, that the current in-memory skeleton chain preserves critical safety behaviours before a future read-only chat pilot go/no-go can be considered.

## Required Posture

Safety test pack only. In-memory metadata evaluation only. No live LLM calls. No final chat answer generation. No citation rendering runtime beyond metadata envelope validation. No live retrieval backend. No vector search. No corpus query. No source content ingestion. No operational corpus mutation. No Code Evidence ingestion. No database reads or writes. No schema migrations. No endpoint changes. No UI changes. No chat exposure. No workforce-platform changes. No award-configurator-v1 changes. No ezeas-analytics changes. No current-truth promotion. No runtime answer-use permission activation beyond supplied metadata evaluation. No runtime retrieval eligibility activation beyond supplied metadata evaluation. No historical source may become answerable current truth in this slice.

## Required Docs

Create:

- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_SAFETY_TEST_PACK.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_SAFETY_SCENARIOS.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_SAFETY_EXPECTED_OUTCOMES.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_SAFETY_BLOCKER_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_SAFETY_CLOSEOUT_ENTRY_CRITERIA.md`

Update existing historical skeleton, runtime, chat-pilot, and control-index docs to reference the safety test pack.

## Required Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
python -m py_compile app/services/historical_read_only_gated_retrieval_skeleton_service.py
python -m py_compile app/services/historical_answer_synthesis_enforcement_skeleton_service.py
python -m py_compile app/services/historical_citation_refusal_enforcement_skeleton_service.py
git diff --check
```

Clean `.pytest_tmp` if present.

## Suggested Commit Message

`minerva-historical-read-only-chat-pilot-safety-test-pack-v01`
