import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def print_summary(result: dict) -> None:
    print(f"Worker Story baseline DB readiness: {result['Status']}")
    print(f"Ready: {'yes' if result['IsReady'] else 'no'}")
    print(f"Checked at UTC: {result['CheckedAtUtc']}")
    print(f"Required tables checked: {', '.join(result['RequiredTablesChecked'])}")
    print(f"Missing tables: {', '.join(result['MissingTables']) if result['MissingTables'] else 'none'}")
    print(f"Error summary: {result['ErrorSummary'] or '-'}")
    print(f"Recommended next action: {result['RecommendedNextAction']}")
    print("Guardrails:")
    for guardrail in result["Guardrails"]:
        print(f"- {guardrail}")


def main(argv: list[str] | None = None, readiness_checker=None) -> int:
    parser = argparse.ArgumentParser(description="Check Worker Story baseline DB readiness without writing data.")
    parser.add_argument("--json", action="store_true", help="Print readiness as JSON.")
    args = parser.parse_args(argv)

    if readiness_checker is None:
        from app.services.worker_story_baseline_db_readiness_service import (
            check_worker_story_baseline_db_readiness,
        )

        readiness_checker = check_worker_story_baseline_db_readiness

    result = readiness_checker().to_dict()

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_summary(result)

    return 0 if result["IsReady"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
