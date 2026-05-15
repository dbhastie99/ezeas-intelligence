# Historical Analytics Cross-Check Findings Template

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This template records the future code/test/schema cross-check findings for a registered historical Analytics Engine source.

Template creation does not perform the cross-check, ingest the source, parse the source, extract historical source content, mutate corpus, connect Code Evidence, call live LLM, change runtime behaviour, promote baselines, change ledger counts, perform ledger promotion, or perform historical ingestion.

ProcessedRule-era analytics claims require current code/test/schema confirmation before being treated as current.

`CalcInterpreterLine` is the current target canonical processed payroll calculation fact.

A finding that something was historically implemented does not prove it remains current.

A finding that a doctrine remains valid does not prove the old implementation remains current.

Minerva may only use reviewed findings according to the Minerva-safe answering boundary recorded for each claim.

## 2. Source Register Details

| Field | Value |
| --- | --- |
| Register ID | `<REGISTER_ID>` |
| Source title | `<SOURCE_TITLE>` |
| Original filename | `<ORIGINAL_FILENAME>` |
| Source placeholder | `<SOURCE_PLACEHOLDER_PATH>` |
| Review-readiness record | `<REVIEW_READINESS_RECORD_PATH>` |
| Review pack draft placeholder | `<REVIEW_PACK_DRAFT_PLACEHOLDER_PATH>` |
| Review decision gate | `<REVIEW_DECISION_GATE_PATH>` |
| Code cross-check plan | `<CODE_CROSSCHECK_PLAN_PATH>` |
| Review status before cross-check | `<NOT_REVIEWED / OTHER>` |
| Ingestion permitted before cross-check | `<NO / YES WITH GOVERNED REFERENCE>` |

## 3. Cross-Check Execution Details

| Field | Value |
| --- | --- |
| Reviewer | `<REVIEWER>` |
| Review date | `<YYYY-MM-DD>` |
| Cross-check date | `<YYYY-MM-DD>` |
| Repositories checked | `<REPOSITORIES_CHECKED>` |
| Cross-check scope | `<SCOPE SUMMARY>` |
| Cross-check result status | `<DRAFT / COMPLETE / BLOCKED>` |
| Branches/commits checked | `<BRANCHES_AND_COMMITS_CHECKED>` |
| Files or schemas checked | `<FILES_OR_SCHEMAS_CHECKED>` |
| Tests checked | `<TESTS_CHECKED>` |
| Limitations | `<LIMITATIONS>` |

## 4. Repositories Checked

| Repository | Branches/commits checked | Scope checked | Result |
| --- | --- | --- | --- |
| `<REPOSITORY>` | `<BRANCH_OR_COMMIT>` | `<CODE_TEST_SCHEMA_SCOPE>` | `<RESULT>` |

## 5. Code/Test/Schema Evidence Reviewed

| Evidence type | Current evidence source | Files or schemas checked | Tests checked | Current evidence result | Notes |
| --- | --- | --- | --- | --- | --- |
| `<CODE / TEST / SCHEMA / DOC>` | `<PATH_OR_COMMIT>` | `<FILES_OR_SCHEMAS_CHECKED>` | `<TESTS_CHECKED>` | `<CURRENT_EVIDENCE_RESULT>` | `<NOTES>` |

## 6. Historical Claim Register

| Claim ID | Historical claim | Claim source location or summary | Claim category | Follow-up action |
| --- | --- | --- | --- | --- |
| `<CLAIM_ID>` | `<HISTORICAL_CLAIM>` | `<CLAIM_SOURCE_LOCATION_OR_SUMMARY>` | `<CLAIM_CATEGORY>` | `<FOLLOW_UP_ACTION>` |

## 7. Claim Classification Table

Use exactly one primary classification for each claim unless the review decision gate records why multiple classifications apply.

