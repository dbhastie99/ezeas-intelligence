import json
from pathlib import Path

from scripts import smoke_internal_chat_stub as smoke


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_DOC = ROOT / "docs" / "knowledge" / "minerva_internal_chat_endpoint_smoke_harness_v0_1.md"
EVALUATION_DIR = ROOT / "docs" / "evaluation" / "minerva_internal_chat_endpoint_smoke_harness_v0_1"
EVALUATION_BASELINE = EVALUATION_DIR / "SMOKE_HARNESS_BASELINE.md"
SAMPLE_OUTPUT = EVALUATION_DIR / "SMOKE_HARNESS_SAMPLE_OUTPUT.json"
PROMPT_ARTEFACT = (
    ROOT
    / "docs"
    / "codex_prompts"
    / "2026-05-22_minerva_internal_chat_endpoint_smoke_harness_v01.md"
)


def _service_report() -> dict:
    return smoke.run_smoke_harness(mode="service")


def _case(report: dict, name: str) -> dict:
    return next(case for case in report["Cases"] if case["CaseName"] == name)


def test_smoke_script_module_imports():
    assert smoke.HARNESS_VERSION == "MINERVA_INTERNAL_CHAT_ENDPOINT_SMOKE_HARNESS_V0_1"


def test_service_mode_smoke_cases_run_successfully():
    report = _service_report()

    assert report["Mode"] == "service"
    assert report["Pass"] is True
    assert report["FailureCount"] == 0


def test_output_includes_all_required_case_names():
    names = {case["CaseName"] for case in _service_report()["Cases"]}

    assert names == {
        "developer admitted draft manual processing",
        "payroll administrator asphalt safe classRates",
        "payroll user post-finalisation ObjectTime",
        "customer administrator code evidence runtime caveat",
        "worker code evidence runtime caveat",
        "analytics user analytics deferred",
        "payroll manager runtime object evidence required",
        "invalid fixture key",
    }


def test_valid_fixture_cases_mark_fixture_evidence_synthetic_true():
    for case in _service_report()["Cases"]:
        if case["CaseName"] == "invalid fixture key":
            continue
        assert case["FixtureEvidenceUsed"] is True
        assert case["FixtureEvidenceSynthetic"] is True


def test_invalid_fixture_case_rejects_deterministically_but_harness_passes():
    case = _case(_service_report(), "invalid fixture key")

    assert case["Pass"] is True
    assert case["RequestStatus"] == "EXPECTED_REJECTION"
    assert case["ResponseStatus"] == "INVALID_FIXTURE_KEY"
    assert case["AnswerPermitted"] is False
    assert case["FixtureEvidenceUsed"] is False
    assert case["FixtureEvidenceStatus"] == "INVALID_FIXTURE_KEY"


def test_all_cases_have_live_llm_used_false():
    assert all(case["LiveLlmUsed"] is False for case in _service_report()["Cases"])


def test_all_cases_have_is_final_answer_false():
    assert all(case["IsFinalAnswer"] is False for case in _service_report()["Cases"])


def test_all_cases_have_final_answer_generation_permitted_false():
    assert all(
        case["FinalAnswerGenerationPermitted"] is False for case in _service_report()["Cases"]
    )


def test_all_cases_include_no_action_attestation():
    assert all(
        case["NoActionAttestationSummary"] == "all no-action flags false"
        for case in _service_report()["Cases"]
    )


def test_payroll_user_case_does_not_expose_file_function_or_test_names():
    report = _service_report()
    case = _case(report, "payroll user post-finalisation ObjectTime")

    assert case["Pass"] is True
    assert case["FailureReason"] is None


def test_worker_case_is_role_restricted_and_has_no_code_evidence():
    case = _case(_service_report(), "worker code evidence runtime caveat")

    assert case["OrchestratorStatus"] == "ROLE_RESTRICTED"
    assert case["DraftStatus"] == "DRAFT_ROLE_RESTRICTED"
    assert case["Pass"] is True


def test_analytics_case_is_deferred_inactive():
    case = _case(_service_report(), "analytics user analytics deferred")

    assert case["OrchestratorStatus"] == "UNSUPPORTED_SCOPE"
    assert case["DraftStatus"] == "DRAFT_UNSUPPORTED_SCOPE"
    assert case["FixtureEvidenceStatus"] == "DEFERRED_INACTIVE"


def test_runtime_evidence_fixture_case_requires_runtime_evidence():
    case = _case(_service_report(), "payroll manager runtime object evidence required")

    assert case["OrchestratorStatus"] == "UNSUPPORTED_SCOPE"
    assert case["DraftStatus"] == "DRAFT_RUNTIME_EVIDENCE_REQUIRED"
    assert case["FixtureEvidenceStatus"] == "NEEDS_RUNTIME_EVIDENCE"


def test_output_writes_valid_json_to_temp_file(capsys):
    output_path = ROOT / "artifacts" / "test_tmp" / "internal_chat_endpoint_smoke_harness_output.json"

    try:
        exit_code = smoke.main(["--output", str(output_path)])
        captured = capsys.readouterr()
        payload = json.loads(output_path.read_text(encoding="utf-8"))
    finally:
        output_path.unlink(missing_ok=True)

    assert exit_code == 0
    assert payload["Pass"] is True
    assert json.loads(captured.out)["HarnessName"] == smoke.HARNESS_NAME


def test_docs_and_prompt_artefact_exist():
    assert KNOWLEDGE_DOC.exists()
    assert EVALUATION_BASELINE.exists()
    assert PROMPT_ARTEFACT.exists()


def test_sample_output_json_exists_if_created_and_validates():
    assert SAMPLE_OUTPUT.exists()
    payload = json.loads(SAMPLE_OUTPUT.read_text(encoding="utf-8"))

    assert payload["Version"] == smoke.HARNESS_VERSION
    assert payload["Pass"] is True
    assert payload["CaseCount"] == 8


def test_new_artefacts_have_no_mojibake_markers():
    paths = [
        ROOT / "scripts" / "smoke_internal_chat_stub.py",
        KNOWLEDGE_DOC,
        EVALUATION_BASELINE,
        SAMPLE_OUTPUT,
        PROMPT_ARTEFACT,
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths if path.exists())

    for marker in ["â†’", "â€”", "�"]:
        assert marker not in combined
