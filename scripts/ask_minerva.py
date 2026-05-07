import argparse
import os
import sys
from pathlib import Path

from sqlalchemy.exc import SQLAlchemyError

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Ask Minerva against the configured local knowledge database.")
    parser.add_argument("question")
    parser.add_argument("--source-type", action="append", default=None)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--include-samples", action="store_true", help="Include SAMPLE documents in retrieval.")
    args = parser.parse_args()

    if not configured_database_url():
        print("MINERVA_DATABASE_URL is not set. Copy .env.example to .env and configure SQL Server first.")
        return 2

    from app.core.enums import ChatRole, normalize_chat_role
    from app.db.session import SessionLocal
    from app.models.chat import KnowledgeChatMessage, KnowledgeChatSession
    from app.services.answer_generation_service import generate_grounded_answer
    from app.services.audit_service import write_ai_interaction_audit
    from app.services.knowledge_retrieval_service import retrieve_relevant_chunks

    try:
        with SessionLocal() as db:
            session = KnowledgeChatSession(Title="ask_minerva.py")
            db.add(session)
            db.flush()

            db.add(
                KnowledgeChatMessage(
                    KnowledgeChatSessionId=session.KnowledgeChatSessionId,
                    Role=normalize_chat_role(ChatRole.USER.value),
                    Content=args.question,
                )
            )
            db.flush()

            retrieved_chunks = retrieve_relevant_chunks(
                db=db,
                query=args.question,
                tenant_id=session.TenantId,
                top_k=args.top_k,
                source_types=args.source_type,
                include_samples=args.include_samples,
            )
            answer, sources, model_name, prompt_policy = generate_grounded_answer(args.question, retrieved_chunks)

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
                user_question=args.question,
                response_text=answer,
                source_references=sources,
                model_name=model_name,
                prompt_policy=prompt_policy,
                chat_session_id=session.KnowledgeChatSessionId,
            )
            db.commit()

            print("Answer:")
            print(answer)
            print()
            print("Sources:")
            for index, source in enumerate(sources, start=1):
                print(
                    f"{index}. title={source.title!r} source_type={source.source_type} "
                    f"score={source.score} matched_tokens={source.matched_tokens}"
                )
                if source.matched_phrases:
                    print(f"   matched_phrases={source.matched_phrases}")
                if source.match_reason:
                    print(f"   match_reason={source.match_reason}")
                print(f"   chunk_id={source.chunk_id} document_id={source.document_id} chunk_index={source.chunk_index}")
                print(f"   snippet={source.snippet}")
            print()
            print(f"Audit id: {audit.AIInteractionAuditId}")
    except (SQLAlchemyError, ValueError) as exc:
        print(f"ask_minerva failed: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
