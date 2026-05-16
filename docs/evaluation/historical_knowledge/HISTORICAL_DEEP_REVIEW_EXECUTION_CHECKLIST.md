# Historical Deep Review Execution Checklist

Version: v0.1

Date: 16 May 2026

Use this checklist for governed historical deep-review execution after a decision record explicitly permits review start.

Conservative status values:

- `NOT_STARTED`
- `REQUIRED`
- `BLOCKED`
- `NOT_APPLICABLE`
- `COMPLETED_FINDINGS_ONLY`

| ChecklistItem | RequiredBeforeReviewCompletion | CurrentStatus | EvidenceRequired | BlockerIfMissing | Notes |
| --- | --- | --- | --- | --- | --- |
| Queue entry confirmed | Yes | `REQUIRED` | `QueueEntryId` and queue entry link | Yes | Required before review completion. |
| Candidate selection confirmed | Yes | `REQUIRED` | `CandidateSelectionId` and candidate-selection link | Yes | Candidate selection alone does not start review. |
| Decision record confirmed | Yes | `REQUIRED` | `DecisionRecordId` and decision-record link | Yes | Decision record must exist before review starts. |
| ReviewStartPermitted confirmed | Yes | `REQUIRED` | Decision record states `ReviewStartPermitted: Yes` | Yes | Without this value, review must not start. |
| Source identity confirmed | Yes | `REQUIRED` | `SourceId`, source title, source location | Yes | Source identity conflicts block review. |
| Source date/version assessed | Yes | `REQUIRED` | Source date, version, date range, or unknown-date blocker | Yes | Unknown date/version is a blocker unless explicitly recorded. |
| Repository/domain relevance assessed | Yes | `REQUIRED` | Repository context and domain context | Yes | Review must stay inside identified scope. |
| Required cross-check repositories identified | Yes | `REQUIRED` | Cross-check repository list | Yes | Missing cross-check targets block completion. |
| Current repository truth checked | Yes | `REQUIRED` | Current docs/code/test/log/control references or blocker | Yes | Current repository truth takes priority unless governed otherwise. |
| Findings captured | Yes | `REQUIRED` | Findings output link | Yes | Findings are review outputs only. |
| Findings classification completed before outcome decision | Yes | `REQUIRED` | Finding classification link and classification status | Yes | Findings classification is required before any outcome decision. |
| Evidence classification assigned | Yes | `REQUIRED` | Classification for each finding | Yes | Use controlled classification values. |
| Conflicts recorded | Yes | `REQUIRED` | Conflict assessment or `None` | Yes | Unresolved conflicts must remain visible. |
| Supersession risk recorded | Yes | `REQUIRED` | Supersession assessment or `None` | Yes | Duplicate/supersession unresolved blocks completion. |
| Ingestion decision kept separate | Yes | `REQUIRED` | Decision record still states `IngestionPermitted: No` or separate future decision reference | Yes | Review completion does not approve ingestion. |
| Answer-use decision kept separate | Yes | `REQUIRED` | Decision record still states `AnswerUsePermitted: No` or separate future decision reference | Yes | Review completion does not approve answer use. |
| Current-truth decision kept separate | Yes | `REQUIRED` | Decision record still states `CurrentTruthPermitted: No` or separate future decision reference | Yes | Review completion does not promote current truth. |
| Corpus mutation not performed | Yes | `REQUIRED` | Reviewer attestation | Yes | Operational corpus mutation is out of scope. |
| Code Evidence ingestion not performed | Yes | `REQUIRED` | Reviewer attestation | Yes | Code Evidence ingestion is out of scope. |
| DB write not performed | Yes | `REQUIRED` | Reviewer attestation | Yes | Database writes are out of scope. |
| Live LLM call not performed | Yes | `REQUIRED` | Reviewer attestation | Yes | Live LLM use is out of scope. |
| Review completion status recorded | Yes | `REQUIRED` | One review execution status and findings link | Yes | Status updates require documented future workflow. |
