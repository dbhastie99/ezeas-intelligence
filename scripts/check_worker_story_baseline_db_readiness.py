import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def print_summary(result: dict) -> None:
    diagnostics = result.get("Diagnostics", {})
    target = diagnostics.get("Target", {})

    print(f"Worker Story baseline DB readiness: {result['Status']}")
    print(f"Ready: {'yes' if result['IsReady'] else 'no'}")
    print(f"Checked at UTC: {result['CheckedAtUtc']}")
    print(f"Required tables checked: {', '.join(result['RequiredTablesChecked'])}")
    print(f"Missing tables: {', '.join(result['MissingTables']) if result['MissingTables'] else 'none'}")
    print(f"Error summary: {result['ErrorSummary'] or '-'}")
    print("Diagnostics:")
    print(f"- Configuration present: {'yes' if diagnostics.get('ConfigurationPresent') else 'no'}")
    print(f"- Configuration source: {diagnostics.get('ConfigurationSource') or '-'}")
    print(f"- Checked configuration sources: {', '.join(diagnostics.get('CheckedConfigurationSources', [])) or '-'}")
    print(f"- Connection string: {diagnostics.get('ConnectionStringRedacted') or '-'}")
    print(f"- Dialect/driver: {target.get('Dialect') or '-'}/{target.get('Driver') or '-'}")
    print(f"- Server target: {target.get('Server') or '-'}")
    print(f"- Database target: {target.get('Database') or '-'}")
    print(f"- DSN target: {target.get('Dsn') or '-'}")
    print(f"- Selected ODBC driver: {target.get('SelectedOdbcDriver') or '-'}")
    print(f"- ODBC inspection: {target.get('OdbcInspection') or '-'}")
    if "SelectedOdbcDriverAvailable" in target:
        available = target.get("SelectedOdbcDriverAvailable")
        print(f"- Selected ODBC driver available: {'unknown' if available is None else 'yes' if available else 'no'}")
    if target.get("InstalledSqlServerOdbcDrivers") is not None:
        installed = target["InstalledSqlServerOdbcDrivers"]
        print(f"- Installed SQL Server ODBC drivers: {', '.join(installed) if installed else 'none detected'}")
    print(f"- Operator next step: {diagnostics.get('OperatorNextStep') or '-'}")
    print(f"Recommended next action: {result['RecommendedNextAction']}")
    print("Guardrails:")
    for guardrail in result["Guardrails"]:
        print(f"- {guardrail}")


def main(argv: list[str] | None = None, readiness_checker=None) -> int:
    parser = argparse.ArgumentParser(description="Check Worker Story baseline DB readiness without writing data.")
    parser.add_argument("--json", action="store_true", help="Print readiness as JSON.")
    args = parser.parse_args(argv)

    if readiness_checker is None:
        from app.services.worker_story_baseline_db_readiness_service import (
            check_worker_story_baseline_db_readiness,
        )

        readiness_checker = check_worker_story_baseline_db_readiness

    result = readiness_checker().to_dict()

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_summary(result)

    return 0 if result["IsReady"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
