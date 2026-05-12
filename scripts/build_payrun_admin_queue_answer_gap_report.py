import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def print_report(report: dict) -> None:
    print(f"PayRun Admin Queue answer gap report: {report['overall_status']}")
    print(f"Report type: {report['report_type']}")
    print(f"Source coverage plan: {report.get('source_coverage_plan_id') or '-'}")
    print()
    for finding in report["group_findings"]:
        print(
            f"[{finding['answer_impact']}] {finding['group_key']} "
            f"{finding['coverage_status']} -> {finding['recommended_action']}"
        )
        print(f"  {finding['diagnostic_summary']}")
        print(f"  Rationale: {finding['rationale']}")
    print()
    print("Recommended next actions:")
    for action in report["recommended_next_actions"]:
        print(f"- {action}")
    print()
    print("Live LLM calls: no")
    print("Corpus mutation: no")
    print("Operational JSON ingestion: no")


def _load_coverage_report(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"Coverage report does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Coverage report is not valid JSON: {exc}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a PayRun Admin Queue answer-quality gap report from coverage JSON.")
    parser.add_argument("--coverage-report", required=True)
    parser.add_argument("--output")
    parser.add_argument("--json", action="store_true", help="Print the report as JSON.")
    args = parser.parse_args()

    from app.services.payrun_admin_queue_answer_gap_report_service import (
        PayRunAdminQueueAnswerGapReportError,
        build_payrun_admin_queue_answer_gap_report,
    )

    try:
        coverage_report = _load_coverage_report(Path(args.coverage_report))
        report = build_payrun_admin_queue_answer_gap_report(coverage_report).to_dict()
    except (ValueError, PayRunAdminQueueAnswerGapReportError) as exc:
        print(f"PayRun Admin Queue answer gap report failed: {exc}")
        return 1

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        if not args.json:
            print(f"Wrote PayRun Admin Queue answer gap report to {output_path}")

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_report(report)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
