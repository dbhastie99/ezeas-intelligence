import subprocess
from pathlib import Path


BASELINE_ROOT = Path("docs/evaluation/worker_story_baselines")
LEDGER_PATH = BASELINE_ROOT / "COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md"
CLOSEOUT_PATH = BASELINE_ROOT / "BASELINE_BATCH_CLOSEOUT_2026_05_13.md"
MATURITY_CLOSEOUT_PATH = BASELINE_ROOT / "BASELINE_MATURITY_CLOSEOUT_2026_05_13.md"
WORKER_STORY_PACK = BASELINE_ROOT / "worker_story" / "v0_1"
ANNUAL_LEAVE_PACK = BASELINE_ROOT / "annual_leave" / "v0_1"
CORE_PAYROLL_BLOCKED_CLOSEOUT_PATH = BASELINE_ROOT / "CORE_PAYROLL_EXPLANATION_BASELINE_BATCH_2026_05_13.md"
CORE_PAYROLL_CLOSEOUT_PATH = BASELINE_ROOT / "CORE_PAYROLL_EXPLANATION_BATCH_CLOSEOUT_2026_05_13.md"
PAYROLL_EVIDENCE_CONTEXT_BLOCKED_CLOSEOUT_PATH = (
    BASELINE_ROOT / "PAYROLL_EVIDENCE_CONTEXT_BASELINE_BATCH_2026_05_13.md"
)
REQUIRED_FILES = (
    "BASELINE_SUMMARY.md",
    "BENCHMARK_BASELINE.md",
    "CORPUS_COVERAGE_BASELINE.md",
    "ANSWER_GAP_REPORT_BASELINE.md",
    "REVIEW_NOTES.md",
)

CAPTURED_BATCH_DOMAINS = {
    "payroll_bases_totals": {
        "name": "Payroll Bases & Totals",
        "runbook": "docs/PAYROLL_BASES_AND_TOTALS_EVALUATION_RUNBOOK.md",
        "manifest": "samples\\eval\\rich_answer_benchmark.payroll_bases_and_totals.json",
        "scan": "scripts\\scan_payroll_bases_corpus_coverage.py",
        "gap": "scripts\\build_payroll_bases_answer_gap_report.py",
    },
    "payrun_admin_queue": {
        "name": "PayRun Admin Queue",
        "runbook": "docs/PAYRUN_ADMIN_QUEUE_EVALUATION_RUNBOOK.md",
        "manifest": "samples\\eval\\rich_answer_benchmark.payrun_admin_queue.json",
        "scan": "scripts\\scan_payrun_admin_queue_corpus_coverage.py",
        "gap": "scripts\\build_payrun_admin_queue_answer_gap_report.py",
    },
    "movement_review": {
        "name": "Movement Review",
        "runbook": "docs/MOVEMENT_REVIEW_EVALUATION_RUNBOOK.md",
        "manifest": "samples\\eval\\rich_answer_benchmark.movement_review.json",
        "scan": "scripts\\scan_movement_review_corpus_coverage.py",
        "gap": "scripts\\build_movement_review_answer_gap_report.py",
    },
    "gross_to_net": {
        "name": "Gross-to-Net",
        "runbook": "docs/GROSS_TO_NET_EVALUATION_RUNBOOK.md",
        "manifest": "samples\\eval\\rich_answer_benchmark.gross_to_net.json",
        "scan": "scripts\\scan_gross_to_net_corpus_coverage.py",
        "gap": "scripts\\build_gross_to_net_answer_gap_report.py",
    },
}

PAYROLL_OUTPUT_CAPTURED_DOMAIN = {
    "name": "Payroll Output",
    "runbook": "docs/PAYROLL_OUTPUT_EVALUATION_RUNBOOK.md",
    "manifest": "samples\\eval\\rich_answer_benchmark.payroll_output.json",
    "scan": "scripts\\scan_payroll_output_corpus_coverage.py",
    "gap": "scripts\\build_payroll_output_answer_gap_report.py",
}

RATE_SOURCE_RATE_STORY_CAPTURED_DOMAIN = {
    "name": "RateSource / Rate Story",
    "runbook": "docs/RATE_SOURCE_RATE_STORY_EVALUATION_RUNBOOK.md",
    "manifest": "samples\\eval\\rich_answer_benchmark.rate_source_rate_story.json",
    "scan": "scripts\\scan_rate_source_rate_story_corpus_coverage.py",
    "gap": "scripts\\build_rate_source_rate_story_answer_gap_report.py",
}

DECISION_STORY_CAPTURED_DOMAIN = {
    "name": "Decision Story",
    "runbook": "docs/DECISION_STORY_EVALUATION_RUNBOOK.md",
    "manifest": "samples\\eval\\rich_answer_benchmark.decision_story.json",
    "scan": "scripts\\scan_decision_story_corpus_coverage.py",
    "gap": "scripts\\build_decision_story_answer_gap_report.py",
}

FINALISATION_READINESS_CAPTURED_DOMAIN = {
    "name": "Finalisation Readiness",
    "runbook": "docs/FINALISATION_READINESS_EVALUATION_RUNBOOK.md",
    "manifest": "samples\\eval\\rich_answer_benchmark.finalisation_readiness.json",
    "scan": "scripts\\scan_finalisation_readiness_corpus_coverage.py",
    "gap": "scripts\\build_finalisation_readiness_answer_gap_report.py",
}

CONTACT_PAYROLL_HISTORY_CAPTURED_DOMAIN = {
    "name": "Contact Payroll History",
    "runbook": "docs/CONTACT_PAYROLL_HISTORY_EVALUATION_RUNBOOK.md",
    "manifest": "samples\\eval\\rich_answer_benchmark.contact_payroll_history.json",
    "scan": "scripts\\scan_contact_payroll_history_corpus_coverage.py",
    "gap": "scripts\\build_contact_payroll_history_answer_gap_report.py",
}

PAYROLL_EVIDENCE_CONTEXT_BLOCKED_DOMAINS = {}

PROCESS_PERIODS_PAYRUN_LIFECYCLE_RECAPTURED_DOMAIN = {
    "name": "Process Periods / PayRun Lifecycle",
    "runbook": "docs/PROCESS_PERIOD_PAYRUN_LIFECYCLE_EVALUATION_RUNBOOK.md",
    "manifest": "samples\\eval\\rich_answer_benchmark.process_period_payrun_lifecycle.json",
    "scan": "scripts\\scan_process_period_payrun_lifecycle_corpus_coverage.py",
    "gap": "scripts\\build_process_period_payrun_lifecycle_answer_gap_report.py",
}

OBJECTTIME_SOURCE_TRUTH_RECAPTURED_DOMAIN = {
    "name": "ObjectTime / Source Truth",
    "runbook": "docs/OBJECTTIME_SOURCE_TRUTH_EVALUATION_RUNBOOK.md",
    "manifest": "samples\\eval\\rich_answer_benchmark.objecttime_source_truth.json",
    "scan": "scripts\\scan_objecttime_source_truth_corpus_coverage.py",
    "gap": "scripts\\build_objecttime_source_truth_answer_gap_report.py",
}

IMPORTS_ACTUALS_RECAPTURED_DOMAIN = {
    "name": "Imports / Actuals",
    "runbook": "docs/IMPORTS_ACTUALS_EVALUATION_RUNBOOK.md",
    "manifest": "samples\\eval\\rich_answer_benchmark.imports_actuals.json",
    "scan": "scripts\\scan_imports_actuals_corpus_coverage.py",
    "gap": "scripts\\build_imports_actuals_answer_gap_report.py",
}

TAX_PAYG_RECAPTURED_DOMAIN = {
    "name": "Tax / PAYG",
    "runbook": "docs/TAX_PAYG_EVALUATION_RUNBOOK.md",
    "manifest": "samples\\eval\\rich_answer_benchmark.tax_payg.json",
    "scan": "scripts\\scan_tax_payg_corpus_coverage.py",
    "gap": "scripts\\build_tax_payg_answer_gap_report.py",
}

