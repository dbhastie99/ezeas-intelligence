import re
from dataclasses import asdict, dataclass
from typing import Any, Iterable

from app.services.controlled_durable_evidence_retrieval_harness_service import (
    BOUNDARY_FLAGS,
)


CONTEXT_READY_FOR_CONTROLLED_PIPELINE = "CONTEXT_READY_FOR_CONTROLLED_PIPELINE"
CONTEXT_READY_WITH_CAVEATS = "CONTEXT_READY_WITH_CAVEATS"
CONTEXT_MISSING_FIELD_METADATA = "CONTEXT_MISSING_FIELD_METADATA"
CONTEXT_MISSING_OBJECT_STORY = "CONTEXT_MISSING_OBJECT_STORY"
CONTEXT_MISSING_SOURCE_CHANGE_SUMMARY = "CONTEXT_MISSING_SOURCE_CHANGE_SUMMARY"
CONTEXT_MISSING_LIFECYCLE_CONTEXT = "CONTEXT_MISSING_LIFECYCLE_CONTEXT"
CONTEXT_MISSING_PAYMENT_CONTEXT = "CONTEXT_MISSING_PAYMENT_CONTEXT"
CONTEXT_MISSING_ACTIONS_NOT_TAKEN = "CONTEXT_MISSING_ACTIONS_NOT_TAKEN"
CONTEXT_REQUIRES_RUNTIME_EVIDENCE = "CONTEXT_REQUIRES_RUNTIME_EVIDENCE"
CONTEXT_REQUIRES_DB_EVIDENCE = "CONTEXT_REQUIRES_DB_EVIDENCE"
CONTEXT_REQUIRES_PRODUCTION_EVIDENCE = "CONTEXT_REQUIRES_PRODUCTION_EVIDENCE"
CONTEXT_BLOCKED_LIVE_EXPOSURE = "CONTEXT_BLOCKED_LIVE_EXPOSURE"
CONTEXT_NOT_READY = "CONTEXT_NOT_READY"

FIELD_HELP_PIPELINE = "FIELD_HELP_PIPELINE"
FORM_GUIDANCE_PIPELINE = "FORM_GUIDANCE_PIPELINE"
OBJECT_STORY_EXPLANATION_PIPELINE = "OBJECT_STORY_EXPLANATION_PIPELINE"
ADMIN_QUEUE_EXPLANATION_PIPELINE = "ADMIN_QUEUE_EXPLANATION_PIPELINE"
TREATMENT_REASONING_PIPELINE = "TREATMENT_REASONING_PIPELINE"
EVIDENCE_GAP_PIPELINE = "EVIDENCE_GAP_PIPELINE"
BLOCKED_NO_SAFE_FLOW = "BLOCKED_NO_SAFE_FLOW"

CONTROLLED_PIPELINE_READY = "CONTROLLED_PIPELINE_READY"
CONTROLLED_PIPELINE_READY_WITH_CAVEATS = "CONTROLLED_PIPELINE_READY_WITH_CAVEATS"
BLOCKED_MISSING_CONTEXT = "BLOCKED_MISSING_CONTEXT"
BLOCKED_LIVE_EXPOSURE_NOT_AUTHORISED = "BLOCKED_LIVE_EXPOSURE_NOT_AUTHORISED"
BLOCKED_RUNTIME_EVIDENCE_REQUIRED = "BLOCKED_RUNTIME_EVIDENCE_REQUIRED"
BLOCKED_DB_EVIDENCE_REQUIRED = "BLOCKED_DB_EVIDENCE_REQUIRED"
BLOCKED_PRODUCTION_EVIDENCE_REQUIRED = "BLOCKED_PRODUCTION_EVIDENCE_REQUIRED"

