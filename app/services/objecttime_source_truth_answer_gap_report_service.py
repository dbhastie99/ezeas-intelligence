from dataclasses import dataclass
from datetime import UTC, datetime


CORE_OBJECTTIME_SOURCE_TRUTH_GROUPS = {
    "purpose_and_operator_meaning",
    "objecttime_as_source_evidence",
    "payrun_inclusion_and_source_truth",
    "imported_and_generated_source_rows",
    "source_truth_vs_worked_hours",
    "current_effective_output_connection",
    "worker_story_connection",
    "payroll_bases_and_leave_accrual_connection",
    "comparison_movement_and_replay_connection",
    "corrections_dirty_contacts_and_reprocessing",
    "evidence_provenance_and_audit",
}
VALID_COVERAGE_STATUSES = {"STRONG", "WEAK", "MISSING"}


class ObjectTimeSourceTruthAnswerGapReportError(ValueError):
    pass


@dataclass(frozen=True)
class ObjectTimeSourceTruthAnswerGapFinding:
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
class ObjectTimeSourceTruthAnswerGapReport:
    report_type: str
    generated_at_utc: str
    overall_status: str
    group_findings: list[ObjectTimeSourceTruthAnswerGapFinding]
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


def validate_objecttime_source_truth_coverage_report(coverage_report: dict) -> None:
    if not isinstance(coverage_report, dict):
        raise ObjectTimeSourceTruthAnswerGapReportError("Coverage report must be a JSON object.")
    if coverage_report.get("plan_id") != "OBJECTTIME_SOURCE_TRUTH":
        raise ObjectTimeSourceTruthAnswerGapReportError(
            "Coverage report must have plan_id OBJECTTIME_SOURCE_TRUTH."
        )
    if not isinstance(coverage_report.get("groups"), list):
        raise ObjectTimeSourceTruthAnswerGapReportError("Coverage report must include groups[].")
    if not coverage_report["groups"]:
        raise ObjectTimeSourceTruthAnswerGapReportError("Coverage report groups[] must not be empty.")

    for index, group in enumerate(coverage_report["groups"]):
        if not isinstance(group, dict):
            raise ObjectTimeSourceTruthAnswerGapReportError(f"Coverage group at index {index} must be an object.")
        group_key = group.get("group_key")
        coverage_status = group.get("coverage_status")
        if not group_key:
            raise ObjectTimeSourceTruthAnswerGapReportError(f"Coverage group at index {index} is missing group_key.")
        if coverage_status not in VALID_COVERAGE_STATUSES:
            raise ObjectTimeSourceTruthAnswerGapReportError(
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


def _finding_for_group(group: dict) -> ObjectTimeSourceTruthAnswerGapFinding:
    group_key = group["group_key"]
    status = group["coverage_status"]
    is_core = group_key in CORE_OBJECTTIME_SOURCE_TRUTH_GROUPS

    if status == "STRONG":
        return ObjectTimeSourceTruthAnswerGapFinding(
            group_key=group_key,
            coverage_status=status,
            answer_impact="LOW",
            diagnostic_summary=_diagnostic_summary(group),
            recommended_action="KEEP",
            rationale=(
                "Formal-corpus coverage is strong enough for the current ObjectTime / Source Truth answer standard."
            ),
        )
    if status == "WEAK":
        action = "IMPROVE_SYNTHESIS" if is_core else "IMPROVE_RETRIEVAL_TERMS"
        return ObjectTimeSourceTruthAnswerGapFinding(
            group_key=group_key,
            coverage_status=status,
            answer_impact="MEDIUM",
            diagnostic_summary=_diagnostic_summary(group),
            recommended_action=action,
            rationale=(
                "Core ObjectTime / Source Truth support exists but may need clearer answer synthesis."
                if is_core
                else "Some evidence exists, but retrieval terms may need tightening before corpus expansion."
            ),
        )
    return ObjectTimeSourceTruthAnswerGapFinding(
        group_key=group_key,
        coverage_status=status,
        answer_impact="HIGH" if is_core else "MEDIUM",
        diagnostic_summary=_diagnostic_summary(group),
        recommended_action="ADD_FORMAL_SOURCE_EVIDENCE_LATER",
        rationale=(
            "This is a core ObjectTime / Source Truth concept and missing evidence will materially weaken answers."
            if is_core
            else "This supporting group has no useful formal-corpus evidence yet."
        ),
    )


def _overall_status(findings: list[ObjectTimeSourceTruthAnswerGapFinding]) -> str:
    core_findings = [finding for finding in findings if finding.group_key in CORE_OBJECTTIME_SOURCE_TRUTH_GROUPS]
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
    findings: list[ObjectTimeSourceTruthAnswerGapFinding],
    overall_status: str,
) -> list[str]:
    actions: list[str] = []
    if overall_status == "GOOD":
        actions.append(
            "Keep current ObjectTime / Source Truth retrieval terms and answer synthesis under benchmark watch."
        )
    if any(f.recommended_action == "ADD_FORMAL_SOURCE_EVIDENCE_LATER" for f in findings):
        actions.append(
            "Add formal source evidence later for missing ObjectTime / Source Truth groups before widening answer claims."
        )
    if any(f.recommended_action == "IMPROVE_RETRIEVAL_TERMS" for f in findings):
        actions.append(
            "Refine ObjectTime / Source Truth retrieval terms for weak supporting groups before adding new corpus."
        )
    if any(f.recommended_action == "IMPROVE_SYNTHESIS" for f in findings):
        actions.append(
            "Tighten ObjectTime / Source Truth answer synthesis for weak core groups while keeping status caveats."
        )
    if overall_status == "INSUFFICIENT_CORPUS":
        actions.append("Treat ObjectTime / Source Truth answers as corpus-limited until core evidence groups are covered.")
    return list(dict.fromkeys(actions))


def build_objecttime_source_truth_answer_gap_report(
    coverage_report: dict,
) -> ObjectTimeSourceTruthAnswerGapReport:
    validate_objecttime_source_truth_coverage_report(coverage_report)
    findings = [_finding_for_group(group) for group in coverage_report["groups"]]
    overall_status = _overall_status(findings)
    return ObjectTimeSourceTruthAnswerGapReport(
        report_type="OBJECTTIME_SOURCE_TRUTH_ANSWER_GAP_REPORT",
        generated_at_utc=datetime.now(UTC).isoformat(),
        overall_status=overall_status,
        source_coverage_plan_id=coverage_report.get("plan_id"),
        group_findings=findings,
        recommended_next_actions=_recommended_next_actions(findings, overall_status),
    )
