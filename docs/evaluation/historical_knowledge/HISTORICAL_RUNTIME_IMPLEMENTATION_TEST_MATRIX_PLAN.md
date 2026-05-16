# Historical Runtime Implementation Test Matrix Plan

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This plan defines the future test matrix groups required before any read-only runtime skeleton or pilot skeleton is implemented.

It is a test-planning control only and does not implement runtime behaviour.

## 2. Planned Test Groups

- current-truth answer allowed case;
- historical-context answer allowed case;
- caveated answer case;
- backlog/context refusal or context-only case;
- doctrine/context answer case;
- missing answer-use permission refusal;
- missing retrieval eligibility refusal;
- missing answer mode refusal;
- missing citation/provenance refusal;
- superseded evidence refusal;
- conflicted evidence refusal;
- not-answerable evidence refusal;
- no live LLM call;
- no endpoint/UI;
- no corpus mutation;
- no DB write.

## 3. Required Boundary Assertions

Future tests must prove that runtime retrieval, answer synthesis runtime, citation rendering runtime, endpoint/UI, chat exposure, live LLM calls, source ingestion, corpus mutation, database writes, current-truth promotion, runtime answer-use activation, and runtime retrieval eligibility activation remain blocked until separately approved.

## 4. Recommended Next Action

The next slice should convert this plan into concrete tests before any runtime skeleton is implemented. If blockers are found, the next slice should remediate blockers instead.

## 5. Link To Full Test Matrix

The full runtime implementation test matrix is `HISTORICAL_RUNTIME_IMPLEMENTATION_TEST_MATRIX.md`.

The full matrix is supported by `HISTORICAL_RUNTIME_IMPLEMENTATION_SCENARIO_FIXTURES.md`, `HISTORICAL_RUNTIME_IMPLEMENTATION_EXPECTED_OUTCOMES.md`, `HISTORICAL_RUNTIME_IMPLEMENTATION_NO_RUNTIME_ASSERTIONS.md`, and `HISTORICAL_RUNTIME_IMPLEMENTATION_BLOCKER_MODEL.md`.

The full matrix remains documentation/control/test hardening only and does not implement runtime retrieval, answer synthesis runtime, citation rendering runtime, endpoint/UI, live LLM calls, database writes, corpus mutation, or chat exposure.
