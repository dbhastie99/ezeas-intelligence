# Codex Prompt - Minerva Formal Evidence Review Decision Record Template v0.1

Date: 15 May 2026

Repository: ezeas-intelligence

Slice: Minerva Formal Evidence Review Decision Record Template v0.1

Mode: Documentation/control-template hardening only

Codex behaviour: Auto is acceptable for bounded repo-internal markdown/test edits only. Do not approve DB writes, migrations, corpus mutation, live LLM calls, endpoint changes, runtime changes, generated artefact commits, or ledger promotion.

## Platform Context

We are continuing the Minerva completed-domain baseline program and implementing the new knowledge-maintenance operating model.

Current expected ledger state:

- BASELINE_REQUIRED = 17
- BASELINE_ALREADY_EXISTS = 14
- RUNBOOK_OUTSTANDING = 0
- NEEDS_REVIEW = 0
- Total domains = 31

Imports / Actuals remains BASELINE_REQUIRED.

Tax / PAYG remains BASELINE_REQUIRED.

Both domains now have:

- formal evidence gap plans
- formal source-evidence drafts
- formal evidence review gates
- central review-gate index entry

The review-gate index records both domains as blocked from governed ingestion while their gates remain NOT_REVIEWED.

The next control need is a standard review decision record template so future review decisions are captured consistently and cannot be implied by chat, draft existence, or informal agreement.

## Purpose

Create a reusable Formal Evidence Review Decision Record template.

This template will be used later when a reviewer makes a formal decision on whether a domain evidence draft is:

- still NOT_REVIEWED;
- NEEDS_REVISION;
- REVIEWED_READY_FOR_INGESTION;
- SUPERSEDED.

The template must prevent shortcutting from draft text to governed ingestion.

## Scope

Create a new reusable template, likely:

docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md

Update or add focused tests in:

tests/test_domain_baseline_capture_batch.py

Preserve this prompt file at:

docs/codex_prompts/2026-05-15_minerva_formal_evidence_review_decision_record_template_v0_1.md

## Required Template Sections

The template must include these sections:

1. Review Decision Record Header
2. Domain and Baseline Status
3. Source Artefacts Reviewed
4. Review Gate Status Before Decision
5. Review Decision
6. Allowed Decision Statuses
7. Doctrine Review Findings
8. Implementation-State Review Findings
9. Evidence-Gap Coverage Findings
10. Non-Overclaiming Review
11. Ingestion Decision
12. Recapture Decision
13. Promotion Decision
14. Reviewer Details
15. Required Follow-Up Actions
16. Minerva Answering Implications
17. Non-Goals / Explicitly Not Changed

## Required Template Fields

The template must include explicit fillable fields for:

- domain name
- domain slug
- baseline status before review
- review gate file path
- formal evidence gap plan path
- formal source-evidence draft path
- review gate index path
- current review status before decision
- selected decision status
- reviewer name
- review date
- reviewed source artefacts
- doctrine review outcome
- implementation-state review outcome
- evidence-gap review outcome
- non-overclaiming review outcome
- whether governed ingestion is permitted
- whether recapture is permitted
- whether promotion is permitted
- required follow-up actions
- reviewer rationale

## Allowed Decision Statuses

The template must list these statuses exactly:

- NOT_REVIEWED
- NEEDS_REVISION
- REVIEWED_READY_FOR_INGESTION
- SUPERSEDED

## Required Decision Rules

The template must state:

1. A formal source-evidence draft alone does not permit governed ingestion.
2. A review gate with NOT_REVIEWED blocks governed ingestion.
3. A review gate with NEEDS_REVISION blocks governed ingestion.
4. A SUPERSEDED draft/gate must not be used for governed ingestion.
5. Only REVIEWED_READY_FOR_INGESTION can permit a future governed ingestion slice.
6. REVIEWED_READY_FOR_INGESTION does not itself mutate corpus.
7. REVIEWED_READY_FOR_INGESTION does not itself promote a baseline.
8. Baseline promotion requires real benchmark, corpus coverage, and answer-gap evidence after governed ingestion and recapture.
9. No domain is promoted merely because a review decision exists.
10. Minerva must not overstate review, ingestion, runtime, or promotion state.

## Required Domain Examples

The template should include short example placeholders for:

### Imports / Actuals

- baseline status before review: BASELINE_REQUIRED
- governed ingestion permitted: No unless REVIEWED_READY_FOR_INGESTION
- promotion permitted: No
- note: Imports / Actuals is not merely file upload or CSV parsing

### Tax / PAYG

- baseline status before review: BASELINE_REQUIRED
- governed ingestion permitted: No unless REVIEWED_READY_FOR_INGESTION
- promotion permitted: No
- note: Minerva may explain Tax / PAYG but must not calculate PAYG withholding

These examples must not mark either domain as reviewed or ready.

## Tests

Add focused tests to assert:

1. FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md exists.
2. The template includes all allowed statuses.
3. The template states that source-evidence drafts alone do not permit governed ingestion.
4. The template states that NOT_REVIEWED blocks governed ingestion.
5. The template states that NEEDS_REVISION blocks governed ingestion.
6. The template states that only REVIEWED_READY_FOR_INGESTION permits a future governed ingestion slice.
7. The template states that REVIEWED_READY_FOR_INGESTION does not itself mutate corpus.
8. The template states that REVIEWED_READY_FOR_INGESTION does not itself promote a baseline.
9. The template states that promotion requires benchmark, corpus coverage, and answer-gap evidence.
10. The template references Imports / Actuals without marking it reviewed.
11. The template references Tax / PAYG without marking it reviewed.
12. The template includes reviewer, date, rationale, source artefacts reviewed, and required follow-up action fields.

## Non-Goals

Do not implement:

- DB writes
- migrations
- corpus mutation
- operational JSON ingestion
- Code Evidence integration
- live LLM calls
- benchmark recapture
- baseline promotion
- ledger promotion
- endpoint changes
- UI changes
- workforce-platform changes
- award-configurator-v1 changes
- payroll runtime changes
- tax runtime changes

Do not change completed-domain ledger counts.

Do not mark Tax / PAYG or Imports / Actuals as REVIEWED_READY_FOR_INGESTION.

Do not mark Tax / PAYG or Imports / Actuals as BASELINE_ALREADY_EXISTS.

Do not create a filled review decision record yet. This slice creates the reusable template only.

## Verification

Run:

```powershell
cd C:\Projects\ezeas-intelligence
python -m pytest tests\test_domain_baseline_capture_batch.py -q
git diff --check
if (Test-Path .\.pytest_tmp) { Remove-Item -Recurse -Force .\.pytest_tmp }
Test-Path .\.pytest_tmp
git --no-pager status --short
```
