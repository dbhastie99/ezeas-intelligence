# Historical Deep Review Execution Plan

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines the governed execution plan for future Minerva historical deep review.

The plan controls how a reviewer must proceed after a historical source has a queue entry, a candidate-selection record, and a decision record that explicitly permits review start. It defines review steps, required cross-checks, findings capture, review-output expectations, and stop/go boundaries.

## 2. Scope

This execution plan applies to historical source review only after the required queue, candidate-selection, and decision-record controls exist.

It is documentation/control guidance only. It does not perform deep review, ingest source content, backfill corpus, mutate operational evidence, promote current truth, or change answer synthesis.

## 3. Review Execution Status Model

| Review execution status | Meaning |
| --- | --- |
| `REVIEW_NOT_STARTED` | No governed deep-review execution has started. |
| `REVIEW_START_PERMITTED_NOT_STARTED` | The decision record permits review start, but review has not begun. |
| `REVIEW_IN_PROGRESS` | A reviewer is executing the governed review process and capturing findings only. |
| `REVIEW_BLOCKED` | Review cannot proceed because required controls, evidence, source identity, or cross-check access is missing. |
| `REVIEW_DEFERRED` | Review is intentionally postponed after review start was considered or permitted. |
| `REVIEW_COMPLETED_FINDINGS_ONLY` | Findings were captured, but no ingestion, answer-use, or current-truth decision has been approved. |
| `REVIEW_COMPLETED_REQUIRES_CROSS_CHECK` | Findings were captured, but required cross-checks remain incomplete. |
| `REVIEW_COMPLETED_REJECT_SOURCE` | Review findings recommend rejecting the source under current controls. |
| `REVIEW_COMPLETED_SUPERSEDED` | Review findings indicate the source is superseded by newer or more authoritative material. |
| `REVIEW_COMPLETED_READY_FOR_INGESTION_DECISION` | Review findings may support a future separate ingestion decision, but ingestion is not approved. |

## 4. Preconditions Before Review Starts

Before any future deep review starts, all preconditions must be true and recorded:

- `QueueEntryId` exists.
- `CandidateSelectionId` exists.
- `DecisionRecordId` exists.
- `SourceId` exists.
- `ReviewStartPermitted` is Yes in the decision record.
- `IngestionPermitted` remains No.
- `AnswerUsePermitted` remains No.
- `CurrentTruthPermitted` remains No.
- `OperationalCorpusMutationPermitted` remains No.
- `CodeEvidenceIngestionPermitted` remains No.
- `LiveLLMUsePermitted` remains No.
- Required cross-check repositories are identified.
- Expected review outputs are identified.

## 5. Review Steps

A future reviewer must:

1. Confirm source identity.
2. Confirm source date/version if known.
3. Confirm repository/domain relevance.
4. Extract claims/decisions as review findings only.
5. Classify each finding as candidate historical evidence, superseded evidence, duplicate evidence, conflicting evidence, or not relevant.
6. Compare against current repository/domain truth where required.
7. Record unresolved conflicts.
8. Record required follow-up decisions.
9. Produce findings output.
10. Update decision record status only through documented future workflow, not runtime mutation in this slice.

## 6. Cross-Check Requirements

Required cross-checking must be identified and performed by a future governed review workflow where relevant:

- `workforce-platform` cross-check where source affects workforce/platform/runtime doctrine.
- `award-configurator-v1` cross-check where source affects award build/configuration/parser/interpreter truth.
- `ezeas-analytics` cross-check where source affects analytics/reporting schema/view/readiness truth.
- `ezeas-intelligence` cross-check where source affects Minerva retrieval/evidence/answering doctrine.
- Current repository files and latest committed logs must take priority over unreviewed historical material unless the decision record says otherwise.

## 7. Findings Capture Requirements

Findings are review outputs only. In this plan, findings are review outputs only.

Findings do not become current truth automatically.

Each findings record must link to:

