from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.minerva_admin_configuration import (
    AdminConfigurationAnswer,
    AdminConfigurationAskRequest,
    AdminConfigurationProposalPreview,
    AdminConfigurationProposalRequest,
)
from app.services.minerva_admin_configuration_service import (
    AdminConfigurationEvidenceError,
    ask_admin_configuration,
    preview_admin_configuration_change,
)


router = APIRouter()


@router.post("/queensland-general-lsl/admin-configuration/ask", response_model=AdminConfigurationAnswer)
def ask_queensland_general_lsl_admin_configuration(
    request: AdminConfigurationAskRequest,
    db: Session = Depends(get_db),
) -> AdminConfigurationAnswer:
    try:
        return ask_admin_configuration(packet=request.packet, question=request.message, db=db, persist_audit=True)
    except AdminConfigurationEvidenceError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/queensland-general-lsl/admin-configuration/proposal", response_model=AdminConfigurationProposalPreview)
def preview_queensland_general_lsl_admin_configuration_change(
    request: AdminConfigurationProposalRequest,
    db: Session = Depends(get_db),
) -> AdminConfigurationProposalPreview:
    try:
        return preview_admin_configuration_change(
            packet=request.packet,
            requested_change=request.requested_change,
            db=db,
            persist_audit=True,
        )
    except AdminConfigurationEvidenceError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