| Claim ID | Historical claim | Current evidence source | Current evidence result | Classification | Confidence | Supersession status | Minerva answer boundary | Follow-up action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<CLAIM_ID>` | `<HISTORICAL_CLAIM>` | `<CURRENT_EVIDENCE_SOURCE>` | `<CURRENT_EVIDENCE_RESULT>` | `<CLASSIFICATION>` | `<CONFIDENCE>` | `<SUPERSESSION_STATUS>` | `<MINERVA_ANSWER_BOUNDARY>` | `<FOLLOW_UP_ACTION>` |

Allowed claim classifications:

- `STILL_VALID_IMPLEMENTED_AND_TESTED`
- `STILL_VALID_DOCTRINE`
- `PARTIALLY_VALID_REQUIRES_UPDATE`
- `SUPERSEDED_BY_CALCINTERPRETERLINE_MODEL`
- `SUPERSEDED_BY_CURRENT_SCHEMA`
- `HISTORICAL_CONTEXT_ONLY`
- `BACKLOG_OR_PLANNED_NOT_IMPLEMENTED`
- `UNCERTAIN_REQUIRES_REVIEW`
- `NOT_SUPPORTED_BY_CURRENT_CODE`

## 8. Source-to-Code Evidence Map

| Claim ID | Claim source location or summary | Current evidence source | Files or schemas checked | Tests checked | Current evidence result | Classification |
| --- | --- | --- | --- | --- | --- | --- |
| `<CLAIM_ID>` | `<CLAIM_SOURCE_LOCATION_OR_SUMMARY>` | `<CURRENT_EVIDENCE_SOURCE>` | `<FILES_OR_SCHEMAS_CHECKED>` | `<TESTS_CHECKED>` | `<CURRENT_EVIDENCE_RESULT>` | `<CLASSIFICATION>` |

## 9. Still-Valid Doctrine

| Claim ID | Historical claim | Doctrine retained | Current implementation dependency | Minerva answer boundary |
| --- | --- | --- | --- | --- |
| `<CLAIM_ID>` | `<HISTORICAL_CLAIM>` | `<DOCTRINE_RETAINED>` | `<CURRENT_IMPLEMENTATION_DEPENDENCY>` | `<MINERVA_ANSWER_BOUNDARY>` |

## 10. Superseded Claims

| Claim ID | Historical claim | Supersession status | Superseding evidence | Minerva answer boundary |
| --- | --- | --- | --- | --- |
| `<CLAIM_ID>` | `<HISTORICAL_CLAIM>` | `<SUPERSESSION_STATUS>` | `<SUPERSEDING_EVIDENCE>` | `<MINERVA_ANSWER_BOUNDARY>` |

## 11. Partially Valid Claims

| Claim ID | Historical claim | Still-valid portion | Outdated portion | Required update | Follow-up action |
| --- | --- | --- | --- | --- | --- |
| `<CLAIM_ID>` | `<HISTORICAL_CLAIM>` | `<STILL_VALID_PORTION>` | `<OUTDATED_PORTION>` | `<REQUIRED_UPDATE>` | `<FOLLOW_UP_ACTION>` |

## 12. Current Implementation Findings

| Area | Current evidence source | Current evidence result | Confidence | Follow-up action |
| --- | --- | --- | --- | --- |
| `<AREA>` | `<CURRENT_EVIDENCE_SOURCE>` | `<CURRENT_EVIDENCE_RESULT>` | `<CONFIDENCE>` | `<FOLLOW_UP_ACTION>` |

## 13. Current Analytics Replatform Implications

| Implication | Evidence basis | CalcInterpreterLine impact | ProcessedRule-era impact | Follow-up action |
| --- | --- | --- | --- | --- |
| `<IMPLICATION>` | `<EVIDENCE_BASIS>` | `<CALCINTERPRETERLINE_IMPACT>` | `<PROCESSEDRULE_ERA_IMPACT>` | `<FOLLOW_UP_ACTION>` |

## 14. Minerva-Safe Answering Boundaries

| Claim ID | Classification | Minerva answer boundary | Required caveat | Follow-up action |
| --- | --- | --- | --- | --- |
| `<CLAIM_ID>` | `<CLASSIFICATION>` | `<MINERVA_ANSWER_BOUNDARY>` | `<REQUIRED_CAVEAT>` | `<FOLLOW_UP_ACTION>` |

Minerva must not answer from the analytics source as current truth until reviewed/backfilled/governed.

Minerva may only use reviewed findings according to the Minerva-safe answering boundary recorded for each claim.

## 15. Backfill Evidence Pack Recommendation

| Field | Recommendation |
| --- | --- |
| Create reviewed backfill evidence pack | `<YES / NO / BLOCKED>` |
| Recommended pack scope | `<SCOPE>` |
| Required exclusions | `<EXCLUSIONS>` |
| Required caveats | `<CAVEATS>` |
| Ingestion recommendation | `<NO / SEPARATE GOVERNED SLICE ONLY>` |

## 16. Review Decision Recommendation

| Field | Recommendation |
| --- | --- |
| Review decision | `<APPROVE_FOR_BACKFILL_DRAFT / BLOCK / NEEDS_MORE_REVIEW>` |
| Governed ingestion permitted | `<NO / SEPARATE GOVERNED SLICE ONLY>` |
| Review rationale | `<RATIONALE>` |
| Open risks | `<OPEN_RISKS>` |

## 17. Non-Goals

Creating or filling this template must not:

- Ingest historical chats.
- Ingest the full developer log.
- Parse or extract source content outside the explicit future review scope.
- Treat the source as current truth.
- Ingest doctrine documents.
- Ingest code.
- Mutate corpus.
- Connect Code Evidence.
- Call live LLM.
- Change runtime behaviour.
- Implement DB writes or migrations.
- Add endpoint changes.
- Add UI changes.
- Change `workforce-platform`, `award-configurator-v1`, or `ezeas-analytics` runtime.
- Approve review.
- Permit governed ingestion.
- Perform historical ingestion.
- Recapture baselines.
- Run benchmark execution.
- Run corpus coverage execution.
- Run answer-gap execution.
- Promote baselines.
- Change ledger counts.
- Perform ledger promotion.

No corpus mutation, no Code Evidence integration, no live LLM call, no runtime change, no baseline promotion, no ledger promotion, and no historical ingestion occur from template creation.

## 18. Required Follow-Up Actions

| Action ID | Follow-up action | Owner | Due date | Status |
| --- | --- | --- | --- | --- |
| `<ACTION_ID>` | `<FOLLOW_UP_ACTION>` | `<OWNER>` | `<YYYY-MM-DD>` | `<STATUS>` |