WHAT_IS_THIS_FIELD = "WHAT_IS_THIS_FIELD"
WHAT_HAPPENS_IF_I_CHANGE_THIS = "WHAT_HAPPENS_IF_I_CHANGE_THIS"
WHY_IS_THIS_BLOCKED = "WHY_IS_THIS_BLOCKED"
WHY_IS_THIS_IN_ADMIN_QUEUE = "WHY_IS_THIS_IN_ADMIN_QUEUE"
WHY_THIS_TREATMENT = "WHY_THIS_TREATMENT"
WHAT_CHANGED = "WHAT_CHANGED"
WHAT_HAS_NOT_HAPPENED = "WHAT_HAS_NOT_HAPPENED"
WHAT_EVIDENCE_IS_MISSING = "WHAT_EVIDENCE_IS_MISSING"
WHAT_SHOULD_I_DO_NEXT = "WHAT_SHOULD_I_DO_NEXT"
GENERAL_HELP = "GENERAL_HELP"

LIVE_OPERATOR_RESPONSE = "LIVE_OPERATOR_RESPONSE"

SUPPORTED_QUESTION_TYPES = (
    WHAT_IS_THIS_FIELD,
    WHAT_HAPPENS_IF_I_CHANGE_THIS,
    WHY_IS_THIS_BLOCKED,
    WHY_IS_THIS_IN_ADMIN_QUEUE,
    WHY_THIS_TREATMENT,
    WHAT_CHANGED,
    WHAT_HAS_NOT_HAPPENED,
    WHAT_EVIDENCE_IS_MISSING,
    WHAT_SHOULD_I_DO_NEXT,
    GENERAL_HELP,
)

FALSE_BOUNDARY_FLAGS = (
    "LiveLLMCalled",
    "FinalAnswerGenerated",
    "ChatExposureEnabled",
    "DatabaseReadPerformed",
    "DatabaseWritePerformed",
    "RuntimeIntegrationPerformed",
    "LiveCorpusMutationPerformed",
    "AnswerDisplayed",
    "PersistedToDb",
)

FIELD_HELP_REQUIRED = (
    "SurfaceContext",
    "SubjectContext",
    "FieldContext",
    "FieldCatalogueAvailable or DomainKnowledgeAvailable",
)

NEXT_STEP_BY_STATUS = {
    CONTEXT_READY_FOR_CONTROLLED_PIPELINE: (
        "Pass this context into the controlled retrieval, answer preparation, "
        "provenance, rehearsal, and gate pipeline. Do not expose a live answer."
    ),
    CONTEXT_READY_WITH_CAVEATS: (
        "Proceed only through the controlled pipeline and preserve missing-evidence "
        "caveats before any later gate decision."
    ),
    CONTEXT_BLOCKED_LIVE_EXPOSURE: (
        "Do not display an answer. Live operator response is not authorised in this slice."
    ),
}


@dataclass(frozen=True)
class ContextualExplanationContractReview:
    ContractStatus: str
    ContractSeverity: str
    SubjectType: str
    QuestionIntent: str
    SupportedQuestionTypes: tuple[str, ...]
    BlockedQuestionTypes: tuple[str, ...]
    RequiredEvidence: tuple[str, ...]
    AvailableEvidence: tuple[str, ...]
    MissingEvidence: tuple[str, ...]
    RequiredCaveats: tuple[str, ...]
    RecommendedMinervaFlow: str
    AnswerEligibility: str
    FieldHelpReadiness: str
    ObjectStoryReadiness: str
    RuntimeEvidenceReadiness: str
    BoundaryFlags: dict[str, bool]
    NextStep: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ContextualExplanationContractService:
    """Deterministic readiness classifier for future Minerva explanation contexts."""

    def review_context(
        self,
        explanation_context: dict[str, Any] | None,
    ) -> dict[str, Any]:
        return review_contextual_explanation_contract(explanation_context)


