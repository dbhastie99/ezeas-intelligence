import json
import sys

from app.models.knowledge import KnowledgeDocument
from app.services.ingestion_service import ingest_file_bytes
from app.services.worker_story_corpus_coverage_service import scan_worker_story_corpus_coverage
from scripts import scan_worker_story_corpus_coverage as scan_worker_story_corpus_coverage_script


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


def test_worker_story_corpus_coverage_report_shape(db_session):
    _ingest(
        db_session,
        "Worker Story and Worker Calculation Story are the Talking Payslip for worker evidence.",
        "Developer Log - Worker Story Purpose",
    )

    report = scan_worker_story_corpus_coverage(db_session).to_dict()

    assert report["plan_id"] == "WORKER_STORY"
    assert report["domain"] == "Worker Story / Worker Calculation Story"
    assert report["total_evidence_groups"] == 10
    assert set(report["coverage_counts"]) == {"STRONG", "WEAK", "MISSING"}
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
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


def test_worker_story_corpus_coverage_classifies_strong_weak_and_missing(db_session):
    _ingest(
        db_session,
        "Worker Story and Worker Calculation Story explain worker evidence.",
        "Developer Log - Worker Story Purpose A",
    )
    _ingest(
        db_session,
        "Talking Payslip is another name for Worker Story and Worker Calculation Story.",
        "Developer Log - Worker Story Purpose B",
    )
    _ingest(
        db_session,
        "Worker Story uses SourceTruth and source truth inclusion evidence for a worker.",
        "Developer Log - Worker Story SourceTruth",
    )

    report = scan_worker_story_corpus_coverage(db_session).to_dict()
    groups = {group["group_key"]: group for group in report["groups"]}

    assert groups["worker_story_purpose"]["coverage_status"] == "STRONG"
    assert groups["source_truth_and_inclusion"]["coverage_status"] == "WEAK"
    assert groups["calculated_payroll_outcome"]["coverage_status"] == "MISSING"
    assert report["coverage_counts"]["STRONG"] >= 1
    assert report["coverage_counts"]["WEAK"] >= 1
    assert report["coverage_counts"]["MISSING"] >= 1


def test_worker_story_corpus_coverage_json_output_shape(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Worker Story and Worker Calculation Story are the Talking Payslip for worker evidence.",
        "Developer Log - Worker Story Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_worker_story_corpus_coverage.py", "--json"])

    exit_code = scan_worker_story_corpus_coverage_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["plan_id"] == "WORKER_STORY"
    assert report["groups"]
    assert "coverage_counts" in report


def test_worker_story_corpus_coverage_writes_output_file(db_session, tmp_path, monkeypatch, capsys):
    output_path = tmp_path / "worker-story-coverage.json"
    _ingest(
        db_session,
        "Worker Story and Worker Calculation Story are the Talking Payslip for worker evidence.",
        "Developer Log - Worker Story Purpose",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["scan_worker_story_corpus_coverage.py", "--output", str(output_path)],
    )

    exit_code = scan_worker_story_corpus_coverage_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote Worker Story corpus coverage report" in captured.out
    assert report["plan_id"] == "WORKER_STORY"


def test_worker_story_corpus_coverage_does_not_mutate_corpus(db_session):
    _ingest(
        db_session,
        "Worker Story and Worker Calculation Story are the Talking Payslip for worker evidence.",
        "Developer Log - Worker Story Purpose",
    )
    before_count = db_session.query(KnowledgeDocument).count()

    scan_worker_story_corpus_coverage(db_session)

    assert db_session.query(KnowledgeDocument).count() == before_count
