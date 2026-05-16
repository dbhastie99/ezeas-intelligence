# Controlled Evaluation CI Command Pack v0.1

## 1. Purpose

Define deterministic PowerShell-only command metadata for local CI-style checks around Minerva controlled evaluation exports, batch harness output, and golden baselines.

## 2. Scope

Scope is limited to returning command metadata.

The command pack service does not execute commands, write files, expose chat, register routes, connect to a DB, call live LLMs, mutate corpus, ingest Code Evidence, or generate final answers.

## 3. PowerShell-Only Command Policy

Every command in the pack is represented as a Windows PowerShell command.

No shell chaining policy outside PowerShell is required by the pack.

## 4. Focused Test Commands

The pack includes focused pytest commands for:

- controlled evaluation batch harness tests;
- controlled evaluation report golden baseline tests;
- controlled evaluation summary export and CI command pack tests.

## 5. Compile Commands

The pack includes `python -m py_compile` for deterministic controlled evaluation services relevant to the batch harness, batch summary, summary export, and CI command pack.

## 6. Diff Check Command

The pack includes `git diff --check`.

This checks for whitespace errors in the current diff.

## 7. Pytest Temp Check

The pack includes a PowerShell `.pytest_tmp` absence check:

`if (Test-Path .pytest_tmp) { throw '.pytest_tmp exists' } else { Write-Output '.pytest_tmp absent' }`

## 8. Stop Conditions

Stop conditions are:

- any focused pytest failure;
- any `py_compile` failure;
- any `git diff --check` failure;
- `.pytest_tmp` exists after command execution.

## 9. Prohibited Commands

The command pack prohibits DB access, migration, validation, read, or write commands; live LLM, chat, endpoint, route, or final-answer-generation commands; corpus mutation or Code Evidence ingestion commands; and workforce-platform or ezeas-analytics runtime commands.

## 10. No Runtime / No DB / No LLM / No Corpus Boundary

The command pack is metadata only. It does not authorise runtime behaviour, DB access, live LLM use, corpus mutation, Code Evidence ingestion, chat exposure, endpoint exposure, route registration, or final answer generation.

## 11. What This Slice Authorises

This slice authorises deterministic PowerShell-only command metadata for local controlled evaluation regression checks.

## 12. What This Slice Does Not Authorise

This slice does not authorise command execution by the service, DB commands, live LLM commands, chat commands, endpoint commands, route commands, corpus mutation commands, Code Evidence ingestion commands, workforce-platform runtime commands, ezeas-analytics runtime commands, final-answer-generation commands, UI changes, deployment readiness, production readiness, or runtime readiness.

## 13. Developer Handoff

Use `build_controlled_evaluation_ci_command_pack` from `app/services/controlled_evaluation_ci_command_pack_service.py`.

Review the returned command metadata and run commands manually in PowerShell when appropriate for local controlled regression checks.