def review_contextual_explanation_contract(
    explanation_context: dict[str, Any] | None,
) -> dict[str, Any]:
    """Classify a generic explanation context without producing an answer."""

    context = explanation_context or {}
    subject = str(_get(context, "SubjectContext", "SubjectType") or "")
    intent = _normalize_code(
        _get(context, "UserQuestionContext", "QuestionIntent") or GENERAL_HELP
    )

    required = list(_required_evidence(context, intent))
    available = list(_available_evidence(context))
    missing: list[str] = []
    caveats: list[str] = []
    blocked_question_types: list[str] = []

    status = CONTEXT_READY_FOR_CONTROLLED_PIPELINE
    flow = _recommended_flow(intent)
    eligibility = CONTROLLED_PIPELINE_READY

    if _live_exposure_requested(context):
        status = CONTEXT_BLOCKED_LIVE_EXPOSURE
        flow = BLOCKED_NO_SAFE_FLOW
        eligibility = BLOCKED_LIVE_EXPOSURE_NOT_AUTHORISED
        blocked_question_types.append(intent)
        caveats.append("Live operator response is not authorised in this contract slice.")
    elif _requires_production_evidence(context) and not _bool(context, "EvidenceContext", "ProductionEvidenceAvailable"):
        status = CONTEXT_REQUIRES_PRODUCTION_EVIDENCE
        flow = BLOCKED_NO_SAFE_FLOW
        eligibility = BLOCKED_PRODUCTION_EVIDENCE_REQUIRED
        missing.append("ProductionEvidenceAvailable")
    elif _requires_db_evidence(context) and not _bool(context, "EvidenceContext", "DbEvidenceAvailable"):
        status = CONTEXT_REQUIRES_DB_EVIDENCE
        flow = BLOCKED_NO_SAFE_FLOW
        eligibility = BLOCKED_DB_EVIDENCE_REQUIRED
        missing.append("DbEvidenceAvailable")
    elif _requires_runtime_evidence(context) and not _bool(context, "EvidenceContext", "RuntimeEvidenceAvailable"):
        status = CONTEXT_REQUIRES_RUNTIME_EVIDENCE
        flow = BLOCKED_NO_SAFE_FLOW
        eligibility = BLOCKED_RUNTIME_EVIDENCE_REQUIRED
        missing.append("RuntimeEvidenceAvailable")
    else:
        status, flow, eligibility, intent_missing, intent_caveats = _intent_decision(context, intent)
        missing.extend(intent_missing)
        caveats.extend(intent_caveats)
        if eligibility.startswith("BLOCKED"):
            blocked_question_types.append(intent)

    if not _has_surface_context(context):
        missing.append("SurfaceContext")
    if not _has_subject_context(context):
        missing.append("SubjectContext")

    missing_tuple = tuple(dict.fromkeys(item for item in missing if item))
    status = _status_after_common_missing(status, missing_tuple)
    if status in _blocked_statuses() and eligibility == CONTROLLED_PIPELINE_READY:
        eligibility = BLOCKED_MISSING_CONTEXT
    if status in _blocked_statuses() and flow != BLOCKED_NO_SAFE_FLOW and not _flow_allowed_when_blocked(status):
        flow = BLOCKED_NO_SAFE_FLOW

    caveats_tuple = tuple(dict.fromkeys(item for item in caveats if item))

    return ContextualExplanationContractReview(
        ContractStatus=status,
        ContractSeverity=_severity(status),
        SubjectType=subject,
        QuestionIntent=intent,
        SupportedQuestionTypes=SUPPORTED_QUESTION_TYPES,
        BlockedQuestionTypes=tuple(dict.fromkeys(blocked_question_types)),
        RequiredEvidence=tuple(dict.fromkeys(required)),
        AvailableEvidence=tuple(dict.fromkeys(available)),
        MissingEvidence=missing_tuple,
        RequiredCaveats=caveats_tuple,
        RecommendedMinervaFlow=flow,
        AnswerEligibility=eligibility,
        FieldHelpReadiness=_field_help_readiness(context),
        ObjectStoryReadiness=_object_story_readiness(context),
        RuntimeEvidenceReadiness=_runtime_evidence_readiness(context),
        BoundaryFlags=_boundary_flags(),
        NextStep=_next_step(status),
    ).to_dict()


def _intent_decision(
    context: dict[str, Any],
    intent: str,
) -> tuple[str, str, str, list[str], list[str]]:
    if intent == WHAT_IS_THIS_FIELD:
        return _field_help_decision(context)
    if intent == WHAT_HAPPENS_IF_I_CHANGE_THIS:
        return _change_impact_decision(context)
    if intent == WHY_IS_THIS_IN_ADMIN_QUEUE:
        return _admin_queue_decision(context)
    if intent == WHY_THIS_TREATMENT:
        return _treatment_decision(context)
    if intent == WHAT_CHANGED:
        return _what_changed_decision(context)
    if intent == WHAT_HAS_NOT_HAPPENED:
        return _actions_not_taken_decision(context)
    if intent in {WHAT_EVIDENCE_IS_MISSING, WHY_IS_THIS_BLOCKED}:
        return _evidence_gap_decision(context)
    return (
        CONTEXT_READY_WITH_CAVEATS,
        FORM_GUIDANCE_PIPELINE,
        CONTROLLED_PIPELINE_READY_WITH_CAVEATS,
        [],
        ("General help must stay generic unless field or object evidence is supplied.",),
    )


