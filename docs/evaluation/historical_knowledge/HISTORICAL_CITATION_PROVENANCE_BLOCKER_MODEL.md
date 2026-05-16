# Historical Citation / Provenance Blocker Model

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines blocker codes for historical citation/provenance answer readiness.

The blocker model is control documentation only. It does not implement citation rendering, retrieval runtime, answer synthesis runtime, live LLM calls, or chat exposure.

## 2. Blocker Codes

| Blocker code | Meaning |
| --- | --- |
| `MISSING_SOURCE_ID` | Source identifier is missing. |
| `MISSING_SOURCE_TITLE` | Source title is missing. |
| `MISSING_SOURCE_DATE_OR_UNKNOWN_MARKER` | Source date and explicit unknown-date marker are both missing. |
| `MISSING_REPOSITORY_CONTEXT` | Repository context is missing. |
| `MISSING_DOMAIN_CONTEXT` | Domain context is missing. |
| `MISSING_ANSWER_USE_PERMISSION` | Answer-use permission id or status is missing. |
| `MISSING_RETRIEVAL_ELIGIBILITY` | Retrieval eligibility id or status is missing. |
| `MISSING_ANSWER_MODE` | Answer mode id or status is missing. |
| `MISSING_CURRENT_TRUTH_PROMOTION` | Current-truth promotion id is missing where current-truth answer mode is requested. |
| `PROVENANCE_INCOMPLETE` | Required provenance fields are incomplete. |
| `CITATION_REQUIREMENT_UNDEFINED` | Citation requirement is undefined. |
| `CAVEAT_REQUIRED_NOT_DEFINED` | Caveat requirement is undefined where caveat may be required. |
| `CONFLICT_UNRESOLVED` | Conflict status is unresolved for requested answer mode. |
| `SUPERSESSION_UNRESOLVED` | Supersession status is unresolved for requested answer mode. |
| `REVOCATION_PATH_MISSING` | Revocation/removal path is missing. |
| `CITATION_RENDERING_NOT_IMPLEMENTED` | Runtime citation rendering is not implemented. |
| `CHAT_CONTRACT_NOT_IMPLEMENTED` | Runtime chat contract is not implemented. |

## 3. Resolution Boundary

Resolving a blocker only permits reassessment of citation/provenance readiness.

Blocker resolution does not itself enable runtime retrieval, citation rendering, answer synthesis, chat, live LLM calls, or answerability.

Blocker resolution does not mutate corpus, ingest source content, promote current truth, write to a database, add endpoints, add UI, activate answer use at runtime, or activate retrieval eligibility at runtime.
