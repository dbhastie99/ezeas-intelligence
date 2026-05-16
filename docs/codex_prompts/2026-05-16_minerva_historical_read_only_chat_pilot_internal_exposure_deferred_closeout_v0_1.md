# Minerva Historical Read-Only Chat Pilot Internal Exposure Deferred Closeout v0.1

Date: 2026-05-16

## Objective

Create the read-only chat pilot internal exposure deferred closeout for Minerva historical knowledge.

This slice records that internal exposure is deferred because explicit exposure approval is not present. It preserves the minimal endpoint/UI candidate, no-production exposure attestations, exposure decision gate, access/audit requirements, and future resume criteria.

## Required Posture

- Internal exposure deferred closeout only.
- Documentation/control/test hardening only.
- No internal exposure enabled.
- No production endpoint creation.
- No public route/controller/API handler creation.
- No tenant/customer endpoint.
- No global route registration.
- No production UI creation.
- No production chat exposure.
- No live LLM calls.
- No final natural-language answer generation.
- No live retrieval backend.
- No vector search.
- No corpus query.
- No source content ingestion.
- No operational corpus mutation.
- No Code Evidence ingestion.
- No database reads or writes.
- No schema migrations.
- No workforce-platform changes.
- No award-configurator-v1 changes.
- No ezeas-analytics changes.

## Create Docs

- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_INTERNAL_EXPOSURE_DEFERRED_CLOSEOUT.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_INTERNAL_EXPOSURE_DEFERRED_DECISION_RECORD.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_INTERNAL_EXPOSURE_RESUME_CRITERIA.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_INTERNAL_EXPOSURE_DEFERRED_BLOCKER_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_INTERNAL_EXPOSURE_NO_RUN_ATTESTATION.md`

## Update Docs

- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_EXPOSURE_DECISION_GATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_EXPOSURE_DECISION_RECORD.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_INTERNAL_EXPOSURE_ENTRY_CRITERIA.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_EXPOSURE_BLOCKER_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_NO_PRODUCTION_EXPOSURE_CLOSEOUT_ATTESTATION.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_CANDIDATE_CLOSEOUT.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_REMAINING_RUNTIME_BOUNDARIES.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `tests/test_domain_baseline_capture_batch.py`

## Required Closeout Status

- InternalExposureCloseoutStatus: DEFERRED_NO_EXPLICIT_EXPOSURE_APPROVAL
- ExplicitExposureApprovalPresent: No
- InternalExposureEnabledThisSlice: No
- ProductionChatExposedThisSlice: No
- PublicAccessEnabledThisSlice: No
- TenantCustomerAccessEnabledThisSlice: No
- GlobalRouteRegisteredThisSlice: No
- LiveLLMCalledThisSlice: No
- FinalAnswerGeneratedThisSlice: No
- LiveRetrievalPerformedThisSlice: No
- CorpusMutationPerformedThisSlice: No
- DatabaseReadPerformedThisSlice: No
- DatabaseWritePerformedThisSlice: No

## Execution Constraints

Do not create endpoint registration, production route, UI component, live LLM, retrieval backend, database, corpus, or cross-repo code.

Do not expose chat, register routes globally, create public endpoints, create tenant/customer access, call live LLMs, generate final natural-language answers, connect live retrieval, read/write DB, mutate corpus, ingest source content, create Code Evidence, or make cross-repo changes.

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

## Suggested Commit Message

`minerva-historical-read-only-chat-pilot-internal-exposure-deferred-closeout-v01`
