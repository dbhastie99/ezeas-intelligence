from app.services.contextual_explanation_contract_service import (
    ADMIN_QUEUE_EXPLANATION_PIPELINE,
    BLOCKED_LIVE_EXPOSURE_NOT_AUTHORISED,
    BLOCKED_MISSING_CONTEXT,
    CONTEXT_BLOCKED_LIVE_EXPOSURE,
    CONTEXT_MISSING_ACTIONS_NOT_TAKEN,
    CONTEXT_MISSING_FIELD_METADATA,
    CONTEXT_MISSING_LIFECYCLE_CONTEXT,
    CONTEXT_MISSING_OBJECT_STORY,
    CONTEXT_MISSING_PAYMENT_CONTEXT,
    CONTEXT_MISSING_SOURCE_CHANGE_SUMMARY,
    CONTEXT_READY_FOR_CONTROLLED_PIPELINE,
    CONTROLLED_PIPELINE_READY,
    FIELD_HELP_PIPELINE,
    LIVE_OPERATOR_RESPONSE,
    TREATMENT_REASONING_PIPELINE,
    WHAT_CHANGED,
    WHAT_HAS_NOT_HAPPENED,
    WHAT_IS_THIS_FIELD,
    WHY_IS_THIS_IN_ADMIN_QUEUE,
    WHY_THIS_TREATMENT,
    build_contextual_explanation_contract_review,
)


