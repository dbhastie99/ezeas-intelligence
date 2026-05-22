import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


HARNESS_NAME = "Internal Chat Endpoint Smoke Harness"
HARNESS_VERSION = "MINERVA_INTERNAL_CHAT_ENDPOINT_SMOKE_HARNESS_V0_1"
INTERNAL_ROUTE = "/api/v1/internal/minerva/chat/stub"


@dataclass(frozen=True)
class SmokeCase:
    name: str
    question: str
    role: str
    fixture_key: str
    source_scopes: list[str] = field(default_factory=list)
    expected_rejection: bool = False

    def request_payload(self) -> dict[str, Any]:
        return {
            "Question": self.question,
            "Role": self.role,
            "FixtureKey": self.fixture_key,
            "SourceScopes": list(self.source_scopes),
            "IncludeDeterministicDraft": True,
            "AllowLiveLlm": False,
            "AllowFinalAnswerGeneration": False,
        }


SMOKE_CASES = [
    SmokeCase(
        name="developer admitted draft manual processing",
        question="What evidence supports manual admitted draft action processing?",
        role="DEVELOPER",
        fixture_key="ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED",
    ),
    SmokeCase(
        name="payroll administrator asphalt safe classRates",
        question="Is the Asphalt safe classRates seeding aligned now?",
        role="PAYROLL_ADMINISTRATOR",
        fixture_key="ASPHALT_SAFE_CLASSRATES_SEEDED_WITH_GATES",
    ),
    SmokeCase(
        name="payroll user post-finalisation ObjectTime",
        question="What should I do with this post-finalisation ObjectTime action?",
        role="PAYROLL_USER",
        fixture_key="POST_FINALISATION_OBJECTTIME_ACTION_SURFACED",
    ),
    SmokeCase(
        name="customer administrator code evidence runtime caveat",
        question="Is this implementation enabled for my tenant in production?",
        role="CUSTOMER_ADMINISTRATOR",
        fixture_key="CODE_EVIDENCE_CANNOT_PROVE_RUNTIME",
    ),
    SmokeCase(
        name="worker code evidence runtime caveat",
        question="What does code evidence confirm, and what does it not confirm?",
        role="WORKER",
        fixture_key="CODE_EVIDENCE_CANNOT_PROVE_RUNTIME",
    ),
    SmokeCase(
        name="analytics user analytics deferred",
        question="Explain this payroll trend chart.",
        role="ANALYTICS_USER",
        fixture_key="ANALYTICS_EVIDENCE_DEFERRED",
        source_scopes=["ANALYTICS_EVIDENCE"],
    ),
    SmokeCase(
        name="payroll manager runtime object evidence required",
        question="Why did this worker get overtime?",
        role="PAYROLL_MANAGER",
        fixture_key="RUNTIME_OBJECT_EVIDENCE_REQUIRED",
        source_scopes=["RUNTIME_OBJECT_EVIDENCE"],
    ),
    SmokeCase(
        name="invalid fixture key",
        question="Can the platform manually process an admitted draft action?",
        role="PAYROLL_ADMINISTRATOR",
        fixture_key="NOT_A_FIXTURE",
        expected_rejection=True,
    ),
]


def run_smoke_harness(mode: str = "service") -> dict[str, Any]:
    if mode not in {"service", "route"}:
        raise ValueError("mode must be 'service' or 'route'")

    cases = [_run_case(case, mode=mode) for case in SMOKE_CASES]
    passed = all(case["Pass"] for case in cases)
    return {
        "HarnessName": HARNESS_NAME,
        "Version": HARNESS_VERSION,
        "Mode": mode,
        "RoutePath": INTERNAL_ROUTE if mode == "route" else None,
        "CaseCount": len(cases),
        "Pass": passed,
        "FailureCount": sum(1 for case in cases if not case["Pass"]),
        "BoundaryAssertions": {
            "LiveLlmUsed": False,
            "FinalAnswerGenerationPermitted": False,
            "IsFinalAnswer": False,
            "RuntimeEvidenceFixtureOrSyntheticOnly": True,
            "DatabaseAccessed": False,
            "WriteActionPerformed": False,
            "ExternalApiCalled": False,
        },
        "Cases": cases,
    }


