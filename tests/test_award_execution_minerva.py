from __future__ import annotations

import copy
from types import SimpleNamespace
from uuid import UUID

import pytest
from pydantic import ValidationError

from app.api.v1.award_execution_minerva import configured_award_execution_evidence_provider
from app.api.v1.award_execution_minerva import authenticated_award_execution_principal
from app.main import app
from app.schemas.award_execution_minerva import (
    AwardExecutionPrincipal,
    AwardExecutionMinervaQuestionRequest,
    AwardRuntimeDecisionEvidenceV1,
)
from app.services.award_execution_question_service import ask_award_execution_question
from app.services.workforce_award_evidence_client import (
    AwardExecutionEvidenceInvalid,
    AwardExecutionEvidenceNotFound,
    AwardExecutionExactVersionMismatch,
    WorkforceAwardExecutionEvidenceClient,
)
from tests.test_award_studio_minerva_exact_version import ma000027_projection, request as configuration_request
from app.services.award_studio_question_service import ask_award_studio_question


VERSION_ID = "5A6145AF-0A80-4BD0-ADAD-80C7ABB254E9"
NORMALIZED_VERSION_ID = str(UUID(VERSION_ID))
CALC_LINE_ID = "dddddddd-dddd-4ddd-8ddd-dddddddddddd"
FOREIGN_CALC_LINE_ID = "eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee"
STALE_VERSION_ID = "ffffffff-ffff-4fff-8fff-ffffffffffff"
CONFIGURATION_FINGERPRINT = "a" * 64
SEMANTIC_FINGERPRINT = "b" * 64
SOURCE_FINGERPRINT = "c" * 64
ACCOUNT_ID = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
OTHER_ACCOUNT_ID = "cccccccc-cccc-4ccc-8ccc-cccccccccccc"
RATE_TYPE_ID = "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"


