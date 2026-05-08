from app.services.ingestion_service import ingest_file_bytes
from app.services.knowledge_retrieval_service import RetrievalResult, classify_query_intent, retrieve_relevant_chunks
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
        "LLM Boundary\nMinerva is not allowed to calculate payroll and must not calculate payroll, "
        "determine entitlements, approve exceptions, suppress warnings, override payroll outcomes, "
        "mutate configuration, or finalise PayRuns.",
        source_type="PLATFORM_DOCTRINE",
        capability_status="DOCTRINE",
        title="Minerva Advisory Boundary",
    )

    results = retrieve_relevant_chunks(db_session, "What is Minerva not allowed to do?")

    assert results
    assert results[0].original_file_name == "minerva-boundary.txt"
    assert results[0].detected_intent == "MINERVA_BOUNDARY_PROHIBITION"
    assert "must not calculate" in results[0].matched_phrases or "payroll calculation truth" in results[0].matched_phrases
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
    assert results[0].detected_intent == "RBAC_BEFORE_LLM"


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


def test_can_minerva_not_do_is_boundary_prohibition_intent():
    intent = classify_query_intent("What can Minerva not do?")

    assert intent is not None
    assert intent.name == "MINERVA_BOUNDARY_PROHIBITION"


def test_boundary_intent_penalises_generic_not_allowed_chunk(db_session):
    _ingest(
        db_session,
        "generic-not-allowed.txt",
        "Users are not allowed to edit archived settings in the Movement Review screen.",
        source_type="DEVELOPER_LOG",
        capability_status="IMPLEMENTED",
        title="Movement Review Not Allowed Note",
    )
    _ingest(
        db_session,
        "llm-boundary.txt",
        "LLM Boundary\nMinerva is advisory. It must not calculate payroll, must not determine entitlements, "
        "must not approve exceptions, must not suppress warnings, must not mutate configuration, and must not finalise PayRuns.",
        source_type="PLATFORM_DOCTRINE",
        capability_status="DOCTRINE",
        title="Platform Doctrine - LLM Boundary",
    )

    results = retrieve_relevant_chunks(db_session, "What is Minerva not allowed to do?")

    assert results
    assert results[0].original_file_name == "llm-boundary.txt"
    assert all(result.original_file_name != "generic-not-allowed.txt" for result in results[:3])
    assert results[0].match_reason is not None


def test_platform_doctrine_with_boundary_phrase_outranks_developer_log_with_similar_phrase(db_session):
    _ingest(
        db_session,
        "developer-boundary-similar.txt",
        "Developer Log: LLM Boundary. Minerva must not calculate payroll or finalise PayRuns. "
        "This was discussed during historical implementation work.",
        source_type="DEVELOPER_LOG",
        capability_status="IMPLEMENTED",
        title="Developer Log - LLM Boundary Discussion",
    )
    _ingest(
        db_session,
        "platform-boundary-source-priority.txt",
        "LLM Boundary\nMinerva must not calculate payroll or finalise PayRuns. "
        "Minerva is advisory and is not payroll calculation truth.",
        source_type="PLATFORM_DOCTRINE",
        capability_status="DOCTRINE",
        title="Platform Doctrine - LLM Boundary",
    )

    results = retrieve_relevant_chunks(db_session, "What is Minerva not allowed to do?")

    assert results
    assert results[0].original_file_name == "platform-boundary-source-priority.txt"
    assert results[0].source_type == "PLATFORM_DOCTRINE"
    assert "llm boundary" in results[0].matched_phrases


def test_developer_log_can_outrank_platform_doctrine_when_doctrine_has_no_intent_phrase(db_session):
    _ingest(
        db_session,
        "weak-platform-context.txt",
        "Platform Doctrine says Minerva is a read-only advisory knowledge service.",
        source_type="PLATFORM_DOCTRINE",
        capability_status="DOCTRINE",
        title="Platform Doctrine - General Minerva Context",
    )
    _ingest(
        db_session,
        "developer-direct-rbac.txt",
        "Developer Log: RBAC-Before-LLM Hardening. User permissions must be enforced before evidence reaches the LLM, "
        "and the model must not receive sensitive evidence the user is not authorised to view.",
        source_type="DEVELOPER_LOG",
        capability_status="IMPLEMENTED",
        title="Developer Log - RBAC-Before-LLM Hardening",
    )

    results = retrieve_relevant_chunks(db_session, "What does RBAC-before-LLM mean?")

    assert results
    assert results[0].original_file_name == "developer-direct-rbac.txt"
    assert results[0].source_type == "DEVELOPER_LOG"
    assert results[0].matched_phrases


