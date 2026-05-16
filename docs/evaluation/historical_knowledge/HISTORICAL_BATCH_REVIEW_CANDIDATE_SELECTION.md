# Historical Batch Review Candidate Selection

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines the governed candidate-selection control model for Minerva historical batch review.

Candidate selection identifies whether a queue entry that is already registered and review-ready should be proposed, selected, blocked, deferred, rejected, or superseded for a future deep-review slice. It is a metadata/control stage only.

## 2. Scope

This model applies after metadata-only batch registration and historical batch review queueing.

It covers candidate status, priority, blocker handling, current-truth risk, duplicate or supersession risk, required repository cross-checks, and required review outputs.

It does not ingest source content, perform deep review, mutate operational corpus, create Code Evidence, write databases, call live LLMs, change runtime behaviour, promote current truth, or permit answer use.

## 3. Candidate Selection Status Model

| Candidate status | Meaning |
| --- | --- |
| `NOT_SELECTED` | No candidate-selection decision has been made for the queue entry. |
| `CANDIDATE_PROPOSED` | The queue entry is proposed for future review but has not been selected. |
| `CANDIDATE_SELECTED_FOR_REVIEW` | The queue entry is selected as a candidate for a future governed deep-review slice. This does not start review. |
| `CANDIDATE_BLOCKED` | The queue entry cannot be selected until blockers are resolved. |
| `CANDIDATE_DEFERRED` | The queue entry is relevant but intentionally deferred behind other candidates or dependency work. |
| `CANDIDATE_REJECTED` | The queue entry should not proceed to review under current controls. |
| `CANDIDATE_SUPERSEDED` | The queue entry is replaced by a newer, broader, or more authoritative source or queue entry. |

## 4. Selection Criteria

A queue entry may be selected as a candidate only when all required criteria are recorded:

- queue entry exists
- queue status is `READY_FOR_DEEP_REVIEW` or equivalent reviewed readiness status
- source id exists
- repository relevance exists
- domain relevance exists
- current-truth risk is assessed
- duplicate/supersession risk is assessed
- required cross-check repositories are identified
- expected review outputs are identified
- ingestion remains `No`
- answer use remains `No`

If any criterion is missing, the candidate status must be `CANDIDATE_BLOCKED`, `CANDIDATE_DEFERRED`, `CANDIDATE_REJECTED`, or `NOT_SELECTED`, with blockers or rationale recorded.

## 5. Priority Model

| Review priority | Meaning |
| --- | --- |
| `HIGH` | High-value or high-risk source where review could materially clarify current Minerva knowledge boundaries or implementation-state assumptions. |
| `MEDIUM` | Relevant source with useful historical value but no urgent current-truth or dependency risk. |
| `LOW` | Source may be reviewed later if capacity allows and higher-priority sources are complete. |
| `DO_NOT_REVIEW` | Source should not proceed to review, usually because it is archival-only, duplicate, superseded, out of scope, or too risky without missing controls. |

Priority does not authorize review execution, ingestion, answer use, current-truth promotion, or corpus mutation.

## 6. Blocker Handling

Use these blocker categories consistently:

- `MISSING_SOURCE_REFERENCE`
- `MISSING_REPOSITORY_CONTEXT`
- `MISSING_DOMAIN_CONTEXT`
- `CURRENT_TRUTH_RISK_UNASSESSED`
- `DUPLICATE_OR_SUPERSEDED_RISK_UNASSESSED`
- `CROSS_CHECKS_NOT_IDENTIFIED`
- `EXPECTED_OUTPUTS_NOT_DEFINED`
- `SOURCE_NOT_READY_FOR_REVIEW`

Each blocked candidate must record the blocker category, the missing control evidence, and the action needed before candidate selection can advance.

Resolving a blocker may allow selection to be reconsidered, but it does not itself start deep review or permit ingestion.

## 7. Current Truth Risk Handling

Candidate selection must assess whether the historical source could be mistaken for current truth.

High-risk sources require explicit cross-check targets before selection, including current repository context, domain context, relevant code/test/schema surfaces where applicable, and any known supersession concerns.

A candidate-selection record must preserve that historical sources are not current truth unless reviewed, cross-checked, backfilled, and governed through a separate explicit decision.

## 8. Required Cross-Checks Before Review

