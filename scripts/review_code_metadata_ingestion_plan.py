import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def main() -> int:
    parser = argparse.ArgumentParser(description="Review a metadata-only code ingestion plan without ingesting anything.")
    parser.add_argument("--plan", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    from app.services.code_metadata_ingestion_plan_service import review_code_metadata_ingestion_plan

    plan_path = Path(args.plan)
    try:
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"Code metadata ingestion plan review failed: {exc}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(f"Code metadata ingestion plan review failed: invalid JSON: {exc}", file=sys.stderr)
        return 1

    if not isinstance(plan, dict):
        print("Code metadata ingestion plan review failed: plan root must be an object.", file=sys.stderr)
        return 1

    result = review_code_metadata_ingestion_plan(plan)
    payload = result.model_dump()
    if args.json:
        print(json.dumps(payload, indent=2))
        return 0 if result.is_valid else 1

    print(f"Plan type: {result.plan_type}")
    print(f"Plan status: {result.plan_status}")
    print(f"Generated at UTC: {result.generated_at_utc}")
    print(f"Approved file count: {result.approved_file_count}")
    print(f"Planned item count: {result.planned_item_count}")
    print("Repository git metadata:")
    for key, value in result.repository_git_metadata.items():
        print(f"  {key}: {value}")
    print("Safety metadata:")
    for key, value in result.safety_metadata_flags.items():
        print(f"  {key}: {value}")
    _print_counts("Counts by source_type", result.counts_by_source_type)
    _print_counts("Counts by file_kind", result.counts_by_file_kind)
    _print_counts("Counts by language", result.counts_by_language)
    print(f"Validation valid: {result.is_valid}")
    print(f"Validation errors: {len(result.errors)}")
    for error in result.errors:
        print(f"Validation error: {error}", file=sys.stderr)
    print(f"Validation warnings: {len(result.warnings)}")
    for warning in result.warnings:
        print(f"Validation warning: {warning}")
    return 0 if result.is_valid else 1


def _print_counts(label: str, counts: dict[str, int]) -> None:
    print(f"{label}:")
    for key, count in sorted(counts.items()):
        print(f"  {key}: {count}")


if __name__ == "__main__":
    raise SystemExit(main())
