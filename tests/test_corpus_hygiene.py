from app.models.knowledge import KnowledgeDocument
from app.services.document_admin_service import list_documents, set_document_status
from app.services.ingestion_service import ingest_file_bytes
from app.services.knowledge_retrieval_service import retrieve_relevant_chunks


def _ingest(db_session, file_name, text, source_type="OTHER", title=None):
    document, duplicate = ingest_file_bytes(
        db=db_session,
        content=text.encode("utf-8"),
        original_file_name=file_name,
        source_type=source_type,
        capability_status="UNKNOWN",
        title=title,
    )
    assert duplicate is False
    return document


def test_sample_source_type_is_accepted(db_session):
    document = _ingest(
        db_session,
        "smoke-sample.txt",
        "Sample smoke document for Minerva local proof.",
        source_type="SAMPLE",
        title="Sample Smoke Document",
    )

    assert document.SourceType == "SAMPLE"
    assert document.SourceAuthority == 1


def test_retrieval_excludes_sample_documents_by_default(db_session):
    _ingest(
        db_session,
        "real-doctrine.txt",
        "Minerva boundary doctrine says Minerva is advisory and must not calculate payroll.",
        source_type="PLATFORM_DOCTRINE",
        title="Real Platform Doctrine",
    )
    _ingest(
        db_session,
        "sample-doctrine.txt",
        "Minerva boundary doctrine sample smoke text should not appear in normal retrieval.",
        source_type="SAMPLE",
        title="Sample Platform Doctrine",
    )

    results = retrieve_relevant_chunks(db_session, "Minerva boundary doctrine")

    assert results
    assert {result.source_type for result in results} == {"PLATFORM_DOCTRINE"}


def test_retrieval_can_include_sample_documents_when_requested(db_session):
    _ingest(
        db_session,
        "sample-only.txt",
        "Minerva sample smoke proof text can be included explicitly.",
        source_type="SAMPLE",
        title="Sample Only Document",
    )

    default_results = retrieve_relevant_chunks(db_session, "Minerva sample smoke proof")
    included_results = retrieve_relevant_chunks(
        db_session,
        "Minerva sample smoke proof",
        include_samples=True,
    )

    assert default_results == []
    assert included_results
    assert included_results[0].source_type == "SAMPLE"


def test_superseded_documents_are_excluded_from_retrieval(db_session):
    document = _ingest(
        db_session,
        "superseded.txt",
        "Minerva superseded document should be excluded from active retrieval.",
        source_type="PLATFORM_DOCTRINE",
        title="Superseded Doctrine",
    )
    set_document_status(db_session, document.KnowledgeDocumentId, "SUPERSEDED")

    results = retrieve_relevant_chunks(db_session, "Minerva superseded document")

    assert results == []
    stored = db_session.get(KnowledgeDocument, document.KnowledgeDocumentId)
    assert stored.DocumentStatus == "SUPERSEDED"


def test_list_documents_filters_and_set_document_status(db_session):
    sample = _ingest(
        db_session,
        "admin-sample.txt",
        "Admin sample document.",
        source_type="SAMPLE",
        title="Admin Sample",
    )
    real = _ingest(
        db_session,
        "admin-real.txt",
        "Admin real document.",
        source_type="OTHER",
        title="Admin Real",
    )

    sample_documents = list_documents(db_session, source_type="SAMPLE")
    title_documents = list_documents(db_session, title_contains="Real")

    assert [document.KnowledgeDocumentId for document in sample_documents] == [sample.KnowledgeDocumentId]
    assert [document.KnowledgeDocumentId for document in title_documents] == [real.KnowledgeDocumentId]

    updated, previous_status, new_status = set_document_status(db_session, sample.KnowledgeDocumentId, "SUPERSEDED")

    assert previous_status == "ACTIVE"
    assert new_status == "SUPERSEDED"
    assert updated.DocumentStatus == "SUPERSEDED"
    assert updated.UpdatedAt is not None
    superseded_documents = list_documents(db_session, status="SUPERSEDED")
    assert [document.KnowledgeDocumentId for document in superseded_documents] == [sample.KnowledgeDocumentId]