Before candidate selection can advance, the record must identify the repositories or evidence surfaces required for future review cross-checking.

Required cross-checks may include:

- current `ezeas-intelligence` docs/tests/control context
- current implementation repository, if separate
- current tests, schemas, commits, or doctrine relevant to the historical claims
- repository separation from `workforce-platform`, `award-configurator-v1`, and `ezeas-analytics`
- existing review-readiness records, decision records, cross-check plans, findings templates, and queue entries

Identifying cross-checks does not perform those cross-checks.

## 9. Required Outputs Before Selection Can Advance

Before a candidate can advance to `CANDIDATE_SELECTED_FOR_REVIEW`, the candidate-selection record must identify the expected future review outputs.

Expected review outputs may include:

- deep-review pack or review pack draft
- cross-check findings
- review execution checklist
- review decision gate
- review decision record
- final recommendation about whether a governed ingestion/backfill slice should be proposed later

These outputs are expected future artefacts only. Candidate selection does not create reviewed source findings.

## 10. Decision Record Requirement Before Review

Selected candidates require a decision record before any future deep review starts.

The decision record must be created through `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_DECISION_RECORD.md` and may use `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_DECISION_RECORD_TEMPLATE.md`.

`CANDIDATE_SELECTED_FOR_REVIEW` does not authorize review execution until the linked decision record explicitly permits review start with `ReviewStartPermitted: Yes`.

The decision record must preserve ingestion `No`, answer use `No`, current truth `No`, operational corpus mutation `No`, Code Evidence ingestion `No`, and live LLM use `No` unless a future governed decision explicitly changes the relevant permission.

### Deep-Review Execution Planning Boundary

Selected candidates proceed to a decision record and then to deep-review execution planning only when the decision record explicitly sets `ReviewStartPermitted: Yes`.

When review start is permitted, the future reviewer must follow `docs/evaluation/historical_knowledge/HISTORICAL_DEEP_REVIEW_EXECUTION_PLAN.md`, use `docs/evaluation/historical_knowledge/HISTORICAL_DEEP_REVIEW_EXECUTION_CHECKLIST.md`, and capture findings using `docs/evaluation/historical_knowledge/HISTORICAL_DEEP_REVIEW_FINDINGS_OUTPUT_TEMPLATE.md`.

Deep-review execution planning does not ingest source content, promote current truth, permit answer use, mutate operational corpus, create Code Evidence, write databases, call live LLM, or change runtime behaviour.

## 11. What Candidate Selection Does Not Mean

Candidate selection does not ingest source content.

Candidate selection does not perform deep review.

Candidate selection does not promote current truth.

Candidate selection does not permit answer use.

Candidate selection does not mutate operational corpus.

Candidate selection does not create Code Evidence.

Candidate selection does not write to a database.

Candidate selection does not call a live LLM.

Candidate selection does not create schema migrations, change endpoints, change UI, change workforce-platform, change award-configurator-v1, change ezeas-analytics, or change runtime behaviour.

## 12. Current Truth Boundary

Historical sources are not current truth unless reviewed, cross-checked, backfilled, and governed through a separate explicit decision.

A selected candidate remains historical source material. Selection only records that the queue entry is a controlled candidate for a future review slice.

`NOT_REVIEWED` sources remain `NOT_REVIEWED` unless a future governed review decision explicitly changes that status.

## 13. Ingestion Boundary

Ingestion remains `No` for candidate-selection records unless a future governed ingestion slice explicitly changes it.

Answer use remains `No` unless a future governed ingestion/backfill/current-truth decision explicitly changes it.

Candidate selection cannot approve governed ingestion, historical backfill, current-truth promotion, or Minerva answer use.

## 14. Developer Handoff

Future developers should use candidate-selection records to choose which review-ready queue entries should be proposed for a future deep-review slice.

Before selecting a candidate, read the source register, batch register, historical batch review queue, readiness rules, queue entry, decision records, existing review-readiness artefacts, cross-check plans, and related templates.

Do not ingest source content, mutate operational corpus, create Code Evidence, call live LLM, write databases, create migrations, change endpoints, change UI, change workforce-platform, change award-configurator-v1, change ezeas-analytics, promote current truth, permit answer use, or execute deep review from candidate selection.
