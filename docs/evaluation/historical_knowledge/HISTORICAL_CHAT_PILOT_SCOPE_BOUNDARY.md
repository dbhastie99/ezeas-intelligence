# Historical Chat Pilot Scope Boundary

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines the narrow pilot boundary for any future Minerva historical chat pilot candidate.

## 2. Narrow Pilot Boundaries

- internal only;
- read-only;
- governed evidence only;
- refusal when gates are missing;
- no source mutation;
- no corpus mutation;
- no Code Evidence ingestion;
- no DB writes;
- no endpoint/UI in this slice;
- no live LLM in this slice;
- no cross-repo changes.

## 3. Evidence Boundary

A future pilot cannot answer from unapproved historical evidence. Historical evidence remains non-answerable by default until governed controls permit a specific answer use, retrieval eligibility, answer mode, citation/provenance chain, and runtime enforcement design.

## 4. Repository Boundary

This slice does not change workforce-platform, award-configurator-v1, or ezeas-analytics.

## 5. Runtime Boundary

This scope boundary does not implement chat, endpoint/UI, retrieval runtime, answer synthesis runtime, citation rendering runtime, live LLM calls, database writes, source ingestion, corpus mutation, Code Evidence ingestion, current-truth promotion, runtime answer-use permission activation, runtime retrieval eligibility activation, or runtime answer-mode activation.
