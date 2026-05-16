# Historical Chat Pilot Implementation Entry Criteria

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines the entry criteria for a future Minerva historical runtime implementation design slice.

It does not approve runtime implementation.

## 2. Entry Criteria

- go/no-go decision recorded;
- governance chain complete;
- runtime gate plan complete;
- answer-mode contract complete;
- citation/provenance contract complete;
- refusal policy complete;
- conflict/supersession handling complete;
- pilot scope boundary complete;
- no runtime implementation yet;
- no endpoint/UI yet;
- no live LLM yet.
- read-only closeout prerequisite recorded in `HISTORICAL_READ_ONLY_CHAT_PILOT_GO_NO_GO_CLOSEOUT.md`;
- read-only implementation candidate entry criteria recorded in `HISTORICAL_READ_ONLY_CHAT_PILOT_IMPLEMENTATION_CANDIDATE_ENTRY_CRITERIA.md`.

Required links:

- `RuntimeImplementationDesignPackLink`: `docs/evaluation/historical_knowledge/HISTORICAL_RUNTIME_IMPLEMENTATION_DESIGN_PACK.md`
- `RuntimeImplementationTestMatrixPlanLink`: `docs/evaluation/historical_knowledge/HISTORICAL_RUNTIME_IMPLEMENTATION_TEST_MATRIX_PLAN.md`
- `RuntimeImplementationTestMatrixLink`: `docs/evaluation/historical_knowledge/HISTORICAL_RUNTIME_IMPLEMENTATION_TEST_MATRIX.md`
- `ReadOnlyGatedRetrievalSkeletonCandidateLink`: `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_GATED_RETRIEVAL_SKELETON_CANDIDATE.md`
- `TestMatrixStatus`: `RUNTIME_TEST_MATRIX_READY_FOR_READ_ONLY_RETRIEVAL_SKELETON` only after the matrix is clean; otherwise `RUNTIME_TEST_MATRIX_DRAFTED` or blocked status applies.

The read-only gated retrieval skeleton candidate is a pre-pilot step only. It does not approve endpoint/UI, live retrieval, live LLM use, answer synthesis runtime, citation rendering runtime, or chat exposure.

## 3. Design Boundary

Meeting these entry criteria allows only a future implementation design slice, not runtime behaviour.

Endpoint/UI remains prohibited until later.

Chat exposure remains prohibited until later.

## 4. Runtime Boundary

This entry-criteria document does not implement retrieval runtime, answer synthesis runtime, citation rendering runtime, endpoint/UI, live LLM calls, database writes, source ingestion, corpus mutation, Code Evidence ingestion, current-truth promotion, runtime answer-use permission activation, runtime retrieval eligibility activation, runtime answer-mode activation, or chat exposure.

## Safety Test Pack Entry Boundary

Future pilot implementation consideration must first satisfy the read-only chat pilot safety test pack governed by `HISTORICAL_READ_ONLY_CHAT_PILOT_SAFETY_TEST_PACK.md`, `HISTORICAL_READ_ONLY_CHAT_PILOT_SAFETY_SCENARIOS.md`, `HISTORICAL_READ_ONLY_CHAT_PILOT_SAFETY_EXPECTED_OUTCOMES.md`, `HISTORICAL_READ_ONLY_CHAT_PILOT_SAFETY_BLOCKER_MODEL.md`, and `HISTORICAL_READ_ONLY_CHAT_PILOT_SAFETY_CLOSEOUT_ENTRY_CRITERIA.md`.

The safety test pack does not expose chat, approve endpoint/UI, approve live LLM use, or make final pilot go/no-go. Final pilot go/no-go remains separate.

## Read-Only Closeout Prerequisite

Future read-only chat pilot implementation candidate consideration requires `HISTORICAL_READ_ONLY_CHAT_PILOT_GO_NO_GO_CLOSEOUT.md` to record `GO_FOR_READ_ONLY_CHAT_PILOT_IMPLEMENTATION_CANDIDATE`.

This prerequisite authorises only a future candidate slice and does not expose chat, approve live LLM use, approve endpoint/UI, connect live retrieval, read/write a database, mutate corpus, or generate final natural-language answers.