def decision_evidence() -> dict:
    return {
        "schemaVersion": "award_runtime_decision_evidence_v1",
        "authorityMode": "STORED_EXECUTION_EVIDENCE",
        "evidencePersistence": "DURABLE_RUNTIME_RECORD",
        "header": {
            "decisionEvidenceId": "decision-evidence-0001",
            "evaluationId": "candidate-overtime",
            "executionId": "execution-0001",
            "executedAtUtc": "2026-08-16T01:02:03Z",
            "awardId": "award-ma000027",
            "awardVersionId": VERSION_ID,
            "configurationFingerprint": CONFIGURATION_FINGERPRINT,
            "semanticGraphFingerprint": SEMANTIC_FINGERPRINT,
            "sourceAuthorityFingerprint": SOURCE_FINGERPRINT,
            "decisionEvidenceHash": "1" * 64,
            "objectTimeId": "object-time-0001",
            "inputFacts": {
                "snapshotId": "fact-snapshot-0001",
                "snapshotFingerprint": "d" * 64,
                "appointmentId": "appointment-0001",
                "workerId": "worker-0001",
                "employmentType": "CASUAL",
                "positionId": "position-0001",
                "awardPositionClassId": "award-class-0001",
                "facts": {
                    "workedDate": "2026-08-12",
                    "hours": "14.0",
                    "dayType": "WEEKDAY",
                },
            },
        },
        "result": {
            "winnerCandidateEvaluationId": "candidate-overtime",
            "configuredRuleId": "configured-rule-overtime-progression",
            "semanticIdentity": "semantic:overtime:second-tier",
            "executableProvisionIdentity": "provision:ma000027:21.2",
            "rateResolution": {
                "rateTypeId": RATE_TYPE_ID,
                "rateSourceId": "rate-source-overtime-0001",
                "value": "57.915",
                "unit": "HOUR",
                "currency": "AUD",
            },
            "payResult": {
                "calcInterpreterLineId": CALC_LINE_ID,
                "resultLineSequence": 1,
                "quantity": "6.0",
                "rate": "57.915",
                "amount": "347.49",
                "currency": "AUD",
                "resultHash": "2" * 64,
            },
        },
        "evaluations": [
            {
                "candidateEvaluationId": "candidate-ordinary",
                "candidateKind": "RATE_CELL",
                "decisionStage": "RATE_RESOLUTION",
                "candidateIdentity": "rate-cell:weekday-ordinary",
                "appliesToResultLineSequence": 1,
                "rateSourceId": "rate-source-ordinary-0001",
                "configuredRuleId": "configured-rule-ordinary",
                "semanticIdentity": "semantic:ordinary:weekday",
                "executableProvisionIdentity": "provision:ma000027:14.1",
                "applicability": {
                    "applicable": True,
                    "reasonCode": "WEEKDAY_ORDINARY_CANDIDATE",
                    "facts": {"dayType": "WEEKDAY"},
                },
                "precedence": {
                    "stage": "RATE_RESOLUTION",
                    "dimension": "HOURS_PROGRESSION",
                    "rank": 2,
                    "outcome": "LOSER",
                    "reasonCode": "OVERTIME_THRESHOLD_EXCEEDED",
                },
                "sourceEvidenceReferences": ["evidence:ordinary"],
            },
            {
                "candidateEvaluationId": "candidate-overtime",
                "candidateKind": "RATE_CELL",
                "decisionStage": "RATE_RESOLUTION",
                "candidateIdentity": "rate-cell:overtime-second-tier",
                "appliesToResultLineSequence": 1,
                "rateSourceId": "rate-source-overtime-0001",
                "configuredRuleId": "configured-rule-overtime-progression",
                "semanticIdentity": "semantic:overtime:second-tier",
                "executableProvisionIdentity": "provision:ma000027:21.2",
                "applicability": {
                    "applicable": True,
                    "reasonCode": "DAILY_HOURS_ABOVE_OT2_THRESHOLD",
                    "facts": {"hours": "14.0", "thresholdHours": "10.0"},
                },
                "precedence": {
                    "stage": "RATE_RESOLUTION",
                    "dimension": "HOURS_PROGRESSION",
                    "rank": 1,
                    "outcome": "WINNER",
                    "reasonCode": "HIGHER_APPLICABLE_OVERTIME_TIER",
                },
                "sourceEvidenceReferences": ["evidence:overtime"],
            },
        ],
        "sourceEvidenceReferences": [
            {
                "evidenceIdentity": "evidence:ordinary",
                "sourceDocumentIdentity": "source:ma000027",
                "sourceSha256": "e" * 64,
                "sourceLocator": {"clause": "14.1"},
            },
            {
                "evidenceIdentity": "evidence:overtime",
                "sourceDocumentIdentity": "source:ma000027",
                "sourceSha256": "e" * 64,
                "sourceLocator": {"clause": "21.2"},
            },
        ],
    }


class StaticEvidenceProvider:
    def __init__(self, payload: dict | None = None) -> None:
        self.evidence = AwardRuntimeDecisionEvidenceV1.model_validate(payload or decision_evidence())
        self.calls: list[tuple[str, str, str]] = []

    def fetch(self, calc_interpreter_line_id: str, award_version_id: str, account_id: str):
        self.calls.append((calc_interpreter_line_id, award_version_id, account_id))
        return self.evidence


def execution_request(*, mode: str = "CHAT", **updates) -> AwardExecutionMinervaQuestionRequest:
    values = {
        "contractVersion": "award_execution_minerva_question_v1",
        "requestIdentity": "execution-question-0001",
        "question": "Why did this worker receive this pay line?",
        "presentationMode": mode,
        "calcInterpreterLineId": CALC_LINE_ID,
        "awardVersionId": VERSION_ID,
        "configurationFingerprint": CONFIGURATION_FINGERPRINT,
        "semanticGraphFingerprint": SEMANTIC_FINGERPRINT,
        "sourceAuthorityFingerprint": SOURCE_FINGERPRINT,
    }
    values.update(updates)
    return AwardExecutionMinervaQuestionRequest.model_validate(values)


