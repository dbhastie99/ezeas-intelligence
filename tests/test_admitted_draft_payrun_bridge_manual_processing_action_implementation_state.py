from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAYROLL_KNOWLEDGE_DIR = ROOT / "docs" / "knowledge" / "payroll"
EVALUATION_DIR = (
    ROOT
    / "docs"
    / "evaluation"
    / "admitted_draft_payrun_bridge_manual_processing_action_v0_1"
)
IMPLEMENTATION_STATE = (
    PAYROLL_KNOWLEDGE_DIR
    / "admitted_draft_payrun_bridge_manual_processing_action_v0_1_implementation_state.md"
)
IMPLEMENTATION_STATE_BASELINE = EVALUATION_DIR / "IMPLEMENTATION_STATE_BASELINE.md"
PROMPT_ARTEFACT = (
    ROOT
    / "docs"
    / "codex_prompts"
    / "2026-05-21_minerva_admitted_draft_payrun_bridge_manual_processing_action_implementation_state_v01.md"
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _implementation_state() -> str:
    return _read(IMPLEMENTATION_STATE)


def _baseline() -> str:
    return _read(IMPLEMENTATION_STATE_BASELINE)


def _combined() -> str:
    return "\n".join(
        [
            _implementation_state(),
            _baseline(),
            _read(PROMPT_ARTEFACT),
        ]
    )


def test_required_implementation_state_files_exist():
    assert IMPLEMENTATION_STATE.exists()
    assert IMPLEMENTATION_STATE_BASELINE.exists()
    assert PROMPT_ARTEFACT.exists()


def test_document_captures_endpoint_path_and_manual_guarding():
    content = _implementation_state()

    assert (
        "POST /api/v1/pay-runs/{id}/pay-process/admitted-draft-actions/process"
        in content
    )
    assert "guarded manual action" in content
    assert "not automation" in content
    assert "not process-all" in content


def test_document_captures_authority_and_preflight_requirements():
    content = _implementation_state()

    required = [
        "active non-stale `PayRunActionDecision`",
        "accepted/authorised admission evidence",
        "existing `PayRunContact`",
        "safe `ProcessPeriod.LifecycleStatusCode`",
        "deterministic processing entrypoint",
        "idempotency basis",
    ]

    for phrase in required:
        assert phrase in content


def test_document_captures_execution_path():
    content = _implementation_state()

    assert "AdmittedDraftPayRunProcessingBridgeService" in content
    assert "PayRunProcessingService.process(..., target_contact_id=...)" in content


def test_document_captures_ui_wiring():
    content = _implementation_state()

    assert "PayRun Detail" in content
    assert "Admin Queue" in content
    assert "UI wires and enables the action only when the backend marks it eligible" in content
    assert "backend status and blockers" in content


def test_document_captures_readiness_and_deferred_items():
    content = _implementation_state()

    assert "READINESS_UPDATE_PENDING" in content
    assert "dedicated readiness refresh adapter" in content
    assert "durable persisted admission lookup" in content


def test_document_lists_required_non_goals():
    content = _implementation_state()

    required = [
        "no finalisation",
        "no payment",
        "no bank file",
        "no `PayRun` creation",
        "no `PayRunContact` creation",
        "no Minerva calculation",
    ]

    for phrase in required:
        assert phrase in content


def test_baseline_contains_prohibited_current_state_claims():
    content = _baseline()

    assert "## Prohibited Current-State Claims" in content
    prohibited_claims = [
        "automation is implemented",
        "process-all is implemented",
        "finalisation is implemented",
        "payment is implemented",
        "bank file generation is implemented",
        "the bridge creates PayRuns",
        "the bridge creates PayRunContacts",
        "Minerva calculates payroll",
    ]

    for claim in prohibited_claims:
        assert claim in content


def test_baseline_contains_no_action_no_runtime_attestation():
    content = _baseline()

    assert "## No-Action/No-Runtime Attestation" in content
    attestations = [
        "No retrieval-plan change",
        "No runtime retrieval change",
        "No database access",
        "No live LLM call",
        "No Workforce Platform change",
        "No runtime execution",
        "No corpus/runtime state mutation",
    ]

    for attestation in attestations:
        assert attestation in content


def test_mojibake_markers_are_absent_from_implementation_state_documents():
    content = _combined()
    mojibake_markers = ["\u00e2\u2020\u2019", "\u00e2\u20ac\u201d", "\ufffd"]

    for marker in mojibake_markers:
        assert marker not in content
