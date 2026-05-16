# Historical Chat Pilot Go / No-Go

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document records the decision model for whether Minerva historical knowledge may move from chat pilot readiness control into a later runtime implementation design slice.

## 2. Decision Statuses

| Status | Meaning |
| --- | --- |
| `GO_FOR_RUNTIME_IMPLEMENTATION_DESIGN` | A later runtime implementation design slice may be considered. This does not implement runtime behaviour. |
| `GO_FOR_READ_ONLY_CHAT_PILOT_CANDIDATE_LATER` | A later read-only chat pilot candidate may be considered only after implementation design, enforcement design, testing, and separate approval. |
| `NO_GO_BLOCKED_BY_GOVERNANCE_GAP` | Governance chain is incomplete. |
| `NO_GO_BLOCKED_BY_RUNTIME_GATE_GAP` | Runtime gate planning or entry criteria are incomplete. |
| `NO_GO_BLOCKED_BY_ANSWER_SAFETY_GAP` | Answer safety, labelling, caveat, backlog, doctrine, or refusal controls are incomplete. |
| `NO_GO_BLOCKED_BY_CITATION_PROVENANCE_GAP` | Citation/provenance requirements are incomplete. |
| `NO_GO_BLOCKED_BY_REFUSAL_POLICY_GAP` | Refusal policy is incomplete. |
| `NO_GO_BLOCKED_BY_CONFLICT_SUPERSESSION_GAP` | Conflict or supersession handling is incomplete. |

## 3. Current Decision

Current status: `GO_FOR_RUNTIME_IMPLEMENTATION_DESIGN`

Rationale: the governance chain has enough documented controls to allow a later runtime implementation design pack. Runtime retrieval, answer synthesis enforcement, citation rendering, endpoint/UI, live LLM usage, and chat exposure remain prohibited.

## 4. GO Boundary

GO does not expose chat.

GO does not permit live LLM call.

GO does not permit endpoint/UI.

GO only permits a future implementation design slice unless explicitly stated otherwise.

## 5. GO Permits Implementation Design Only

GO permits implementation design only unless later explicitly expanded by a separate approved control.

GO does not permit read-only retrieval skeleton work, answer synthesis skeleton work, citation rendering skeleton work, endpoint/UI work, live LLM use, or chat exposure.

## 6. Runtime Boundary

This go/no-go record does not implement retrieval runtime, answer synthesis runtime, citation rendering runtime, endpoint/UI, live LLM calls, database writes, source ingestion, corpus mutation, Code Evidence ingestion, current-truth promotion, runtime answer-use permission activation, runtime retrieval eligibility activation, or chat exposure.

## 7. Read-Only Closeout Reference

The read-only pilot closeout is recorded separately in `HISTORICAL_READ_ONLY_CHAT_PILOT_GO_NO_GO_CLOSEOUT.md`.

That closeout may authorise only a future read-only chat pilot implementation candidate. It does not expose chat in this slice, approve live LLM use, approve endpoint/UI, connect live retrieval, read/write a database, mutate corpus, or generate final natural-language answers.
