import copy

import pytest
from pydantic import ValidationError

from app.schemas.award_studio_minerva import (
    AwardStudioMinervaQuestionRequest,
    AwardVersionExplainableContextV1,
)
from app.services.award_studio_answer_planner import (
    AwardStudioContractError,
    build_answer_plan,
    canonical_projection_fingerprint,
)
from app.services.award_studio_question_service import ask_award_studio_question


SHA_A = "a" * 64
SHA_B = "b" * 64
SHA_C = "c" * 64
SHA_D = "d" * 64
SHA_E = "e" * 64
MA000027_VERSION = "081C6599-334D-4C2F-BD15-4373C4A944F9"


def _node(
    identity: str,
    node_type: str,
    code: str,
    label: str,
    authority: str,
    evidence_ids: list[str],
    *,
    values=None,
    quantities=None,
    applicability=None,
):
    return {
        "semanticIdentity": identity,
        "type": node_type,
        "code": code,
        "friendlyName": label,
        "purpose": f"Configured {label} meaning supplied by Workforce.",
        "status": "REVIEW_REQUIRED" if authority == "HELD" else "CONFIGURED",
        "authorityClassification": authority,
        "values": values or {},
        "quantities": quantities or [],
        "applicability": applicability or {},
        "evidenceIds": evidence_ids,
        "workspaceAnchor": f"award-studio:{code.lower()}",
    }


def _evidence(identity: str, semantic_identity: str, title: str, source_sha: str, page: int):
    return {
        "evidenceIdentity": identity,
        "propositionIdentity": f"proposition:{identity}",
        "semanticIdentity": semantic_identity,
        "sourceDocumentIdentity": f"document:{source_sha[:8]}",
        "sourceTitle": title,
        "sourceSha256": source_sha,
        "officialUrl": "https://example.invalid/governed-source",
        "sourceLocator": {"page": page, "row": f"row-{page}"},
        "extractedValue": None,
        "authorityClassification": "EXPLICIT_STRUCTURED",
    }


def _with_fingerprint(payload: dict) -> AwardVersionExplainableContextV1:
    projection = AwardVersionExplainableContextV1.model_validate(payload)
    fingerprint = canonical_projection_fingerprint(projection)
    return projection.model_copy(
        update={
            "authorityEnvelope": projection.authorityEnvelope.model_copy(
                update={"projectionFingerprint": fingerprint}
            )
        }
    )


