# Historical Read-Only Chat Pilot Exposure Decision Record

Version: v0.1

Date: 16 May 2026

## Purpose

This record defines the conservative decision fields for a future Minerva historical read-only chat pilot exposure decision.

## Decision Record Fields

| Field | Default value |
| --- | --- |
| DecisionId | `HISTORICAL_READ_ONLY_CHAT_PILOT_EXPOSURE_DECISION_v0_1` |
| DecisionStatus | `PILOT_EXPOSURE_DECISION_DRAFTED` |
| DecisionDate | `2026-05-16` |
| DeferredCloseoutStatus | `DEFERRED_NO_EXPLICIT_EXPOSURE_APPROVAL` |
| DeferredCloseoutRecord | `HISTORICAL_READ_ONLY_CHAT_PILOT_INTERNAL_EXPOSURE_DEFERRED_CLOSEOUT.md` |
| InputsReviewed | `HISTORICAL_READ_ONLY_CHAT_PILOT_EXPOSURE_DECISION_GATE.md`; `HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_CANDIDATE_CLOSEOUT.md`; `HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_STATIC_REVIEW.md`; `HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_DECISION_CATALOG.md`; `HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_NO_PRODUCTION_EXPOSURE_ATTESTATION.md` |
| MinimalEndpointUiCloseoutComplete | Yes |
| StaticReviewComplete | Yes |
| NoProductionExposureAttestationComplete | Yes |
| AccessControlDecisionComplete | No |
| AuditLoggingDecisionComplete | No |
| InternalExposureCandidatePermitted | No |
| ProductionChatExposedThisSlice | No |
| PublicAccessEnabledThisSlice | No |
| TenantCustomerAccessEnabledThisSlice | No |
| GlobalRouteRegisteredThisSlice | No |
| LiveLLMCalledThisSlice | No |
| FinalAnswerGeneratedThisSlice | No |
| LiveRetrievalPerformedThisSlice | No |
| CorpusMutationPerformedThisSlice | No |
| DatabaseReadPerformedThisSlice | No |
| DatabaseWritePerformedThisSlice | No |
| Blockers | `EXPOSURE_DECISION_INCOMPLETE`; `ACCESS_CONTROL_DECISION_INCOMPLETE`; `AUDIT_LOGGING_DECISION_INCOMPLETE`; `LIVE_LLM_POLICY_UNRESOLVED`; `FINAL_ANSWER_POLICY_UNRESOLVED` |
| DecisionRationale | Minimal endpoint/UI candidate is closed out, but internal exposure is not approved until access control, audit/logging, and explicit exposure decisioning are complete. |
| ApprovedBy | Not approved |
| Notes | Conservative default is No for exposure/runtime fields. This record does not expose chat. Because explicit exposure approval is absent, the stream is deferred by `HISTORICAL_READ_ONLY_CHAT_PILOT_INTERNAL_EXPOSURE_DEFERRED_DECISION_RECORD.md`. |
