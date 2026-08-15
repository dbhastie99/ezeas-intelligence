import secrets
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException

from app.core.config import get_settings
from app.schemas.award_execution_minerva import (
    AwardExecutionPrincipal,
    AwardExecutionMinervaQuestionRequest,
    AwardExecutionMinervaQuestionResponse,
)
from app.services.award_execution_question_service import ask_award_execution_question
from app.services.workforce_award_evidence_client import (
    AwardExecutionEvidenceInvalid,
    AwardExecutionEvidenceNotFound,
    AwardExecutionEvidenceProvider,
    AwardExecutionEvidenceUnavailable,
    AwardExecutionExactVersionMismatch,
    get_award_execution_evidence_provider,
)


router = APIRouter()


def authenticated_award_execution_principal(
    authorization: str | None = Header(default=None),
    x_account_id: str | None = Header(default=None, alias="X-Account-Id"),
) -> AwardExecutionPrincipal:
    configured_token = get_settings().award_execution_inbound_service_token
    if not configured_token:
        raise HTTPException(
            status_code=503,
            detail="Award execution inbound authentication is not configured",
        )
    scheme, _, supplied_token = (authorization or "").partition(" ")
    if scheme.lower() != "bearer" or not supplied_token or not secrets.compare_digest(
        supplied_token,
        configured_token,
    ):
        raise HTTPException(
            status_code=401,
            detail="authenticated Award execution service principal required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        account_id = UUID(x_account_id or "")
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="valid X-Account-Id UUID required") from exc
    return AwardExecutionPrincipal(accountId=account_id)


def configured_award_execution_evidence_provider() -> AwardExecutionEvidenceProvider:
    try:
        return get_award_execution_evidence_provider()
    except AwardExecutionEvidenceUnavailable as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.post("/award-execution/questions", response_model=AwardExecutionMinervaQuestionResponse)
def ask_stored_award_execution_question(
    request: AwardExecutionMinervaQuestionRequest,
    principal: AwardExecutionPrincipal = Depends(authenticated_award_execution_principal),
    evidence_provider: AwardExecutionEvidenceProvider = Depends(
        configured_award_execution_evidence_provider
    ),
) -> AwardExecutionMinervaQuestionResponse:
    try:
        return ask_award_execution_question(request, evidence_provider, str(principal.accountId))
    except AwardExecutionEvidenceNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AwardExecutionExactVersionMismatch as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except AwardExecutionEvidenceInvalid as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except AwardExecutionEvidenceUnavailable as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
