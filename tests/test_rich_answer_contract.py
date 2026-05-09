import json
import sys

from app.services.answer_mode_service import AnswerMode, RichAnswerPlan, classify_answer_mode
from app.services.golden_question_service import load_golden_manifest, run_golden_questions
from app.services.ingestion_service import ingest_file_bytes
from scripts import run_golden_questions as run_golden_questions_script


def _manifest(tmp_path, questions):
    path = tmp_path / "rich.json"
    path.write_text(
        json.dumps(
            {
                "name": "Rich answer fixture",
                "description": "Fixture manifest",
                "questions": questions,
            }
        ),
        encoding="utf-8",
    )
    return path


def _ingest(db_session, text: str, title: str = "Developer Log - Annual Leave"):
    document, duplicate = ingest_file_bytes(
        db=db_session,
        content=text.encode("utf-8"),
        original_file_name="annual-leave.txt",
        source_type="DEVELOPER_LOG",
        capability_status="IMPLEMENTED",
        title=title,
    )
    assert duplicate is False
    return document


def _ingest_worker_story_benchmark_evidence(db_session):
    evidence = [
        (
            "Worker Story and Worker Calculation Story are the Talking Payslip for worker evidence and explain payroll "
            "outcomes.",
            "Developer Log - Worker Story Purpose",
        ),
        (
            "Worker Story uses SourceTruth and source truth inclusion to show which source truth inputs are included for "
            "a worker in PayRun evidence.",
            "Developer Log - Worker Story SourceTruth",
        ),
        (
            "Interpreted Worked Hours are shown from the current-effective interpreter run with ObjectTime grouping.",
            "Developer Log - Worker Story Interpreted Worked Hours",
        ),
        (
            "Calculated Payroll Outcome shows the current-effective payroll output from PayRun calculation evidence, "
            "including quantity, rate, amount and line proof.",
            "Developer Log - Worker Story Calculated Payroll Outcome",
        ),
        (
            "Decision Story explains why a treatment or line exists. Rate Story explains rate source and rate amount. "
            "DecisionEvidenceIndex and RateSourceEvidenceIndex provide award decision evidence and rate evidence.",
            "Developer Log - Worker Story Decision Rate Evidence",
        ),
        (
            "Worker Story includes Leave and Accrual Outcome evidence using server-owned leave output and ledger evidence.",
            "Developer Log - Worker Story Leave Accrual",
        ),
        (
            "Worker Story includes Payroll Bases & Totals evidence with payroll bases and totals.",
            "Developer Log - Worker Story Payroll Bases Totals",
        ),
        (
            "Movement Review and PayRun Admin Queue evidence explain operator action, review context, evidence and "
            "return context for the reusable Worker Story platform evidence surface.",
            "Developer Log - Worker Story Movement Review",
        ),
        (
            "Worker Story uses current-effective truth from current-effective payroll output and current-effective "
            "interpreter run, with Correction Audit Story where corrections exist.",
            "Developer Log - Worker Story Current Effective Truth",
        ),
        (
            "Worker Story outstanding hardening records limitations, shared Worker Story surface/component work, explicit "
            "break-treatment proof and future reusable story surfaces for evidence explanation.",
            "Developer Log - Worker Story Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def test_answer_mode_classification_examples():
    assert classify_answer_mode("What is Minerva not allowed to do?") == AnswerMode.DOCTRINE.value
    assert classify_answer_mode("How is Annual Leave managed in the system?") == AnswerMode.PRODUCT_DOMAIN.value
    assert classify_answer_mode("Estimate my leave balance") == AnswerMode.WORKER_FACING.value
    assert classify_answer_mode("Why is worker leave balance wrong?") == AnswerMode.TECHNICAL_SUPPORT.value
    assert classify_answer_mode("Which hardening item explains this?") == AnswerMode.DEVELOPER_PLATFORM.value


def test_rich_answer_plan_is_lightweight_internal_structure():
    plan = RichAnswerPlan(
        answer_mode=AnswerMode.PRODUCT_DOMAIN.value,
        direct_summary="Annual Leave is managed through formal leave services.",
        system_operation_points=["LeaveLedger records accrual and TAKEN rows."],
    )

    assert plan.model_dump()["answer_mode"] == "PRODUCT_DOMAIN"
    assert plan.model_dump()["system_operation_points"] == ["LeaveLedger records accrual and TAKEN rows."]


def test_golden_evaluator_checks_required_answer_sections(db_session, tmp_path):
    _ingest(
        db_session,
        "Annual Leave management uses LeaveType and LeaveTypeRule. LeaveLedger records accrual and TAKEN rows. "
        "PayRun processing includes public holiday valuation evidence and Worker Story output. "
        "The Developer Log also records outstanding hardening for valuation.",
    )
    manifest_path = _manifest(
        tmp_path,
        [
            {
                "id": "rich-sections",
                "question": "How is Annual Leave managed in the system?",
                "answer_mode": "PRODUCT_DOMAIN",
                "expected_source_types": ["DEVELOPER_LOG"],
                "required_answer_sections": [
                    "Direct summary",
                    "How the system works",
                    "Current implementation status",
                    "What remains outstanding",
                ],
                "expected_answer_terms_all": ["LeaveType", "LeaveLedger", "PayRun"],
            }
        ],
    )

    result = run_golden_questions(db_session, manifest_path)

    assert result["all_passed"] is True
    assert result["results"][0]["checks"]["answer_mode"] is True
    assert result["results"][0]["checks"]["required_answer_sections"] is True


def test_golden_evaluator_fails_when_required_answer_section_missing(db_session, tmp_path):
    _ingest(db_session, "General evidence about Annual Leave and LeaveLedger.")
    manifest_path = _manifest(
        tmp_path,
        [
            {
                "id": "missing-section",
                "question": "How is Annual Leave managed in the system?",
                "answer_mode": "PRODUCT_DOMAIN",
                "expected_source_types": ["DEVELOPER_LOG"],
                "required_answer_sections": ["Direct summary", "Intentionally Missing Section"],
            }
        ],
    )

    result = run_golden_questions(db_session, manifest_path)

    assert result["all_passed"] is False
    assert result["results"][0]["checks"]["required_answer_sections"] is False


def test_golden_evaluator_fails_when_forbidden_answer_pattern_matches(db_session, tmp_path):
    _ingest(
        db_session,
        "Annual Leave management uses LeaveType and LeaveTypeRule. LeaveLedger records accrual and TAKEN rows. "
        "PayRun public holiday valuation evidence is shown in Worker Story.",
    )
    manifest_path = _manifest(
        tmp_path,
        [
            {
                "id": "forbidden-pattern",
                "question": "How is Annual Leave managed in the system?",
                "answer_mode": "PRODUCT_DOMAIN",
                "expected_source_types": ["DEVELOPER_LOG"],
                "forbidden_answer_patterns_any": ["Direct\\s+summary"],
            }
        ],
    )

    result = run_golden_questions(db_session, manifest_path)

    assert result["all_passed"] is False
    assert result["results"][0]["checks"]["forbidden_answer_patterns_any"] is False


def test_rich_answer_benchmark_manifest_loads_and_can_be_evaluated(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.annual_leave.json")

    assert manifest["name"] == "Annual Leave rich-answer benchmark"
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.annual_leave.json")
    assert result["total"] == 1
    assert result["results"][0]["checks"]["answer_mode"] is True


def test_worker_story_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.worker_story.json")

    assert manifest["name"] == "Worker Story rich-answer benchmark"
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.worker_story.json")
    assert result["total"] == 5
    assert result["results"][0]["checks"]["answer_mode"] is True


def test_worker_story_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_worker_story_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.worker_story.json")

    assert result["name"] == "Worker Story rich-answer benchmark"
    assert result["total"] == 5
    assert result["all_passed"] is True
    assert {item["id"] for item in result["results"]} >= {
        "worker-story-evidence-rich-answer",
        "worker-story-source-truth",
        "worker-story-calculated-payroll-outcome",
        "worker-story-decision-vs-rate-story",
        "worker-story-movement-review-admin-queue",
    }


def test_golden_runner_script_reports_worker_story_benchmark_summary(db_session, tmp_path, monkeypatch, capsys):
    _ingest_worker_story_benchmark_evidence(db_session)
    output_path = tmp_path / "worker-story-results.json"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_golden_questions.py",
            "--manifest",
            "samples/eval/rich_answer_benchmark.worker_story.json",
            "--verbose",
            "--json-output",
            str(output_path),
        ],
    )

    exit_code = run_golden_questions_script.main()
    captured = capsys.readouterr()
    result = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert "Golden questions: Worker Story rich-answer benchmark" in captured.out
    assert "Total: 5  Passed: 5  Failed: 0" in captured.out
    assert "[PASS] worker-story-source-truth" in captured.out
    assert result["all_passed"] is True
    assert result["total"] == 5


def test_golden_runner_script_reports_annual_leave_benchmark_summary(db_session, tmp_path, monkeypatch, capsys):
    _ingest(
        db_session,
        "Annual Leave configuration uses LeaveType and LeaveTypeRule. LeaveTypeKind and Rule Cockpit organise "
        "Accrual Payment Governance settings.",
        title="Developer Log - Annual Leave Configuration",
    )
    _ingest(
        db_session,
        "Annual Leave accrual posts LeaveLedger minutes using interpreter truth with no fallback during PayRun.",
        title="Developer Log - Annual Leave Accrual",
    )
    _ingest(
        db_session,
        "Annual Leave TAKEN consumption posts LeaveLedger minutes. Public holiday treatment uses "
        "DeductsOnPublicHoliday with resolver skip behaviour.",
        title="Developer Log - Annual Leave TAKEN",
    )
    _ingest(
        db_session,
        "Annual Leave valuation uses valuation basis, ordinary rate, PayRun snapshot and liability evidence.",
        title="Developer Log - Annual Leave Valuation",
    )
    _ingest(
        db_session,
        "PayRun processing includes Generate Leave Accruals on Process, leave accruals, valuation basis and Admin Queue.",
        title="Developer Log - PayRun Leave Orchestration",
    )
    _ingest(
        db_session,
        "Worker Story includes Leave and Accrual Outcome as server-owned leave output with ledger, valuation basis "
        "and evidence chain.",
        title="Developer Log - Worker Story Leave Evidence",
    )
    _ingest(
        db_session,
        "Annual Leave outstanding hardening includes Leave Source Model, FIFO lot consumption, revaluation and "
        "production hardening.",
        title="Developer Log - Annual Leave Outstanding",
    )
    output_path = tmp_path / "annual-leave-results.json"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_golden_questions.py",
            "--manifest",
            "samples/eval/rich_answer_benchmark.annual_leave.json",
            "--json-output",
            str(output_path),
        ],
    )

    exit_code = run_golden_questions_script.main()
    captured = capsys.readouterr()
    result = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert "Golden questions: Annual Leave rich-answer benchmark" in captured.out
    assert "Total: 1  Passed: 1  Failed: 0" in captured.out
    assert result["all_passed"] is True


def test_golden_runner_script_invalid_manifest_fails_clearly(tmp_path, monkeypatch, capsys):
    invalid_path = tmp_path / "invalid.json"
    invalid_path.write_text("{not valid json", encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        ["run_golden_questions.py", "--manifest", str(invalid_path)],
    )

    exit_code = run_golden_questions_script.main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Golden question evaluation failed" in captured.out
    assert "not valid JSON" in captured.out


def test_run_golden_questions_allow_failures_returns_zero(db_session, tmp_path, monkeypatch):
    manifest_path = _manifest(
        tmp_path,
        [
            {
                "id": "allowed-failure",
                "question": "How is Annual Leave managed in the system?",
                "answer_mode": "PRODUCT_DOMAIN",
                "required_answer_sections": ["Missing Section"],
            }
        ],
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["run_golden_questions.py", "--manifest", str(manifest_path), "--allow-failures"],
    )

    assert run_golden_questions_script.main() == 0
