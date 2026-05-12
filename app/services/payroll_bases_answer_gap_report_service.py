from dataclasses import dataclass
from datetime import UTC, datetime


CORE_PAYROLL_BASES_GROUPS = {
    "purpose_and_operator_meaning",
    "bucket_definition_and_membership",
    "current_effective_truth",
    "readiness_and_rebuild",
}
VALID_COVERAGE_STATUSES = {"STRONG", "WEAK", "MISSING"}


class PayrollBasesAnswerGapReportError(ValueError):
    pass


@dataclass(frozen=True)
class PayrollBasesAnswerGapFinding:
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
class PayrollBasesAnswerGapReport:
    report_type: str
    generated_at_utc: str
    overall_status: str
    group_findings: list[PayrollBasesAnswerGapFinding]
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


def validate_payroll_bases_coverage_report(coverage_report: dict) -> None:
    if not isinstance(coverage_report, dict):
        raise PayrollBasesAnswerGapReportError("Coverage report must be a JSON object.")
    if coverage_report.get("plan_id") != "PAYROLL_BASES_AND_TOTALS":
        raise PayrollBasesAnswerGapReportError("Coverage report must have plan_id PAYROLL_BASES_AND_TOTALS.")
    if not isinstance(coverage_report.get("groups"), list):
        raise PayrollBasesAnswerGapReportError("Coverage report must include groups[].")
    if not coverage_report["groups"]:
        raise PayrollBasesAnswerGapReportError("Coverage report groups[] must not be empty.")

    for index, group in enumerate(coverage_report["groups"]):
        if not isinstance(group, dict):
            raise PayrollBasesAnswerGapReportError(f"Coverage group at index {index} must be an object.")
        group_key = group.get("group_key")
        coverage_status = group.get("coverage_status")
        if not group_key:
            raise PayrollBasesAnswerGapReportError(f"Coverage group at index {index} is missing group_key.")
        if coverage_status not in VALID_COVERAGE_STATUSES:
            raise PayrollBasesAnswerGapReportError(
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


def _finding_for_group(group: dict) -> PayrollBasesAnswerGapFinding:
    group_key = group["group_key"]
    status = group["coverage_status"]
    is_core = group_key in CORE_PAYROLL_BASES_GROUPS

    if status == "STRONG":
        return PayrollBasesAnswerGapFinding(
            group_key=group_key,
            coverage_status=status,
            answer_impact="LOW",
            diagnostic_summary=_diagnostic_summary(group),
            recommended_action="KEEP",
            rationale="Formal-corpus coverage is strong enough for the current Payroll Bases & Totals answer standard.",
        )
    if status == "WEAK":
        action = "IMPROVE_SYNTHESIS" if is_core else "IMPROVE_RETRIEVAL_TERMS"
        return PayrollBasesAnswerGapFinding(
            group_key=group_key,
            coverage_status=status,
            answer_impact="MEDIUM",
            diagnostic_summary=_diagnostic_summary(group),
            recommended_action=action,
            rationale=(
                "Core Payroll Bases & Totals support exists but may need clearer answer synthesis."
                if is_core
                else "Some evidence exists, but retrieval terms may need tightening before corpus expansion."
            ),
        )
    return PayrollBasesAnswerGapFinding(
        group_key=group_key,
        coverage_status=status,
        answer_impact="HIGH" if is_core else "MEDIUM",
        diagnostic_summary=_diagnostic_summary(group),
        recommended_action="ADD_FORMAL_SOURCE_EVIDENCE_LATER",
        rationale=(
            "This is a core Payroll Bases & Totals concept and missing evidence will materially weaken answers."
            if is_core
            else "This supporting group has no useful formal-corpus evidence yet."
        ),
    )


def _overall_status(findings: list[PayrollBasesAnswerGapFinding]) -> str:
    core_findings = [finding for finding in findings if finding.group_key in CORE_PAYROLL_BASES_GROUPS]
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


def _recommended_next_actions(findings: list[PayrollBasesAnswerGapFinding], overall_status: str) -> list[str]:
    actions: list[str] = []
    if overall_status == "GOOD":
        actions.append("Keep current Payroll Bases & Totals retrieval terms and answer synthesis under benchmark watch.")
    if any(f.recommended_action == "ADD_FORMAL_SOURCE_EVIDENCE_LATER" for f in findings):
        actions.append(
            "Add formal source evidence later for missing Payroll Bases & Totals groups before widening answer claims."
        )
    if any(f.recommended_action == "IMPROVE_RETRIEVAL_TERMS" for f in findings):
        actions.append("Refine Payroll Bases & Totals retrieval terms for weak supporting groups before adding new corpus.")
    if any(f.recommended_action == "IMPROVE_SYNTHESIS" for f in findings):
        actions.append("Tighten Payroll Bases & Totals answer synthesis for weak core groups while keeping status caveats.")
    if overall_status == "INSUFFICIENT_CORPUS":
        actions.append("Treat Payroll Bases & Totals answers as corpus-limited until core evidence groups are covered.")
    return list(dict.fromkeys(actions))


def build_payroll_bases_answer_gap_report(coverage_report: dict) -> PayrollBasesAnswerGapReport:
    validate_payroll_bases_coverage_report(coverage_report)
    findings = [_finding_for_group(group) for group in coverage_report["groups"]]
    overall_status = _overall_status(findings)
    return PayrollBasesAnswerGapReport(
        report_type="PAYROLL_BASES_ANSWER_GAP_REPORT",
        generated_at_utc=datetime.now(UTC).isoformat(),
        overall_status=overall_status,
        source_coverage_plan_id=coverage_report.get("plan_id"),
        group_findings=findings,
        recommended_next_actions=_recommended_next_actions(findings, overall_status),
    )
