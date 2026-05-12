import json
import sys

from app.models.knowledge import KnowledgeDocument
from app.services.ingestion_service import ingest_file_bytes
from app.services.retro_replay_corpus_coverage_service import scan_retro_replay_corpus_coverage
from scripts import scan_retro_replay_corpus_coverage as scan_retro_replay_corpus_coverage_script


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


def test_retro_replay_corpus_coverage_report_shape(db_session):
    _ingest(
        db_session,
        "Retro / Replay is governed historical correction and evidence replay, not ordinary reprocessing.",
        "Developer Log - Retro Replay Purpose",
    )

    report = scan_retro_replay_corpus_coverage(db_session).to_dict()

    assert report["plan_id"] == "RETRO_REPLAY"
    assert report["domain"] == "Retro / Replay"
    assert report["total_evidence_groups"] == 12
    assert set(report["coverage_counts"]) == {"STRONG", "WEAK", "MISSING"}
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False
    assert {group["group_key"] for group in report["groups"]} == {
        "purpose_and_operator_meaning",
        "attributed_period_and_paid_period_truth",
        "finalised_outcome_memory",
        "current_effective_and_historical_truth",
        "bucket_and_basis_snapshot_dependency",
        "source_change_and_dependency_detection",
        "retro_payrun_and_supplementary_distinction",
        "comparison_and_variance_connection",
        "worker_story_connection",
        "admin_queue_and_movement_review_connection",
        "audit_replay_and_non_destructive_history",
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


def test_retro_replay_corpus_coverage_classifies_strong_weak_and_missing(db_session):
    _ingest(
        db_session,
        "Retro / Replay is governed historical correction and evidence replay.",
        "Developer Log - Retro Purpose A",
    )
    _ingest(
        db_session,
        "Retro / Replay is not ordinary reprocessing.",
        "Developer Log - Retro Purpose B",
    )
    _ingest(
        db_session,
        "Attributed-period truth and paid-period truth must remain distinct.",
        "Developer Log - Retro Period Truth",
    )

    report = scan_retro_replay_corpus_coverage(db_session).to_dict()
    groups = {group["group_key"]: group for group in report["groups"]}

    assert groups["purpose_and_operator_meaning"]["coverage_status"] == "STRONG"
    assert groups["attributed_period_and_paid_period_truth"]["coverage_status"] == "WEAK"
    assert groups["source_change_and_dependency_detection"]["coverage_status"] == "MISSING"
    assert report["coverage_counts"]["STRONG"] >= 1
    assert report["coverage_counts"]["WEAK"] >= 1
    assert report["coverage_counts"]["MISSING"] >= 1


def test_retro_replay_corpus_coverage_json_output_shape(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Retro / Replay is governed historical correction and evidence replay.",
        "Developer Log - Retro Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_retro_replay_corpus_coverage.py", "--json"])

    exit_code = scan_retro_replay_corpus_coverage_script.main()
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["plan_id"] == "RETRO_REPLAY"
    assert report["groups"]
    assert "coverage_counts" in report
    assert report["mutation_performed"] is False
    assert report["live_llm_call_performed"] is False
    assert report["operational_json_ingestion_performed"] is False


def test_retro_replay_corpus_coverage_writes_output_file(db_session, tmp_path, monkeypatch, capsys):
    output_path = tmp_path / "retro-replay-coverage.json"
    _ingest(
        db_session,
        "Retro / Replay is governed historical correction and evidence replay.",
        "Developer Log - Retro Purpose",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["scan_retro_replay_corpus_coverage.py", "--output", str(output_path)],
    )

    exit_code = scan_retro_replay_corpus_coverage_script.main()
    captured = capsys.readouterr()
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_path.exists()
    assert "Wrote Retro / Replay corpus coverage report" in captured.out
    assert "Live LLM calls: no" in captured.out
    assert report["plan_id"] == "RETRO_REPLAY"


def test_retro_replay_corpus_coverage_human_output_is_diagnostic_only(db_session, monkeypatch, capsys):
    _ingest(
        db_session,
        "Retro / Replay is governed historical correction and evidence replay.",
        "Developer Log - Retro Purpose",
    )
    monkeypatch.setattr(sys, "argv", ["scan_retro_replay_corpus_coverage.py"])

    exit_code = scan_retro_replay_corpus_coverage_script.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Live LLM calls: no" in captured.out
    assert "Corpus mutation: no" in captured.out
    assert "Operational JSON ingestion: no" in captured.out


def test_retro_replay_corpus_coverage_does_not_mutate_corpus(db_session):
    _ingest(
        db_session,
        "Retro / Replay is governed historical correction and evidence replay.",
        "Developer Log - Retro Purpose",
    )
    before_count = db_session.query(KnowledgeDocument).count()

    scan_retro_replay_corpus_coverage(db_session)

    assert db_session.query(KnowledgeDocument).count() == before_count
