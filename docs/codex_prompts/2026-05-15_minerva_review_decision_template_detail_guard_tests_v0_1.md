# Codex Prompt — Minerva Review Decision Template Detail Guard Tests v0.1

Date: 15 May 2026  
Repository: ezeas-intelligence  
Slice: Minerva Review Decision Template Detail Guard Tests v0.1  
Mode: Test-hardening only  
Codex behaviour: Auto is acceptable for bounded repo-internal test edits and prompt-file preservation only. Do not approve DB writes, migrations, corpus mutation, live LLM calls, endpoint changes, runtime changes, generated artefact commits, ledger promotion, or document rewriting beyond what is required to satisfy the quality guard.

## Platform Context

We just added the reusable formal evidence review decision record template:

docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md

We also preserved the implementation prompt at:

docs/codex_prompts/2026-05-15_minerva_formal_evidence_review_decision_record_template_v0_1.md

The next task is not a new feature. It is a focused quality-control test slice to ensure the template has the detail and safeguards required for Minerva knowledge maintenance.

## Purpose

Add stronger focused tests proving that the review decision record template is complete, detailed, and guarded against accidental overclaiming.

This should verify:

- required sections exist;
- required fillable fields exist;
- all allowed statuses exist;
- decision rules are explicit;
- Imports / Actuals and Tax / PAYG examples exist;
- non-goals are preserved;
- the template does not imply review approval, corpus ingestion, or baseline promotion.

## Scope

Update:

tests/test_domain_baseline_capture_batch.py

Preserve this prompt at:

docs/codex_prompts/2026-05-15_minerva_review_decision_template_detail_guard_tests_v0_1.md

If the constant for the template already exists, reuse it. If it does not exist, add:

```python
FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE = (
    Path("docs/evaluation/source_evidence_drafts")
    / "FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md"
)
```
