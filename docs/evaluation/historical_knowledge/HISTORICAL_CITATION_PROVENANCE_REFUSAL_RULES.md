# Historical Citation / Provenance Refusal Rules

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines refusal rules for missing, blocked, conflicted, superseded, or incomplete citation/provenance.

These rules are control documentation only and do not implement answer synthesis runtime, citation rendering runtime, retrieval filtering, live LLM calls, or chat exposure.

## 2. Refusal Rules

| Condition | Required treatment |
| --- | --- |
| Missing provenance | Refuse or state insufficient governed evidence. |
| Incomplete provenance | Refuse or state insufficient governed evidence. |
| Missing citation requirement | Refuse chat-answer readiness; do not generate a non-refusal answer. |
| Missing citation | Refuse or state insufficient governed evidence. |
| Unresolved conflict | Refuse settled answer unless a caveated answer mode is explicitly approved. |
| Supersession | Refuse current-truth answer unless source is used only as labelled historical context with approval. |
| Missing answer-use permission | Refuse as not answer-approved or insufficient governed evidence. |
| Missing retrieval eligibility | Refuse as not retrieval-eligible or insufficient governed evidence. |
| Missing answer mode | Refuse because answer mode is not governed. |

## 3. Behaviour Rules

Refusal may cite absence of governed evidence, missing answer-use permission, missing retrieval eligibility, missing provenance, conflict, or supersession.

Refusal must not fabricate citations.

Refusal should explain which gate is missing where known.

Unknown source date must be visibly marked and may require caveat or refusal depending on answer mode.

If citation rendering is not implemented, chat-answer readiness remains blocked.

## 4. Runtime Boundary

These refusal rules do not expose chat, call a live LLM, change retrieval runtime, change answer synthesis runtime, render citations at runtime, mutate corpus, ingest source content, promote current truth, write to a database, create endpoint changes, create UI changes, activate answer use at runtime, or activate retrieval eligibility at runtime.
