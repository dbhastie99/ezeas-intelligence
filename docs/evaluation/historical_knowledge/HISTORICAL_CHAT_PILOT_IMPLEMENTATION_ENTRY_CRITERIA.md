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

Required links:

- `RuntimeImplementationDesignPackLink`: `docs/evaluation/historical_knowledge/HISTORICAL_RUNTIME_IMPLEMENTATION_DESIGN_PACK.md`
- `RuntimeImplementationTestMatrixPlanLink`: `docs/evaluation/historical_knowledge/HISTORICAL_RUNTIME_IMPLEMENTATION_TEST_MATRIX_PLAN.md`
- `RuntimeImplementationTestMatrixLink`: `docs/evaluation/historical_knowledge/HISTORICAL_RUNTIME_IMPLEMENTATION_TEST_MATRIX.md`
- `TestMatrixStatus`: `RUNTIME_TEST_MATRIX_READY_FOR_READ_ONLY_RETRIEVAL_SKELETON` only after the matrix is clean; otherwise `RUNTIME_TEST_MATRIX_DRAFTED` or blocked status applies.

## 3. Design Boundary

Meeting these entry criteria allows only a future implementation design slice, not runtime behaviour.

Endpoint/UI remains prohibited until later.

Chat exposure remains prohibited until later.

## 4. Runtime Boundary

This entry-criteria document does not implement retrieval runtime, answer synthesis runtime, citation rendering runtime, endpoint/UI, live LLM calls, database writes, source ingestion, corpus mutation, Code Evidence ingestion, current-truth promotion, runtime answer-use permission activation, runtime retrieval eligibility activation, runtime answer-mode activation, or chat exposure.