def test_literal_workforce_wire_shape_and_nullable_rate_fields_are_accepted() -> None:
    payload = decision_evidence()
    payload["result"]["rateResolution"]["rateTypeId"] = None
    payload["evaluations"][0]["precedence"]["rank"] = None
    payload["evaluations"][1]["precedence"]["rank"] = None
    evidence = AwardRuntimeDecisionEvidenceV1.model_validate(payload)
    projected = evidence.model_dump(mode="json")

    assert set(projected) == {
        "schemaVersion",
        "authorityMode",
        "evidencePersistence",
        "header",
        "result",
        "evaluations",
        "sourceEvidenceReferences",
    }
    assert set(projected["header"]) == {
        "decisionEvidenceId",
        "evaluationId",
        "executionId",
        "executedAtUtc",
        "decisionEvidenceHash",
        "awardId",
        "awardVersionId",
        "configurationFingerprint",
        "semanticGraphFingerprint",
        "sourceAuthorityFingerprint",
        "objectTimeId",
        "inputFacts",
    }
    assert set(projected["result"]["rateResolution"]) == {
        "rateTypeId",
        "rateSourceId",
        "value",
        "unit",
        "currency",
    }
    assert set(projected["result"]["payResult"]) == {
        "calcInterpreterLineId",
        "resultLineSequence",
        "quantity",
        "rate",
        "amount",
        "currency",
        "resultHash",
    }
    assert set(projected["evaluations"][0]) == {
        "candidateEvaluationId",
        "candidateKind",
        "decisionStage",
        "candidateIdentity",
        "appliesToResultLineSequence",
        "rateSourceId",
        "configuredRuleId",
        "semanticIdentity",
        "executableProvisionIdentity",
        "applicability",
        "precedence",
        "sourceEvidenceReferences",
    }
    assert projected["header"]["inputFacts"]["appointmentId"] == "appointment-0001"
    assert projected["result"]["rateResolution"]["rateTypeId"] is None


def test_worker_execution_evidence_rejects_missing_appointment_identity() -> None:
    payload = decision_evidence()
    payload["header"]["inputFacts"]["appointmentId"] = None

    with pytest.raises(ValidationError):
        AwardRuntimeDecisionEvidenceV1.model_validate(payload)


def test_execution_explanation_reports_only_stored_winner_rate_and_pay_result() -> None:
    provider = StaticEvidenceProvider()
    response = ask_award_execution_question(execution_request(), provider, ACCOUNT_ID)

    assert response.decisionEvidenceId == "decision-evidence-0001"
    assert response.awardId == "award-ma000027"
    assert response.awardVersionId == VERSION_ID
    assert response.appointmentId == "appointment-0001"
    assert response.objectTimeId == "object-time-0001"
    assert response.winnerConfiguredRuleId == "configured-rule-overtime-progression"
    assert response.winnerSemanticIdentity == "semantic:overtime:second-tier"
    assert response.rateResolution.rateSourceId == "rate-source-overtime-0001"
    assert response.payResult.calcInterpreterLineId == CALC_LINE_ID
    assert str(response.payResult.amount) == "347.49"
    assert response.storedExecutionEvidenceUsed is True
    assert response.configurationExplanationUsed is False
    assert response.independentAwardRecomputationPerformed is False
    assert response.decisionEvidenceHash == "1" * 64
    assert response.resultHash == "2" * 64
    assert "HIGHER_APPLICABLE_OVERTIME_TIER" in response.answer
    assert "AUD 347.49" in response.answer
    assert provider.calls == [(CALC_LINE_ID, NORMALIZED_VERSION_ID, ACCOUNT_ID)]


