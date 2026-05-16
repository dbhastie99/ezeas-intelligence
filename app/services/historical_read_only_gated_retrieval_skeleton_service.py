from dataclasses import asdict, dataclass
from typing import Any


ANSWER_USE_BLOCKERS = {"", "MISSING", "BLOCK", "BLOCKED", "REVOKED", "REJECTED", "SUPERSEDED"}
RETRIEVAL_BLOCKERS = {"", "MISSING", "BLOCK", "BLOCKED", "REVOKED", "REJECTED", "EXCLUDED"}
PROVENANCE_BLOCKERS = {"", "MISSING", "INCOMPLETE"}
CONFLICT_BLOCKERS = {"UNRESOLVED", "CONFLICTED"}
NOT_ANSWERABLE_VALUES = {"NOT_ANSWERABLE", "UNANSWERABLE", "NO_ANSWER_USE"}


@dataclass(frozen=True)
class HistoricalRetrievalGateResponse:
    RetrievalGateSkeletonImplemented: bool
    LiveRetrievalPerformed: bool
    LiveLLMCalled: bool
    CorpusMutationPerformed: bool
    DatabaseReadPerformed: bool
    DatabaseWritePerformed: bool
    EndpointUIPresent: bool
    RetrievalDecision: str
    RetrievalMode: str
    ExpectedAnswerMode: str
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
    "no corpus mutation",
    "no database read or write",
    "no endpoint or UI",
    "no chat exposure",
)

NON_GOALS = (
    "source content ingestion",
    "operational corpus mutation",
    "Code Evidence ingestion",
    "current-truth promotion",
    "runtime answer-use activation",
    "runtime retrieval activation",
    "answer synthesis runtime",
    "citation rendering runtime",
)


def evaluate_historical_retrieval_gate(
    metadata: dict[str, Any] | object,
) -> dict[str, Any]:
    answer_use_status = _normalized(metadata, "AnswerUsePermissionStatus")
    retrieval_status = _normalized(metadata, "RetrievalEligibilityStatus")
    provenance_status = _normalized(metadata, "ProvenanceStatus")
    citation_status = _normalized(metadata, "CitationStatus")
    conflict_status = _normalized(metadata, "ConflictStatus")
    supersession_status = _normalized(metadata, "SupersessionStatus")
    evidence_scope = _normalized(metadata, "EvidenceScope")
    answer_mode = _normalized(metadata, "AnswerMode")

    citation_required = _bool_value(metadata, "CitationRequired", True)
    caveat_required = _bool_value(metadata, "CaveatRequired", False)

    if _runtime_requested(metadata):
        return _response(
            decision="BLOCKED_RUNTIME_NOT_IMPLEMENTED",
            mode="RUNTIME_NOT_IMPLEMENTED",
            answer_mode="REFUSAL",
            reason="RUNTIME_RETRIEVAL_NOT_IMPLEMENTED",
            citation_required=citation_required,
            caveat_required=caveat_required,
            explanation="Runtime retrieval is not implemented; this skeleton only evaluates supplied metadata in-memory.",
        )

    if _not_answerable(metadata, evidence_scope, answer_mode):
        return _response(
            decision="REFUSE_NOT_ANSWERABLE",
            mode="REFUSAL",
            answer_mode="REFUSAL",
            reason="EVIDENCE_NOT_ANSWERABLE",
            citation_required=citation_required,
            caveat_required=caveat_required,
            explanation="Evidence is explicitly marked not answerable and cannot be used for retrieval handoff.",
        )

    if answer_use_status in ANSWER_USE_BLOCKERS:
        return _response(
            decision="REFUSE_MISSING_ANSWER_USE_PERMISSION",
            mode="REFUSAL",
            answer_mode="REFUSAL",
            reason="ANSWER_USE_PERMISSION_MISSING_OR_BLOCKED",
            citation_required=citation_required,
            caveat_required=caveat_required,
            explanation="Answer-use permission is missing or blocked; evidence is not eligible.",
        )

    if retrieval_status in RETRIEVAL_BLOCKERS:
        return _response(
            decision="REFUSE_MISSING_RETRIEVAL_ELIGIBILITY",
            mode="REFUSAL",
            answer_mode="REFUSAL",
            reason="RETRIEVAL_ELIGIBILITY_MISSING_OR_BLOCKED",
            citation_required=citation_required,
            caveat_required=caveat_required,
            explanation="Retrieval eligibility is missing or blocked; evidence is not eligible.",
        )

    if provenance_status in PROVENANCE_BLOCKERS or citation_status in PROVENANCE_BLOCKERS:
        return _response(
            decision="REFUSE_MISSING_PROVENANCE",
            mode="REFUSAL",
            answer_mode="REFUSAL",
            reason="MISSING_OR_INCOMPLETE_PROVENANCE",
            citation_required=citation_required,
            caveat_required=caveat_required,
            explanation="Citation/provenance metadata is missing or incomplete.",
        )

    if conflict_status in CONFLICT_BLOCKERS and not _approved_caveat_present(metadata):
        return _response(
            decision="REFUSE_CONFLICTED_EVIDENCE",
            mode="REFUSAL",
            answer_mode="REFUSAL",
            reason="CONFLICTED_EVIDENCE_WITHOUT_APPROVED_CAVEAT",
            citation_required=citation_required,
            caveat_required=True,
            explanation="Conflicted or unresolved evidence requires an approved caveat.",
        )

    if supersession_status == "SUPERSEDED" and _requests_current_truth(answer_mode):
        return _response(
            decision="REFUSE_SUPERSEDED_EVIDENCE",
            mode="REFUSAL",
            answer_mode="REFUSAL",
            reason="SUPERSEDED_EVIDENCE_CANNOT_ANSWER_CURRENT_TRUTH",
            citation_required=citation_required,
            caveat_required=caveat_required,
            explanation="Superseded evidence cannot support a current-truth answer.",
        )

    if evidence_scope == "HISTORICAL_CONTEXT_ONLY" and _requests_current_truth(answer_mode):
        return _response(
            decision="REFUSE_HISTORICAL_CONTEXT_NOT_CURRENT_TRUTH",
            mode="HISTORICAL_CONTEXT_ONLY",
            answer_mode="HISTORICAL_CONTEXT_ONLY",
            reason="HISTORICAL_CONTEXT_ONLY_CANNOT_ANSWER_CURRENT_TRUTH",
            citation_required=citation_required,
            caveat_required=True,
            explanation="Historical-context-only evidence remains historical and is not current truth.",
        )

    if (
        _approved(answer_use_status)
        and _approved(retrieval_status)
        and _provenance_ready(provenance_status, citation_status)
        and _bool_value(metadata, "CurrentTruthPermitted", False)
        and _bool_value(metadata, "RetrievalEligible", True)
        and _requests_current_truth(answer_mode)
        and supersession_status != "SUPERSEDED"
        and conflict_status not in CONFLICT_BLOCKERS
    ):
        if caveat_required:
            return _response(
                decision="ELIGIBLE_CAVEATED_RETRIEVAL",
                mode="READ_ONLY_METADATA_ONLY",
                answer_mode="CAVEATED_CURRENT_TRUTH",
                reason=None,
                citation_required=citation_required,
                caveat_required=True,
                explanation="Metadata is eligible for caveated retrieval gate handoff only; caveat requirement is preserved.",
            )

        return _response(
            decision="ELIGIBLE_CURRENT_TRUTH_RETRIEVAL",
            mode="READ_ONLY_METADATA_ONLY",
            answer_mode="CURRENT_TRUTH",
            reason=None,
            citation_required=citation_required,
            caveat_required=caveat_required,
            explanation="Metadata is eligible for current-truth retrieval gate handoff only.",
        )

    if (
        _approved(answer_use_status)
        and _approved(retrieval_status)
        and _provenance_ready(provenance_status, citation_status)
        and (evidence_scope == "HISTORICAL_CONTEXT_ONLY" or _requests_historical_context(answer_mode))
    ):
        return _response(
            decision="ELIGIBLE_HISTORICAL_CONTEXT_RETRIEVAL",
            mode="READ_ONLY_METADATA_ONLY",
            answer_mode="HISTORICAL_CONTEXT_ONLY",
            reason=None,
            citation_required=citation_required,
            caveat_required=True if evidence_scope == "HISTORICAL_CONTEXT_ONLY" else caveat_required,
            explanation="Metadata is eligible only as labelled historical context with required caveats preserved.",
        )

    return _response(
        decision="REFUSE_NOT_ANSWERABLE",
        mode="REFUSAL",
        answer_mode="REFUSAL",
        reason="NO_APPROVED_RETRIEVAL_PATH",
        citation_required=citation_required,
        caveat_required=caveat_required,
        explanation="No approved in-memory metadata-only retrieval path matched.",
    )