- `SourceId`
- `DecisionRecordId`
- Reviewer
- ReviewDate
- source location
- evidence excerpt/summary
- cross-check status
- recommended decision

Findings must distinguish fact, decision, doctrine, backlog item, historical note, superseded item, and conflict.

## 8. Evidence Classification Requirements

Each finding must use one or more controlled classifications:

- `CANDIDATE_HISTORICAL_EVIDENCE`
- `CURRENT_TRUTH_CANDIDATE_REQUIRES_APPROVAL`
- `SUPERSEDED_EVIDENCE`
- `DUPLICATE_EVIDENCE`
- `CONFLICTING_EVIDENCE`
- `BACKLOG_OR_FOLLOW_UP`
- `NOT_RELEVANT`
- `REQUIRES_REPOSITORY_CROSS_CHECK`

## 9. Conflict / Supersession Handling

Conflicts and supersession risks must be recorded as findings, not resolved by silent promotion.

When historical material conflicts with current repository files, committed logs, tests, schemas, current control documents, or more recent decision records, the current source remains authoritative unless a separate future governed decision explains otherwise.

Duplicate or superseded material must be marked with the related source, record, or repository reference when known. If the reviewer cannot determine duplicate or supersession status, review must remain blocked or completed with cross-check required.

## 10. Stop Conditions

Review must stop or remain blocked when any of these conditions exist:

- missing source reference;
- missing decision record;
- `ReviewStartPermitted` is not Yes;
- source identity conflict;
- duplicate/supersession unresolved;
- required cross-check unavailable;
- reviewer cannot determine date/version;
- findings would require corpus mutation, Code Evidence ingestion, DB write, live LLM call, current-truth promotion, or answer-use permission.

## 11. Completion Criteria

Review execution can be marked complete only when:

- findings output is completed;
- cross-check status is recorded;
- unresolved blockers are listed;
- ingestion decision remains separate;
- answer-use decision remains separate;
- current-truth decision remains separate;
- no corpus mutation occurs;
- no Code Evidence ingestion occurs;
- no live LLM call occurs;
- no DB write occurs.

## 12. Post-Review Decision Boundaries

Review completion may recommend ingestion consideration, but does not approve ingestion.

Review completion may recommend answer-use consideration, but does not approve answer use.

Review completion may recommend current-truth consideration, but does not promote current truth.

Completed findings must flow into `docs/evaluation/historical_knowledge/HISTORICAL_REVIEW_FINDINGS_CLASSIFICATION_MODEL.md` before any ingestion, answer-use, or current-truth decision can be considered. Findings classification is a required control step between findings output and any later outcome decision.

A separate decision record update and future governed ingestion/backfill slice are required before any operational use.

## 13. What Deep Review Execution Planning Does Not Mean

Creating the execution plan does not perform deep review.

Creating the execution plan does not ingest source content.

Creating the execution plan does not promote current truth.

Creating the execution plan does not permit answer use.

Creating the execution plan does not mutate operational corpus.

Creating the execution plan does not create Code Evidence.

Creating the execution plan does not write to a database.

Creating the execution plan does not call a live LLM.

## 14. Developer Handoff

Future developers must use this execution plan only after a queue entry, candidate-selection record, and decision record exist and the decision record explicitly sets `ReviewStartPermitted: Yes`.

Use `docs/evaluation/historical_knowledge/HISTORICAL_DEEP_REVIEW_EXECUTION_CHECKLIST.md` before review completion and `docs/evaluation/historical_knowledge/HISTORICAL_DEEP_REVIEW_FINDINGS_OUTPUT_TEMPLATE.md` for findings output.

Do not ingest source content, mutate operational corpus, create Code Evidence, call live LLM, write databases, create migrations, change endpoints, change UI, change workforce-platform, change award-configurator-v1, change ezeas-analytics, promote current truth, permit answer use, or execute deep review merely because this plan exists.
