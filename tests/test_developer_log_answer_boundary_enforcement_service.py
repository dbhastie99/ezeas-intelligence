import json
from copy import deepcopy
from pathlib import Path

from app.services.developer_log_answer_boundary_enforcement_service import (
    DEVELOPER_LOG_ANSWER_BOUNDARY_ENFORCED,
    build_developer_log_answer_boundary_enforcement,
)
from app.services.developer_log_evidence_retrieval_metadata_service import (
    build_developer_log_evidence_retrieval_metadata,
)
from app.services.durable_evidence_retrieval_readiness_service import (
    build_durable_evidence_retrieval_readiness,
)


FIXTURE_ROOT = Path("tests/fixtures/durable_evidence_intake")


def _json_fixture(name):
    return json.loads((FIXTURE_ROOT / name).read_text(encoding="utf-8"))


def _record():
    return _json_fixture("developer_log_durable_record_envelope_v0_1.json")


def _rollback():
    return _json_fixture("developer_log_rollback_metadata_v0_1.json")


def _retrieval_metadata(**overrides):
    record = _record()
    readiness = build_durable_evidence_retrieval_readiness(record, _rollback())
    metadata = build_developer_log_evidence_retrieval_metadata(record, readiness)
    metadata.update(overrides)
    return metadata


def _boundary(metadata=None):
    return build_developer_log_answer_boundary_enforcement(
        _retrieval_metadata() if metadata is None else metadata,
    )


def test_valid_developer_log_retrieval_metadata_enforces_boundaries():
    result = _boundary()

    assert result["boundary_status"] == DEVELOPER_LOG_ANSWER_BOUNDARY_ENFORCED


def test_evidence_boundary_is_enforced():
    assert _boundary()["evidence_boundary_enforced"] is True


def test_implementation_status_boundary_is_enforced():
    assert _boundary()["implementation_status_boundary_enforced"] is True


def test_runtime_status_boundary_is_enforced():
    assert _boundary()["runtime_status_boundary_enforced"] is True


def test_production_status_boundary_is_enforced():
    assert _boundary()["production_status_boundary_enforced"] is True


def test_phrasing_rules_distinguish_evidence_decisions_and_statuses():
    rules = " ".join(_boundary()["required_phrasing_rules"]).lower()

    assert "evidence says" in rules
    assert "project decided" in rules
    assert "implemented" in rules
    assert "verified" in rules
    assert "still to do" in rules


def test_prohibited_inferences_include_required_overstatements():
    prohibited = " ".join(_boundary()["prohibited_inferences"]).lower()

    assert "implementation complete" in prohibited
    assert "runtime enabled" in prohibited
    assert "production-ready" in prohibited
    assert "db or corpus mutated" in prohibited
    assert "user-facing" in prohibited


def test_output_is_deterministic():
    metadata = _retrieval_metadata()

    assert _boundary(deepcopy(metadata)) == _boundary(deepcopy(metadata))