def _response(
    decision: str,
    mode: str,
    answer_mode: str,
    reason: str | None,
    citation_required: bool,
    caveat_required: bool,
    explanation: str,
) -> dict[str, Any]:
    return HistoricalRetrievalGateResponse(
        RetrievalGateSkeletonImplemented=True,
        LiveRetrievalPerformed=False,
        LiveLLMCalled=False,
        CorpusMutationPerformed=False,
        DatabaseReadPerformed=False,
        DatabaseWritePerformed=False,
        EndpointUIPresent=False,
        RetrievalDecision=decision,
        RetrievalMode=mode,
        ExpectedAnswerMode=answer_mode,
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


def _approved(status: str) -> bool:
    return "APPROVED" in status or status in {"ELIGIBLE", "READY"}


def _provenance_ready(provenance_status: str, citation_status: str) -> bool:
    return provenance_status not in PROVENANCE_BLOCKERS and citation_status not in PROVENANCE_BLOCKERS


def _requests_current_truth(answer_mode: str) -> bool:
    return "CURRENT_TRUTH" in answer_mode or answer_mode == "CURRENT"


def _requests_historical_context(answer_mode: str) -> bool:
    return "HISTORICAL_CONTEXT" in answer_mode or answer_mode == "HISTORICAL"


def _approved_caveat_present(metadata: dict[str, Any] | object) -> bool:
    return _bool_value(metadata, "CaveatApproved", False) or _bool_value(
        metadata,
        "ApprovedCaveatPresent",
        False,
    )


def _runtime_requested(metadata: dict[str, Any] | object) -> bool:
    return any(
        _bool_value(metadata, field_name, False)
        for field_name in (
            "RuntimeRequired",
            "LiveRetrievalRequired",
            "DatabaseReadRequired",
            "LiveLLMRequired",
            "EndpointUIRequired",
        )
    )


def _not_answerable(
    metadata: dict[str, Any] | object,
    evidence_scope: str,
    answer_mode: str,
) -> bool:
    evidence_answerable = _value(metadata, "EvidenceAnswerable")
    if evidence_answerable is not None and not _bool_value(metadata, "EvidenceAnswerable", True):
        return True
    return evidence_scope in NOT_ANSWERABLE_VALUES or answer_mode in NOT_ANSWERABLE_VALUES
