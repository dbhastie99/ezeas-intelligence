# Historical Runtime Answer Synthesis Gate Design

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines the future answer synthesis gate design for a narrow, read-only Minerva historical chat pilot.

No answer synthesis runtime or live LLM is implemented.

## 2. Required Inputs From Retrieval Gate

- request/query context;
- retrieval mode;
- requested answer mode;
- eligible evidence ids;
- excluded evidence ids and exclusion reasons;
- answer-use permission ids;
- retrieval eligibility ids;
- evidence scopes;
- current-truth statuses;
- conflict and supersession statuses;
- caveat requirements;
- citation/provenance statuses;
- refusal-required flag;
- refusal reason.

## 3. Allowed Answer Modes

The future gate may only use approved answer modes:

- current-truth answer;
- historical-context answer;
- caveated answer;
- backlog/context response;
- doctrine/context response;
- refusal.

## 4. Refusal Modes

Refusal modes must cover insufficient governed evidence, missing answer-use permission, missing retrieval eligibility, missing answer mode, missing citation/provenance, conflicted evidence, superseded evidence, not-answerable evidence, and out-of-scope request.

## 5. Historical / Context Caveat Handling

Historical-context answers must be labelled historical and must not be rendered as current truth.

Caveated answers must carry required caveats visibly into the citation/refusal gate output.

## 6. Backlog / Doctrine / Hardening Context Handling

Backlog/context answers must not be represented as implemented behaviour.

Doctrine/context and hardening context answers must not be represented as runtime implementation evidence unless separately confirmed by current code/test evidence and approved controls.

## 7. Current-Truth-Only Answer Handling

Current-truth-only answers require current-truth promotion, answer-use permission, retrieval eligibility, answer mode, citation/provenance readiness, and no unresolved conflict or supersession.

If any required current-truth gate is missing, the answer synthesis gate must refuse or return insufficient governed evidence.

## 8. Output Shape To Citation / Refusal Gate

The future answer synthesis gate should output:

- `RequestId`;
- `AnswerMode`;
- `AnswerEligibility`;
- `EvidenceIdsUsed`;
- `EvidenceIdsExcluded`;
- `CaveatsRequired`;
- `HistoricalContextRequired`;
- `CitationRequired`;
- `ProvenanceRequired`;
- `RefusalRequired`;
- `RefusalReason`;
- `DraftAnswerPayload` or `RefusalPayload`.

## 9. Boundary

This document is design only. It does not implement answer synthesis runtime, does not call a live LLM, does not implement retrieval runtime, does not render citations, does not create endpoint/UI, and does not expose chat.
