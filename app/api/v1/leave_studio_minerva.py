from fastapi import APIRouter, HTTPException

from app.schemas.leave_studio_minerva import LeaveStudioAnswerResponse, LeaveStudioQuestionRequest
from app.services.leave_studio_answer_planner import LeaveStudioContractError
from app.services.leave_studio_question_service import ask_leave_studio_question


router = APIRouter()


@router.post("/leave-studio/questions", response_model=LeaveStudioAnswerResponse)
def ask_governed_leave_studio_question(request: LeaveStudioQuestionRequest) -> LeaveStudioAnswerResponse:
    try:
        return ask_leave_studio_question(request)
    except LeaveStudioContractError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
