from dataclasses import asdict, dataclass
from typing import Any


REFUSAL_RETRIEVAL_DECISIONS = {
    "REFUSE_MISSING_ANSWER_USE_PERMISSION": "REFUSE_NOT_ANSWER_APPROVED",
    "REFUSE_MISSING_RETRIEVAL_ELIGIBILITY": "REFUSE_RETRIEVAL_NOT_ELIGIBLE",
    "REFUSE_MISSING_PROVENANCE": "REFUSE_MISSING_PROVENANCE",
    "REFUSE_CONFLICTED_EVIDENCE": "REFUSE_CONFLICTED_EVIDENCE",
    "REFUSE_SUPERSEDED_EVIDENCE": "REFUSE_SUPERSEDED_EVIDENCE",
    "REFUSE_HISTORICAL_CONTEXT_NOT_CURRENT_TRUTH": "REFUSE_INSUFFICIENT_GOVERNED_EVIDENCE",
    "REFUSE_NOT_ANSWERABLE": "REFUSE_NOT_ANSWER_APPROVED",
}
PROVENANCE_BLOCKERS = {"", "MISSING", "INCOMPLETE"}
CONFLICT_BLOCKERS = {"UNRESOLVED", "CONFLICTED"}
NOT_ANSWERABLE_VALUES = {"NOT_ANSWERABLE", "UNANSWERABLE", "NO_ANSWER_USE"}


@dataclass(frozen=True)
class HistoricalAnswerSynthesisEnforcementResponse:
    AnswerSynthesisSkeletonImplemented: bool
    LiveLLMCalled: bool
    FinalAnswerGenerated: bool
    ChatExposed: bool
    RetrievalRuntimeCalled: bool
    CorpusMutationPerformed: bool
    DatabaseReadPerformed: bool
    DatabaseWritePerformed: bool
    EndpointUIPresent: bool
    AnswerModeDecision: str
    AllowedAnswerMode: str | None
    RefusalRequired: bool
    RefusalReason: str | None
    CitationRequired: bool
    CaveatRequired: bool
    RuntimeBoundaryAsserted: bool
    Guardrails: tuple[str, ...]
    NonGoals: tuple[str, ...]
    Explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


GUARDRAILS = (
    "in-memory metadata evaluation only",
    "no live retrieval backend",
    "no live LLM call",
    "no final chat answer generation",
    "no endpoint or UI",
    "no chat exposure",
    "no corpus mutation",
    "no database read or write",
)

NON_GOALS = (
    "live answer synthesis runtime",
    "source content ingestion",
    "operational corpus mutation",
    "Code Evidence ingestion",
    "current-truth promotion",
    "runtime answer-use activation",
    "runtime retrieval activation",
    "citation rendering runtime",
)


