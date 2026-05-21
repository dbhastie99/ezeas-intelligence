from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAYROLL_KNOWLEDGE_DIR = ROOT / "docs" / "knowledge" / "payroll"
EVALUATION_DIR = (
    ROOT / "docs" / "evaluation" / "admitted_draft_payrun_processing_bridge_v0_1"
)
SOURCE_RESPONSE = (
    PAYROLL_KNOWLEDGE_DIR
    / "admitted_draft_payrun_processing_bridge_v0_1_source_response.md"
)
STRUCTURED_PACK = PAYROLL_KNOWLEDGE_DIR / "admitted_draft_payrun_processing_bridge_v0_1.md"
ANSWER_EVALUATION_BASELINE = EVALUATION_DIR / "ANSWER_EVALUATION_BASELINE.md"
IMPLEMENTATION_STATE = (
    PAYROLL_KNOWLEDGE_DIR
    / "admitted_draft_payrun_processing_bridge_v0_1_implementation_state.md"
)
IMPLEMENTATION_STATE_BASELINE = EVALUATION_DIR / "IMPLEMENTATION_STATE_BASELINE.md"
PROMPT_ARTEFACT = (
    ROOT
    / "docs"
    / "codex_prompts"
    / "2026-05-21_minerva_admitted_draft_payrun_bridge_implementation_state_v01.md"
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _implementation_state() -> str:
    return _read(IMPLEMENTATION_STATE)


def _baseline() -> str:
    return _read(IMPLEMENTATION_STATE_BASELINE)


def test_implementation_state_files_exist():
    assert IMPLEMENTATION_STATE.exists()
    assert IMPLEMENTATION_STATE_BASELINE.exists()
    assert PROMPT_ARTEFACT.exists()


def test_implementation_state_references_workforce_commits():
    content = _implementation_state()

    assert "dde4286" in content
    assert "e8f4f06" in content


def test_implementation_state_captures_implemented_service_foundation():
    content = _implementation_state()

    assert "service foundation is implemented" in content
    assert "AdmittedDraftPayRunProcessingBridgeService" in content
    assert "authorised admission evidence" in content
    assert "active `PayRunActionDecision`" in content


def test_implementation_state_captures_implemented_operator_action_contract():
    content = _implementation_state()

    assert "guarded operator action contract is implemented" in content
    assert "AdmittedDraftPayRunProcessingBridgeOperatorActionService" in content
    assert "preview_admitted_decision" in content
    assert "operator packet" in content


def test_implementation_state_captures_route_and_ui_boundaries():
    content = _implementation_state()

    assert "No route was added." in content
    assert "No UI was added." in content
    assert "No UI mutation button was added." in content
    assert "No route or UI mutation action exists yet." in content


def test_implementation_state_captures_dry_run_and_disabled_execution_boundary():
    content = _implementation_state()

    assert "dry-run preview by default" in content
    assert "Execution is not permitted by default" in content
    assert "EXECUTION_GUARD_REQUIRED" in content
    assert "EXECUTION_DISABLED_FOR_THIS_SLICE" in content
    assert "Execution disabled for this slice" in content


def test_implementation_state_captures_existing_processing_entrypoint():
    content = _implementation_state()

    assert "PayRunProcessingService.process(..., target_contact_id=...)" in content
    assert "existing deterministic processing entrypoint" in content


def test_implementation_state_says_preview_does_not_call_processing():
    content = _implementation_state()

    assert "Preview does not call processing." in content
    assert "Preview does not call `PayRunProcessingService.process`." in content


def test_implementation_state_says_bridge_does_not_create_payrun_targets():
    content = _implementation_state()

    assert "The bridge does not create PayRuns." in content
    assert "The bridge does not create PayRunContacts." in content
    assert "No PayRun creation by the bridge." in content
    assert "No PayRunContact creation by the bridge." in content


def test_implementation_state_captures_terminal_payrun_protections():
    content = _implementation_state()

    assert "Finalised/frozen/paid/payment-batch/bank-file PayRuns are protected." in content
    assert "terminal, frozen, payment-batch, bank-file, finalised, and paid PayRuns" in content


def test_implementation_state_respects_process_period_lifecycle_status_code():
    content = _implementation_state()

    assert "ProcessPeriod.LifecycleStatusCode" in content
    assert "The bridge respects `ProcessPeriod.LifecycleStatusCode`." in content


def test_implementation_state_includes_prohibited_claims_section():
    content = _implementation_state()

    assert "## Prohibited Current-State Claims" in content
    prohibited = [
        "The bridge is exposed in the UI.",
        "Operators can click a button to process admitted actions.",
        "The bridge route is live.",
        "Automation now processes admitted actions.",
        "Minerva calculates payroll.",
        "Broad runtime execution is enabled.",
    ]

    for claim in prohibited:
        assert claim in content


def test_implementation_state_includes_no_action_attestation():
    content = _implementation_state()

    assert "## No-Action Attestation" in content
    attestations = [
        "No live LLM call happened",
        "No DB connection happened",
        "No workforce-platform edit happened",
        "No route exposure happened",
        "No UI exposure happened",
        "No runtime execution happened",
        "No payroll calculation happened",
        "No payment, finalisation, payment batch, or banking happened",
    ]

    for attestation in attestations:
        assert attestation in content


def test_implementation_state_baseline_links_to_required_sources():
    content = _baseline()

    assert str(SOURCE_RESPONSE.relative_to(ROOT)).replace("\\", "/") in content
    assert str(STRUCTURED_PACK.relative_to(ROOT)).replace("\\", "/") in content
    assert str(ANSWER_EVALUATION_BASELINE.relative_to(ROOT)).replace("\\", "/") in content


def test_implementation_state_baseline_captures_current_answer_posture():
    content = _baseline()

    assert "service foundation is implemented" in content
    assert "guarded operator action contract is implemented" in content
    assert "dry-run preview/operator packet" in content
    assert "Execution disabled for this slice" in content
    assert "No route was added" in content
    assert "No UI mutation button was added" in content


def test_prompt_artefact_exists_and_preserves_slice_boundary():
    content = _read(PROMPT_ARTEFACT)

    assert "Admitted Draft PayRun Bridge Implementation State v0.1" in content
    assert "dde4286" in content
    assert "e8f4f06" in content
    assert "no live LLM call" in content
    assert "no database connection" in content
    assert "no workforce-platform edit" in content
    assert "Do not commit." in content


def test_implementation_state_documents_have_no_mojibake_markers():
    combined = "\n".join(
        [
            _implementation_state(),
            _baseline(),
            _read(PROMPT_ARTEFACT),
        ]
    )
    mojibake_markers = ["â†’", "â€”", "�"]

    for marker in mojibake_markers:
        assert marker not in combined