def ma000027_projection() -> AwardVersionExplainableContextV1:
    nodes = [
        _node("semantic:award", "AWARD", "MA000027", "Health Professionals and Support Services Award", "EXPLICIT_STRUCTURED", ["evidence:award"]),
        _node("semantic:classification", "CLASSIFICATION", "GRADE_1", "Configured grade 1 classification", "EXPLICIT_STRUCTURED", ["evidence:classification"]),
        _node(
            "semantic:saturday",
            "RATE_TREATMENT",
            "SATURDAY",
            "Configured Saturday treatment",
            "EXPLICIT_STRUCTURED",
            ["evidence:saturday"],
            values={"treatmentCode": "SATURDAY"},
            applicability={"employmentType": "CASUAL"},
        ),
        _node(
            "semantic:sunday",
            "RATE_TREATMENT",
            "SUNDAY",
            "Configured Sunday treatment",
            "EXPLICIT_STRUCTURED",
            ["evidence:sunday"],
            values={"treatmentCode": "SUNDAY"},
        ),
        _node(
            "semantic:ot1",
            "OVERTIME_TREATMENT",
            "OT1",
            "Configured first overtime treatment",
            "DETERMINISTICALLY_DERIVABLE",
            ["evidence:ot1"],
            values={"treatmentCode": "OT1"},
        ),
        _node(
            "semantic:allowance",
            "ALLOWANCE",
            "MEAL1",
            "Configured meal allowance",
            "EXPLICIT_STRUCTURED",
            ["evidence:allowance"],
            quantities=[{"value": "17.30", "unit": "PUBLISHED_AMOUNT"}],
        ),
        _node(
            "semantic:damaged-clothing",
            "REIMBURSEMENT",
            "DAMAGED_CLOTHING_AND_PERSONAL_EFFECTS",
            "Damaged clothing and personal effects",
            "HELD",
            ["evidence:damaged-clothing"],
        ),
    ]
    evidence = [
        _evidence("evidence:award", "semantic:award", "MA000027 source package", SHA_A, 1),
        _evidence("evidence:classification", "semantic:classification", "MA000027 pay guide", SHA_B, 3),
        _evidence("evidence:saturday", "semantic:saturday", "MA000027 pay guide", SHA_B, 7),
        _evidence("evidence:sunday", "semantic:sunday", "MA000027 pay guide", SHA_B, 7),
        _evidence("evidence:ot1", "semantic:ot1", "MA000027 governed proposition", SHA_C, 8),
        _evidence("evidence:allowance", "semantic:allowance", "MA000027 allowance table", SHA_D, 40),
        _evidence("evidence:damaged-clothing", "semantic:damaged-clothing", "MA000027 allowance table", SHA_D, 41),
    ]
    payload = {
        "schemaVersion": "award_version_explainable_context_v1",
        "authorityEnvelope": {
            "awardHeaderId": "award-header-ma000027",
            "awardVersionId": MA000027_VERSION,
            "awardCode": "MA000027",
            "awardName": "Health Professionals and Support Services Award",
            "effectiveFrom": "2026-07-02",
            "effectiveTo": None,
            "lifecycle": "GENERATED_INACTIVE",
            "configurationFingerprint": SHA_A,
            "semanticGraphFingerprint": SHA_B,
            "sourceAuthorityFingerprint": SHA_C,
            "projectionFingerprint": "0" * 64,
            "projectionSchemaVersion": "award_version_explainable_context_v1",
            "versionLineage": {"predecessorAwardVersionId": None, "successorAwardVersionIds": []},
        },
        "semanticNodes": nodes,
        "relationships": [
            {
                "relationshipIdentity": "relationship:saturday-rate",
                "type": "USES_RATE",
                "sourceSemanticIdentity": "semantic:saturday",
                "targetKind": "OPERATIONAL_BINDING",
                "targetIdentity": "binding:saturday-rate-source",
                "authorityClassification": "EXPLICIT_STRUCTURED",
                "applicability": {"employmentType": "CASUAL"},
            },
            {
                "relationshipIdentity": "relationship:ot1-saturday",
                "type": "DERIVED_FROM",
                "sourceSemanticIdentity": "semantic:ot1",
                "targetKind": "SEMANTIC_NODE",
                "targetIdentity": "semantic:saturday",
                "authorityClassification": "DETERMINISTICALLY_DERIVABLE",
                "applicability": {},
            },
        ],
        "evidence": evidence,
        "operationalBindings": [
            {
                "bindingIdentity": "binding:saturday-rate-source",
                "bindingType": "RateSource",
                "semanticIdentity": "semantic:saturday",
                "targetIdentity": "rate-source-saturday",
                "targetCode": "SATURDAY",
                "authorityClassification": "EXPLICIT_STRUCTURED",
            }
        ],
        "holds": [
            {
                "holdIdentity": "hold:damaged-clothing",
                "semanticIdentity": "semantic:damaged-clothing",
                "code": "DAMAGED_CLOTHING_AND_PERSONAL_EFFECTS",
                "friendlyName": "Damaged clothing and personal effects",
                "status": "REVIEW_REQUIRED",
                "reason": "The governed source semantic is reimbursement while the configured candidate RateType semantic is allowance.",
                "sourceSemantic": "REIMBURSEMENT",
                "candidateSemantic": "ALLOWANCE",
                "requiredAction": "Owner or reviewer must select a compatible configured treatment.",
                "evidenceIds": ["evidence:damaged-clothing"],
            }
        ],
        "completeness": [
            {
                "conceptCode": "PUBLIC_HOLIDAY",
                "friendlyName": "Public holiday treatment",
                "authorityClassification": "NOT_CONFIGURED",
                "explanation": "The selected version contains no configured public-holiday semantic node.",
                "semanticIdentities": [],
            },
            {
                "conceptCode": "OT2",
                "friendlyName": "Second overtime treatment",
                "authorityClassification": "MISSING",
                "explanation": "No governed OT2 authority is present in this projection.",
                "semanticIdentities": [],
            },
        ],
        "presentationPayloads": [
            {
                "presentationKey": "OVERVIEW",
                "conciseSpokenSummary": "This is the exact configured MA000027 version overview.",
                "expandableDetail": ["Open the configured semantic authority for detail."],
                "evidenceIds": ["evidence:award"],
                "workspaceAnchors": ["award-studio:overview"],
                "subtitles": ["Exact configured MA000027 version overview."],
                "recommendedSequence": 1,
            },
            {
                "presentationKey": "SATURDAY",
                "conciseSpokenSummary": "The selected version contains a configured Saturday treatment.",
                "expandableDetail": ["Inspect its operational binding and source evidence."],
                "evidenceIds": ["evidence:saturday"],
                "workspaceAnchors": ["award-studio:saturday"],
                "subtitles": ["Configured Saturday treatment."],
                "recommendedSequence": 2,
            },
            {
                "presentationKey": "HOLD",
                "conciseSpokenSummary": "Damaged clothing remains held for review.",
                "expandableDetail": ["The source and candidate semantics differ."],
                "evidenceIds": ["evidence:damaged-clothing"],
                "workspaceAnchors": ["award-studio:damaged-clothing"],
                "subtitles": ["Review required; no resolution was made."],
                "recommendedSequence": 3,
            },
        ],
        "readOnly": True,
        "noChangesMade": True,
    }
    return _with_fingerprint(payload)


