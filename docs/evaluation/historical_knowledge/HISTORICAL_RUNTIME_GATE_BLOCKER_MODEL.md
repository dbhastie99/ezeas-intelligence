# Historical Runtime Gate Blocker Model

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines blocker codes for Minerva historical runtime gate planning.

## 2. Blocker Codes

- `MISSING_ANSWER_USE_GATE`
- `MISSING_RETRIEVAL_ELIGIBILITY_GATE`
- `MISSING_ANSWER_MODE_GATE`
- `MISSING_CITATION_PROVENANCE_GATE`
- `MISSING_REFUSAL_POLICY`
- `MISSING_EVIDENCE_CHAIN`
- `CONFLICT_BEHAVIOUR_UNRESOLVED`
- `SUPERSESSION_BEHAVIOUR_UNRESOLVED`
- `PROVENANCE_RUNTIME_ENFORCEMENT_UNDEFINED`
- `CITATION_RUNTIME_ENFORCEMENT_UNDEFINED`
- `RETRIEVAL_RUNTIME_NOT_DESIGNED`
- `ANSWER_SYNTHESIS_RUNTIME_NOT_DESIGNED`
- `CHAT_PILOT_READINESS_NOT_APPROVED`

## 3. Resolution Boundary

Blocker resolution permits reassessment only.

Blocker resolution does not itself implement runtime retrieval, answer synthesis, citation rendering, live LLM, endpoint/UI, or chat exposure.

Blocker resolution does not ingest source content, mutate corpus, promote current truth, activate answer-use permission at runtime, or activate retrieval eligibility at runtime.
