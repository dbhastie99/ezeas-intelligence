# Tax / PAYG Formal Source Evidence Draft v0.1

Slice: Tax / PAYG Formal Source Evidence Draft v0.1

Domain: Tax / PAYG

Status: reviewed draft evidence only. This document is not ingested into the corpus, does not mutate operational data, and does not promote Tax / PAYG in the completed-domain baseline ledger.

## Evidence Gap Context

This draft addresses the known Tax / PAYG formal evidence gaps from the recaptured baseline:

- `purpose_and_operator_meaning`: MISSING.
- `outstanding_hardening`: WEAK.

The recaptured baseline remains 9 total / 7 passed / 2 failed, corpus coverage STRONG=10, WEAK=1, MISSING=1, and answer gap status `NEEDS_REFINEMENT`. Tax / PAYG remains `BASELINE_REQUIRED`.

## 1. Domain Purpose And Operator Meaning

Tax / PAYG is the governed payroll-tax evidence and explanation context for Pay As You Go withholding in payroll review. It provides governed withholding calculation evidence for operator review. It is not a generic calculator, not runtime calculation by Minerva, not hardcoded tax truth in application code, and not a replacement for deterministic tax providers or deterministic payroll services.

Deterministic services and tax providers own PAYG withholding calculation. Minerva explains Tax / PAYG but does not calculate PAYG withholding. The Tax / PAYG domain provides the evidence/story layer that explains what deterministic payroll and tax services selected, calculated, skipped or could not support.

TaxStory is the explanation and evidence surface for Tax / PAYG. Operators need it because PAYG outcomes cannot be reviewed safely from a final net amount alone. Operators need source truth, worker tax profile, payroll context, rule-pack selection, component selection, frequency conversion, band/formula calculation, rounding, net-pay effect, unsupported or skipped rules, and audit provenance.

## 2. Source Truth And Payroll Context

Tax / PAYG evidence must preserve source truth and payroll context. Source truth identifies the governed evidence that deterministic services used or rejected when producing a withholding outcome.

ProcessPeriod PaymentDate and payment date are core context because PAYG treatment depends on the payment timing selected for the pay run. Pay frequency is also core context because deterministic withholding services may need to convert the taxable basis into the frequency expected by the governed rule pack.

Payroll context, pay run context, gross-to-net context and finalised totals context should be available to the explanation layer. Supplementary incremental PAYG context should preserve when the calculation is based on additional same-period or supplementary taxable amounts instead of treating the run as an isolated ordinary calculation.

## 3. Worker Tax Profile And Withholding Inputs

Worker tax profile evidence should identify the worker tax declaration and withholding instruction used by deterministic tax services. The evidence should preserve date-effective and governed inputs rather than relying on current mutable profile labels.

Where relevant, worker tax profile evidence may include residency/status flags, but it must not overclaim implementation support beyond governed source evidence and provider capability. Additional, reduced or override withholding instructions should be visible where relevant because they can change the deterministic output or explain a deliberate adjustment.

Missing, ambiguous or unsupported withholding inputs must enter review states. The evidence layer should identify whether a declaration, withholding instruction, residency/status flag or other governed input is missing, stale, ambiguous, unsupported by the provider, or blocked by configuration.

## 4. Rule-Pack Selection And Governed Tax Logic

Rule pack selection must be explicit evidence. Governed tax rule packs, tax providers and deterministic services own the tax logic used to calculate withholding. Rates, thresholds, bands, offsets and formulas are governed data, rule-pack content or provider/configuration inputs, not hardcoded tax rates, thresholds, formulas or bands in application code.

Component selection should explain which earnings, allowances, deductions or other payroll components were relevant to the taxable basis or withholding calculation. Unsupported or skipped rule handling should explain when deterministic services skipped a rule, declined a provider path, could not support a scenario, or required operator review.

Audit provenance must identify the rule pack, provider or deterministic service boundary, configuration context, source inputs and output evidence needed to review the decision later. The story must not rewrite governed tax logic into conversational tax truth.

## 5. Taxable Basis And Payroll Bases & Totals

Tax / PAYG evidence must explain the taxable basis used by deterministic services. Taxable earnings should be grounded in Payroll Bases & Totals and governed basis membership, including inclusion/exclusion evidence for the components that did or did not contribute to the basis.

Finalised totals are important because operators often need to understand the relationship between already finalised payroll evidence and current withholding context. The prior PAYG withheld, same-period taxable earnings and supplementary incremental PAYG should be visible where they affect the explanation of an incremental or supplementary withholding outcome.

Tax / PAYG should make clear whether taxable earnings came from current pay run evidence, same-period taxable earnings, supplementary taxable earnings or finalised totals context. It must not hide basis membership or prior withholding behind final net pay.

## 6. Frequency Conversion And Calculation Story

Frequency conversion evidence should explain how pay frequency affected the deterministic withholding path. The calculation story may include frequency conversion, band/formula calculation and rounding, but only as an explanation of deterministic output produced by payroll/tax services.

Calculated withholding is the deterministic output from the selected service, provider and governed rule pack. Minerva explanation only applies after that deterministic output exists or after the deterministic service reports that the case is unsupported, skipped or blocked.

The net-pay effect should show how calculated withholding changed the worker's gross-to-net result without turning Tax / PAYG into a net-pay-only story. Operators need to understand the withholding amount, the deterministic path that produced it, and the review state for unsupported or incomplete evidence.

## 7. Worker Story And Admin Queue Surfacing

Worker Story should surface TaxStory, source truth, worker tax profile, payroll context, basis membership, rule-pack selection, component selection, unsupported/skipped rules, net-pay effect and audit provenance.

Admin Queue should surface unsupported tax states, missing or ambiguous declarations, unsupported provider cases, review blockers and configuration issues. Tax / PAYG issues should not be hidden behind final net pay.

Worker Story and Admin Queue are evidence and review surfaces. They should help operators understand selected, skipped, unsupported or blocked Tax / PAYG outcomes without creating automatic correction, payment or finalisation execution.

## 8. Outstanding Hardening And Non-Goals

This source-evidence draft is bounded documentation. It records evidence expectations and hardening boundaries only.

Explicit non-goals for this slice:

- no operational JSON ingestion in current baseline work.
- no Code Evidence answer integration in current baseline work.
- no live LLM tax calculation claims.
- no runtime tax/PAYG changes.
- no PAYG calculation by Minerva.
- no hardcoded tax truth.
- no payroll execution changes.
- no automatic correction/payment/finalisation execution.
- no DB writes or migrations.
- no corpus mutation in this slice.
- no ledger promotion in this slice.
- no generated JSON committed under artifacts or reports.

Tax / PAYG remains an unpromoted baseline domain until real governed evidence ingestion and command results support a different ledger status.

## 9. Future Corpus-Ingestion Acceptance Criteria

Before this draft can support future corpus ingestion or ledger promotion:

- The draft is reviewed against Platform Doctrine and Hardening Doctrine.
- A governed ingestion process is identified.
- Corpus mutation is performed only in a separate explicit slice.
- Coverage rerun shows no MISSING groups.
- `outstanding_hardening` becomes STRONG or is documented accepted.
- Benchmark passes 9/9.
- Answer gap becomes GOOD or acceptable.
- Generated JSON remains uncommitted unless an explicit repo policy changes.
- Ledger is promoted only after real command results support promotion.

Until those criteria are met, this draft is source-evidence preparation only and Tax / PAYG is not promoted.
