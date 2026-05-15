# Tax / PAYG Formal Evidence Review Gate v0.1

Slice: Tax / PAYG Formal Evidence Review Gate v0.1

Domain: Tax / PAYG

Review gate version: v0.1

Current review status: `NOT_REVIEWED`

Default review status: `NOT_REVIEWED`

This review gate prevents shortcutting from draft text directly into Minerva corpus evidence. The Tax / PAYG formal source-evidence draft is not approved for governed corpus ingestion until it has been reviewed for doctrine accuracy, implementation-state accuracy, evidence-gap coverage and non-overclaiming.

Tax / PAYG remains `BASELINE_REQUIRED`. This gate does not ingest the draft, mutate the corpus, mutate the database, recapture the benchmark or promote Tax / PAYG.

## Source Artefacts Under Review

- `docs/evaluation/worker_story_baselines/tax_payg/v0_1/FORMAL_EVIDENCE_GAP_PLAN.md`
- `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_SOURCE_EVIDENCE_DRAFT_v0_1.md`
- Tax / PAYG baseline recapture result: 9 total / 7 passed / 2 failed; corpus coverage STRONG=10, WEAK=1, MISSING=1; answer gap `NEEDS_REFINEMENT`; ledger status remains `BASELINE_REQUIRED`.

## Required Review Outcomes

A reviewer must record exactly one explicit status before any governed ingestion slice can use the draft:

- `NOT_REVIEWED`
- `NEEDS_REVISION`
- `REVIEWED_READY_FOR_INGESTION`
- `SUPERSEDED`

This slice records the default and current status as `NOT_REVIEWED`. It does not mark the draft as reviewed or ready for ingestion.

## Doctrine Review Checklist

Before status can move to `REVIEWED_READY_FOR_INGESTION`, the reviewer must confirm that the draft accurately preserves these doctrine boundaries:

- Minerva may explain Tax / PAYG doctrine, source evidence, implementation state and known gaps.
- Minerva must not calculate PAYG withholding.
- Tax / PAYG is governed payroll-tax evidence and explanation context, not a generic calculator domain.
- Deterministic services, tax providers and governed rule packs own PAYG withholding calculation.
- TaxStory explains selected, skipped, unsupported or blocked Tax / PAYG outcomes without rewriting governed tax logic into conversational tax truth.
- Source truth, worker tax profile, payroll context, rule-pack selection, component selection, taxable basis, frequency conversion, rounding, net-pay effect and audit provenance remain evidence/explanation concepts.
- Tax / PAYG remains `BASELINE_REQUIRED` until real recapture evidence supports promotion.
- The formal source-evidence draft is not enough by itself to permit ingestion.
- Governed ingestion must not happen until this review gate is marked `REVIEWED_READY_FOR_INGESTION`.
- This review gate is a control artefact, not a runtime feature.
- No runtime behaviour is claimed unless already implemented and evidenced.

## Implementation-State Review Checklist

The reviewer must confirm that the draft does not claim any of these are implemented:

- operational JSON ingestion.
- Code Evidence answer integration.
- live LLM answer integration or live LLM tax calculation.
- corpus mutation has occurred.
- tax runtime changes.
- PAYG runtime changes.
- payroll execution changes.
- endpoint changes.
- UI changes.
- workforce-platform changes.
- award-configurator-v1 changes.
- runtime tax calculation.
- runtime PAYG calculation.
- Minerva PAYG calculation.
- hardcoded tax rates, thresholds, formulas or bands in application code.
- automatic correction, payment, remittance or finalisation execution.

## Evidence-Gap Coverage Review Checklist

The reviewer must confirm that the draft addresses these gap and coverage terms:

- `purpose_and_operator_meaning`
- `outstanding_hardening`
- governed withholding calculation evidence
- deterministic services
- tax providers
- TaxStory
- source truth
- worker tax profile
- worker tax declaration
- withholding instruction
- rule-pack selection
- component selection
- taxable basis
- taxable earnings
- Payroll Bases & Totals
- governed basis membership
- ProcessPeriod PaymentDate
- payment date
- pay frequency
- frequency conversion
- band/formula calculation
- rounding
- net-pay effect
- gross-to-net relationship
- finalised totals
- supplementary incremental PAYG
- same-period taxable earnings
- prior PAYG withheld
- unsupported/skipped rules
- Worker Story
- PayRun Admin Queue
- audit provenance
- no runtime mutation guarantee

## Ingestion Decision

Current ingestion decision: governed corpus ingestion is blocked.

A future ingestion slice may proceed only in a future explicit ingestion slice after review readiness, and only after all of these are true:

- Status is `REVIEWED_READY_FOR_INGESTION`.
- Reviewer, date and evidence are recorded.
- The ingestion mechanism is identified.
- Corpus mutation is explicitly in scope for that future slice.
- Tests are updated for the ingestion path.
- Generated JSON policy is confirmed.
- Baseline recapture plan is attached.

## Reviewer Notes

Reviewer: not assigned.

Review date: not recorded.

Evidence reviewed: not recorded.

Decision notes: not reviewed. The draft is not approved for governed corpus ingestion.

## Minerva Implication

Minerva may explain Tax / PAYG doctrine, source evidence, implementation state and known gaps from approved corpus evidence. This review gate does not add approved corpus evidence and does not widen answer claims by itself.

Tax / PAYG remains `BASELINE_REQUIRED` until governed ingestion, recapture, corpus coverage evidence, answer-gap evidence and benchmark evidence support a later promotion decision.

## Future Recapture Acceptance Criteria

Tax / PAYG may be promoted only after real command results show:

- coverage improves to no MISSING groups.
- `outstanding_hardening` becomes STRONG or is otherwise accepted with documented rationale.
- benchmark passes 9/9.
- answer gap becomes GOOD or acceptable under documented baseline policy.
- ledger promotion is performed only after successful recapture.

## Non-Goals

This slice preserves:

- no DB writes
- no migrations
- no corpus mutation
- no operational JSON ingestion
- no Code Evidence answer integration
- no live LLM calls
- no runtime tax calculation
- no PAYG calculation
- no payroll runtime changes
- no endpoint changes
- no UI changes
- no workforce-platform changes
- no award-configurator-v1 changes
- no benchmark recapture
- no baseline promotion
- no ledger promotion
- no generated artefact commits
