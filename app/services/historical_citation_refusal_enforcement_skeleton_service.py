from dataclasses import asdict, dataclass
from typing import Any


CONFLICT_BLOCKERS = {"UNRESOLVED", "CONFLICTED"}
CURRENT_TRUTH_MODES = {"CURRENT_TRUTH", "CAVEATED_CURRENT_TRUTH", "CURRENT"}
HISTORICAL_CONTEXT_MODES = {"HISTORICAL_CONTEXT", "HISTORICAL_CONTEXT_ONLY", "HISTORICAL"}
CAVEATED_MODES = {"CAVEATED", "CAVEATED_CURRENT_TRUTH"}
NOT_ANSWER_APPROVED_DECISIONS = {
    "",
    "REFUSE_NOT_ANSWER_APPROVED",
    "REFUSE_INSUFFICIENT_GOVERNED_EVIDENCE",
}


@dataclass(frozen=True)
class HistoricalCitationRefusalEnforcementResponse:
    CitationRefusalSkeletonImplemented: bool
    CitationRefusalDecision: str
    CitationReady: bool
    RefusalRequired: bool
    RefusalReason: str | None
    CitationEnvelopePrepared: bool
    FinalAnswerGenerated: bool
    LiveLLMCalled: bool
    ChatExposed: bool
    RetrievalRuntimeCalled: bool
    CorpusMutationPerformed: bool
    DatabaseReadPerformed: bool
    DatabaseWritePerformed: bool
    EndpointUIPresent: bool
    RequiredCitationFieldsPresent: bool
    MissingCitationFields: tuple[str, ...]
    CaveatRequired: bool
    CaveatReady: bool
    RuntimeBoundaryAsserted: bool
    Guardrails: tuple[str, ...]
    NonGoals: tuple[str, ...]
    Explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


GUARDRAILS = (
    "in-memory metadata evaluation only",
    "consumes supplied answer synthesis skeleton output only",
    "no live retrieval backend",
    "no live LLM call",
    "no final chat answer generation",
    "no citation rendering runtime",
    "no endpoint or UI",
    "no chat exposure",
    "no corpus mutation",
    "no database read or write",
)

NON_GOALS = (
    "live answer generation",
    "citation rendering runtime",
    "source content ingestion",
    "operational corpus mutation",
    "Code Evidence ingestion",
    "current-truth promotion",
    "runtime answer-use activation",
    "runtime retrieval activation",
    "endpoint or UI exposure",
)


