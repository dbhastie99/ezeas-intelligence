# Historical Chat Pilot Blocker Model

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines blocker codes that prevent Minerva historical chat pilot readiness or later runtime implementation design entry.

## 2. Blocker Codes

| Blocker code | Meaning |
| --- | --- |
| `GOVERNANCE_CHAIN_INCOMPLETE` | One or more required governance-chain controls are missing or incomplete. |
| `RUNTIME_GATE_PLAN_MISSING` | Runtime retrieval / answer synthesis gate plan is missing or incomplete. |
| `ANSWER_USE_GATE_MISSING` | Answer-use permission gate is missing or incomplete. |
| `RETRIEVAL_ELIGIBILITY_GATE_MISSING` | Retrieval eligibility gate is missing or incomplete. |
| `ANSWER_MODE_CONTRACT_MISSING` | Answer-mode contract is missing or incomplete. |
| `CITATION_PROVENANCE_CONTRACT_MISSING` | Citation/provenance contract is missing or incomplete. |
| `REFUSAL_POLICY_INCOMPLETE` | Refusal policy or missing-gate refusal handling is incomplete. |
| `CONFLICT_HANDLING_INCOMPLETE` | Conflict handling is incomplete. |
| `SUPERSESSION_HANDLING_INCOMPLETE` | Supersession handling is incomplete. |
| `LIVE_LLM_APPROVAL_MISSING` | Live LLM usage approval is missing. |
| `ENDPOINT_UI_APPROVAL_MISSING` | Endpoint/UI approval is missing. |
| `RUNTIME_IMPLEMENTATION_DESIGN_MISSING` | Runtime retrieval/answer/citation enforcement design is missing. |
| `PILOT_AUDIT_LOGGING_PLAN_MISSING` | Pilot audit/logging plan is missing. |

## 3. Resolution Boundary

Blocker resolution does not itself expose chat or implement runtime behaviour.

Resolving a blocker only permits reassessment of readiness or entry criteria. It does not implement retrieval runtime, answer synthesis runtime, citation rendering runtime, endpoint/UI, live LLM calls, database writes, source ingestion, corpus mutation, Code Evidence ingestion, current-truth promotion, runtime answer-use permission activation, runtime retrieval eligibility activation, or chat exposure.
