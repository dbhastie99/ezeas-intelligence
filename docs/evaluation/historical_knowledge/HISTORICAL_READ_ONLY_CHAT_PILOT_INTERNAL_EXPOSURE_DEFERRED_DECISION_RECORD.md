# Historical Read-Only Chat Pilot Internal Exposure Deferred Decision Record

Version: v0.1

Date: 16 May 2026

## Purpose

This record captures the conservative deferred decision for Minerva historical read-only chat pilot internal exposure.

## Decision Record Fields

| Field | Value |
| --- | --- |
| DecisionId | `HISTORICAL_READ_ONLY_CHAT_PILOT_INTERNAL_EXPOSURE_DEFERRED_DECISION_v0_1` |
| DecisionStatus | `DEFERRED_NO_EXPLICIT_EXPOSURE_APPROVAL` |
| DecisionDate | `2026-05-16` |
| CandidateService | `app/services/historical_read_only_chat_pilot_endpoint_ui_candidate_service.py` |
| ExplicitExposureApprovalPresent | No |
| InternalExposureEnabledThisSlice | No |
| ProductionChatExposedThisSlice | No |
| PublicAccessEnabledThisSlice | No |
| TenantCustomerAccessEnabledThisSlice | No |
| GlobalRouteRegisteredThisSlice | No |
| LiveLLMCalledThisSlice | No |
| FinalAnswerGeneratedThisSlice | No |
| DBReadPerformedThisSlice | No |
| DBWritePerformedThisSlice | No |
| DeferralReason | Explicit exposure approval is not present. Access control and audit/logging decisions are unresolved. |
| ResumeCriteria | Explicit exposure approval; internal-only scope confirmation; operator/developer-only access confirmation; access-control decision complete; audit/logging decision complete; no-production exposure attestation carried forward; candidate currency confirmed. |
| Blockers | `EXPLICIT_EXPOSURE_APPROVAL_MISSING`; `ACCESS_CONTROL_DECISION_MISSING`; `AUDIT_LOGGING_DECISION_MISSING`; `CANDIDATE_CURRENCY_UNCONFIRMED`; `LIVE_LLM_POLICY_UNRESOLVED`; `FINAL_ANSWER_POLICY_UNRESOLVED` |
| DecisionRationale | The minimal endpoint/UI candidate is closed out and metadata/envelope-only, but internal exposure cannot proceed without explicit approval, access-control decisioning, and audit/logging decisioning. |
| ApprovedBy | Not approved |
| Notes | Conservative default is No for approval, exposure, and runtime fields. This record does not expose chat or capture exposure evidence. |
