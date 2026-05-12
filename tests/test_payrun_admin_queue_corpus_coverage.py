import json
import sys

from app.models.knowledge import KnowledgeDocument
from app.services.ingestion_service import ingest_file_bytes
from app.services.payrun_admin_queue_corpus_coverage_service import scan_payrun_admin_queue_corpus_coverage
from scripts import scan_payrun_admin_queue_corpus_coverage as scan_payrun_admin_queue_corpus_coverage_script


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


def test_payrun_admin_queue_corpus_coverage_report_shape(db_session):
    _ingest(
        db_session,
        "PayRun Admin Queue is the operator workbench for what needs action now.",
        "Developer Log - Admin Queue Purpose",
    )

    report = scan_payrun_admin_queue_corpus_coverage(db_session).to_dict()

    assert report["plan_id"] == "PAYRUN_ADMIN_QUEUE"
    assert report["domain"] == "PayRun Admin Queue"
    assert report["total_evidence_groups"] == 11
    assert set(report["coverage_counts"]) == {"STRONG", "WEAK", "MISSING"}
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False
    assert {group["group_key"] for group in report["groups"]} == {
        "purpose_and_operator_meaning",
        "blockers_warnings_and_ready_actions",
        "worker_attention_and_dirty_contacts",
        "processing_and_reprocessing_actions",
        "finalisation_readiness",
        "assurance_snapshot",
        "review_surfaces_and_navigation",
        "worker_story_connection",
        "payroll_bases_connection",
        "movement_review_connection",
        "outstanding_hardening",
    }
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


def test_payrun_admin_queue_corpus_coverage_classifies_strong_weak_and_missing(db_session):
    _ingest(
        db_session,
        "PayRun Admin Queue is the operator workbench for what needs action now.",
        "Developer Log - Admin Queue Purpose A",
    )
    _ingest(
        db_session,
        "Admin Queue is an operator workbench for what needs action now in PayRun.",
        "Developer Log - Admin Queue Purpose B",
    )
    _ingest(
        db_session,
        "Assurance Snapshot provides reasonableness and review signals.",
        "Developer Log - Admin Queue Assurance",
    )

    report = scan_payrun_admin_queue_corpus_coverage(db_session).to_dict()
    groups = {group["group_key"]: group for group in report["groups"]}

    assert groups["purpose_and_operator_meaning"]["coverage_status"] == "STRONG"
    assert groups["assurance_snapshot"]["coverage_status"] == "WEAK"
    assert groups["finalisation_readiness"]["coverage_status"] == "MISSING"
    assert report["coverage_counts"]["STRONG"] >= 1
    assert report["coverage_counts"]["WEAK"] >= 1
    assert report["coverage_counts"]["MISSING"] >= 1


def test_payrun_admin_queue_corpus_coverage_json_output_shape(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "PayRun Admin Queue is the operator workbench for what needs action now.",
        "Developer Log - Admin Queue Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_payrun_admin_queue_corpus_coverage.py", "--json"])

    exit_code = scan_payrun_admin_queue_corpus_coverage_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["plan_id"] == "PAYRUN_ADMIN_QUEUE"
    assert report["groups"]
    assert "coverage_counts" in report
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False


def test_payrun_admin_queue_corpus_coverage_writes_output_file(db_session, tmp_path, monkeypatch, capsys):
    output_path = tmp_path / "payrun-admin-queue-coverage.json"
    _ingest(
        db_session,
        "PayRun Admin Queue is the operator workbench for what needs action now.",
        "Developer Log - Admin Queue Purpose",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["scan_payrun_admin_queue_corpus_coverage.py", "--output", str(output_path)],
    )

    exit_code = scan_payrun_admin_queue_corpus_coverage_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote PayRun Admin Queue corpus coverage report" in captured.out
    assert "Live LLM calls: no" in captured.out
    assert report["plan_id"] == "PAYRUN_ADMIN_QUEUE"


def test_payrun_admin_queue_corpus_coverage_human_output_is_diagnostic_only(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "PayRun Admin Queue is the operator workbench for what needs action now.",
        "Developer Log - Admin Queue Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_payrun_admin_queue_corpus_coverage.py"])

    exit_code = scan_payrun_admin_queue_corpus_coverage_script.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Live LLM calls: no" in captured.out
    assert "Corpus mutation: no" in captured.out
    assert "Operational JSON ingestion: no" in captured.out


def test_payrun_admin_queue_corpus_coverage_does_not_mutate_corpus(db_session):
    _ingest(
        db_session,
        "PayRun Admin Queue is the operator workbench for what needs action now.",
        "Developer Log - Admin Queue Purpose",
    )
    before_count = db_session.query(KnowledgeDocument).count()

    scan_payrun_admin_queue_corpus_coverage(db_session)

    assert db_session.query(KnowledgeDocument).count() == before_count
