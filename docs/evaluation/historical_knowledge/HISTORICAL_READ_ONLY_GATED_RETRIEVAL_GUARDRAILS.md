# Historical Read-Only Gated Retrieval Guardrails

Version: v0.1

Date: 16 May 2026

## Purpose

This document records guardrails for the Minerva historical read-only gated retrieval skeleton candidate.

## Guardrails

- in-memory metadata evaluation only;
- no live retrieval backend;
- no vector search;
- no corpus query;
- no source content ingestion;
- no operational corpus mutation;
- no Code Evidence ingestion;
- no live LLM calls;
- no database reads;
- no database writes;
- no schema migrations;
- no endpoint changes;
- no UI changes;
- no answer synthesis runtime;
- no citation rendering runtime;
- no chat exposure;
- no workforce-platform changes;
- no award-configurator-v1 changes;
- no ezeas-analytics changes;
- no current-truth promotion;
- no runtime answer-use permission activation;
- no runtime retrieval eligibility activation beyond evaluating supplied metadata in-memory.

## Non-Goals

This candidate does not make historical sources answerable current truth. It does not expose Minerva for chat. It does not implement retrieval runtime, answer synthesis runtime, or citation rendering runtime.

The response is for gate evaluation only.

## Contract Hardening

The hardened contract is `HISTORICAL_READ_ONLY_GATED_RETRIEVAL_CONTRACT_HARDENING.md`.

The decision catalog is `HISTORICAL_READ_ONLY_GATED_RETRIEVAL_DECISION_CATALOG.md`.

The closeout is `HISTORICAL_READ_ONLY_GATED_RETRIEVAL_CONTRACT_CLOSEOUT.md`.

All decisions remain read-only metadata decisions. RuntimeActionPermitted is No for all decisions.
