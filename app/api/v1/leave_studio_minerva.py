from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.leave_studio_minerva import (
    LeaveStudioAnswerResponse,
    LeaveStudioConversationRequest,
    LeaveStudioConversationResponse,
    LeaveStudioQuestionRequest,
)
from app.services.leave_studio_conversation_service import (
    ConversationValidationFailure,
    ask_leave_studio_conversation,
)
from app.services.leave_studio_answer_planner import LeaveStudioContractError
from app.services.leave_studio_question_service import ask_leave_studio_question


router = APIRouter()


@router.post("/leave-studio/questions", response_model=LeaveStudioAnswerResponse)
def ask_governed_leave_studio_question(request: LeaveStudioQuestionRequest) -> LeaveStudioAnswerResponse:
    try:
        return ask_leave_studio_question(request)
    except LeaveStudioContractError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/leave-studio/conversations", response_model=LeaveStudioConversationResponse)
def ask_governed_leave_studio_conversation(
    request: LeaveStudioConversationRequest,
    db: Session = Depends(get_db),
) -> LeaveStudioConversationResponse:
    try:
        response = ask_leave_studio_conversation(request, db=db)
        db.commit()
        return response
    except ConversationValidationFailure as exc:
        db.rollback()
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception:
        db.rollback()
        raise