def evaluate_historical_citation_refusal_enforcement(
    answer_synthesis_output: dict[str, Any] | object,
) -> dict[str, Any]:
    citation_required = _bool_value(answer_synthesis_output, "CitationRequired", True)
    caveat_required = _bool_value(answer_synthesis_output, "CaveatRequired", False)
    caveat_ready = _bool_value(
        answer_synthesis_output,
        "CaveatReady",
        not caveat_required,
    )
    refusal_reason = _string_or_none(_value(answer_synthesis_output, "RefusalReason"))

    if _runtime_requested(answer_synthesis_output):
        return _response(
            decision="BLOCKED_RUNTIME_NOT_IMPLEMENTED",
            citation_ready=False,
            refusal_required=True,
            reason=refusal_reason or "RUNTIME_NOT_IMPLEMENTED",
            missing_fields=(),
            caveat_required=caveat_required,
            caveat_ready=caveat_ready,
            explanation="Runtime citation/refusal handling is not implemented; this skeleton only evaluates supplied answer synthesis metadata in-memory.",
        )

    if _bool_value(answer_synthesis_output, "RefusalRequired", False):
        return _response(
            decision="REFUSE_PRIOR_GATE_REFUSAL",
            citation_ready=False,
            refusal_required=True,
            reason=refusal_reason or "PRIOR_GATE_REFUSAL",
            missing_fields=(),
            caveat_required=caveat_required,
            caveat_ready=caveat_ready,
            explanation="Prior answer synthesis refusal is preserved by the citation/refusal enforcement skeleton.",
        )

    answer_mode_decision = _normalized(answer_synthesis_output, "AnswerModeDecision")
    allowed_answer_mode = _normalized(answer_synthesis_output, "AllowedAnswerMode")
    answer_mode = _normalized(answer_synthesis_output, "AnswerMode")
    conflict_status = _normalized(answer_synthesis_output, "ConflictStatus")
    supersession_status = _normalized(answer_synthesis_output, "SupersessionStatus")

    if _not_answer_approved(answer_mode_decision, allowed_answer_mode):
        return _response(
            decision="REFUSE_NOT_ANSWER_APPROVED",
            citation_ready=False,
            refusal_required=True,
            reason=refusal_reason or "ANSWER_SYNTHESIS_NOT_APPROVED",
            missing_fields=(),
            caveat_required=caveat_required,
            caveat_ready=caveat_ready,
            explanation="The supplied answer synthesis metadata does not contain an approved non-refusal answer mode.",
        )

    missing_governance_fields = _missing_fields(
        answer_synthesis_output,
        ("AnswerUsePermissionId", "RetrievalEligibilityId", "AnswerModeId"),
    )
    if missing_governance_fields:
        return _response(
            decision="REFUSE_MISSING_GOVERNANCE_CHAIN",
            citation_ready=False,
            refusal_required=True,
            reason=refusal_reason or "MISSING_GOVERNANCE_CHAIN",
            missing_fields=missing_governance_fields,
            caveat_required=caveat_required,
            caveat_ready=caveat_ready,
            explanation="A non-refusal answer requires answer-use permission, retrieval eligibility, and answer-mode identifiers.",
        )

    if conflict_status in CONFLICT_BLOCKERS and not caveat_ready:
        return _response(
            decision="REFUSE_CONFLICTED_EVIDENCE",
            citation_ready=False,
            refusal_required=True,
            reason=refusal_reason or "CONFLICTED_EVIDENCE_WITHOUT_READY_CAVEAT",
            missing_fields=(),
            caveat_required=True,
            caveat_ready=False,
            explanation="Conflicted or unresolved evidence cannot proceed unless a required caveat is ready.",
        )

    if supersession_status == "SUPERSEDED" and _requests_current_truth(
        allowed_answer_mode,
        answer_mode,
    ):
        return _response(
            decision="REFUSE_SUPERSEDED_EVIDENCE",
            citation_ready=False,
            refusal_required=True,
            reason=refusal_reason or "SUPERSEDED_EVIDENCE_CANNOT_ANSWER_CURRENT_TRUTH",
            missing_fields=(),
            caveat_required=caveat_required,
            caveat_ready=caveat_ready,
            explanation="Superseded evidence cannot proceed to a current-truth citation-ready envelope.",
        )

    missing_citation_fields = _missing_citation_fields(answer_synthesis_output)
    if citation_required and "SourceId" in missing_citation_fields:
        return _response(
            decision="REFUSE_MISSING_SOURCE_ID",
            citation_ready=False,
            refusal_required=True,
            reason=refusal_reason or "MISSING_SOURCE_ID",
            missing_fields=missing_citation_fields,
            caveat_required=caveat_required,
            caveat_ready=caveat_ready,
            explanation="Citation-required metadata is missing SourceId.",
        )

    if citation_required and "SourceTitle" in missing_citation_fields:
        return _response(
            decision="REFUSE_MISSING_SOURCE_TITLE",
            citation_ready=False,
            refusal_required=True,
            reason=refusal_reason or "MISSING_SOURCE_TITLE",
            missing_fields=missing_citation_fields,
            caveat_required=caveat_required,
            caveat_ready=caveat_ready,
            explanation="Citation-required metadata is missing SourceTitle.",
        )

    if citation_required and "SourceDateOrUnknownDateMarker" in missing_citation_fields:
        return _response(
            decision="REFUSE_MISSING_SOURCE_DATE_OR_UNKNOWN_MARKER",
            citation_ready=False,
            refusal_required=True,
            reason=refusal_reason or "MISSING_SOURCE_DATE_OR_UNKNOWN_DATE_MARKER",
            missing_fields=missing_citation_fields,
            caveat_required=True,
            caveat_ready=caveat_ready,
            explanation="Citation-required metadata needs SourceDate or an UnknownDateMarker before a citation-ready envelope can be prepared.",
        )

    decision = _ready_decision(allowed_answer_mode, answer_mode, caveat_required)
    return _response(
        decision=decision,
        citation_ready=True,
        refusal_required=False,
        reason=None,
        missing_fields=(),
        caveat_required=caveat_required,
        caveat_ready=caveat_ready,
        explanation="Required governance and citation/provenance metadata are present for a citation-ready envelope; no final answer text is generated.",
    )


