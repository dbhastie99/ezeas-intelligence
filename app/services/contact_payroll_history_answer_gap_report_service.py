from dataclasses import dataclass
from datetime import UTC, datetime


CORE_CONTACT_PAYROLL_HISTORY_GROUPS = {
    "contact_payroll_history_purpose",
    "contact_identity_and_payrun_participation",
    "current_and_historical_payroll_output",
    "gross_to_net_history",
    "deductions_obligations_and_negative_net_pay",
    "tax_and_payment_readiness_history",
    "leave_and_accrual_history",
}
VALID_COVERAGE_STATUSES = {"STRONG", "WEAK", "MISSING"}


class ContactPayrollHistoryAnswerGapReportError(ValueError):
    pass


@dataclass(frozen=True)
class ContactPayrollHistoryAnswerGapFinding:
    group_key: str
    coverage_status: str
    answer_impact: str
    diagnostic_summary: str
    recommended_action: str
    rationale: str

    def to_dict(self) -> dict:
        return {
            "group_key": self.group_key,
            "coverage_status": self.coverage_status,
            "answer_impact": self.answer_impact,
            "diagnostic_summary": self.diagnostic_summary,
            "recommended_action": self.recommended_action,
            "rationale": self.rationale,
        }


@dataclass(frozen=True)
class ContactPayrollHistoryAnswerGapReport:
    report_type: str
    generated_at_utc: str
    overall_status: str
    group_findings: list[ContactPayrollHistoryAnswerGapFinding]
    recommended_next_actions: list[str]
    source_coverage_plan_id: str | None = None

    def to_dict(self) -> dict:
        return {
            "report_type": self.report_type,
            "generated_at_utc": self.generated_at_utc,
            "overall_status": self.overall_status,
            "source_coverage_plan_id": self.source_coverage_plan_id,
            "group_findings": [finding.to_dict() for finding in self.group_findings],
            "recommended_next_actions": self.recommended_next_actions,
        }


def validate_contact_payroll_history_coverage_report(coverage_report: dict) -> None:
    if not isinstance(coverage_report, dict):
        raise ContactPayrollHistoryAnswerGapReportError("Coverage report must be a JSON object.")
    if coverage_report.get("plan_id") != "CONTACT_PAYROLL_HISTORY":
        raise ContactPayrollHistoryAnswerGapReportError("Coverage report must have plan_id CONTACT_PAYROLL_HISTORY.")
    if not isinstance(coverage_report.get("groups"), list):
        raise ContactPayrollHistoryAnswerGapReportError("Coverage report must include groups[].")
    if not coverage_report["groups"]:
        raise ContactPayrollHistoryAnswerGapReportError("Coverage report groups[] must not be empty.")

    for index, group in enumerate(coverage_report["groups"]):
        if not isinstance(group, dict):
            raise ContactPayrollHistoryAnswerGapReportError(f"Coverage group at index {index} must be an object.")
        group_key = group.get("group_key")
        coverage_status = group.get("coverage_status")
        if not group_key:
            raise ContactPayrollHistoryAnswerGapReportError(f"Coverage group at index {index} is missing group_key.")
        if coverage_status not in VALID_COVERAGE_STATUSES:
            raise ContactPayrollHistoryAnswerGapReportError(
                f"Coverage group {group_key} has invalid coverage_status {coverage_status!r}."
            )


def _diagnostic_summary(group: dict) -> str:
    notes = group.get("diagnostic_notes") or []
    first_note = notes[0] if notes else "No diagnostic note was provided."
    return (
        f"{group.get('group_label') or group['group_key']}: {first_note} "
        f"Matched {group.get('matched_chunk_count', 0)} chunk(s) across "
        f"{group.get('matched_document_count', 0)} document(s)."
    )


