from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.enums import ChatRole, normalize_chat_role
from app.db.session import get_db
from app.models.chat import KnowledgeChatMessage, KnowledgeChatSession
from app.schemas.chat import ChatMessageRequest, ChatMessageResponse, ChatSessionCreate, ChatSessionResponse
from app.services.answer_generation_service import generate_grounded_answer
from app.services.audit_service import write_ai_interaction_audit
from app.services.domain_retrieval_plan_service import retrieve_chunks_for_question

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
    if request.tenant_id is not None and request.tenant_id != session.TenantId:
        raise HTTPException(status_code=400, detail="tenant_id does not match the chat session.")
    if request.user_id is not None and request.user_id != session.UserId:
        raise HTTPException(status_code=400, detail="user_id does not match the chat session.")

    user_message = KnowledgeChatMessage(
        KnowledgeChatSessionId=request.session_id,
        Role=normalize_chat_role(ChatRole.USER.value),
        Content=request.message,
    )
    db.add(user_message)
    db.flush()

    retrieved_chunks = retrieve_chunks_for_question(db=db, query=request.message, tenant_id=session.TenantId)
    answer, sources, model_name, prompt_policy = generate_grounded_answer(request.message, retrieved_chunks)

    assistant_message = KnowledgeChatMessage(
        KnowledgeChatSessionId=request.session_id,
        Role=normalize_chat_role(ChatRole.ASSISTANT.value),
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
        tenant_id=session.TenantId,
        user_id=session.UserId,
        chat_session_id=request.session_id,
    )
    db.commit()
    db.refresh(audit)

    return ChatMessageResponse(answer=answer, sources=sources, audit_id=audit.AIInteractionAuditId)
