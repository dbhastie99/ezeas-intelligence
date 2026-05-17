# Controlled Evidence Intake Dry-Run Summary Model v0.1

## Purpose

This document records the deterministic batch summary model for controlled evidence intake dry-run outputs.

## Summary Model

The summary model accepts dry-run result dictionaries and returns a deterministic summary ID, batch counts, non-mutation flags, blocked-claim counts, required caveats, no-action attestation, and recommended next slice.

## Batch Counts

The model counts total dry runs, ready results, review results, and blocked results. Blocked results are decisions prefixed with `DRY_RUN_BLOCKED`. Ready results must be `DRY_RUN_READY_FOR_FUTURE_INTAKE` and non-mutating. All remaining results require review.

## Non-Mutation Rules

`all_non_mutating` is true only when no result reports evidence ingestion, corpus mutation, Code Evidence ingestion, DB writes, live retrieval, live LLM use, or final answer generation. Any positive execution or mutation flag makes the batch non-mutating check fail.

## Review / Blocked Rules

Runtime or production overstatement and unauthorised ingestion claims are counted separately. Corpus mutation and Code Evidence ingestion claims remain blocked by dry-run decision and do not authorise state change.

## Recommended Next Slice

The recommended next slice is controlled evidence intake review ledger / no-corpus-mutation v0.1.

## Required Caveats

Required caveats are aggregated deterministically from every dry-run result and deduplicated in first-seen order.

## Developer Handoff

Use the summary model for local deterministic batch review only. The summary never authorises ingestion, corpus mutation, Code Evidence ingestion, runtime action, DB access, live retrieval, live LLM use, final answer generation, chat exposure, deployment, or production readiness.