def ma000084_projection() -> AwardVersionExplainableContextV1:
    payload = {
        "schemaVersion": "award_version_explainable_context_v1",
        "authorityEnvelope": {
            "awardHeaderId": "award-header-ma000084",
            "awardVersionId": "award-version-ma000084-published",
            "awardCode": "MA000084",
            "awardName": "Storage Services and Wholesale Award",
            "effectiveFrom": "2026-07-01",
            "effectiveTo": None,
            "lifecycle": "PUBLISHED",
            "configurationFingerprint": SHA_B,
            "semanticGraphFingerprint": SHA_C,
            "sourceAuthorityFingerprint": SHA_D,
            "projectionFingerprint": "0" * 64,
            "projectionSchemaVersion": "award_version_explainable_context_v1",
            "versionLineage": {"predecessorAwardVersionId": "ma000084-prior"},
        },
        "semanticNodes": [
            _node(
                "semantic:ma000084:saturday",
                "RATE_TREATMENT",
                "SATURDAY_WHOLESALE",
                "Configured wholesale Saturday treatment",
                "EXPLICIT_STRUCTURED",
                ["evidence:ma000084:saturday"],
                values={"configuredTreatment": "SATURDAY_WHOLESALE"},
            )
        ],
        "relationships": [],
        "evidence": [
            _evidence(
                "evidence:ma000084:saturday",
                "semantic:ma000084:saturday",
                "MA000084 configured clause evidence",
                SHA_E,
                12,
            )
        ],
        "operationalBindings": [],
        "holds": [],
        "completeness": [],
        "presentationPayloads": [],
        "readOnly": True,
        "noChangesMade": True,
    }
    return _with_fingerprint(payload)


def request(
    projection: AwardVersionExplainableContextV1,
    question: str,
    *,
    mode: str = "CHAT",
    **updates,
) -> AwardStudioMinervaQuestionRequest:
    authority = projection.authorityEnvelope
    values = {
        "contractVersion": "award_version_minerva_question_v1",
        "requestIdentity": "request-award-0001",
        "question": question,
        "presentationMode": mode,
        "awardVersionId": authority.awardVersionId,
        "configurationFingerprint": authority.configurationFingerprint,
        "semanticGraphFingerprint": authority.semanticGraphFingerprint,
        "sourceAuthorityFingerprint": authority.sourceAuthorityFingerprint,
        "projectionFingerprint": authority.projectionFingerprint,
        "projection": projection,
        "conversationHistory": [],
        "workerSpecificContextIncluded": False,
    }
    values.update(updates)
    return AwardStudioMinervaQuestionRequest(**values)


def test_projection_fingerprint_is_canonical_and_excludes_only_its_own_value() -> None:
    projection = ma000027_projection()
    assert canonical_projection_fingerprint(projection) == projection.authorityEnvelope.projectionFingerprint
    replaced = projection.model_copy(
        update={
            "authorityEnvelope": projection.authorityEnvelope.model_copy(
                update={"projectionFingerprint": "f" * 64}
            )
        }
    )
    assert canonical_projection_fingerprint(replaced) == canonical_projection_fingerprint(projection)


def test_configured_saturday_answer_is_exact_version_grounded() -> None:
    response = ask_award_studio_question(request(ma000027_projection(), "What Saturday treatment is configured?"))
    assert response.answerClassification == "EXPLICIT_STRUCTURED"
    assert response.awardVersionId == MA000027_VERSION
    assert response.semanticIdentities == ["semantic:saturday"]
    assert response.relationshipIdentities == ["relationship:saturday-rate", "relationship:ot1-saturday"]
    assert response.evidenceIdentities == ["evidence:saturday"]
    assert "This configured AwardVersion contains" in response.answer
    assert response.generalCorpusUsedAsConfiguredAuthority is False
    assert response.workerDecisionEvidenceIncluded is False