def _response(
    decision: str,
    citation_ready: bool,
    refusal_required: bool,
    reason: str | None,
    missing_fields: tuple[str, ...],
    caveat_required: bool,
    caveat_ready: bool,
    explanation: str,
) -> dict[str, Any]:
    return HistoricalCitationRefusalEnforcementResponse(
        CitationRefusalSkeletonImplemented=True,
        CitationRefusalDecision=decision,
        CitationReady=citation_ready,
        RefusalRequired=refusal_required,
        RefusalReason=reason,
        CitationEnvelopePrepared=citation_ready and not refusal_required,
        FinalAnswerGenerated=False,
        LiveLLMCalled=False,
        ChatExposed=False,
        RetrievalRuntimeCalled=False,
        CorpusMutationPerformed=False,
        DatabaseReadPerformed=False,
        DatabaseWritePerformed=False,
        EndpointUIPresent=False,
        RequiredCitationFieldsPresent=not missing_fields,
        MissingCitationFields=missing_fields,
        CaveatRequired=caveat_required,
        CaveatReady=caveat_ready,
        RuntimeBoundaryAsserted=True,
        Guardrails=GUARDRAILS,
        NonGoals=NON_GOALS,
        Explanation=explanation,
    ).to_dict()


def _missing_citation_fields(metadata: dict[str, Any] | object) -> tuple[str, ...]:
    missing = list(_missing_fields(metadata, ("SourceId", "SourceTitle")))
    if _is_missing(_value(metadata, "SourceDate")) and _is_missing(
        _value(metadata, "UnknownDateMarker")
    ):
        missing.append("SourceDateOrUnknownDateMarker")
    return tuple(missing)


def _missing_fields(
    metadata: dict[str, Any] | object,
    field_names: tuple[str, ...],
) -> tuple[str, ...]:
    return tuple(
        field_name for field_name in field_names if _is_missing(_value(metadata, field_name))
    )


def _ready_decision(
    allowed_answer_mode: str,
    answer_mode: str,
    caveat_required: bool,
) -> str:
    if caveat_required or allowed_answer_mode in CAVEATED_MODES or answer_mode in CAVEATED_MODES:
        return "CITATION_READY_CAVEATED"
    if allowed_answer_mode in HISTORICAL_CONTEXT_MODES or answer_mode in HISTORICAL_CONTEXT_MODES:
        return "CITATION_READY_HISTORICAL_CONTEXT"
    return "CITATION_READY_CURRENT_TRUTH"


def _not_answer_approved(answer_mode_decision: str, allowed_answer_mode: str) -> bool:
    return (
        answer_mode_decision in NOT_ANSWER_APPROVED_DECISIONS
        or answer_mode_decision.startswith("REFUSE_")
        or allowed_answer_mode in {"", "REFUSAL", "NOT_ANSWERABLE", "UNANSWERABLE"}
    )


def _requests_current_truth(allowed_answer_mode: str, answer_mode: str) -> bool:
    return allowed_answer_mode in CURRENT_TRUTH_MODES or answer_mode in CURRENT_TRUTH_MODES


def _runtime_requested(metadata: dict[str, Any] | object) -> bool:
    return any(
        _bool_value(metadata, field_name, False)
        for field_name in (
            "RuntimeRequired",
            "LiveLLMRequired",
            "FinalAnswerRequired",
            "ChatRequired",
            "LiveRetrievalRequired",
            "RetrievalRuntimeRequired",
            "DatabaseReadRequired",
            "DatabaseWriteRequired",
            "EndpointUIRequired",
            "CitationRenderingRequired",
        )
    )


def _normalized(metadata: dict[str, Any] | object, field_name: str) -> str:
    value = _value(metadata, field_name)
    if value is None:
        return ""
    return str(value).strip().replace("-", "_").replace(" ", "_").upper()


def _value(metadata: dict[str, Any] | object, field_name: str) -> Any:
    if isinstance(metadata, dict):
        return metadata.get(field_name)
    return getattr(metadata, field_name, None)


def _bool_value(
    metadata: dict[str, Any] | object,
    field_name: str,
    default: bool,
) -> bool:
    value = _value(metadata, field_name)
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "yes", "y", "1", "approved", "ready"}


def _string_or_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    return False
