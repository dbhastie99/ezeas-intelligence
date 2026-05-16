# Historical Read-Only Chat Pilot Implementation Candidate Closeout Entry Criteria

Version: v0.1

Date: 16 May 2026

## Purpose

This document defines entry criteria for a future closeout of the in-memory read-only chat pilot orchestrator candidate.

## Entry Criteria

- implementation candidate doc exists;
- orchestrator response contract doc exists;
- fixture catalog doc exists;
- guardrails doc exists;
- orchestrator candidate service exists;
- service composes the existing retrieval, answer synthesis, and citation/refusal skeleton helpers;
- current-truth fixture returns `READY_CURRENT_TRUTH_ENVELOPE` without final answer generation;
- historical-context fixture returns `READY_HISTORICAL_CONTEXT_ENVELOPE` and not current truth;
- caveated fixture preserves `CaveatRequired: true`;
- missing answer-use permission refuses;
- missing retrieval eligibility refuses;
- missing provenance/citation refuses;
- conflicted settled/current-truth evidence refuses unless approved caveat-ready metadata produces caveated envelope;
- superseded current-truth evidence refuses;
- prior refusal remains refusal;
- no endpoint/UI exists;
- no live LLM is called;
- no final answer is generated;
- no live retrieval backend is used;
- no DB read/write occurs;
- no corpus mutation occurs.

## Boundary

These criteria support future orchestrator closeout only. They do not expose chat, approve endpoint/UI, approve live LLM use, approve live retrieval, approve database access, approve corpus mutation, or authorise production deployment.
