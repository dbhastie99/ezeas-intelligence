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
    args = parser.parse_args()

    from app.services.code_evidence_scanner_service import scan_code_evidence

    try:
        result = scan_code_evidence(repo_path=args.repo_path, repo_name=args.repo_name)
    except ValueError as exc:
        print(f"Code evidence scan failed: {exc}", file=sys.stderr)
        return 1

    payload = result.model_dump()
    if args.json:
        print(json.dumps(payload, indent=2))
        return 0

    print(f"Repo: {payload['repo_name']}")
    print(f"Repo path: {payload['repo_path']}")
    print(f"Total files scanned: {payload['total_files_scanned']}")
    print(f"Included files: {payload['included_count']}")
    print(f"Excluded files: {payload['excluded_count']}")
    print("Counts by source_type:")
    for source_type, count in sorted(payload["counts_by_source_type"].items()):
        print(f"  {source_type}: {count}")
    print("Top exclusion reasons:")
    for item in payload["top_exclusion_reasons"][:10]:
        print(f"  {item['reason']}: {item['count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