def _field_help_decision(context: dict[str, Any]) -> tuple[str, str, str, list[str], list[str]]:
    missing: list[str] = []
    if not _has_field_context(context):
        missing.append("FieldContext")
    if not (_bool(context, "EvidenceContext", "FieldCatalogueAvailable") or _bool(context, "EvidenceContext", "DomainKnowledgeAvailable")):
        missing.append("FieldCatalogueAvailable or DomainKnowledgeAvailable")
    if missing:
        return (
            CONTEXT_MISSING_FIELD_METADATA,
            BLOCKED_NO_SAFE_FLOW,
            BLOCKED_MISSING_CONTEXT,
            missing,
            [],
        )
    caveats = []
    if not _bool(context, "EvidenceContext", "PlatformDoctrineAvailable"):
        caveats.append("Field help is ready, but platform doctrine is not present for policy-level explanation.")
    status = CONTEXT_READY_WITH_CAVEATS if caveats else CONTEXT_READY_FOR_CONTROLLED_PIPELINE
    eligibility = CONTROLLED_PIPELINE_READY_WITH_CAVEATS if caveats else CONTROLLED_PIPELINE_READY
    return (status, FIELD_HELP_PIPELINE, eligibility, [], caveats)


def _change_impact_decision(context: dict[str, Any]) -> tuple[str, str, str, list[str], list[str]]:
    missing: list[str] = []
    caveats: list[str] = []
    if not _has_field_context(context):
        missing.append("FieldContext")
    if not _bool(context, "EvidenceContext", "DomainKnowledgeAvailable"):
        missing.append("DomainKnowledgeAvailable")
    if not (_bool(context, "EvidenceContext", "PlatformDoctrineAvailable") or _bool(context, "EvidenceContext", "SliceKnowledgeAvailable")):
        caveats.append("Configuration impact explanation lacks platform doctrine or slice knowledge.")
    if missing:
        return (CONTEXT_MISSING_FIELD_METADATA, BLOCKED_NO_SAFE_FLOW, BLOCKED_MISSING_CONTEXT, missing, caveats)
    status = CONTEXT_READY_WITH_CAVEATS if caveats else CONTEXT_READY_FOR_CONTROLLED_PIPELINE
    eligibility = CONTROLLED_PIPELINE_READY_WITH_CAVEATS if caveats else CONTROLLED_PIPELINE_READY
    return (status, FORM_GUIDANCE_PIPELINE, eligibility, [], caveats)


def _admin_queue_decision(context: dict[str, Any]) -> tuple[str, str, str, list[str], list[str]]:
    missing: list[str] = []
    if not _object_story_available(context):
        missing.append("ObjectStoryAvailable or StoryContext")
    if not _actions_taken_available(context):
        missing.append("ActionsTakenAvailable")
    if not _actions_not_taken_available(context):
        missing.append("ActionsNotTakenAvailable")
    if not _has_object_status_or_lifecycle(context):
        missing.append("ObjectStatus or LifecycleState")
    if missing:
        status = CONTEXT_MISSING_OBJECT_STORY if "ObjectStoryAvailable or StoryContext" in missing else CONTEXT_MISSING_LIFECYCLE_CONTEXT
        return (status, BLOCKED_NO_SAFE_FLOW, BLOCKED_MISSING_CONTEXT, missing, [])
    return (CONTEXT_READY_FOR_CONTROLLED_PIPELINE, ADMIN_QUEUE_EXPLANATION_PIPELINE, CONTROLLED_PIPELINE_READY, [], [])


