# Imports / Actuals Review Notes

This blocked pack preserves Imports / Actuals DB-readiness non-execution without inventing benchmark, coverage or answer gap output.

## Review Checklist

- Confirm DB readiness result is recorded as `DATABASE_CONNECTION_FAILED`.
- Confirm result status is `BLOCKED_DATABASE_CONNECTION`.
- Confirm benchmark result is not run.
- Confirm corpus coverage result is not run.
- Confirm answer gap report is not run.
- Confirm generated JSON reports were not produced.
- Confirm final ledger status remains `BASELINE_REQUIRED`.
- Confirm this blocked pack does not count as `BASELINE_ALREADY_EXISTS`.
- Confirm Imports / Actuals remains diagnostic-only and not operational truth.

## Domain Checks

The next captured run must preserve the domain boundary that Imports / Actuals is source-evidence and reconciliation context for payroll truth, not merely file upload or CSV parsing and not calculated payroll truth.

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

- operational JSON ingestion;
- Code Evidence answer integration;
- live LLM calls;
- corpus mutation;
- DB or schema migration;
- endpoint or UI changes;
- workforce-platform changes;
- import runtime changes;
- reconciliation runtime changes;
- PayRun runtime changes;
- actuals ingestion runtime;
- dirty runtime calls;
- finalised correction intake creation;
- review request creation;
- correction execution;
- payment or remittance execution;
- finalisation execution.

## Follow-Up

Fix SQL Server connectivity or credentials, rerun readiness, and only run the Imports / Actuals benchmark, corpus coverage diagnostic and answer gap report after readiness returns `READY`.
