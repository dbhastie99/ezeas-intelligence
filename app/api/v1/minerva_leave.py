from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.minerva_leave import (
    LeaveAskRequest,
    LeaveAskResponse,
    LeaveProposalRequest,
    LeaveProposalResponse,
)
from app.services.governed_knowledge_pack_service import (
    PackNotIngestedError,
    PackValidationError,
    UnsupportedPackRequest,
    ask_published_pack,
)
from app.services.minerva_leave_proposal_service import ProposalRequestError, build_draft_leave_proposal
from app.api.v1.minerva_admin_configuration import router as admin_configuration_router


router = APIRouter()


@router.post("/queensland-general-lsl/ask", response_model=LeaveAskResponse)
def ask_queensland_general_lsl(request: LeaveAskRequest, db: Session = Depends(get_db)) -> LeaveAskResponse:
    try:
        return ask_published_pack(
            db=db,
            question=request.message,
            pack_key=request.pack_key,
            semantic_version=request.semantic_version,
            persist_audit=True,
        )
    except PackNotIngestedError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except (PackValidationError, UnsupportedPackRequest) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/queensland-general-lsl/proposal", response_model=LeaveProposalResponse)
def draft_queensland_general_lsl_proposal(request: LeaveProposalRequest) -> LeaveProposalResponse:
    try:
        return build_draft_leave_proposal(
            context=request.context,
            requested_change=request.requested_change,
            fact_ids=request.fact_ids,
            pack_key=request.pack_key,
            semantic_version=request.semantic_version,
            answer_plan=request.answer_plan,
        )
    except (PackValidationError, UnsupportedPackRequest, ProposalRequestError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


router.include_router(
    admin_configuration_router,
    tags=["governed-queensland-lsl-administrator-configuration"],
)
