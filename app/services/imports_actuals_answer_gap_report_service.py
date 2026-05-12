from dataclasses import dataclass
from datetime import UTC, datetime


CORE_IMPORTS_ACTUALS_GROUPS = {
    "purpose_and_operator_meaning",
    "imported_timesheet_source_truth",
    "imported_payroll_actuals_lane",
    "source_system_mapping_and_validation",
    "pay_code_and_rate_type_mapping",
    "position_classification_mapping",
    "objecttime_and_source_truth_connection",
    "comparison_and_remediation_connection",
    "reconciliation_and_movement_review_connection",
    "worker_story_and_admin_queue_connection",
    "evidence_provenance_and_audit",
}
VALID_COVERAGE_STATUSES = {"STRONG", "WEAK", "MISSING"}


class ImportsActualsAnswerGapReportError(ValueError):
    pass


@dataclass(frozen=True)
class ImportsActualsAnswerGapFinding:
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
class ImportsActualsAnswerGapReport:
    report_type: str
    generated_at_utc: str
    overall_status: str
    group_findings: list[ImportsActualsAnswerGapFinding]
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


def validate_imports_actuals_coverage_report(coverage_report: dict) -> None:
    if not isinstance(coverage_report, dict):
        raise ImportsActualsAnswerGapReportError("Coverage report must be a JSON object.")
    if coverage_report.get("plan_id") != "IMPORTS_ACTUALS":
        raise ImportsActualsAnswerGapReportError("Coverage report must have plan_id IMPORTS_ACTUALS.")
    if not isinstance(coverage_report.get("groups"), list):
        raise ImportsActualsAnswerGapReportError("Coverage report must include groups[].")
    if not coverage_report["groups"]:
        raise ImportsActualsAnswerGapReportError("Coverage report groups[] must not be empty.")

    for index, group in enumerate(coverage_report["groups"]):
        if not isinstance(group, dict):
            raise ImportsActualsAnswerGapReportError(f"Coverage group at index {index} must be an object.")
        group_key = group.get("group_key")
        coverage_status = group.get("coverage_status")
        if not group_key:
            raise ImportsActualsAnswerGapReportError(f"Coverage group at index {index} is missing group_key.")
        if coverage_status not in VALID_COVERAGE_STATUSES:
            raise ImportsActualsAnswerGapReportError(
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


def _finding_for_group(group: dict) -> ImportsActualsAnswerGapFinding:
    group_key = group["group_key"]
    status = group["coverage_status"]
    is_core = group_key in CORE_IMPORTS_ACTUALS_GROUPS

    if status == "STRONG":
        return ImportsActualsAnswerGapFinding(
            group_key=group_key,
            coverage_status=status,
            answer_impact="LOW",
            diagnostic_summary=_diagnostic_summary(group),
            recommended_action="KEEP",
            rationale="Formal-corpus coverage is strong enough for the current Imports / Actuals answer standard.",
        )
    if status == "WEAK":
        action = "IMPROVE_SYNTHESIS" if is_core else "IMPROVE_RETRIEVAL_TERMS"
        return ImportsActualsAnswerGapFinding(
            group_key=group_key,
            coverage_status=status,
            answer_impact="MEDIUM",
            diagnostic_summary=_diagnostic_summary(group),
            recommended_action=action,
            rationale=(
                "Core Imports / Actuals support exists but may need clearer answer synthesis."
                if is_core
                else "Some evidence exists, but retrieval terms may need tightening before corpus expansion."
            ),
        )
    return ImportsActualsAnswerGapFinding(
        group_key=group_key,
        coverage_status=status,
        answer_impact="HIGH" if is_core else "MEDIUM",
        diagnostic_summary=_diagnostic_summary(group),
        recommended_action="ADD_FORMAL_SOURCE_EVIDENCE_LATER",
        rationale=(
            "This is a core Imports / Actuals concept and missing evidence will materially weaken answers."
            if is_core
            else "This supporting group has no useful formal-corpus evidence yet."
        ),
    )


def _overall_status(findings: list[ImportsActualsAnswerGapFinding]) -> str:
    core_findings = [finding for finding in findings if finding.group_key in CORE_IMPORTS_ACTUALS_GROUPS]
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


def _recommended_next_actions(
    findings: list[ImportsActualsAnswerGapFinding],
    overall_status: str,
) -> list[str]:
    actions: list[str] = []
    if overall_status == "GOOD":
        actions.append("Keep current Imports / Actuals retrieval terms and answer synthesis under benchmark watch.")
    if any(f.recommended_action == "ADD_FORMAL_SOURCE_EVIDENCE_LATER" for f in findings):
        actions.append("Add formal source evidence later for missing Imports / Actuals groups before widening answer claims.")
    if any(f.recommended_action == "IMPROVE_RETRIEVAL_TERMS" for f in findings):
        actions.append("Refine Imports / Actuals retrieval terms for weak supporting groups before adding new corpus.")
    if any(f.recommended_action == "IMPROVE_SYNTHESIS" for f in findings):
        actions.append("Tighten Imports / Actuals answer synthesis for weak core groups while keeping status caveats.")
    if overall_status == "INSUFFICIENT_CORPUS":
        actions.append("Treat Imports / Actuals answers as corpus-limited until core evidence groups are covered.")
    return list(dict.fromkeys(actions))


def build_imports_actuals_answer_gap_report(
    coverage_report: dict,
) -> ImportsActualsAnswerGapReport:
    validate_imports_actuals_coverage_report(coverage_report)
    findings = [_finding_for_group(group) for group in coverage_report["groups"]]
    overall_status = _overall_status(findings)
    return ImportsActualsAnswerGapReport(
        report_type="IMPORTS_ACTUALS_ANSWER_GAP_REPORT",
        generated_at_utc=datetime.now(UTC).isoformat(),
        overall_status=overall_status,
        source_coverage_plan_id=coverage_report.get("plan_id"),
        group_findings=findings,
        recommended_next_actions=_recommended_next_actions(findings, overall_status),
    )
