import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DESIGN_DOC = ROOT / "docs/diagnostics/workforce_ask_minerva_panel_integration_design_v0_1.md"
CONTROL_JSON = ROOT / "docs/diagnostics/workforce_ask_minerva_panel_integration_design_v0_1.json"
KNOWLEDGE_DOC = ROOT / "docs/knowledge/workforce_ask_minerva_panel_integration_v0_1.md"
EVAL_BASELINE = (
    ROOT
    / "docs/evaluation/workforce_ask_minerva_panel_integration_v0_1/ANSWER_EVALUATION_BASELINE.md"
)
PROMPT_ARTEFACT = (
    ROOT / "docs/codex_prompts/2026-05-22_workforce_ask_minerva_panel_integration_design_v01.md"
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_required_design_artifacts_exist() -> None:
    assert DESIGN_DOC.exists()
    assert CONTROL_JSON.exists()
    assert KNOWLEDGE_DOC.exists()
    assert EVAL_BASELINE.exists()
    assert PROMPT_ARTEFACT.exists()


def test_design_recommends_admin_queue_first_surface() -> None:
    design = _read(DESIGN_DOC)
    control = json.loads(_read(CONTROL_JSON))

    assert "Recommended initial surface: **PayRun Admin Queue**" in design
    assert control["recommendedInitialSurface"]["surface"] == "PAYRUN_ADMIN_QUEUE"


def test_design_defines_request_contract_and_panel_response_consumption() -> None:
    design = _read(DESIGN_DOC)
    control = json.loads(_read(CONTROL_JSON))

    for field in [
        "Question",
        "Role",
        "SourceScopes",
        "SurfaceContext",
        "DomainTags",
        "FixtureKey",
        "CandidateEvidence",
        "ClaimToValidate",
        "IncludeDeterministicDraft",
        "IncludePanelResponse",
        "AllowLiveLlm",
        "AllowFinalAnswerGeneration",
        "PanelMode",
        "IncludeTechnicalDetails",
    ]:
        assert field in design
        assert field in control["requestContract"]["fields"]

    for field in [
        "Headline",
        "Summary",
        "DraftText",
        "EvidenceChips",
        "CaveatBanners",
        "BoundaryBanners",
        "RoleRestrictionNotice",
        "RuntimeEvidenceNotice",
        "SuggestedNextStep",
        "TechnicalDetails",
        "NoActionAttestation",
    ]:
        assert field in design
        assert field in control["responseFieldsForPanel"]

    assert "The UI should not parse the entire orchestrator envelope directly for primary display." in design


def test_design_includes_role_mappings_and_source_scopes() -> None:
    design = _read(DESIGN_DOC)
    control = json.loads(_read(CONTROL_JSON))

    for role in [
        "DEVELOPER",
        "PAYROLL_ADMINISTRATOR",
        "PAYROLL_MANAGER",
        "PAYROLL_USER",
        "CUSTOMER_ADMINISTRATOR",
        "WORKER",
    ]:
        assert role in design

    assert control["roleMappings"]["developerOrPlatformAdmin"] == "DEVELOPER"
    assert control["roleMappings"]["payrollAdministrator"] == "PAYROLL_ADMINISTRATOR"
    assert control["roleMappings"]["payrollManager"] == "PAYROLL_MANAGER"
    assert control["roleMappings"]["payrollUser"] == "PAYROLL_USER"
    assert control["roleMappings"]["customerAdministrator"] == "CUSTOMER_ADMINISTRATOR"
    assert control["roleMappings"]["worker"] == "WORKER"

    for scope in [
        "PLATFORM_KNOWLEDGE",
        "IMPLEMENTATION_STATE",
        "CODE_EVIDENCE",
        "TEST_EVIDENCE",
        "PROMPT_ARTEFACTS",
        "EVALUATION_BASELINES",
        "RUNTIME_OBJECT_EVIDENCE",
    ]:
        assert scope in design


def test_fixture_and_runtime_boundaries_are_explicit() -> None:
    design = _read(DESIGN_DOC)
    knowledge = _read(KNOWLEDGE_DOC)
    control = json.loads(_read(CONTROL_JSON))

    assert "Fixture evidence is synthetic/internal." in design
    assert "Fixture evidence is synthetic/internal." in knowledge
    assert control["fixtureMode"]["fixtureEvidenceIsSyntheticInternal"] is True
    assert control["fixtureMode"]["fixtureEvidenceIsRuntimeEvidence"] is False

    assert "Minerva must not fetch it in v0.1" in design
    assert "In v0.1, Minerva does not fetch runtime object evidence." in knowledge
    assert control["safetyBoundaries"]["runtimeObjectEvidenceFetchedByMinervaV0"] is False


def test_payroll_execution_and_calculation_are_blocked() -> None:
    design = _read(DESIGN_DOC)
    knowledge = _read(KNOWLEDGE_DOC)
    control = json.loads(_read(CONTROL_JSON))

    assert "It cannot authorise payroll action, execute treatment decisions, calculate payroll" in design
    assert "Minerva cannot execute payroll actions" in knowledge
    assert "Minerva cannot calculate payroll" in knowledge
    assert control["safetyBoundaries"]["payrollCalculationEnabled"] is False
    assert control["safetyBoundaries"]["writeActionsEnabled"] is False
    assert control["safetyBoundaries"]["treatmentDecisioningByMinervaEnabled"] is False


def test_recommended_next_slices_are_present() -> None:
    design = _read(DESIGN_DOC)
    control = json.loads(_read(CONTROL_JSON))

    expected = [
        "Workforce Ask Minerva Panel Shell v0.1",
        "Workforce Ask Minerva Surface Context Packet v0.1",
        "Workforce Runtime Evidence Packet for Admin Queue v0.1",
        "Minerva Runtime Evidence Answer Support v0.1",
        "Live LLM / richer answer generation later, only after gates",
    ]
    for item in expected:
        assert item in design
        assert item in control["recommendedNextSlices"]


def test_evaluation_baseline_contains_all_golden_questions_and_prohibited_claims() -> None:
    baseline = _read(EVAL_BASELINE)

    questions = [
        "Where should the first Workforce Ask Minerva panel appear?",
        "Why is Admin Queue the first recommended surface?",
        "What can Minerva answer in the Admin Queue panel v0.1?",
        "What can Minerva not answer without runtime evidence?",
        "What should Workforce send in the chat request?",
        "What is FixtureKey mode?",
        "Why is fixture evidence not production/runtime evidence?",
        "How should role mapping work?",
        "Can payroll users see code evidence?",
        "What should the panel display from PanelResponse?",
        "Can Minerva execute treatment decisions?",
        "Can Minerva calculate payroll?",
        "What is the runtime evidence gap?",
        "What is the recommended implementation sequence after this design?",
    ]
    for question in questions:
        assert question in baseline

    prohibited_claims = [
        "Minerva can execute payroll actions.",
        "Minerva can calculate payroll in the panel.",
        "Fixture evidence proves live runtime state.",
        "Code evidence proves customer availability.",
        "Payroll users can see raw code evidence by default.",
        "Workforce should expose raw orchestrator internals as the UI.",
        "Live LLM is enabled.",
        "Runtime object evidence is fetched by Minerva in v0.1.",
    ]
    for claim in prohibited_claims:
        assert claim in baseline


def test_no_production_runtime_api_ui_files_are_modified() -> None:
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    changed_paths = []
    for line in result.stdout.splitlines():
        if not line.strip() or line.startswith("warning:"):
            continue
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1].strip()
        changed_paths.append(path.replace("\\", "/"))

    blocked_prefixes = (
        "app/",
        "workforce_platform/",
        "workforce-platform/",
        "frontend/",
        "migrations/",
        "alembic/",
    )
    offenders = [path for path in changed_paths if path.startswith(blocked_prefixes)]
    assert offenders == []


def test_mojibake_markers_are_absent_from_new_artifacts() -> None:
    markers = ["â†’", "â€”", "�"]
    for path in [DESIGN_DOC, CONTROL_JSON, KNOWLEDGE_DOC, EVAL_BASELINE, PROMPT_ARTEFACT]:
        text = _read(path)
        for marker in markers:
            assert marker not in text
