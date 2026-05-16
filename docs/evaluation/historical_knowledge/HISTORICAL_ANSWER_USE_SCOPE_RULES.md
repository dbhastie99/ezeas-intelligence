# Historical Answer-Use Scope Rules

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines evidence scopes and answer scopes for future Minerva answer-use permission decisions.

This is a rule document only and does not implement retrieval or chat behaviour.

## 2. Evidence Scopes

| EvidenceScope | Future retrieval/chat treatment |
| --- | --- |
| `HISTORICAL_CONTEXT_ONLY` | Eligible only for historical-context answer mode after answer-use approval; excluded from current-truth mode. |
| `CURRENT_TRUTH` | Eligible for current-truth mode only after current-truth approval and answer-use approval. |
| `CURRENT_TRUTH_WITH_CAVEAT` | Eligible for current-truth mode only when caveats are preserved in the answer contract. |
| `BACKLOG_CONTEXT_ONLY` | Eligible only for backlog/planning explanation after answer-use approval; not current implemented truth. |
| `PLATFORM_DOCTRINE_CONTEXT` | Eligible only within approved platform doctrine scope and repository/domain context. |
| `HARDENING_REQUIREMENT_CONTEXT` | Eligible only to explain hardening requirements or rationale within approved scope. |
| `DEVELOPER_LOG_CONTEXT` | Eligible only to explain historical developer-log rationale, never as standalone current truth. |
| `NOT_ANSWERABLE` | Excluded from retrieval/chat answer use. |
| `SUPERSEDED_NOT_ANSWERABLE` | Excluded from current-truth mode; may be cited only in later historical explanation mode if separately approved and labelled. |
| `CONFLICTED_NOT_ANSWERABLE` | Excluded from settled-truth answers; may be discussed only if a later answer contract permits conflict explanation. |

## 3. Answer Scopes

Future answer-use records must define answer scope by:

- `RepositoryContext`
- `DomainContext`
- answer mode, such as historical context, current truth, current truth with caveat, backlog context, doctrine context, hardening requirement context, or developer-log context
- allowed citation/provenance form
- required caveat text or caveat pointer
- revocation/removal path

Answer scopes must distinguish historical explanation from current operating truth.

Answer scopes must not silently mix historical and current truth.

Answer scopes must not allow superseded evidence to answer current-state questions.

Answer scopes must not allow conflicting evidence to answer current-state questions unless explicitly caveated and approved.

## 4. Runtime Boundary

This is a rule document only and does not implement retrieval or chat behaviour.

Future retrieval must consume answer-use permission status before evidence can be eligible for answer assembly.

Future chat must consume a later answer-mode contract, citation/provenance contract, refusal policy, and pilot-readiness gate before exposure.

## 5. Retrieval Eligibility and Answer Modes

Evidence scopes link to retrieval eligibility and answer modes through `docs/evaluation/historical_knowledge/HISTORICAL_RETRIEVAL_ELIGIBILITY_GATE.md` and `docs/evaluation/historical_knowledge/HISTORICAL_RETRIEVAL_ANSWER_MODE_MAPPING.md`.

`HISTORICAL_CONTEXT_ONLY` maps to historical-context retrieval eligibility and must not be presented as current truth.

`CURRENT_TRUTH` maps to current-truth retrieval eligibility only after current-truth approval, answer-use permission, and retrieval eligibility approval.

`CURRENT_TRUTH_WITH_CAVEAT` maps to caveated retrieval eligibility and must preserve caveats in any future answer contract.

`BACKLOG_CONTEXT_ONLY` maps to backlog/context retrieval eligibility and must not present backlog items as implemented behaviour.

`PLATFORM_DOCTRINE_CONTEXT` and `HARDENING_REQUIREMENT_CONTEXT` map to doctrine/context retrieval eligibility and must preserve source and review status.

`DEVELOPER_LOG_CONTEXT` maps to historical-context retrieval eligibility unless separately promoted.

`NOT_ANSWERABLE`, `SUPERSEDED_NOT_ANSWERABLE`, and `CONFLICTED_NOT_ANSWERABLE` map to excluded retrieval states and must not be used for current-truth answer generation.