def _treatment_decision(context: dict[str, Any]) -> tuple[str, str, str, list[str], list[str]]:
    missing: list[str] = []
    if not _object_story_available(context):
        missing.append("ObjectStoryAvailable or StoryContext")
    if not _has_lifecycle_context(context):
        missing.append("ProcessPeriodLifecycleContext")
    if not _has_treatment_context(context):
        missing.append("CorrectionPathCode or treatment summary")
    if not _actions_not_taken_available(context):
        missing.append("ActionsNotTakenAvailable")
    if _payment_question(context) and not _has_payment_context(context):
        missing.append("PaymentWindowContext")

    if "PaymentWindowContext" in missing:
        return (CONTEXT_MISSING_PAYMENT_CONTEXT, BLOCKED_NO_SAFE_FLOW, BLOCKED_MISSING_CONTEXT, missing, [])
    if "ProcessPeriodLifecycleContext" in missing:
        return (CONTEXT_MISSING_LIFECYCLE_CONTEXT, BLOCKED_NO_SAFE_FLOW, BLOCKED_MISSING_CONTEXT, missing, [])
    if "ActionsNotTakenAvailable" in missing:
        return (CONTEXT_MISSING_ACTIONS_NOT_TAKEN, BLOCKED_NO_SAFE_FLOW, BLOCKED_MISSING_CONTEXT, missing, [])
    if missing:
        return (CONTEXT_MISSING_OBJECT_STORY, BLOCKED_NO_SAFE_FLOW, BLOCKED_MISSING_CONTEXT, missing, [])
    return (CONTEXT_READY_FOR_CONTROLLED_PIPELINE, TREATMENT_REASONING_PIPELINE, CONTROLLED_PIPELINE_READY, [], [])


def _what_changed_decision(context: dict[str, Any]) -> tuple[str, str, str, list[str], list[str]]:
    if not _has_source_change_summary(context):
        return (
            CONTEXT_MISSING_SOURCE_CHANGE_SUMMARY,
            BLOCKED_NO_SAFE_FLOW,
            BLOCKED_MISSING_CONTEXT,
            ["SourceChangeSummary or ChangedFields"],
            [],
        )
    return (CONTEXT_READY_FOR_CONTROLLED_PIPELINE, OBJECT_STORY_EXPLANATION_PIPELINE, CONTROLLED_PIPELINE_READY, [], [])


def _actions_not_taken_decision(context: dict[str, Any]) -> tuple[str, str, str, list[str], list[str]]:
    if not _actions_not_taken_available(context):
        return (
            CONTEXT_MISSING_ACTIONS_NOT_TAKEN,
            BLOCKED_NO_SAFE_FLOW,
            BLOCKED_MISSING_CONTEXT,
            ["ActionsNotTakenAvailable"],
            [],
        )
    return (CONTEXT_READY_FOR_CONTROLLED_PIPELINE, OBJECT_STORY_EXPLANATION_PIPELINE, CONTROLLED_PIPELINE_READY, [], [])


def _evidence_gap_decision(context: dict[str, Any]) -> tuple[str, str, str, list[str], list[str]]:
    if not _missing_evidence_available(context):
        return (
            CONTEXT_READY_WITH_CAVEATS,
            EVIDENCE_GAP_PIPELINE,
            CONTROLLED_PIPELINE_READY_WITH_CAVEATS,
            [],
            ["Missing-evidence explanation can identify absent context, but no object-specific gap list was supplied."],
        )
    return (CONTEXT_READY_FOR_CONTROLLED_PIPELINE, EVIDENCE_GAP_PIPELINE, CONTROLLED_PIPELINE_READY, [], [])


