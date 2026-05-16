# Historical Retrieval Eligibility Blocker Model

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines blocker codes and resolution expectations for historical retrieval eligibility decisions.

Blocker resolution does not itself enable retrieval runtime, expose chat, call a live LLM, or make evidence answerable.

## 2. Blocker Codes

| Blocker code | Resolution expectation |
| --- | --- |
| `MISSING_SOURCE_ID` | Record the governed `SourceId` before reassessment. |
| `MISSING_ANSWER_USE_PERMISSION` | Create or link an answer-use permission record before reassessment. |
| `ANSWER_USE_NOT_APPROVED` | Obtain answer-use approval for the requested mode or reject retrieval eligibility. |
| `ANSWER_USE_REVOKED` | Keep retrieval excluded unless a later valid permission replaces the revoked record. |
| `ANSWER_USE_SUPERSEDED` | Link the controlling successor permission before reassessment. |
| `MISSING_CURRENT_TRUTH_PROMOTION` | Link current-truth promotion before current-truth retrieval reassessment. |
| `CURRENT_TRUTH_NOT_APPROVED` | Keep current-truth retrieval blocked or rejected until `CurrentTruthPermitted` is Yes. |
| `PROVENANCE_INCOMPLETE` | Complete source provenance before reassessment. |
| `CROSS_CHECK_INCOMPLETE` | Complete cross-check or explicitly approve caveated/historical-only scope. |
| `CONFLICT_UNRESOLVED` | Resolve conflict or restrict to approved caveated/historical explanation scope. |
| `SUPERSESSION_UNRESOLVED` | Record supersession status before reassessment. |
| `EVIDENCE_SCOPE_UNDEFINED` | Record `EvidenceScope` from the answer-use permission record. |
| `ANSWER_SCOPE_UNDEFINED` | Record `AnswerScope` from the answer-use permission record. |
| `RETRIEVAL_MODE_UNDEFINED` | Record the requested retrieval mode before reassessment. |
| `CITATION_REQUIREMENT_UNDEFINED` | Record citation/provenance requirements before reassessment. |
| `REVOCATION_PATH_MISSING` | Define revocation/removal path before reassessment. |
| `RETRIEVAL_RUNTIME_NOT_IMPLEMENTED` | Preserve control-only status; runtime implementation requires a later explicit slice. |
| `CHAT_CONTRACT_NOT_IMPLEMENTED` | Preserve non-chat status until later answer-mode, refusal, citation, and pilot gates exist. |

## 3. Resolution Boundary

Resolving a blocker only permits reassessment of the retrieval eligibility decision.

Resolution does not enable retrieval runtime.

Resolution does not expose chat.

Resolution does not call a live LLM.

Resolution does not make evidence answerable.

Resolution does not mutate corpus, write to a database, promote current truth, ingest source content, create endpoints, or create UI changes.
