# Historical Read-Only Chat Pilot Orchestrator Decision Catalog

Version: v0.1

Date: 16 May 2026

## Purpose

This catalog defines orchestrator envelope and refusal decisions for the in-memory metadata-only read-only chat pilot orchestrator candidate.

## Decisions

| Decision | PilotResponseMode | RefusalRequired | CitationReady | CaveatRequired | FinalAnswerGenerated | LiveLLMCalled | ChatExposed | EndpointUIPresent | RuntimeActionPermitted | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `READY_CURRENT_TRUTH_ENVELOPE` | `READY_CURRENT_TRUTH_ENVELOPE` | false | true | false | false | false | false | false | false | Fully governed metadata can reach a current-truth envelope only; no final answer text is generated. |
| `READY_HISTORICAL_CONTEXT_ENVELOPE` | `READY_HISTORICAL_CONTEXT_ENVELOPE` | false | true | true | false | false | false | false | false | Historical-context metadata remains labelled context and is not current truth. |
| `READY_CAVEATED_ENVELOPE` | `READY_CAVEATED_ENVELOPE` | false | true | true | false | false | false | false | false | Caveat-ready metadata can reach a caveated envelope only. |
| `REFUSAL_ENVELOPE` | `REFUSAL_ENVELOPE` | true | false | context-dependent | false | false | false | false | false | Any prior gate refusal remains refusal. |
| `BLOCKED_NO_RUNTIME_ENVELOPE` | `BLOCKED_NO_RUNTIME_ENVELOPE` | true | false | context-dependent | false | false | false | false | false | Runtime-required metadata is blocked because runtime chat/retrieval/LLM/DB actions are not implemented or authorised. |
| `REFUSE_MISSING_ANSWER_USE` | `REFUSAL_ENVELOPE` | true | false | context-dependent | false | false | false | false | false | Missing or blocked answer-use permission refuses. |
| `REFUSE_MISSING_RETRIEVAL_ELIGIBILITY` | `REFUSAL_ENVELOPE` | true | false | context-dependent | false | false | false | false | false | Missing or blocked retrieval eligibility refuses. |
| `REFUSE_MISSING_PROVENANCE` | `REFUSAL_ENVELOPE` | true | false | context-dependent | false | false | false | false | false | Missing or incomplete provenance refuses. |
| `REFUSE_MISSING_CITATION` | `REFUSAL_ENVELOPE` | true | false | context-dependent | false | false | false | false | false | Missing required citation fields refuse. |
| `REFUSE_CONFLICTED` | `REFUSAL_ENVELOPE` | true | false | true | false | false | false | false | false | Conflicted settled/current-truth evidence refuses unless approved caveat-ready metadata produces `READY_CAVEATED_ENVELOPE`. |
| `REFUSE_SUPERSEDED` | `REFUSAL_ENVELOPE` | true | false | context-dependent | false | false | false | false | false | Superseded evidence refuses current-truth envelope use. |
| `REFUSE_NOT_ANSWERABLE` | `REFUSAL_ENVELOPE` | true | false | context-dependent | false | false | false | false | false | Not-answerable metadata refuses. |

## Runtime Action Boundary

All runtime action fields remain No/false. No endpoint/UI exists. No live LLM is called. No final answer is generated. No live retrieval backend is used. No DB read/write occurs. No corpus mutation occurs. This is not production chat exposure.
