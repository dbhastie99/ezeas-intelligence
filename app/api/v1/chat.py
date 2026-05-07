from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.chat import KnowledgeChatMessage, KnowledgeChatSession
from app.schemas.chat import ChatMessageRequest, ChatMessageResponse, ChatSessionCreate, ChatSessionResponse
from app.services.answer_generation_service import generate_grounded_answer
from app.services.audit_service import write_ai_interaction_audit
from app.services.knowledge_retrieval_service import retrieve_relevant_chunks

router = APIRouter()


@router.post("/session", response_model=ChatSessionResponse)
def create_chat_session(request: ChatSessionCreate, db: Session = Depends(get_db)) -> ChatSessionResponse:
    session = KnowledgeChatSession(TenantId=request.tenant_id, UserId=request.user_id, Title=request.title)
    db.add(session)
    db.commit()
    db.refresh(session)
    return ChatSessionResponse(session_id=session.KnowledgeChatSessionId)


@router.post("/message", response_model=ChatMessageResponse)
def create_chat_message(request: ChatMessageRequest, db: Session = Depends(get_db)) -> ChatMessageResponse:
    session = db.get(KnowledgeChatSession, request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found.")

    user_message = KnowledgeChatMessage(
        KnowledgeChatSessionId=request.session_id,
        Role="USER",
        Content=request.message,
    )
    db.add(user_message)
    db.flush()

    retrieved_chunks = retrieve_relevant_chunks(db=db, query=request.message, tenant_id=request.tenant_id)
    answer, sources, model_name, prompt_policy = generate_grounded_answer(request.message, retrieved_chunks)

    assistant_message = KnowledgeChatMessage(
        KnowledgeChatSessionId=request.session_id,
        Role="ASSISTANT",
        Content=answer,
    )
    db.add(assistant_message)
    db.flush()

    audit = write_ai_interaction_audit(
        db=db,
        user_question=request.message,
        response_text=answer,
        source_references=sources,
        model_name=model_name,
        prompt_policy=prompt_policy,
        tenant_id=request.tenant_id,
        user_id=request.user_id,
        chat_session_id=request.session_id,
    )
    db.commit()
    db.refresh(audit)

    return ChatMessageResponse(answer=answer, sources=sources, audit_id=audit.AIInteractionAuditId)