COMPARISON_REMEDIATION_CAPTURED_DOMAIN = {
    "name": "Comparison / Remediation",
    "runbook": "docs/COMPARISON_REMEDIATION_EVALUATION_RUNBOOK.md",
    "manifest": "samples\\eval\\rich_answer_benchmark.comparison_remediation.json",
    "scan": "scripts\\scan_comparison_remediation_corpus_coverage.py",
    "gap": "scripts\\build_comparison_remediation_answer_gap_report.py",
}
IMPORTS_ACTUALS_FORMAL_EVIDENCE_GAP_PLAN = (
    BASELINE_ROOT / "imports_actuals" / "v0_1" / "FORMAL_EVIDENCE_GAP_PLAN.md"
)
TAX_PAYG_FORMAL_EVIDENCE_GAP_PLAN = (
    BASELINE_ROOT / "tax_payg" / "v0_1" / "FORMAL_EVIDENCE_GAP_PLAN.md"
)
IMPORTS_ACTUALS_FORMAL_SOURCE_EVIDENCE_DRAFT = (
    Path("docs/evaluation/source_evidence_drafts/imports_actuals")
    / "IMPORTS_ACTUALS_FORMAL_SOURCE_EVIDENCE_DRAFT_v0_1.md"
)
TAX_PAYG_FORMAL_SOURCE_EVIDENCE_DRAFT = (
    Path("docs/evaluation/source_evidence_drafts/tax_payg")
    / "TAX_PAYG_FORMAL_SOURCE_EVIDENCE_DRAFT_v0_1.md"
)
TAX_PAYG_FORMAL_EVIDENCE_REVIEW_GATE = (
    Path("docs/evaluation/source_evidence_drafts/tax_payg")
    / "TAX_PAYG_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md"
)
IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_GATE = (
    Path("docs/evaluation/source_evidence_drafts/imports_actuals")
    / "IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md"
)
FORMAL_EVIDENCE_REVIEW_GATE_INDEX = (
    Path("docs/evaluation/source_evidence_drafts")
    / "FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md"
)
FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE = (
    Path("docs/evaluation/source_evidence_drafts")
    / "FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md"
)
FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX = (
    Path("docs/evaluation/source_evidence_drafts")
    / "FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md"
)
FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST = (
    Path("docs/evaluation/source_evidence_drafts")
    / "FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST.md"
)
FORMAL_EVIDENCE_REVIEW_STATUS_TRANSITION_RUNBOOK = (
    Path("docs/evaluation/source_evidence_drafts")
    / "FORMAL_EVIDENCE_REVIEW_STATUS_TRANSITION_RUNBOOK.md"
)
FORMAL_EVIDENCE_GOVERNED_INGESTION_PLANNING_RUNBOOK = (
    Path("docs/evaluation/source_evidence_drafts")
    / "FORMAL_EVIDENCE_GOVERNED_INGESTION_PLANNING_RUNBOOK.md"
)
FORMAL_EVIDENCE_RECAPTURE_PLANNING_RUNBOOK = (
    Path("docs/evaluation/source_evidence_drafts")
    / "FORMAL_EVIDENCE_RECAPTURE_PLANNING_RUNBOOK.md"
)
FORMAL_EVIDENCE_PROMOTION_PLANNING_RUNBOOK = (
    Path("docs/evaluation/source_evidence_drafts")
    / "FORMAL_EVIDENCE_PROMOTION_PLANNING_RUNBOOK.md"
)
FORMAL_EVIDENCE_PROMOTION_EXECUTION_GUARDRAIL = (
    Path("docs/evaluation/source_evidence_drafts")
    / "FORMAL_EVIDENCE_PROMOTION_EXECUTION_GUARDRAIL.md"
)
FORMAL_EVIDENCE_CONTROL_INDEX = (
    Path("docs/evaluation/source_evidence_drafts")
    / "FORMAL_EVIDENCE_CONTROL_INDEX.md"
)
FORMAL_EVIDENCE_CONTROL_MODEL_CLOSEOUT = (
    Path("docs/evaluation/source_evidence_drafts")
    / "FORMAL_EVIDENCE_CONTROL_MODEL_CLOSEOUT_2026_05_15.md"
)
FORMAL_EVIDENCE_CURRENT_STATE_SUMMARY = (
    Path("docs/evaluation/source_evidence_drafts")
    / "FORMAL_EVIDENCE_CURRENT_STATE_SUMMARY_2026_05_15.md"
)
SOURCE_EVIDENCE_DRAFTS_README = Path("docs/evaluation/source_evidence_drafts/README.md")
FORMAL_EVIDENCE_CONTROL_README_PROMPT = Path(
    "docs/codex_prompts/2026-05-15_minerva_formal_evidence_control_readme_v0_1.md"
)
FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST_PROMPT = Path(
    "docs/codex_prompts/2026-05-15_minerva_formal_evidence_review_readiness_checklist_v0_1.md"
)
FORMAL_EVIDENCE_REVIEW_STATUS_TRANSITION_RUNBOOK_PROMPT = Path(
    "docs/codex_prompts/2026-05-15_minerva_formal_evidence_review_status_transition_runbook_v0_1.md"
)
FORMAL_EVIDENCE_GOVERNED_INGESTION_PLANNING_RUNBOOK_PROMPT = Path(
    "docs/codex_prompts/2026-05-15_minerva_formal_evidence_governed_ingestion_planning_runbook_v0_1.md"
)
FORMAL_EVIDENCE_RECAPTURE_PLANNING_RUNBOOK_PROMPT = Path(
    "docs/codex_prompts/2026-05-15_minerva_formal_evidence_recapture_planning_runbook_v0_1.md"
)
FORMAL_EVIDENCE_PROMOTION_PLANNING_RUNBOOK_PROMPT = Path(
    "docs/codex_prompts/2026-05-15_minerva_formal_evidence_promotion_planning_runbook_v0_1.md"
)
FORMAL_EVIDENCE_PROMOTION_EXECUTION_GUARDRAIL_PROMPT = Path(
    "docs/codex_prompts/2026-05-15_minerva_formal_evidence_promotion_execution_guardrail_v0_1.md"
)
FORMAL_EVIDENCE_CONTROL_INDEX_PROMPT = Path(
    "docs/codex_prompts/2026-05-15_minerva_formal_evidence_control_index_v0_1.md"
)
HISTORICAL_KNOWLEDGE_ROOT = Path("docs/evaluation/historical_knowledge")
HISTORICAL_KNOWLEDGE_CONTROL_INDEX = (
    HISTORICAL_KNOWLEDGE_ROOT / "HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md"
)
HISTORICAL_KNOWLEDGE_GAP_REGISTER = (
    HISTORICAL_KNOWLEDGE_ROOT / "HISTORICAL_KNOWLEDGE_GAP_REGISTER.md"
)
HISTORICAL_SOURCE_TIERING_MODEL = (
    HISTORICAL_KNOWLEDGE_ROOT / "HISTORICAL_SOURCE_TIERING_MODEL.md"
)
HISTORICAL_BACKFILL_PROCESS = (
    HISTORICAL_KNOWLEDGE_ROOT / "HISTORICAL_BACKFILL_PROCESS.md"
)
HISTORICAL_KNOWLEDGE_CONTROL_INDEX_PROMPT = Path(
    "docs/codex_prompts/2026-05-15_minerva_historical_knowledge_control_index_v0_1.md"
)
HISTORICAL_SOURCE_INVENTORY_TEMPLATE = (
    HISTORICAL_KNOWLEDGE_ROOT / "HISTORICAL_SOURCE_INVENTORY_TEMPLATE.md"
)
HISTORICAL_DEVELOPER_LOG_DOCTRINE_INVENTORY_TEMPLATE = (
    HISTORICAL_KNOWLEDGE_ROOT / "HISTORICAL_DEVELOPER_LOG_DOCTRINE_INVENTORY_TEMPLATE.md"
)
HISTORICAL_CHAT_CONTINUANCE_INVENTORY_TEMPLATE = (
    HISTORICAL_KNOWLEDGE_ROOT / "HISTORICAL_CHAT_CONTINUANCE_INVENTORY_TEMPLATE.md"
)
HISTORICAL_CODE_EVIDENCE_INVENTORY_TEMPLATE = (
    HISTORICAL_KNOWLEDGE_ROOT / "HISTORICAL_CODE_EVIDENCE_INVENTORY_TEMPLATE.md"
)
HISTORICAL_SOURCE_INVENTORY_TEMPLATE_PROMPT = Path(
    "docs/codex_prompts/2026-05-15_minerva_historical_source_inventory_template_v0_1.md"
)
FORMAL_EVIDENCE_CONTROL_INDEX_README_LINK_PROMPT = Path(
    "docs/codex_prompts/2026-05-15_minerva_formal_evidence_control_index_readme_link_v0_1.md"
)
FORMAL_EVIDENCE_CONTROL_INDEX_ROOT_README_LINK_PROMPT = Path(
    "docs/codex_prompts/2026-05-15_minerva_formal_evidence_control_index_root_readme_link_v0_1.md"
)
FORMAL_EVIDENCE_CONTROL_MODEL_CLOSEOUT_PROMPT = Path(
    "docs/codex_prompts/2026-05-15_minerva_formal_evidence_control_model_closeout_v0_1.md"
)
FORMAL_EVIDENCE_CURRENT_STATE_SUMMARY_PROMPT = Path(
    "docs/codex_prompts/2026-05-15_minerva_formal_evidence_current_state_summary_v0_1.md"
)
TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED = (
    Path("docs/evaluation/source_evidence_drafts/tax_payg")
    / "TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md"
)
IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED = (
    Path("docs/evaluation/source_evidence_drafts/imports_actuals")
    / "IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md"
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_batch_baseline_packs_exist_with_required_files():
    for slug in CAPTURED_BATCH_DOMAINS:
        pack_path = BASELINE_ROOT / slug / "v0_1"
        assert pack_path.exists()
        for file_name in REQUIRED_FILES:
            assert (pack_path / file_name).exists()


def test_four_domain_batch_closeout_exists_and_is_linked_from_readme():
    assert CLOSEOUT_PATH.exists()

    readme = _read(Path("README.md"))

    assert "docs/evaluation/worker_story_baselines/BASELINE_BATCH_CLOSEOUT_2026_05_13.md" in readme


def test_six_domain_maturity_closeout_exists_and_is_linked_from_readme():
    assert MATURITY_CLOSEOUT_PATH.exists()

    readme = _read(Path("README.md"))

    assert "docs/evaluation/worker_story_baselines/BASELINE_MATURITY_CLOSEOUT_2026_05_13.md" in readme


def test_six_domain_maturity_closeout_records_packs_and_final_ledger_counts():
    closeout = _read(MATURITY_CLOSEOUT_PATH)

    assert "`BASELINE_REQUIRED`: 25" in closeout
    assert "`BASELINE_ALREADY_EXISTS`: 6" in closeout
    assert "`RUNBOOK_OUTSTANDING`: 0" in closeout
    assert "Domains with runbook outstanding: none" in closeout
    assert "Annual Leave / Leave Management is no longer `RUNBOOK_OUTSTANDING`; it is now `BASELINE_ALREADY_EXISTS`" in closeout

    for pack_name in (
        "worker_story/v0_1/",
        "payroll_bases_totals/v0_1/",
        "payrun_admin_queue/v0_1/",
        "movement_review/v0_1/",
        "gross_to_net/v0_1/",
        "annual_leave/v0_1/",
    ):
        assert f"docs/evaluation/worker_story_baselines/{pack_name}" in closeout


def test_core_payroll_explanation_blocked_closeout_exists_and_is_linked_from_readme():
    assert CORE_PAYROLL_BLOCKED_CLOSEOUT_PATH.exists()

    readme = _read(Path("README.md"))

    assert "docs/evaluation/worker_story_baselines/CORE_PAYROLL_EXPLANATION_BASELINE_BATCH_2026_05_13.md" in readme


def test_core_payroll_explanation_batch_closeout_exists_and_is_linked_from_readme():
    assert CORE_PAYROLL_CLOSEOUT_PATH.exists()

    readme = _read(Path("README.md"))

    assert "docs/evaluation/worker_story_baselines/CORE_PAYROLL_EXPLANATION_BATCH_CLOSEOUT_2026_05_13.md" in readme


def test_payroll_evidence_context_blocked_closeout_exists_and_is_linked_from_readme():
    assert PAYROLL_EVIDENCE_CONTEXT_BLOCKED_CLOSEOUT_PATH.exists()

    readme = _read(Path("README.md"))

    assert "docs/evaluation/worker_story_baselines/PAYROLL_EVIDENCE_CONTEXT_BASELINE_BATCH_2026_05_13.md" in readme


def test_decision_story_baseline_pack_exists_with_required_files():
    pack_path = BASELINE_ROOT / "decision_story" / "v0_1"
    assert pack_path.exists()
    for file_name in REQUIRED_FILES:
        assert (pack_path / file_name).exists()


def test_finalisation_readiness_baseline_pack_exists_with_required_files():
    pack_path = BASELINE_ROOT / "finalisation_readiness" / "v0_1"
    assert pack_path.exists()
    for file_name in REQUIRED_FILES:
        assert (pack_path / file_name).exists()


def test_payroll_output_baseline_pack_exists_with_required_files():
    pack_path = BASELINE_ROOT / "payroll_output" / "v0_1"
    assert pack_path.exists()
    for file_name in REQUIRED_FILES:
        assert (pack_path / file_name).exists()


def test_rate_source_rate_story_baseline_pack_exists_with_required_files():
    pack_path = BASELINE_ROOT / "ratesource_rate_story" / "v0_1"
    assert pack_path.exists()
    for file_name in REQUIRED_FILES:
        assert (pack_path / file_name).exists()


def test_payroll_evidence_context_blocked_packs_exist_with_required_files():
    for slug in PAYROLL_EVIDENCE_CONTEXT_BLOCKED_DOMAINS:
        pack_path = BASELINE_ROOT / slug / "v0_1"
        assert pack_path.exists()
        for file_name in REQUIRED_FILES:
            assert (pack_path / file_name).exists()


def test_contact_payroll_history_baseline_pack_exists_with_required_files():
    pack_path = BASELINE_ROOT / "contact_payroll_history" / "v0_1"
    assert pack_path.exists()
    for file_name in REQUIRED_FILES:
        assert (pack_path / file_name).exists()


def test_core_payroll_explanation_blocked_closeout_records_honest_statuses():
    closeout = _read(CORE_PAYROLL_BLOCKED_CLOSEOUT_PATH)

    assert "`BASELINE_REQUIRED`: 25" in closeout
    assert "`BASELINE_ALREADY_EXISTS`: 6" in closeout
    assert "`RUNBOOK_OUTSTANDING`: 0" in closeout
    assert "Readiness status: `DATABASE_CONNECTION_FAILED`" in closeout
    assert "Because readiness was not `READY`, benchmark, corpus coverage and answer gap commands were not run" in closeout
    assert "No other baseline-required domains were attempted" in closeout
    assert "No benchmark, corpus coverage or answer gap JSON reports were generated for this batch" in closeout

    for domain in ("Finalisation Readiness", "Payroll Output", "RateSource / Rate Story", "Decision Story"):
        assert f"| {domain} | `DATABASE_CONNECTION_FAILED` | blocked pack only | not run | not run | not run | `BASELINE_REQUIRED` |" in closeout


def test_payroll_evidence_context_blocked_closeout_records_honest_statuses():
    closeout = _read(PAYROLL_EVIDENCE_CONTEXT_BLOCKED_CLOSEOUT_PATH)

    assert "`BASELINE_REQUIRED`: 21" in closeout
    assert "`BASELINE_ALREADY_EXISTS`: 10" in closeout
    assert "`RUNBOOK_OUTSTANDING`: 0" in closeout
    assert "Readiness status: `DATABASE_CONNECTION_FAILED`" in closeout
    assert "Because readiness was not `READY`, benchmark, corpus coverage and answer gap commands were not run" in closeout
    assert "No other baseline-required domains were attempted" in closeout
    assert "No benchmark, corpus coverage or answer gap JSON reports were generated for this batch" in closeout

    for domain in (
        "Contact Payroll History",
        "ObjectTime / Source Truth",
        "Process Periods / PayRun Lifecycle",
        "Imports / Actuals",
    ):
        assert f"| {domain} | `DATABASE_CONNECTION_FAILED` | blocked pack only | not run | not run | not run | `BASELINE_REQUIRED` |" in closeout


def test_core_payroll_explanation_batch_closeout_records_ledger_and_packs():
    closeout = _read(CORE_PAYROLL_CLOSEOUT_PATH)

    assert "`BASELINE_REQUIRED`: 21" in closeout
    assert "`BASELINE_ALREADY_EXISTS`: 10" in closeout
    assert "`RUNBOOK_OUTSTANDING`: 0" in closeout
    assert "No Core Payroll Explanation batch domains remain blocked" in closeout

    for pack_name in (
        "finalisation_readiness/v0_1/",
        "payroll_output/v0_1/",
        "ratesource_rate_story/v0_1/",
        "decision_story/v0_1/",
    ):
        assert f"docs/evaluation/worker_story_baselines/{pack_name}" in closeout


def test_core_payroll_explanation_batch_closeout_records_outcomes_without_changing_numbers():
    closeout = _read(CORE_PAYROLL_CLOSEOUT_PATH)

    assert "| Finalisation Readiness | Passed baseline with refinement | 12 total / 12 passed / 0 failed | STRONG=11, WEAK=1, MISSING=0 | NEEDS_REFINEMENT; 11 KEEP actions; 1 IMPROVE_SYNTHESIS action |" in closeout
    assert "| Payroll Output | Captured-with-failures baseline | 7 total / 6 passed / 1 failed | STRONG=10, WEAK=1, MISSING=0 | NEEDS_REFINEMENT; 10 KEEP actions; 1 IMPROVE_SYNTHESIS action |" in closeout
    assert "| RateSource / Rate Story | Captured-with-failures baseline | 6 total / 5 passed / 1 failed | STRONG=10, WEAK=1, MISSING=0 | NEEDS_REFINEMENT; 10 KEEP actions; 1 IMPROVE_SYNTHESIS action |" in closeout
    assert "| Decision Story | Captured-with-failures baseline | 7 total / 6 passed / 1 failed | STRONG=10, WEAK=0, MISSING=0 | GOOD; 10 KEEP actions |" in closeout
    assert "Passed baselines and captured-with-failures baselines are both durable comparison controls, but they are different signals" in closeout


def test_core_payroll_explanation_batch_closeout_records_failure_and_refinement_classifications():
    closeout = _read(CORE_PAYROLL_CLOSEOUT_PATH)

    assert "payroll-output-rich-answer" in closeout
    assert "rate-source-rate-story-rich-answer" in closeout
    assert "decision-story-rich-answer" in closeout
    assert "Payroll Output failure is not corpus gap" in closeout
    assert "RateSource / Rate Story failure is not corpus gap" in closeout
    assert "Decision Story failure is not corpus gap" in closeout
    assert "benchmark/source-evidence check or retrieval/source-matched-phrase drift, not corpus gap" in closeout
    assert "Finalisation Readiness needs synthesis refinement for `purpose_and_operator_meaning`" in closeout
    assert "Payroll Output needs synthesis refinement for `worker_level_output`" in closeout
    assert "RateSource / Rate Story needs synthesis refinement for `rate_source_evidence_index`" in closeout


def test_core_payroll_explanation_batch_closeout_records_transient_json_policy_and_guardrails():
    closeout = _read(CORE_PAYROLL_CLOSEOUT_PATH)

    assert "Generated JSON outputs from benchmark, corpus coverage or answer-gap commands are transient evaluation materials" in closeout
    assert "not durable checked-in artefacts unless explicitly versioned" in closeout
    assert "operational JSON ingestion" in closeout
    assert "Code Evidence answer integration" in closeout
    assert "live LLM calls" in closeout
    assert "corpus mutation" in closeout
    assert "DB or schema migration" in closeout
    assert "endpoints or UI" in closeout
    assert "workforce-platform changes" in closeout
    assert "No operational JSON ingestion occurred" in closeout
    assert "No Code Evidence answer integration occurred" in closeout
    assert "No live LLM call occurred" in closeout
    assert "No corpus mutation occurred" in closeout
    assert "No DB or schema migration occurred" in closeout
    assert "No endpoint or UI change occurred" in closeout
    assert "No workforce-platform change occurred" in closeout
    assert "should be small" in closeout
    assert "not attempt all remaining 21 `BASELINE_REQUIRED` domains at once" in closeout


def test_payroll_evidence_context_blocked_packs_record_non_execution_honestly():
    for slug, metadata in PAYROLL_EVIDENCE_CONTEXT_BLOCKED_DOMAINS.items():
        pack_path = BASELINE_ROOT / slug / "v0_1"
        combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

        assert metadata["name"] in combined
        assert metadata["runbook"] in combined
        assert metadata["manifest"] in combined
        assert metadata["scan"] in combined
        assert metadata["gap"] in combined
        assert "DB readiness returned `DATABASE_CONNECTION_FAILED`" in combined
        assert "Result status: `BLOCKED_DATABASE_CONNECTION`" in combined
        assert "Baseline pack created: blocked pack only" in combined
        assert "Benchmark result: not run" in combined
        assert "Corpus coverage result: not run" in combined
        assert "Answer gap report: not run" in combined
        assert "Total: not run" in combined
        assert "`STRONG`: not evaluated" in combined
        assert "Overall status: not evaluated" in combined
        assert "Generated artefact committed: no" in combined
        assert "Final ledger status remains `BASELINE_REQUIRED`" in combined
        assert "does not count as `BASELINE_ALREADY_EXISTS`" in combined
        assert "Code Evidence answer integration: no" in combined
        assert "READY` before running commands" in combined
        assert "Result status: `COMPLETED`" not in combined
        assert "Result status: `COMPLETED_WITH_FAILURES`" not in combined


def test_process_periods_payrun_lifecycle_pack_records_promoted_state():
    metadata = PROCESS_PERIODS_PAYRUN_LIFECYCLE_RECAPTURED_DOMAIN
    pack_path = BASELINE_ROOT / "process_periods_payrun_lifecycle" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    assert metadata["name"] in combined
    assert metadata["runbook"] in combined
    assert metadata["manifest"] in combined
    assert metadata["scan"] in combined
    assert metadata["gap"] in combined
    assert "Readiness status: `READY`" in combined
    assert "Result status: `PROMOTED_BASELINE_CAPTURED`" in combined
    assert "Result status: `COMPLETED`" in combined
    assert "Total: 13" in combined
    assert "Passed: 13" in combined
    assert "Failed: 0" in combined
    assert "Audit/chat rows created: false" in combined
    assert "Evidence groups: 13" in combined
    assert "`STRONG`: 13" in combined
    assert "`WEAK`: 0" in combined
    assert "`MISSING`: 0" in combined
    assert "Indexed corpus: 5 active documents, 4583 chunks" in combined
    assert "Overall status: `GOOD`" in combined
    assert "`LOW` / `KEEP` groups: 13" in combined
    assert "`MEDIUM` refinement groups: 0" in combined
    assert "`purpose_and_operator_meaning`: STRONG -> `KEEP`" in combined
    assert "`close_rolls_forward`: STRONG -> `KEEP`" in combined
    assert "`outstanding_hardening`: STRONG -> `KEEP`" in combined
    assert "Baseline pack state: captured evidence and promoted" in combined
    assert "Final ledger status is `BASELINE_ALREADY_EXISTS`" in combined
    assert "not corpus absence issues" in combined
    assert "Generated artefact committed: no" in combined
    assert "Code Evidence answer integration: no" in combined
    assert "DB readiness returned `DATABASE_CONNECTION_FAILED`" not in combined
    assert "Result status: `BLOCKED_DATABASE_CONNECTION`" not in combined
    assert "Benchmark result: not run" not in combined


def test_payroll_evidence_context_blocked_packs_are_diagnostic_only_not_runtime_truth():
    for slug in PAYROLL_EVIDENCE_CONTEXT_BLOCKED_DOMAINS:
        pack_path = BASELINE_ROOT / slug / "v0_1"
        combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

        assert "diagnostic-only" in combined
        assert "not operational truth" in combined
        assert "does not mutate corpus" in combined
        assert "does not change routing" in combined
        assert "does not change answer generation" in combined
        assert "does not call live LLM" in combined
        assert "does not ingest operational JSON" in combined
        assert "does not connect Code Evidence" in combined
        assert "does not create DB schema or migrations" in combined
        assert "does not add endpoints or UI" in combined
        assert "does not change workforce-platform" in combined


def test_imports_actuals_recaptured_pack_records_unpromoted_refinement_state():
    metadata = IMPORTS_ACTUALS_RECAPTURED_DOMAIN
    pack_path = BASELINE_ROOT / "imports_actuals" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    assert metadata["name"] in combined
    assert metadata["runbook"] in combined
    assert metadata["manifest"] in combined
    assert metadata["scan"] in combined
    assert metadata["gap"] in combined
    assert "DB readiness result: `READY`" in combined
    assert "Result status: `RECAPTURED_BASELINE_REQUIRES_REFINEMENT`" in combined
    assert "Result status: `COMPLETED_WITH_FAILURES`" in combined
    assert "Total: 11" in combined
    assert "Passed: 8" in combined
    assert "Failed: 3" in combined
    assert "Audit/chat rows created: false" in combined
    assert "imports-actuals-pay-code-ratetype-mapping" in combined
    assert "imports-actuals-comparison-remediation-connection" in combined
    assert "imports-actuals-worker-story-admin-queue" in combined
    assert "Evidence groups: 12" in combined
    assert "`STRONG`: 9" in combined
    assert "`WEAK`: 1" in combined
    assert "`MISSING`: 2" in combined
    assert "`purpose_and_operator_meaning`: MISSING" in combined
    assert "`pay_code_and_rate_type_mapping`: WEAK" in combined
    assert "`outstanding_hardening`: MISSING" in combined
    assert "Indexed corpus: 5 active documents, 4583 chunks" in combined
    assert "Overall status: `NEEDS_REFINEMENT`" in combined
    assert "`LOW` / `KEEP` groups: 9" in combined
    assert "`MEDIUM` / `IMPROVE_SYNTHESIS` groups: 1" in combined
    assert "`ADD_FORMAL_SOURCE_EVIDENCE_LATER` groups: 2" in combined
    assert "This is not a successful captured/promoted baseline" in combined
    assert "Final ledger status remains `BASELINE_REQUIRED`" in combined
    assert "does not count as `BASELINE_ALREADY_EXISTS`" in combined
    assert "real formal-corpus gaps" in combined
    assert "Promotion cannot happen solely through synthesis hardening" in combined
    assert "Generated artefact committed: no" in combined
    assert "Code Evidence answer integration: no" in combined
    assert "DB readiness returned `DATABASE_CONNECTION_FAILED`" not in combined
    assert "Result status: `BLOCKED_DATABASE_CONNECTION`" not in combined
    assert "Benchmark result: not run" not in combined
    assert "Baseline pack created: blocked pack only" not in combined
    assert "Final ledger status is `BASELINE_ALREADY_EXISTS`" not in combined


def test_tax_payg_recaptured_pack_records_unpromoted_refinement_state():
    metadata = TAX_PAYG_RECAPTURED_DOMAIN
    pack_path = BASELINE_ROOT / "tax_payg" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    assert metadata["name"] in combined
    assert metadata["runbook"] in combined
    assert metadata["manifest"] in combined
    assert metadata["scan"] in combined
    assert metadata["gap"] in combined
    assert "DB readiness result: `READY`" in combined
    assert "Result status: `RECAPTURED_BASELINE_REQUIRES_REFINEMENT`" in combined
    assert "Result status: `COMPLETED_WITH_FAILURES`" in combined
    assert "Total: 9" in combined
    assert "Passed: 7" in combined
    assert "Failed: 2" in combined
    assert "Audit/chat rows created: false" in combined
    assert "tax-payg-rich-answer" in combined
    assert "tax-payg-minerva-not-calculate" in combined
    assert "Evidence groups: 12" in combined
    assert "`STRONG`: 10" in combined
    assert "`WEAK`: 1" in combined
    assert "`MISSING`: 1" in combined
    assert "`purpose_and_operator_meaning`: MISSING" in combined
    assert "`outstanding_hardening`: WEAK" in combined
    assert "Indexed corpus: 5 active documents, 4583 chunks" in combined
    assert "Overall status: `NEEDS_REFINEMENT`" in combined
    assert "`LOW` / `KEEP` groups: 10" in combined
    assert "`HIGH` / `ADD_FORMAL_SOURCE_EVIDENCE_LATER` groups: 1" in combined
    assert "`MEDIUM` / `IMPROVE_RETRIEVAL_TERMS` groups: 1" in combined
    assert "This is not a successful captured/promoted baseline" in combined
    assert "It is not DB-blocked" in combined
    assert "Final ledger status remains `BASELINE_REQUIRED`" in combined
    assert "does not count as `BASELINE_ALREADY_EXISTS`" in combined
    assert "real formal source-evidence gap" in combined
    assert "Promotion cannot happen solely through synthesis hardening" in combined
    assert "Minerva must explain Tax / PAYG but must not calculate PAYG withholding" in combined
    assert "Deterministic services and tax providers own withholding calculation" in combined
    assert "Tax/PAYG rates, thresholds, bands, offsets and formulas must be governed data/rule-pack/configuration" in combined
    assert "PaymentDate and payroll context matter for Tax / PAYG selection" in combined
    assert "no tax runtime changes" in combined
    assert "no PAYG runtime changes" in combined
    assert "no ledger promotion" in combined
    assert "Generated artefact committed: no" in combined
    assert "Code Evidence answer integration: no" in combined
    assert "DB readiness returned `DATABASE_CONNECTION_FAILED`" not in combined
    assert "Result status: `BLOCKED_DATABASE_CONNECTION`" not in combined
    assert "Benchmark result: not run" not in combined
    assert "Baseline pack created: blocked pack only" not in combined
    assert "Final ledger status is `BASELINE_ALREADY_EXISTS`" not in combined


def test_tax_payg_formal_evidence_gap_plan_records_required_gaps_and_guardrails():
    assert TAX_PAYG_FORMAL_EVIDENCE_GAP_PLAN.exists()

    plan = _read(TAX_PAYG_FORMAL_EVIDENCE_GAP_PLAN)

    assert "Tax / PAYG remains `BASELINE_REQUIRED`" in plan
    assert "cannot be promoted solely through answer-synthesis hardening" in plan
    assert "DB readiness was not the blocker" in plan
    assert "Benchmark: 9 total / 7 passed / 2 failed" in plan
    assert "STRONG=10, WEAK=1, MISSING=1" in plan
    assert "Answer gap: `NEEDS_REFINEMENT`" in plan
    assert "10 KEEP, 1 ADD_FORMAL_SOURCE_EVIDENCE_LATER, 1 IMPROVE_RETRIEVAL_TERMS" in plan
    assert "`purpose_and_operator_meaning`" in plan
    assert "`outstanding_hardening`" in plan
    assert "Missing formal source evidence group" in plan
    assert "Weak formal source evidence group" in plan
    assert "Minerva explains Tax / PAYG but does not calculate PAYG withholding" in plan
    assert "Formal source evidence is added to the corpus through the governed ingestion process" in plan
    assert "Coverage improves to no MISSING groups" in plan
    assert "`outstanding_hardening` becomes STRONG or is otherwise accepted with documented rationale" in plan
    assert "Benchmark passes 9/9" in plan
    assert "Answer gap becomes GOOD or acceptable" in plan
    assert "Ledger is promoted only after real command results support it" in plan
    assert "no corpus mutation" in plan
    assert "no operational JSON ingestion" in plan
    assert "no Code Evidence answer integration" in plan
    assert "no ledger promotion" in plan


def test_objecttime_source_truth_recaptured_pack_records_promoted_state():
    metadata = OBJECTTIME_SOURCE_TRUTH_RECAPTURED_DOMAIN
    pack_path = BASELINE_ROOT / "objecttime_source_truth" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    assert metadata["name"] in combined
    assert metadata["runbook"] in combined
    assert metadata["manifest"] in combined
    assert metadata["scan"] in combined
    assert metadata["gap"] in combined
    assert "DB readiness returned `READY`" in combined
    assert "Ready: yes" in combined
    assert "Selected ODBC driver: `ODBC Driver 17 for SQL Server`" in combined
    assert "Result status: `PROMOTED_BASELINE_CAPTURED`" in combined
    assert "captured evidence and promoted" in combined
    assert "Total: 12" in combined
    assert "Passed: 12" in combined
    assert "Failed: 0" in combined
    assert "Audit/chat rows created: false" in combined
    assert "`STRONG`: 12" in combined
    assert "`WEAK`: 0" in combined
    assert "`MISSING`: 0" in combined
    assert "Overall status: `GOOD`" in combined
    assert "`KEEP`: 12" in combined
    assert "`IMPROVE_RETRIEVAL_TERMS`: 0" in combined
    assert "`outstanding_hardening` -> `KEEP`" in combined
    assert "previous promotion blocker is resolved without adding corpus" in combined
    assert "Final ledger status is `BASELINE_ALREADY_EXISTS`" in combined
    assert "Generated artefact committed: no" in combined
    assert "Code Evidence answer integration: no" in combined
    assert "DB readiness returned `DATABASE_CONNECTION_FAILED`" not in combined
    assert "Result status: `BLOCKED_DATABASE_CONNECTION`" not in combined
    assert "Benchmark result: not run" not in combined
    assert "objecttime-payrun-inclusion" not in combined
    assert "objecttime-sourcetruth-vs-workedhours" not in combined
    assert "objecttime-current-effective-output" not in combined
    assert "objecttime-worker-story-source-truth" not in combined


def test_comparison_remediation_pack_records_promoted_state():
    metadata = COMPARISON_REMEDIATION_CAPTURED_DOMAIN
    pack_path = BASELINE_ROOT / "comparison_remediation" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    assert metadata["name"] in combined
    assert metadata["runbook"] in combined
    assert metadata["manifest"] in combined
    assert metadata["scan"] in combined
    assert metadata["gap"] in combined
    assert "DB readiness returned `READY`" in combined
    assert "Ready: yes" in combined
    assert "Selected ODBC driver: `ODBC Driver 17 for SQL Server`" in combined
    assert "Result status: `PROMOTED_BASELINE_CAPTURED`" in combined
    assert "captured evidence and promoted" in combined
    assert "Total: 9" in combined
    assert "Passed: 9" in combined
    assert "Failed: 0" in combined
    assert "Audit/chat rows created: false" in combined
    assert "Evidence groups: 12" in combined
    assert "`STRONG`: 12" in combined
    assert "`WEAK`: 0" in combined
    assert "`MISSING`: 0" in combined
    assert "Indexed corpus: 5 active documents, 4583 chunks" in combined
    assert "Overall status: `GOOD`" in combined
    assert "`LOW` / `KEEP` groups: 12" in combined
    assert "`MEDIUM` refinement groups: 0" in combined
    assert "`three_lane_comparison_model`: STRONG -> `KEEP`" in combined
    assert "`actuals_as_external_outcome_truth`: STRONG -> `KEEP`" in combined
    assert "`outstanding_hardening`: STRONG -> `KEEP`" in combined
    assert "Final ledger status is `BASELINE_ALREADY_EXISTS`" in combined
    assert "Generated artefact committed: no" in combined
    assert "Code Evidence answer integration: no" in combined
    assert "DB readiness returned `DATABASE_CONNECTION_FAILED`" not in combined
    assert "Result status: `BLOCKED_DATABASE_CONNECTION`" not in combined
    assert "Benchmark result: not run" not in combined


def test_comparison_remediation_pack_preserves_domain_boundaries():
    pack_path = BASELINE_ROOT / "comparison_remediation" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    for term in (
        "payroll evidence and review/remediation context, not generic diffing",
        "primary calculated",
        "comparator calculated",
        "actual imported / actuals lane",
        "primary award path remains operational payroll truth",
        "Imported actuals are external outcome truth",
        "comparison policy",
        "comparator selection",
        "active lanes",
        "offset policy",
        "output mode",
        "variance treatment",
        "review requirements",
        "Comparison run and line evidence",
        "Variance/top-up is a governed consequence",
        "Position/classification mapping",
        "Worker Story, Admin Queue, and Movement Review consume comparison evidence",
        "Baseline capture does not implement runtime comparison/remediation behaviour",
    ):
        assert term in combined


def test_objecttime_source_truth_recaptured_pack_preserves_domain_boundaries():
    pack_path = BASELINE_ROOT / "objecttime_source_truth" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    for term in (
        "ObjectTimeAttribute",
        "ObjectTimeAssessment",
        "ObjectTimeAssessmentResponse",
        "SourceTruth is not WorkedHours",
        "Raw span hours are not user-facing payroll worked hours",
        "RoundedStart boundary for WORK ObjectTime",
        "changed-field detection",
        "previous value capture",
        "new value capture",
        "Finalised or protected dirty exclusion",
        "finalised correction review pathway",
        "EnableFinalisedCorrectionObjectTimeHookDryRun",
        "FinalisedCorrectionObjectTimeHookDryRunPreview",
        "DRY_RUN_PREVIEW_ERROR",
        "runtime intake readiness versus runtime intake implementation",
        "no mutation guarantee",
        "no dirty runtime call guarantee",
        "no review request creation guarantee",
    ):
        assert term in combined

    assert "Do not overclaim v5.56" in combined
    assert "It is not runtime intake" in combined
    assert "runtime source-change hook or intake" in combined
    assert "correction execution" in combined
    assert "payment or remittance execution" in combined
    assert "finalisation mutation" in combined


def test_process_periods_payrun_lifecycle_pack_preserves_domain_boundaries():
    pack_path = BASELINE_ROOT / "process_periods_payrun_lifecycle" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    for term in (
        "not merely a date range or run list domain",
        "ProcessPeriod",
        "ProcessPeriodGroup",
        "PaymentDate",
        "PayRunContact",
        "Worker Story",
        "PayRun Admin Queue",
        "Movement Review",
        "`PaymentDate` belongs on `ProcessPeriod`",
        "payment-date derivation policy belongs on `ProcessPeriodGroup`",
        "admission is not processing",
        "closed dominates open",
        "current-effective payroll output",
    ):
        assert term in combined


def test_imports_actuals_recaptured_pack_preserves_domain_boundaries():
    pack_path = BASELINE_ROOT / "imports_actuals" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    for term in (
        "not merely file upload or CSV parsing",
        "import batch",
        "import row",
        "import validation",
        "import error",
        "import warning",
        "award-specific CSV template",
        "timesheet import",
        "payroll actuals import",
        "external actuals",
        "calculated versus actual",
        "reconciliation",
        "variance",
        "pay code mapping",
        "RateType mapping",
        "tenant override mapping",
        "mapping snapshot",
        "shift assessment import",
        "shift attribute import",
        "claim import",
        "Claimable",
        "Claimable Hourly",
        "Claim Amount",
        "piece work / expense / mileage amount import context",
        "source truth provenance",
        "evidence preservation",
        "worker story explanation context",
        "source truth impact on PayRun outcomes",
        "no runtime mutation guarantee",
        "no promotion while benchmark failures and formal corpus gaps remain",
        "Imported actuals are evidence for reconciliation",
        "not the same as calculated payroll truth",
        "Minerva baseline packs do not mutate operational payroll data",
    ):
        assert term in combined


def test_imports_actuals_formal_evidence_gap_plan_records_required_gaps_and_guardrails():
    assert IMPORTS_ACTUALS_FORMAL_EVIDENCE_GAP_PLAN.exists()

    plan = _read(IMPORTS_ACTUALS_FORMAL_EVIDENCE_GAP_PLAN)

    assert "Imports / Actuals remains `BASELINE_REQUIRED`" in plan
    assert "cannot be promoted solely through answer-synthesis hardening" in plan
    assert "DB readiness was not the blocker" in plan
    assert "Benchmark: 11 total / 8 passed / 3 failed" in plan
    assert "STRONG=9, WEAK=1, MISSING=2" in plan
    assert "Answer gap: `NEEDS_REFINEMENT`" in plan
    assert "9 KEEP, 1 IMPROVE_SYNTHESIS, 2 ADD_FORMAL_SOURCE_EVIDENCE_LATER" in plan
    assert "`purpose_and_operator_meaning`" in plan
    assert "`outstanding_hardening`" in plan
    assert "`pay_code_and_rate_type_mapping`" in plan
    assert "Missing formal source evidence groups" in plan
    assert "Weak formal source evidence group" in plan
    assert "Formal source evidence is added to the corpus through the governed ingestion process" in plan
    assert "Coverage improves to no MISSING groups" in plan
    assert "Benchmark passes 11/11" in plan
    assert "Answer gap becomes GOOD or acceptable" in plan
    assert "Ledger is promoted only after real command results support it" in plan
    assert "no corpus mutation" in plan
    assert "no operational JSON ingestion" in plan
    assert "no Code Evidence answer integration" in plan
    assert "no ledger promotion" in plan


def test_imports_actuals_formal_source_evidence_draft_records_required_evidence_and_guardrails():
    assert IMPORTS_ACTUALS_FORMAL_SOURCE_EVIDENCE_DRAFT.exists()

    draft = _read(IMPORTS_ACTUALS_FORMAL_SOURCE_EVIDENCE_DRAFT)

    assert "not merely file upload or CSV parsing" in draft
    assert "not calculated payroll truth" in draft
    assert "`purpose_and_operator_meaning`: MISSING" in draft
    assert "`outstanding_hardening`: MISSING" in draft
    assert "`pay_code_and_rate_type_mapping`: WEAK" in draft
    assert "pay code mapping" in draft
    assert "RateType mapping" in draft
    assert "imported actuals lane" in draft
    assert "primary calculated lane" in draft
    assert "comparator calculated lane" in draft
    assert "actuals lane" in draft
    assert "variance" in draft
    assert "Worker Story" in draft
    assert "Admin Queue" in draft
    assert "Mapping issues must be visible as reviewable issues" in draft
    assert "no operational JSON ingestion" in draft
    assert "no Code Evidence answer integration" in draft
    assert "no corpus mutation in this slice" in draft
    assert "no ledger promotion in this slice" in draft
    assert "Future Corpus-Ingestion Acceptance Criteria" in draft
    assert "Coverage rerun shows no MISSING groups" in draft
    assert "Benchmark passes 11/11" in draft
    assert "Ledger promotion happens only after real command results support promotion" in draft
    assert "Imports / Actuals is not promoted" in draft


def test_tax_payg_formal_source_evidence_draft_records_required_evidence_and_guardrails():
    assert TAX_PAYG_FORMAL_SOURCE_EVIDENCE_DRAFT.exists()

    draft = _read(TAX_PAYG_FORMAL_SOURCE_EVIDENCE_DRAFT)

    assert "not a generic calculator" in draft
    assert "Minerva explains Tax / PAYG but does not calculate PAYG withholding" in draft
    assert "`purpose_and_operator_meaning`: MISSING" in draft
    assert "`outstanding_hardening`: WEAK" in draft
    assert "governed withholding calculation evidence" in draft
    assert "deterministic services" in draft
    assert "tax providers" in draft
    assert "TaxStory" in draft
    assert "worker tax profile" in draft
    assert "ProcessPeriod PaymentDate" in draft
    assert "pay frequency" in draft
    assert "taxable basis" in draft
    assert "Payroll Bases & Totals" in draft
    assert "finalised totals" in draft
    assert "supplementary incremental PAYG" in draft
    assert "same-period taxable earnings" in draft
    assert "prior PAYG withheld" in draft
    assert "Worker Story" in draft
    assert "Admin Queue" in draft
    assert "no operational JSON ingestion" in draft
    assert "no Code Evidence answer integration" in draft
    assert "no corpus mutation in this slice" in draft
    assert "no ledger promotion in this slice" in draft
    assert "Future Corpus-Ingestion Acceptance Criteria" in draft
    assert "Coverage rerun shows no MISSING groups" in draft
    assert "`outstanding_hardening` becomes STRONG or is documented accepted" in draft
    assert "Benchmark passes 9/9" in draft
    assert "Answer gap becomes GOOD or acceptable" in draft
    assert "Ledger is promoted only after real command results support promotion" in draft
    assert "Tax / PAYG is not promoted" in draft


def test_imports_actuals_formal_evidence_review_gate_blocks_ingestion_until_ready():
    assert IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_GATE.exists()

    gate = _read(IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_GATE)

    assert "Current review status: `NOT_REVIEWED`" in gate
    assert "Default review status: `NOT_REVIEWED`" in gate
    assert "`REVIEWED_READY_FOR_INGESTION`" in gate
    assert "Current review status: `REVIEWED_READY_FOR_INGESTION`" not in gate
    assert "FORMAL_EVIDENCE_GAP_PLAN.md" in gate
    assert "IMPORTS_ACTUALS_FORMAL_SOURCE_EVIDENCE_DRAFT_v0_1.md" in gate
    assert "`purpose_and_operator_meaning`" in gate
    assert "`outstanding_hardening`" in gate
    assert "`pay_code_and_rate_type_mapping`" in gate
    assert "no corpus mutation" in gate
    assert "no operational JSON ingestion" in gate
    assert "no Code Evidence answer integration" in gate
    assert "no ledger promotion" in gate
    assert "future explicit ingestion slice after review readiness" in gate


def test_tax_payg_formal_evidence_review_gate_blocks_ingestion_until_ready():
    assert TAX_PAYG_FORMAL_EVIDENCE_REVIEW_GATE.exists()

    gate = _read(TAX_PAYG_FORMAL_EVIDENCE_REVIEW_GATE)

    assert "Review gate version: v0.1" in gate
    assert "Current review status: `NOT_REVIEWED`" in gate
    assert "Default review status: `NOT_REVIEWED`" in gate
    assert "`NOT_REVIEWED`" in gate
    assert "`NEEDS_REVISION`" in gate
    assert "`REVIEWED_READY_FOR_INGESTION`" in gate
    assert "`SUPERSEDED`" in gate
    assert "Current review status: `REVIEWED_READY_FOR_INGESTION`" not in gate
    assert "FORMAL_EVIDENCE_GAP_PLAN.md" in gate
    assert "TAX_PAYG_FORMAL_SOURCE_EVIDENCE_DRAFT_v0_1.md" in gate
    assert "governed corpus ingestion is blocked" in gate
    assert "Governed ingestion must not happen until this review gate is marked `REVIEWED_READY_FOR_INGESTION`" in gate
    assert "Status is `REVIEWED_READY_FOR_INGESTION`" in gate
    assert "Tax / PAYG remains `BASELINE_REQUIRED`" in gate
    assert "The formal source-evidence draft is not enough by itself to permit ingestion" in gate
    assert "Minerva must not calculate PAYG withholding" in gate
    assert "control artefact, not a runtime feature" in gate
    assert "`purpose_and_operator_meaning`" in gate
    assert "`outstanding_hardening`" in gate
    assert "no corpus mutation" in gate
    assert "no operational JSON ingestion" in gate
    assert "no Code Evidence answer integration" in gate
    assert "no benchmark recapture" in gate
    assert "no baseline promotion" in gate
    assert "no ledger promotion" in gate
    assert "benchmark promotion" not in gate.lower()
    assert "runtime PAYG calculation has been implemented" not in gate


def test_formal_evidence_review_gate_index_records_ingestion_guards():
    assert FORMAL_EVIDENCE_REVIEW_GATE_INDEX.exists()

    index = _read(FORMAL_EVIDENCE_REVIEW_GATE_INDEX)

    assert "Imports / Actuals" in index
    assert "Tax / PAYG" in index
    assert "Tax / PAYG is not promoted and remains `BASELINE_REQUIRED`" in index
    assert "Imports / Actuals is not promoted and remains `BASELINE_REQUIRED`" in index
    assert "A review gate with `NOT_REVIEWED` blocks governed ingestion" in index
    assert "Only `REVIEWED_READY_FOR_INGESTION` can permit a future governed ingestion slice" in index
    assert "A formal source-evidence draft alone does not permit governed ingestion" in index
    assert "Baseline promotion requires real benchmark, corpus coverage, and answer-gap evidence" in index
    assert "| Tax / PAYG | `BASELINE_REQUIRED`" in index
    assert "| Imports / Actuals | `BASELINE_REQUIRED`" in index
    assert "| Tax / PAYG | `BASELINE_ALREADY_EXISTS`" not in index
    assert "| Imports / Actuals | `BASELINE_ALREADY_EXISTS`" not in index
    assert "Tax / PAYG is promoted" not in index
    assert "Imports / Actuals is promoted" not in index


def test_formal_evidence_review_decision_record_template_records_review_decision_guards():
    assert FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.exists()

    template = _read(FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE)

    assert "`NOT_REVIEWED`" in template
    assert "`NEEDS_REVISION`" in template
    assert "`REVIEWED_READY_FOR_INGESTION`" in template
    assert "`SUPERSEDED`" in template
    assert "A formal source-evidence draft alone does not permit governed ingestion" in template
    assert "A review gate with `NOT_REVIEWED` blocks governed ingestion" in template
    assert "A review gate with `NEEDS_REVISION` blocks governed ingestion" in template
    assert "Only `REVIEWED_READY_FOR_INGESTION` can permit a future governed ingestion slice" in template
    assert "`REVIEWED_READY_FOR_INGESTION` does not itself mutate corpus" in template
    assert "`REVIEWED_READY_FOR_INGESTION` does not itself promote a baseline" in template
    assert "Baseline promotion requires real benchmark, corpus coverage, and answer-gap evidence" in template
    assert "No domain is promoted merely because a review decision exists" in template
    assert "Minerva must not overstate review, ingestion, runtime, or promotion state" in template
    assert "Reviewer name:" in template
    assert "Review date:" in template
    assert "Reviewer rationale:" in template
    assert "Reviewed source artefacts:" in template
    assert "Required follow-up actions:" in template
    assert "Whether governed ingestion is permitted:" in template
    assert "Whether recapture is permitted:" in template
    assert "Whether promotion is permitted:" in template
    assert "Imports / Actuals" in template
    assert "Tax / PAYG" in template
    assert "These examples are placeholders for future completed decision records. They do not mark either domain as reviewed or ready." in template
    assert "Governed ingestion permitted: No unless `REVIEWED_READY_FOR_INGESTION`" in template
    assert "Promotion permitted: No" in template
    assert "Imports / Actuals is not merely file upload or CSV parsing" in template
    assert "Minerva may explain Tax / PAYG but must not calculate PAYG withholding" in template
    assert "Imports / Actuals remains `BASELINE_ALREADY_EXISTS`" not in template
    assert "Tax / PAYG remains `BASELINE_ALREADY_EXISTS`" not in template


def test_formal_evidence_review_decision_record_template_has_required_sections():
    template = _read(FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE)

    for section in (
        "## 1. Review Decision Record Header",
        "## 2. Domain and Baseline Status",
        "## 3. Source Artefacts Reviewed",
        "## 4. Review Gate Status Before Decision",
        "## 5. Review Decision",
        "## 6. Allowed Decision Statuses",
        "## 7. Doctrine Review Findings",
        "## 8. Implementation-State Review Findings",
        "## 9. Evidence-Gap Coverage Findings",
        "## 10. Non-Overclaiming Review",
        "## 11. Ingestion Decision",
        "## 12. Recapture Decision",
        "## 13. Promotion Decision",
        "## 14. Reviewer Details",
        "## 15. Required Follow-Up Actions",
        "## 16. Minerva Answering Implications",
        "## 17. Non-Goals / Explicitly Not Changed",
        "## Domain Example Placeholders",
        "### Imports / Actuals",
        "### Tax / PAYG",
    ):
        assert section in template


def test_formal_evidence_review_decision_record_template_has_required_fillable_fields():
    template = _read(FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE)

    for field in (
        "Decision record title: `<domain name> Formal Evidence Review Decision Record <version>`",
        "Decision record version: `<version>`",
        "Domain name: `<domain name>`",
        "Domain slug: `<domain slug>`",
        "Review date: `<YYYY-MM-DD>`",
        "Reviewer name: `<reviewer name>`",
        "Reviewer rationale: `<brief rationale for the selected decision status>`",
        "Baseline status before review: `<BASELINE_REQUIRED | BASELINE_ALREADY_EXISTS | other recorded status>`",
        "Review gate file path: `<docs/evaluation/source_evidence_drafts/.../..._FORMAL_EVIDENCE_REVIEW_GATE_...md>`",
        "Formal evidence gap plan path: `<docs/evaluation/worker_story_baselines/.../FORMAL_EVIDENCE_GAP_PLAN.md>`",
        "Formal source-evidence draft path: `<docs/evaluation/source_evidence_drafts/.../..._FORMAL_SOURCE_EVIDENCE_DRAFT_...md>`",
        "Reviewed source artefacts: `<list every artefact reviewed>`",
        "Current review status before decision: `<NOT_REVIEWED | NEEDS_REVISION | REVIEWED_READY_FOR_INGESTION | SUPERSEDED>`",
        "Governed ingestion permitted before decision: `<Yes | No>`",
        "Recapture permitted before decision: `<Yes | No>`",
        "Promotion permitted before decision: `<Yes | No>`",
        "Selected decision status: `<NOT_REVIEWED | NEEDS_REVISION | REVIEWED_READY_FOR_INGESTION | SUPERSEDED>`",
        "Doctrine review outcome: `<pass | needs revision | not reviewed | superseded, with detail>`",
        "Implementation-state review outcome: `<pass | needs revision | not reviewed | superseded, with detail>`",
        "Evidence-gap review outcome: `<pass | needs revision | not reviewed | superseded, with detail>`",
        "Non-overclaiming review outcome: `<pass | needs revision | not reviewed | superseded, with detail>`",
        "Whether governed ingestion is permitted: `<Yes | No>`",
        "Whether recapture is permitted: `<Yes | No>`",
        "Whether promotion is permitted: `<Yes | No>`",
        "Required promotion evidence: `real benchmark, corpus coverage, and answer-gap evidence after governed ingestion and recapture`",
        "Minerva may say: `<allowed answer implication>`",
        "Minerva must not say: `<blocked answer implication>`",
    ):
        assert field in template


def test_formal_evidence_review_decision_record_template_lists_allowed_statuses_and_rules_explicitly():
    template = _read(FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE)

    assert "The selected decision status must be exactly one of:" in template
    for status in (
        "`NOT_REVIEWED`",
        "`NEEDS_REVISION`",
        "`REVIEWED_READY_FOR_INGESTION`",
        "`SUPERSEDED`",
    ):
        assert status in template

    for rule in (
        "1. A formal source-evidence draft alone does not permit governed ingestion.",
        "2. A review gate with `NOT_REVIEWED` blocks governed ingestion.",
        "3. A review gate with `NEEDS_REVISION` blocks governed ingestion.",
        "4. A `SUPERSEDED` draft/gate must not be used for governed ingestion.",
        "5. Only `REVIEWED_READY_FOR_INGESTION` can permit a future governed ingestion slice.",
        "6. `REVIEWED_READY_FOR_INGESTION` does not itself mutate corpus.",
        "7. `REVIEWED_READY_FOR_INGESTION` does not itself promote a baseline.",
        "8. Baseline promotion requires real benchmark, corpus coverage, and answer-gap evidence after governed ingestion and recapture.",
        "9. No domain is promoted merely because a review decision exists.",
        "10. Minerva must not overstate review, ingestion, runtime, or promotion state.",
    ):
        assert rule in template


def test_formal_evidence_review_decision_record_template_preserves_examples_and_non_goals():
    template = _read(FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE)

    for required_text in (
        "These examples are placeholders for future completed decision records. They do not mark either domain as reviewed or ready.",
        "Domain name: `Imports / Actuals`",
        "Domain slug: `imports_actuals`",
        "Example current review status before decision: `NOT_REVIEWED`",
        "Example selected decision status: `<NOT_REVIEWED | NEEDS_REVISION | SUPERSEDED, unless a future reviewer explicitly selects REVIEWED_READY_FOR_INGESTION>`",
        "Note: Imports / Actuals is not merely file upload or CSV parsing.",
        "Domain name: `Tax / PAYG`",
        "Domain slug: `tax_payg`",
        "Note: Minerva may explain Tax / PAYG but must not calculate PAYG withholding.",
        "It does not change completed-domain ledger counts.",
    ):
        assert required_text in template

    for non_goal in (
        "DB writes",
        "migrations",
        "corpus mutation",
        "operational JSON ingestion",
        "Code Evidence integration",
        "live LLM calls",
        "benchmark recapture",
        "baseline promotion",
        "ledger promotion",
        "endpoint changes",
        "UI changes",
        "workforce-platform changes",
        "award-configurator-v1 changes",
        "payroll runtime changes",
        "tax runtime changes",
    ):
        assert f"- {non_goal}" in template


def test_formal_evidence_review_decision_record_template_does_not_overclaim_approval_ingestion_or_promotion():
    template = _read(FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE)

    assert "Do not treat draft text, chat agreement or file existence as review approval." in template
    assert "Governed ingestion is permitted only when the selected decision status is `REVIEWED_READY_FOR_INGESTION`" in template
    assert "this decision record only permits a future governed ingestion slice; it does not perform ingestion or mutate corpus" in template
    assert "Recapture must not be treated as permitted merely because a draft exists or because a review decision exists" in template
    assert "No domain is promoted merely because a review decision exists" in template
    assert "It must not describe a formal source-evidence draft as ingested corpus evidence unless a later governed ingestion artefact records that fact" in template

    for overclaim in (
        "Current review status: `REVIEWED_READY_FOR_INGESTION`",
        "Example current review status before decision: `REVIEWED_READY_FOR_INGESTION`",
        "Governed ingestion permitted: Yes",
        "Promotion permitted: Yes",
        "baseline has been promoted",
        "ledger has been promoted",
        "corpus evidence has been ingested",
        "review approval is implied",
    ):
        assert overclaim not in template


def test_tax_payg_not_reviewed_decision_record_blocks_ingestion_recapture_and_promotion():
    assert TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED.exists()

    record = _read(TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED)

    for referenced_path in (
        "docs/evaluation/worker_story_baselines/tax_payg/v0_1/FORMAL_EVIDENCE_GAP_PLAN.md",
        "docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_SOURCE_EVIDENCE_DRAFT_v0_1.md",
        "docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md",
    ):
        assert referenced_path in record

    for required_text in (
        "Domain name: `Tax / PAYG`",
        "Domain slug: `tax_payg`",
        "Baseline status before review: `BASELINE_REQUIRED`",
        "Review gate status before decision: `NOT_REVIEWED`",
        "Selected decision status: `NOT_REVIEWED`",
        "Reviewer name: not assigned",
        "Review date: not recorded",
        "Doctrine review outcome: not reviewed",
        "Implementation-state review outcome: not reviewed",
        "Evidence-gap review outcome: not reviewed",
        "Non-overclaiming review outcome: not reviewed",
        "Governed ingestion permitted: No",
        "Recapture permitted: No",
        "Promotion permitted: No",
        "Minerva must not calculate PAYG withholding",
        "Tax / PAYG remains `BASELINE_REQUIRED`",
        "No Tax / PAYG corpus mutation has occurred in this slice",
        "No Tax / PAYG benchmark recapture has occurred in this slice",
        "No Tax / PAYG ledger promotion occurred in this slice",
    ):
        assert required_text in record

    assert "Selected decision status: `REVIEWED_READY_FOR_INGESTION`" not in record
    assert "Tax / PAYG is `BASELINE_ALREADY_EXISTS`" not in record
    assert "governed ingestion has occurred" not in record
    assert "corpus has been mutated" not in record
    assert "ledger has been promoted" not in record


def test_imports_actuals_not_reviewed_decision_record_blocks_ingestion_recapture_and_promotion():
    assert IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED.exists()

    record = _read(IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED)

    for referenced_path in (
        "docs/evaluation/worker_story_baselines/imports_actuals/v0_1/FORMAL_EVIDENCE_GAP_PLAN.md",
        "docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_SOURCE_EVIDENCE_DRAFT_v0_1.md",
        "docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md",
    ):
        assert referenced_path in record

    for required_text in (
        "Domain name: `Imports / Actuals`",
        "Domain slug: `imports_actuals`",
        "Baseline status before review: `BASELINE_REQUIRED`",
        "Review gate status before decision: `NOT_REVIEWED`",
        "Selected decision status: `NOT_REVIEWED`",
        "Reviewer name: not assigned",
        "Review date: not recorded",
        "Doctrine review outcome: not reviewed",
        "Implementation-state review outcome: not reviewed",
        "Evidence-gap review outcome: not reviewed",
        "Non-overclaiming review outcome: not reviewed",
        "Governed ingestion permitted: No",
        "Recapture permitted: No",
        "Promotion permitted: No",
        "Imports / Actuals is not merely file upload or CSV parsing",
        "Imported actuals are evidence for reconciliation and comparison; they are not the same as calculated payroll truth.",
        "Pay code and RateType mapping must remain evidence-bearing and reviewable.",
        "Imports / Actuals remains `BASELINE_REQUIRED`",
        "No Imports / Actuals corpus mutation has occurred in this slice",
        "No Imports / Actuals benchmark recapture has occurred in this slice",
        "No Imports / Actuals ledger promotion occurred in this slice",
    ):
        assert required_text in record

    assert "Selected decision status: `REVIEWED_READY_FOR_INGESTION`" not in record
    assert "Imports / Actuals is `BASELINE_ALREADY_EXISTS`" not in record
    assert "governed ingestion has occurred" not in record
    assert "corpus has been mutated" not in record
    assert "ledger has been promoted" not in record


def test_formal_evidence_review_decision_record_index_records_not_reviewed_decisions_and_guards():
    assert FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.exists()

    index = _read(FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX)

    for referenced_path in (
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md",
        "docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md",
        "docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md",
        "docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md",
        "docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md",
    ):
        assert referenced_path in index

    for required_text in (
        "| Tax / PAYG | `tax_payg` | `BASELINE_REQUIRED` | `NOT_REVIEWED` | `TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` | `NOT_REVIEWED` | No | No | No | assign reviewer / doctrine review |",
        "| Imports / Actuals | `imports_actuals` | `BASELINE_REQUIRED` | `NOT_REVIEWED` | `IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` | `NOT_REVIEWED` | No | No | No | assign reviewer / doctrine review |",
        "Tax / PAYG remains `BASELINE_REQUIRED` while its latest decision record is `NOT_REVIEWED`.",
        "Imports / Actuals remains `BASELINE_REQUIRED` while its latest decision record is `NOT_REVIEWED`.",
        "1. A filled decision record does not itself permit governed ingestion.",
        "2. A `NOT_REVIEWED` decision record blocks governed ingestion.",
        "3. A `NEEDS_REVISION` decision record blocks governed ingestion.",
        "4. A `SUPERSEDED` decision record must not be used for governed ingestion.",
        "5. Only `REVIEWED_READY_FOR_INGESTION` can permit planning a future governed ingestion slice.",
        "6. `REVIEWED_READY_FOR_INGESTION` does not itself mutate corpus.",
        "7. `REVIEWED_READY_FOR_INGESTION` does not itself run recapture.",
        "8. `REVIEWED_READY_FOR_INGESTION` does not itself promote a baseline.",
        "9. Baseline promotion requires real benchmark, corpus coverage, and answer-gap evidence after governed ingestion and recapture.",
        "10. No domain is promoted merely because a decision record exists.",
        "11. Minerva must not overstate review, ingestion, runtime, recapture, or promotion state.",
    ):
        assert required_text in index

    assert "| Tax / PAYG | `tax_payg` | `BASELINE_ALREADY_EXISTS`" not in index
    assert "| Imports / Actuals | `imports_actuals` | `BASELINE_ALREADY_EXISTS`" not in index
    assert "governed ingestion has occurred" not in index
    assert "corpus has been mutated" not in index
    assert "ledger has been promoted" not in index


def test_source_evidence_drafts_readme_records_formal_evidence_control_model():
    assert SOURCE_EVIDENCE_DRAFTS_README.exists()

    readme = _read(SOURCE_EVIDENCE_DRAFTS_README)

    for section in (
        "## 1. Purpose",
        "## 2. Scope",
        "## 3. Formal Evidence Lifecycle",
        "## 4. Artefact Types",
        "## 5. Current Controlled Domains",
        "## 6. Status and Permission Rules",
        "## 7. Minerva Usage Guidance",
        "## 8. Codex Prompt Preservation Workflow",
        "## 9. Generated Artefact Policy",
        "## 10. Non-Goals",
        "## 11. Follow-Up Workflow",
    ):
        assert section in readme

    for referenced_path in (
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md",
        "docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md",
        "docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md",
        "docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md",
        "docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md",
        "docs/codex_prompts/",
    ):
        assert referenced_path in readme

    for lifecycle_step in (
        "evidence gap identified",
        "→ formal evidence gap plan",
        "→ formal source-evidence draft",
        "→ formal evidence review gate",
        "→ review-gate index",
        "→ formal evidence review decision record template",
        "→ filled review decision record",
        "→ decision-record index",
        "→ REVIEWED_READY_FOR_INGESTION only after explicit review",
        "→ separate governed ingestion slice",
        "→ recapture",
        "→ benchmark/corpus/answer-gap evidence",
        "→ possible ledger promotion",
    ):
        assert lifecycle_step in readme

    for required_text in (
        "`BASELINE_REQUIRED`: 17",
        "`BASELINE_ALREADY_EXISTS`: 14",
        "`RUNBOOK_OUTSTANDING`: 0",
        "`NEEDS_REVIEW`: 0",
        "Tax / PAYG and Imports / Actuals remain `BASELINE_REQUIRED`.",
        "Both domains have complete `NOT_REVIEWED` control chains.",
        "A draft is not ingested corpus evidence and does not permit recapture or promotion.",
        "A `NOT_REVIEWED` decision record is a durable block, not approval.",
        "Only `REVIEWED_READY_FOR_INGESTION` can permit planning a separate governed ingestion slice.",
        "Minerva must say that both domains remain `BASELINE_REQUIRED` while the latest decision records are `NOT_REVIEWED`.",
        "repository artefacts, not chat, as the durable source of truth",
        "Generated benchmark, corpus coverage, answer-gap, and evaluation JSON outputs are transient",
        "docs/codex_prompts/2026-05-15_minerva_formal_evidence_control_readme_v0_1.md",
    ):
        assert required_text in readme

    for blocked_claim in (
        "review approval has occurred",
        "governed ingestion has occurred",
        "corpus has been mutated",
        "ledger has been promoted",
        "Tax / PAYG is `BASELINE_ALREADY_EXISTS`",
        "Imports / Actuals is `BASELINE_ALREADY_EXISTS`",
    ):
        assert blocked_claim not in readme


def test_formal_evidence_control_model_closeout_records_current_control_state():
    assert FORMAL_EVIDENCE_CONTROL_MODEL_CLOSEOUT.exists()
    assert FORMAL_EVIDENCE_CONTROL_MODEL_CLOSEOUT_PROMPT.exists()

    closeout = _read(FORMAL_EVIDENCE_CONTROL_MODEL_CLOSEOUT)

    for referenced_path in (
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_INDEX.md",
        "docs/evaluation/source_evidence_drafts/README.md",
        "README.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_STATUS_TRANSITION_RUNBOOK.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_GOVERNED_INGESTION_PLANNING_RUNBOOK.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_RECAPTURE_PLANNING_RUNBOOK.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_PROMOTION_PLANNING_RUNBOOK.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_PROMOTION_EXECUTION_GUARDRAIL.md",
        "docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md",
        "docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md",
        "docs/codex_prompts/2026-05-15_minerva_formal_evidence_control_model_closeout_v0_1.md",
    ):
        assert referenced_path in closeout

    for required_text in (
        "stop relying on brittle chat history or copied Word documents",
        "Prompts, decisions, source evidence controls, review gates, permission state, and follow-up status are preserved as durable repository artefacts.",
        "Repository artefacts, not chat memory, are the durable source of truth for prompts, decisions, evidence controls, gates, and review state.",
        "| Tax / PAYG | `BASELINE_REQUIRED` | `NOT_REVIEWED` | No | No | No | No |",
        "| Imports / Actuals | `BASELINE_REQUIRED` | `NOT_REVIEWED` | No | No | No | No |",
        "Tax / PAYG remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.",
        "Imports / Actuals remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.",
        "Governed ingestion permitted: No.",
        "Recapture permitted: No.",
        "Promotion permitted: No.",
        "Promotion execution permitted: No.",
        "Future Codex and Minerva slices should begin at `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_INDEX.md`",
        "Future slices should preserve prompt files under `docs/codex_prompts/`",
        "Tax / PAYG remains blocked until explicit review is performed in a separate future slice.",
        "Imports / Actuals remains blocked until explicit review is performed in a separate future slice.",
        "A possible `REVIEWED_READY_FOR_INGESTION` transition, governed ingestion, recapture, and possible promotion must each be performed only in separately scoped future slices",
    ):
        assert required_text in closeout


def test_formal_evidence_control_model_closeout_records_non_operational_boundaries():
    closeout = _read(FORMAL_EVIDENCE_CONTROL_MODEL_CLOSEOUT)

    for boundary in (
        "No corpus mutation occurred.",
        "No Code Evidence integration occurred.",
        "No live LLM call occurred.",
        "No benchmark recapture occurred.",
        "No corpus coverage run occurred.",
        "No answer-gap run occurred.",
        "No runtime change occurred.",
        "No UI change occurred.",
        "No endpoint change occurred.",
        "No workforce-platform change occurred.",
        "No award-configurator-v1 change occurred.",
        "No review approval occurred.",
        "No governed ingestion occurred.",
        "No recapture occurred.",
        "No promotion occurred.",
        "No ledger update occurred.",
        "No DB write, migration, benchmark execution, corpus coverage execution, answer-gap execution, generated artefact creation, ledger promotion, or baseline promotion was performed.",
    ):
        assert boundary in closeout

    for blocked_claim in (
        "governed ingestion has occurred",
        "recapture has occurred",
        "promotion has occurred",
        "ledger has been promoted",
        "Tax / PAYG is `BASELINE_ALREADY_EXISTS`",
        "Imports / Actuals is `BASELINE_ALREADY_EXISTS`",
        "Tax / PAYG is BASELINE_ALREADY_EXISTS",
        "Imports / Actuals is BASELINE_ALREADY_EXISTS",
    ):
        assert blocked_claim not in closeout


def test_formal_evidence_current_state_summary_records_blocked_operator_state():
    assert FORMAL_EVIDENCE_CURRENT_STATE_SUMMARY.exists()
    assert FORMAL_EVIDENCE_CURRENT_STATE_SUMMARY_PROMPT.exists()

    summary = _read(FORMAL_EVIDENCE_CURRENT_STATE_SUMMARY)

    for referenced_path in (
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_INDEX.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_MODEL_CLOSEOUT_2026_05_15.md",
        "docs/codex_prompts/2026-05-15_minerva_formal_evidence_current_state_summary_v0_1.md",
    ):
        assert referenced_path in summary

    for required_text in (
        "## Current Controlled Domains",
        "| Domain | Baseline status | Review status | Governed ingestion permitted | Recapture permitted | Promotion permitted | Promotion execution permitted |",
        "| Tax / PAYG | `BASELINE_REQUIRED` | `NOT_REVIEWED` | No | No | No | No |",
        "| Imports / Actuals | `BASELINE_REQUIRED` | `NOT_REVIEWED` | No | No | No | No |",
        "Tax / PAYG remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.",
        "Imports / Actuals remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.",
        "Governed ingestion permitted: No.",
        "Recapture permitted: No.",
        "Promotion permitted: No.",
        "Promotion execution permitted: No.",
        "Minerva may explain Tax / PAYG doctrine, evidence, implementation state, and current gaps, but must not calculate PAYG withholding.",
        "Imports / Actuals is not merely file upload or CSV parsing.",
    ):
        assert required_text in summary


def test_formal_evidence_current_state_summary_records_boundaries_and_next_actions():
    summary = _read(FORMAL_EVIDENCE_CURRENT_STATE_SUMMARY)

    for boundary in (
        "No review approval occurred.",
        "No governed ingestion occurred.",
        "No corpus mutation occurred.",
        "No recapture occurred.",
        "No benchmark run occurred.",
        "No corpus coverage run occurred.",
        "No answer-gap run occurred.",
        "No promotion occurred.",
        "No ledger update occurred.",
        "No runtime change occurred.",
        "No endpoint change occurred.",
        "No UI change occurred.",
        "No workforce-platform change occurred.",
        "No award-configurator-v1 change occurred.",
        "No DB write, migration, Code Evidence integration, live LLM call, generated artefact creation, ledger promotion, or baseline promotion was performed.",
    ):
        assert boundary in summary

    for required_text in (
        "## Next Allowed Actions",
        "Future work may assign a reviewer.",
        "Future work may perform an explicit review slice.",
        "Future work may create `NEEDS_REVISION` or `REVIEWED_READY_FOR_INGESTION` decision records.",
        "Future work may plan governed ingestion only after review readiness and the required review decision state exist.",
        "Future work must not skip gates.",
        "## Blocked Actions",
        "Corpus ingestion remains blocked for Tax / PAYG and Imports / Actuals.",
        "Recapture remains blocked for Tax / PAYG and Imports / Actuals.",
        "Promotion remains blocked for Tax / PAYG and Imports / Actuals.",
        "Ledger changes remain blocked for Tax / PAYG and Imports / Actuals.",
    ):
        assert required_text in summary

    for blocked_claim in (
        "governed ingestion has occurred",
        "recapture has occurred",
        "promotion has occurred",
        "ledger has been promoted",
        "Tax / PAYG is `BASELINE_ALREADY_EXISTS`",
        "Imports / Actuals is `BASELINE_ALREADY_EXISTS`",
        "Tax / PAYG is BASELINE_ALREADY_EXISTS",
        "Imports / Actuals is BASELINE_ALREADY_EXISTS",
    ):
        assert blocked_claim not in summary


def test_formal_evidence_review_readiness_checklist_records_required_gates():
    assert FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST.exists()

    checklist = _read(FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST)

    for referenced_path in (
        "docs/evaluation/source_evidence_drafts/README.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md",
        "docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md",
        "docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md",
    ):
        assert referenced_path in checklist

    for section in (
        "## 1. Purpose",
        "## 2. Scope",
        "## 3. Reviewer Preconditions",
        "## 4. Source Artefact Checklist",
        "## 5. Doctrine Review Checklist",
        "## 6. Implementation-State Review Checklist",
        "## 7. Evidence-Gap Coverage Checklist",
        "## 8. Non-Overclaiming Checklist",
        "## 9. Decision Status Guidance",
        "## 10. Ingestion Readiness Gate",
        "## 11. Recapture Readiness Gate",
        "## 12. Promotion Readiness Gate",
        "## 13. Domain-Specific Notes",
        "## 14. Minerva Answering Guidance",
        "## 15. Non-Goals",
        "## 16. Follow-Up Actions",
    ):
        assert section in checklist

    for precondition in (
        "Correct domain and slug.",
        "Current baseline status.",
        "Current review gate status.",
        "Latest decision record.",
        "Source-evidence draft under review.",
        "Formal evidence gap plan.",
        "Review-gate index entry.",
        "Decision-record index entry.",
        "No newer superseding artefact exists.",
    ):
        assert precondition in checklist

    for required_text in (
        "Use when no formal review has occurred.",
        "Use when the draft has been reviewed and is not safe for governed ingestion.",
        "Use only when doctrine review, implementation-state review, evidence-gap coverage review, and non-overclaiming review are all acceptable.",
        "Use when the draft/gate/decision record has been replaced and must not be used for governed ingestion.",
        "A checklist alone does not change review status.",
        "A checklist alone does not permit governed ingestion.",
        "A checklist alone does not mutate corpus.",
        "A checklist alone does not run recapture.",
        "A checklist alone does not promote a baseline.",
        "`REVIEWED_READY_FOR_INGESTION` permits planning a future governed ingestion slice only.",
        "Governed ingestion must be a separate explicit slice.",
        "Recapture must happen only after governed ingestion.",
        "Promotion requires benchmark, corpus coverage, answer-gap evidence, and ledger update.",
        "Minerva must not overstate checklist completion as review approval, ingestion, recapture, or promotion.",
        "Tax / PAYG remains `BASELINE_REQUIRED`.",
        "Imports / Actuals remains `BASELINE_REQUIRED`.",
        "Minerva may explain Tax / PAYG but must not calculate PAYG withholding.",
        "Deterministic services, tax providers, and governed rule packs own PAYG withholding calculation.",
        "Imports / Actuals is not merely file upload or CSV parsing.",
        "Imported actuals are not the same as calculated payroll truth.",
        "Pay code and RateType mapping must remain evidence-bearing and reviewable.",
        "| Tax / PAYG | `BASELINE_REQUIRED` | `NOT_REVIEWED` | No | No | No |",
        "| Imports / Actuals | `BASELINE_REQUIRED` | `NOT_REVIEWED` | No | No | No |",
        "generated artefact commits",
    ):
        assert required_text in checklist

    assert "### NOT_REVIEWED" in checklist
    assert "### NEEDS_REVISION" in checklist
    assert "### REVIEWED_READY_FOR_INGESTION" in checklist
    assert "### SUPERSEDED" in checklist
    assert checklist.count("Governed ingestion permitted: No.") == 2
    assert checklist.count("Recapture permitted: No.") == 2
    assert checklist.count("Promotion permitted: No.") == 2

    for blocked_claim in (
        "Tax / PAYG is `BASELINE_ALREADY_EXISTS`",
        "Imports / Actuals is `BASELINE_ALREADY_EXISTS`",
        "governed ingestion has occurred",
        "corpus has been mutated",
        "ledger has been promoted",
    ):
        assert blocked_claim not in checklist


def test_formal_evidence_review_status_transition_runbook_records_required_controls():
    assert FORMAL_EVIDENCE_REVIEW_STATUS_TRANSITION_RUNBOOK.exists()

    runbook = _read(FORMAL_EVIDENCE_REVIEW_STATUS_TRANSITION_RUNBOOK)

    for referenced_path in (
        "docs/evaluation/source_evidence_drafts/README.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md",
        "docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md",
        "docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md",
    ):
        assert referenced_path in runbook

    for status_heading in (
        "### NOT_REVIEWED",
        "### NEEDS_REVISION",
        "### REVIEWED_READY_FOR_INGESTION",
        "### SUPERSEDED",
    ):
        assert status_heading in runbook

    for required_text in (
        "A status transition from `NOT_REVIEWED` to `NEEDS_REVISION`, `REVIEWED_READY_FOR_INGESTION`, or `SUPERSEDED` requires a separate explicit review slice.",
        "The filled decision record must include:",
        "reviewer identity",
        "review date",
        "reviewer rationale",
        "doctrine review outcome",
        "implementation-state review outcome",
        "evidence-gap review outcome",
        "non-overclaiming review outcome",
        "The reviewer must complete:",
        "doctrine review",
        "implementation-state review",
        "evidence-gap review",
        "non-overclaiming review",
        "`NEEDS_REVISION` blocks governed ingestion and requires follow-up changes before review can proceed.",
        "`SUPERSEDED` blocks governed ingestion and requires the superseded draft/gate/decision record not be used for governed ingestion planning.",
    ):
        assert required_text in runbook


def test_formal_evidence_review_status_transition_runbook_preserves_blocked_states():
    runbook = _read(FORMAL_EVIDENCE_REVIEW_STATUS_TRANSITION_RUNBOOK)

    for required_text in (
        "| Tax / PAYG | `BASELINE_REQUIRED` | `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` | `NOT_REVIEWED` | No | No | No |",
        "| Imports / Actuals | `BASELINE_REQUIRED` | `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` | `NOT_REVIEWED` | No | No | No |",
        "Tax / PAYG remains `BASELINE_REQUIRED`.",
        "Imports / Actuals remains `BASELINE_REQUIRED`.",
        "Governed ingestion permitted: No.",
        "Recapture permitted: No.",
        "Promotion permitted: No.",
        "For Tax / PAYG, Minerva may explain Tax / PAYG doctrine, source evidence, implementation state, and known gaps, but must not calculate PAYG withholding.",
        "For Imports / Actuals, Minerva must preserve that Imports / Actuals is not merely file upload or CSV parsing.",
        "`REVIEWED_READY_FOR_INGESTION` permits planning a future governed ingestion slice only.",
        "It does not mutate corpus.",
        "It does not run recapture.",
        "It does not promote a baseline.",
        "It does not change runtime behaviour.",
        "It does not change ledger counts.",
    ):
        assert required_text in runbook

    for blocked_claim in (
        "governed ingestion has occurred",
        "corpus has been mutated",
        "ledger has been promoted",
        "Tax / PAYG is BASELINE_ALREADY_EXISTS",
        "Tax / PAYG is `BASELINE_ALREADY_EXISTS`",
        "Imports / Actuals is BASELINE_ALREADY_EXISTS",
        "Imports / Actuals is `BASELINE_ALREADY_EXISTS`",
    ):
        assert blocked_claim not in runbook


def test_formal_evidence_governed_ingestion_planning_runbook_records_required_controls():
    assert FORMAL_EVIDENCE_GOVERNED_INGESTION_PLANNING_RUNBOOK.exists()

    runbook = _read(FORMAL_EVIDENCE_GOVERNED_INGESTION_PLANNING_RUNBOOK)

    for referenced_path in (
        "docs/evaluation/source_evidence_drafts/README.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_STATUS_TRANSITION_RUNBOOK.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md",
        "docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md",
        "docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md",
    ):
        assert referenced_path in runbook

    for precondition in (
        "Latest decision record selected status is `REVIEWED_READY_FOR_INGESTION`.",
        "Reviewer identity present.",
        "Reviewer date present.",
        "Reviewer rationale present.",
        "Reviewed source artefacts identified.",
        "Ingestion scope documented.",
        "Target corpus location documented.",
        "Mutation risk documented.",
        "Rollback/restore plan documented.",
        "Generated artefact policy documented.",
        "Recapture plan documented.",
        "Tests planned before corpus mutation.",
    ):
        assert precondition in runbook

    for required_text in (
        "Current Tax / PAYG and Imports / Actuals records are `NOT_REVIEWED`, so governed ingestion is currently not permitted for either domain.",
        "Governed ingestion must be a separate explicit slice after planning and review readiness.",
        "Ingestion planning alone does not mutate corpus.",
        "Ingestion planning alone does not run recapture.",
        "Ingestion planning alone does not promote a baseline.",
        "Ingestion planning alone does not change runtime behaviour.",
        "Ingestion planning alone does not change ledger counts.",
        "Ingestion planning alone does not permit Minerva to answer as if ingestion has happened.",
        "For Tax / PAYG, Minerva may explain Tax / PAYG doctrine, source evidence, implementation state, and known gaps, but must not calculate PAYG withholding.",
        "For Imports / Actuals, Minerva must preserve that Imports / Actuals is not merely file upload or CSV parsing.",
    ):
        assert required_text in runbook


def test_formal_evidence_governed_ingestion_planning_runbook_preserves_blocked_states():
    runbook = _read(FORMAL_EVIDENCE_GOVERNED_INGESTION_PLANNING_RUNBOOK)

    for required_text in (
        "| Tax / PAYG | `BASELINE_REQUIRED` | `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` | `NOT_REVIEWED` | No | No | No |",
        "| Imports / Actuals | `BASELINE_REQUIRED` | `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` | `NOT_REVIEWED` | No | No | No |",
        "Tax / PAYG remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.",
        "Imports / Actuals remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.",
        "Governed ingestion permitted: No.",
        "Recapture permitted: No.",
        "Promotion permitted: No.",
        "It does not change completed-domain ledger counts.",
        "It does not mark Tax / PAYG or Imports / Actuals as `REVIEWED_READY_FOR_INGESTION`.",
        "It does not mark Tax / PAYG or Imports / Actuals as `BASELINE_ALREADY_EXISTS`.",
    ):
        assert required_text in runbook

    for blocked_claim in (
        "governed ingestion has occurred",
        "corpus has been mutated",
        "ledger has been promoted",
        "Tax / PAYG is BASELINE_ALREADY_EXISTS",
        "Tax / PAYG is `BASELINE_ALREADY_EXISTS`",
        "Imports / Actuals is BASELINE_ALREADY_EXISTS",
        "Imports / Actuals is `BASELINE_ALREADY_EXISTS`",
    ):
        assert blocked_claim not in runbook


def test_formal_evidence_recapture_planning_runbook_records_required_controls():
    assert FORMAL_EVIDENCE_RECAPTURE_PLANNING_RUNBOOK.exists()

    runbook = _read(FORMAL_EVIDENCE_RECAPTURE_PLANNING_RUNBOOK)

    for referenced_path in (
        "docs/evaluation/source_evidence_drafts/README.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_STATUS_TRANSITION_RUNBOOK.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_GOVERNED_INGESTION_PLANNING_RUNBOOK.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md",
        "docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md",
        "docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md",
    ):
        assert referenced_path in runbook

    for precondition in (
        "Latest decision record selected status is `REVIEWED_READY_FOR_INGESTION`.",
        "Separate governed ingestion slice completed.",
        "Corpus mutation evidence recorded.",
        "Ingested source artefacts identified.",
        "Generated artefact policy documented.",
        "Benchmark manifest identified.",
        "Corpus coverage command identified.",
        "Answer-gap command identified.",
        "Expected evidence groups identified.",
        "Regression guardrails documented.",
        "Rollback/restore notes preserved.",
    ):
        assert precondition in runbook

    for required_text in (
        "Current Tax / PAYG and Imports / Actuals records are `NOT_REVIEWED`, so recapture is currently not permitted for either domain.",
        "Actual recapture must be a separate explicit slice after governed ingestion evidence exists.",
        "Recapture planning alone does not mutate corpus.",
        "Recapture planning alone does not run benchmark.",
        "Recapture planning alone does not run corpus coverage.",
        "Recapture planning alone does not run answer-gap reporting.",
        "Recapture planning alone does not promote a baseline.",
        "Recapture planning alone does not change runtime behaviour.",
        "Recapture planning alone does not change ledger counts.",
        "Recapture planning alone does not permit Minerva to answer as if recapture has happened.",
        "For Tax / PAYG, Minerva may explain Tax / PAYG doctrine, source evidence, implementation state, and known gaps, but must not calculate PAYG withholding.",
        "For Imports / Actuals, Minerva must preserve that Imports / Actuals is not merely file upload or CSV parsing.",
    ):
        assert required_text in runbook


def test_formal_evidence_recapture_planning_runbook_preserves_blocked_states():
    runbook = _read(FORMAL_EVIDENCE_RECAPTURE_PLANNING_RUNBOOK)

    for required_text in (
        "| Tax / PAYG | `BASELINE_REQUIRED` | `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` | `NOT_REVIEWED` | No | No | No |",
        "| Imports / Actuals | `BASELINE_REQUIRED` | `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` | `NOT_REVIEWED` | No | No | No |",
        "Tax / PAYG remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.",
        "Imports / Actuals remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.",
        "Governed ingestion permitted: No.",
        "Recapture permitted: No.",
        "Promotion permitted: No.",
        "It does not change completed-domain ledger counts.",
        "It does not mark Tax / PAYG or Imports / Actuals as `REVIEWED_READY_FOR_INGESTION`.",
        "It does not mark Tax / PAYG or Imports / Actuals as `BASELINE_ALREADY_EXISTS`.",
    ):
        assert required_text in runbook

    for blocked_claim in (
        "recapture has occurred",
        "benchmark has passed",
        "corpus coverage has passed",
        "answer gap is GOOD",
        "ledger has been promoted",
        "Tax / PAYG is BASELINE_ALREADY_EXISTS",
        "Tax / PAYG is `BASELINE_ALREADY_EXISTS`",
        "Imports / Actuals is BASELINE_ALREADY_EXISTS",
        "Imports / Actuals is `BASELINE_ALREADY_EXISTS`",
    ):
        assert blocked_claim not in runbook


def test_formal_evidence_promotion_planning_runbook_records_required_controls():
    assert FORMAL_EVIDENCE_PROMOTION_PLANNING_RUNBOOK.exists()

    runbook = _read(FORMAL_EVIDENCE_PROMOTION_PLANNING_RUNBOOK)

    for referenced_path in (
        "docs/evaluation/source_evidence_drafts/README.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_STATUS_TRANSITION_RUNBOOK.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_GOVERNED_INGESTION_PLANNING_RUNBOOK.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_RECAPTURE_PLANNING_RUNBOOK.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md",
        "docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md",
        "docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md",
    ):
        assert referenced_path in runbook

    for precondition in (
        "Latest decision record selected status is `REVIEWED_READY_FOR_INGESTION`.",
        "Separate governed ingestion slice completed.",
        "Recapture slice completed.",
        "Benchmark command results recorded.",
        "Corpus coverage command results recorded.",
        "Answer-gap command results recorded.",
        "No unresolved `MISSING` evidence groups unless accepted with documented rationale.",
        "Benchmark pass/failure status documented.",
        "Answer-gap `GOOD` or accepted under documented policy.",
        "Generated artefact policy satisfied.",
        "Ledger update plan documented.",
        "Rollback/supersession notes preserved.",
    ):
        assert precondition in runbook

    for required_text in (
        "Current Tax / PAYG and Imports / Actuals records are `NOT_REVIEWED`, so promotion is currently not permitted for either domain.",
        "Actual promotion must be a separate explicit slice after recapture evidence exists and is accepted.",
        "Promotion planning alone does not mutate corpus.",
        "Promotion planning alone does not run benchmark.",
        "Promotion planning alone does not run corpus coverage.",
        "Promotion planning alone does not run answer-gap reporting.",
        "Promotion planning alone does not promote a baseline.",
        "Promotion planning alone does not change runtime behaviour.",
        "Promotion planning alone does not change ledger counts.",
        "Promotion planning alone does not permit Minerva to answer as if promotion has happened.",
        "For Tax / PAYG, Minerva may explain Tax / PAYG doctrine, source evidence, implementation state, and known gaps, but must not calculate PAYG withholding.",
        "For Imports / Actuals, Minerva must preserve that Imports / Actuals is not merely file upload or CSV parsing.",
    ):
        assert required_text in runbook


def test_formal_evidence_promotion_planning_runbook_preserves_blocked_states():
    runbook = _read(FORMAL_EVIDENCE_PROMOTION_PLANNING_RUNBOOK)

    for required_text in (
        "| Tax / PAYG | `BASELINE_REQUIRED` | `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` | `NOT_REVIEWED` | No | No | No |",
        "| Imports / Actuals | `BASELINE_REQUIRED` | `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` | `NOT_REVIEWED` | No | No | No |",
        "Tax / PAYG remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.",
        "Imports / Actuals remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.",
        "Governed ingestion permitted: No.",
        "Recapture permitted: No.",
        "Promotion permitted: No.",
        "It does not change completed-domain ledger counts.",
        "It does not mark Tax / PAYG or Imports / Actuals as `REVIEWED_READY_FOR_INGESTION`.",
        "It does not mark Tax / PAYG or Imports / Actuals as `BASELINE_ALREADY_EXISTS`.",
    ):
        assert required_text in runbook

    for blocked_claim in (
        "promotion has occurred",
        "benchmark has passed",
        "corpus coverage has passed",
        "answer gap is GOOD",
        "ledger has been promoted",
        "Tax / PAYG is BASELINE_ALREADY_EXISTS",
        "Tax / PAYG is `BASELINE_ALREADY_EXISTS`",
        "Imports / Actuals is BASELINE_ALREADY_EXISTS",
        "Imports / Actuals is `BASELINE_ALREADY_EXISTS`",
    ):
        assert blocked_claim not in runbook


def test_formal_evidence_promotion_execution_guardrail_records_required_controls():
    assert FORMAL_EVIDENCE_PROMOTION_EXECUTION_GUARDRAIL.exists()

    guardrail = _read(FORMAL_EVIDENCE_PROMOTION_EXECUTION_GUARDRAIL)

    for referenced_path in (
        "docs/evaluation/source_evidence_drafts/README.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_STATUS_TRANSITION_RUNBOOK.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_GOVERNED_INGESTION_PLANNING_RUNBOOK.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_RECAPTURE_PLANNING_RUNBOOK.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_PROMOTION_PLANNING_RUNBOOK.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md",
        "docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md",
        "docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md",
    ):
        assert referenced_path in guardrail

    for preflight_requirement in (
        "Latest decision record selected status is `REVIEWED_READY_FOR_INGESTION`.",
        "Governed ingestion slice completed.",
        "Corpus mutation evidence recorded.",
        "Recapture slice completed.",
        "Benchmark results recorded.",
        "Corpus coverage results recorded.",
        "Answer-gap results recorded.",
        "Benchmark pass/failure status accepted.",
        "No unresolved `MISSING` evidence groups unless accepted with written rationale.",
        "Answer-gap `GOOD` or accepted under documented policy.",
        "Generated artefact policy satisfied.",
        "Reviewer identity/date/rationale recorded.",
        "Ledger update diff planned.",
        "Rollback/supersession notes preserved.",
        "Explicit user approval for ledger promotion.",
    ):
        assert preflight_requirement in guardrail

    for required_text in (
        "Current Tax / PAYG and Imports / Actuals records are `NOT_REVIEWED`, so promotion execution is currently blocked for both domains.",
        "Actual promotion must be a separate explicit execution slice after this final preflight passes.",
        "This guardrail alone does not mutate corpus.",
        "This guardrail alone does not run benchmark.",
        "This guardrail alone does not run corpus coverage.",
        "This guardrail alone does not run answer-gap reporting.",
        "This guardrail alone does not promote a baseline.",
        "This guardrail alone does not change runtime behaviour.",
        "This guardrail alone does not change ledger counts.",
        "This guardrail alone does not permit Minerva to answer as if promotion has happened.",
        "For Tax / PAYG, Minerva may explain Tax / PAYG doctrine, source evidence, implementation state, and known gaps, but must not calculate PAYG withholding.",
        "For Imports / Actuals, Minerva must preserve that Imports / Actuals is not merely file upload or CSV parsing.",
    ):
        assert required_text in guardrail


def test_formal_evidence_promotion_execution_guardrail_preserves_blocked_states():
    guardrail = _read(FORMAL_EVIDENCE_PROMOTION_EXECUTION_GUARDRAIL)

    for required_text in (
        "| Tax / PAYG | `BASELINE_REQUIRED` | `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` | `NOT_REVIEWED` | No | No | No |",
        "| Imports / Actuals | `BASELINE_REQUIRED` | `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` | `NOT_REVIEWED` | No | No | No |",
        "Tax / PAYG remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.",
        "Imports / Actuals remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.",
        "Governed ingestion permitted: No.",
        "Recapture permitted: No.",
        "Promotion permitted: No.",
        "It does not change completed-domain ledger counts.",
        "It does not mark Tax / PAYG or Imports / Actuals as `REVIEWED_READY_FOR_INGESTION`.",
        "It does not mark Tax / PAYG or Imports / Actuals as `BASELINE_ALREADY_EXISTS`.",
    ):
        assert required_text in guardrail

    for blocked_claim in (
        "promotion has occurred",
        "benchmark has passed",
        "corpus coverage has passed",
        "answer gap is GOOD",
        "ledger has been promoted",
        "Tax / PAYG is BASELINE_ALREADY_EXISTS",
        "Tax / PAYG is `BASELINE_ALREADY_EXISTS`",
        "Imports / Actuals is BASELINE_ALREADY_EXISTS",
        "Imports / Actuals is `BASELINE_ALREADY_EXISTS`",
    ):
        assert blocked_claim not in guardrail


def test_formal_evidence_control_index_records_master_navigation_and_lifecycle():
    assert FORMAL_EVIDENCE_CONTROL_INDEX.exists()

    index = _read(FORMAL_EVIDENCE_CONTROL_INDEX)

    for section in (
        "## 1. Purpose",
        "## 2. Scope",
        "## 3. Control Artefact Map",
        "## 4. Formal Evidence Lifecycle",
        "## 5. Current Controlled Domains",
        "## 6. Current Permission State",
        "## 7. How Minerva Should Use This Index",
        "## 8. How Codex Should Use This Index",
        "## 9. Non-Goals",
        "## 10. Follow-Up Workflow",
    ):
        assert section in index

    for referenced_path in (
        "docs/evaluation/source_evidence_drafts/README.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_STATUS_TRANSITION_RUNBOOK.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_GOVERNED_INGESTION_PLANNING_RUNBOOK.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_RECAPTURE_PLANNING_RUNBOOK.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_PROMOTION_PLANNING_RUNBOOK.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_PROMOTION_EXECUTION_GUARDRAIL.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_MODEL_CLOSEOUT_2026_05_15.md",
        "docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md",
        "docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md",
    ):
        assert referenced_path in index

    for lifecycle_step in (
        "evidence gap identified",
        "-> formal evidence gap plan",
        "-> formal source-evidence draft",
        "-> formal evidence review gate",
        "-> review-gate index",
        "-> decision record template",
        "-> filled decision record",
        "-> decision-record index",
        "-> review readiness checklist",
        "-> status transition runbook",
        "-> governed ingestion planning",
        "-> recapture planning",
        "-> promotion planning",
        "-> promotion execution guardrail",
        "-> possible explicit promotion slice only after final preflight",
    ):
        assert lifecycle_step in index


def test_formal_evidence_control_index_preserves_current_blocks_and_boundaries():
    index = _read(FORMAL_EVIDENCE_CONTROL_INDEX)

    for required_text in (
        "| Formal evidence control model closeout/state summary | `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_MODEL_CLOSEOUT_2026_05_15.md` |",
        "Future Minerva/Codex work should start at this control index and use `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_MODEL_CLOSEOUT_2026_05_15.md` as the closeout/state summary to understand what was created, why it exists, what remains blocked, and what future slices are allowed or forbidden to do.",
        "| Tax / PAYG | `BASELINE_REQUIRED` | `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` | `NOT_REVIEWED` | No | No | No | No |",
        "| Imports / Actuals | `BASELINE_REQUIRED` | `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` | `NOT_REVIEWED` | No | No | No | No |",
        "Tax / PAYG remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.",
        "Imports / Actuals remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.",
        "Governed ingestion permitted: No.",
        "Recapture permitted: No.",
        "Promotion permitted: No.",
        "Promotion execution permitted: No.",
        "No control artefact by itself mutates corpus, runs benchmark, runs corpus coverage, runs answer-gap reporting, changes runtime behaviour, changes ledger counts, or promotes a baseline.",
        "For Tax / PAYG, Minerva may explain Tax / PAYG doctrine, source evidence, implementation state, and known gaps, but must not calculate PAYG withholding.",
        "For Imports / Actuals, Minerva must preserve that Imports / Actuals is not merely file upload or CSV parsing.",
        "Future Codex slices should check this control index before changing formal evidence status, ingestion, recapture, promotion, or ledger state.",
    ):
        assert required_text in index

    for blocked_claim in (
        "governed ingestion has occurred",
        "recapture has occurred",
        "promotion has occurred",
        "ledger has been promoted",
        "Tax / PAYG is BASELINE_ALREADY_EXISTS",
        "Tax / PAYG is `BASELINE_ALREADY_EXISTS`",
        "Imports / Actuals is BASELINE_ALREADY_EXISTS",
        "Imports / Actuals is `BASELINE_ALREADY_EXISTS`",
    ):
        assert blocked_claim not in index


def test_historical_knowledge_control_files_exist_and_are_linked():
    for path in (
        HISTORICAL_KNOWLEDGE_CONTROL_INDEX,
        HISTORICAL_KNOWLEDGE_GAP_REGISTER,
        HISTORICAL_SOURCE_TIERING_MODEL,
        HISTORICAL_BACKFILL_PROCESS,
    ):
        assert path.exists()

    index = _read(HISTORICAL_KNOWLEDGE_CONTROL_INDEX)

    for referenced_path in (
        "docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_GAP_REGISTER.md",
        "docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_TIERING_MODEL.md",
        "docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_PROCESS.md",
    ):
        assert referenced_path in index


def test_historical_knowledge_gap_register_records_incomplete_pre_control_state():
    gap_register = _read(HISTORICAL_KNOWLEDGE_GAP_REGISTER)

    for required_text in (
        "pre-control-model historical knowledge is incomplete",
        "not yet captured to the same durable standard as the new formal-evidence model",
        "does not mean historical knowledge has been reviewed, backfilled, ingested, or promoted",
    ):
        assert required_text in gap_register


def test_historical_source_tiering_model_defines_three_source_tiers():
    tiering_model = _read(HISTORICAL_SOURCE_TIERING_MODEL)

    for required_text in (
        "| Tier 1 | Code and tests | Highest authority for implemented state |",
        "| Tier 2 | Developer logs, hardening logs, and platform doctrine | Curated decision/rationale sources requiring review |",
        "| Tier 3 | Historical chats and continuance prompts | Raw historical source material, not final truth |",
        "Historical chats must not be ingested directly as truth.",
        "Developer logs and doctrine documents are valuable but may include planned, partial, superseded, or backlog work",
        "Code/tests must be used to confirm implemented behaviour, but code alone may not explain why.",
    ):
        assert required_text in tiering_model


def test_historical_backfill_process_records_classifications_and_chat_boundary():
    backfill_process = _read(HISTORICAL_BACKFILL_PROCESS)

    for classification in (
        "IMPLEMENTED_AND_TESTED",
        "IMPLEMENTED_NOT_FULLY_TESTED",
        "DOCUMENTED_DOCTRINE",
        "DOCUMENTED_BACKLOG",
        "PLANNED_NOT_IMPLEMENTED",
        "SUPERSEDED",
        "UNCERTAIN_REQUIRES_REVIEW",
    ):
        assert classification in backfill_process

    for required_text in (
        "Identify historical source material",
        "Register source provenance",
        "Classify source tier",
        "Extract candidate decisions",
        "Cross-check against code/tests/logs/doctrine/commits",
        "Classify implementation state",
        "Create a curated backfill evidence pack",
        "Add a review gate",
        "Only later consider governed ingestion",
        "Historical chats and continuance prompts are raw source material, not final truth.",
        "Historical chats must not be ingested directly as truth.",
    ):
        assert required_text in backfill_process


def test_historical_knowledge_documents_preserve_non_ingestion_boundaries():
    combined = "\n".join(
        _read(path)
        for path in (
            HISTORICAL_KNOWLEDGE_CONTROL_INDEX,
            HISTORICAL_KNOWLEDGE_GAP_REGISTER,
            HISTORICAL_SOURCE_TIERING_MODEL,
            HISTORICAL_BACKFILL_PROCESS,
        )
    )

    for required_text in (
        "does not consume historical chats",
        "does not ingest developer logs",
        "does not ingest doctrine documents",
        "does not ingest code",
        "does not mutate corpus",
        "does not run live LLM",
        "does not connect Code Evidence",
        "does not change runtime behaviour",
        "does not promote baselines",
        "does not change ledger counts",
        "does not implement DB writes",
        "does not implement DB writes, migrations, corpus mutation, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, runtime changes, historical ingestion, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, ledger update, or generated artefact creation",
        "does not mark any domain `REVIEWED_READY_FOR_INGESTION`",
        "does not mark any domain `BASELINE_ALREADY_EXISTS`",
    ):
        assert required_text in combined


def test_historical_knowledge_priority_domains_are_listed():
    combined = "\n".join(
        _read(path)
        for path in (
            HISTORICAL_KNOWLEDGE_CONTROL_INDEX,
            HISTORICAL_KNOWLEDGE_GAP_REGISTER,
            HISTORICAL_BACKFILL_PROCESS,
        )
    )

    for priority_domain in (
        "Worker Story",
        "ObjectTime / Source Truth",
        "Process Periods / PayRun Lifecycle",
        "Payroll Buckets / Bases / Totals",
        "Deductions and Obligations",
        "Tax / PAYG",
        "Imports / Actuals",
        "Leave Workflow / Annual Leave",
        "Award Configurator",
        "Asphalt Award Build",
    ):
        assert priority_domain in combined

    assert "Tax / PAYG and Imports / Actuals remain governed by the formal evidence control model" in combined


def test_historical_source_inventory_templates_exist_and_reference_controls():
    for path in (
        HISTORICAL_SOURCE_INVENTORY_TEMPLATE,
        HISTORICAL_DEVELOPER_LOG_DOCTRINE_INVENTORY_TEMPLATE,
        HISTORICAL_CHAT_CONTINUANCE_INVENTORY_TEMPLATE,
        HISTORICAL_CODE_EVIDENCE_INVENTORY_TEMPLATE,
    ):
        assert path.exists()

        template = _read(path)

        for referenced_path in (
            "docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md",
            "docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_GAP_REGISTER.md",
            "docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_TIERING_MODEL.md",
            "docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_PROCESS.md",
        ):
            assert referenced_path in template


def test_historical_source_inventory_templates_define_required_fields_and_classifications():
    required_fields = (
        "Source title",
        "Source type",
        "Source tier",
        "Date or date range",
        "Repository/domain",
        "Related commits if known",
        "Related developer log or doctrine reference",
        "Implementation-state classification",
        "Evidence confidence",
        "Supersession risk",
        "Backlog/doctrine/runtime distinction",
        "Review required",
        "Ingestion permitted",
        "Notes",
    )
    classifications = (
        "IMPLEMENTED_AND_TESTED",
        "IMPLEMENTED_NOT_FULLY_TESTED",
        "DOCUMENTED_DOCTRINE",
        "DOCUMENTED_BACKLOG",
        "PLANNED_NOT_IMPLEMENTED",
        "SUPERSEDED",
        "UNCERTAIN_REQUIRES_REVIEW",
    )

    for path in (
        HISTORICAL_SOURCE_INVENTORY_TEMPLATE,
        HISTORICAL_DEVELOPER_LOG_DOCTRINE_INVENTORY_TEMPLATE,
        HISTORICAL_CHAT_CONTINUANCE_INVENTORY_TEMPLATE,
        HISTORICAL_CODE_EVIDENCE_INVENTORY_TEMPLATE,
    ):
        template = _read(path)

        for required_field in required_fields:
            assert required_field in template

        for classification in classifications:
            assert classification in template


def test_historical_source_inventory_templates_preserve_tier_rules():
    general_template = _read(HISTORICAL_SOURCE_INVENTORY_TEMPLATE)
    log_doctrine_template = _read(HISTORICAL_DEVELOPER_LOG_DOCTRINE_INVENTORY_TEMPLATE)
    chat_template = _read(HISTORICAL_CHAT_CONTINUANCE_INVENTORY_TEMPLATE)
    code_template = _read(HISTORICAL_CODE_EVIDENCE_INVENTORY_TEMPLATE)

    for required_text in (
        "Tier 1 code and tests are the highest authority for implemented state",
        "Tier 2 developer logs, hardening logs, and platform doctrine are curated decision/rationale sources requiring review",
        "Tier 3 historical chats and continuance prompts are raw historical source material, not final truth",
    ):
        assert required_text in general_template

    for required_text in (
        "curated decision/rationale sources requiring review and implementation-state classification",
        "may include planned, partial, superseded, or backlog work",
        "does not override Tier 1 code and tests for implemented state",
    ):
        assert required_text in log_doctrine_template

    for required_text in (
        "raw historical source material, not final truth",
        "require cross-check against code/tests/logs/doctrine/commits",
        "must not be ingested directly as truth",
    ):
        assert required_text in chat_template

    for required_text in (
        "highest authority for implemented state",
        "code alone may not explain why",
        "does not automatically explain rationale",
    ):
        assert required_text in code_template


def test_historical_source_inventory_templates_preserve_non_mutation_boundaries():
    combined = "\n".join(
        _read(path)
        for path in (
            HISTORICAL_SOURCE_INVENTORY_TEMPLATE,
            HISTORICAL_DEVELOPER_LOG_DOCTRINE_INVENTORY_TEMPLATE,
            HISTORICAL_CHAT_CONTINUANCE_INVENTORY_TEMPLATE,
            HISTORICAL_CODE_EVIDENCE_INVENTORY_TEMPLATE,
        )
    )

    for required_text in (
        "does not mutate corpus",
        "does not ingest sources",
        "does not connect Code Evidence",
        "does not run live LLM",
        "does not change runtime behaviour",
        "does not promote baselines",
        "does not change ledger counts",
        "does not consume historical chats",
        "does not ingest developer logs",
        "does not ingest doctrine documents",
        "does not ingest code",
        "historical ingestion",
        "review approval",
        "governed ingestion",
        "recapture",
        "benchmark execution",
        "corpus coverage execution",
        "answer-gap execution",
        "ledger update",
        "generated artefact creation",
    ):
        assert required_text in combined
    assert "remain `BASELINE_REQUIRED` and `NOT_REVIEWED`" in combined


def test_source_evidence_readme_links_control_index_as_master_starting_point():
    readme = _read(SOURCE_EVIDENCE_DRAFTS_README)

    for required_text in (
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_INDEX.md",
        "master starting point/control index",
        "review gates",
        "decision records",
        "readiness checklists",
        "status transitions",
        "governed ingestion planning",
        "recapture planning",
        "promotion planning",
        "promotion execution guardrails",
        "the control index is the master map",
        "Tax / PAYG and Imports / Actuals remain `BASELINE_REQUIRED`.",
        "| Tax / PAYG | `BASELINE_REQUIRED`",
        "| Imports / Actuals | `BASELINE_REQUIRED`",
        "| `NOT_REVIEWED` | blocked | blocked | blocked |",
    ):
        assert required_text in readme


def test_root_readme_links_control_index_as_master_starting_point():
    readme = _read(Path("README.md"))

    for required_text in (
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_INDEX.md",
        "master starting point/control index",
        "formal evidence review gates",
        "decision records",
        "readiness checklists",
        "status transitions",
        "governed ingestion planning",
        "recapture planning",
        "promotion planning",
        "promotion execution guardrails",
        "Tax / PAYG and Imports / Actuals remain `BASELINE_REQUIRED` and `NOT_REVIEWED`",
        "governed ingestion permitted: No",
        "recapture permitted: No",
        "promotion permitted: No",
    ):
        assert required_text in readme


def test_formal_evidence_control_readme_prompt_is_preserved():
    assert FORMAL_EVIDENCE_CONTROL_README_PROMPT.exists()

    prompt = _read(FORMAL_EVIDENCE_CONTROL_README_PROMPT)

    for required_text in (
        "# Codex Prompt — Minerva Formal Evidence Control README v0.1",
        "Mode: Documentation/control-readme hardening only",
        "Do not approve DB writes, migrations, corpus mutation, live LLM calls, endpoint changes, runtime changes, generated artefact commits, ledger promotion, review approval, recapture, or governed ingestion.",
        "Both domains now have complete NOT_REVIEWED control chains.",
        "Chat is not the durable source of truth.",
        "docs/evaluation/source_evidence_drafts/README.md",
        "tests/test_domain_baseline_capture_batch.py",
        "docs/codex_prompts/2026-05-15_minerva_formal_evidence_control_readme_v0_1.md",
        "→ REVIEWED_READY_FOR_INGESTION only after explicit review",
        "→ possible ledger promotion",
    ):
        assert required_text in prompt


def test_formal_evidence_review_readiness_checklist_prompt_is_preserved():
    assert FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST_PROMPT.exists()

    prompt = _read(FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST_PROMPT)

    for required_text in (
        "# Codex Prompt - Minerva Formal Evidence Review Readiness Checklist v0.1",
        "Mode: Documentation/control-checklist hardening only",
        "Do not approve DB writes, migrations, corpus mutation, live LLM calls, endpoint changes, runtime changes, generated artefact commits, ledger promotion, review approval, recapture, or governed ingestion.",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST.md",
        "tests/test_domain_baseline_capture_batch.py",
        "docs/codex_prompts/2026-05-15_minerva_formal_evidence_review_readiness_checklist_v0_1.md",
        "`FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST.md` exists.",
        "A checklist alone does not change review status.",
        "Tax / PAYG remains BASELINE_REQUIRED.",
        "Imports / Actuals remains BASELINE_REQUIRED.",
    ):
        assert required_text in prompt


def test_formal_evidence_review_status_transition_runbook_prompt_is_preserved():
    assert FORMAL_EVIDENCE_REVIEW_STATUS_TRANSITION_RUNBOOK_PROMPT.exists()

    prompt = _read(FORMAL_EVIDENCE_REVIEW_STATUS_TRANSITION_RUNBOOK_PROMPT)

    for required_text in (
        "# Codex Prompt - Minerva Formal Evidence Review Status Transition Runbook v0.1",
        "Mode: Documentation/control-runbook hardening only",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_STATUS_TRANSITION_RUNBOOK.md",
        "tests/test_domain_baseline_capture_batch.py",
        "a separate explicit review slice",
        "a filled decision record",
        "reviewer identity",
        "review date",
        "reviewer rationale",
        "doctrine review",
        "implementation-state review",
        "evidence-gap review",
        "non-overclaiming review",
        "`REVIEWED_READY_FOR_INGESTION` permits planning a future governed ingestion slice only",
        "Do not change ledger counts.",
        "Do not mark any domain `REVIEWED_READY_FOR_INGESTION`.",
        "Do not mark any domain `BASELINE_ALREADY_EXISTS`.",
    ):
        assert required_text in prompt


def test_formal_evidence_governed_ingestion_planning_runbook_prompt_is_preserved():
    assert FORMAL_EVIDENCE_GOVERNED_INGESTION_PLANNING_RUNBOOK_PROMPT.exists()

    prompt = _read(FORMAL_EVIDENCE_GOVERNED_INGESTION_PLANNING_RUNBOOK_PROMPT)

    for required_text in (
        "# Codex Prompt - Minerva Formal Evidence Governed Ingestion Planning Runbook v0.1",
        "Mode: Documentation/control-runbook hardening only",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_GOVERNED_INGESTION_PLANNING_RUNBOOK.md",
        "tests/test_domain_baseline_capture_batch.py",
        "latest decision record selected status `REVIEWED_READY_FOR_INGESTION`",
        "reviewer identity present",
        "reviewer date present",
        "reviewer rationale present",
        "reviewed source artefacts identified",
        "ingestion scope documented",
        "target corpus location documented",
        "mutation risk documented",
        "rollback/restore plan documented",
        "generated artefact policy documented",
        "recapture plan documented",
        "tests planned before corpus mutation",
        "Do not change ledger counts.",
        "Do not mark any domain `REVIEWED_READY_FOR_INGESTION`.",
        "Do not mark any domain `BASELINE_ALREADY_EXISTS`.",
    ):
        assert required_text in prompt


def test_formal_evidence_recapture_planning_runbook_prompt_is_preserved():
    assert FORMAL_EVIDENCE_RECAPTURE_PLANNING_RUNBOOK_PROMPT.exists()

    prompt = _read(FORMAL_EVIDENCE_RECAPTURE_PLANNING_RUNBOOK_PROMPT)

    for required_text in (
        "# Codex Prompt - Minerva Formal Evidence Recapture Planning Runbook v0.1",
        "Mode: Documentation/control-runbook hardening only",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_RECAPTURE_PLANNING_RUNBOOK.md",
        "tests/test_domain_baseline_capture_batch.py",
        "latest decision record selected status `REVIEWED_READY_FOR_INGESTION`",
        "separate governed ingestion slice completed",
        "corpus mutation evidence recorded",
        "ingested source artefacts identified",
        "generated artefact policy documented",
        "benchmark manifest identified",
        "corpus coverage command identified",
        "answer-gap command identified",
        "expected evidence groups identified",
        "regression guardrails documented",
        "rollback/restore notes preserved",
        "does not run benchmark",
        "does not run corpus coverage",
        "does not run answer-gap reporting",
        "Do not change ledger counts.",
        "Do not mark any domain `REVIEWED_READY_FOR_INGESTION`.",
        "Do not mark any domain `BASELINE_ALREADY_EXISTS`.",
    ):
        assert required_text in prompt


def test_formal_evidence_promotion_planning_runbook_prompt_is_preserved():
    assert FORMAL_EVIDENCE_PROMOTION_PLANNING_RUNBOOK_PROMPT.exists()

    prompt = _read(FORMAL_EVIDENCE_PROMOTION_PLANNING_RUNBOOK_PROMPT)

    for required_text in (
        "# Codex Prompt - Minerva Formal Evidence Promotion Planning Runbook v0.1",
        "Mode: Documentation/control-runbook hardening only",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_PROMOTION_PLANNING_RUNBOOK.md",
        "tests/test_domain_baseline_capture_batch.py",
        "latest decision record selected status `REVIEWED_READY_FOR_INGESTION`",
        "separate governed ingestion slice completed",
        "recapture slice completed",
        "benchmark command results recorded",
        "corpus coverage command results recorded",
        "answer-gap command results recorded",
        "no unresolved `MISSING` evidence groups unless accepted with documented rationale",
        "benchmark pass/failure status documented",
        "answer-gap `GOOD` or accepted under documented policy",
        "generated artefact policy satisfied",
        "ledger update plan documented",
        "rollback/supersession notes preserved",
        "does not run benchmark",
        "does not run corpus coverage",
        "does not run answer-gap reporting",
        "does not promote a baseline",
        "Do not change ledger counts.",
        "Do not mark any domain `REVIEWED_READY_FOR_INGESTION`.",
        "Do not mark any domain `BASELINE_ALREADY_EXISTS`.",
    ):
        assert required_text in prompt


def test_formal_evidence_promotion_execution_guardrail_prompt_is_preserved():
    assert FORMAL_EVIDENCE_PROMOTION_EXECUTION_GUARDRAIL_PROMPT.exists()

    prompt = _read(FORMAL_EVIDENCE_PROMOTION_EXECUTION_GUARDRAIL_PROMPT)

    for required_text in (
        "# Codex Prompt - Minerva Formal Evidence Promotion Execution Guardrail v0.1",
        "Mode: Documentation/control-guardrail hardening only",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_PROMOTION_EXECUTION_GUARDRAIL.md",
        "tests/test_domain_baseline_capture_batch.py",
        "latest decision record selected status `REVIEWED_READY_FOR_INGESTION`",
        "governed ingestion slice completed",
        "corpus mutation evidence recorded",
        "recapture slice completed",
        "benchmark results recorded",
        "corpus coverage results recorded",
        "answer-gap results recorded",
        "benchmark pass/failure status accepted",
        "no unresolved `MISSING` evidence groups unless accepted with written rationale",
        "answer-gap `GOOD` or accepted under documented policy",
        "generated artefact policy satisfied",
        "reviewer identity/date/rationale recorded",
        "ledger update diff planned",
        "rollback/supersession notes preserved",
        "explicit user approval for ledger promotion",
        "does not run benchmark",
        "does not run corpus coverage",
        "does not run answer-gap reporting",
        "does not promote a baseline",
        "Do not change ledger counts.",
        "Do not mark any domain `REVIEWED_READY_FOR_INGESTION`.",
        "Do not mark any domain `BASELINE_ALREADY_EXISTS`.",
    ):
        assert required_text in prompt


def test_formal_evidence_control_index_prompt_is_preserved():
    assert FORMAL_EVIDENCE_CONTROL_INDEX_PROMPT.exists()

    prompt = _read(FORMAL_EVIDENCE_CONTROL_INDEX_PROMPT)

    for required_text in (
        "# Codex Prompt - Minerva Formal Evidence Control Index v0.1",
        "Mode: Documentation/control-index hardening only",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_INDEX.md",
        "tests/test_domain_baseline_capture_batch.py",
        "evidence gap identified",
        "-> formal evidence gap plan",
        "-> formal source-evidence draft",
        "-> formal evidence review gate",
        "-> review-gate index",
        "-> decision record template",
        "-> filled decision record",
        "-> decision-record index",
        "-> review readiness checklist",
        "-> status transition runbook",
        "-> governed ingestion planning",
        "-> recapture planning",
        "-> promotion planning",
        "-> promotion execution guardrail",
        "-> possible explicit promotion slice only after final preflight",
        "governed ingestion permitted: No",
        "recapture permitted: No",
        "promotion permitted: No",
        "promotion execution permitted: No",
        "no control artefact by itself mutates corpus, runs benchmark, runs corpus coverage, runs answer-gap reporting, changes runtime, changes ledger counts, or promotes a baseline",
        "Do not change ledger counts.",
        "Do not mark any domain `REVIEWED_READY_FOR_INGESTION`.",
        "Do not mark any domain `BASELINE_ALREADY_EXISTS`.",
    ):
        assert required_text in prompt


def test_historical_knowledge_control_index_prompt_is_preserved():
    assert HISTORICAL_KNOWLEDGE_CONTROL_INDEX_PROMPT.exists()

    prompt = _read(HISTORICAL_KNOWLEDGE_CONTROL_INDEX_PROMPT)

    for required_text in (
        "# Codex Prompt - Minerva Historical Knowledge Control Index v0.1",
        "Mode: Documentation/control-model hardening only",
        "docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md",
        "docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_GAP_REGISTER.md",
        "docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_TIERING_MODEL.md",
        "docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_PROCESS.md",
        "pre-control-model historical knowledge is incomplete",
        "Tier 1 code and tests as highest authority for implemented state",
        "Tier 2 developer logs, hardening logs, and platform doctrine",
        "Tier 3 historical chats and continuance prompts",
        "Historical chats must not be ingested directly as truth",
        "IMPLEMENTED_AND_TESTED",
        "UNCERTAIN_REQUIRES_REVIEW",
        "Only later consider governed ingestion",
        "does not mutate corpus",
        "does not run live LLM",
        "does not connect Code Evidence",
        "does not change runtime behaviour",
        "does not promote baselines",
        "does not change ledger counts",
        "Do not mark any domain `REVIEWED_READY_FOR_INGESTION`.",
        "Do not mark any domain `BASELINE_ALREADY_EXISTS`.",
        "Tax / PAYG and Imports / Actuals remain governed by the formal evidence control model",
    ):
        assert required_text in prompt


def test_historical_source_inventory_template_prompt_is_preserved():
    assert HISTORICAL_SOURCE_INVENTORY_TEMPLATE_PROMPT.exists()

    prompt = _read(HISTORICAL_SOURCE_INVENTORY_TEMPLATE_PROMPT)

    for required_text in (
        "# Codex Prompt - Minerva Historical Source Inventory Template v0.1",
        "Mode: Documentation/control-model hardening only",
        "docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_INVENTORY_TEMPLATE.md",
        "docs/evaluation/historical_knowledge/HISTORICAL_DEVELOPER_LOG_DOCTRINE_INVENTORY_TEMPLATE.md",
        "docs/evaluation/historical_knowledge/HISTORICAL_CHAT_CONTINUANCE_INVENTORY_TEMPLATE.md",
        "docs/evaluation/historical_knowledge/HISTORICAL_CODE_EVIDENCE_INVENTORY_TEMPLATE.md",
        "Source title",
        "Source type",
        "Source tier",
        "Date or date range",
        "Repository/domain",
        "Related commits if known",
        "Related developer log or doctrine reference",
        "Implementation-state classification",
        "Evidence confidence",
        "Supersession risk",
        "Backlog/doctrine/runtime distinction",
        "Review required",
        "Ingestion permitted",
        "IMPLEMENTED_AND_TESTED",
        "UNCERTAIN_REQUIRES_REVIEW",
        "curated decision/rationale sources requiring review",
        "raw historical source material, not final truth",
        "code/tests as highest authority for implemented state",
        "does not mutate corpus",
        "does not ingest sources",
        "does not connect Code Evidence",
        "does not run live LLM",
        "does not change runtime behaviour",
        "does not promote baselines",
        "does not change ledger counts",
    ):
        assert required_text in prompt


def test_formal_evidence_control_index_readme_link_prompt_is_preserved():
    assert FORMAL_EVIDENCE_CONTROL_INDEX_README_LINK_PROMPT.exists()

    prompt = _read(FORMAL_EVIDENCE_CONTROL_INDEX_README_LINK_PROMPT)

    for required_text in (
        "# Codex Prompt - Minerva Formal Evidence Control Index README Link v0.1",
        "Mode: Documentation/navigation hardening only",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_INDEX.md",
        "master starting point/control index",
        "review gates",
        "decision records",
        "readiness checklists",
        "status transitions",
        "governed ingestion planning",
        "recapture planning",
        "promotion planning",
        "promotion execution guardrails",
        "Tax / PAYG",
        "Imports / Actuals",
        "baseline status: `BASELINE_REQUIRED`",
        "decision status: `NOT_REVIEWED`",
        "governed ingestion permitted: No",
        "recapture permitted: No",
        "promotion permitted: No",
        "Do not change ledger counts.",
        "Do not mark any domain `REVIEWED_READY_FOR_INGESTION`.",
        "Do not mark any domain `BASELINE_ALREADY_EXISTS`.",
    ):
        assert required_text in prompt


def test_formal_evidence_control_index_root_readme_link_prompt_is_preserved():
    assert FORMAL_EVIDENCE_CONTROL_INDEX_ROOT_README_LINK_PROMPT.exists()

    prompt = _read(FORMAL_EVIDENCE_CONTROL_INDEX_ROOT_README_LINK_PROMPT)

    for required_text in (
        "# Codex Prompt - Minerva Formal Evidence Control Index Root README Link v0.1",
        "Mode: Documentation/navigation hardening only",
        "README.md",
        "docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_INDEX.md",
        "master starting point/control index",
        "formal evidence review gates",
        "decision records",
        "readiness checklists",
        "status transitions",
        "governed ingestion planning",
        "recapture planning",
        "promotion planning",
        "promotion execution guardrails",
        "Tax / PAYG",
        "Imports / Actuals",
        "baseline status: `BASELINE_REQUIRED`",
        "decision status: `NOT_REVIEWED`",
        "governed ingestion permitted: No",
        "recapture permitted: No",
        "promotion permitted: No",
        "Do not change ledger counts.",
        "Do not mark any domain `REVIEWED_READY_FOR_INGESTION`.",
        "Do not mark any domain `BASELINE_ALREADY_EXISTS`.",
    ):
        assert required_text in prompt


def test_tax_payg_review_notes_reference_review_gate_and_preserve_not_promoted_state():
    notes_path = BASELINE_ROOT / "tax_payg" / "v0_1" / "REVIEW_NOTES.md"
    notes = _read(notes_path)

    assert "TAX_PAYG_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md" in notes
    assert "current review status `NOT_REVIEWED`" in notes
    assert "governed corpus ingestion remains blocked until the gate is marked `REVIEWED_READY_FOR_INGESTION`" in notes
    assert "Tax / PAYG as `BASELINE_REQUIRED`" in notes
    assert "Do not promote Tax / PAYG" in notes
    assert "no ledger promotion" in notes


def test_contact_payroll_history_baseline_pack_records_captured_ready_results_with_failures():
    metadata = CONTACT_PAYROLL_HISTORY_CAPTURED_DOMAIN
    pack_path = BASELINE_ROOT / "contact_payroll_history" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    assert metadata["name"] in combined
    assert metadata["runbook"] in combined
    assert metadata["manifest"] in combined
    assert metadata["scan"] in combined
    assert metadata["gap"] in combined
    assert "DB readiness result: `READY`" in combined
    assert "Result status: `COMPLETED_WITH_FAILURES`" in combined
    assert "Total: 7" in combined
    assert "Passed: 5" in combined
    assert "Failed: 2" in combined
    assert "Audit/chat rows created: false" in combined
    assert "contact-payroll-history-rich-answer" in combined
    assert "contact-payroll-history-retro-replay-correction" in combined
    assert "combination of benchmark answer-term expectation gap and source-evidence/matched-phrase drift" in combined
    assert "with corpus gap present for `gross_to_net_history`" in combined
    assert "Evidence groups: 11" in combined
    assert "`STRONG`: 7" in combined
    assert "`WEAK`: 3" in combined
    assert "`MISSING`: 1" in combined
    assert "`gross_to_net_history`" in combined
    assert "`current_and_historical_payroll_output`" in combined
    assert "`retro_replay_and_correction_relationship`" in combined
    assert "`outstanding_hardening`" in combined
    assert "Overall status: `NEEDS_REFINEMENT`" in combined
    assert "`KEEP`: 7" in combined
    assert "`IMPROVE_SYNTHESIS`: 1" in combined
    assert "`IMPROVE_RETRIEVAL_TERMS`: 2" in combined
    assert "`ADD_FORMAL_SOURCE_EVIDENCE_LATER`: 1" in combined
    assert "Report type: `CONTACT_PAYROLL_HISTORY_ANSWER_GAP_REPORT`" in combined
    assert "Source coverage plan: `CONTACT_PAYROLL_HISTORY`" in combined
    assert "Generated artefact committed: no" in combined
    assert "Code Evidence answer integration: no" in combined
    assert "BLOCKED_DATABASE_CONNECTION" not in combined


def test_decision_story_baseline_pack_records_captured_ready_results_with_failures():
    metadata = DECISION_STORY_CAPTURED_DOMAIN
    pack_path = BASELINE_ROOT / "decision_story" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    assert metadata["name"] in combined
    assert metadata["runbook"] in combined
    assert metadata["manifest"] in combined
    assert metadata["scan"] in combined
    assert metadata["gap"] in combined
    assert "DB readiness result: `READY`" in combined
    assert "Result status: `COMPLETED_WITH_FAILURES`" in combined
    assert "Total: 7" in combined
    assert "Passed: 6" in combined
    assert "Failed: 1" in combined
    assert "Audit/chat rows created: false" in combined
    assert "decision-story-rich-answer" in combined
    assert "Source snippets/matched phrases did not contain all expected terms: Decision Story, DecisionEvidenceIndex, why a treatment" in combined
    assert "benchmark/source-evidence check or retrieval/source-matched-phrase drift, not corpus gap" in combined
    assert "Evidence groups: 10" in combined
    assert "`STRONG`: 10" in combined
    assert "`WEAK`: 0" in combined
    assert "`MISSING`: 0" in combined
    assert "Overall status: `GOOD`" in combined
    assert "`KEEP`: 10" in combined
    assert "Report type: `DECISION_STORY_ANSWER_GAP_REPORT`" in combined
    assert "Source coverage plan: `DECISION_STORY`" in combined
    assert "Keep current Decision Story retrieval terms and answer synthesis under benchmark watch" in combined
    assert "Generated artefact committed: no" in combined
    assert "Code Evidence answer integration: no" in combined
    assert "BLOCKED_DATABASE_CONNECTION" not in combined


def test_finalisation_readiness_baseline_pack_records_captured_ready_results():
    metadata = FINALISATION_READINESS_CAPTURED_DOMAIN
    pack_path = BASELINE_ROOT / "finalisation_readiness" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    assert metadata["name"] in combined
    assert metadata["runbook"] in combined
    assert metadata["manifest"] in combined
    assert metadata["scan"] in combined
    assert metadata["gap"] in combined
    assert "DB readiness result: `READY`" in combined
    assert "Result status: `COMPLETED`" in combined
    assert "Total: 12" in combined
    assert "Passed: 12" in combined
    assert "Failed: 0" in combined
    assert "Audit/chat rows created: false" in combined
    assert "Evidence groups: 12" in combined
    assert "`STRONG`: 11" in combined
    assert "`WEAK`: 1" in combined
    assert "`MISSING`: 0" in combined
    assert "Overall status: `NEEDS_REFINEMENT`" in combined
    assert "`KEEP`: 11" in combined
    assert "`IMPROVE_SYNTHESIS`: 1" in combined
    assert "Report type: `FINALISATION_READINESS_ANSWER_GAP_REPORT`" in combined
    assert "Source coverage plan: `FINALISATION_READINESS`" in combined
    assert "`purpose_and_operator_meaning` -> `IMPROVE_SYNTHESIS`" in combined
    assert "Tighten Finalisation Readiness answer synthesis for weak core groups while keeping status caveats" in combined
    assert "Generated artefact committed: no" in combined
    assert "Code Evidence answer integration: no" in combined
    assert "BLOCKED_DATABASE_CONNECTION" not in combined


def test_payroll_output_baseline_pack_records_captured_ready_results_with_failures():
    metadata = PAYROLL_OUTPUT_CAPTURED_DOMAIN
    pack_path = BASELINE_ROOT / "payroll_output" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    assert metadata["name"] in combined
    assert metadata["runbook"] in combined
    assert metadata["manifest"] in combined
    assert metadata["scan"] in combined
    assert metadata["gap"] in combined
    assert "DB readiness result: `READY`" in combined
    assert "Result status: `COMPLETED_WITH_FAILURES`" in combined
    assert "Total: 7" in combined
    assert "Passed: 6" in combined
    assert "Failed: 1" in combined
    assert "Audit/chat rows created: false" in combined
    assert "payroll-output-rich-answer" in combined
    assert "benchmark/source-evidence check or retrieval/source-matched-phrase drift, not corpus gap" in combined
    assert "Evidence groups: 11" in combined
    assert "`STRONG`: 10" in combined
    assert "`WEAK`: 1" in combined
    assert "`MISSING`: 0" in combined
    assert "Overall status: `NEEDS_REFINEMENT`" in combined
    assert "`KEEP`: 10" in combined
    assert "`IMPROVE_SYNTHESIS`: 1" in combined
    assert "Report type: `PAYROLL_OUTPUT_ANSWER_GAP_REPORT`" in combined
    assert "Source coverage plan: `PAYROLL_OUTPUT`" in combined
    assert "`worker_level_output` -> `IMPROVE_SYNTHESIS`" in combined
    assert "Tighten Payroll Output answer synthesis for weak core groups while keeping status caveats" in combined
    assert "Generated artefact committed: no" in combined
    assert "Code Evidence answer integration: no" in combined
    assert "BLOCKED_DATABASE_CONNECTION" not in combined


def test_rate_source_rate_story_baseline_pack_records_captured_ready_results_with_failures():
    metadata = RATE_SOURCE_RATE_STORY_CAPTURED_DOMAIN
    pack_path = BASELINE_ROOT / "ratesource_rate_story" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    assert metadata["name"] in combined
    assert metadata["runbook"] in combined
    assert metadata["manifest"] in combined
    assert metadata["scan"] in combined
    assert metadata["gap"] in combined
    assert "DB readiness result: `READY`" in combined
    assert "Result status: `COMPLETED_WITH_FAILURES`" in combined
    assert "Total: 6" in combined
    assert "Passed: 5" in combined
    assert "Failed: 1" in combined
    assert "Audit/chat rows created: false" in combined
    assert "rate-source-rate-story-rich-answer" in combined
    assert "Source snippets/matched phrases did not contain all expected terms: RateSource, Rate Story, rate amount" in combined
    assert "benchmark/source-evidence check or retrieval/source-matched-phrase drift, not corpus gap" in combined
    assert "Evidence groups: 11" in combined
    assert "`STRONG`: 10" in combined
    assert "`WEAK`: 1" in combined
    assert "`MISSING`: 0" in combined
    assert "Overall status: `NEEDS_REFINEMENT`" in combined
    assert "`KEEP`: 10" in combined
    assert "`IMPROVE_SYNTHESIS`: 1" in combined
    assert "Report type: `RATE_SOURCE_RATE_STORY_ANSWER_GAP_REPORT`" in combined
    assert "Source coverage plan: `RATE_SOURCE_RATE_STORY`" in combined
    assert "`rate_source_evidence_index` -> `IMPROVE_SYNTHESIS`" in combined
    assert "Tighten RateSource / Rate Story answer synthesis for weak core groups while keeping status caveats" in combined
    assert "Generated artefact committed: no" in combined
    assert "Code Evidence answer integration: no" in combined
    assert "BLOCKED_DATABASE_CONNECTION" not in combined


def test_core_payroll_explanation_blocked_packs_are_diagnostic_only_not_runtime_truth():
    for slug in ("decision_story",):
        pack_path = BASELINE_ROOT / slug / "v0_1"
        combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

        assert "diagnostic-only" in combined
        assert "not operational truth" in combined
        assert "does not mutate corpus" in combined
        assert "change routing" in combined
        assert "change answer generation" in combined
        assert "call live LLM" in combined
        assert "ingest operational JSON" in combined
        assert "connect Code Evidence" in combined
        assert "create DB schema or migrations" in combined
        assert "add endpoints or UI" in combined
        assert "change workforce-platform" in combined


def test_six_domain_maturity_closeout_records_outcomes_without_changing_numbers():
    closeout = _read(MATURITY_CLOSEOUT_PATH)

    assert "Original v0.3 history records 5 total / 4 passed / 1 failed" in closeout
    assert "later rerun records 5 total / 5 passed / 0 failed" in closeout
    assert "| Payroll Bases & Totals | Passed baseline with refinement | 6 total / 6 passed / 0 failed | STRONG=8, WEAK=1, MISSING=0 | NEEDS_REFINEMENT |" in closeout
    assert "| PayRun Admin Queue | Captured-with-failures baseline | 8 total / 6 passed / 2 failed | STRONG=11, WEAK=0, MISSING=0 | GOOD; 11 KEEP actions |" in closeout
    assert "| Movement Review | Passed baseline | 8 total / 8 passed / 0 failed | STRONG=11, WEAK=0, MISSING=0 | GOOD; 11 KEEP actions |" in closeout
    assert "| Gross-to-Net | Captured-with-failures baseline | 6 total / 5 passed / 1 failed | STRONG=10, WEAK=0, MISSING=0 | GOOD; 10 KEEP actions |" in closeout
    assert "| Annual Leave / Leave Management | Passed baseline | 1 total / 1 passed / 0 failed | STRONG=7, WEAK=0, MISSING=0 | GOOD; 7 KEEP actions |" in closeout


def test_six_domain_maturity_closeout_records_failure_and_refinement_classifications():
    closeout = _read(MATURITY_CLOSEOUT_PATH)

    assert "Payroll Bases & Totals remains `NEEDS_REFINEMENT`" in closeout
    assert "weak `outstanding_hardening` coverage maps to `IMPROVE_RETRIEVAL_TERMS`" in closeout
    assert "payrun-admin-queue-rich-answer" in closeout
    assert "payrun-admin-queue-cleanliness-assurance" in closeout
    assert "PayRun Admin Queue failures are not corpus gaps" in closeout
    assert "gross-to-net-current-effective-worker-story" in closeout
    assert "Gross-to-Net failure is not a corpus gap" in closeout
    assert "Do not weaken benchmark expectations" in closeout


def test_six_domain_maturity_closeout_records_transient_json_policy_and_guardrails():
    closeout = _read(MATURITY_CLOSEOUT_PATH)

    assert "Generated JSON outputs from benchmark, corpus coverage or answer-gap commands are transient evaluation materials" in closeout
    assert "not durable checked-in artefacts unless explicitly versioned" in closeout
    assert "operational JSON ingestion" in closeout
    assert "Code Evidence answer integration" in closeout
    assert "live LLM calls" in closeout
    assert "corpus mutation" in closeout
    assert "DB or schema migration" in closeout
    assert "endpoints or UI" in closeout
    assert "workforce-platform changes" in closeout
    assert "No operational JSON ingestion occurred" in closeout
    assert "No Code Evidence answer integration occurred" in closeout
    assert "No live LLM call occurred" in closeout
    assert "No corpus mutation occurred" in closeout
    assert "No DB or schema migration occurred" in closeout
    assert "No endpoint or UI change occurred" in closeout
    assert "No workforce-platform change occurred" in closeout
    assert "should be small" in closeout
    assert "not attempt all remaining 25 `BASELINE_REQUIRED` domains at once" in closeout


def test_four_domain_batch_closeout_records_all_domain_outcomes_and_ledger_counts():
    closeout = _read(CLOSEOUT_PATH)

    assert "`BASELINE_REQUIRED`: 25" in closeout
    assert "`BASELINE_ALREADY_EXISTS`: 5" in closeout
    assert "`RUNBOOK_OUTSTANDING`: 1" in closeout
    assert "Baseline already existing: Worker Story; Payroll Bases & Totals; PayRun Admin Queue; Movement Review; Gross-to-Net" in closeout
    assert "Annual Leave / Leave Management remains `RUNBOOK_OUTSTANDING`" in closeout

    assert "| Payroll Bases & Totals | Passed baseline | 6 total / 6 passed / 0 failed | STRONG=8, WEAK=1, MISSING=0 | NEEDS_REFINEMENT |" in closeout
    assert "| PayRun Admin Queue | Captured-with-failures baseline | 8 total / 6 passed / 2 failed | STRONG=11, WEAK=0, MISSING=0 | GOOD; 11 KEEP actions |" in closeout
    assert "| Movement Review | Passed baseline | 8 total / 8 passed / 0 failed | STRONG=11, WEAK=0, MISSING=0 | GOOD; 11 KEEP actions |" in closeout
    assert "| Gross-to-Net | Captured-with-failures baseline | 6 total / 5 passed / 1 failed | STRONG=10, WEAK=0, MISSING=0 | GOOD; 10 KEEP actions |" in closeout


def test_four_domain_batch_closeout_preserves_failure_and_refinement_classifications():
    closeout = _read(CLOSEOUT_PATH)

    assert "Weak `outstanding_hardening` coverage requires retrieval-term hardening" in closeout
    assert "`outstanding_hardening` -> `IMPROVE_RETRIEVAL_TERMS`" in closeout
    assert "This is not a corpus gap" in closeout
    assert "payrun-admin-queue-rich-answer" in closeout
    assert "payrun-admin-queue-cleanliness-assurance" in closeout
    assert "benchmark/source-evidence check or retrieval/source-matched-phrase drift, not corpus gap" in closeout
    assert "gross-to-net-current-effective-worker-story" in closeout
    assert "benchmark answer-term expectation drift, not corpus gap" in closeout
    assert "Do not weaken benchmark expectations" in closeout
    assert "Movement Review is the clean baseline in this batch" in closeout


def test_four_domain_batch_closeout_records_diagnostic_boundaries_and_json_policy():
    closeout = _read(CLOSEOUT_PATH)

    assert "operational JSON ingestion" in closeout
    assert "Code Evidence answer integration" in closeout
    assert "live LLM calls" in closeout
    assert "corpus mutation" in closeout
    assert "DB or schema migration" in closeout
    assert "endpoints or UI" in closeout
    assert "workforce-platform changes" in closeout
    assert "Generated JSON outputs from benchmark, corpus coverage or answer-gap commands are transient evaluation materials" in closeout
    assert "not durable checked-in artefacts unless explicitly versioned" in closeout


def test_payroll_bases_baseline_pack_records_captured_ready_results():
    metadata = CAPTURED_BATCH_DOMAINS["payroll_bases_totals"]
    pack_path = BASELINE_ROOT / "payroll_bases_totals" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    assert metadata["name"] in combined
    assert metadata["runbook"] in combined
    assert metadata["manifest"] in combined
    assert metadata["scan"] in combined
    assert metadata["gap"] in combined
    assert "DB readiness result: `READY`" in combined
    assert "Result status: `COMPLETED`" in combined
    assert "Total: 6" in combined
    assert "Passed: 6" in combined
    assert "Failed: 0" in combined
    assert "Audit/chat rows created: false" in combined
    assert "`STRONG`: 8" in combined
    assert "`WEAK`: 1" in combined
    assert "`MISSING`: 0" in combined
    assert "Overall status: `NEEDS_REFINEMENT`" in combined
    assert "`KEEP`: 8" in combined
    assert "`IMPROVE_RETRIEVAL_TERMS`: 1" in combined
    assert "`outstanding_hardening` -> `IMPROVE_RETRIEVAL_TERMS`" in combined


def test_payrun_admin_queue_baseline_pack_records_captured_ready_results_with_failures():
    metadata = CAPTURED_BATCH_DOMAINS["payrun_admin_queue"]
    pack_path = BASELINE_ROOT / "payrun_admin_queue" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    assert metadata["name"] in combined
    assert metadata["runbook"] in combined
    assert metadata["manifest"] in combined
    assert metadata["scan"] in combined
    assert metadata["gap"] in combined
    assert "DB readiness result: `READY`" in combined
    assert "Result status: `COMPLETED_WITH_FAILURES`" in combined
    assert "Total: 8" in combined
    assert "Passed: 6" in combined
    assert "Failed: 2" in combined
    assert "Audit/chat rows created: false" in combined
    assert "payrun-admin-queue-rich-answer" in combined
    assert "payrun-admin-queue-cleanliness-assurance" in combined
    assert "benchmark/source-evidence check or retrieval/source-matched-phrase drift, not corpus gap" in combined
    assert "`STRONG`: 11" in combined
    assert "`WEAK`: 0" in combined
    assert "`MISSING`: 0" in combined
    assert "Overall status: `GOOD`" in combined
    assert "`KEEP`: 11" in combined
    assert "Generated artefact committed: no" in combined
    assert "BLOCKED_DATABASE_CONNECTION" not in combined


def test_movement_review_baseline_pack_records_captured_ready_results():
    metadata = CAPTURED_BATCH_DOMAINS["movement_review"]
    pack_path = BASELINE_ROOT / "movement_review" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    assert metadata["name"] in combined
    assert metadata["runbook"] in combined
    assert metadata["manifest"] in combined
    assert metadata["scan"] in combined
    assert metadata["gap"] in combined
    assert "DB readiness result: `READY`" in combined
    assert "Result status: `COMPLETED`" in combined
    assert "Total: 8" in combined
    assert "Passed: 8" in combined
    assert "Failed: 0" in combined
    assert "Audit/chat rows created: false" in combined
    assert "`STRONG`: 11" in combined
    assert "`WEAK`: 0" in combined
    assert "`MISSING`: 0" in combined
    assert "Overall status: `GOOD`" in combined
    assert "`KEEP`: 11" in combined
    assert "Report type: `MOVEMENT_REVIEW_ANSWER_GAP_REPORT`" in combined
    assert "Source coverage plan: `MOVEMENT_REVIEW`" in combined
    assert "Keep current Movement Review retrieval terms and answer synthesis under benchmark watch" in combined
    assert "Generated artefact committed: no" in combined
    assert "BLOCKED_DATABASE_CONNECTION" not in combined


def test_gross_to_net_baseline_pack_records_captured_ready_results_with_failures():
    metadata = CAPTURED_BATCH_DOMAINS["gross_to_net"]
    pack_path = BASELINE_ROOT / "gross_to_net" / "v0_1"
    combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

    assert metadata["name"] in combined
    assert metadata["runbook"] in combined
    assert metadata["manifest"] in combined
    assert metadata["scan"] in combined
    assert metadata["gap"] in combined
    assert "DB readiness result: `READY`" in combined
    assert "Result status: `COMPLETED_WITH_FAILURES`" in combined
    assert "Total: 6" in combined
    assert "Passed: 5" in combined
    assert "Failed: 1" in combined
    assert "Audit/chat rows created: false" in combined
    assert "gross-to-net-current-effective-worker-story" in combined
    assert "benchmark answer-term expectation drift, not corpus gap" in combined
    assert "`STRONG`: 10" in combined
    assert "`WEAK`: 0" in combined
    assert "`MISSING`: 0" in combined
    assert "Overall status: `GOOD`" in combined
    assert "`KEEP`: 10" in combined
    assert "Report type: `GROSS_TO_NET_ANSWER_GAP_REPORT`" in combined
    assert "Source coverage plan: `GROSS_TO_NET`" in combined
    assert "Keep current Gross-to-Net retrieval terms and answer synthesis under benchmark watch" in combined
    assert "Generated artefact committed: no" in combined
    assert "BLOCKED_DATABASE_CONNECTION" not in combined


def test_batch_baseline_packs_are_diagnostic_only_not_runtime_truth():
    for slug in CAPTURED_BATCH_DOMAINS:
        pack_path = BASELINE_ROOT / slug / "v0_1"
        combined = "\n".join(_read(pack_path / file_name) for file_name in REQUIRED_FILES)

        assert "diagnostic-only" in combined
        assert "not operational truth" in combined
        assert "does not mutate corpus" in combined
        assert "does not change routing" in combined
        assert "does not change answer generation" in combined
        assert "does not call live LLM" in combined
        assert "does not ingest operational JSON" in combined
        assert "does not connect Code Evidence" in combined
        assert "does not create DB schema or migrations" in combined
        assert "does not add endpoints or UI" in combined
        assert "does not change workforce-platform" in combined


def test_ledger_counts_remain_honest_for_captured_batch():
    ledger = _read(LEDGER_PATH)

    assert "`BASELINE_REQUIRED`: 17" in ledger
    assert "`BASELINE_ALREADY_EXISTS`: 14" in ledger
    assert "`RUNBOOK_OUTSTANDING`: 0" in ledger
    assert "Domains with baseline already existing: Worker Story; Payroll Bases & Totals; PayRun Admin Queue; Movement Review; Gross-to-Net; Annual Leave / Leave Management; Finalisation Readiness; Payroll Output; RateSource / Rate Story; Decision Story; Contact Payroll History; ObjectTime / Source Truth; Process Periods / PayRun Lifecycle; Comparison / Remediation" in ledger
    assert "Annual Leave / Leave Management" in ledger
    assert "Movement Review now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "Gross-to-Net now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "benchmark 6 total, 5 passed, 1 failed" in ledger
    assert "gross-to-net-current-effective-worker-story" in ledger
    assert "Failure is benchmark answer-term expectation drift, not corpus gap" in ledger
    assert "| PayRun Admin Queue | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "| Movement Review | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "BASELINE_ALREADY_EXISTS | Movement Review now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "benchmark 8 total, 8 passed, 0 failed" in ledger
    assert "| Gross-to-Net | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "BASELINE_ALREADY_EXISTS | Gross-to-Net now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "| Payroll Bases & Totals | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "| Annual Leave / Leave Management | v0.4 | yes | yes | no | yes | yes | yes | yes |" in ledger
    assert "BASELINE_ALREADY_EXISTS | Annual Leave / Leave Management now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "| Finalisation Readiness | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "BASELINE_ALREADY_EXISTS | Finalisation Readiness now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "benchmark 12 total, 12 passed, 0 failed" in ledger
    assert "corpus coverage 11 STRONG, 1 WEAK, 0 MISSING" in ledger
    assert "answer gap status NEEDS_REFINEMENT with 11 KEEP actions and 1 IMPROVE_SYNTHESIS action for `purpose_and_operator_meaning`" in ledger
    assert "| Payroll Output | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "BASELINE_ALREADY_EXISTS | Payroll Output now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "benchmark 7 total, 6 passed, 1 failed" in ledger
    assert "payroll-output-rich-answer" in ledger
    assert "corpus coverage 10 STRONG, 1 WEAK, 0 MISSING" in ledger
    assert "answer gap status NEEDS_REFINEMENT with 10 KEEP actions and 1 IMPROVE_SYNTHESIS action for `worker_level_output`" in ledger
    assert "Failure is benchmark/source-evidence check or retrieval/source-matched-phrase drift, not corpus gap" in ledger
    assert "| RateSource / Rate Story | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "BASELINE_ALREADY_EXISTS | RateSource / Rate Story now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "benchmark 6 total, 5 passed, 1 failed" in ledger
    assert "rate-source-rate-story-rich-answer" in ledger
    assert "answer gap status NEEDS_REFINEMENT with 10 KEEP actions and 1 IMPROVE_SYNTHESIS action for `rate_source_evidence_index`" in ledger
    assert "| Decision Story | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "BASELINE_ALREADY_EXISTS | Decision Story now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "decision-story-rich-answer" in ledger
    assert "answer gap status GOOD with 10 KEEP actions" in ledger
    assert "| Contact Payroll History | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "BASELINE_ALREADY_EXISTS | Contact Payroll History now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "benchmark 7 total, 5 passed, 2 failed" in ledger
    assert "contact-payroll-history-rich-answer" in ledger
    assert "contact-payroll-history-retro-replay-correction" in ledger
    assert "corpus coverage 7 STRONG, 3 WEAK, 1 MISSING" in ledger
    assert "answer gap status NEEDS_REFINEMENT with 7 KEEP actions, 1 IMPROVE_SYNTHESIS action, 2 IMPROVE_RETRIEVAL_TERMS actions and 1 ADD_FORMAL_SOURCE_EVIDENCE_LATER action" in ledger
    assert "| ObjectTime / Source Truth | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "BASELINE_ALREADY_EXISTS | ObjectTime / Source Truth now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "corpus coverage 12 STRONG, 0 WEAK, 0 MISSING" in ledger
    assert "answer gap status GOOD with 12 KEEP actions" in ledger
    assert "| Process Periods / PayRun Lifecycle | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "BASELINE_ALREADY_EXISTS | Process Periods / PayRun Lifecycle now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "corpus coverage 13 STRONG, 0 WEAK, 0 MISSING" in ledger
    assert "answer gap status GOOD with 13 KEEP actions" in ledger
    assert "| Comparison / Remediation | v0.4 | yes | yes | yes | yes | yes | yes | yes |" in ledger
    assert "BASELINE_ALREADY_EXISTS | Comparison / Remediation now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "benchmark 9 total, 9 passed, 0 failed" in ledger
    assert "corpus coverage 12 STRONG, 0 WEAK, 0 MISSING" in ledger
    assert "answer gap status GOOD with 12 KEEP actions" in ledger
    assert "| Imports / Actuals | v0.4 | yes | yes | yes | yes | yes | yes | no |" in ledger


def test_worker_story_baseline_history_remains_unchanged_after_batch():
    summary = _read(WORKER_STORY_PACK / "BASELINE_SUMMARY.md")
    benchmark = _read(WORKER_STORY_PACK / "BENCHMARK_BASELINE.md")

    assert "Benchmark result: 5 total, 4 passed, 1 failed" in summary
    assert "Failed benchmark: `worker-story-evidence-rich-answer`" in summary
    assert "synthesis/routing/answer-mode drift" in summary
    assert "Worker Story benchmark rerun: 5 total, 5 passed, 0 failed" in summary
    assert "Result status: `COMPLETED_WITH_FAILURES`" in benchmark


def test_annual_leave_baseline_pack_records_captured_ready_results():
    ledger = _read(LEDGER_PATH)
    combined = "\n".join(_read(ANNUAL_LEAVE_PACK / file_name) for file_name in REQUIRED_FILES)

    assert ANNUAL_LEAVE_PACK.exists()
    for file_name in REQUIRED_FILES:
        assert (ANNUAL_LEAVE_PACK / file_name).exists()

    assert "| Annual Leave / Leave Management | v0.4 | yes | yes | no | yes | yes | yes | yes |" in ledger
    assert "BASELINE_ALREADY_EXISTS | Annual Leave / Leave Management now has a checked-in DB-backed baseline artefact pack" in ledger
    assert "app/services/annual_leave_answer_gap_report_service.py" in ledger
    assert "scripts/build_annual_leave_answer_gap_report.py" in ledger
    assert "Adjacent leave-domain v0.4 diagnostics are not substitutes" in ledger
    assert "Domains with runbook outstanding: none" in ledger

    assert "Annual Leave / Leave Management" in combined
    assert "docs/ANNUAL_LEAVE_EVALUATION_RUNBOOK.md" in combined
    assert "samples\\eval\\rich_answer_benchmark.annual_leave.json" in combined
    assert "scripts\\scan_annual_leave_corpus_coverage.py" in combined
    assert "scripts\\build_annual_leave_answer_gap_report.py" in combined
    assert "DB readiness result: `READY`" in combined
    assert "Result status: `COMPLETED`" in combined
    assert "Total: 1" in combined
    assert "Passed: 1" in combined
    assert "Failed: 0" in combined
    assert "Audit/chat rows created: false" in combined
    assert "Evidence groups: 7" in combined
    assert "`STRONG`: 7" in combined
    assert "`WEAK`: 0" in combined
    assert "`MISSING`: 0" in combined
    assert "Overall status: `GOOD`" in combined
    assert "`KEEP`: 7" in combined
    assert "Report type: `ANNUAL_LEAVE_MANAGEMENT_ANSWER_GAP_REPORT`" in combined
    assert "Source coverage plan: `ANNUAL_LEAVE_MANAGEMENT`" in combined
    assert "Keep current Annual Leave / Leave Management retrieval terms and answer synthesis under benchmark watch" in combined
    assert "Generated artefact committed: no" in combined
    assert "Code Evidence answer integration: no" in combined
    assert "BLOCKED_DATABASE_CONNECTION" not in combined


def test_annual_leave_baseline_is_diagnostic_only_not_runtime_truth():
    combined = "\n".join(_read(ANNUAL_LEAVE_PACK / file_name) for file_name in REQUIRED_FILES)

    assert "diagnostic-only" in combined
    assert "not operational truth" in combined
    assert "does not mutate corpus" in combined
    assert "does not change routing" in combined
    assert "does not change answer generation" in combined
    assert "does not call live LLM" in combined
    assert "does not ingest operational JSON" in combined
    assert "does not connect Code Evidence" in combined
    assert "does not create DB schema or migrations" in combined
    assert "does not add endpoints or UI" in combined
    assert "does not change workforce-platform" in combined


def test_generated_json_reports_are_not_required_committed_baseline_artefacts():
    policy = _read(BASELINE_ROOT / "BASELINE_CAPTURE_POLICY.md")
    ledger = _read(LEDGER_PATH)

    assert "Generated outputs are transient evaluation materials" in policy
    assert "those command targets are not themselves checked-in baseline artefacts" in ledger

    for relative_path in (
        "reports/worker_story_corpus_coverage.json",
        "reports/worker_story_answer_gap_report.json",
        "artifacts/eval/payroll_bases_corpus_coverage.json",
        "artifacts/eval/payroll_bases_answer_gap_report.json",
        "artifacts/eval/payrun_admin_queue_corpus_coverage.json",
        "artifacts/eval/payrun_admin_queue_answer_gap_report.json",
        "artifacts/eval/movement_review_corpus_coverage.json",
        "artifacts/eval/movement_review_answer_gap_report.json",
        "artifacts/eval/gross_to_net_corpus_coverage.json",
        "artifacts/eval/gross_to_net_answer_gap_report.json",
        "artifacts/eval/annual_leave_corpus_coverage.json",
        "artifacts/eval/annual_leave_answer_gap_report.json",
        "artifacts/eval/finalisation_readiness_corpus_coverage.json",
        "artifacts/eval/finalisation_readiness_answer_gap_report.json",
        "artifacts/eval/payroll_output_corpus_coverage.json",
        "artifacts/eval/payroll_output_answer_gap_report.json",
        "artifacts/eval/rate_source_rate_story_corpus_coverage.json",
        "artifacts/eval/rate_source_rate_story_answer_gap_report.json",
        "artifacts/eval/decision_story_corpus_coverage.json",
        "artifacts/eval/decision_story_answer_gap_report.json",
        "artifacts/eval/contact_payroll_history_corpus_coverage.json",
        "artifacts/eval/contact_payroll_history_answer_gap_report.json",
        "artifacts/eval/objecttime_source_truth_corpus_coverage.json",
        "artifacts/eval/objecttime_source_truth_answer_gap_report.json",
        "artifacts/eval/process_period_payrun_lifecycle_corpus_coverage.json",
        "artifacts/eval/process_period_payrun_lifecycle_answer_gap_report.json",
        "artifacts/eval/imports_actuals_corpus_coverage.json",
        "artifacts/eval/imports_actuals_answer_gap_report.json",
        "artifacts/eval/tax_payg_corpus_coverage.json",
        "artifacts/eval/tax_payg_answer_gap_report.json",
        "artifacts/eval/comparison_remediation_corpus_coverage.json",
        "artifacts/eval/comparison_remediation_answer_gap_report.json",
    ):
        tracked = subprocess.run(
            ["git", "ls-files", "--error-unmatch", relative_path],
            capture_output=True,
            text=True,
            check=False,
        )
        assert tracked.returncode != 0
