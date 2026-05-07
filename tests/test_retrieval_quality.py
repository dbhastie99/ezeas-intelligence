from app.services.ingestion_service import ingest_file_bytes
from app.services.knowledge_retrieval_service import RetrievalResult, retrieve_relevant_chunks
from app.services.llm_client import StubLLMClient


def _ingest(db_session, file_name, text, source_type="OTHER", capability_status="UNKNOWN", title=None):
    document, _ = ingest_file_bytes(
        db=db_session,
        content=text.encode("utf-8"),
        original_file_name=file_name,
        source_type=source_type,
        capability_status=capability_status,
        title=title,
    )
    return document


def test_minerva_boundary_query_prefers_minerva_doctrine_over_unrelated_payroll_movement(db_session):
    _ingest(
        db_session,
        "movement-review.txt",
        "Movement Review and PayRunFinalisedTotals reconcile payroll movement totals. "
        "This historical developer log mentions Minerva only as project context.",
        source_type="DEVELOPER_LOG",
        capability_status="IMPLEMENTED",
        title="Movement Review PayRunFinalisedTotals",
    )
    _ingest(
        db_session,
        "minerva-boundary.txt",
        "Minerva is not allowed to calculate payroll, determine entitlements, approve exceptions, "
        "suppress warnings, override payroll outcomes, mutate configuration, or finalise PayRuns.",
        source_type="PLATFORM_DOCTRINE",
        capability_status="DOCTRINE",
        title="Minerva Advisory Boundary",
    )

    results = retrieve_relevant_chunks(db_session, "What is Minerva not allowed to do?")

    assert results
    assert results[0].original_file_name == "minerva-boundary.txt"
    assert {"minerva", "not", "allowed"} <= set(results[0].matched_tokens)
    assert "Movement Review" not in results[0].title


def test_separate_database_query_returns_intelligence_store_chunk(db_session):
    _ingest(
        db_session,
        "separate-db.txt",
        "Minerva uses a separate SQL Server database as an intelligence store so knowledge and audit evidence "
        "remain separate from the operational payroll database.",
        source_type="PLATFORM_DOCTRINE",
        capability_status="DOCTRINE",
        title="Separate Minerva Database",
    )
    _ingest(
        db_session,
        "payroll-db.txt",
        "Payroll processing tables store pay run execution state and totals.",
        source_type="DEVELOPER_LOG",
        capability_status="IMPLEMENTED",
        title="Payroll Database Notes",
    )

    results = retrieve_relevant_chunks(db_session, "Why does Minerva use a separate database?")

    assert results
    assert results[0].original_file_name == "separate-db.txt"
    assert {"minerva", "separate", "database"} <= set(results[0].matched_tokens)


def test_rbac_before_llm_query_returns_rbac_boundary_chunk(db_session):
    _ingest(
        db_session,
        "rbac-before-llm.txt",
        "RBAC-before-LLM means tenant and user authorization boundaries must be enforced before any LLM answer "
        "can use retrieved evidence.",
        source_type="HARDENING_LOG",
        capability_status="OUTSTANDING_HARDENING",
        title="RBAC before LLM",
    )
    _ingest(
        db_session,
        "generic-llm.txt",
        "The stub LLM creates deterministic grounded answers without external provider calls.",
        source_type="OTHER",
        capability_status="UNKNOWN",
        title="Stub LLM Notes",
    )

    results = retrieve_relevant_chunks(db_session, "What does RBAC-before-LLM mean?")

    assert results
    assert results[0].original_file_name == "rbac-before-llm.txt"
    assert {"rbac", "llm"} <= set(results[0].matched_tokens)


def test_source_authority_does_not_overpower_direct_relevance(db_session):
    _ingest(
        db_session,
        "high-authority-unrelated.txt",
        "Platform doctrine says Minerva is advisory and read-only.",
        source_type="PLATFORM_DOCTRINE",
        capability_status="DOCTRINE",
        title="High Authority Generic Minerva Doctrine",
    )
    _ingest(
        db_session,
        "lower-authority-relevant.txt",
        "RBAC-before-LLM requires authorization checks before LLM evidence retrieval and answer generation.",
        source_type="OTHER",
        capability_status="UNKNOWN",
        title="RBAC-before-LLM Implementation Note",
    )

    results = retrieve_relevant_chunks(db_session, "What does RBAC-before-LLM mean?")

    assert results
    assert results[0].original_file_name == "lower-authority-relevant.txt"
    assert results[0].source_authority == 10


def test_source_type_filter_restricts_retrieval(db_session):
    _ingest(
        db_session,
        "platform-filter.txt",
        "Minerva source type filter platform doctrine evidence.",
        source_type="PLATFORM_DOCTRINE",
        capability_status="DOCTRINE",
    )
    _ingest(
        db_session,
        "developer-filter.txt",
        "Minerva source type filter developer log evidence.",
        source_type="DEVELOPER_LOG",
        capability_status="IMPLEMENTED",
    )

    results = retrieve_relevant_chunks(
        db_session,
        "Minerva source type filter evidence",
        source_types=["DEVELOPER_LOG"],
    )

    assert results
    assert {result.source_type for result in results} == {"DEVELOPER_LOG"}
    assert results[0].original_file_name == "developer-filter.txt"


def test_stub_answer_uses_top_relevant_chunks_without_low_score_concatenation():
    strong = RetrievalResult(
        chunk_id="strong",
        document_id="doc-strong",
        chunk_index=0,
        chunk_text="Minerva is not allowed to calculate payroll or change payroll truth.",
        title="Minerva Boundary",
        original_file_name="boundary.txt",
        source_type="PLATFORM_DOCTRINE",
        source_authority=100,
        score=35.0,
        matched_tokens=["minerva", "not", "allowed"],
        snippet="Minerva is not allowed to calculate payroll or change payroll truth.",
        match_ratio=0.75,
    )
    weak = RetrievalResult(
        chunk_id="weak",
        document_id="doc-weak",
        chunk_index=0,
        chunk_text="Movement Review PayRunFinalisedTotals unrelated chunk should not be concatenated.",
        title="Movement Review",
        original_file_name="movement.txt",
        source_type="DEVELOPER_LOG",
        source_authority=80,
        score=4.0,
        matched_tokens=["minerva"],
        snippet="Movement Review PayRunFinalisedTotals unrelated chunk should not be concatenated.",
        match_ratio=0.2,
    )

    answer = StubLLMClient().generate_answer("What is Minerva not allowed to do?", [strong, weak])

    assert "Minerva is not allowed to calculate payroll" in answer
    assert "Movement Review PayRunFinalisedTotals" not in answer
    assert "Minerva is advisory and does not calculate or change payroll truth." in answer
