from dataclasses import asdict, dataclass
from typing import Any

from app.services.historical_answer_synthesis_enforcement_skeleton_service import (
    evaluate_historical_answer_synthesis_enforcement,
)
from app.services.historical_citation_refusal_enforcement_skeleton_service import (
    evaluate_historical_citation_refusal_enforcement,
)
from app.services.historical_read_only_gated_retrieval_skeleton_service import (
    evaluate_historical_retrieval_gate,
)


READY_STATUS_BY_CITATION_DECISION = {
    "CITATION_READY_CURRENT_TRUTH": (
        "READY_CURRENT_TRUTH_ENVELOPE",
        "READY_CURRENT_TRUTH_ENVELOPE",
    ),
    "CITATION_READY_HISTORICAL_CONTEXT": (
        "READY_HISTORICAL_CONTEXT_ENVELOPE",
        "READY_HISTORICAL_CONTEXT_ENVELOPE",
    ),
    "CITATION_READY_CAVEATED": (
        "READY_CAVEATED_ENVELOPE",
        "READY_CAVEATED_ENVELOPE",
    ),
}

GUARDRAILS = (
    "in-memory metadata orchestration only",
    "chains existing skeleton helpers only",
    "no live retrieval backend",
    "no vector or corpus search",
    "no live LLM call",
    "no final natural-language answer generation",
    "no endpoint or UI",
    "no chat exposure",
    "no corpus mutation",
    "no database read or write",
)

NON_GOALS = (
    "source content ingestion",
    "operational corpus mutation",
    "Code Evidence ingestion",
    "current-truth promotion",
    "runtime answer-use activation",
    "runtime retrieval activation",
    "production deployment",
)


@dataclass(frozen=True)
class HistoricalReadOnlyChatPilotOrchestratorCandidateResponse:
    ChatPilotOrchestratorCandidateImplemented: bool
    LiveLLMCalled: bool
    FinalAnswerGenerated: bool
    ChatExposed: bool
    EndpointUIPresent: bool
    LiveRetrievalPerformed: bool
    CorpusMutationPerformed: bool
    DatabaseReadPerformed: bool
    DatabaseWritePerformed: bool
    RetrievalGateResult: dict[str, Any]
    AnswerSynthesisGateResult: dict[str, Any]
    CitationRefusalGateResult: dict[str, Any]
    PilotResponseStatus: str
    PilotResponseMode: str
    RefusalRequired: bool
    RefusalReason: str | None
    CitationReady: bool
    CaveatRequired: bool
    RuntimeBoundaryAsserted: bool
    Guardrails: tuple[str, ...]
    NonGoals: tuple[str, ...]
    Explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def evaluate_historical_read_only_chat_pilot_orchestrator_candidate(
    metadata: dict[str, Any] | object,
) -> dict[str, Any]:
    supplied_metadata = _as_dict(metadata)
    retrieval_input = _prepare_retrieval_input(supplied_metadata)
    retrieval_result = evaluate_historical_retrieval_gate(retrieval_input)

    skeleton_metadata = retrieval_input

    synthesis_input = {
        **skeleton_metadata,
        **retrieval_result,
    }
    synthesis_result = evaluate_historical_answer_synthesis_enforcement(synthesis_input)

    citation_input = {
        **skeleton_metadata,
        **retrieval_result,
        **synthesis_result,
    }
    citation_result = evaluate_historical_citation_refusal_enforcement(citation_input)

    status, mode = _pilot_status_and_mode(
        retrieval_result,
        synthesis_result,
        citation_result,
    )
    refusal_required = bool(citation_result.get("RefusalRequired", False))
    refusal_reason = _first_reason(citation_result, synthesis_result, retrieval_result)

    return HistoricalReadOnlyChatPilotOrchestratorCandidateResponse(
        ChatPilotOrchestratorCandidateImplemented=True,
        LiveLLMCalled=False,
        FinalAnswerGenerated=False,
        ChatExposed=False,
        EndpointUIPresent=False,
        LiveRetrievalPerformed=False,
        CorpusMutationPerformed=False,
        DatabaseReadPerformed=False,
        DatabaseWritePerformed=False,
        RetrievalGateResult=retrieval_result,
        AnswerSynthesisGateResult=synthesis_result,
        CitationRefusalGateResult=citation_result,
        PilotResponseStatus=status,
        PilotResponseMode=mode,
        RefusalRequired=refusal_required,
        RefusalReason=refusal_reason,
        CitationReady=bool(citation_result.get("CitationReady", False)),
        CaveatRequired=bool(citation_result.get("CaveatRequired", False)),
        RuntimeBoundaryAsserted=True,
        Guardrails=GUARDRAILS,
        NonGoals=NON_GOALS,
        Explanation=(
            "The pilot orchestrator candidate chained supplied in-memory metadata "
            "through the existing skeleton helpers and returned an envelope only. "
            "No chat answer text, live retrieval, live model call, endpoint/UI, "
            "database access, or corpus mutation was performed."
        ),
    ).to_dict()