def test_material_winner_and_loser_are_explained_from_recorded_outcomes() -> None:
    response = ask_award_execution_question(execution_request(), StaticEvidenceProvider(), ACCOUNT_ID)
    by_id = {item.candidateEvaluationId: item for item in response.candidateExplanations}

    assert by_id["candidate-overtime"].precedenceOutcome == "WINNER"
    assert by_id["candidate-overtime"].applicabilityReasonCode == "DAILY_HOURS_ABOVE_OT2_THRESHOLD"
    assert by_id["candidate-ordinary"].precedenceOutcome == "LOSER"
    assert by_id["candidate-ordinary"].precedenceReasonCode == "OVERTIME_THRESHOLD_EXCEEDED"
    assert by_id["candidate-ordinary"].candidateKind == "RATE_CELL"
    assert by_id["candidate-ordinary"].decisionStage == "RATE_RESOLUTION"
    assert by_id["candidate-ordinary"].candidateIdentity == "rate-cell:weekday-ordinary"
    assert by_id["candidate-ordinary"].appliesToResultLineSequence == 1
    assert by_id["candidate-ordinary"].rateSourceId == "rate-source-ordinary-0001"
    assert "rate-cell:weekday-ordinary (RATE_CELL, semantic:ordinary:weekday) was applicable" in response.answer


def test_multi_stage_precedence_preserves_upstream_and_final_winners() -> None:
    payload = decision_evidence()
    payload["evaluations"].insert(
        0,
        {
            "candidateEvaluationId": "candidate-overtime-boundary",
            "candidateKind": "RULE_BOUNDARY",
            "decisionStage": "RULE_SELECTION",
            "candidateIdentity": "rule-boundary:overtime",
            "appliesToResultLineSequence": None,
            "rateSourceId": None,
            "configuredRuleId": "configured-rule-overtime-boundary",
            "semanticIdentity": "semantic:overtime:boundary",
            "executableProvisionIdentity": "provision:ma000027:21.2:boundary",
            "applicability": {
                "applicable": True,
                "reasonCode": "OVERTIME_BOUNDARY_REACHED",
                "facts": {"hours": "14.0", "ordinaryBoundaryHours": "8.0"},
            },
            "precedence": {
                "stage": "RULE_SELECTION",
                "dimension": "ORDINARY_VS_OVERTIME",
                "rank": 20,
                "outcome": "WINNER",
                "reasonCode": "OVERTIME_SUPERSEDES_ORDINARY_AFTER_BOUNDARY",
            },
            "sourceEvidenceReferences": ["evidence:overtime"],
        },
    )
    response = ask_award_execution_question(
        execution_request(),
        StaticEvidenceProvider(payload),
        ACCOUNT_ID,
    )
    by_id = {item.candidateEvaluationId: item for item in response.candidateExplanations}

    assert by_id["candidate-overtime-boundary"].precedenceStage == "RULE_SELECTION"
    assert by_id["candidate-overtime-boundary"].precedenceOutcome == "WINNER"
    assert by_id["candidate-overtime"].precedenceStage == "RATE_RESOLUTION"
    assert by_id["candidate-overtime"].precedenceOutcome == "WINNER"
    assert response.winnerCandidateEvaluationId == "candidate-overtime"
    assert "WINNER at RULE_SELECTION" in response.answer


def test_rate_resolution_stage_requires_exactly_one_result_winner() -> None:
    payload = decision_evidence()
    payload["evaluations"][0]["precedence"]["outcome"] = "WINNER"
    with pytest.raises(ValidationError, match="exactly one RATE_RESOLUTION"):
        AwardRuntimeDecisionEvidenceV1.model_validate(payload)


def test_candidate_projection_stage_line_and_rate_source_links_are_validated() -> None:
    payload = decision_evidence()
    payload["evaluations"][0]["decisionStage"] = "RULE_SELECTION"
    with pytest.raises(ValidationError, match="decisionStage must equal"):
        AwardRuntimeDecisionEvidenceV1.model_validate(payload)

    payload = decision_evidence()
    payload["evaluations"][0]["appliesToResultLineSequence"] = 2
    with pytest.raises(ValidationError, match="selected result line sequence"):
        AwardRuntimeDecisionEvidenceV1.model_validate(payload)

    payload = decision_evidence()
    payload["evaluations"][1]["rateSourceId"] = "rate-source-wrong"
    with pytest.raises(ValidationError, match="RateSource must match"):
        AwardRuntimeDecisionEvidenceV1.model_validate(payload)


