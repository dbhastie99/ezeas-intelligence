import json
import sys

from app.models.knowledge import KnowledgeDocument
from app.services.ingestion_service import ingest_file_bytes
from app.services.worker_attention_issue_resolution_corpus_coverage_service import (
    scan_worker_attention_issue_resolution_corpus_coverage,
)
from scripts import scan_worker_attention_issue_resolution_corpus_coverage as scan_worker_attention_script


EXPECTED_GROUPS = {
    "worker_attention_purpose",
    "worker_issue_model",
    "blockers_warnings_and_readiness",
    "deterministic_fix_links",
    "dirty_contact_and_reprocessing",
    "payment_allocation_readiness",
    "tax_deduction_leave_readiness",
    "negative_net_pay_and_obligations",
    "worker_story_relationship",
    "admin_queue_relationship",
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


def test_worker_attention_issue_resolution_corpus_coverage_report_shape(db_session):
    _ingest(
        db_session,
        "Worker Attention / Issue Resolution is the worker-level issue surface.",
        "Developer Log - Worker Attention Purpose",
    )

    report = scan_worker_attention_issue_resolution_corpus_coverage(db_session).to_dict()

    assert report["plan_id"] == "WORKER_ATTENTION_ISSUE_RESOLUTION"
    assert report["domain"] == "Worker Attention / Issue Resolution"
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


def test_worker_attention_issue_resolution_corpus_coverage_classifies_strong_weak_and_missing(db_session):
    _ingest(
        db_session,
        "Worker Attention / Issue Resolution is the worker-level issue surface.",
        "Developer Log - Worker Attention Purpose A",
    )
    _ingest(
        db_session,
        "WorkerAttention and Worker Attention Centre provide Issue Resolution evidence.",
        "Developer Log - Worker Attention Purpose B",
    )
    _ingest(
        db_session,
        "Payment allocation readiness can create worker attention blockers.",
        "Developer Log - Worker Attention Payment Allocation",
    )

    report = scan_worker_attention_issue_resolution_corpus_coverage(db_session).to_dict()
    groups = {group["group_key"]: group for group in report["groups"]}

    assert groups["worker_attention_purpose"]["coverage_status"] == "STRONG"
    assert groups["payment_allocation_readiness"]["coverage_status"] == "WEAK"
    assert groups["negative_net_pay_and_obligations"]["coverage_status"] == "MISSING"
    assert groups["worker_attention_purpose"]["matched_sources"]
    assert groups["worker_attention_purpose"]["representative_matched_terms"]
    assert set(report["coverage_counts"]) == {"STRONG", "WEAK", "MISSING"}


def test_worker_attention_issue_resolution_corpus_coverage_json_output_shape(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Worker Attention / Issue Resolution is the worker-level issue surface.",
        "Developer Log - Worker Attention Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_worker_attention_issue_resolution_corpus_coverage.py", "--json"])

    exit_code = scan_worker_attention_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["plan_id"] == "WORKER_ATTENTION_ISSUE_RESOLUTION"
    assert report["groups"]
    assert "coverage_counts" in report
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False


def test_worker_attention_issue_resolution_corpus_coverage_writes_output_file(
    db_session, tmp_path, monkeypatch, capsys
):
    output_path = tmp_path / "worker-attention-coverage.json"
    _ingest(
        db_session,
        "Worker Attention / Issue Resolution is the worker-level issue surface.",
        "Developer Log - Worker Attention Purpose",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["scan_worker_attention_issue_resolution_corpus_coverage.py", "--output", str(output_path)],
    )

    exit_code = scan_worker_attention_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote Worker Attention / Issue Resolution corpus coverage report" in captured.out
    assert "Live LLM calls: no" in captured.out
    assert report["plan_id"] == "WORKER_ATTENTION_ISSUE_RESOLUTION"


def test_worker_attention_issue_resolution_corpus_coverage_human_output_is_diagnostic_only(
    db_session, monkeypatch, capsys
):
    _ingest(
        db_session,
        "Worker Attention / Issue Resolution is the worker-level issue surface.",
        "Developer Log - Worker Attention Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_worker_attention_issue_resolution_corpus_coverage.py"])

    exit_code = scan_worker_attention_script.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Live LLM calls: no" in captured.out
    assert "Corpus mutation: no" in captured.out
    assert "Operational JSON ingestion: no" in captured.out


def test_worker_attention_issue_resolution_corpus_coverage_does_not_mutate_corpus(db_session):
    _ingest(
        db_session,
        "Worker Attention / Issue Resolution is the worker-level issue surface.",
        "Developer Log - Worker Attention Purpose",
    )
    before_count = db_session.query(KnowledgeDocument).count()

    scan_worker_attention_issue_resolution_corpus_coverage(db_session)

    assert db_session.query(KnowledgeDocument).count() == before_count