def _run_case(case: SmokeCase, *, mode: str) -> dict[str, Any]:
    try:
        response = _call_stub(case.request_payload(), mode=mode)
        checks = _evaluate_case(case, response)
        request_status = "EXPECTED_REJECTION" if case.expected_rejection else "REQUEST_ACCEPTED"
        return _case_result(case, response, checks, request_status=request_status)
    except Exception as exc:
        failure = f"{type(exc).__name__}: {exc}"
        if case.expected_rejection:
            failure = f"unexpected exception shape for expected rejection: {failure}"
        return _exception_case_result(case, failure)


def _call_stub(payload: dict[str, Any], *, mode: str) -> dict[str, Any]:
    if mode == "service":
        from app.services.internal_chat_api_stub_service import InternalChatApiStubService

        return InternalChatApiStubService().build_response(payload).model_dump()

    from fastapi.testclient import TestClient

    from app.main import app

    response = TestClient(app).post(INTERNAL_ROUTE, json=payload)
    try:
        body = response.json()
    except json.JSONDecodeError:
        body = {"Status": "HTTP_RESPONSE_NOT_JSON", "Detail": response.text}
    if response.status_code >= 400:
        body.setdefault("Status", f"HTTP_{response.status_code}")
        body["HttpStatusCode"] = response.status_code
    return body


