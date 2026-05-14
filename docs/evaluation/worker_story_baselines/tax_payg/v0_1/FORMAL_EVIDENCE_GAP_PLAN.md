# Tax / PAYG Formal Evidence Gap Plan

Slice name: Tax / PAYG Formal Evidence Gap Plan v0.1

Domain: Tax / PAYG

This plan records why Tax / PAYG cannot be promoted solely through answer-synthesis hardening. The recaptured baseline found a formal source-evidence gap in the corpus plus weak hardening evidence, so promotion must wait for governed source evidence to be added later and for real command results to support the ledger change.

## Current Baseline Status

Tax / PAYG remains `BASELINE_REQUIRED`.

Recapture was attempted after DB readiness returned `READY`; DB readiness was not the blocker. Promotion was withheld because the benchmark failed 2 of 9 cases and the answer gap report remained `NEEDS_REFINEMENT`.

This document does not promote Tax / PAYG and does not update the completed-domain baseline ledger.

## Current Measured Results

- Benchmark: 9 total / 7 passed / 2 failed.
- Corpus coverage: 12 evidence groups; STRONG=10, WEAK=1, MISSING=1.
- Answer gap: `NEEDS_REFINEMENT`.
- Answer gap actions: 10 KEEP, 1 ADD_FORMAL_SOURCE_EVIDENCE_LATER, 1 IMPROVE_RETRIEVAL_TERMS.

Failed benchmark cases:

- `tax-payg-rich-answer`
- `tax-payg-minerva-not-calculate`

## Formal Evidence Gaps

Missing formal source evidence group:

- `purpose_and_operator_meaning`

Weak formal source evidence group:

- `outstanding_hardening`

## Why The Gaps Matter

`purpose_and_operator_meaning` matters because the corpus must contain formal evidence defining Tax / PAYG as a domain, not merely scattered tax calculation features. It should define Tax / PAYG as governed payroll-tax evidence and explanation context, not a generic calculator and not runtime calculation by Minerva.

`outstanding_hardening` matters because the corpus must preserve known implementation boundaries and future-hardening items. Future evidence must explicitly preserve no runtime tax/PAYG changes, no Minerva PAYG calculation, no hardcoded rates or thresholds, no operational JSON ingestion, no Code Evidence answer integration, no live LLM tax calculation claims and no payroll execution overclaiming.

## Required Source Evidence To Add Later

Do not add this evidence in this slice. Future governed evidence should cover:

- Tax / PAYG domain purpose.
- Tax / PAYG as governed payroll-tax evidence and explanation context.
- Minerva explains Tax / PAYG but does not calculate PAYG withholding.
- Deterministic services/tax providers own withholding calculation.
- TaxStory and explainability.
- Source truth and payroll context.
- Worker tax profile.
- Worker tax declaration.
- Withholding instruction.
- Rule-pack selection.
- Component selection.
- Taxable basis.
- Taxable earnings.
- Payroll Bases & Totals.
- Governed basis membership.
- PaymentDate.
- ProcessPeriod PaymentDate.
- Pay frequency.
- Frequency conversion.
- Band/formula calculation.
- Rounding.
- Net-pay effect.
- Gross-to-net relationship.
- Finalised totals.
- Supplementary incremental PAYG.
- Same-period taxable earnings.
- Prior PAYG withheld.
- Unsupported/skipped rules.
- Review/admin queue surfacing.
- Worker Story surfacing.
- Audit provenance.
- Explicit non-goals / outstanding hardening.

## Proposed Source Locations

Likely future source locations, without creating or ingesting anything in this slice:

- platform doctrine / hardening doctrine source docs
- tax/PAYG design notes
- gross-to-net design notes
- Payroll Bases & Totals design notes
- Process Period / PaymentDate design notes
- Worker Story / Admin Queue design notes
- future formal Tax / PAYG domain source document
- future Code Evidence source packs, only when Code Evidence integration is intentionally implemented

## Future Promotion Acceptance Criteria

Before any future promotion attempt:

- Formal source evidence is added to the corpus through the governed ingestion process.
- Coverage improves to no MISSING groups.
- `outstanding_hardening` becomes STRONG or is otherwise accepted with documented rationale.
- Benchmark passes 9/9.
- Answer gap becomes GOOD or acceptable under a documented baseline policy.
- Generated JSON remains uncommitted unless repo convention changes.
- Ledger is promoted only after real command results support it.

## Explicit Non-Goals For This Slice

This slice preserves:

- no DB writes
- no migrations
- no corpus mutation
- no operational JSON ingestion
- no Code Evidence answer integration
- no live LLM calls
- no endpoint/UI/workforce-platform/runtime changes
- no payroll runtime changes
- no tax runtime changes
- no PAYG runtime changes
- no correction/payment/finalisation execution
- no ledger promotion
