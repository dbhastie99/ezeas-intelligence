import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a metadata-only code ingestion plan from an approval manifest.")
    parser.add_argument("--approval-manifest", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    from app.services.code_metadata_ingestion_plan_service import (
        build_code_metadata_ingestion_plan,
        summarize_code_metadata_ingestion_plan,
    )

    approval_manifest_path = Path(args.approval_manifest)
    output_path = Path(args.output)
    try:
        approval_manifest = json.loads(approval_manifest_path.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"Code metadata ingestion plan failed: {exc}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(f"Code metadata ingestion plan failed: invalid JSON: {exc}", file=sys.stderr)
        return 1

    if not isinstance(approval_manifest, dict):
        print("Code metadata ingestion plan failed: approval manifest root must be an object.", file=sys.stderr)
        return 1

    plan, validation_result = build_code_metadata_ingestion_plan(
        approval_manifest=approval_manifest,
        source_approval_manifest=approval_manifest_path,
    )
    if plan is None or not validation_result.is_valid:
        for error in validation_result.errors:
            print(f"Code metadata ingestion plan error: {error}", file=sys.stderr)
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    summary = summarize_code_metadata_ingestion_plan(plan)
    summary["plan_path"] = str(output_path.resolve())
    if args.json:
        print(json.dumps(summary, indent=2))
        return 0

    print(f"Plan path: {output_path.resolve()}")
    print(f"Plan status: {summary['plan_status']}")
    print(f"Approved file count: {summary['approved_file_count']}")
    _print_counts("Counts by source_type", summary["counts_by_source_type"])
    _print_counts("Counts by file_kind", summary["counts_by_file_kind"])
    _print_counts("Counts by language", summary["counts_by_language"])
    return 0


def _print_counts(label: str, counts: dict[str, int]) -> None:
    print(f"{label}:")
    for key, count in sorted(counts.items()):
        print(f"  {key}: {count}")


if __name__ == "__main__":
    raise SystemExit(main())