def test_deterministically_derived_ot1_is_labelled_as_derived() -> None:
    response = ask_award_studio_question(request(ma000027_projection(), "Explain configured OT1."))
    assert response.questionClassification == "OVERTIME_1"
    assert response.answerClassification == "DETERMINISTICALLY_DERIVABLE"
    assert response.semanticIdentities == ["semantic:ot1"]
    assert "deterministically derivable" in response.answer


@pytest.mark.parametrize(
    ("question", "classification", "semantic_identity"),
    [
        ("Which classification is configured?", "CLASSIFICATION", "semantic:classification"),
        ("What Sunday treatment is configured?", "SUNDAY", "semantic:sunday"),
        ("What allowance is configured?", "ALLOWANCE_REIMBURSEMENT", "semantic:allowance"),
    ],
)
def test_other_configured_domains_are_selected_from_semantic_identity_not_award_code(
    question: str,
    classification: str,
    semantic_identity: str,
) -> None:
    response = ask_award_studio_question(request(ma000027_projection(), question))
    assert response.questionClassification == classification
    assert response.answerClassification == "EXPLICIT_STRUCTURED"
    assert semantic_identity in response.semanticIdentities


def test_version_and_source_answers_echo_only_projection_authority() -> None:
    projection = ma000027_projection()
    version = ask_award_studio_question(request(projection, "Show the selected version lineage."))
    assert version.questionClassification == "VERSION_LINEAGE"
    assert version.answerClassification == "EXPLICIT_STRUCTURED"
    assert MA000027_VERSION in version.answer
    assert "GENERATED_INACTIVE" in version.answer

    sources = ask_award_studio_question(request(projection, "What source evidence supports this version?"))
    assert sources.questionClassification == "SOURCE_EVIDENCE"
    assert sources.answerClassification == "EXPLICIT_STRUCTURED"
    assert len(sources.evidenceIdentities) == len(projection.evidence)
    assert SHA_A in sources.answer


def test_damaged_clothing_hold_remains_unresolved_and_explains_semantic_difference() -> None:
    response = ask_award_studio_question(request(ma000027_projection(), "Why is damaged clothing unresolved?"))
    assert response.answerClassification == "HELD"
    assert response.holdIdentities == ["hold:damaged-clothing"]
    assert "REIMBURSEMENT" in response.answer
    assert "ALLOWANCE" in response.answer
    assert "has not resolved or reclassified" in response.answer
    assert response.noChangesMade is True


def test_not_configured_and_missing_are_not_filled_from_general_corpus() -> None:
    public_holiday = ask_award_studio_question(request(ma000027_projection(), "What public holiday rule is configured?"))
    assert public_holiday.answerClassification == "NOT_CONFIGURED"
    assert "does not contain a configured rule" in public_holiday.answer
    assert public_holiday.generalCorpusUsedAsConfiguredAuthority is False

    ot2 = ask_award_studio_question(request(ma000027_projection(), "Explain configured OT2."))
    assert ot2.answerClassification == "MISSING"
    assert "missing governed authority" in ot2.answer
    assert ot2.semanticIdentities == []


def test_conflicting_authority_is_surfaced_without_silent_reconciliation() -> None:
    projection = ma000027_projection()
    nodes = [
        node.model_copy(update={"authorityClassification": "CONFLICT", "status": "CONFLICT"})
        if node.semanticIdentity == "semantic:saturday"
        else node
        for node in projection.semanticNodes
    ]
    conflicted = projection.model_copy(update={"semanticNodes": nodes})
    conflicted = conflicted.model_copy(
        update={
            "authorityEnvelope": conflicted.authorityEnvelope.model_copy(
                update={"projectionFingerprint": canonical_projection_fingerprint(conflicted)}
            )
        }
    )
    response = ask_award_studio_question(request(conflicted, "What Saturday treatment is configured?"))
    assert response.answerClassification == "CONFLICT"
    assert "conflicting configured authority" in response.answer
    assert "has not reconciled" in response.answer


def test_stale_envelope_and_cross_version_history_fail_closed() -> None:
    projection = ma000027_projection()
    with pytest.raises(ValidationError, match="exact AwardVersion projection"):
        request(projection, "Overview", awardVersionId="stale-award-version")

    authority = projection.authorityEnvelope
    stale_history = [
        {
            "turnIdentity": "history-0001",
            "role": "MINERVA",
            "content": "Earlier text is continuity only.",
            "awardVersionId": authority.awardVersionId,
            "configurationFingerprint": authority.configurationFingerprint,
            "semanticGraphFingerprint": authority.semanticGraphFingerprint,
            "sourceAuthorityFingerprint": authority.sourceAuthorityFingerprint,
            "projectionFingerprint": "f" * 64,
        }
    ]
    with pytest.raises(ValidationError, match="history must be pinned"):
        request(projection, "Overview", conversationHistory=stale_history)


