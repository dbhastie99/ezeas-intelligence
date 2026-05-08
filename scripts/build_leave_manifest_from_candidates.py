import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a draft Annual Leave ingestion manifest from candidate docs.")
    parser.add_argument("folder_path")
    parser.add_argument("--output", required=True)
    parser.add_argument("--min-score", type=int, default=3)
    args = parser.parse_args()

    from app.services.leave_corpus_candidate_service import build_leave_manifest_from_candidates

    try:
        result = build_leave_manifest_from_candidates(
            folder_path=args.folder_path,
            output_manifest_path=args.output,
            min_score=args.min_score,
        )
    except ValueError as exc:
        print(f"Manifest build failed: {exc}")
        return 1

    for warning in result["warnings"]:
        print(f"WARNING: {warning}")
    print(f"Wrote draft manifest: {result['output_path']}")
    print(f"Included: {result['included_count']}")
    print(f"Skipped below score {args.min_score}: {result['skipped_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