def test_rbac_intent_ranks_doctrine_above_weaker_contextual_chunk(db_session):
    _ingest(
        db_session,
        "weak-rbac-context.txt",
        "Developer thread context mentioned RBAC and LLM while discussing future cleanup tasks.",
        source_type="DEVELOPER_LOG",
        capability_status="DESIGN_DISCUSSION",
        title="Developer Context RBAC LLM",
    )
    _ingest(
        db_session,
        "rbac-doctrine.txt",
        "RBAC-Before-LLM Doctrine\nUser permissions must be enforced before evidence reaches the LLM. "
        "The model must not receive sensitive evidence the user is not authorised to view.",
        source_type="PLATFORM_DOCTRINE",
        capability_status="DOCTRINE",
        title="Platform Doctrine - RBAC-Before-LLM Doctrine",
    )

    results = retrieve_relevant_chunks(db_session, "What does RBAC-before-LLM mean?")

    assert results
    assert results[0].original_file_name == "rbac-doctrine.txt"
    assert "rbac-before-llm doctrine" in results[0].matched_phrases
    assert results[0].match_reason is not None


def test_separate_database_intent_still_returns_intelligence_store_doctrine(db_session):
    _ingest(
        db_session,
        "separate-store-doctrine.txt",
        "Separate Intelligence Store Doctrine\nMinerva uses ezeas-intelligence-db as a separate database. "
        "The operational database remains authoritative and remains source of payroll truth.",
        source_type="PLATFORM_DOCTRINE",
        capability_status="DOCTRINE",
        title="Platform Doctrine - Separate Intelligence Store Doctrine",
    )
    _ingest(
        db_session,
        "database-context.txt",
        "Developer notes mention database migrations for ordinary application tables.",
        source_type="DEVELOPER_LOG",
        capability_status="IMPLEMENTED",
        title="Developer Database Notes",
    )

    results = retrieve_relevant_chunks(db_session, "Why does Minerva use a separate database?")

    assert results
    assert results[0].original_file_name == "separate-store-doctrine.txt"
    assert results[0].detected_intent == "SEPARATE_DATABASE"
    assert "separate intelligence store doctrine" in results[0].matched_phrases


def test_boundary_answer_is_direct_not_source_labelled():
    result = RetrievalResult(
        chunk_id="boundary",
        document_id="doc-boundary",
        chunk_index=0,
        chunk_text="LLM Boundary. Minerva must not calculate payroll or finalise PayRuns.",
        title="Platform Doctrine - LLM Boundary",
        original_file_name="boundary.txt",
        source_type="PLATFORM_DOCTRINE",
        source_authority=100,
        score=90.0,
        matched_tokens=["minerva"],
        snippet="LLM Boundary. Minerva must not calculate payroll or finalise PayRuns.",
        match_ratio=1.0,
        detected_intent="MINERVA_BOUNDARY_PROHIBITION",
        matched_phrases=["llm boundary", "must not calculate"],
        match_reason="matched llm boundary heading",
    )

    answer = StubLLMClient().generate_answer("What is Minerva not allowed to do?", [result])

    assert "Source 1:" not in answer
    assert "calculate payroll" in answer
    assert "determine entitlements" in answer
    assert "finalise PayRuns" in answer


def test_rbac_answer_explains_permissions_before_context():
    result = RetrievalResult(
        chunk_id="rbac",
        document_id="doc-rbac",
        chunk_index=0,
        chunk_text="RBAC-Before-LLM Doctrine. User permissions must be enforced before evidence reaches the LLM.",
        title="Platform Doctrine - RBAC-Before-LLM Doctrine",
        original_file_name="rbac.txt",
        source_type="PLATFORM_DOCTRINE",
        source_authority=100,
        score=90.0,
        matched_tokens=["rbac", "llm"],
        snippet="RBAC-Before-LLM Doctrine. User permissions must be enforced before evidence reaches the LLM.",
        match_ratio=1.0,
        detected_intent="RBAC_BEFORE_LLM",
        matched_phrases=["rbac-before-llm doctrine"],
        match_reason="matched rbac-before-llm doctrine heading",
    )

    answer = StubLLMClient().generate_answer("What does RBAC-before-LLM mean?", [result])

    assert "permissions must be checked before evidence is retrieved into model context" in answer
    assert "must not receive sensitive evidence" in answer


