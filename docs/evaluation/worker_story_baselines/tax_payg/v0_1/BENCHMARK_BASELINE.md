# Tax / PAYG Benchmark Baseline

This file records the manually captured benchmark result for the Tax / PAYG baseline pack. It is diagnostic-only and not operational truth.

## Command Executed

```powershell
python scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.tax_payg.json
```

Recaptured on 2026-05-14 from `C:\Projects\ezeas-intelligence` after DB readiness returned `READY`.

## Scope

The benchmark scope is the Tax / PAYG rich-answer manifest:

```text
samples\eval\rich_answer_benchmark.tax_payg.json
```

The manifest covers governed Tax / PAYG withholding evidence and explanation context. It expects answers to preserve Minerva's calculation boundary, TaxStory, taxable basis, Payroll Bases & Totals, ProcessPeriod PaymentDate, pay frequency support, worker tax declarations, withholding instructions, supplementary incremental PAYG, Worker Story, PayRun Admin Queue and outstanding hardening.

## Captured Result Summary

Result status: `COMPLETED_WITH_FAILURES`

Pass/fail summary:

- Golden questions: Tax / PAYG rich-answer benchmark
- Total: 9
- Passed: 7
- Failed: 2
- Audit/chat rows created: false

Benchmark result: recaptured with failures.

Baseline pack state: recaptured result, not promoted.

Generated artefact committed: no.

Live LLM calls: no.

Corpus mutation: no.

Operational JSON ingestion: no.

Code Evidence answer integration: no.

Final ledger status remains `BASELINE_REQUIRED`; this recaptured result does not count as `BASELINE_ALREADY_EXISTS`.

## Failed Cases

### `tax-payg-rich-answer`

Question: How should Tax / PAYG work in Ezeas?

Failed check:

- Answer did not contain all expected terms.

Missing expected terms:

- Tax / PAYG
- governed withholding calculation evidence
- deterministic services
- tax providers
- TaxStory
- source truth
- worker tax profile
- rule pack selection
- frequency conversion
- band/formula calculation
- rounding
- net-pay effect
- taxable basis
- taxable earnings
- Payroll Bases & Totals
- governed basis membership
- worker tax declaration
- withholding instruction
- ProcessPeriod PaymentDate
- payment date
- pay frequency
- unsupported
- gross-to-net
- finalised totals
- supplementary incremental PAYG
- same-period taxable earnings
- prior PAYG withheld
- Worker Story
- PayRun Admin Queue
- outstanding hardening

### `tax-payg-minerva-not-calculate`

Question: Why must Minerva not calculate PAYG withholding?

Failed check:

- No source snippet/matched phrase contained any expected terms.

Expected source terms:

- PAYG withholding
- deterministic services
- tax providers

The source-evidence/matched-phrase failure exists even though the corpus coverage group `deterministic_tax_boundary` is STRONG and matched tax providers / withholding calculation support.

## Boundary Expectations

Refinement must not weaken expectations that:

- Tax / PAYG is governed payroll-tax evidence and explanation context, not a generic calculator domain.
- Minerva must explain Tax / PAYG but must not calculate PAYG withholding.
- Deterministic services and tax providers own withholding calculation.
- Tax/PAYG rates, thresholds, bands, offsets and formulas are governed data/rule-pack/configuration, not hardcoded application truth.
- TaxStory explains source truth, worker tax profile, payroll context, rule-pack selection, component selection, frequency conversion, band/formula calculation, rounding, net-pay effect, unsupported/skipped rules and audit provenance.
- PaymentDate and payroll context matter for Tax / PAYG selection.
- Baseline capture does not implement tax runtime behaviour.

## Source References

- Runbook: `docs/TAX_PAYG_EVALUATION_RUNBOOK.md`
- Manifest: `samples\eval\rich_answer_benchmark.tax_payg.json`
- Runner: `scripts/run_golden_questions.py`
- Readiness check: `scripts/check_worker_story_baseline_db_readiness.py`

## Diagnostic-Only Guardrails

This benchmark baseline:

- does not mutate corpus;
- does not change routing;
- does not change answer generation;
- does not call live LLM;
- does not ingest operational JSON;
- does not connect Code Evidence;
- does not connect Code Evidence to answer generation;
- does not prove runtime platform truth;
- does not prove payroll/runtime truth;
- does not change workforce-platform.