def test_cross_calc_line_evidence_is_rejected_after_trusted_fetch() -> None:
    payload = decision_evidence()
    payload["result"]["payResult"]["calcInterpreterLineId"] = FOREIGN_CALC_LINE_ID
    with pytest.raises(AwardExecutionExactVersionMismatch, match="different CalcInterpreterLine"):
        ask_award_execution_question(
            execution_request(),
            StaticEvidenceProvider(payload),
            ACCOUNT_ID,
        )

def test_candidate_projection_remains_extra_forbid() -> None:
    payload = decision_evidence()
    payload["evaluations"][0]["uncontractedField"] = "must-not-pass-through"
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        AwardRuntimeDecisionEvidenceV1.model_validate(payload)


def test_orphan_loser_and_invalid_rank_order_fail_closed() -> None:
    payload = decision_evidence()
    payload["evaluations"][0]["precedence"]["dimension"] = "ORPHAN_CONTEST"
    with pytest.raises(ValidationError, match="same-line winner"):
        AwardRuntimeDecisionEvidenceV1.model_validate(payload)

    payload = decision_evidence()
    payload["evaluations"][0]["precedence"]["rank"] = 1
    payload["evaluations"][1]["precedence"]["rank"] = 2
    with pytest.raises(ValidationError, match="numerically greater rank"):
        AwardRuntimeDecisionEvidenceV1.model_validate(payload)

    payload = decision_evidence()
    payload["evaluations"][0]["precedence"]["rank"] = 1
    payload["evaluations"][1]["precedence"]["rank"] = 1
    with pytest.raises(ValidationError, match="unique ranks"):
        AwardRuntimeDecisionEvidenceV1.model_validate(payload)

    payload = decision_evidence()
    payload["evaluations"][0]["precedence"]["rank"] = None
    payload["evaluations"][1]["precedence"]["rank"] = None
    assert AwardRuntimeDecisionEvidenceV1.model_validate(payload)


def test_source_references_and_required_authority_hashes_fail_closed() -> None:
    payload = decision_evidence()
    payload["evaluations"][1]["sourceEvidenceReferences"] = []
    with pytest.raises(ValidationError, match="winner must reference source evidence"):
        AwardRuntimeDecisionEvidenceV1.model_validate(payload)

    payload = decision_evidence()
    payload["evaluations"][0]["sourceEvidenceReferences"] = ["evidence:orphan"]
    with pytest.raises(ValidationError, match="only supplied source evidence"):
        AwardRuntimeDecisionEvidenceV1.model_validate(payload)

    payload = decision_evidence()
    payload["header"].pop("sourceAuthorityFingerprint")
    with pytest.raises(ValidationError):
        AwardRuntimeDecisionEvidenceV1.model_validate(payload)

    payload = decision_evidence()
    payload["header"]["decisionEvidenceHash"] = "NOT-A-SHA"
    with pytest.raises(ValidationError):
        AwardRuntimeDecisionEvidenceV1.model_validate(payload)

    payload = decision_evidence()
    payload["result"]["payResult"]["resultHash"] = "A" * 64
    with pytest.raises(ValidationError):
        AwardRuntimeDecisionEvidenceV1.model_validate(payload)


