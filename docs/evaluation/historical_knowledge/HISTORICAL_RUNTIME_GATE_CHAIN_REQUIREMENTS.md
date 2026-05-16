# Historical Runtime Gate Chain Requirements

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines the required governance chain that must exist before Minerva historical knowledge can proceed toward runtime gates or chat pilot readiness.

## 2. Required Source-To-Chat Chain

The required chain is:

source registration -> review/candidate/decision -> findings/classification -> ingestion/backfill decision -> current-truth promotion where applicable -> answer-use permission -> retrieval eligibility -> answer mode -> citation/provenance -> runtime gate -> chat pilot.

Missing links block chat readiness.

## 3. Required Chain Controls

Each chain step must remain independently governed:

- Source registration controls source identity, source title, date or unknown-date marker, repository context, and domain context.
- Review/candidate/decision control determines whether a source can be reviewed and what decision state exists.
- Findings/classification control determines whether reviewed material is implemented, planned, superseded, conflicted, or not answerable.
- Ingestion/backfill decision control determines whether future ingestion/backfill may be considered; it does not itself ingest content.
- Current-truth promotion applies only where current-truth answers are requested and approved.
- Answer-use permission determines whether evidence may be used in a future non-refusal answer.
- Retrieval eligibility determines whether answer-use-approved evidence may be exposed to future retrieval.
- Answer mode determines the allowed answer treatment.
- Citation/provenance determines required source traceability before chat-answer readiness.
- Runtime gate determines future runtime enforcement design.
- Chat pilot requires separate readiness approval.

## 4. Runtime Boundary

This document does not implement runtime retrieval, answer synthesis, citation rendering, live LLM calls, endpoint/UI, or chat exposure.
