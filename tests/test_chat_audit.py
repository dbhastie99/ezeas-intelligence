from app.models.audit import AIInteractionAudit
from app.models.chat import KnowledgeChatMessage
from app.services.knowledge_retrieval_service import RetrievalResult
from app.services.llm_client import StubLLMClient


def test_chat_message_creates_messages_sources_and_audit(client, db_session):
    ingest = client.post(
        "/api/v1/ingest/file",
        files={
            "file": (
                "sample_platform_doctrine.txt",
                b"Minerva reads, indexes, retrieves, explains and audits. Minerva is advisory.",
                "text/plain",
            )
        },
        data={"source_type": "PLATFORM_DOCTRINE", "capability_status": "DOCTRINE"},
    )
    assert ingest.status_code == 200
    session_response = client.post("/api/v1/chat/session", json={"title": "Doctrine"})
    session_id = session_response.json()["session_id"]

    response = client.post(
        "/api/v1/chat/message",
        json={"session_id": session_id, "message": "What does Minerva retrieve and audit?"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["sources"]
    assert body["audit_id"]
    assert "Based on the retrieved Minerva knowledge sources" in body["answer"]

    messages = db_session.query(KnowledgeChatMessage).order_by(KnowledgeChatMessage.CreatedAt).all()
    assert [message.Role for message in messages] == ["USER", "ASSISTANT"]
    audit = db_session.get(AIInteractionAudit, body["audit_id"])
    assert audit is not None
    assert audit.ModelName == "STUB_LLM"
    assert audit.PromptPolicy == "MINERVA_V0_GROUNDED_READ_ONLY"
    assert "sample_platform_doctrine" in audit.SourceReferencesJson


def test_no_evidence_chat_returns_honest_answer_and_still_audits(client, db_session):
    session_response = client.post("/api/v1/chat/session", json={"title": "Empty"})
    session_id = session_response.json()["session_id"]

    response = client.post(
        "/api/v1/chat/message",
        json={"session_id": session_id, "message": "What is the current award interpretation?"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["sources"] == []
    assert "I do not have retrieved Minerva knowledge evidence" in body["answer"]
    assert "does not calculate or change payroll truth" in body["answer"]
    assert db_session.query(AIInteractionAudit).count() == 1
    assert db_session.query(KnowledgeChatMessage).count() == 2


def test_stub_llm_does_not_leave_dangling_partial_word_before_safety_boundary():
    chunk_text = ("A" * 349) + " I should not leak as a dangling partial word."
    result = RetrievalResult(
        chunk_id="chunk-1",
        document_id="doc-1",
        chunk_index=0,
        chunk_text=chunk_text,
        title="Stub test",
        original_file_name="stub.txt",
        source_type="OTHER",
        source_authority=10,
        score=1.0,
    )

    answer = StubLLMClient().generate_answer("What is Minerva allowed to do?", [result])

    assert " I Minerva is advisory" not in answer
    assert "Minerva is advisory and does not calculate or change payroll truth." in answer
