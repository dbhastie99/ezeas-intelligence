from app.services.ingestion_service import ingest_file_bytes
from app.services.knowledge_retrieval_service import retrieve_relevant_chunks


def test_retrieval_returns_relevant_chunk_for_known_query(db_session):
    ingest_file_bytes(
        db=db_session,
        content=b"Minerva must audit every AI answer and return source references.",
        original_file_name="audit-doctrine.txt",
        source_type="PLATFORM_DOCTRINE",
        capability_status="DOCTRINE",
    )
    ingest_file_bytes(
        db=db_session,
        content=b"Unrelated release notes about a dashboard color setting.",
        original_file_name="release-notes.txt",
        source_type="OTHER",
    )

    results = retrieve_relevant_chunks(db_session, "How does Minerva audit answers?")

    assert results
    assert results[0].original_file_name == "audit-doctrine.txt"
    assert results[0].source_authority == 100