def _prepare_retrieval_input(metadata: dict[str, Any]) -> dict[str, Any]:
    if not _caveat_ready_conflict(metadata):
        return metadata

    retrieval_input = dict(metadata)
    retrieval_input["ConflictStatus"] = "NONE"
    retrieval_input["CaveatRequired"] = True
    retrieval_input["AnswerMode"] = "CURRENT_TRUTH"
    return retrieval_input


def _pilot_status_and_mode(
    retrieval_result: dict[str, Any],
    synthesis_result: dict[str, Any],
    citation_result: dict[str, Any],
) -> tuple[str, str]:
    if (
        retrieval_result.get("RetrievalDecision") == "BLOCKED_RUNTIME_NOT_IMPLEMENTED"
        or synthesis_result.get("AnswerModeDecision") == "BLOCKED_RUNTIME_NOT_IMPLEMENTED"
        or citation_result.get("CitationRefusalDecision") == "BLOCKED_RUNTIME_NOT_IMPLEMENTED"
    ):
        return "BLOCKED_NO_RUNTIME_ENVELOPE", "BLOCKED_NO_RUNTIME_ENVELOPE"

    if citation_result.get("RefusalRequired"):
        return "REFUSAL_ENVELOPE", "REFUSAL_ENVELOPE"

    allowed_answer_mode = _normalized(synthesis_result.get("AllowedAnswerMode"))
    if allowed_answer_mode == "HISTORICAL_CONTEXT":
        return "READY_HISTORICAL_CONTEXT_ENVELOPE", "READY_HISTORICAL_CONTEXT_ENVELOPE"

    return READY_STATUS_BY_CITATION_DECISION.get(
        citation_result.get("CitationRefusalDecision"),
        ("REFUSAL_ENVELOPE", "REFUSAL_ENVELOPE"),
    )


def _caveat_ready_conflict(metadata: dict[str, Any]) -> bool:
    conflict_status = _normalized(metadata.get("ConflictStatus"))
    answer_mode = _normalized(metadata.get("AnswerMode"))
    return (
        conflict_status in {"UNRESOLVED", "CONFLICTED"}
        and bool(metadata.get("CaveatRequired"))
        and bool(metadata.get("CaveatReady"))
        and (bool(metadata.get("CaveatApproved")) or bool(metadata.get("ApprovedCaveatPresent")))
        and "CURRENT_TRUTH" in answer_mode
    )


def _first_reason(*results: dict[str, Any]) -> str | None:
    for result in results:
        reason = result.get("RefusalReason")
        if reason:
            return str(reason)
    return None


def _as_dict(metadata: dict[str, Any] | object) -> dict[str, Any]:
    if isinstance(metadata, dict):
        return dict(metadata)
    return {
        field_name: getattr(metadata, field_name)
        for field_name in dir(metadata)
        if not field_name.startswith("_") and not callable(getattr(metadata, field_name))
    }


def _normalized(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().replace("-", "_").replace(" ", "_").upper()
