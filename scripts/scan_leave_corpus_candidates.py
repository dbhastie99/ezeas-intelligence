import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan TXT/DOCX files for likely Annual Leave corpus relevance.")
    parser.add_argument("folder_path")
    parser.add_argument("--top", type=int, default=20)
    args = parser.parse_args()

    from app.services.leave_corpus_candidate_service import scan_leave_corpus_candidates

    try:
        result = scan_leave_corpus_candidates(args.folder_path, top=args.top)
    except ValueError as exc:
        print(f"Candidate scan failed: {exc}")
        return 1

    for warning in result.warnings:
        print(f"WARNING: {warning}")

    print(f"Scanned folder: {args.folder_path}")
    print(f"Showing top {len(result.candidates)} candidates")
    for candidate in result.candidates:
        matched = ", ".join(candidate.matched_terms) if candidate.matched_terms else "none"
        date = candidate.detected_document_date or "-"
        print(
            f"{candidate.score:>3} | {candidate.source_type:<17} | {date:<10} | "
            f"{candidate.inferred_title} | {candidate.path}"
        )
        print(f"      matched: {matched}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