def test_integrity_hashes_are_preserved_and_bound_into_explanation_fingerprint() -> None:
    original = ask_award_execution_question(
        execution_request(), StaticEvidenceProvider(), ACCOUNT_ID
    )
    changed_payload = decision_evidence()
    changed_payload["header"]["decisionEvidenceHash"] = "3" * 64
    changed = ask_award_execution_question(
        execution_request(), StaticEvidenceProvider(changed_payload), ACCOUNT_ID
    )
    other_account = ask_award_execution_question(
        execution_request(), StaticEvidenceProvider(), OTHER_ACCOUNT_ID
    )
    assert changed.decisionEvidenceHash == "3" * 64
    assert changed.explanationFingerprint != original.explanationFingerprint
    assert other_account.explanationFingerprint != original.explanationFingerprint


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("awardVersionId", STALE_VERSION_ID),
        ("configurationFingerprint", "f" * 64),
        ("semanticGraphFingerprint", "f" * 64),
        ("sourceAuthorityFingerprint", "f" * 64),
    ],
)
def test_exact_version_or_fingerprint_mismatch_fails_closed(field: str, value: str) -> None:
    with pytest.raises(AwardExecutionExactVersionMismatch, match="exact AwardVersion authority"):
        ask_award_execution_question(
            execution_request(**{field: value}),
            StaticEvidenceProvider(),
            ACCOUNT_ID,
        )


def test_public_execution_request_requires_uuid_object_identities() -> None:
    with pytest.raises(ValidationError):
        execution_request(calcInterpreterLineId="predictable-line-name")
    with pytest.raises(ValidationError):
        execution_request(awardVersionId="current-version")


def test_execution_evidence_and_durable_authority_discriminators_are_required() -> None:
    values = execution_request().model_dump(mode="json")
    values["decisionEvidence"] = decision_evidence()
    with pytest.raises(ValidationError):
        AwardExecutionMinervaQuestionRequest.model_validate(values)

    values = decision_evidence()
    values["authorityMode"] = "CONFIGURATION_EXPLANATION"
    with pytest.raises(ValidationError):
        AwardRuntimeDecisionEvidenceV1.model_validate(values)

    values = decision_evidence()
    values["evidencePersistence"] = "TRANSIENT"
    with pytest.raises(ValidationError):
        AwardRuntimeDecisionEvidenceV1.model_validate(values)

    values = execution_request().model_dump(mode="json")
    values.pop("sourceAuthorityFingerprint")
    with pytest.raises(ValidationError):
        AwardExecutionMinervaQuestionRequest.model_validate(values)


def test_winner_identity_must_match_recorded_evaluation_and_result_rule() -> None:
    values = decision_evidence()
    values["result"]["winnerCandidateEvaluationId"] = "candidate-ordinary"
    with pytest.raises(ValidationError, match="winner identity"):
        AwardRuntimeDecisionEvidenceV1.model_validate(values)

    values = decision_evidence()
    values["result"]["semanticIdentity"] = "semantic:invented"
    with pytest.raises(ValidationError, match="result rule identities"):
        AwardRuntimeDecisionEvidenceV1.model_validate(values)

    values = decision_evidence()
    values["header"]["evaluationId"] = "candidate-ordinary"
    with pytest.raises(ValidationError, match="winning result-line evaluation"):
        AwardRuntimeDecisionEvidenceV1.model_validate(values)


def test_level2_changes_presentation_only_not_authority_or_answer() -> None:
    chat = ask_award_execution_question(
        execution_request(mode="CHAT"), StaticEvidenceProvider(), ACCOUNT_ID
    )
    level2 = ask_award_execution_question(
        execution_request(mode="LEVEL_2"), StaticEvidenceProvider(), ACCOUNT_ID
    )

    assert level2.explanationFingerprint == chat.explanationFingerprint
    assert level2.answer == chat.answer
    assert level2.candidateExplanations == chat.candidateExplanations
    assert level2.rateResolution == chat.rateResolution
    assert level2.payResult == chat.payResult
    assert chat.presentation.spokenSummary is None
    assert level2.presentation.spokenSummary is not None


def test_configuration_explanation_does_not_imply_worker_execution() -> None:
    configuration = ma000027_projection()
    response = ask_award_studio_question(
        configuration_request(configuration, "Why did this worker get this rate?")
    )
    assert response.questionClassification == "UNKNOWN_OR_UNSUPPORTED"
    assert response.workerDecisionEvidenceIncluded is False
    assert "cannot" in response.answer.lower()