EXPECTED_FALSE_BOUNDARIES = (
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


def _base_context():
    return {
        "SurfaceContext": {
            "PageId": "LeaveTypeForm",
            "Route": "/admin/leave/types/new",
            "ComponentId": "leave-type-form",
            "SurfaceType": "CONFIG_FORM",
            "Mode": "EDIT",
        },
        "SubjectContext": {
            "SubjectType": "LeaveType",
            "EntityType": "LeaveType",
            "Domain": "LeaveManagement",
            "ObjectId": "leave-type-fixture",
            "ObjectStatus": "DRAFT",
        },
        "UserQuestionContext": {
            "QuestionText": "What does this field mean?",
            "QuestionIntent": WHAT_IS_THIS_FIELD,
            "UserRole": "PAYROLL_ADMIN",
            "Audience": "OPERATOR",
        },
        "EvidenceContext": {
            "DomainKnowledgeAvailable": True,
            "FieldCatalogueAvailable": True,
            "PlatformDoctrineAvailable": True,
            "SliceKnowledgeAvailable": True,
            "ObjectStoryAvailable": False,
            "RuntimeEvidenceAvailable": False,
            "DbEvidenceAvailable": False,
            "DeploymentEvidenceAvailable": False,
            "ProductionEvidenceAvailable": False,
            "EvidenceReferenceIds": ("leave-field-catalogue-accrual-method",),
        },
        "AnswerControlContext": {
            "RequestedExposureMode": "CONTROLLED_TEST_ONLY",
            "LiveAnswerRequested": False,
            "FinalAnswerRequested": False,
            "RequiresObjectSpecificAnswer": False,
            "RequiresRuntimeTruth": False,
            "RequiresDbTruth": False,
            "RequiresProductionTruth": False,
        },
    }


def _leave_type_field_help_context():
    context = _base_context()
    context["FieldContext"] = {
        "FieldName": "AccrualMethod",
        "FieldLabel": "Accrual method",
        "CurrentValue": "PRO_RATA",
        "AllowedValues": ("PRO_RATA", "FIXED", "NONE"),
        "ValidationState": "VALID",
        "HelpKey": "leave_type.accrual_method",
        "IsFieldLevelQuestion": True,
    }
    return context


def _admin_queue_context():
    context = {
        "SurfaceContext": {
            "PageId": "AdminQueue",
            "Route": "/admin/queue",
            "ComponentId": "correction-review-row",
            "SurfaceType": "REVIEW_QUEUE",
            "Mode": "REVIEW",
        },
        "SubjectContext": {
            "SubjectType": "CorrectionReview",
            "EntityType": "CorrectionReview",
            "Domain": "Payroll",
            "ObjectId": "cr-001",
            "ObjectStatus": "READY_FOR_REVIEW",
        },
        "ObjectContext": {
            "ObjectSummary": "Correction review created by a late ObjectTime source change.",
            "LifecycleState": "PROCESS_PERIOD_FINALISED",
            "RelevantIds": ("process-period-2026-05",),
            "Status": "READY_FOR_REVIEW",
            "RelatedEntityIds": ("worker-001", "payrun-001"),
        },
        "StoryContext": {
            "StoryJsonAvailable": True,
            "EvidenceJsonAvailable": True,
            "ActionsTakenAvailable": True,
            "ActionsNotTakenAvailable": True,
            "MissingEvidenceAvailable": True,
            "StorySummary": "Late ObjectTime change routed to CorrectionReview.",
            "EvidenceSummary": "Source change and lifecycle evidence are present.",
            "ActionsTaken": ("CorrectionReview queued.",),
            "ActionsNotTaken": ("Original finalised payrun was not mutated.",),
            "MissingEvidence": (),
        },
        "UserQuestionContext": {
            "QuestionText": "Why is this in Admin Queue?",
            "QuestionIntent": WHY_IS_THIS_IN_ADMIN_QUEUE,
            "UserRole": "PAYROLL_OPERATOR",
            "Audience": "OPERATOR",
        },
        "EvidenceContext": {
            "DomainKnowledgeAvailable": True,
            "FieldCatalogueAvailable": False,
            "PlatformDoctrineAvailable": True,
            "SliceKnowledgeAvailable": True,
            "ObjectStoryAvailable": True,
            "RuntimeEvidenceAvailable": False,
            "DbEvidenceAvailable": False,
            "DeploymentEvidenceAvailable": False,
            "ProductionEvidenceAvailable": False,
            "EvidenceReferenceIds": ("correction-review-story-fixture",),
        },
        "AnswerControlContext": {
            "RequestedExposureMode": "CONTROLLED_TEST_ONLY",
            "LiveAnswerRequested": False,
            "FinalAnswerRequested": False,
            "RequiresObjectSpecificAnswer": True,
            "RequiresRuntimeTruth": False,
            "RequiresDbTruth": False,
            "RequiresProductionTruth": False,
        },
    }
    return context


def _assert_boundaries(review):
    for flag in EXPECTED_FALSE_BOUNDARIES:
        assert review["BoundaryFlags"][flag] is False


def test_leave_type_field_help_is_ready_for_controlled_pipeline():
    review = build_contextual_explanation_contract_review(_leave_type_field_help_context())

    assert review["ContractStatus"] == CONTEXT_READY_FOR_CONTROLLED_PIPELINE
    assert review["SubjectType"] == "LeaveType"
    assert review["QuestionIntent"] == WHAT_IS_THIS_FIELD
    assert review["RecommendedMinervaFlow"] == FIELD_HELP_PIPELINE
    assert review["AnswerEligibility"] == CONTROLLED_PIPELINE_READY
    assert review["FieldHelpReadiness"] == "FIELD_HELP_CONTEXT_READY"
    assert "FieldContext" in review["AvailableEvidence"]
    _assert_boundaries(review)


def test_leave_type_field_help_missing_metadata_is_blocked():
    context = _leave_type_field_help_context()
    context.pop("FieldContext")
    context["EvidenceContext"]["FieldCatalogueAvailable"] = False
    context["EvidenceContext"]["DomainKnowledgeAvailable"] = False

    review = build_contextual_explanation_contract_review(context)

    assert review["ContractStatus"] == CONTEXT_MISSING_FIELD_METADATA
    assert review["AnswerEligibility"] == BLOCKED_MISSING_CONTEXT
    assert "FieldContext" in review["MissingEvidence"]
    assert "FieldCatalogueAvailable or DomainKnowledgeAvailable" in review["MissingEvidence"]
    _assert_boundaries(review)


def test_correction_review_admin_queue_explanation_is_ready():
    review = build_contextual_explanation_contract_review(_admin_queue_context())

    assert review["ContractStatus"] == CONTEXT_READY_FOR_CONTROLLED_PIPELINE
    assert review["RecommendedMinervaFlow"] == ADMIN_QUEUE_EXPLANATION_PIPELINE
    assert review["AnswerEligibility"] == CONTROLLED_PIPELINE_READY
    assert review["ObjectStoryReadiness"] == "OBJECT_STORY_CONTEXT_READY"
    assert "ActionsNotTaken" in review["AvailableEvidence"]
    _assert_boundaries(review)


def test_correction_review_retro_treatment_missing_lifecycle_is_blocked():
    context = _admin_queue_context()
    context["UserQuestionContext"]["QuestionIntent"] = WHY_THIS_TREATMENT
    context["UserQuestionContext"]["QuestionText"] = "Why is this retro and not current adjustment?"
    context["ObjectContext"].pop("LifecycleState")
    context["ObjectContext"]["CorrectionPathCode"] = "RETRO_REVIEW"

    review = build_contextual_explanation_contract_review(context)

    assert review["ContractStatus"] == CONTEXT_MISSING_LIFECYCLE_CONTEXT
    assert review["AnswerEligibility"] == BLOCKED_MISSING_CONTEXT
    assert "ProcessPeriodLifecycleContext" in review["MissingEvidence"]
    _assert_boundaries(review)


def test_banking_netting_treatment_missing_payment_context_is_blocked():
    context = _admin_queue_context()
    context["UserQuestionContext"]["QuestionIntent"] = WHY_THIS_TREATMENT
    context["UserQuestionContext"]["QuestionText"] = (
        "Why can this negative delta be netted before banking but recovered after payment?"
    )
    context["ObjectContext"]["CorrectionPathCode"] = "SUPPLEMENTARY_NEGATIVE_DELTA"

    review = build_contextual_explanation_contract_review(context)

    assert review["ContractStatus"] == CONTEXT_MISSING_PAYMENT_CONTEXT
    assert review["RecommendedMinervaFlow"] == "BLOCKED_NO_SAFE_FLOW"
    assert "PaymentWindowContext" in review["MissingEvidence"]
    _assert_boundaries(review)


def test_what_changed_missing_source_change_summary_is_blocked():
    context = _admin_queue_context()
    context["UserQuestionContext"]["QuestionIntent"] = WHAT_CHANGED
    context["UserQuestionContext"]["QuestionText"] = "What changed?"
    context["StoryContext"].pop("EvidenceSummary")

    review = build_contextual_explanation_contract_review(context)

    assert review["ContractStatus"] == CONTEXT_MISSING_SOURCE_CHANGE_SUMMARY
    assert "SourceChangeSummary or ChangedFields" in review["MissingEvidence"]
    _assert_boundaries(review)


def test_what_has_not_happened_missing_actions_not_taken_is_blocked():
    context = _admin_queue_context()
    context["UserQuestionContext"]["QuestionIntent"] = WHAT_HAS_NOT_HAPPENED
    context["UserQuestionContext"]["QuestionText"] = "What has not happened?"
    context["StoryContext"]["ActionsNotTakenAvailable"] = False
    context["StoryContext"].pop("ActionsNotTaken")

    review = build_contextual_explanation_contract_review(context)

    assert review["ContractStatus"] == CONTEXT_MISSING_ACTIONS_NOT_TAKEN
    assert "ActionsNotTakenAvailable" in review["MissingEvidence"]
    _assert_boundaries(review)


def test_live_operator_response_is_blocked():
    context = _leave_type_field_help_context()
    context["AnswerControlContext"]["RequestedExposureMode"] = LIVE_OPERATOR_RESPONSE
    context["AnswerControlContext"]["LiveAnswerRequested"] = True

    review = build_contextual_explanation_contract_review(context)

    assert review["ContractStatus"] == CONTEXT_BLOCKED_LIVE_EXPOSURE
    assert review["AnswerEligibility"] == BLOCKED_LIVE_EXPOSURE_NOT_AUTHORISED
    assert review["RecommendedMinervaFlow"] == "BLOCKED_NO_SAFE_FLOW"
    _assert_boundaries(review)


def test_object_specific_answer_without_object_story_is_blocked():
    context = _admin_queue_context()
    context["EvidenceContext"]["ObjectStoryAvailable"] = False
    context["ObjectContext"].pop("ObjectSummary")
    context["StoryContext"].clear()

    review = build_contextual_explanation_contract_review(context)

    assert review["ContractStatus"] == CONTEXT_MISSING_OBJECT_STORY
    assert review["AnswerEligibility"] == BLOCKED_MISSING_CONTEXT
    assert "ObjectStoryAvailable or StoryContext" in review["MissingEvidence"]
    _assert_boundaries(review)


def test_treatment_with_full_context_routes_to_treatment_reasoning_pipeline():
    context = _admin_queue_context()
    context["UserQuestionContext"]["QuestionIntent"] = WHY_THIS_TREATMENT
    context["UserQuestionContext"]["QuestionText"] = "Why is this retro and not current adjustment?"
    context["ObjectContext"]["CorrectionPathCode"] = "RETRO_REVIEW"
    context["ObjectContext"]["ProcessPeriodLifecycleStatus"] = "FINALISED"

    review = build_contextual_explanation_contract_review(context)

    assert review["ContractStatus"] == CONTEXT_READY_FOR_CONTROLLED_PIPELINE
    assert review["RecommendedMinervaFlow"] == TREATMENT_REASONING_PIPELINE
    assert review["AnswerEligibility"] == CONTROLLED_PIPELINE_READY
    _assert_boundaries(review)
