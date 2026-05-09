import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def main() -> int:
    parser = argparse.ArgumentParser(description="Review a code evidence approval manifest without modifying it.")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    from app.services.code_evidence_approval_manifest_service import review_code_evidence_approval_manifest

    try:
        payload = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"Approval manifest review failed: {exc}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(f"Approval manifest review failed: invalid JSON: {exc}", file=sys.stderr)
        return 1

    if not isinstance(payload, dict):
        print("Approval manifest review failed: manifest root must be an object.", file=sys.stderr)
        return 1

    result = review_code_evidence_approval_manifest(payload)
    result_payload = result.model_dump()

    if args.json:
        print(json.dumps(result_payload, indent=2))
        return 0 if result.is_valid else 1

    print(f"Approval status: {result.approval_status}")
    print(f"Approval required: {result.approval_required}")
    print(f"Total included files: {result.total_included_files}")
    print(f"Approved file count: {result.approved_file_count}")
    print(f"Rejected file count: {result.rejected_file_count}")
    print(f"Pending review count: {result.pending_review_count}")
    print(f"Validation valid: {result.validation_status}")
    print("Safety summary:")
    for key, value in result.safety_summary_flags.items():
        print(f"  {key}: {value}")
    _print_counts("Counts by review_status", result.counts_by_review_status)
    _print_counts("Counts by proposed_ingestion_action", result.counts_by_proposed_ingestion_action)
    _print_counts("Counts by source_type", result.counts_by_source_type)
    _print_counts("Counts by file_kind", result.counts_by_file_kind)
    _print_counts("Counts by language", result.counts_by_language)
    if result.errors:
        print("Approval manifest validation errors:", file=sys.stderr)
        for error in result.errors:
            print(f"  {error}", file=sys.stderr)
    return 0 if result.is_valid else 1


def _print_counts(label: str, counts: dict[str, int]) -> None:
    print(f"{label}:")
    for key, count in sorted(counts.items()):
        print(f"  {key}: {count}")


if __name__ == "__main__":
    raise SystemExit(main())