def _required_evidence(context: dict[str, Any], intent: str) -> tuple[str, ...]:
    if intent == WHAT_IS_THIS_FIELD:
        return FIELD_HELP_REQUIRED
    if intent == WHAT_HAPPENS_IF_I_CHANGE_THIS:
        return (
            "FieldContext",
            "DomainKnowledgeAvailable",
            "PlatformDoctrineAvailable or SliceKnowledgeAvailable",
            "Validation or configuration impact knowledge",
        )
    if intent == WHY_IS_THIS_IN_ADMIN_QUEUE:
        return (
            "SubjectContext",
            "ObjectStoryAvailable or StoryContext",
            "ActionsTaken",
            "ActionsNotTaken",
            "ObjectStatus or lifecycle/status summary",
        )
    if intent == WHY_THIS_TREATMENT:
        required = [
            "ObjectStoryAvailable or StoryContext",
            "ProcessPeriodLifecycleContext",
            "CorrectionPathCode or treatment summary",
            "DomainKnowledgeAvailable or PlatformDoctrineAvailable",
            "ActionsNotTaken",
        ]
        if _payment_question(context):
            required.append("PaymentWindowContext")
        return tuple(required)
    if intent == WHAT_CHANGED:
        return ("SourceChangeSummary", "ChangedFields or before-after summary")
    if intent == WHAT_HAS_NOT_HAPPENED:
        return ("ActionsNotTaken",)
    if intent in {WHAT_EVIDENCE_IS_MISSING, WHY_IS_THIS_BLOCKED}:
        return ("MissingEvidence", "Blocker or validation context")
    return ("SurfaceContext", "SubjectContext", "DomainKnowledgeAvailable or SliceKnowledgeAvailable")


def _available_evidence(context: dict[str, Any]) -> tuple[str, ...]:
    evidence = []
    if _has_surface_context(context):
        evidence.append("SurfaceContext")
    if _has_subject_context(context):
        evidence.append("SubjectContext")
    if _has_field_context(context):
        evidence.append("FieldContext")
    if _object_story_available(context):
        evidence.append("ObjectStoryAvailable")
    if _actions_taken_available(context):
        evidence.append("ActionsTaken")
    if _actions_not_taken_available(context):
        evidence.append("ActionsNotTaken")
    if _missing_evidence_available(context):
        evidence.append("MissingEvidence")
    if _has_lifecycle_context(context):
        evidence.append("ProcessPeriodLifecycleContext")
    if _has_payment_context(context):
        evidence.append("PaymentWindowContext")
    if _has_source_change_summary(context):
        evidence.append("SourceChangeSummary")

    evidence_context = _section(context, "EvidenceContext")
    for key in (
        "DomainKnowledgeAvailable",
        "FieldCatalogueAvailable",
        "PlatformDoctrineAvailable",
        "SliceKnowledgeAvailable",
        "RuntimeEvidenceAvailable",
        "DbEvidenceAvailable",
        "DeploymentEvidenceAvailable",
        "ProductionEvidenceAvailable",
    ):
        if bool(evidence_context.get(key)):
            evidence.append(key)
    return tuple(evidence)


def _recommended_flow(intent: str) -> str:
    return {
        WHAT_IS_THIS_FIELD: FIELD_HELP_PIPELINE,
        WHAT_HAPPENS_IF_I_CHANGE_THIS: FORM_GUIDANCE_PIPELINE,
        WHY_IS_THIS_BLOCKED: EVIDENCE_GAP_PIPELINE,
        WHY_IS_THIS_IN_ADMIN_QUEUE: ADMIN_QUEUE_EXPLANATION_PIPELINE,
        WHY_THIS_TREATMENT: TREATMENT_REASONING_PIPELINE,
        WHAT_CHANGED: OBJECT_STORY_EXPLANATION_PIPELINE,
        WHAT_HAS_NOT_HAPPENED: OBJECT_STORY_EXPLANATION_PIPELINE,
        WHAT_EVIDENCE_IS_MISSING: EVIDENCE_GAP_PIPELINE,
        WHAT_SHOULD_I_DO_NEXT: FORM_GUIDANCE_PIPELINE,
        GENERAL_HELP: FORM_GUIDANCE_PIPELINE,
    }.get(intent, FORM_GUIDANCE_PIPELINE)


def _status_after_common_missing(status: str, missing: tuple[str, ...]) -> str:
    if status in _blocked_statuses():
        return status
    common_missing = {"SurfaceContext", "SubjectContext"} & set(missing)
    if common_missing:
        return CONTEXT_NOT_READY
    return status


