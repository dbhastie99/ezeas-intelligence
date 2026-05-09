import argparse
import json
import os
import sys
from pathlib import Path

from sqlalchemy.exc import SQLAlchemyError

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def configured_database_url() -> str | None:
    env_value = os.getenv("MINERVA_DATABASE_URL")
    if env_value:
        return env_value

    env_file = PROJECT_ROOT / ".env"
    if not env_file.exists():
        return None

    for line in env_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        if key.strip() == "MINERVA_DATABASE_URL" and value.strip():
            return value.strip().strip('"').strip("'")
    return None


def print_report(report: dict) -> None:
    print(f"Worker Story corpus coverage: {report['plan_id']}")
    print(f"Domain: {report['domain']}")
    print(f"Evidence groups: {report['total_evidence_groups']}")
    print(
        "Coverage: "
        f"STRONG={report['coverage_counts']['STRONG']} "
        f"WEAK={report['coverage_counts']['WEAK']} "
        f"MISSING={report['coverage_counts']['MISSING']}"
    )
    print(f"Indexed corpus: {report['corpus_document_count']} active document(s), {report['corpus_chunk_count']} chunk(s)")
    print("Live LLM calls: no")
    print("Corpus mutation: no")
    print()

    for group in report["groups"]:
        terms = ", ".join(group["representative_matched_terms"]) if group["representative_matched_terms"] else "none"
        sources = ", ".join(
            source["title"] or source["original_file_name"] for source in group["matched_sources"][:3]
        )
        print(f"[{group['coverage_status']}] {group['group_key']} - {group['group_label']}")
        print(
            f"  Matches: {group['matched_chunk_count']} chunk(s), "
            f"{group['matched_document_count']} document(s)"
        )
        print(f"  Representative terms: {terms}")
        print(f"  Sources: {sources or 'none'}")
        if group["diagnostic_notes"]:
            print(f"  Note: {group['diagnostic_notes'][0]}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan formal corpus coverage for Worker Story evidence groups.")
    parser.add_argument("--json", action="store_true", help="Print the report as JSON.")
    parser.add_argument("--output", help="Optional path to write the JSON report.")
    parser.add_argument("--top-k-per-group", type=int, default=10)
    args = parser.parse_args()

    if not configured_database_url():
        print("MINERVA_DATABASE_URL is not set. Copy .env.example to .env and configure SQL Server first.")
        return 2

    from app.db.session import SessionLocal
    from app.services.worker_story_corpus_coverage_service import scan_worker_story_corpus_coverage

    try:
        with SessionLocal() as db:
            report = scan_worker_story_corpus_coverage(db=db, top_k_per_group=args.top_k_per_group).to_dict()
    except SQLAlchemyError as exc:
        print(f"Worker Story corpus coverage scan failed: {exc}")
        return 1

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        if not args.json:
            print(f"Wrote Worker Story corpus coverage report to {output_path}")

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_report(report)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
