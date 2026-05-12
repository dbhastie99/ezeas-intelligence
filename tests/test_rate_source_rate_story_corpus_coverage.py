import json
import sys

from app.models.knowledge import KnowledgeDocument
from app.services.ingestion_service import ingest_file_bytes
from app.services.rate_source_rate_story_corpus_coverage_service import scan_rate_source_rate_story_corpus_coverage
from scripts import scan_rate_source_rate_story_corpus_coverage as scan_rate_source_rate_story_script


EXPECTED_GROUPS = {
    "rate_story_purpose",
    "rate_source_selection",
    "rate_amount_evidence",
    "date_effective_rates",
    "award_account_class_scope",
    "pay_guide_rate_evidence",
    "rate_source_evidence_index",
    "rate_story_vs_decision_story",
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


def test_rate_source_rate_story_corpus_coverage_report_shape(db_session):
    _ingest(
        db_session,
        "RateSource / Rate Story explains selected rate evidence and rate explanation.",
        "Developer Log - RateSource Rate Story Purpose",
    )

    report = scan_rate_source_rate_story_corpus_coverage(db_session).to_dict()

    assert report["plan_id"] == "RATE_SOURCE_RATE_STORY"
    assert report["domain"] == "RateSource / Rate Story"
    assert report["total_evidence_groups"] == 11
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


def test_rate_source_rate_story_corpus_coverage_classifies_strong_weak_and_missing(db_session):
    _ingest(
        db_session,
        "RateSource / Rate Story explains selected rate evidence and rate explanation.",
        "Developer Log - RateSource Purpose A",
    )
    _ingest(
        db_session,
        "Rate Story and RateStory explain why a selected rate was used.",
        "Developer Log - RateSource Purpose B",
    )
    _ingest(
        db_session,
        "AwardRateType and RateType can represent award rate, account rate and class rate scope.",
        "Developer Log - RateSource Scope",
    )

    report = scan_rate_source_rate_story_corpus_coverage(db_session).to_dict()
    groups = {group["group_key"]: group for group in report["groups"]}

    assert groups["rate_story_purpose"]["coverage_status"] == "STRONG"
    assert groups["award_account_class_scope"]["coverage_status"] == "WEAK"
    assert groups["pay_guide_rate_evidence"]["coverage_status"] == "MISSING"
    assert groups["rate_story_purpose"]["matched_sources"]
    assert groups["rate_story_purpose"]["representative_matched_terms"]
    assert set(report["coverage_counts"]) == {"STRONG", "WEAK", "MISSING"}
    assert {group["coverage_status"] for group in report["groups"]} <= {"STRONG", "WEAK", "MISSING"}


def test_rate_source_rate_story_corpus_coverage_json_output_shape(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "RateSource / Rate Story explains selected rate evidence and rate explanation.",
        "Developer Log - RateSource Rate Story Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_rate_source_rate_story_corpus_coverage.py", "--json"])

    exit_code = scan_rate_source_rate_story_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["plan_id"] == "RATE_SOURCE_RATE_STORY"
    assert report["groups"]
    assert "coverage_counts" in report
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False


def test_rate_source_rate_story_corpus_coverage_writes_output_file(db_session, tmp_path, monkeypatch, capsys):
    output_path = tmp_path / "rate-source-rate-story-coverage.json"
    _ingest(
        db_session,
        "RateSource / Rate Story explains selected rate evidence and rate explanation.",
        "Developer Log - RateSource Rate Story Purpose",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["scan_rate_source_rate_story_corpus_coverage.py", "--output", str(output_path)],
    )

    exit_code = scan_rate_source_rate_story_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote RateSource / Rate Story corpus coverage report" in captured.out
    assert "Live LLM calls: no" in captured.out
    assert "Code Evidence answer integration: no" in captured.out
    assert report["plan_id"] == "RATE_SOURCE_RATE_STORY"


def test_rate_source_rate_story_corpus_coverage_human_output_is_diagnostic_only(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "RateSource / Rate Story explains selected rate evidence and rate explanation.",
        "Developer Log - RateSource Rate Story Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_rate_source_rate_story_corpus_coverage.py"])

    exit_code = scan_rate_source_rate_story_script.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Live LLM calls: no" in captured.out
    assert "Corpus mutation: no" in captured.out
    assert "Operational JSON ingestion: no" in captured.out
    assert "Code Evidence answer integration: no" in captured.out


def test_rate_source_rate_story_corpus_coverage_does_not_mutate_corpus(db_session):
    _ingest(
        db_session,
        "RateSource / Rate Story explains selected rate evidence and rate explanation.",
        "Developer Log - RateSource Rate Story Purpose",
    )
    before_count = db_session.query(KnowledgeDocument).count()

    scan_rate_source_rate_story_corpus_coverage(db_session)

    assert db_session.query(KnowledgeDocument).count() == before_count


def test_rate_source_rate_story_readme_documents_diagnostic_only_guardrails():
    readme = open("README.md", encoding="utf-8").read()

    assert "scan_rate_source_rate_story_corpus_coverage.py" in readme
    assert "build_rate_source_rate_story_answer_gap_report.py" in readme
    assert "RateSource / Rate Story diagnostics" in readme
    assert "do not mutate corpus records" in readme
    assert "ingest operational JSON" in readme
    assert "call a live LLM" in readme
    assert "connect Code Evidence Index to answer generation" in readme
