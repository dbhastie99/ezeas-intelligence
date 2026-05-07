import os
import sys
from pathlib import Path

from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

SAMPLE_PATH = PROJECT_ROOT / "samples" / "knowledge" / "sample_platform_doctrine.txt"


def configured_database_url() -> str | None:
    env_value = os.getenv("MINERVA_DATABASE_URL")
    if env_value:
        return env_value

    env_file = PROJECT_ROOT / ".env"
    if not env_file.exists():
        return None

    for line in env_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        if key.strip() == "MINERVA_DATABASE_URL" and value.strip():
            return value.strip().strip('"').strip("'")
    return None


def require_ok(response, label: str) -> dict:
    if response.status_code >= 400:
        raise SystemExit(f"{label} failed with HTTP {response.status_code}: {response.text}")
    return response.json()


def main() -> int:
    if not configured_database_url():
        print("MINERVA_DATABASE_URL is not set. Copy .env.example to .env and configure SQL Server first.")
        return 2
    if not SAMPLE_PATH.exists():
        print(f"Sample file not found: {SAMPLE_PATH}")
        return 1

    from app.main import app
    from app.core.enums import ChatRole, normalize_chat_role
    from app.db.session import SessionLocal
    from app.models.chat import KnowledgeChatMessage, KnowledgeChatSession
    from app.services.answer_generation_service import generate_grounded_answer
    from app.services.audit_service import write_ai_interaction_audit
    from app.services.knowledge_retrieval_service import retrieve_relevant_chunks

    client = TestClient(app)

    health = require_ok(client.get("/health"), "Health check")
    print(f"Health: {health}")

    with SAMPLE_PATH.open("rb") as sample_file:
        ingest = require_ok(
            client.post(
                "/api/v1/ingest/file",
                files={"file": (SAMPLE_PATH.name, sample_file, "text/plain")},
                data={
                    "source_type": "SAMPLE",
                    "capability_status": "UNKNOWN",
                    "title": "Sample Platform Doctrine / Smoke Test Document",
                },
            ),
            "Sample ingestion",
        )
    print(f"Ingestion: {ingest}")
    print(f"Duplicate flag: {ingest['duplicate']}")

    question = "What is Minerva allowed to do?"
    with SessionLocal() as db:
        session = KnowledgeChatSession(Title="Local SQL Server smoke test")
        db.add(session)
        db.flush()
        db.add(
            KnowledgeChatMessage(
                KnowledgeChatSessionId=session.KnowledgeChatSessionId,
                Role=normalize_chat_role(ChatRole.USER.value),
                Content=question,
            )
        )
        db.flush()
        retrieved_chunks = retrieve_relevant_chunks(db=db, query=question, include_samples=True)
        answer, sources, model_name, prompt_policy = generate_grounded_answer(question, retrieved_chunks)
        db.add(
            KnowledgeChatMessage(
                KnowledgeChatSessionId=session.KnowledgeChatSessionId,
                Role=normalize_chat_role(ChatRole.ASSISTANT.value),
                Content=answer,
            )
        )
        db.flush()
        audit = write_ai_interaction_audit(
            db=db,
            user_question=question,
            response_text=answer,
            source_references=sources,
            model_name=model_name,
            prompt_policy=prompt_policy,
            chat_session_id=session.KnowledgeChatSessionId,
        )
        db.commit()

    print(f"Chat answer: {answer}")
    print(f"Source reference count: {len(sources)}")
    print(f"Audit id: {audit.AIInteractionAuditId}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
