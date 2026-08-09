from __future__ import annotations

import json
from pathlib import Path

import pytest
from sqlalchemy import select

from app.models.audit import AIInteractionAudit
from app.schemas.minerva_admin_configuration import LeavePolicyConfigurationEvidencePacket
from app.services import minerva_admin_configuration_service as service
from app.services.minerva_admin_configuration_service import (
    AdminConfigurationEvidenceError,
    ask_admin_configuration,
    classify_admin_question,
    preview_admin_configuration_change,
    validate_packet,
)


FIXTURE = Path(__file__).parents[1] / "app" / "fixtures" / "minerva_qld_lsl_admin_configuration_packet.json"


def packet() -> LeavePolicyConfigurationEvidencePacket:
    return LeavePolicyConfigurationEvidencePacket.model_validate(json.loads(FIXTURE.read_text(encoding="utf-8")))


def test_packet_fixture_is_exactly_validated_and_hashable() -> None:
    value = packet()
    assert validate_packet(value) == value
    assert hash(value) == hash(packet())
    assert value.packet_fingerprint == "9d81c00d1064edab7a7a76d3564f275eb90a62bcf1e3d94510cde8e5c240a4c0"
    assert value.model_dump_json() == packet().model_dump_json()


def test_admin_packet_endpoint_consumes_fixture_and_proposal_endpoint_is_preview_only(client) -> None:
    body = {"packet": json.loads(FIXTURE.read_text(encoding="utf-8")), "message": "Which policy version is selected?"}
    response = client.post("/api/v1/minerva/queensland-general-lsl/admin-configuration/ask", json=body)
    assert response.status_code == 200
    assert response.json()["outcome"] == "ANSWERED"
    assert response.json()["answer"].splitlines()[0] == "Answer"

    proposal = client.post(
        "/api/v1/minerva/queensland-general-lsl/admin-configuration/proposal",
        json={"packet": body["packet"], "requested_change": "Lower the ten-year threshold to eight years."},
    )
    assert proposal.status_code == 200
    assert proposal.json()["outcome"] == "PREVIEW_ONLY"
    assert proposal.json()["no_mutation"] is True


@pytest.mark.parametrize(
    ("question", "intent"),
    [
        ("Which Queensland General LSL policy and version is selected?", "CONFIGURATION_IDENTITY"),
        ("Is this supplied configuration or our organisation’s successor?", "OWNERSHIP_LINEAGE"),
        ("Which service and entitlement settings are configured?", "CONFIGURED_RULE_VALUES"),
        ("Why was the ten-year setting configured this way?", "RATIONALE"),
        ("Which legal source supports that setting?", "SOURCE"),
        ("Which settings can an administrator change?", "CHANGEABILITY"),
        ("What is configured, needs review, inactive or on hold?", "READINESS"),
        ("Is calculation or runtime processing enabled?", "RUNTIME_SUPPORT"),
        ("How does this version differ from its predecessor?", "VERSION_LINEAGE"),
        ("What would changing this setting affect?", "PROPOSED_CHANGE_IMPACT"),
        ("Would that change require a successor version?", "PROPOSED_CHANGE_IMPACT"),
        ("Would the proposed change weaken a statutory minimum?", "PROPOSED_CHANGE_IMPACT"),
        ("What configuration evidence is missing?", "MISSING_EVIDENCE"),
        ("Is QLeave operational?", "QLEAVE_BOUNDARY"),
    ],
)
def test_representative_administrator_intents_are_deterministic(question: str, intent: str) -> None:
    assert classify_admin_question(question) == intent
    answer = ask_admin_configuration(packet=packet(), question=question)
    assert answer.intent == intent
    assert answer.answer.splitlines()[0] == "Answer"
    assert answer.answer.index("What matters") < answer.answer.index("Capability boundary") < answer.answer.index("Sources")
    assert all(label in answer.answer for label in answer.evidence_classifications)


def test_answers_keep_configuration_separate_from_knowledge_pack_facts() -> None:
    answer = ask_admin_configuration(packet=packet(), question="Which service and entitlement settings are configured?")
    assert "[Supplied configuration]" in answer.answer
    assert "[Knowledge-pack fact] The published pack is explanatory evidence" in answer.answer
    assert "8.6667 WEEKS" in answer.answer
    assert "10 YEARS" in answer.answer
    assert "3 CALENDAR_MONTHS" in answer.answer


