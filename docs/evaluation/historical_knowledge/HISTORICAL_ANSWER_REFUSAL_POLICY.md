# Historical Answer Refusal Policy

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines refusal behaviours for future Minerva historical answer modes.

This refusal policy is control documentation only and does not implement answer synthesis runtime.

## 2. Refusal Behaviours

| Condition | Required answer mode |
| --- | --- |
| Insufficient governed evidence | `REFUSAL_INSUFFICIENT_GOVERNED_EVIDENCE` |
| Missing answer-use permission | `REFUSAL_NOT_ANSWER_APPROVED` or `REFUSAL_INSUFFICIENT_GOVERNED_EVIDENCE` |
| Missing retrieval eligibility | `REFUSAL_RETRIEVAL_NOT_ELIGIBLE` or `REFUSAL_INSUFFICIENT_GOVERNED_EVIDENCE` |
| Not-answer-approved evidence | `REFUSAL_NOT_ANSWER_APPROVED` |
| Conflicted evidence | `REFUSAL_CONFLICTED_EVIDENCE` unless a caveated answer mode is explicitly approved |
| Superseded evidence | `REFUSAL_SUPERSEDED_EVIDENCE` for current-truth answers |
| Missing citation/provenance | `REFUSAL_INSUFFICIENT_GOVERNED_EVIDENCE`; chat-answer readiness is blocked |
| Missing citation/provenance contract record | `REFUSAL_INSUFFICIENT_GOVERNED_EVIDENCE`; non-refusal chat answer is blocked |
| Incomplete citation/provenance | `REFUSAL_INSUFFICIENT_GOVERNED_EVIDENCE`; insufficient governed evidence must be stated |
| Runtime retrieval not implemented | `REFUSAL_RETRIEVAL_NOT_ELIGIBLE` or insufficient governed evidence for chat readiness |
| Chat contract not implemented | `REFUSAL_INSUFFICIENT_GOVERNED_EVIDENCE` for chat-answer readiness |

## 3. Behaviour Rules

If answer-use permission is absent, blocked, rejected, revoked, superseded, or missing, future Minerva answer logic must refuse or state insufficient governed evidence.

If retrieval eligibility is absent, blocked, revoked, superseded, conflicted, excluded, or missing, future Minerva answer logic must refuse or state insufficient governed evidence.

If evidence is historical-only, future Minerva answer logic must not answer as current truth.

If evidence is conflicted, future Minerva answer logic must not answer as settled truth unless a caveated answer mode is explicitly approved and the caveat is visible.

If evidence is superseded, future Minerva answer logic must refuse current-truth answers and may only use it for labelled historical explanation when separately approved.

If citation/provenance is missing, chat-answer readiness is blocked.

If citation/provenance is incomplete, future Minerva answer logic must refuse or state insufficient governed evidence.

Refusal must not fabricate citations, and should explain which citation/provenance, answer-use, retrieval eligibility, or answer-mode gate is missing where known.

## 4. Runtime Boundary

This policy does not implement answer synthesis runtime, retrieval filtering, chat exposure, live LLM calls, corpus mutation, source ingestion, current-truth promotion, database writes, endpoint changes, or UI changes.