def test_no_raw_json_intent_returns_json_specific_answer_not_boundary_answer(db_session):
    _ingest(
        db_session,
        "generic-boundary.txt",
        "LLM Boundary\nMinerva must not calculate payroll and must not finalise PayRuns.",
        source_type="PLATFORM_DOCTRINE",
        capability_status="DOCTRINE",
        title="Platform Doctrine - LLM Boundary",
    )
    _ingest(
        db_session,
        "json-boundary.txt",
        "No raw JSON by default\nOperational payroll JSON should be registered, hashed, classified, "
        "extracted into facts and safe summaries. Only minimum necessary evidence should reach the LLM "
        "after tenant-filtered, access-controlled redaction.",
        source_type="HARDENING_LOG",
        capability_status="OUTSTANDING_HARDENING",
        title="Hardening Doctrine - Sensitive JSON Boundary",
    )

    results = retrieve_relevant_chunks(db_session, "Why is raw JSON not sent to the LLM by default?")
    answer = StubLLMClient().generate_answer("Why is raw JSON not sent to the LLM by default?", results)

    assert results
    assert results[0].original_file_name == "json-boundary.txt"
    assert results[0].detected_intent == "NO_RAW_JSON_BY_DEFAULT"
    assert "no raw json by default" in results[0].matched_phrases
    assert "Raw JSON is not sent to the LLM by default" in answer
    assert "facts or safe summaries" in answer
    assert "not allowed to calculate payroll" not in answer


def test_source_authority_answer_is_direct_and_mentions_doctrine_logs_outrank_chat_history(db_session):
    _ingest(
        db_session,
        "source-authority.txt",
        "Source Authority Doctrine\nPlatform Doctrine, Hardening Logs and Developer Logs outrank raw chat history. "
        "Chat history is supporting material and must not override formal doctrine or formal logged decisions.",
        source_type="PLATFORM_DOCTRINE",
        capability_status="DOCTRINE",
        title="Platform Doctrine - Source Authority Doctrine",
    )

    results = retrieve_relevant_chunks(db_session, "Why does source authority matter?")
    answer = StubLLMClient().generate_answer("Why does source authority matter?", results)

    assert results[0].detected_intent == "SOURCE_AUTHORITY"
    assert "source authority doctrine" in results[0].matched_phrases
    assert "Source 1:" not in answer
    assert "Platform Doctrine" in answer
    assert "Raw chat history" in answer
    assert "must not override" in answer


def test_chat_history_authority_ranks_direct_raw_chat_history_chunk_above_unrelated_platform_doctrine(db_session):
    _ingest(
        db_session,
        "generic-platform-history.txt",
        "Platform Doctrine contains general platform history and implementation context for Minerva.",
        source_type="PLATFORM_DOCTRINE",
        capability_status="DOCTRINE",
        title="Platform Doctrine - General History",
    )
    _ingest(
        db_session,
        "chat-history-authority.txt",
        "Raw chat history is supporting material. It may include exploratory design discussion, abandoned ideas, "
        "corrections and superseded thinking. It must not override formal doctrine.",
        source_type="DEVELOPER_LOG",
        capability_status="IMPLEMENTED",
        title="Developer Log - Chat History Authority",
    )

    results = retrieve_relevant_chunks(db_session, "What is the difference between Platform Doctrine and chat history?")

    assert results
    assert results[0].original_file_name == "chat-history-authority.txt"
    assert results[0].detected_intent == "CHAT_HISTORY_AUTHORITY"
    assert "raw chat history" in results[0].matched_phrases


def test_developer_logs_role_and_user_guide_rationale_answers_are_direct(db_session):
    _ingest(
        db_session,
        "developer-logs-role.txt",
        "Developer Logs are platform memory and structured memory. The Intelligence Layer uses Developer Logs as "
        "source knowledge, and full project history captures design and hardening decisions.",
        source_type="DEVELOPER_LOG",
        capability_status="IMPLEMENTED",
        title="Developer Log - Developer Logs Role",
    )
    _ingest(
        db_session,
        "user-guide-rationale.txt",
        "Why the new User Guide / Rationale section is required\nThe User Guide / Rationale and Operating Model "
        "explains why the work matters, how the platform should operate, and supports future LLM retrieval so "
        "Minerva can explain the work later.",
        source_type="DEVELOPER_LOG",
        capability_status="IMPLEMENTED",
        title="Developer Log - User Guide / Rationale and Operating Model",
    )

    developer_results = retrieve_relevant_chunks(db_session, "What is the role of Developer Logs in Minerva?")
    developer_answer = StubLLMClient().generate_answer("What is the role of Developer Logs in Minerva?", developer_results)
    rationale_results = retrieve_relevant_chunks(db_session, "What is the User Guide / Rationale section for?")
    rationale_answer = StubLLMClient().generate_answer("What is the User Guide / Rationale section for?", rationale_results)

    assert developer_results[0].detected_intent == "DEVELOPER_LOGS_ROLE"
    assert "Source 1:" not in developer_answer
    assert "formal knowledge corpus" in developer_answer
    assert rationale_results[0].detected_intent == "USER_GUIDE_RATIONALE"
    assert "Source 1:" not in rationale_answer
    assert "why the work matters" in rationale_answer
