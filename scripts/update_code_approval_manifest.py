import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def main() -> int:
    parser = argparse.ArgumentParser(description="Update review fields in a code evidence approval manifest.")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--file-path", required=True)
    parser.add_argument("--review-status", required=True, choices=["PENDING_REVIEW", "APPROVED", "REJECTED"])
    parser.add_argument(
        "--proposed-ingestion-action",
        required=True,
        choices=["DO_NOT_INGEST_YET", "INGEST_METADATA_ONLY"],
    )
    parser.add_argument("--note", action="append", default=[])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    from app.services.code_evidence_approval_manifest_service import update_code_evidence_approval_manifest

    manifest_path = Path(args.manifest)
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"Approval manifest update failed: {exc}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(f"Approval manifest update failed: invalid JSON: {exc}", file=sys.stderr)
        return 1

    if not isinstance(payload, dict):
        print("Approval manifest update failed: manifest root must be an object.", file=sys.stderr)
        return 1

    updated_payload, result = update_code_evidence_approval_manifest(
        payload=payload,
        file_path=args.file_path,
        review_status=args.review_status,
        proposed_ingestion_action=args.proposed_ingestion_action,
        notes=args.note,
    )
    result_payload = result.model_dump()
    if not result.is_valid:
        if args.json:
            print(json.dumps(result_payload, indent=2))
        for error in result.errors:
            print(f"Approval manifest update error: {error}", file=sys.stderr)
        return 1

    manifest_path.write_text(json.dumps(updated_payload, indent=2), encoding="utf-8")
    if args.json:
        print(json.dumps(result_payload, indent=2))
        return 0

    print(f"Updated file_path: {result.file_path}")
    print(f"Review status: {result.review_status}")
    print(f"Proposed ingestion action: {result.proposed_ingestion_action}")
    print(f"Approved file count: {result.approved_file_count}")
    print(f"Rejected file count: {result.rejected_file_count}")
    print(f"Pending review count: {result.pending_review_count}")
    print(f"Approval status: {result.approval_status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