def _evaluate_case(case: SmokeCase, response: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    status = response.get("Status")
    fixture = response.get("FixtureEvidence") or {}
    draft = response.get("DeterministicDraft")
    attestation = response.get("NoActionAttestation") or {}
    packet = response.get("EvidenceSupportPacket") or {}
    envelope = response.get("OrchestratorEnvelope") or {}
    diagnostics = response.get("Diagnostics") or {}
    dumped = json.dumps(response, sort_keys=True)

    if case.expected_rejection:
        _expect(status == "INVALID_FIXTURE_KEY", "invalid fixture key was not rejected", failures)
        _expect(response.get("AnswerPermitted") is False, "invalid fixture answer was permitted", failures)
        _expect(draft is None, "invalid fixture returned a deterministic draft", failures)
        _expect(fixture.get("FixtureEvidenceUsed") is False, "invalid fixture used fixture evidence", failures)
        _expect(
            fixture.get("FixtureEvidenceStatus") == "INVALID_FIXTURE_KEY",
            "invalid fixture status was not deterministic",
            failures,
        )
    else:
        _expect(status == "STUB_RESPONSE_BUILT", "valid fixture did not build a stub response", failures)
        _expect(draft is not None, "deterministic draft was not returned", failures)
        _expect(fixture.get("FixtureEvidenceUsed") is True, "fixture evidence was not used", failures)
        _expect(fixture.get("FixtureEvidenceSynthetic") is True, "fixture evidence was not synthetic", failures)

    _expect(response.get("LiveLlmUsed") is False, "live LLM was used", failures)
    _expect(response.get("IsFinalAnswer") is False, "response was marked final", failures)
    _expect(
        response.get("FinalAnswerGenerationPermitted") is False,
        "final answer generation was permitted",
        failures,
    )
    _expect(attestation, "no-action attestation missing", failures)
    for key in [
        "LiveLlmCalled",
        "DatabaseAccessed",
        "ExternalApiCalled",
        "WriteActionPerformed",
        "RuntimeObjectEvidenceFetched",
        "FinalAnswerGenerated",
    ]:
        _expect(attestation.get(key) is False, f"no-action attestation {key} was not false", failures)

    _expect(
        diagnostics.get("RuntimeObjectEvidenceFetched") is False,
        "diagnostics indicate runtime evidence was fetched",
        failures,
    )
    _expect(
        diagnostics.get("WriteActionPerformed") is False,
        "diagnostics indicate a write action was performed",
        failures,
    )

    if case.name == "payroll user post-finalisation ObjectTime":
        for technical_name in [
            "app/services/post_finalisation_objecttime_action_service.py",
            "PostFinalisationObjectTimeActionService",
            "test_post_finalisation_objecttime_action_keeps_finalised_payrun_protected",
        ]:
            _expect(technical_name not in dumped, f"payroll user exposed {technical_name}", failures)

    if case.name == "worker code evidence runtime caveat":
        _expect(packet.get("code_evidence") == [], "worker received code evidence", failures)
        _expect(packet.get("test_evidence") == [], "worker received test evidence", failures)
        _expect(
            (draft or {}).get("DraftStatus") == "DRAFT_ROLE_RESTRICTED",
            "worker response was not role restricted",
            failures,
        )

    if case.name == "analytics user analytics deferred":
        _expect(
            envelope.get("Status") == "UNSUPPORTED_SCOPE",
            "analytics fixture was not deferred as unsupported scope",
            failures,
        )
        _expect("ANALYTICS_EVIDENCE" in response.get("UnsupportedScopes", []), "analytics scope not listed", failures)
        _expect(
            fixture.get("FixtureEvidenceStatus") == "DEFERRED_INACTIVE",
            "analytics fixture status was not deferred inactive",
            failures,
        )

    if case.name == "payroll manager runtime object evidence required":
        _expect(
            fixture.get("FixtureEvidenceStatus") == "NEEDS_RUNTIME_EVIDENCE",
            "runtime fixture did not require runtime evidence",
            failures,
        )
        _expect(
            (draft or {}).get("DraftStatus") == "DRAFT_RUNTIME_EVIDENCE_REQUIRED",
            "runtime fixture draft did not require runtime evidence",
            failures,
        )
        _expect(
            fixture.get("RuntimeObjectEvidenceFetched") is False,
            "runtime fixture fetched live runtime evidence",
            failures,
        )

    return failures


def _expect(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def _case_result(
    case: SmokeCase,
    response: dict[str, Any],
    failures: list[str],
    *,
    request_status: str,
) -> dict[str, Any]:
    fixture = response.get("FixtureEvidence") or {}
    draft = response.get("DeterministicDraft") or {}
    attestation = response.get("NoActionAttestation") or {}
    caveats = list(response.get("RequiredCaveats") or [])
    passed = not failures
    return {
        "CaseName": case.name,
        "Question": case.question,
        "Role": case.role,
        "FixtureKey": case.fixture_key,
        "RequestStatus": request_status,
        "ResponseStatus": response.get("Status"),
        "OrchestratorStatus": (response.get("OrchestratorEnvelope") or {}).get("Status"),
        "DraftStatus": draft.get("DraftStatus"),
        "IsFinalAnswer": response.get("IsFinalAnswer"),
        "LiveLlmUsed": response.get("LiveLlmUsed"),
        "FinalAnswerGenerationPermitted": response.get("FinalAnswerGenerationPermitted"),
        "FixtureEvidenceUsed": fixture.get("FixtureEvidenceUsed"),
        "FixtureEvidenceSynthetic": fixture.get("FixtureEvidenceSynthetic"),
        "FixtureEvidenceStatus": fixture.get("FixtureEvidenceStatus"),
        "AnswerPermitted": response.get("AnswerPermitted"),
        "RequiredCaveatsCount": len(caveats),
        "RequiredCaveats": caveats,
        "NoActionAttestationSummary": _attestation_summary(attestation),
        "Pass": passed,
        "FailureReason": None if passed else "; ".join(failures),
    }


def _exception_case_result(case: SmokeCase, failure: str) -> dict[str, Any]:
    return {
        "CaseName": case.name,
        "Question": case.question,
        "Role": case.role,
        "FixtureKey": case.fixture_key,
        "RequestStatus": "EXCEPTION",
        "ResponseStatus": None,
        "DraftStatus": None,
        "IsFinalAnswer": None,
        "LiveLlmUsed": None,
        "FinalAnswerGenerationPermitted": None,
        "FixtureEvidenceUsed": None,
        "FixtureEvidenceSynthetic": None,
        "AnswerPermitted": None,
        "RequiredCaveatsCount": 0,
        "RequiredCaveats": [],
        "NoActionAttestationSummary": "missing",
        "Pass": False,
        "FailureReason": failure,
    }


def _attestation_summary(attestation: dict[str, Any]) -> str:
    if not attestation:
        return "missing"
    failed = [key for key, value in attestation.items() if value is not False]
    if failed:
        return "unexpected true flags: " + ", ".join(sorted(failed))
    return "all no-action flags false"


def write_output(report: dict[str, Any], output_path: str | Path | None) -> None:
    if not output_path:
        return
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the internal Minerva chat stub smoke harness.")
    parser.add_argument("--mode", choices=["service", "route"], default="service")
    parser.add_argument("--output", help="Optional path to write the concise JSON smoke result.")
    args = parser.parse_args(argv)

    report = run_smoke_harness(mode=args.mode)
    write_output(report, args.output)
    print(json.dumps(report, indent=2))
    return 0 if report["Pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
