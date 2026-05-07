import json

from sqlalchemy.orm import Session

from app.models.audit import AIInteractionAudit
from app.schemas.common import SourceReference


def write_ai_interaction_audit(
    db: Session,
    user_question: str,
    response_text: str,
    source_references: list[SourceReference],
    model_name: str,
    prompt_policy: str,
    tenant_id: str | None = None,
    user_id: str | None = None,
    chat_session_id: str | None = None,
) -> AIInteractionAudit:
    chunk_ids = [source.chunk_id for source in source_references]
    document_ids = sorted({source.document_id for source in source_references})
    audit = AIInteractionAudit(
        TenantId=tenant_id,
        UserId=user_id,
        KnowledgeChatSessionId=chat_session_id,
        UserQuestion=user_question,
        RetrievedChunkIdsJson=json.dumps(chunk_ids),
        RetrievedDocumentIdsJson=json.dumps(document_ids),
        SourceReferencesJson=json.dumps([source.model_dump() for source in source_references]),
        ModelName=model_name,
        PromptPolicy=prompt_policy,
        ResponseText=response_text,
    )
    db.add(audit)
    db.flush()
    return audit
