import argparse
import json
import os
import sys
from pathlib import Path

from sqlalchemy.exc import SQLAlchemyError

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DEFAULT_MANIFEST = PROJECT_ROOT / "samples" / "eval" / "golden_questions.minerva.json"


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


def _answer_excerpt(answer: str, max_length: int = 280) -> str:
    compact = " ".join(answer.split())
    if len(compact) <= max_length:
        return compact
    return compact[:max_length].rstrip() + "..."


def print_summary(result: dict, verbose: bool) -> None:
    print(f"Golden questions: {result.get('name') or 'Unnamed'}")
    print(f"Total: {result['total']}  Passed: {result['passed']}  Failed: {result['failed']}")
    print(f"Audit/chat rows created: {result['create_audit']}")
    print()

    for item in result["results"]:
        if item["passed"] and not verbose:
            continue
        status = "PASS" if item["passed"] else "FAIL"
        print(f"[{status}] {item['id']}: {item['question']}")
        if item["failure_reasons"]:
            print("  Failed checks:")
            for reason in item["failure_reasons"]:
                print(f"  - {reason}")
        if item["top_sources"]:
            print("  Top sources:")
            for source in item["top_sources"][:3]:
                print(
                    f"  - title={source['title']!r} type={source['source_type']} "
                    f"score={source['score']} phrases={source['matched_phrases']}"
                )
        else:
            print("  Top sources: none")
        print(f"  Answer: {_answer_excerpt(item['answer'])}")
        if item["audit_id"]:
            print(f"  Audit id: {item['audit_id']}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic Minerva golden question evaluation.")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--json-output")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--create-audit", action="store_true", help="Create chat/session/audit rows for each question.")
    parser.add_argument("--allow-failures", action="store_true", help="Exit 0 even when golden checks fail.")
    args = parser.parse_args()

    if not configured_database_url():
        print("MINERVA_DATABASE_URL is not set. Copy .env.example to .env and configure SQL Server first.")
        return 2

    from app.db.session import SessionLocal
    from app.services.golden_question_service import GoldenQuestionError, run_golden_questions

    try:
        with SessionLocal() as db:
            result = run_golden_questions(
                db=db,
                manifest_path=args.manifest,
                top_k=args.top_k,
                create_audit=args.create_audit,
            )
    except GoldenQuestionError as exc:
        print(f"Golden question evaluation failed: {exc}")
        return 1
    except SQLAlchemyError as exc:
        print(f"Database connection or evaluation failed: {exc}")
        return 1

    print_summary(result, args.verbose)

    if args.json_output:
        output_path = Path(args.json_output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(f"Wrote JSON results to {output_path}")

    return 0 if result["all_passed"] or args.allow_failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