def test_execution_api_requires_evidence_and_rejects_stale_version(client) -> None:
    req = execution_request()
    provider = StaticEvidenceProvider()
    app.dependency_overrides[configured_award_execution_evidence_provider] = lambda: provider
    app.dependency_overrides[authenticated_award_execution_principal] = lambda: AwardExecutionPrincipal(
        accountId=ACCOUNT_ID
    )
    try:
        response = client.post(
            "/api/v1/minerva/award-execution/questions",
            json=req.model_dump(mode="json"),
        )
        assert response.status_code == 200
        assert response.json()["storedExecutionEvidenceUsed"] is True

        stale = copy.deepcopy(req.model_dump(mode="json"))
        stale["awardVersionId"] = STALE_VERSION_ID
        stale_response = client.post("/api/v1/minerva/award-execution/questions", json=stale)
        assert stale_response.status_code == 409
        assert "exact AwardVersion authority" in str(stale_response.json())
    finally:
        app.dependency_overrides.pop(configured_award_execution_evidence_provider, None)
        app.dependency_overrides.pop(authenticated_award_execution_principal, None)


def test_execution_api_fails_closed_when_workforce_provider_is_not_configured(client) -> None:
    app.dependency_overrides[authenticated_award_execution_principal] = lambda: AwardExecutionPrincipal(
        accountId=ACCOUNT_ID
    )
    try:
        response = client.post(
            "/api/v1/minerva/award-execution/questions",
            json=execution_request().model_dump(mode="json"),
        )
        assert response.status_code == 503
        assert "not configured" in response.json()["detail"]
    finally:
        app.dependency_overrides.pop(authenticated_award_execution_principal, None)


def test_execution_api_does_not_fall_back_when_stored_evidence_is_absent(client) -> None:
    class MissingEvidenceProvider:
        def fetch(self, calc_interpreter_line_id: str, award_version_id: str, account_id: str):
            raise AwardExecutionEvidenceNotFound("no stored Award decision evidence exists")

    app.dependency_overrides[configured_award_execution_evidence_provider] = MissingEvidenceProvider
    app.dependency_overrides[authenticated_award_execution_principal] = lambda: AwardExecutionPrincipal(
        accountId=ACCOUNT_ID
    )
    try:
        response = client.post(
            "/api/v1/minerva/award-execution/questions",
            json=execution_request().model_dump(mode="json"),
        )
        assert response.status_code == 404
        assert "no stored Award decision evidence" in response.json()["detail"]
    finally:
        app.dependency_overrides.pop(configured_award_execution_evidence_provider, None)
        app.dependency_overrides.pop(authenticated_award_execution_principal, None)


def test_execution_api_requires_authenticated_service_principal_and_account_scope(
    client,
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        "app.api.v1.award_execution_minerva.get_settings",
        lambda: SimpleNamespace(award_execution_inbound_service_token="trusted-inbound-token"),
    )
    provider = StaticEvidenceProvider()
    app.dependency_overrides[configured_award_execution_evidence_provider] = lambda: provider
    payload = execution_request().model_dump(mode="json")
    try:
        missing = client.post("/api/v1/minerva/award-execution/questions", json=payload)
        assert missing.status_code == 401

        wrong = client.post(
            "/api/v1/minerva/award-execution/questions",
            json=payload,
            headers={"Authorization": "Bearer wrong", "X-Account-Id": ACCOUNT_ID},
        )
        assert wrong.status_code == 401

        account_missing = client.post(
            "/api/v1/minerva/award-execution/questions",
            json=payload,
            headers={"Authorization": "Bearer trusted-inbound-token"},
        )
        assert account_missing.status_code == 422

        allowed = client.post(
            "/api/v1/minerva/award-execution/questions",
            json=payload,
            headers={
                "Authorization": "Bearer trusted-inbound-token",
                "X-Account-Id": ACCOUNT_ID,
            },
        )
        assert allowed.status_code == 200
        assert provider.calls == [(CALC_LINE_ID, NORMALIZED_VERSION_ID, ACCOUNT_ID)]
    finally:
        app.dependency_overrides.pop(configured_award_execution_evidence_provider, None)


