# Historical Answer Mode Blocker Model

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines blocker codes for future Minerva historical answer-mode decisions.

Blocker resolution does not itself enable runtime retrieval, answer synthesis, chat, live LLM calls, or answerability.

## 2. Blocker Codes

| BlockerCode | Meaning |
| --- | --- |
| `MISSING_RETRIEVAL_ELIGIBILITY` | Required retrieval eligibility record is missing. |
| `RETRIEVAL_NOT_ELIGIBLE` | Retrieval eligibility is absent, blocked, rejected, revoked, superseded, conflicted, or excluded. |
| `MISSING_ANSWER_USE_PERMISSION` | Required answer-use permission record is missing. |
| `ANSWER_USE_NOT_APPROVED` | Answer-use permission is absent, blocked, rejected, revoked, superseded, or not approved for requested scope. |
| `MISSING_CURRENT_TRUTH_PROMOTION` | Current-truth answer was requested without current-truth promotion record. |
| `CURRENT_TRUTH_NOT_APPROVED` | Current-truth answer was requested without current-truth approval. |
| `PROVENANCE_INCOMPLETE` | Required source provenance is missing or incomplete. |
| `CITATION_REQUIREMENT_UNDEFINED` | Citation requirement is not defined. |
| `CONFLICT_UNRESOLVED` | Conflict status is unresolved and no caveated mode is approved. |
| `SUPERSESSION_UNRESOLVED` | Supersession status is unresolved. |
| `CAVEAT_REQUIRED_NOT_DEFINED` | Caveat is required but not defined. |
| `ANSWER_SCOPE_UNDEFINED` | Answer scope is missing or incomplete. |
| `ANSWER_MODE_UNDEFINED` | Answer mode is missing or invalid. |
| `CHAT_ELIGIBILITY_NOT_APPROVED` | Chat eligibility is not approved; chat is not enabled in this slice. |
| `RUNTIME_RETRIEVAL_NOT_IMPLEMENTED` | Runtime retrieval filtering has not been implemented. |
| `ANSWER_SYNTHESIS_GATE_NOT_IMPLEMENTED` | Runtime answer synthesis gating has not been implemented. |
| `CHAT_CONTRACT_NOT_IMPLEMENTED` | Later chat contract or pilot readiness gate has not been implemented. |

## 3. Resolution Boundary

Resolving blockers permits reassessment only.

Resolving blockers does not activate runtime retrieval eligibility, activate answer-use permission at runtime, implement answer synthesis runtime, expose chat, call a live LLM, mutate corpus, ingest source content, write to a database, create endpoints, create UI, promote current truth, or make historical evidence answerable current truth.