def evaluate_historical_answer_synthesis_enforcement(
    retrieval_gate_output: dict[str, Any] | object,
) -> dict[str, Any]:
    retrieval_decision = _normalized(retrieval_gate_output, "RetrievalDecision")
    expected_answer_mode = _normalized(retrieval_gate_output, "ExpectedAnswerMode")
    answer_mode = _normalized(retrieval_gate_output, "AnswerMode")
    evidence_scope = _normalized(retrieval_gate_output, "EvidenceScope")
    provenance_status = _normalized(retrieval_gate_output, "ProvenanceStatus")
    citation_status = _normalized(retrieval_gate_output, "CitationStatus")
    conflict_status = _normalized(retrieval_gate_output, "ConflictStatus")
    supersession_status = _normalized(retrieval_gate_output, "SupersessionStatus")
    source_id = _value(retrieval_gate_output, "SourceId")

    citation_required = _bool_value(retrieval_gate_output, "CitationRequired", True)
    caveat_required = _bool_value(retrieval_gate_output, "CaveatRequired", False)
    refusal_reason = _string_or_none(_value(retrieval_gate_output, "RefusalReason"))

    if retrieval_decision == "BLOCKED_RUNTIME_NOT_IMPLEMENTED" or _runtime_requested(
        retrieval_gate_output
    ):
        return _response(
            decision="BLOCKED_RUNTIME_NOT_IMPLEMENTED",
            allowed_answer_mode=None,
            refusal_required=True,
            reason=refusal_reason or "RUNTIME_NOT_IMPLEMENTED",
            citation_required=citation_required,
            caveat_required=caveat_required,
            explanation="Runtime answer synthesis is not implemented; this skeleton only evaluates supplied retrieval metadata in-memory.",
        )

    if _not_answerable(evidence_scope, answer_mode, expected_answer_mode):
        return _response(
            decision="REFUSE_NOT_ANSWER_APPROVED",
            allowed_answer_mode=None,
            refusal_required=True,
            reason=refusal_reason or "EVIDENCE_NOT_ANSWERABLE",
            citation_required=citation_required,
            caveat_required=caveat_required,
            explanation="Evidence is marked not answerable and cannot reach answer synthesis.",
        )

    mapped_refusal = REFUSAL_RETRIEVAL_DECISIONS.get(retrieval_decision)
    if mapped_refusal:
        return _response(
            decision=mapped_refusal,
            allowed_answer_mode=None,
            refusal_required=True,
            reason=refusal_reason or mapped_refusal,
            citation_required=citation_required,
            caveat_required=caveat_required,
            explanation="Retrieval gate refusal is preserved by the answer synthesis enforcement skeleton.",
        )

    if conflict_status in CONFLICT_BLOCKERS:
        return _response(
            decision="REFUSE_CONFLICTED_EVIDENCE",
            allowed_answer_mode=None,
            refusal_required=True,
            reason=refusal_reason or "CONFLICTED_EVIDENCE_CANNOT_SUPPORT_SETTLED_ANSWER",
            citation_required=citation_required,
            caveat_required=True,
            explanation="Conflicted evidence cannot produce a settled or current-truth answer.",
        )

    if supersession_status == "SUPERSEDED" and _requests_current_truth(
        expected_answer_mode, answer_mode, retrieval_decision
    ):
        return _response(
            decision="REFUSE_SUPERSEDED_EVIDENCE",
            allowed_answer_mode=None,
            refusal_required=True,
            reason=refusal_reason or "SUPERSEDED_EVIDENCE_CANNOT_ANSWER_CURRENT_TRUTH",
            citation_required=citation_required,
            caveat_required=caveat_required,
            explanation="Superseded evidence cannot produce a current-truth answer.",
        )

    if citation_required and (
        source_id in (None, "")
        or provenance_status in PROVENANCE_BLOCKERS
        or (
            _value(retrieval_gate_output, "CitationStatus") is not None
            and citation_status in PROVENANCE_BLOCKERS
        )
    ):
        return _response(
            decision="REFUSE_CITATION_REQUIRED",
            allowed_answer_mode=None,
            refusal_required=True,
            reason=refusal_reason or "CITATION_OR_PROVENANCE_REQUIRED_BEFORE_ANSWER",
            citation_required=True,
            caveat_required=caveat_required,
            explanation="Citation/provenance enforcement is pending; missing citation metadata blocks answer mode allowance.",
        )

    if retrieval_decision == "ELIGIBLE_CURRENT_TRUTH_RETRIEVAL":
        return _response(
            decision="CURRENT_TRUTH_ANSWER_ALLOWED",
            allowed_answer_mode="CURRENT_TRUTH",
            refusal_required=False,
            reason=None,
            citation_required=citation_required,
            caveat_required=caveat_required,
            explanation="Current-truth retrieval gate output may proceed to a current-truth answer mode decision only.",
        )

    if retrieval_decision == "ELIGIBLE_HISTORICAL_CONTEXT_RETRIEVAL":
        return _response(
            decision="HISTORICAL_CONTEXT_ANSWER_ALLOWED",
            allowed_answer_mode="HISTORICAL_CONTEXT",
            refusal_required=False,
            reason=None,
            citation_required=citation_required,
            caveat_required=True if caveat_required or evidence_scope else True,
            explanation="Historical-context retrieval gate output may proceed only with historical label/caveat behaviour preserved.",
        )

    if retrieval_decision == "ELIGIBLE_CAVEATED_RETRIEVAL":
        return _response(
            decision="CAVEATED_ANSWER_ALLOWED",
            allowed_answer_mode="CAVEATED",
            refusal_required=False,
            reason=None,
            citation_required=citation_required,
            caveat_required=True,
            explanation="Caveated retrieval gate output may proceed only with CaveatRequired preserved.",
        )

    if _requests_context_only(expected_answer_mode, answer_mode, evidence_scope):
        return _response(
            decision="CONTEXT_ONLY_ANSWER_ALLOWED",
            allowed_answer_mode="CONTEXT_ONLY",
            refusal_required=False,
            reason=None,
            citation_required=citation_required,
            caveat_required=True if caveat_required else caveat_required,
            explanation="Context-only metadata may proceed only as labelled context and not as current truth.",
        )

    return _response(
        decision="REFUSE_INSUFFICIENT_GOVERNED_EVIDENCE",
        allowed_answer_mode=None,
        refusal_required=True,
        reason=refusal_reason or "NO_ALLOWED_ANSWER_SYNTHESIS_PATH",
        citation_required=citation_required,
        caveat_required=caveat_required,
        explanation="No approved in-memory metadata-only answer synthesis path matched.",
    )