def _blocked_statuses() -> set[str]:
    return {
        CONTEXT_MISSING_FIELD_METADATA,
        CONTEXT_MISSING_OBJECT_STORY,
        CONTEXT_MISSING_SOURCE_CHANGE_SUMMARY,
        CONTEXT_MISSING_LIFECYCLE_CONTEXT,
        CONTEXT_MISSING_PAYMENT_CONTEXT,
        CONTEXT_MISSING_ACTIONS_NOT_TAKEN,
        CONTEXT_REQUIRES_RUNTIME_EVIDENCE,
        CONTEXT_REQUIRES_DB_EVIDENCE,
        CONTEXT_REQUIRES_PRODUCTION_EVIDENCE,
        CONTEXT_BLOCKED_LIVE_EXPOSURE,
        CONTEXT_NOT_READY,
    }


def _flow_allowed_when_blocked(status: str) -> bool:
    return status in {
        CONTEXT_MISSING_SOURCE_CHANGE_SUMMARY,
        CONTEXT_MISSING_ACTIONS_NOT_TAKEN,
    }


def _severity(status: str) -> str:
    if status == CONTEXT_READY_FOR_CONTROLLED_PIPELINE:
        return "GREEN"
    if status == CONTEXT_READY_WITH_CAVEATS:
        return "AMBER"
    return "RED"


def _field_help_readiness(context: dict[str, Any]) -> str:
    if _has_field_context(context) and (
        _bool(context, "EvidenceContext", "FieldCatalogueAvailable")
        or _bool(context, "EvidenceContext", "DomainKnowledgeAvailable")
    ):
        return "FIELD_HELP_CONTEXT_READY"
    return "FIELD_HELP_CONTEXT_NOT_READY"


def _object_story_readiness(context: dict[str, Any]) -> str:
    if _object_story_available(context) and _actions_not_taken_available(context):
        return "OBJECT_STORY_CONTEXT_READY"
    if _object_story_available(context):
        return "OBJECT_STORY_CONTEXT_READY_WITH_CAVEATS"
    return "OBJECT_STORY_CONTEXT_NOT_READY"


def _runtime_evidence_readiness(context: dict[str, Any]) -> str:
    if _bool(context, "EvidenceContext", "RuntimeEvidenceAvailable"):
        return "RUNTIME_EVIDENCE_AVAILABLE"
    return "RUNTIME_EVIDENCE_NOT_AVAILABLE"


def _next_step(status: str) -> str:
    return NEXT_STEP_BY_STATUS.get(
        status,
        "Do not expose an answer. Supply the missing context and rerun the contextual contract review.",
    )


def _boundary_flags() -> dict[str, bool]:
    flags = dict(BOUNDARY_FLAGS)
    for flag in FALSE_BOUNDARY_FLAGS:
        flags[flag] = False
    return flags


def _has_surface_context(context: dict[str, Any]) -> bool:
    surface = _section(context, "SurfaceContext")
    return any(surface.get(key) for key in ("PageId", "Route", "ComponentId", "SurfaceType", "Mode"))


def _has_subject_context(context: dict[str, Any]) -> bool:
    subject = _section(context, "SubjectContext")
    return any(subject.get(key) for key in ("SubjectType", "EntityType", "Domain", "ObjectId", "ObjectStatus"))


def _has_field_context(context: dict[str, Any]) -> bool:
    field = _section(context, "FieldContext")
    return any(field.get(key) is not None for key in ("FieldName", "FieldLabel", "HelpKey"))


def _object_story_available(context: dict[str, Any]) -> bool:
    story = _section(context, "StoryContext")
    return (
        _bool(context, "EvidenceContext", "ObjectStoryAvailable")
        or bool(story.get("StoryJsonAvailable"))
        or bool(story.get("StorySummary"))
        or bool(_section(context, "ObjectContext").get("ObjectSummary"))
    )


def _actions_taken_available(context: dict[str, Any]) -> bool:
    story = _section(context, "StoryContext")
    return bool(story.get("ActionsTakenAvailable") or story.get("ActionsTaken"))


def _actions_not_taken_available(context: dict[str, Any]) -> bool:
    story = _section(context, "StoryContext")
    return bool(story.get("ActionsNotTakenAvailable") or story.get("ActionsNotTaken"))


def _missing_evidence_available(context: dict[str, Any]) -> bool:
    story = _section(context, "StoryContext")
    return bool(story.get("MissingEvidenceAvailable") or story.get("MissingEvidence"))


