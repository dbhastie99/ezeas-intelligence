# Imports / Actuals Review Notes

This pack preserves the Imports / Actuals recaptured baseline result without promoting it. It records manually captured PowerShell outputs and does not invent runtime, corpus or answer-generation behaviour.

## Review Checklist

- Confirm DB readiness result is recorded as `READY`.
- Confirm result status is `RECAPTURED_BASELINE_REQUIRES_REFINEMENT`.
- Confirm benchmark result is 11 total, 8 passed, 3 failed.
- Confirm failed benchmark cases are preserved.
- Confirm corpus coverage result is STRONG=9, WEAK=1, MISSING=2.
- Confirm missing groups are `purpose_and_operator_meaning` and `outstanding_hardening`.
- Confirm weak group is `pay_code_and_rate_type_mapping`.
- Confirm answer gap report is `NEEDS_REFINEMENT`.
- Confirm formal source evidence is required before widening answer claims.
- Confirm generated JSON reports are transient and not committed.
- Confirm final ledger status remains `BASELINE_REQUIRED`.
- Confirm this recaptured result does not count as `BASELINE_ALREADY_EXISTS`.
- Confirm Imports / Actuals remains diagnostic-only and not operational truth.

## Failure Notes

Benchmark failures:

- `imports-actuals-pay-code-ratetype-mapping` missed pay code mapping, RateType mapping, platform concepts, unmapped actuals, deterministic, review and configuration issues.
- `imports-actuals-comparison-remediation-connection` missed Imports / Actuals, Comparison / Remediation, primary calculated, comparator calculated, imported actual lanes, actuals lane and variance.
- `imports-actuals-worker-story-admin-queue` failed the source-evidence check because no source snippet or matched phrase contained Worker Story, Admin Queue or mapping issues.

Coverage details:

- `purpose_and_operator_meaning` matched 0 chunks across 0 documents.
- `outstanding_hardening` matched 0 chunks across 0 documents.
- `pay_code_and_rate_type_mapping` matched 4 chunks across 1 document and is WEAK.
- `worker_story_and_admin_queue_connection` is STRONG, but the benchmark source-evidence check still failed for Worker Story, Admin Queue and mapping issues.
- `comparison_and_remediation_connection` is STRONG, but the benchmark answer still missed expected lane terms.

## Domain Checks

The next refinement run must preserve the domain boundary that Imports / Actuals is source-evidence and reconciliation context for payroll truth, not merely file upload or CSV parsing and not calculated payroll truth.

Reviewers should verify that future captured output handles:

- imported timesheet truth;
- imported payroll actuals;
- imported external/payroll-system results;
- source-to-payroll comparison;
- actual-versus-calculated reconciliation;
- validation and error-resolution workflow;
- award-specific import template expectations;
- shift assessment and attribute import expectations;
- claim and claim amount import expectations;
- RateType mapping, tenant override mapping and mapping snapshot context;
- source truth provenance and evidence preservation;
- worker story explanation context;
- no runtime mutation guarantee.

## Non-Implemented Confirmation

This slice did not implement:

- no DB writes;
- no migrations;
- no corpus mutation;
- no operational JSON ingestion;
- no Code Evidence answer integration;
- no live LLM calls;
- no endpoint/UI/workforce-platform/runtime changes;
- no import runtime changes;
- no reconciliation runtime changes;
- no PayRun runtime changes;
- no actuals ingestion runtime;
- no dirty runtime calls;
- no correction/review/payment/finalisation execution;
- finalised correction intake creation;
- review request creation;
- correction execution;
- payment or remittance execution;
- finalisation execution.

## Follow-Up

Add formal source evidence for `purpose_and_operator_meaning` and `outstanding_hardening`, tighten answer synthesis for `pay_code_and_rate_type_mapping`, and preserve the failed benchmark expectations until a documented refinement resolves them. Do not promote Imports / Actuals while benchmark failures and formal corpus gaps remain.