def _response(
    decision: str,
    allowed_answer_mode: str | None,
    refusal_required: bool,
    reason: str | None,
    citation_required: bool,
    caveat_required: bool,
    explanation: str,
) -> dict[str, Any]:
    return HistoricalAnswerSynthesisEnforcementResponse(
        AnswerSynthesisSkeletonImplemented=True,
        LiveLLMCalled=False,
        FinalAnswerGenerated=False,
        ChatExposed=False,
        RetrievalRuntimeCalled=False,
        CorpusMutationPerformed=False,
        DatabaseReadPerformed=False,
        DatabaseWritePerformed=False,
        EndpointUIPresent=False,
        AnswerModeDecision=decision,
        AllowedAnswerMode=allowed_answer_mode,
        RefusalRequired=refusal_required,
        RefusalReason=reason,
        CitationRequired=citation_required,
        CaveatRequired=caveat_required,
        RuntimeBoundaryAsserted=True,
        Guardrails=GUARDRAILS,
        NonGoals=NON_GOALS,
        Explanation=explanation,
    ).to_dict()


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
    return str(value).strip().lower() in {"true", "yes", "y", "1", "approved"}


def _string_or_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


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
        )
    )


def _not_answerable(
    evidence_scope: str,
    answer_mode: str,
    expected_answer_mode: str,
) -> bool:
    return (
        evidence_scope in NOT_ANSWERABLE_VALUES
        or answer_mode in NOT_ANSWERABLE_VALUES
        or expected_answer_mode in NOT_ANSWERABLE_VALUES
    )


def _requests_current_truth(
    expected_answer_mode: str,
    answer_mode: str,
    retrieval_decision: str,
) -> bool:
    return (
        "CURRENT_TRUTH" in expected_answer_mode
        or "CURRENT_TRUTH" in answer_mode
        or retrieval_decision == "ELIGIBLE_CURRENT_TRUTH_RETRIEVAL"
    )


def _requests_context_only(
    expected_answer_mode: str,
    answer_mode: str,
    evidence_scope: str,
) -> bool:
    return any(
        marker in value
        for value in (expected_answer_mode, answer_mode, evidence_scope)
        for marker in ("CONTEXT_ONLY", "BACKLOG_CONTEXT", "DOCTRINE_CONTEXT")
    )
