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


def _ingest_payroll_bases_benchmark_evidence(db_session):
    evidence = [
        (
            "Payroll Bases & Totals are governed payroll basis evidence for operators, not reporting totals. "
            "They explain why payroll bases matter operationally.",
            "Developer Log - Payroll Bases Purpose",
        ),
        (
            "PayrollBucketDefinition and Payroll Bucket Definition evidence define bucket definition, period "
            "definition, calendar policy and membership for payroll basis evidence.",
            "Developer Log - Payroll Bucket Definition",
        ),
        (
            "Payroll Bases & Totals govern worked hours and basis quantity using hours, minutes and quantity evidence.",
            "Developer Log - Payroll Worked Hours Quantity",
        ),
        (
            "Payroll Bases & Totals include gross basis, ordinary basis, superable basis, taxable basis, payroll tax, "
            "WIC and PAYG evidence where formal implementation evidence supports it.",
            "Developer Log - Payroll Basis Types",
        ),
        (
            "Payroll Bases & Totals require current-effective truth, current effective source truth and "
            "current-effective payroll output; stale basis evidence is not safe current truth.",
            "Developer Log - Payroll Current Effective Truth",
        ),
        (
            "PayrollBucketResult and Payroll Bucket Result readiness identifies stale rows and rebuild requirements "
            "before basis evidence is trusted.",
            "Developer Log - Payroll Bucket Result Readiness",
        ),
        (
            "Payroll Bases & Totals connect to Worker Story and Worker Calculation Story as worker evidence in the "
            "platform evidence surface.",
            "Developer Log - Payroll Bases Worker Story",
        ),
        (
            "Payroll Bases & Totals connect to Movement Review and PayRun Admin Queue for operator review of basis "
            "movement evidence.",
            "Developer Log - Payroll Bases Movement Review",
        ),
        (
            "Payroll Bases & Totals outstanding hardening includes limitations, bucket lifecycle, versioning and "
            "future work.",
            "Developer Log - Payroll Bases Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_payrun_admin_queue_benchmark_evidence(db_session):
    evidence = [
        (
            "PayRun Admin Queue is the operator workbench for what needs action now. Command Centre remains the full "
            "evidence and control-room surface, and queue cleanliness is not the same as assurance.",
            "Developer Log - Admin Queue Purpose",
        ),
        (
            "PayRun Admin Queue separates blockers, warnings and ready actions because they have different operational "
            "meaning for operators.",
            "Developer Log - Admin Queue Blockers Warnings Ready",
        ),
        (
            "Worker Attention and dirty contacts belong in the PayRun Admin Queue action workflow for worker attention "
            "and contact changes.",
            "Developer Log - Admin Queue Worker Attention",
        ),
        (
            "PayRun Admin Queue surfaces processing actions and reprocessing actions, but deterministic services remain "
            "payroll calculation truth.",
            "Developer Log - Admin Queue Processing Actions",
        ),
        (
            "Finalisation readiness in PayRun Admin Queue distinguishes blockers and warnings, including amber warnings "
            "that cannot simply be ignored.",
            "Developer Log - Admin Queue Finalisation Readiness",
        ),
        (
            "Assurance Snapshot provides reasonableness, review signals and assurance signals, not hidden calculation "
            "truth; governed assurance thresholds remain hardening.",
            "Developer Log - Admin Queue Assurance Snapshot",
        ),
        (
            "PayRun Admin Queue review surfaces and navigation connect to Worker Story, Payroll Bases & Totals, "
            "Movement Review, PayRun Output and Command Centre.",
            "Developer Log - Admin Queue Review Navigation",
        ),
        (
            "PayRun Admin Queue connects to Worker Story and Worker Calculation Story as worker evidence and review "
            "context.",
            "Developer Log - Admin Queue Worker Story",
        ),
        (
            "PayRun Admin Queue connects to Payroll Bases & Totals payroll bases and basis evidence for operator review.",
            "Developer Log - Admin Queue Payroll Bases",
        ),
        (
            "PayRun Admin Queue connects to Movement Review for operator review and movement evidence.",
            "Developer Log - Admin Queue Movement Review",
        ),
        (
            "PayRun Admin Queue outstanding hardening includes server-owned operation tracker, global queue resolver, "
            "reusable Worker Story surface, governed assurance thresholds and warning acknowledgement.",
            "Developer Log - Admin Queue Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_movement_review_benchmark_evidence(db_session):
    evidence = [
        (
            "Movement Review is a payroll reasonableness review surface for operators to understand changes, variance "
            "and review-worthy movement.",
            "Developer Log - Movement Review Purpose",
        ),
        (
            "Movement Review is reasonableness evidence, not automatic proof that payroll is wrong.",
            "Developer Log - Movement Review Reasonableness",
        ),
        (
            "Movement Review operates across worker lens and organisation lens, including worker-level and "
            "organisation-level movement views.",
            "Developer Log - Movement Review Lenses",
        ),
        (
            "Movement Review variance depends on comparable period and comparable baseline evidence, with "
            "review-worthy items prioritised.",
            "Developer Log - Movement Review Variance",
        ),
        (
            "Movement Review connects to Payroll Bases & Totals payroll bases and basis evidence for movement "
            "explanations.",
            "Developer Log - Movement Review Payroll Bases",
        ),
        (
            "Movement Review connects to Worker Story for worker-level drill-through, worker evidence and explanation.",
            "Developer Log - Movement Review Worker Story",
        ),
        (
            "Movement Review connects to PayRun Admin Queue and Admin Queue review actions for assurance review actions.",
            "Developer Log - Movement Review Admin Queue",
        ),
        (
            "Movement Review depends on current-effective payroll, current-effective truth and bucket source truth; "
            "stale bucket evidence is not safe current truth.",
            "Developer Log - Movement Review Current Effective Truth",
        ),
        (
            "Movement Review trend-only, rolling average and YTD evidence should not be treated like ordinary "
            "current-period blockers unless governed policy says so.",
            "Developer Log - Movement Review Trend Threshold",
        ),
        (
            "Movement Review filters, filtered lenses, return context, all-worker views and audit views support review.",
            "Developer Log - Movement Review Filters",
        ),
        (
            "Movement Review outstanding hardening includes governed Movement Review Policy, thresholds, comparable "
            "period rules, filtered lenses and historical bucket rebuild governance.",
            "Developer Log - Movement Review Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_comparison_remediation_benchmark_evidence(db_session):
    evidence = [
        (
            "Comparison / Remediation is a governed comparison capability, not a simple top-up adjustment.",
            "Developer Log - Comparison Remediation Purpose",
        ),
        (
            "The comparison model has primary calculated, comparator calculated and actual imported actuals lane "
            "evidence.",
            "Developer Log - Comparison Three Lane Model",
        ),
        (
            "ObjectTime to EmployeeAppointment to AwardPositionClass remains the primary award path and operational "
            "payroll truth.",
            "Developer Log - Comparison Primary Award Path",
        ),
        (
            "Imported actuals and the actuals lane are external outcome truth and imported actual payroll truth, not "
            "calculated interpreter truth.",
            "Developer Log - Comparison Imported Actuals",
        ),
        (
            "AwardComparisonPolicy and Award Comparison Policy govern comparator selection, active lanes, grain, "
            "offset policy, review requirements and variance treatment.",
            "Developer Log - Comparison Policy",
        ),
        (
            "PayRunComparisonRun, PayRun Comparison Run, PayRunComparisonLine and PayRun Comparison Line provide "
            "comparison evidence before variance generation.",
            "Developer Log - Comparison Run Line Evidence",
        ),
        (
            "PayRunVarianceLine and PayRun Variance Line variance line evidence supports remediation top-up lines that "
            "must be typed and explainable.",
            "Developer Log - Comparison Variance Governance",
        ),
        (
            "AwardPositionClassComparisonMap, EmployeeAppointmentAwardClassAssignment and "
            "ObjectTimeClassificationResolution are required because comparator classification and classification lens "
            "mapping cannot be guessed.",
            "Developer Log - Comparison Classification Mapping",
        ),
        (
            "Comparison / Remediation should connect to Worker Story through a future comparison chapter and worker "
            "evidence for remediation evidence.",
            "Developer Log - Comparison Worker Story",
        ),
        (
            "Comparison / Remediation should connect to PayRun Admin Queue for missing policy, unmapped actuals and "
            "variance review actions.",
            "Developer Log - Comparison Admin Queue",
        ),
        (
            "Comparison / Remediation should connect to Movement Review for variance and comparison outcomes; variance "
            "is not automatic proof of error.",
            "Developer Log - Comparison Movement Review",
        ),
        (
            "Comparison / Remediation outstanding hardening remains design doctrine and not yet implemented as a full "
            "runtime capability; future work includes comparison policy, comparison run and line models, variance "
            "generation, classification mapping and Worker Story comparison chapter.",
            "Developer Log - Comparison Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_tax_payg_benchmark_evidence(db_session):
    evidence = [
        (
            "Tax / PAYG is governed withholding calculation evidence and tax evidence, not an LLM calculation.",
            "Developer Log - Tax PAYG Purpose",
        ),
        (
            "Tax / PAYG uses deterministic services and tax providers for withholding calculation; Minerva explains "
            "evidence and status.",
            "Developer Log - Tax PAYG Boundary",
        ),
        (
            "TaxStory and Tax Story should explain source truth, worker tax profile, payroll context, rule pack "
            "selection, component selection, frequency conversion, band/formula calculation, rounding, net-pay effect, "
            "unsupported or skipped rules and audit provenance.",
            "Developer Log - TaxStory Explainability",
        ),
        (
            "Taxable basis and taxable earnings must align with Payroll Bases & Totals and governed basis membership, "
            "not raw flags.",
            "Developer Log - Taxable Basis Payroll Bases",
        ),
        (
            "Worker tax declaration, withholding instruction, withholding inputs and tax profile affect calculation "
            "readiness.",
            "Developer Log - Tax Declaration Withholding Inputs",
        ),
        (
            "ProcessPeriod PaymentDate, payment date and process period provide tax context that should be governed "
            "derived, not hardcoded.",
            "Developer Log - Tax Payment Date",
        ),
        (
            "Pay frequency and provider support must be status-honest for daily, weekly, fortnightly, monthly and "
            "quarterly frequencies, with unsupported frequency status where support is missing.",
            "Developer Log - Tax Pay Frequency",
        ),
        (
            "Gross-to-net, gross to net, net pay, finalised totals, finalised payment memory and PAYG outcome connect "
            "withholding to payment evidence.",
            "Developer Log - Tax Gross Net Finalised Totals",
        ),
        (
            "Supplementary incremental PAYG and supplementary PAYG should be incremental over same-period taxable "
            "earnings, less prior PAYG withheld.",
            "Developer Log - Supplementary PAYG",
        ),
        (
            "Tax / PAYG should connect to Worker Story and PayRun Admin Queue for tax readiness, unsupported states, "
            "correction and reprocessing consequences.",
            "Developer Log - Tax Worker Story Admin Queue",
        ),
        (
            "Unsupported tax scenarios, unsupported frequencies, explicit status, configuration status and review "
            "states should prevent silent success.",
            "Developer Log - Tax Unsupported Review States",
        ),
        (
            "Tax / PAYG outstanding hardening includes provider support, non-weekly frequencies, taxable basis "
            "governance, withholding instruction UI, supplementary tax and full TaxStory.",
            "Developer Log - Tax Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_deductions_obligations_benchmark_evidence(db_session):
    evidence = [
        (
            "Deductions / Obligations are governed application outcomes and governed payroll outcome evidence, not "
            "automatic raw net-pay subtraction.",
            "Developer Log - Deductions Obligations Purpose",
        ),
        (
            "The deduction chain is LibraryDeductionTemplate to AccountDeductionTemplate to ContactPayrollDeduction "
            "to PayRunDeductionApplication. Library templates are advisory accelerators; account templates and worker "
            "instructions become operative configuration.",
            "Developer Log - Deduction Template Chain",
        ),
        (
            "ContactPayrollDeduction is the worker-specific deduction instruction and operative configuration for a "
            "worker deduction.",
            "Developer Log - Worker Deduction Instruction",
        ),
        (
            "PayRunDeductionApplication is PayRun event and outcome memory for requested, taken, skipped and unmet "
            "amounts.",
            "Developer Log - PayRun Deduction Application Memory",
        ),
        (
            "Supplementary deduction memory means supplementary PayRuns must use prior same-period application memory "
            "so recurring deductions do not blindly repeat.",
            "Developer Log - Supplementary Deduction Memory",
        ),
        (
            "Deduction applicability comes before affordability. Affordability, priority, partial, full-only and "
            "carry-forward treatment must be governed and explainable.",
            "Developer Log - Deduction Applicability Affordability Priority",
        ),
        (
            "Skipped, partial, unmet and carry-forward deductions must remain visible and must not silently disappear.",
            "Developer Log - Skipped Partial Unmet Carry Forward",
        ),
        (
            "ContactPayrollObligation and ContactPayrollObligationLedger represent durable obligations and "
            "balance-bearing recovery. Reducing-balance recovery must cap recovery by outstanding balance and complete "
            "with ledger evidence.",
            "Developer Log - Obligation Reducing Balance Recovery",
        ),
        (
            "Negative net pay is a governed outcome requiring policy treatment, not a silent arithmetic side effect.",
            "Developer Log - Negative Net Pay Governance",
        ),
        (
            "Gross-to-net, gross to net, payment execution and remittance surfaces should expose deduction readiness.",
            "Developer Log - Deductions Gross Net Payment Execution",
        ),
        (
            "Deductions / Obligations connect to Worker Story, PayRun Admin Queue and Worker Attention for readiness "
            "and issues.",
            "Developer Log - Deductions Worker Story Admin Queue",
        ),
        (
            "Deductions / Obligations outstanding hardening remains around full UI, remittance, payment execution, "
            "obligation write-off, costing consequences, negative-net-pay policy and deduction tax integration.",
            "Developer Log - Deductions Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_retro_replay_benchmark_evidence(db_session):
    evidence = [
        (
            "Retro / Replay is governed historical correction and evidence replay, not ordinary reprocessing.",
            "Developer Log - Retro Replay Purpose",
        ),
        (
            "Attributed-period truth and paid-period truth must remain distinct for replay correction evidence.",
            "Developer Log - Retro Attributed Paid Period Truth",
        ),
        (
            "Finalised outcome memory records finalised outcomes as historical payment truth and should not be "
            "silently overwritten.",
            "Developer Log - Retro Finalised Outcome Memory",
        ),
        (
            "Current-effective payroll truth is not the same as historical truth or finalised truth.",
            "Developer Log - Retro Current Effective Historical Truth",
        ),
        (
            "Bucket snapshot, basis snapshots, calculation evidence, source hashes and historical bucket evidence "
            "matter for replay.",
            "Developer Log - Retro Bucket Basis Snapshot",
        ),
        (
            "Source change and configuration change should create dependency detection and dirty/replay candidates "
            "rather than hidden recalculation.",
            "Developer Log - Retro Dependency Detection",
        ),
        (
            "Retro PayRuns and retro PayRun evidence differ from supplementary PayRuns and supplementary PayRun "
            "evidence; they are not the same concept.",
            "Developer Log - Retro Supplementary Distinction",
        ),
        (
            "Comparison / Remediation and variance may depend on retro/replay evidence, but comparison is not the "
            "same concept as Retro / Replay.",
            "Developer Log - Retro Comparison Variance",
        ),
        (
            "Retro / Replay should connect to Worker Story at worker level so worker evidence explains retro impacts "
            "and replay impacts.",
            "Developer Log - Retro Worker Story",
        ),
        (
            "PayRun Admin Queue, Admin Queue and Movement Review should surface retro candidates, blockers, review "
            "actions, dependency issues and variance without treating variance as automatic proof of retro error.",
            "Developer Log - Retro Admin Queue Movement Review",
        ),
        (
            "Audit replay should preserve non-destructive history so historical evidence remains auditable through "
            "correction/replay.",
            "Developer Log - Retro Audit Replay",
        ),
        (
            "Retro / Replay outstanding hardening remains future work because full retro/replay implementation and "
            "dependency detection are not complete.",
            "Developer Log - Retro Outstanding Hardening",
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


def test_payroll_bases_and_totals_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.payroll_bases_and_totals.json")

    assert manifest["name"] == "Payroll Bases & Totals rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} >= {
        "payroll-bases-and-totals-rich-answer",
        "payroll-bases-current-effective-truth",
        "payroll-bases-vs-reporting-totals",
        "payroll-bases-bucket-definition-membership",
        "payroll-bases-stale-bucket-results",
        "payroll-bases-worker-story-movement-review",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.payroll_bases_and_totals.json")
    assert result["total"] == 6
    assert result["results"][0]["checks"]["answer_mode"] is True


def test_payrun_admin_queue_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.payrun_admin_queue.json")

    assert manifest["name"] == "PayRun Admin Queue rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} >= {
        "payrun-admin-queue-rich-answer",
        "payrun-admin-queue-vs-command-centre",
        "payrun-admin-queue-cleanliness-assurance",
        "payrun-admin-queue-blockers-warnings-ready",
        "payrun-admin-queue-worker-attention-dirty-contacts",
        "payrun-admin-queue-finalisation-readiness",
        "payrun-admin-queue-assurance-snapshot",
        "payrun-admin-queue-review-surface-connections",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.payrun_admin_queue.json")
    assert result["total"] == 8
    assert result["results"][0]["checks"]["answer_mode"] is True


def test_movement_review_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.movement_review.json")

    assert manifest["name"] == "Movement Review rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} >= {
        "movement-review-rich-answer",
        "movement-review-review-worthy-not-error",
        "movement-review-organisation-worker-lenses",
        "movement-review-comparable-periods-variance",
        "movement-review-payroll-bases",
        "movement-review-worker-story",
        "movement-review-admin-queue-assurance",
        "movement-review-trend-only-rolling-ytd",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.movement_review.json")
    assert result["total"] == 8
    assert result["results"][0]["checks"]["answer_mode"] is True


def test_comparison_remediation_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.comparison_remediation.json")

    assert manifest["name"] == "Comparison / Remediation rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} >= {
        "comparison-remediation-rich-answer",
        "comparison-remediation-three-lanes",
        "comparison-remediation-primary-award-path",
        "comparison-remediation-imported-actuals",
        "comparison-remediation-policy",
        "comparison-remediation-evidence-before-variance",
        "comparison-remediation-variance-lines-not-manual",
        "comparison-remediation-classification-mapping",
        "comparison-remediation-surface-connections",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.comparison_remediation.json")
    assert result["total"] == 9
    assert result["results"][0]["checks"]["answer_mode"] is True


def test_tax_payg_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.tax_payg.json")

    assert manifest["name"] == "Tax / PAYG rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} >= {
        "tax-payg-rich-answer",
        "tax-payg-minerva-not-calculate",
        "tax-payg-taxstory-explainability",
        "tax-payg-taxable-basis-payroll-bases",
        "tax-payg-payment-date-context",
        "tax-payg-pay-frequency-support",
        "tax-payg-worker-tax-readiness",
        "tax-payg-supplementary-incremental",
        "tax-payg-worker-story-admin-queue",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.tax_payg.json")
    assert result["total"] == 9
    assert result["results"][0]["checks"]["answer_mode"] is True


def test_deductions_obligations_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.deductions_obligations.json")

    assert manifest["name"] == "Deductions / Obligations rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} >= {
        "deductions-obligations-rich-answer",
        "deductions-obligations-template-chain",
        "deductions-obligations-application-memory",
        "deductions-obligations-supplementary-memory",
        "deductions-obligations-applicability-affordability",
        "deductions-obligations-skipped-partial-unmet",
        "deductions-obligations-deduction-vs-obligation",
        "deductions-obligations-reducing-balance",
        "deductions-obligations-negative-net-pay",
        "deductions-obligations-worker-story-admin-queue",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.deductions_obligations.json")
    assert result["total"] == 10
    assert result["results"][0]["checks"]["answer_mode"] is True


def test_retro_replay_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.retro_replay.json")

    assert manifest["name"] == "Retro / Replay rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} >= {
        "retro-replay-rich-answer",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.retro_replay.json")
    assert result["total"] == 1
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


def test_payroll_bases_and_totals_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_payroll_bases_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.payroll_bases_and_totals.json")

    assert result["name"] == "Payroll Bases & Totals rich-answer benchmark"
    assert result["total"] == 6
    assert result["all_passed"] is True
    assert {item["id"] for item in result["results"]} == {
        "payroll-bases-and-totals-rich-answer",
        "payroll-bases-current-effective-truth",
        "payroll-bases-vs-reporting-totals",
        "payroll-bases-bucket-definition-membership",
        "payroll-bases-stale-bucket-results",
        "payroll-bases-worker-story-movement-review",
    }


def test_payrun_admin_queue_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_payrun_admin_queue_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.payrun_admin_queue.json")

    assert result["name"] == "PayRun Admin Queue rich-answer benchmark"
    assert result["total"] == 8
    assert result["all_passed"] is True
    assert {item["id"] for item in result["results"]} == {
        "payrun-admin-queue-rich-answer",
        "payrun-admin-queue-vs-command-centre",
        "payrun-admin-queue-cleanliness-assurance",
        "payrun-admin-queue-blockers-warnings-ready",
        "payrun-admin-queue-worker-attention-dirty-contacts",
        "payrun-admin-queue-finalisation-readiness",
        "payrun-admin-queue-assurance-snapshot",
        "payrun-admin-queue-review-surface-connections",
    }


def test_movement_review_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_movement_review_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.movement_review.json")

    assert result["name"] == "Movement Review rich-answer benchmark"
    assert result["total"] == 8
    assert result["all_passed"] is True
    assert {item["id"] for item in result["results"]} == {
        "movement-review-rich-answer",
        "movement-review-review-worthy-not-error",
        "movement-review-organisation-worker-lenses",
        "movement-review-comparable-periods-variance",
        "movement-review-payroll-bases",
        "movement-review-worker-story",
        "movement-review-admin-queue-assurance",
        "movement-review-trend-only-rolling-ytd",
    }


def test_comparison_remediation_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_comparison_remediation_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.comparison_remediation.json")

    assert result["name"] == "Comparison / Remediation rich-answer benchmark"
    assert result["total"] == 9
    assert result["all_passed"] is True
    assert {item["id"] for item in result["results"]} == {
        "comparison-remediation-rich-answer",
        "comparison-remediation-three-lanes",
        "comparison-remediation-primary-award-path",
        "comparison-remediation-imported-actuals",
        "comparison-remediation-policy",
        "comparison-remediation-evidence-before-variance",
        "comparison-remediation-variance-lines-not-manual",
        "comparison-remediation-classification-mapping",
        "comparison-remediation-surface-connections",
    }


def test_tax_payg_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_tax_payg_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.tax_payg.json")

    assert result["name"] == "Tax / PAYG rich-answer benchmark"
    assert result["total"] == 9
    assert result["all_passed"] is True
    assert {item["id"] for item in result["results"]} == {
        "tax-payg-rich-answer",
        "tax-payg-minerva-not-calculate",
        "tax-payg-taxstory-explainability",
        "tax-payg-taxable-basis-payroll-bases",
        "tax-payg-payment-date-context",
        "tax-payg-pay-frequency-support",
        "tax-payg-worker-tax-readiness",
        "tax-payg-supplementary-incremental",
        "tax-payg-worker-story-admin-queue",
    }


def test_deductions_obligations_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_deductions_obligations_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.deductions_obligations.json")

    assert result["name"] == "Deductions / Obligations rich-answer benchmark"
    assert result["total"] == 10
    assert result["all_passed"] is True
    assert {item["id"] for item in result["results"]} == {
        "deductions-obligations-rich-answer",
        "deductions-obligations-template-chain",
        "deductions-obligations-application-memory",
        "deductions-obligations-supplementary-memory",
        "deductions-obligations-applicability-affordability",
        "deductions-obligations-skipped-partial-unmet",
        "deductions-obligations-deduction-vs-obligation",
        "deductions-obligations-reducing-balance",
        "deductions-obligations-negative-net-pay",
        "deductions-obligations-worker-story-admin-queue",
    }


def test_retro_replay_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_retro_replay_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.retro_replay.json")

    assert result["name"] == "Retro / Replay rich-answer benchmark"
    assert result["total"] == 1
    assert result["all_passed"] is True
    assert {item["id"] for item in result["results"]} == {
        "retro-replay-rich-answer",
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
