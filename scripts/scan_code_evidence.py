import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def main() -> int:
    parser = argparse.ArgumentParser(description="Dry-run scan a local repo for code evidence metadata.")
    parser.add_argument("--repo-path", required=True)
    parser.add_argument("--repo-name", required=True)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--output")
    parser.add_argument("--approval-manifest")
    args = parser.parse_args()

    from app.services.code_evidence_approval_manifest_service import build_code_evidence_approval_manifest
    from app.services.code_evidence_manifest_validation_service import validate_code_evidence_manifest
    from app.services.code_evidence_scanner_service import scan_code_evidence

    try:
        result = scan_code_evidence(repo_path=args.repo_path, repo_name=args.repo_name)
    except ValueError as exc:
        print(f"Code evidence scan failed: {exc}", file=sys.stderr)
        return 1

    payload = result.model_dump()
    validation_result = validate_code_evidence_manifest(payload)
    payload["validation_result"] = validation_result.model_dump()
    if args.output:
        write_manifest(payload, args.output)
    approval_manifest_path = None
    if args.approval_manifest:
        if validation_result.is_valid:
            approval_manifest = build_code_evidence_approval_manifest(payload)
            approval_manifest_path = write_manifest(approval_manifest, args.approval_manifest)
        else:
            print("Approval manifest not written because scanner validation failed.", file=sys.stderr)
            for error in validation_result.errors:
                print(f"Validation error: {error}", file=sys.stderr)
    if args.json:
        print(json.dumps(payload, indent=2))
        return 0 if validation_result.is_valid else 1

    print(f"Repo: {payload['repo_name']}")
    print(f"Repo path: {payload['repo_path']}")
    repository_metadata = payload["repository_metadata"]
    print(f"Git repository: {repository_metadata['is_git_repo']}")
    print(f"Branch: {repository_metadata['branch'] or 'unresolved'}")
    print(f"Commit: {repository_metadata['commit'] or 'unresolved'}")
    dirty_status = repository_metadata["is_dirty"]
    print(f"Dirty: {'unknown' if dirty_status is None else dirty_status}")
    print(f"Metadata resolution: {repository_metadata['metadata_resolution_status']}")
    for warning in repository_metadata["metadata_resolution_warnings"]:
        print(f"Metadata warning: {warning}")
    print("Mode: dry-run only")
    print("No code content captured.")
    print("No database ingestion performed.")
    print("No LLM exposure performed.")
    print(f"Validation valid: {validation_result.is_valid}")
    print(f"Validation errors: {len(validation_result.errors)}")
    for error in validation_result.errors:
        print(f"Validation error: {error}")
    print(f"Validation warnings: {len(validation_result.warnings)}")
    for warning in validation_result.warnings:
        print(f"Validation warning: {warning}")
    if args.output:
        print(f"Manifest written: {Path(args.output).resolve()}")
    if approval_manifest_path:
        print(f"Approval manifest written to {approval_manifest_path.resolve()}")
        print("Approval status PENDING_REVIEW")
        print("No files approved for ingestion.")
    print(f"Total files scanned: {payload['total_files_scanned']}")
    print(f"Included files: {payload['included_count']}")
    print(f"Excluded files: {payload['excluded_count']}")
    print("Counts by source_type:")
    for source_type, count in sorted(payload["counts_by_source_type"].items()):
        print(f"  {source_type}: {count}")
    print("Counts by language:")
    for language, count in sorted(payload["counts_by_language"].items()):
        print(f"  {language}: {count}")
    print("Counts by file_kind:")
    for file_kind, count in sorted(payload["counts_by_file_kind"].items()):
        print(f"  {file_kind}: {count}")
    print("Top exclusion reasons:")
    for item in payload["top_exclusion_reasons"][:10]:
        print(f"  {item['reason']}: {item['count']}")
    return 0 if validation_result.is_valid else 1


def write_manifest(payload: dict, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


if __name__ == "__main__":
    raise SystemExit(main())