def test_negative_identity_scope_provenance_pack_and_missing_value_cases_fail_closed() -> None:
    value = packet()
    with pytest.raises(AdminConfigurationEvidenceError, match="Policy and policy-version identity"):
        validate_packet(value.model_copy(update={"selected_policy_id": ""}))
    with pytest.raises(AdminConfigurationEvidenceError, match="tenant scope"):
        validate_packet(value.model_copy(update={"tenant_reference": ""}))
    with pytest.raises(AdminConfigurationEvidenceError, match="fingerprint"):
        validate_packet(value.model_copy(update={"packet_fingerprint": "0" * 64}))
    with pytest.raises(AdminConfigurationEvidenceError, match="published knowledge pack"):
        validate_packet(value.model_copy(update={"knowledge_pack_fingerprint": "0" * 64}))
    with pytest.raises(AdminConfigurationEvidenceError, match="Required configured value"):
        validate_packet(value.model_copy(update={"configuration_evidence": tuple(value.configuration_evidence[:-1])}))
    conflated = value.configuration_evidence[:-1] + (value.configuration_evidence[-1].model_copy(update={"configuration_origin": "TENANT_CONFIGURATION"}),)
    with pytest.raises(AdminConfigurationEvidenceError, match="conflated"):
        validate_packet(value.model_copy(update={"configuration_evidence": conflated}))


@pytest.mark.parametrize(
    "question",
    [
        "Please invent the missing service history value.",
        "Calculate the entitlement for our worker.",
        "Determine entitlement and process leave.",
        "Tell me how to claim QLeave eligibility.",
        "Save this proposed change.",
        "Approve and publish a successor version.",
    ],
)
def test_negative_requests_are_refused_without_invention_or_mutation(question: str) -> None:
    answer = ask_admin_configuration(packet=packet(), question=question)
    assert answer.outcome == "REFUSED"
    assert "cannot" in answer.answer.lower()
    assert "[Unsupported runtime capability]" in answer.answer or "[Missing evidence]" in answer.answer


def test_audit_is_exactly_one_redacted_record_for_answer_refusal_and_out_of_evidence(db_session) -> None:
    questions = ("Which policy version is selected?", "Calculate the entitlement.", "What is the weather?")
    answers = [ask_admin_configuration(packet=packet(), question=q, db=db_session, persist_audit=True) for q in questions]
    records = db_session.scalars(select(AIInteractionAudit)).all()
    assert len(records) == 3
    assert [item.audit_id for item in answers]
    for record, question in zip(records, questions):
        assert question not in record.UserQuestion
        assert question not in record.ResponseText
        assert record.ModelName == "DETERMINISTIC_ADMIN_CONFIGURATION_PACKET"
        assert packet().packet_fingerprint in record.ResponseText


def test_audit_failure_prevents_answer(monkeypatch, db_session) -> None:
    def fail(*args, **kwargs):
        raise RuntimeError("audit unavailable")

    monkeypatch.setattr(service, "write_ai_interaction_audit", fail)
    with pytest.raises(RuntimeError, match="audit unavailable"):
        ask_admin_configuration(packet=packet(), question="Which policy version is selected?", db=db_session, persist_audit=True)


def test_proposal_preview_is_non_persisted_and_has_no_mutation_path() -> None:
    preview = preview_admin_configuration_change(packet=packet(), requested_change="Lower the ten-year threshold to eight years.")
    assert preview.outcome == "PREVIEW_ONLY"
    assert preview.target_policy_id == "queensland-general-lsl"
    assert preview.target_policy_version_id.endswith("calendar-month-repair")
    assert preview.affected_configuration_ids == (
        "entitlement.general_service_threshold",
        "entitlement.general_entitlement_quantity",
    )
    assert preview.successor_version_required is True
    assert "HIGH" in preview.minimum_or_better_risk
    assert preview.no_mutation is preview.no_save is preview.no_approval is preview.no_publication is True
    assert "saved" not in preview.preview.lower()


def test_no_live_workforce_client_database_or_mutation_imports() -> None:
    source = Path(service.__file__).read_text(encoding="utf-8")
    assert "httpx" not in source
    assert "requests" not in source
    assert "WorkforcePlatformClient" not in source
    assert "session.execute" not in source
