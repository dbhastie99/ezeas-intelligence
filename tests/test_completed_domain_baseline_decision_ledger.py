from pathlib import Path


LEDGER_PATH = Path("docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md")


def _ledger() -> str:
    return LEDGER_PATH.read_text(encoding="utf-8")


def test_completed_domain_baseline_decision_ledger_exists_and_is_linked_from_readme():
    assert LEDGER_PATH.exists()

    readme = Path("README.md").read_text(encoding="utf-8")

    assert "docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md" in readme


def test_completed_domain_baseline_decision_ledger_contains_status_enum_values_and_core_columns():
    ledger = _ledger()

    for status in (
        "BASELINE_REQUIRED",
        "BASELINE_ALREADY_EXISTS",
        "NO_BASELINE_NEEDED",
        "RUNBOOK_OUTSTANDING",
        "NEEDS_REVIEW",
    ):
        assert status in ledger

    for column in (
        "DomainName",
        "LatestKnownVersion",
        "HasRetrievalPlan",
        "HasBroadBenchmark",
        "HasFocusedCoverage",
        "HasCoverageDiagnostic",
        "HasAnswerGapReport",
        "HasEvaluationRunbook",
        "HasCheckedInBaselineArtefact",
        "EvidencePaths",
        "DecisionStatus",
        "DecisionReason",
        "RecommendedFollowUpSlice",
    ):
        assert column in ledger


def test_completed_domain_baseline_decision_ledger_contains_guardrails():
    ledger = _ledger()

    assert "does not mutate corpus" in ledger
    assert "does not change routing" in ledger
    assert "does not change answer generation" in ledger
    assert "does not call live LLM" in ledger
    assert "does not ingest operational JSON" in ledger
    assert "does not connect Code Evidence" in ledger
    assert "does not prove runtime platform truth" in ledger
    assert "does not create v0.5 slices automatically" in ledger


def test_completed_domain_baseline_decision_ledger_includes_required_domains_and_completed_v04_domains():
    ledger = _ledger()

    for domain in (
        "Annual Leave / Leave Management",
        "Worker Story",
        "Payroll Bases & Totals",
        "PayRun Admin Queue",
        "Movement Review",
        "Comparison / Remediation",
        "Tax / PAYG",
        "Deductions / Obligations",
        "Retro / Replay",
        "Payment Execution / Remittance",
        "Leave Accrual / Processing",
        "Finalisation Readiness",
        "Leave Source Model",
        "On-costs / Employer Liabilities",
        "Award Build / Award Evidence",
        "Imports / Actuals",
        "ObjectTime / Source Truth",
        "Contacts / Employee Appointments",
        "Process Periods / PayRun Lifecycle",
        "Costing / GL Consequence Evidence",
        "Worker Attention / Issue Resolution",
        "Gross-to-Net",
        "RateSource / Rate Story",
        "Decision Story",
        "Payroll Output",
        "Contact Payroll History",
        "Leave Requests / Leave Workflow",
        "Public Holidays",
        "Rosters / Patterns / Scheduling",
        "Award Positions / Classifications",
        "Payroll Tax / WorkCover / WIC Liability Detail",
    ):
        assert domain in ledger

    assert "PAYROLL_TAX_WORKCOVER_WIC_LIABILITY_DETAIL_EVALUATION_RUNBOOK.md" in ledger
    assert "PUBLIC_HOLIDAYS_EVALUATION_RUNBOOK.md" in ledger
    assert "ROSTERS_PATTERNS_SCHEDULING_EVALUATION_RUNBOOK.md" in ledger
    assert "AWARD_POSITIONS_CLASSIFICATIONS_EVALUATION_RUNBOOK.md" in ledger


def test_completed_domain_baseline_decision_ledger_summary_and_counts_are_documented():
    ledger = _ledger()

    assert "## Summary" in ledger
    assert "Total domains inventoried: 31" in ledger
    assert "`BASELINE_REQUIRED`: 29" in ledger
    assert "`BASELINE_ALREADY_EXISTS`: 1" in ledger
    assert "`NO_BASELINE_NEEDED`: 0" in ledger
    assert "`RUNBOOK_OUTSTANDING`: 1" in ledger
    assert "`NEEDS_REVIEW`: 0" in ledger
    assert "Domains with baseline already existing: Worker Story" in ledger
    assert "Recommended next slice: restore DB connectivity" in ledger
    assert "Domains with runbook outstanding: Annual Leave / Leave Management" in ledger


def test_completed_domain_baseline_decision_ledger_records_only_worker_story_baseline():
    ledger = _ledger()

    assert "This summary is not authorization to run benchmarks" in ledger
    assert "For every other completed v0.4 domain, this ledger does not claim baseline capture has already happened" in ledger
    assert "blocked v0.1 capture packs" in ledger
    assert "They are not counted as `BASELINE_ALREADY_EXISTS`" in ledger
    assert "| Worker Story | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "docs/evaluation/worker_story_baselines/worker_story/v0_1/BASELINE_SUMMARY.md" in ledger
    assert "BASELINE_ALREADY_EXISTS | Worker Story now has a checked-in baseline artefact pack" in ledger
    assert "| Payroll Tax / WorkCover / WIC Liability Detail | v0.4 | yes | yes | yes | yes | yes | yes | no |" in ledger
