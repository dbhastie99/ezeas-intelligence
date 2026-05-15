# Historical Batch Triage Process

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This process defines how metadata-level historical source batches are triaged before any source graduates to the full review chain.

Batch triage does not ingest historical content, does not mutate corpus, does not connect Code Evidence, does not call live LLM, does not change runtime behaviour, does not promote baselines, does not change ledger counts, and does not perform ledger promotion.

Minerva must not treat batch-registered sources as current truth unless later reviewed, backfilled, and governed.

## 2. Inputs

Use:

- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REGISTRATION_AND_TRIAGE_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REGISTER_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_DEVELOPER_LOG_BATCH_INTAKE_GUIDANCE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER_VALIDATION_RUNBOOK.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_TIERING_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_PROCESS.md`

## 3. Triage Outcomes

Use one primary outcome:

| Outcome | Meaning |
| --- | --- |
| `REGISTER_ONLY` | Register metadata and take no further action until needed. |
| `REGISTER_AND_MONITOR` | Register metadata and monitor for later domain relevance or supersession risk. |
| `NEEDS_DOMAIN_REVIEW` | Domain owner review is required before backfill reliance. |
| `NEEDS_CODE_CROSSCHECK` | Implementation claims or current-state risk require code/test/schema confirmation. |
| `NEEDS_FULL_REVIEW_CHAIN` | The source must graduate to review-readiness, decision gate, cross-check plan, findings, and decision record. |
| `SUPERSEDED_HISTORICAL_ONLY` | Source is useful as historical context only and should not drive current truth. |
| `DUPLICATE_OR_COVERED_BY_EXISTING_SOURCE` | Source is duplicative or adequately represented by an existing registered source. |
| `UNCERTAIN_REQUIRES_REVIEW` | Metadata or provenance is insufficient; review is required before reliance. |

## 4. Escalation Criteria For Full Review Chain

Escalate to the full review chain when any criterion applies:

- Source contains major architecture decisions.
- Source may be superseded by later platform changes.
- Source will influence current Minerva answers.
- Source covers high-risk domains such as payroll calculation, ObjectTime source truth, tax, imports/actuals, reconciliation, deductions/obligations, leave, worker story, analytics, award configurator, or finalised correction.
- Source contains conflicting claims.
- Source contains implementation claims requiring code/test/schema confirmation.

## 5. Ordinary Source Handling

Ordinary developer logs can remain batch-registered until needed.

Many sources can be grouped by domain/date range rather than creating separate deep-review artefacts for every file. Grouping is allowed when the register preserves enough metadata to find the source later and no current-answer, high-risk, conflicting, or implementation-state claim requires immediate deep review.

## 6. Triage Workflow

1. Identify source metadata without parsing or extracting historical source content.
2. Assign or propose source type, source tier, domain tags, review status, implementation-state classification, supersession risk, backfill priority, and whether a full review chain is required.
3. Record `Ingestion permitted` as `No` unless a later explicit governed ingestion slice has already authorized a different state.
4. Record `Review status` as `NOT_REVIEWED` unless a later explicit review decision has already authorized a different state.
5. Record `Implementation-state classification` as `UNCERTAIN_REQUIRES_REVIEW` unless the operator has strong evidence from the document/register context.
6. Choose one triage outcome.
7. Update the governing register or prepare a batch register entry for later register update.
8. Escalate only high-value/high-risk sources to the full review-readiness / decision-gate / cross-check path.

## 7. Boundaries

Batch triage does not ingest source content.

Batch triage does not parse developer logs, doctrine documents, historical chats, continuance prompts, hardening logs, code, tests, or prompt files for historical claims.

Batch triage does not mutate corpus, connect Code Evidence, call live LLM, change runtime behaviour, promote baselines, change ledger counts, perform ledger promotion, implement DB writes or migrations, add endpoint or UI changes, approve review, perform governed ingestion, perform historical ingestion, run recapture, run benchmark execution, run corpus coverage execution, run answer-gap execution, or create generated artefacts.
