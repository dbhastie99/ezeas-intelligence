# Tax / PAYG Review Notes

This pack preserves the Tax / PAYG recaptured baseline result without promoting it. It records manually captured PowerShell outputs and does not invent runtime, corpus or answer-generation behaviour.

## Review Checklist

- Confirm DB readiness result is recorded as `READY`.
- Confirm result status is `RECAPTURED_BASELINE_REQUIRES_REFINEMENT`.
- Confirm benchmark result is 9 total, 7 passed, 2 failed.
- Confirm failed benchmark cases are `tax-payg-rich-answer` and `tax-payg-minerva-not-calculate`.
- Confirm corpus coverage result is STRONG=10, WEAK=1, MISSING=1.
- Confirm missing group is `purpose_and_operator_meaning`.
- Confirm weak group is `outstanding_hardening`.
- Confirm answer gap report is `NEEDS_REFINEMENT`.
- Confirm formal source evidence is required before widening answer claims.
- Confirm `FORMAL_EVIDENCE_GAP_PLAN.md` records the required future evidence, acceptance criteria and non-goals before any promotion attempt.
- Confirm `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md` records current review status `NOT_REVIEWED`, blocks governed corpus ingestion until `REVIEWED_READY_FOR_INGESTION`, and preserves Tax / PAYG as `BASELINE_REQUIRED`.
- Confirm the `tax-payg-minerva-not-calculate` benchmark failure is preserved as a source-evidence/matched-phrase retrieval issue even though `deterministic_tax_boundary` is STRONG.
- Confirm generated JSON reports are transient and not committed.
- Confirm final ledger status remains `BASELINE_REQUIRED`.
- Confirm this recaptured result does not count as `BASELINE_ALREADY_EXISTS`.
- Confirm Tax / PAYG remains diagnostic-only and not operational truth.
- Confirm no ledger promotion occurred.

## Failure Notes

Benchmark failures:

- `tax-payg-rich-answer` did not contain all expected Tax / PAYG terms, including governed withholding calculation evidence, deterministic services, tax providers, TaxStory, source truth, worker tax profile, rule pack selection, frequency conversion, band/formula calculation, rounding, net-pay effect, taxable basis, taxable earnings, Payroll Bases & Totals, governed basis membership, worker tax declaration, withholding instruction, ProcessPeriod PaymentDate, payment date, pay frequency, unsupported, gross-to-net, finalised totals, supplementary incremental PAYG, same-period taxable earnings, prior PAYG withheld, Worker Story, PayRun Admin Queue and outstanding hardening.
- `tax-payg-minerva-not-calculate` failed the source-evidence check because no source snippet or matched phrase contained PAYG withholding, deterministic services or tax providers.

Coverage details:

- `purpose_and_operator_meaning` matched 0 chunks across 0 documents.
- `outstanding_hardening` matched 4 chunks across 1 document.
- `deterministic_tax_boundary` matched 4 chunks across 3 documents and includes tax providers / withholding calculation support.
- `tax_story_and_explainability` matched 10 chunks across 3 documents.
- `worker_story_and_admin_queue_connection` matched 7 chunks across 3 documents.

## Domain Checks

The next refinement run must preserve the domain boundary that Tax / PAYG is governed payroll-tax evidence and explanation context, not a generic calculator domain. Minerva must explain Tax / PAYG but must not calculate PAYG withholding.

Reviewers should verify that future captured output handles:

- governed withholding calculation evidence;
- deterministic services;
- tax providers;
- TaxStory;
- source truth;
- worker tax profile;
- rule pack selection;
- frequency conversion;
- band/formula calculation;
- rounding;
- net-pay effect;
- taxable basis;
- taxable earnings;
- Payroll Bases & Totals;
- governed basis membership;
- worker tax declaration;
- withholding instruction;
- ProcessPeriod PaymentDate;
- payment date;
- pay frequency;
- unsupported states;
- gross-to-net;
- finalised totals;
- supplementary incremental PAYG;
- same-period taxable earnings;
- prior PAYG withheld;
- Worker Story;
- PayRun Admin Queue;
- outstanding hardening;
- no runtime mutation guarantee.

## Non-Implemented Confirmation

This slice did not implement:

- no DB writes;
- no migrations;
- no corpus mutation;
- no operational JSON ingestion;
- no Code Evidence answer integration;
- no live LLM calls;
- no endpoint/UI/runtime changes;
- no workforce-platform changes;
- no payroll runtime changes;
- no tax runtime changes;
- no PAYG runtime changes;
- no correction execution;
- no payment/remittance execution;
- no finalisation execution;
- no generated artefacts committed;
- no ledger promotion.

## Follow-Up

Add formal source evidence for `purpose_and_operator_meaning`, refine retrieval terms for `outstanding_hardening`, and preserve the failed benchmark expectations until a documented refinement resolves them. Do not promote Tax / PAYG while benchmark failures and the formal corpus gap remain.

Use `FORMAL_EVIDENCE_GAP_PLAN.md` as the gap plan for any future source-evidence slice. Use `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md` as the formal evidence review gate before any governed ingestion slice can use the Tax / PAYG draft. The current review status is `NOT_REVIEWED`; governed corpus ingestion remains blocked until the gate is marked `REVIEWED_READY_FOR_INGESTION`. The plan and gate do not add source evidence, mutate corpus, ingest operational JSON, connect Code Evidence or promote the ledger.
