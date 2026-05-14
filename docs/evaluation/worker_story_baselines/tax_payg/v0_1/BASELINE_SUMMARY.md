# Tax / PAYG Baseline Summary

Slice name: Tax / PAYG Baseline Recapture Result Update v0.1

Domain: Tax / PAYG

Source runbook: `docs/TAX_PAYG_EVALUATION_RUNBOOK.md`

Source decision ledger: `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`

Baseline policy: `docs/evaluation/worker_story_baselines/BASELINE_CAPTURE_POLICY.md`

This recaptured baseline result pack is diagnostic-only and not operational truth. It records manually captured PowerShell command outputs after DB readiness returned `READY`. Tax / PAYG remains `BASELINE_REQUIRED` because the benchmark failed 2 of 9 cases and the answer gap report is `NEEDS_REFINEMENT` with a formal corpus gap.

This is not a successful captured/promoted baseline. It is not DB-blocked. It is a recaptured baseline result requiring refinement and formal source evidence.

## Execution Context

Recaptured on 2026-05-14 from `C:\Projects\ezeas-intelligence`.

DB readiness returned `READY` in normal PowerShell before capture.

- Readiness status: `READY`
- Ready: yes.
- Configuration source: `.env:MINERVA_DATABASE_URL`
- Selected ODBC driver: `ODBC Driver 17 for SQL Server`
- Required tables checked: `KnowledgeDocument`, `KnowledgeChunk`
- Missing tables: none.
- Read-only guardrails remained in place.

## Commands

| Area | Command | Completed | Captured Result Summary |
|---|---|---:|---|
| Tax / PAYG benchmark | `python scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.tax_payg.json` | yes | 9 total / 7 passed / 2 failed; audit/chat rows created: false. |
| Corpus coverage diagnostic | `python scripts\scan_tax_payg_corpus_coverage.py` | yes | 12 evidence groups; STRONG=10, WEAK=1, MISSING=1; indexed corpus 5 active documents, 4583 chunks. |
| Corpus coverage JSON | `python scripts\scan_tax_payg_corpus_coverage.py --json --output .\artifacts\eval\tax_payg_corpus_coverage.json` | yes | Generated transient JSON; committed: no. |
| Answer gap report | `python scripts\build_tax_payg_answer_gap_report.py --coverage-report .\artifacts\eval\tax_payg_corpus_coverage.json` | yes | `NEEDS_REFINEMENT`; 10 LOW / KEEP groups, 1 MEDIUM / IMPROVE_RETRIEVAL_TERMS group, 1 HIGH / ADD_FORMAL_SOURCE_EVIDENCE_LATER group. |
| Answer gap report JSON | `python scripts\build_tax_payg_answer_gap_report.py --coverage-report .\artifacts\eval\tax_payg_corpus_coverage.json --json --output .\artifacts\eval\tax_payg_answer_gap_report.json` | yes | Generated transient JSON; committed: no. |

## Captured Finding

- DB readiness result: `READY`.
- Result status: `RECAPTURED_BASELINE_REQUIRES_REFINEMENT`.
- Baseline pack state: recaptured result, not promoted.
- Benchmark result: 9 total, 7 passed, 2 failed.
- Failed benchmark cases: `tax-payg-rich-answer`, `tax-payg-minerva-not-calculate`.
- Corpus coverage result: STRONG=10, WEAK=1, MISSING=1.
- Missing coverage group: `purpose_and_operator_meaning`.
- Weak coverage group: `outstanding_hardening`.
- Answer gap report: `NEEDS_REFINEMENT`.
- Answer gap actions: 10 KEEP, 1 IMPROVE_RETRIEVAL_TERMS, 1 ADD_FORMAL_SOURCE_EVIDENCE_LATER.
- Indexed corpus: 5 active documents, 4583 chunks.
- Generated artefact committed: no.
- Live LLM calls: no.
- Corpus mutation: no.
- Operational JSON ingestion: no.
- Code Evidence answer integration: no.
- Final ledger status remains `BASELINE_REQUIRED`.
- This recaptured result does not count as `BASELINE_ALREADY_EXISTS`.
- No ledger promotion occurred.

Tax / PAYG has a real formal source-evidence gap for `purpose_and_operator_meaning` plus weak `outstanding_hardening` retrieval support. Promotion cannot happen solely through synthesis hardening unless the missing formal source evidence is addressed or the coverage plan is legitimately revised with justification.

## Domain Boundary To Preserve

Tax / PAYG is governed payroll-tax evidence and explanation context, not a generic calculator domain. Minerva must explain Tax / PAYG but must not calculate PAYG withholding.

The next refinement slice must preserve evidence for:

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
- outstanding hardening.

Current doctrine to preserve:

- Deterministic services and tax providers own withholding calculation.
- Tax/PAYG rates, thresholds, bands, offsets and formulas must be governed data/rule-pack/configuration, not hardcoded application truth.
- TaxStory should explain source truth, worker tax profile, payroll context, rule-pack selection, component selection, frequency conversion, band/formula calculation, rounding, net-pay effect, unsupported/skipped rules and audit provenance.
- PaymentDate and payroll context matter for Tax / PAYG selection.
- Baseline capture does not implement tax runtime behaviour.

## Not Implemented

This pack does not implement or claim:

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

## Guardrails

This recaptured baseline result pack:

- does not mutate corpus;
- does not change routing;
- does not change answer generation;
- does not call live LLM;
- does not ingest operational JSON;
- does not connect Code Evidence;
- does not connect Code Evidence to answer generation;
- does not prove runtime tax/PAYG truth;
- does not prove PAYG withholding calculation truth;
- does not prove all pay frequencies are supported;
- does not create payroll/runtime truth;
- does not create DB schema or migrations;
- does not add endpoints or UI;
- does not change workforce-platform;
- does not create v0.5 slices automatically.

## Recommended Next Slice

Add formal source evidence later for `purpose_and_operator_meaning` before widening Tax / PAYG answer claims. Refine retrieval terms for weak `outstanding_hardening` support, preserve the failed benchmark expectations, and rerun benchmark, corpus coverage and answer gap diagnostics before considering promotion.
