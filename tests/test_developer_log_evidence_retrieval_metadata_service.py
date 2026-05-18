import json
from copy import deepcopy
from pathlib import Path

from app.services.developer_log_durable_evidence_candidate_service import (
    REQUIRED_DEVELOPER_LOG_SECTIONS,
)
from app.services.developer_log_evidence_retrieval_metadata_service import (
    DEVELOPER_LOG_RETRIEVAL_METADATA_READY,
    build_developer_log_evidence_retrieval_metadata,
)
from app.services.durable_evidence_retrieval_readiness_service import (
    build_durable_evidence_retrieval_readiness,
)


FIXTURE_ROOT = Path("tests/fixtures/durable_evidence_intake")


def _json_fixture(name):
    return json.loads((FIXTURE_ROOT / name).read_text(encoding="utf-8"))


def _record(**overrides):
    record = _json_fixture("developer_log_durable_record_envelope_v0_1.json")
    record.update(overrides)
    return record


def _rollback():
    return _json_fixture("developer_log_rollback_metadata_v0_1.json")


def _metadata(record=None):
    record = _record() if record is None else record
    readiness = build_durable_evidence_retrieval_readiness(record, _rollback())
    return build_developer_log_evidence_retrieval_metadata(record, readiness)


def test_retrieval_ready_developer_log_record_produces_metadata_ready():
    result = _metadata()

    assert result["metadata_status"] == DEVELOPER_LOG_RETRIEVAL_METADATA_READY


def test_evidence_type_is_developer_log():
    assert _metadata()["evidence_type"] == "DEVELOPER_LOG"


def test_standard_developer_log_sections_are_retrievable():
    result = _metadata()

    for section in REQUIRED_DEVELOPER_LOG_SECTIONS:
        assert section in result["retrievable_sections"]


def test_source_reference_and_source_status_are_preserved():
    record = _record()
    result = _metadata(record)

    assert result["source_reference"] == record["source_reference"]
    assert result["source_status"] == record["source_status"]


def test_answer_boundaries_distinguish_evidence_decision_and_implementation_status():
    boundaries = " ".join(_metadata()["answer_boundaries"]).lower()

    assert "evidence says" in boundaries
    assert "project decisions" in boundaries
    assert "implementation status remains unknown" in boundaries


def test_prohibited_inferences_include_overstatement_boundaries():
    prohibited = " ".join(_metadata()["prohibited_inferences"]).lower()

    assert "production readiness" in prohibited
    assert "runtime deployment" in prohibited
    assert "db mutation" in prohibited
    assert "corpus mutation" in prohibited
    assert "implementation completion" in prohibited


def test_source_reference_is_required():
    assert _metadata()["citation_required"] is True


def test_output_is_deterministic():
    record = _record()

    assert _metadata(deepcopy(record)) == _metadata(deepcopy(record))
