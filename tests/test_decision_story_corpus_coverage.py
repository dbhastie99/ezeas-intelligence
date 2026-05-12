import json
import sys

from app.models.knowledge import KnowledgeDocument
from app.services.decision_story_corpus_coverage_service import scan_decision_story_corpus_coverage
from app.services.ingestion_service import ingest_file_bytes
from scripts import scan_decision_story_corpus_coverage as scan_decision_story_script


EXPECTED_GROUPS = {
    "decision_story_purpose",
    "treatment_and_entitlement_selection",
    "decision_evidence_index",
    "award_rule_and_runtime_fact_evidence",
    "allowance_penalty_overtime_shift_evidence",
    "break_public_holiday_and_special_condition_evidence",
    "decision_story_vs_rate_story",
    "worker_story_relationship",
    "payroll_output_and_gross_to_net_relationship",
    "outstanding_hardening",
}


def _ingest(db_session, text: str, title: str):
    document, duplicate = ingest_file_bytes(
        db=db_session,
        content=text.encode("utf-8"),
        original_file_name=f"{title.lower().replace(' ', '-')}.txt",
        source_type="DEVELOPER_LOG",
        capability_status="IMPLEMENTED",
        title=title,
    )
    assert duplicate is False
    return document


def test_decision_story_corpus_coverage_report_shape(db_session):
    _ingest(
        db_session,
        "Decision Story explains why a treatment and why a line exists.",
        "Developer Log - Decision Story Purpose",
    )

    report = scan_decision_story_corpus_coverage(db_session).to_dict()

    assert report["plan_id"] == "DECISION_STORY"
    assert report["domain"] == "Decision Story"
    assert report["total_evidence_groups"] == 10
    assert set(report["coverage_counts"]) == {"STRONG", "WEAK", "MISSING"}
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False
    assert {group["group_key"] for group in report["groups"]} == EXPECTED_GROUPS
    first_group = report["groups"][0]
    assert {
        "group_key",
        "group_label",
        "search_terms_used",
        "matched_chunk_count",
        "matched_document_count",
        "matched_sources",
        "representative_matched_terms",
        "coverage_status",
        "diagnostic_notes",
    }.issubset(first_group)


def test_decision_story_corpus_coverage_classifies_strong_weak_and_missing(db_session):
    _ingest(
        db_session,
        "Decision Story and DecisionStory explain why a treatment and why a line exists.",
        "Developer Log - Decision Story Purpose A",
    )
    _ingest(
        db_session,
        "Decision Story explains payroll decision evidence for why a treatment was selected.",
        "Developer Log - Decision Story Purpose B",
    )
    _ingest(
        db_session,
        "Allowance decision and penalty decision evidence explain allowance and penalty treatment.",
        "Developer Log - Decision Story Allowance Penalty",
    )

    report = scan_decision_story_corpus_coverage(db_session).to_dict()
    groups = {group["group_key"]: group for group in report["groups"]}

    assert groups["decision_story_purpose"]["coverage_status"] == "STRONG"
    assert groups["allowance_penalty_overtime_shift_evidence"]["coverage_status"] == "WEAK"
    assert groups["break_public_holiday_and_special_condition_evidence"]["coverage_status"] == "MISSING"
    assert groups["decision_story_purpose"]["matched_sources"]
    assert groups["decision_story_purpose"]["representative_matched_terms"]
    assert set(report["coverage_counts"]) == {"STRONG", "WEAK", "MISSING"}
    assert {group["coverage_status"] for group in report["groups"]} <= {"STRONG", "WEAK", "MISSING"}


def test_decision_story_corpus_coverage_json_output_shape(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Decision Story explains why a treatment and why a line exists.",
        "Developer Log - Decision Story Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_decision_story_corpus_coverage.py", "--json"])

    exit_code = scan_decision_story_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["plan_id"] == "DECISION_STORY"
    assert report["groups"]
    assert "coverage_counts" in report
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False


def test_decision_story_corpus_coverage_writes_output_file(db_session, tmp_path, monkeypatch, capsys):
    output_path = tmp_path / "decision-story-coverage.json"
    _ingest(
        db_session,
        "Decision Story explains why a treatment and why a line exists.",
        "Developer Log - Decision Story Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_decision_story_corpus_coverage.py", "--output", str(output_path)])

    exit_code = scan_decision_story_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote Decision Story corpus coverage report" in captured.out
    assert "Live LLM calls: no" in captured.out
    assert "Code Evidence answer integration: no" in captured.out
    assert report["plan_id"] == "DECISION_STORY"


def test_decision_story_corpus_coverage_human_output_is_diagnostic_only(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Decision Story explains why a treatment and why a line exists.",
        "Developer Log - Decision Story Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_decision_story_corpus_coverage.py"])

    exit_code = scan_decision_story_script.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Live LLM calls: no" in captured.out
    assert "Corpus mutation: no" in captured.out
    assert "Operational JSON ingestion: no" in captured.out
    assert "Code Evidence answer integration: no" in captured.out


def test_decision_story_corpus_coverage_does_not_mutate_corpus(db_session):
    _ingest(
        db_session,
        "Decision Story explains why a treatment and why a line exists.",
        "Developer Log - Decision Story Purpose",
    )
    before_count = db_session.query(KnowledgeDocument).count()

    scan_decision_story_corpus_coverage(db_session)

    assert db_session.query(KnowledgeDocument).count() == before_count


def test_decision_story_readme_documents_diagnostic_only_guardrails():
    readme = open("README.md", encoding="utf-8").read()

    assert "scan_decision_story_corpus_coverage.py" in readme
    assert "build_decision_story_answer_gap_report.py" in readme
    assert "Decision Story diagnostics" in readme
    assert "do not mutate corpus records" in readme
    assert "ingest operational JSON" in readme
    assert "call a live LLM" in readme
    assert "connect Code Evidence Index to answer generation" in readme