def _has_lifecycle_context(context: dict[str, Any]) -> bool:
    object_context = _section(context, "ObjectContext")
    story_context = _section(context, "StoryContext")
    return any(
        object_context.get(key) or story_context.get(key)
        for key in (
            "LifecycleState",
            "ProcessPeriodLifecycleStatus",
            "LifecycleSummary",
            "LifecycleContext",
        )
    )


def _has_object_status_or_lifecycle(context: dict[str, Any]) -> bool:
    subject = _section(context, "SubjectContext")
    object_context = _section(context, "ObjectContext")
    return bool(subject.get("ObjectStatus") or object_context.get("Status") or _has_lifecycle_context(context))


def _has_treatment_context(context: dict[str, Any]) -> bool:
    object_context = _section(context, "ObjectContext")
    story_context = _section(context, "StoryContext")
    return any(
        object_context.get(key) or story_context.get(key)
        for key in (
            "CorrectionPathCode",
            "TreatmentCode",
            "TreatmentSummary",
            "RoutingSummary",
            "CorrectionTreatment",
        )
    )


def _has_payment_context(context: dict[str, Any]) -> bool:
    object_context = _section(context, "ObjectContext")
    story_context = _section(context, "StoryContext")
    return any(
        object_context.get(key) or story_context.get(key)
        for key in (
            "PaymentWindowStatus",
            "PaymentContext",
            "PaymentWindowContext",
            "PaymentBatchStatus",
            "BankingStatus",
            "NettingContext",
        )
    )


def _has_source_change_summary(context: dict[str, Any]) -> bool:
    object_context = _section(context, "ObjectContext")
    story_context = _section(context, "StoryContext")
    return any(
        object_context.get(key) or story_context.get(key)
        for key in (
            "SourceChangeSummary",
            "ChangedFields",
            "BeforeAfterSummary",
            "EvidenceSummary",
        )
    )


def _payment_question(context: dict[str, Any]) -> bool:
    text = " ".join(
        str(item or "")
        for item in (
            _get(context, "UserQuestionContext", "QuestionText"),
            _get(context, "StoryContext", "StorySummary"),
            _get(context, "StoryContext", "EvidenceSummary"),
            _get(context, "ObjectContext", "ObjectSummary"),
            _get(context, "ObjectContext", "TreatmentSummary"),
        )
    )
    normalized = _normalize(text)
    return any(
        marker in normalized
        for marker in (
            "payment",
            "banking",
            "bank",
            "netting",
            "netted",
            "recovery",
            "paid",
            "payment window",
        )
    )


def _live_exposure_requested(context: dict[str, Any]) -> bool:
    requested = _normalize_code(_get(context, "AnswerControlContext", "RequestedExposureMode"))
    return requested == LIVE_OPERATOR_RESPONSE or _bool(context, "AnswerControlContext", "LiveAnswerRequested")


def _requires_runtime_evidence(context: dict[str, Any]) -> bool:
    return _bool(context, "AnswerControlContext", "RequiresRuntimeTruth")


def _requires_db_evidence(context: dict[str, Any]) -> bool:
    return _bool(context, "AnswerControlContext", "RequiresDbTruth")


def _requires_production_evidence(context: dict[str, Any]) -> bool:
    return _bool(context, "AnswerControlContext", "RequiresProductionTruth")


def _get(context: dict[str, Any], section: str, key: str) -> Any:
    return _section(context, section).get(key)


def _bool(context: dict[str, Any], section: str, key: str) -> bool:
    return bool(_get(context, section, key))


def _section(context: dict[str, Any], section: str) -> dict[str, Any]:
    value = context.get(section)
    if isinstance(value, dict):
        return value
    for key, candidate in context.items():
        if _normalize_code(key) == _normalize_code(section) and isinstance(candidate, dict):
            return candidate
    return {}


def _normalize_code(value: Any) -> str:
    return str(value or "").strip().upper().replace("-", "_").replace(" ", "_")


def _normalize(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").lower().replace("-", " ")).strip()


def build_contextual_explanation_contract_review(
    explanation_context: dict[str, Any] | None,
) -> dict[str, Any]:
    return review_contextual_explanation_contract(explanation_context)
