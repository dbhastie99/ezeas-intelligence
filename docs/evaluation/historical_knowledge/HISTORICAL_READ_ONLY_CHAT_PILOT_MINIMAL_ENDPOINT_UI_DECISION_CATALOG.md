# Historical Read-Only Chat Pilot Minimal Endpoint/UI Decision Catalog

Version: v0.1

Date: 16 May 2026

## Purpose

This catalog records the decision envelopes reviewed for the minimal endpoint/UI candidate closeout.

## Decision Catalog

| Decision | ExposurePermitted | FinalAnswerGenerated | LiveLLMCalled | ChatExposed | DatabaseReadPerformed | DatabaseWritePerformed | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `READY_CURRENT_TRUTH_ENVELOPE` | No/false | No/false | No/false | No/false | No/false | No/false | Ready status envelope only; no production exposure. |
| `READY_HISTORICAL_CONTEXT_ENVELOPE` | No/false | No/false | No/false | No/false | No/false | No/false | Historical-context envelope only; not silently converted to current truth. |
| `READY_CAVEATED_ENVELOPE` | No/false | No/false | No/false | No/false | No/false | No/false | Caveat remains visible in envelope/status output. |
| `REFUSAL_ENVELOPE` | No/false | No/false | No/false | No/false | No/false | No/false | Refusal remains visible and no answer is generated. |
| `BLOCKED_NO_RUNTIME_ENVELOPE` | No/false | No/false | No/false | No/false | No/false | No/false | Runtime remains blocked: no LLM, retrieval, final answer, DB, or corpus. |
| `BLOCKED_NO_EXPOSURE_ENVELOPE` | No/false | No/false | No/false | No/false | No/false | No/false | Exposure remains blocked: no public, tenant/customer, production chat, or global route. |

## Boundary

All runtime and exposure fields remain No/false. This catalog does not approve endpoint registration, UI exposure, live LLM use, final answer generation, live retrieval, corpus/vector search, DB reads, DB writes, or corpus mutation.

