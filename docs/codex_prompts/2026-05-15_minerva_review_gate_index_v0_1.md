# Codex Prompt — Minerva Review Gate Index / Ingestion Guard Register v0.1

Date: 15 May 2026
Repository: ezeas-intelligence
Slice: Minerva Review Gate Index / Ingestion Guard Register v0.1
Mode: Documentation/control-register hardening only
Codex behaviour: Auto is acceptable for bounded repo-internal markdown/test edits only. Do not approve DB writes, migrations, corpus mutation, live LLM calls, endpoint changes, runtime changes, or generated artefact commits.

## Platform Context

We are continuing the Minerva completed-domain baseline program and implementing the new knowledge-maintenance operating model.

The current expected ledger state is:

- BASELINE_REQUIRED = 17
- BASELINE_ALREADY_EXISTS = 14
- RUNBOOK_OUTSTANDING = 0
- NEEDS_REVIEW = 0
- Total domains = 31

Tax / PAYG remains BASELINE_REQUIRED.

Imports / Actuals remains BASELINE_REQUIRED.

Both Tax / PAYG and Imports / Actuals have formal source-evidence paths and must not be promoted through synthesis alone.

The new knowledge-maintenance model requires repo-preserved artefacts, prompt files, review gates, source-evidence drafts, and durable control files rather than relying on chat history or copied Word documents.

## Purpose

Create a central review-gate index / ingestion guard register for Minerva baseline domains that have formal evidence drafts and review gates.

This register should make it obvious whether a domain is:

- draft-only;
- review gate created but not reviewed;
- needs revision;
- reviewed and ready for governed ingestion;
- superseded;
- blocked from ingestion;
- eligible for recapture;
- still BASELINE_REQUIRED.

## Scope

Create a new control artefact, likely:

docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md

Update or add tests in:

tests/test_domain_baseline_capture_batch.py

If there is a better existing test file for baseline-control artefacts, use that instead.

Preserve this prompt file at:

docs/codex_prompts/2026-05-15_minerva_review_gate_index_v0_1.md

## Required Register Content

The register must include at least:

1. Purpose
2. Scope
3. Status definitions
4. Ingestion decision rules
5. Current domain gate table
6. Non-goals
7. Minerva usage guidance

The current domain gate table must include:

### Imports / Actuals

- baseline status: BASELINE_REQUIRED
- evidence gap plan: present
- formal source-evidence draft: present
- review gate: present
- current review status: NOT_REVIEWED unless the existing Imports gate says otherwise
- governed ingestion permitted: No, unless REVIEWED_READY_FOR_INGESTION
- promotion permitted: No
- recapture permitted: only after governed ingestion or explicit evidence update

### Tax / PAYG

- baseline status: BASELINE_REQUIRED
- evidence gap plan: present
- formal source-evidence draft: present
- review gate: present
- current review status: NOT_REVIEWED
- governed ingestion permitted: No
- promotion permitted: No
- recapture permitted: only after governed ingestion or explicit evidence update

## Required Decision Rules

The register must state:

1. A formal source-evidence draft alone does not permit governed ingestion.
2. A review gate with NOT_REVIEWED blocks ingestion.
3. A review gate with NEEDS_REVISION blocks ingestion.
4. Only REVIEWED_READY_FOR_INGESTION can permit a future governed ingestion slice.
5. SUPERSEDED means the referenced draft/gate must not be used for ingestion.
6. Baseline promotion requires real benchmark, corpus coverage, and answer-gap evidence.
7. No domain is promoted merely because source-evidence documents exist.
8. Generated JSON artefacts remain transient unless repo convention changes.
9. Minerva must not overstate review, ingestion, runtime, or promotion state.

## Required Tests

Add focused tests to assert:

1. FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md exists.
2. The index references Imports / Actuals.
3. The index references Tax / PAYG.
4. The index states that Tax / PAYG remains BASELINE_REQUIRED.
5. The index states that Imports / Actuals remains BASELINE_REQUIRED.
6. The index states that NOT_REVIEWED blocks governed ingestion.
7. The index states that only REVIEWED_READY_FOR_INGESTION permits governed ingestion.
8. The index states that source-evidence drafts alone do not permit ingestion.
9. The index states that baseline promotion requires benchmark, corpus coverage, and answer-gap evidence.
10. The index does not mark Tax / PAYG or Imports / Actuals as promoted.

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

Do not change the completed-domain ledger counts.

Do not mark either Tax / PAYG or Imports / Actuals as BASELINE_ALREADY_EXISTS.

## Verification

Run:

```powershell
cd C:\Projects\ezeas-intelligence
python -m pytest tests\test_domain_baseline_capture_batch.py -q
git diff --check
if (Test-Path .\.pytest_tmp) { Remove-Item -Recurse -Force .\.pytest_tmp }
Test-Path .\.pytest_tmp


