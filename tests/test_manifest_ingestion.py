import json

import pytest

from app.models.knowledge import KnowledgeChunk, KnowledgeDocument
from app.services.manifest_ingestion_service import ManifestIngestionError, ingest_manifest


def _write_manifest(tmp_path, payload):
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(payload), encoding="utf-8")
    return manifest_path


def test_valid_manifest_ingestion(db_session, tmp_path):
    document_path = tmp_path / "doctrine.txt"
    document_path.write_text("Minerva doctrine is advisory and audited.", encoding="utf-8")
    manifest_path = _write_manifest(
        tmp_path,
        {
            "default_source_type": "OTHER",
            "default_capability_status": "UNKNOWN",
            "default_tenant_id": None,
            "documents": [
                {
                    "path": "doctrine.txt",
                    "source_type": "PLATFORM_DOCTRINE",
                    "capability_status": "DOCTRINE",
                    "title": "Doctrine Title",
                }
            ],
        },
    )

    summary = ingest_manifest(db_session, manifest_path)

    assert summary["total_documents_listed"] == 1
    assert summary["ingested"] == 1
    assert summary["duplicates"] == 0
    assert summary["skipped"] == 0
    assert summary["error_count"] == 0
    assert summary["results"][0]["status"] == "INGESTED"
    document = db_session.query(KnowledgeDocument).one()
    assert document.Title == "Doctrine Title"
    assert document.SourceType == "PLATFORM_DOCTRINE"
    assert document.CapabilityStatus == "DOCTRINE"


def test_manifest_duplicate_rerun_reports_duplicate(db_session, tmp_path):
    document_path = tmp_path / "repeat.txt"
    document_path.write_text("Repeatable corpus ingestion should be safe to rerun.", encoding="utf-8")
    manifest_path = _write_manifest(
        tmp_path,
        {
            "documents": [{"path": "repeat.txt", "source_type": "OTHER", "capability_status": "UNKNOWN"}],
        },
    )

    first = ingest_manifest(db_session, manifest_path)
    second = ingest_manifest(db_session, manifest_path)

    assert first["ingested"] == 1
    assert second["ingested"] == 0
    assert second["duplicates"] == 1
    assert second["results"][0]["duplicate"] is True
    assert db_session.query(KnowledgeDocument).count() == 1
    assert db_session.query(KnowledgeChunk).count() == first["results"][0]["chunk_count"]


def test_document_metadata_overrides_manifest_defaults(db_session, tmp_path):
    document_path = tmp_path / "requirements.txt"
    document_path.write_text("Planning document for Minerva requirements.", encoding="utf-8")
    manifest_path = _write_manifest(
        tmp_path,
        {
            "default_source_type": "OTHER",
            "default_capability_status": "UNKNOWN",
            "default_tenant_id": "tenant-default",
            "documents": [
                {
                    "path": "requirements.txt",
                    "source_type": "REQUIREMENTS",
                    "capability_status": "PHASE_ONE",
                    "tenant_id": "tenant-doc",
                    "title": "Requirements Override",
                }
            ],
        },
    )

    summary = ingest_manifest(db_session, manifest_path)

    assert summary["ingested"] == 1
    document = db_session.query(KnowledgeDocument).one()
    assert document.SourceType == "REQUIREMENTS"
    assert document.SourceAuthority == 70
    assert document.CapabilityStatus == "PHASE_ONE"
    assert document.TenantId == "tenant-doc"
    assert document.Title == "Requirements Override"


def test_manifest_invalid_source_type_is_rejected(db_session, tmp_path):
    document_path = tmp_path / "bad-source.txt"
    document_path.write_text("Bad source.", encoding="utf-8")
    manifest_path = _write_manifest(tmp_path, {"documents": [{"path": "bad-source.txt", "source_type": "PAYROLL"}]})

    with pytest.raises(ManifestIngestionError, match="Invalid source_type"):
        ingest_manifest(db_session, manifest_path)


def test_manifest_invalid_capability_status_is_rejected(db_session, tmp_path):
    document_path = tmp_path / "bad-status.txt"
    document_path.write_text("Bad status.", encoding="utf-8")
    manifest_path = _write_manifest(
        tmp_path,
        {"documents": [{"path": "bad-status.txt", "capability_status": "DONE"}]},
    )

    with pytest.raises(ManifestIngestionError, match="Invalid capability_status"):
        ingest_manifest(db_session, manifest_path)


def test_manifest_missing_file_path_is_handled_cleanly(db_session, tmp_path):
    manifest_path = _write_manifest(tmp_path, {"documents": [{"path": "missing.txt"}]})

    summary = ingest_manifest(db_session, manifest_path)

    assert summary["ingested"] == 0
    assert summary["error_count"] == 1
    assert summary["results"][0]["status"] == "ERROR"
    assert summary["results"][0]["error"] == "File not found."
    assert db_session.query(KnowledgeDocument).count() == 0


def test_manifest_title_defaults_to_filename_when_missing(db_session, tmp_path):
    document_path = tmp_path / "developer-log.txt"
    document_path.write_text("Developer log title should default from filename.", encoding="utf-8")
    manifest_path = _write_manifest(tmp_path, {"documents": [{"path": "developer-log.txt"}]})

    summary = ingest_manifest(db_session, manifest_path)

    assert summary["ingested"] == 1
    document = db_session.query(KnowledgeDocument).one()
    assert document.Title == "developer-log"
    assert summary["results"][0]["title"] == "developer-log"