def test_execution_api_rejects_account_scope_in_json_body(client) -> None:
    payload = execution_request().model_dump(mode="json")
    payload["accountId"] = ACCOUNT_ID
    app.dependency_overrides[authenticated_award_execution_principal] = lambda: AwardExecutionPrincipal(
        accountId=ACCOUNT_ID
    )
    app.dependency_overrides[configured_award_execution_evidence_provider] = lambda: StaticEvidenceProvider()
    try:
        response = client.post("/api/v1/minerva/award-execution/questions", json=payload)
        assert response.status_code == 422
    finally:
        app.dependency_overrides.pop(authenticated_award_execution_principal, None)
        app.dependency_overrides.pop(configured_award_execution_evidence_provider, None)


def test_workforce_provider_reads_exact_calc_line_and_award_version(monkeypatch) -> None:
    captured: dict = {}

    def fake_get(url, *, params, headers, timeout):
        captured.update(url=url, params=params, headers=headers, timeout=timeout)
        import httpx

        return httpx.Response(200, json=decision_evidence())

    monkeypatch.setattr("app.services.workforce_award_evidence_client.httpx.get", fake_get)
    provider = WorkforceAwardExecutionEvidenceClient(
        base_url="https://workforce.internal",
        timeout_seconds=3.0,
        service_token="service-token",
    )
    evidence = provider.fetch(CALC_LINE_ID, NORMALIZED_VERSION_ID, ACCOUNT_ID)

    assert captured["url"].endswith(
        f"/api/v1/interpreter-results/calc-interpreter-lines/{CALC_LINE_ID}/award-decision-evidence"
    )
    assert captured["params"] == {
        "award_version_id": NORMALIZED_VERSION_ID,
        "account_id": ACCOUNT_ID,
    }
    assert captured["headers"]["Authorization"] == "Bearer service-token"
    assert evidence.authorityMode == "STORED_EXECUTION_EVIDENCE"


@pytest.mark.parametrize(
    ("status_code", "exception_type"),
    [
        (404, AwardExecutionEvidenceNotFound),
        (409, AwardExecutionExactVersionMismatch),
        (422, AwardExecutionEvidenceInvalid),
    ],
)
def test_workforce_provider_preserves_evidence_failure_statuses(
    monkeypatch,
    status_code: int,
    exception_type: type[Exception],
) -> None:
    import httpx

    monkeypatch.setattr(
        "app.services.workforce_award_evidence_client.httpx.get",
        lambda *args, **kwargs: httpx.Response(status_code),
    )
    provider = WorkforceAwardExecutionEvidenceClient(
        base_url="https://workforce.internal",
        timeout_seconds=3.0,
    )
    with pytest.raises(exception_type):
        provider.fetch(CALC_LINE_ID, NORMALIZED_VERSION_ID, ACCOUNT_ID)


def test_workforce_provider_rejects_non_durable_or_malformed_payload(monkeypatch) -> None:
    import httpx

    payload = decision_evidence()
    payload["evidencePersistence"] = "TRANSIENT"
    monkeypatch.setattr(
        "app.services.workforce_award_evidence_client.httpx.get",
        lambda *args, **kwargs: httpx.Response(200, json=payload),
    )
    provider = WorkforceAwardExecutionEvidenceClient(
        base_url="https://workforce.internal",
        timeout_seconds=3.0,
    )
    with pytest.raises(AwardExecutionEvidenceInvalid, match="durable execution contract"):
        provider.fetch(CALC_LINE_ID, NORMALIZED_VERSION_ID, ACCOUNT_ID)