def test_tampered_projection_with_stale_fingerprint_fails_planner_validation() -> None:
    projection = ma000027_projection()
    tampered = projection.model_copy(
        update={
            "semanticNodes": [
                projection.semanticNodes[0].model_copy(update={"friendlyName": "Tampered authority"}),
                *projection.semanticNodes[1:],
            ]
        }
    )
    with pytest.raises(AwardStudioContractError, match="fingerprint mismatch"):
        build_answer_plan(request(tampered, "Give me an overview."))


def test_chat_and_level2_share_identical_authority_plan_and_only_presentation_changes() -> None:
    projection = ma000027_projection()
    chat = ask_award_studio_question(request(projection, "What Saturday treatment is configured?", mode="CHAT"))
    level2 = ask_award_studio_question(request(projection, "What Saturday treatment is configured?", mode="LEVEL_2"))
    assert chat.plannerFingerprint == level2.plannerFingerprint
    assert chat.answer == level2.answer
    assert chat.semanticIdentities == level2.semanticIdentities
    assert chat.relationshipIdentities == level2.relationshipIdentities
    assert chat.evidenceIdentities == level2.evidenceIdentities
    assert chat.projectionFingerprint == level2.projectionFingerprint
    assert chat.presentation.spokenSummary is None
    assert chat.presentation.subtitles == []
    assert level2.presentation.spokenSummary == "The selected version contains a configured Saturday treatment."
    assert level2.presentation.subtitles == ["Configured Saturday treatment."]
    assert level2.presentation.evidenceCards[0].evidenceIdentity == "evidence:saturday"


def test_ma000084_uses_the_same_generic_contract_without_award_specific_branching() -> None:
    projection = ma000084_projection()
    response = ask_award_studio_question(request(projection, "What Saturday treatment is configured?"))
    assert response.awardCode == "MA000084"
    assert response.answerClassification == "EXPLICIT_STRUCTURED"
    assert response.semanticIdentities == ["semantic:ma000084:saturday"]
    assert response.evidenceIdentities == ["evidence:ma000084:saturday"]
    assert "wholesale" in response.answer.lower()


def test_worker_specific_execution_question_is_withheld() -> None:
    response = ask_award_studio_question(request(ma000027_projection(), "Why did this worker get this rate?"))
    assert response.questionClassification == "UNKNOWN_OR_UNSUPPORTED"
    assert "cannot" in response.answer.lower()
    assert "worker" in response.answer.lower()
    assert response.workerDecisionEvidenceIncluded is False


def test_unknown_graph_reference_is_rejected() -> None:
    payload = ma000084_projection().model_dump(mode="json")
    payload["authorityEnvelope"]["projectionFingerprint"] = "0" * 64
    payload["semanticNodes"][0]["evidenceIds"] = ["evidence:foreign"]
    with pytest.raises(ValidationError, match="unknown evidence"):
        AwardVersionExplainableContextV1.model_validate(payload)


def test_api_route_echoes_exact_version_and_fingerprints(client) -> None:
    req = request(ma000027_projection(), "What Saturday treatment is configured?")
    response = client.post("/api/v1/minerva/award-studio/questions", json=req.model_dump(mode="json"))
    assert response.status_code == 200
    body = response.json()
    assert body["contractVersion"] == "award_version_minerva_answer_v1"
    assert body["awardVersionId"] == req.awardVersionId
    assert body["configurationFingerprint"] == req.configurationFingerprint
    assert body["semanticGraphFingerprint"] == req.semanticGraphFingerprint
    assert body["sourceAuthorityFingerprint"] == req.sourceAuthorityFingerprint
    assert body["projectionFingerprint"] == req.projectionFingerprint
    assert body["deterministicAnswerUsed"] is True
    assert body["noChangesMade"] is True


def test_api_route_rejects_tampered_projection_fingerprint(client) -> None:
    req = request(ma000027_projection(), "Give me an overview.")
    payload = copy.deepcopy(req.model_dump(mode="json"))
    payload["projection"]["semanticNodes"][0]["friendlyName"] = "Tampered authority"
    response = client.post("/api/v1/minerva/award-studio/questions", json=payload)
    assert response.status_code == 422
    assert "projection fingerprint mismatch" in response.json()["detail"]