def _finding_for_group(group: dict) -> ContactPayrollHistoryAnswerGapFinding:
    group_key = group["group_key"]
    status = group["coverage_status"]
    is_core = group_key in CORE_CONTACT_PAYROLL_HISTORY_GROUPS

    if status == "STRONG":
        return ContactPayrollHistoryAnswerGapFinding(
            group_key=group_key,
            coverage_status=status,
            answer_impact="LOW",
            diagnostic_summary=_diagnostic_summary(group),
            recommended_action="KEEP",
            rationale="Formal-corpus coverage is strong enough for the current Contact Payroll History answer standard.",
        )
    if status == "WEAK":
        action = "IMPROVE_SYNTHESIS" if is_core else "IMPROVE_RETRIEVAL_TERMS"
        return ContactPayrollHistoryAnswerGapFinding(
            group_key=group_key,
            coverage_status=status,
            answer_impact="MEDIUM",
            diagnostic_summary=_diagnostic_summary(group),
            recommended_action=action,
            rationale=(
                "Core Contact Payroll History support exists but may need clearer answer synthesis."
                if is_core
                else "Some evidence exists, but retrieval terms may need tightening before corpus expansion."
            ),
        )
    return ContactPayrollHistoryAnswerGapFinding(
        group_key=group_key,
        coverage_status=status,
        answer_impact="HIGH" if is_core else "MEDIUM",
        diagnostic_summary=_diagnostic_summary(group),
        recommended_action="ADD_FORMAL_SOURCE_EVIDENCE_LATER",
        rationale=(
            "This is a core Contact Payroll History concept and missing evidence will materially weaken answers."
            if is_core
            else "This supporting group has no useful formal-corpus evidence yet."
        ),
    )


def _overall_status(findings: list[ContactPayrollHistoryAnswerGapFinding]) -> str:
    core_findings = [finding for finding in findings if finding.group_key in CORE_CONTACT_PAYROLL_HISTORY_GROUPS]
    missing_core_count = sum(1 for finding in core_findings if finding.coverage_status == "MISSING")
    strong_count = sum(1 for finding in findings if finding.coverage_status == "STRONG")
    weak_count = sum(1 for finding in findings if finding.coverage_status == "WEAK")
    missing_count = sum(1 for finding in findings if finding.coverage_status == "MISSING")

    if missing_core_count >= 2 or (missing_core_count >= 1 and missing_count >= 3):
        return "INSUFFICIENT_CORPUS"
    if weak_count > 0 or missing_count > 0:
        return "NEEDS_REFINEMENT"
    if strong_count >= max(1, len(findings) - 1):
        return "GOOD"
    return "NEEDS_REFINEMENT"


def _recommended_next_actions(findings: list[ContactPayrollHistoryAnswerGapFinding], overall_status: str) -> list[str]:
    actions: list[str] = []
    if overall_status == "GOOD":
        actions.append("Keep current Contact Payroll History retrieval terms and answer synthesis under benchmark watch.")
    if any(f.recommended_action == "ADD_FORMAL_SOURCE_EVIDENCE_LATER" for f in findings):
        actions.append(
            "Add formal source evidence later for missing Contact Payroll History groups before widening answer claims."
        )
    if any(f.recommended_action == "IMPROVE_RETRIEVAL_TERMS" for f in findings):
        actions.append("Refine Contact Payroll History retrieval terms for weak supporting groups before adding new corpus.")
    if any(f.recommended_action == "IMPROVE_SYNTHESIS" for f in findings):
        actions.append("Tighten Contact Payroll History answer synthesis for weak core groups while keeping status caveats.")
    if overall_status == "INSUFFICIENT_CORPUS":
        actions.append("Treat Contact Payroll History answers as corpus-limited until core evidence groups are covered.")
    return list(dict.fromkeys(actions))


def build_contact_payroll_history_answer_gap_report(coverage_report: dict) -> ContactPayrollHistoryAnswerGapReport:
    validate_contact_payroll_history_coverage_report(coverage_report)
    findings = [_finding_for_group(group) for group in coverage_report["groups"]]
    overall_status = _overall_status(findings)
    return ContactPayrollHistoryAnswerGapReport(
        report_type="CONTACT_PAYROLL_HISTORY_ANSWER_GAP_REPORT",
        generated_at_utc=datetime.now(UTC).isoformat(),
        overall_status=overall_status,
        source_coverage_plan_id=coverage_report.get("plan_id"),
        group_findings=findings,
        recommended_next_actions=_recommended_next_actions(findings, overall_status),
    )
