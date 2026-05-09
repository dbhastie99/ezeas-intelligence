import json
import subprocess
import sys
from pathlib import Path
from subprocess import CompletedProcess

from app.core.enums import normalize_source_type
from app.services.code_evidence_approval_manifest_service import build_code_evidence_approval_manifest
from app.services.code_evidence_manifest_validation_service import validate_code_evidence_manifest
from app.services.code_metadata_ingestion_plan_service import (
    build_code_metadata_ingestion_plan,
    review_code_metadata_ingestion_plan,
    validate_code_metadata_ingestion_plan,
)
from app.services.code_evidence_scanner_service import scan_code_evidence


def _write(path, content: str = "content") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _mock_non_git(monkeypatch) -> None:
    def fake_run(command, check, capture_output, text):
        return CompletedProcess(command, 128, stdout="", stderr="not a git repository")

    monkeypatch.setattr("app.services.repository_metadata_service.subprocess.run", fake_run)


def _valid_manifest_payload(tmp_path, monkeypatch) -> dict:
    _mock_non_git(monkeypatch)
    _write(tmp_path / "src" / "main.py", "print('ok')")
    return scan_code_evidence(tmp_path, "sample").model_dump()


def _valid_approval_manifest_payload(tmp_path, monkeypatch) -> dict:
    payload = _valid_manifest_payload(tmp_path, monkeypatch)
    validation_result = validate_code_evidence_manifest(payload)
    payload["validation_result"] = validation_result.model_dump()
    return build_code_evidence_approval_manifest(payload)


def _multi_file_approval_manifest_payload(tmp_path, monkeypatch) -> dict:
    _mock_non_git(monkeypatch)
    _write(tmp_path / "src" / "main.py", "print('ok')")
    _write(tmp_path / "src" / "worker.py", "print('ok')")
    payload = scan_code_evidence(tmp_path, "sample").model_dump()
    validation_result = validate_code_evidence_manifest(payload)
    payload["validation_result"] = validation_result.model_dump()
    return build_code_evidence_approval_manifest(payload)


def _set_file_review(
    approval_manifest: dict,
    file_path: str,
    review_status: str,
    proposed_ingestion_action: str,
    review_notes: list[str] | None = None,
) -> dict:
    payload = _copy_payload(approval_manifest)
    matching_file = next(item for item in payload["included_files"] if item["file_path"] == file_path)
    matching_file["review_status"] = review_status
    matching_file["proposed_ingestion_action"] = proposed_ingestion_action
    matching_file["review_notes"] = review_notes or []
    payload["approved_file_count"] = sum(item["review_status"] == "APPROVED" for item in payload["included_files"])
    payload["rejected_file_count"] = sum(item["review_status"] == "REJECTED" for item in payload["included_files"])
    payload["approval_status"] = (
        "PENDING_REVIEW"
        if any(item["review_status"] == "PENDING_REVIEW" for item in payload["included_files"])
        else "REVIEWED"
    )
    return payload


def _copy_payload(payload: dict) -> dict:
    return json.loads(json.dumps(payload))


def test_code_evidence_source_types_are_valid():
    assert normalize_source_type("CODE") == "CODE"
    assert normalize_source_type("TEST") == "TEST"
    assert normalize_source_type("SCHEMA") == "SCHEMA"
    assert normalize_source_type("MIGRATION") == "MIGRATION"
    assert normalize_source_type("API_CONTRACT") == "API_CONTRACT"


def test_scanner_excludes_unsafe_files(tmp_path):
    _write(tmp_path / ".env", "SECRET=value")
    _write(tmp_path / ".env.local", "SECRET=value")
    _write(tmp_path / "config" / "credentials.json", "{}")
    _write(tmp_path / "config" / "api_tokens.py", "TOKEN = 'x'")
    _write(tmp_path / "certs" / "private.key", "PRIVATE KEY")
    (tmp_path / "assets" / "logo.png").parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / "assets" / "logo.png").write_bytes(b"\x89PNG\r\n\x00")
    _write(tmp_path / "src" / "main.py", "print('ok')")

    result = scan_code_evidence(tmp_path, "sample")

    assert result.included_count == 1
    reasons_by_path = {item.file_path: item.reason for item in result.excluded_files}
    assert reasons_by_path[".env"] == "environment_file"
    assert reasons_by_path[".env.local"] == "environment_file"
    assert reasons_by_path["config/credentials.json"] == "sensitive_name"
    assert reasons_by_path["config/api_tokens.py"] == "sensitive_name"
    assert reasons_by_path["certs/private.key"] == "private_key"
    assert reasons_by_path["assets/logo.png"] == "binary_file"


def test_scanner_classifies_source_types(tmp_path):
    _write(tmp_path / "src" / "service.py")
    _write(tmp_path / "db" / "schema.sql")
    _write(tmp_path / "migrations" / "001_create_users.sql")
    _write(tmp_path / "contracts" / "openapi.yaml")

    result = scan_code_evidence(tmp_path, "sample")

    source_types_by_path = {item.file_path: item.source_type for item in result.included_files}
    assert source_types_by_path["src/service.py"] == "CODE"
    assert source_types_by_path["db/schema.sql"] == "SCHEMA"
    assert source_types_by_path["migrations/001_create_users.sql"] == "MIGRATION"
    assert source_types_by_path["contracts/openapi.yaml"] == "API_CONTRACT"


def test_scanner_classifies_test_files(tmp_path):
    _write(tmp_path / "tests" / "test_service.py")
    _write(tmp_path / "src" / "widget.spec.ts")

    result = scan_code_evidence(tmp_path, "sample")

    files = {item.file_path: item for item in result.included_files}
    assert files["tests/test_service.py"].source_type == "TEST"
    assert files["tests/test_service.py"].is_test is True
    assert files["src/widget.spec.ts"].source_type == "TEST"
    assert files["src/widget.spec.ts"].is_test is True


def test_scanner_excludes_generated_and_cache_folders(tmp_path):
    _write(tmp_path / "__pycache__" / "module.py")
    _write(tmp_path / ".git" / "config")
    _write(tmp_path / ".venv" / "Lib" / "site.py")
    _write(tmp_path / "node_modules" / "pkg" / "index.js")
    _write(tmp_path / "dist" / "bundle.js")
    _write(tmp_path / "build" / "bundle.js")
    _write(tmp_path / "generated" / "client.ts")
    _write(tmp_path / "cache" / "artifact.py")
    _write(tmp_path / "src" / "main.py")

    result = scan_code_evidence(tmp_path, "sample")

    assert [item.file_path for item in result.included_files] == ["src/main.py"]
    reasons = {item.reason for item in result.excluded_files}
    assert "excluded_directory" in reasons
    assert "generated_or_cache_directory" in reasons


def test_scanner_json_output_shape(tmp_path, monkeypatch):
    _mock_non_git(monkeypatch)
    _write(tmp_path / "src" / "main.py", "print('ok')")
    _write(tmp_path / "README.md", "# ignored")

    result = scan_code_evidence(tmp_path, "sample").model_dump()

    assert result["repo_name"] == "sample"
    assert result["repo_path"] == str(tmp_path.resolve())
    assert result["branch"] is None
    assert result["commit"] is None
    assert result["repository_metadata"]["repo_name"] == "sample"
    assert result["repository_metadata"]["repo_path"] == str(tmp_path.resolve())
    assert result["repository_metadata"]["is_git_repo"] is False
    assert result["repository_metadata"]["branch"] is None
    assert result["repository_metadata"]["commit"] is None
    assert result["repository_metadata"]["is_dirty"] is None
    assert result["repository_metadata"]["metadata_resolution_status"] == "not_git_repo"
    assert result["repository_metadata"]["metadata_resolution_warnings"]
    assert result["approval_required"] is True
    assert result["approval_status"] == "PENDING_REVIEW"
    assert result["approval_notes"] == []
    assert result["approved_file_count"] == 0
    assert result["rejected_file_count"] == 0
    assert result["total_files_scanned"] == 2
    assert result["included_count"] == 2
    assert result["excluded_count"] == 0
    assert result["counts_by_source_type"] == {"CODE": 2}
    assert result["counts_by_language"] == {"markdown": 1, "python": 1}
    assert result["counts_by_file_kind"] == {"documentation": 1, "implementation": 1}
    assert result["top_exclusion_reasons"] == []
    assert result["safety_summary"] == {
        "unsafe_files_excluded_count": 0,
        "generated_or_cache_excluded_count": 0,
        "binary_files_excluded_count": 0,
        "included_code_content_bytes": 0,
        "code_content_captured": False,
        "database_ingestion_performed": False,
        "llm_exposure_performed": False,
    }
    files = {item["file_path"]: item for item in result["included_files"]}
    assert files["src/main.py"] == {
        "repo_name": "sample",
        "repo_path": str(tmp_path.resolve()),
        "branch": None,
        "commit": None,
        "file_path": "src/main.py",
        "source_type": "CODE",
        "language": "python",
        "file_kind": "implementation",
        "is_test": False,
        "is_generated": False,
        "classification_reason": "code extension",
        "review_status": "PENDING_REVIEW",
        "review_notes": [],
        "proposed_ingestion_action": "DO_NOT_INGEST_YET",
    }
    readme = files["README.md"]
    assert readme["file_path"] == "README.md"
    assert readme["language"] == "markdown"
    assert readme["file_kind"] == "documentation"
    assert readme["classification_reason"] == "project documentation evidence"
    assert readme["review_status"] == "PENDING_REVIEW"
    assert readme["review_notes"] == []
    assert readme["proposed_ingestion_action"] == "DO_NOT_INGEST_YET"
    assert result["excluded_files"] == []


def test_language_classification_for_common_extensions_and_special_filenames(tmp_path, monkeypatch):
    _mock_non_git(monkeypatch)
    paths = [
        "Dockerfile",
        "package.json",
        "pyproject.toml",
        "requirements.txt",
        "src/app.py",
        "src/app.js",
        "src/component.jsx",
        "src/app.ts",
        "src/component.tsx",
        "config/settings.json",
        "config/settings.yaml",
        "config/settings.yml",
        "db/schema.sql",
        "README.md",
        "setup.cfg",
        "tox.ini",
        "templates/index.html",
        "assets/site.css",
        "assets/site.scss",
    ]
    for path in paths:
        _write(tmp_path / path)

    result = scan_code_evidence(tmp_path, "sample").model_dump()

    languages = {item["file_path"]: item["language"] for item in result["included_files"]}
    assert languages["Dockerfile"] == "dockerfile"
    assert languages["package.json"] == "node-project"
    assert languages["pyproject.toml"] == "python-project"
    assert languages["requirements.txt"] == "python-requirements"
    assert languages["src/app.py"] == "python"
    assert languages["src/app.js"] == "javascript"
    assert languages["src/component.jsx"] == "javascript/react"
    assert languages["src/app.ts"] == "typescript"
    assert languages["src/component.tsx"] == "typescript/react"
    assert languages["config/settings.json"] == "json"
    assert languages["config/settings.yaml"] == "yaml"
    assert languages["config/settings.yml"] == "yaml"
    assert languages["db/schema.sql"] == "sql"
    assert languages["README.md"] == "markdown"
    assert languages["setup.cfg"] == "config"
    assert languages["tox.ini"] == "config"
    assert languages["templates/index.html"] == "html"
    assert languages["assets/site.css"] == "css"
    assert languages["assets/site.scss"] == "scss"


def test_file_kind_classification(tmp_path, monkeypatch):
    _mock_non_git(monkeypatch)
    _write(tmp_path / "src" / "service.py")
    _write(tmp_path / "tests" / "test_service.py")
    _write(tmp_path / "models" / "user.py")
    _write(tmp_path / "migrations" / "0001_create_user.py")
    _write(tmp_path / "api" / "routes" / "users.py")
    _write(tmp_path / "settings.ini")
    _write(tmp_path / "README.md")
    _write(tmp_path / "package.json")

    result = scan_code_evidence(tmp_path, "sample").model_dump()

    kinds = {item["file_path"]: item["file_kind"] for item in result["included_files"]}
    assert kinds["src/service.py"] == "implementation"
    assert kinds["tests/test_service.py"] == "test"
    assert kinds["models/user.py"] == "schema"
    assert kinds["migrations/0001_create_user.py"] == "migration"
    assert kinds["api/routes/users.py"] == "api_contract"
    assert kinds["settings.ini"] == "config"
    assert kinds["README.md"] == "documentation"
    assert kinds["package.json"] == "project_manifest"


def test_source_type_classification_precedence(tmp_path, monkeypatch):
    _mock_non_git(monkeypatch)
    _write(tmp_path / "tests" / "migrations" / "001_test_schema.sql")
    _write(tmp_path / "api" / "migrations" / "001_create_user.sql")
    _write(tmp_path / "api" / "schemas" / "user.py")
    _write(tmp_path / "api" / "routes" / "users.py")

    result = scan_code_evidence(tmp_path, "sample").model_dump()

    source_types = {item["file_path"]: item["source_type"] for item in result["included_files"]}
    assert source_types["tests/migrations/001_test_schema.sql"] == "TEST"
    assert source_types["api/migrations/001_create_user.sql"] == "MIGRATION"
    assert source_types["api/schemas/user.py"] == "SCHEMA"
    assert source_types["api/routes/users.py"] == "API_CONTRACT"


def test_summary_counts_by_language_and_file_kind(tmp_path, monkeypatch):
    _mock_non_git(monkeypatch)
    _write(tmp_path / "src" / "service.py")
    _write(tmp_path / "src" / "widget.tsx")
    _write(tmp_path / "tests" / "test_service.py")
    _write(tmp_path / "README.md")
    _write(tmp_path / "package.json")

    result = scan_code_evidence(tmp_path, "sample").model_dump()

    assert result["counts_by_language"] == {
        "markdown": 1,
        "node-project": 1,
        "python": 2,
        "typescript/react": 1,
    }
    assert result["counts_by_file_kind"] == {
        "documentation": 1,
        "implementation": 2,
        "project_manifest": 1,
        "test": 1,
    }


def test_approval_metadata_exists(tmp_path, monkeypatch):
    payload = _valid_manifest_payload(tmp_path, monkeypatch)

    assert payload["approval_required"] is True
    assert payload["approval_status"] == "PENDING_REVIEW"
    assert payload["approval_notes"] == []
    assert payload["approved_file_count"] == 0
    assert payload["rejected_file_count"] == 0


def test_per_file_review_fields_exist(tmp_path, monkeypatch):
    payload = _valid_manifest_payload(tmp_path, monkeypatch)

    included_file = payload["included_files"][0]
    assert included_file["review_status"] == "PENDING_REVIEW"
    assert included_file["review_notes"] == []
    assert included_file["proposed_ingestion_action"] == "DO_NOT_INGEST_YET"


def test_valid_scanner_result_passes_manifest_validation(tmp_path, monkeypatch):
    payload = _valid_manifest_payload(tmp_path, monkeypatch)

    result = validate_code_evidence_manifest(payload).model_dump()

    assert result["is_valid"] is True
    assert result["errors"] == []
    assert result["warnings"] == []
    assert result["included_file_count"] == 1
    assert result["excluded_file_count"] == 0
    assert result["checked_at_utc"]


def test_missing_safety_summary_fails_manifest_validation(tmp_path, monkeypatch):
    payload = _copy_payload(_valid_manifest_payload(tmp_path, monkeypatch))
    payload.pop("safety_summary")

    result = validate_code_evidence_manifest(payload)

    assert result.is_valid is False
    assert "safety_summary is required." in result.errors


def test_code_content_captured_true_fails_manifest_validation(tmp_path, monkeypatch):
    payload = _copy_payload(_valid_manifest_payload(tmp_path, monkeypatch))
    payload["safety_summary"]["code_content_captured"] = True

    result = validate_code_evidence_manifest(payload)

    assert result.is_valid is False
    assert "safety_summary.code_content_captured must be False." in result.errors


def test_included_code_content_bytes_fails_manifest_validation(tmp_path, monkeypatch):
    payload = _copy_payload(_valid_manifest_payload(tmp_path, monkeypatch))
    payload["safety_summary"]["included_code_content_bytes"] = 1

    result = validate_code_evidence_manifest(payload)

    assert result.is_valid is False
    assert "safety_summary.included_code_content_bytes must be 0." in result.errors


def test_unsafe_included_path_fails_manifest_validation(tmp_path, monkeypatch):
    payload = _copy_payload(_valid_manifest_payload(tmp_path, monkeypatch))
    payload["included_files"][0]["file_path"] = "src/secret_token.py"

    result = validate_code_evidence_manifest(payload)

    assert result.is_valid is False
    assert any("unsafe fragment" in error for error in result.errors)


def test_count_mismatch_fails_manifest_validation(tmp_path, monkeypatch):
    payload = _copy_payload(_valid_manifest_payload(tmp_path, monkeypatch))
    payload["counts_by_language"] = {"python": 2}

    result = validate_code_evidence_manifest(payload)

    assert result.is_valid is False
    assert "counts_by_language does not reconcile with included_files." in result.errors


def test_non_git_directory_metadata_resolution_does_not_fail(tmp_path, monkeypatch):
    _mock_non_git(monkeypatch)
    _write(tmp_path / "src" / "main.py", "print('ok')")

    result = scan_code_evidence(tmp_path, "sample").model_dump()

    assert result["repository_metadata"]["is_git_repo"] is False
    assert result["repository_metadata"]["branch"] is None
    assert result["repository_metadata"]["commit"] is None
    assert result["repository_metadata"]["metadata_resolution_status"] == "not_git_repo"
    assert result["included_count"] == 1


def test_git_command_failure_metadata_resolution_does_not_fail(tmp_path, monkeypatch):
    _write(tmp_path / "src" / "main.py", "print('ok')")

    def fake_run(command, check, capture_output, text):
        if command[-1] == "--is-inside-work-tree":
            return CompletedProcess(command, 0, stdout="true\n", stderr="")
        if command[-2:] == ["--abbrev-ref", "HEAD"]:
            return CompletedProcess(command, 1, stdout="", stderr="branch unavailable")
        return CompletedProcess(command, 0, stdout="", stderr="")

    monkeypatch.setattr("app.services.repository_metadata_service.subprocess.run", fake_run)

    result = scan_code_evidence(tmp_path, "sample").model_dump()

    assert result["repository_metadata"]["is_git_repo"] is True
    assert result["repository_metadata"]["branch"] is None
    assert result["repository_metadata"]["commit"] is None
    assert result["repository_metadata"]["is_dirty"] is None
    assert result["repository_metadata"]["metadata_resolution_status"] == "partial"
    assert result["repository_metadata"]["metadata_resolution_warnings"]
    assert result["included_files"][0]["branch"] is None
    assert result["included_files"][0]["commit"] is None


def test_git_unavailable_metadata_resolution_does_not_fail(tmp_path, monkeypatch):
    _write(tmp_path / "src" / "main.py", "print('ok')")

    def fake_run(command, check, capture_output, text):
        raise FileNotFoundError

    monkeypatch.setattr("app.services.repository_metadata_service.subprocess.run", fake_run)

    result = scan_code_evidence(tmp_path, "sample").model_dump()

    assert result["repository_metadata"]["is_git_repo"] is False
    assert result["repository_metadata"]["branch"] is None
    assert result["repository_metadata"]["commit"] is None
    assert result["repository_metadata"]["metadata_resolution_status"] == "git_unavailable"
    assert result["repository_metadata"]["metadata_resolution_warnings"]
    assert result["included_count"] == 1


def test_git_dirty_status_is_represented(tmp_path, monkeypatch):
    _write(tmp_path / "src" / "main.py", "print('ok')")

    def fake_run(command, check, capture_output, text):
        if command[-1] == "--is-inside-work-tree":
            return CompletedProcess(command, 0, stdout="true\n", stderr="")
        if command[-2:] == ["--abbrev-ref", "HEAD"]:
            return CompletedProcess(command, 0, stdout="main\n", stderr="")
        if command[-1] == "HEAD":
            return CompletedProcess(command, 0, stdout="abc123\n", stderr="")
        if command[-2:] == ["status", "--short"]:
            return CompletedProcess(command, 0, stdout=" M src/main.py\n", stderr="")
        raise AssertionError(f"Unexpected command: {command}")

    monkeypatch.setattr("app.services.repository_metadata_service.subprocess.run", fake_run)

    result = scan_code_evidence(tmp_path, "sample").model_dump()

    assert result["branch"] == "main"
    assert result["commit"] == "abc123"
    assert result["repository_metadata"]["is_git_repo"] is True
    assert result["repository_metadata"]["is_dirty"] is True
    assert result["repository_metadata"]["metadata_resolution_status"] == "resolved"
    assert result["included_files"][0]["branch"] == "main"
    assert result["included_files"][0]["commit"] == "abc123"


def test_scanner_safety_summary_counts_exclusions(tmp_path):
    _write(tmp_path / ".env", "SECRET=value")
    _write(tmp_path / "generated" / "client.ts")
    (tmp_path / "logo.png").write_bytes(b"\x89PNG\r\n\x00")
    _write(tmp_path / "src" / "main.py", "print('ok')")

    result = scan_code_evidence(tmp_path, "sample").model_dump()

    assert result["safety_summary"] == {
        "unsafe_files_excluded_count": 1,
        "generated_or_cache_excluded_count": 1,
        "binary_files_excluded_count": 1,
        "included_code_content_bytes": 0,
        "code_content_captured": False,
        "database_ingestion_performed": False,
        "llm_exposure_performed": False,
    }


def test_cli_output_writes_valid_metadata_only_json_and_creates_parent_directory(tmp_path):
    project_root = Path(__file__).resolve().parents[1]
    repo = tmp_path / "repo"
    code_content = "def secret_calculation():\n    return 'do not export this content'\n"
    _write(repo / "src" / "main.py", code_content)
    _write(repo / ".env", "SECRET=value")
    output_path = tmp_path / "exports" / "nested" / "code-evidence.json"

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/scan_code_evidence.py",
            "--repo-path",
            str(repo),
            "--repo-name",
            "sample",
            "--output",
            str(output_path),
        ],
        cwd=project_root,
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    serialized = json.dumps(payload)
    assert output_path.exists()
    assert payload["repo_name"] == "sample"
    assert payload["repository_metadata"]["repo_name"] == "sample"
    assert payload["approval_required"] is True
    assert payload["approval_status"] == "PENDING_REVIEW"
    assert payload["approved_file_count"] == 0
    assert payload["rejected_file_count"] == 0
    assert set(payload["repository_metadata"]) == {
        "repo_name",
        "repo_path",
        "is_git_repo",
        "branch",
        "commit",
        "is_dirty",
        "metadata_resolution_status",
        "metadata_resolution_warnings",
    }
    assert payload["validation_result"]["is_valid"] is True
    assert payload["validation_result"]["errors"] == []
    assert payload["validation_result"]["included_file_count"] == 1
    assert payload["included_count"] == 1
    assert payload["included_files"][0]["review_status"] == "PENDING_REVIEW"
    assert payload["included_files"][0]["review_notes"] == []
    assert payload["included_files"][0]["proposed_ingestion_action"] == "DO_NOT_INGEST_YET"
    assert payload["safety_summary"]["code_content_captured"] is False
    assert payload["safety_summary"]["included_code_content_bytes"] == 0
    assert payload["safety_summary"]["database_ingestion_performed"] is False
    assert payload["safety_summary"]["llm_exposure_performed"] is False
    assert "secret_calculation" not in serialized
    assert "do not export this content" not in serialized
    assert "Mode: dry-run only" in completed.stdout
    assert "No code content captured." in completed.stdout
    assert "No database ingestion performed." in completed.stdout
    assert "No LLM exposure performed." in completed.stdout
    assert "Validation valid: True" in completed.stdout


def test_cli_approval_manifest_writes_valid_review_json(tmp_path):
    project_root = Path(__file__).resolve().parents[1]
    repo = tmp_path / "repo"
    code_content = "def secret_calculation():\n    return 'do not export this content'\n"
    _write(repo / "src" / "main.py", code_content)
    _write(repo / ".env", "SECRET=value")
    approval_path = tmp_path / "approval" / "code-evidence-approval.json"

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/scan_code_evidence.py",
            "--repo-path",
            str(repo),
            "--repo-name",
            "sample",
            "--approval-manifest",
            str(approval_path),
        ],
        cwd=project_root,
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(approval_path.read_text(encoding="utf-8"))
    serialized = json.dumps(payload)
    assert approval_path.exists()
    assert payload["repository_metadata"]["repo_name"] == "sample"
    assert payload["safety_summary"]["code_content_captured"] is False
    assert payload["validation_result"]["is_valid"] is True
    assert payload["approval_required"] is True
    assert payload["approval_status"] == "PENDING_REVIEW"
    assert payload["approval_notes"] == []
    assert payload["approved_file_count"] == 0
    assert payload["rejected_file_count"] == 0
    assert payload["included_files"][0]["review_status"] == "PENDING_REVIEW"
    assert payload["included_files"][0]["review_notes"] == []
    assert payload["included_files"][0]["proposed_ingestion_action"] == "DO_NOT_INGEST_YET"
    assert payload["excluded_file_summary"]["excluded_count"] == 1
    assert "excluded_files" not in payload
    assert "secret_calculation" not in serialized
    assert "do not export this content" not in serialized
    assert f"Approval manifest written to {approval_path.resolve()}" in completed.stdout
    assert "Approval status PENDING_REVIEW" in completed.stdout
    assert "No files approved for ingestion." in completed.stdout


def test_cli_returns_non_zero_when_manifest_validation_fails(tmp_path, monkeypatch):
    from scripts import scan_code_evidence

    class InvalidScanResult:
        def model_dump(self):
            payload = _valid_manifest_payload(tmp_path / "repo", monkeypatch)
            payload["safety_summary"]["code_content_captured"] = True
            return payload

    output_path = tmp_path / "invalid" / "code-evidence.json"

    monkeypatch.setattr(
        "app.services.code_evidence_scanner_service.scan_code_evidence",
        lambda repo_path, repo_name: InvalidScanResult(),
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "scan_code_evidence.py",
            "--repo-path",
            str(tmp_path),
            "--repo-name",
            "sample",
            "--output",
            str(output_path),
            "--json",
        ],
    )

    exit_code = scan_code_evidence.main()

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert exit_code == 1
    assert payload["validation_result"]["is_valid"] is False
    assert "safety_summary.code_content_captured must be False." in payload["validation_result"]["errors"]


def test_cli_approval_manifest_not_written_when_validation_fails(tmp_path, monkeypatch, capsys):
    from scripts import scan_code_evidence

    class InvalidScanResult:
        def model_dump(self):
            payload = _valid_manifest_payload(tmp_path / "repo", monkeypatch)
            payload["safety_summary"]["included_code_content_bytes"] = 10
            return payload

    output_path = tmp_path / "invalid" / "code-evidence.json"
    approval_path = tmp_path / "invalid" / "approval.json"

    monkeypatch.setattr(
        "app.services.code_evidence_scanner_service.scan_code_evidence",
        lambda repo_path, repo_name: InvalidScanResult(),
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "scan_code_evidence.py",
            "--repo-path",
            str(tmp_path),
            "--repo-name",
            "sample",
            "--output",
            str(output_path),
            "--approval-manifest",
            str(approval_path),
        ],
    )

    exit_code = scan_code_evidence.main()
    captured = capsys.readouterr()

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert exit_code == 1
    assert output_path.exists()
    assert approval_path.exists() is False
    assert payload["validation_result"]["is_valid"] is False
    assert "Approval manifest not written because scanner validation failed." in captured.err


def test_review_approval_manifest_summary_for_valid_manifest(tmp_path, monkeypatch, capsys):
    from scripts import review_code_approval_manifest

    manifest_path = tmp_path / "approval.json"
    payload = _valid_approval_manifest_payload(tmp_path / "repo", monkeypatch)
    manifest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    before = manifest_path.read_text(encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "review_code_approval_manifest.py",
            "--manifest",
            str(manifest_path),
        ],
    )

    exit_code = review_code_approval_manifest.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Approval status: PENDING_REVIEW" in captured.out
    assert "Approval required: True" in captured.out
    assert "Total included files: 1" in captured.out
    assert "Approved file count: 0" in captured.out
    assert "Rejected file count: 0" in captured.out
    assert "Pending review count: 1" in captured.out
    assert "Validation valid: True" in captured.out
    assert "PENDING_REVIEW: 1" in captured.out
    assert "DO_NOT_INGEST_YET: 1" in captured.out
    assert manifest_path.read_text(encoding="utf-8") == before


def test_review_approval_manifest_json_output_shape(tmp_path, monkeypatch, capsys):
    from scripts import review_code_approval_manifest

    manifest_path = tmp_path / "approval.json"
    payload = _valid_approval_manifest_payload(tmp_path / "repo", monkeypatch)
    manifest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "review_code_approval_manifest.py",
            "--manifest",
            str(manifest_path),
            "--json",
        ],
    )

    exit_code = review_code_approval_manifest.main()
    captured = capsys.readouterr()

    result = json.loads(captured.out)
    assert exit_code == 0
    assert result["is_valid"] is True
    assert result["errors"] == []
    assert result["approval_status"] == "PENDING_REVIEW"
    assert result["approval_required"] is True
    assert result["total_included_files"] == 1
    assert result["approved_file_count"] == 0
    assert result["rejected_file_count"] == 0
    assert result["pending_review_count"] == 1
    assert result["counts_by_review_status"] == {"PENDING_REVIEW": 1}
    assert result["counts_by_proposed_ingestion_action"] == {"DO_NOT_INGEST_YET": 1}
    assert result["counts_by_source_type"] == {"CODE": 1}
    assert result["counts_by_file_kind"] == {"implementation": 1}
    assert result["counts_by_language"] == {"python": 1}
    assert result["validation_status"] is True
    assert result["safety_summary_flags"] == {
        "code_content_captured": False,
        "included_code_content_bytes": 0,
        "database_ingestion_performed": False,
        "llm_exposure_performed": False,
    }


def test_review_approval_manifest_missing_approval_metadata_fails(tmp_path, monkeypatch, capsys):
    from scripts import review_code_approval_manifest

    manifest_path = tmp_path / "approval.json"
    payload = _valid_approval_manifest_payload(tmp_path / "repo", monkeypatch)
    payload.pop("approval_status")
    manifest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "review_code_approval_manifest.py",
            "--manifest",
            str(manifest_path),
        ],
    )

    exit_code = review_code_approval_manifest.main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "approval_status is required." in captured.err


def test_review_approval_manifest_unsafe_safety_flags_fail(tmp_path, monkeypatch, capsys):
    from scripts import review_code_approval_manifest

    manifest_path = tmp_path / "approval.json"
    payload = _valid_approval_manifest_payload(tmp_path / "repo", monkeypatch)
    payload["safety_summary"]["code_content_captured"] = True
    payload["safety_summary"]["included_code_content_bytes"] = 99
    manifest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "review_code_approval_manifest.py",
            "--manifest",
            str(manifest_path),
        ],
    )

    exit_code = review_code_approval_manifest.main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "safety_summary.code_content_captured must be False." in captured.err
    assert "safety_summary.included_code_content_bytes must be 0." in captured.err


def test_review_approval_manifest_missing_per_file_review_fields_fails(tmp_path, monkeypatch, capsys):
    from scripts import review_code_approval_manifest

    manifest_path = tmp_path / "approval.json"
    payload = _valid_approval_manifest_payload(tmp_path / "repo", monkeypatch)
    payload["included_files"][0].pop("review_status")
    payload["included_files"][0].pop("proposed_ingestion_action")
    manifest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "review_code_approval_manifest.py",
            "--manifest",
            str(manifest_path),
        ],
    )

    exit_code = review_code_approval_manifest.main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "included_files[0].review_status is required." in captured.err
    assert "included_files[0].proposed_ingestion_action is required." in captured.err


def test_update_approval_manifest_approves_one_file_as_metadata_only(tmp_path, monkeypatch, capsys):
    from scripts import update_code_approval_manifest

    manifest_path = tmp_path / "approval.json"
    payload = _multi_file_approval_manifest_payload(tmp_path / "repo", monkeypatch)
    manifest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "update_code_approval_manifest.py",
            "--manifest",
            str(manifest_path),
            "--file-path",
            "src/main.py",
            "--review-status",
            "APPROVED",
            "--proposed-ingestion-action",
            "INGEST_METADATA_ONLY",
            "--note",
            "Reviewed metadata only.",
        ],
    )

    exit_code = update_code_approval_manifest.main()
    captured = capsys.readouterr()

    updated = json.loads(manifest_path.read_text(encoding="utf-8"))
    files = {item["file_path"]: item for item in updated["included_files"]}
    assert exit_code == 0
    assert files["src/main.py"]["review_status"] == "APPROVED"
    assert files["src/main.py"]["proposed_ingestion_action"] == "INGEST_METADATA_ONLY"
    assert files["src/main.py"]["review_notes"] == ["Reviewed metadata only."]
    assert files["src/worker.py"]["review_status"] == "PENDING_REVIEW"
    assert updated["approved_file_count"] == 1
    assert updated["rejected_file_count"] == 0
    assert updated["approval_status"] == "PENDING_REVIEW"
    assert "Pending review count: 1" in captured.out
    assert "Approval status: PENDING_REVIEW" in captured.out


def test_update_approval_manifest_rejects_one_file(tmp_path, monkeypatch, capsys):
    from scripts import update_code_approval_manifest

    manifest_path = tmp_path / "approval.json"
    payload = _valid_approval_manifest_payload(tmp_path / "repo", monkeypatch)
    manifest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "update_code_approval_manifest.py",
            "--manifest",
            str(manifest_path),
            "--file-path",
            "src/main.py",
            "--review-status",
            "REJECTED",
            "--proposed-ingestion-action",
            "DO_NOT_INGEST_YET",
            "--note",
            "Not needed.",
            "--json",
        ],
    )

    exit_code = update_code_approval_manifest.main()
    captured = capsys.readouterr()

    result = json.loads(captured.out)
    updated = json.loads(manifest_path.read_text(encoding="utf-8"))
    included_file = updated["included_files"][0]
    assert exit_code == 0
    assert result["review_status"] == "REJECTED"
    assert result["proposed_ingestion_action"] == "DO_NOT_INGEST_YET"
    assert result["rejected_file_count"] == 1
    assert result["pending_review_count"] == 0
    assert result["approval_status"] == "REVIEWED"
    assert included_file["review_status"] == "REJECTED"
    assert included_file["proposed_ingestion_action"] == "DO_NOT_INGEST_YET"
    assert included_file["review_notes"] == ["Not needed."]
    assert updated["approved_file_count"] == 0
    assert updated["rejected_file_count"] == 1
    assert updated["approval_status"] == "REVIEWED"


def test_update_approval_manifest_invalid_action_status_combination_fails(tmp_path, monkeypatch, capsys):
    from scripts import update_code_approval_manifest

    manifest_path = tmp_path / "approval.json"
    payload = _valid_approval_manifest_payload(tmp_path / "repo", monkeypatch)
    manifest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    before = manifest_path.read_text(encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "update_code_approval_manifest.py",
            "--manifest",
            str(manifest_path),
            "--file-path",
            "src/main.py",
            "--review-status",
            "PENDING_REVIEW",
            "--proposed-ingestion-action",
            "INGEST_METADATA_ONLY",
        ],
    )

    exit_code = update_code_approval_manifest.main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "INGEST_METADATA_ONLY requires review_status APPROVED." in captured.err
    assert manifest_path.read_text(encoding="utf-8") == before


def test_update_approval_manifest_unknown_file_path_fails_without_modifying(tmp_path, monkeypatch, capsys):
    from scripts import update_code_approval_manifest

    manifest_path = tmp_path / "approval.json"
    payload = _valid_approval_manifest_payload(tmp_path / "repo", monkeypatch)
    manifest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    before = manifest_path.read_text(encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "update_code_approval_manifest.py",
            "--manifest",
            str(manifest_path),
            "--file-path",
            "src/missing.py",
            "--review-status",
            "APPROVED",
            "--proposed-ingestion-action",
            "INGEST_METADATA_ONLY",
        ],
    )

    exit_code = update_code_approval_manifest.main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Expected exactly one included file matching file_path 'src/missing.py'; found 0." in captured.err
    assert manifest_path.read_text(encoding="utf-8") == before


def test_update_approval_manifest_validation_failure_fails_without_modifying(tmp_path, monkeypatch, capsys):
    from scripts import update_code_approval_manifest

    manifest_path = tmp_path / "approval.json"
    payload = _valid_approval_manifest_payload(tmp_path / "repo", monkeypatch)
    payload["safety_summary"]["code_content_captured"] = True
    manifest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    before = manifest_path.read_text(encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "update_code_approval_manifest.py",
            "--manifest",
            str(manifest_path),
            "--file-path",
            "src/main.py",
            "--review-status",
            "APPROVED",
            "--proposed-ingestion-action",
            "INGEST_METADATA_ONLY",
        ],
    )

    exit_code = update_code_approval_manifest.main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "safety_summary.code_content_captured must be False." in captured.err
    assert manifest_path.read_text(encoding="utf-8") == before


def test_update_approval_manifest_counts_status_recompute_correctly(tmp_path, monkeypatch):
    from scripts import update_code_approval_manifest

    manifest_path = tmp_path / "approval.json"
    payload = _multi_file_approval_manifest_payload(tmp_path / "repo", monkeypatch)
    manifest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "update_code_approval_manifest.py",
            "--manifest",
            str(manifest_path),
            "--file-path",
            "src/main.py",
            "--review-status",
            "APPROVED",
            "--proposed-ingestion-action",
            "INGEST_METADATA_ONLY",
        ],
    )
    assert update_code_approval_manifest.main() == 0

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "update_code_approval_manifest.py",
            "--manifest",
            str(manifest_path),
            "--file-path",
            "src/worker.py",
            "--review-status",
            "REJECTED",
            "--proposed-ingestion-action",
            "DO_NOT_INGEST_YET",
        ],
    )
    assert update_code_approval_manifest.main() == 0

    updated = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert updated["approved_file_count"] == 1
    assert updated["rejected_file_count"] == 1
    assert updated["approval_status"] == "REVIEWED"


def test_update_approval_manifest_never_adds_code_content_and_preserves_safety_flags(tmp_path, monkeypatch):
    from scripts import update_code_approval_manifest

    manifest_path = tmp_path / "approval.json"
    payload = _valid_approval_manifest_payload(tmp_path / "repo", monkeypatch)
    manifest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "update_code_approval_manifest.py",
            "--manifest",
            str(manifest_path),
            "--file-path",
            "src/main.py",
            "--review-status",
            "APPROVED",
            "--proposed-ingestion-action",
            "INGEST_METADATA_ONLY",
        ],
    )
    assert update_code_approval_manifest.main() == 0

    serialized = manifest_path.read_text(encoding="utf-8")
    updated = json.loads(serialized)
    assert "print('ok')" not in serialized
    assert "code_content" not in updated["included_files"][0]
    assert updated["safety_summary"]["code_content_captured"] is False
    assert updated["safety_summary"]["included_code_content_bytes"] == 0
    assert updated["safety_summary"]["database_ingestion_performed"] is False
    assert updated["safety_summary"]["llm_exposure_performed"] is False


def test_metadata_ingestion_plan_zero_approved_files_writes_no_approved_files_plan(tmp_path, monkeypatch):
    approval_manifest = _valid_approval_manifest_payload(tmp_path / "repo", monkeypatch)

    plan, validation_result = build_code_metadata_ingestion_plan(approval_manifest, "approval.json")

    assert validation_result.is_valid is True
    assert plan["plan_type"] == "CODE_METADATA_ONLY_INGESTION_PLAN"
    assert plan["plan_status"] == "NO_APPROVED_FILES"
    assert plan["approved_file_count"] == 0
    assert plan["planned_items"] == []
    assert plan["source_approval_manifest"] == "approval.json"


def test_metadata_ingestion_plan_approved_file_creates_one_planned_item(tmp_path, monkeypatch):
    approval_manifest = _set_file_review(
        _valid_approval_manifest_payload(tmp_path / "repo", monkeypatch),
        "src/main.py",
        "APPROVED",
        "INGEST_METADATA_ONLY",
        ["Approved for metadata planning."],
    )

    plan, validation_result = build_code_metadata_ingestion_plan(approval_manifest, "approval.json")

    assert validation_result.is_valid is True
    assert plan["plan_status"] == "READY_FOR_REVIEW"
    assert plan["approved_file_count"] == 1
    assert len(plan["planned_items"]) == 1
    item = plan["planned_items"][0]
    assert item["file_path"] == "src/main.py"
    assert item["repo_name"] == "sample"
    assert item["source_type"] == "CODE"
    assert item["language"] == "python"
    assert item["file_kind"] == "implementation"
    assert item["review_status"] == "APPROVED"
    assert item["proposed_ingestion_action"] == "INGEST_METADATA_ONLY"
    assert item["review_notes"] == ["Approved for metadata planning."]


def test_metadata_ingestion_plan_excludes_unapproved_and_rejected_files(tmp_path, monkeypatch):
    approval_manifest = _multi_file_approval_manifest_payload(tmp_path / "repo", monkeypatch)
    approval_manifest = _set_file_review(approval_manifest, "src/main.py", "REJECTED", "DO_NOT_INGEST_YET")

    plan, validation_result = build_code_metadata_ingestion_plan(approval_manifest, "approval.json")

    assert validation_result.is_valid is True
    assert plan["plan_status"] == "NO_APPROVED_FILES"
    assert plan["approved_file_count"] == 0
    assert plan["planned_items"] == []


def test_metadata_ingestion_plan_safety_flags_are_false_and_zero(tmp_path, monkeypatch):
    approval_manifest = _set_file_review(
        _valid_approval_manifest_payload(tmp_path / "repo", monkeypatch),
        "src/main.py",
        "APPROVED",
        "INGEST_METADATA_ONLY",
    )

    plan, validation_result = build_code_metadata_ingestion_plan(approval_manifest, "approval.json")

    assert validation_result.is_valid is True
    assert plan["code_content_included"] is False
    assert plan["code_content_bytes"] == 0
    assert plan["db_ingestion_performed"] is False
    assert plan["llm_exposure_performed"] is False
    assert plan["execution_performed"] is False


def test_metadata_ingestion_plan_validation_catches_content_like_fields(tmp_path, monkeypatch):
    approval_manifest = _set_file_review(
        _valid_approval_manifest_payload(tmp_path / "repo", monkeypatch),
        "src/main.py",
        "APPROVED",
        "INGEST_METADATA_ONLY",
    )
    plan, validation_result = build_code_metadata_ingestion_plan(approval_manifest, "approval.json")
    assert validation_result.is_valid is True
    plan["planned_items"][0]["source_code"] = "print('do not include')"
    plan["planned_items"][0]["content"] = "do not include"

    result = validate_code_metadata_ingestion_plan(plan)

    assert result.is_valid is False
    assert "planned_items[0] must not contain content-like field 'source_code'." in result.errors
    assert "planned_items[0] must not contain content-like field 'content'." in result.errors


def test_build_code_metadata_ingestion_plan_cli_writes_valid_json(tmp_path, monkeypatch, capsys):
    from scripts import build_code_metadata_ingestion_plan

    approval_manifest = _set_file_review(
        _valid_approval_manifest_payload(tmp_path / "repo", monkeypatch),
        "src/main.py",
        "APPROVED",
        "INGEST_METADATA_ONLY",
    )
    approval_path = tmp_path / "approval.json"
    output_path = tmp_path / "plan" / "code-metadata-plan.json"
    approval_path.write_text(json.dumps(approval_manifest, indent=2), encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_code_metadata_ingestion_plan.py",
            "--approval-manifest",
            str(approval_path),
            "--output",
            str(output_path),
            "--json",
        ],
    )

    exit_code = build_code_metadata_ingestion_plan.main()
    captured = capsys.readouterr()

    summary = json.loads(captured.out)
    plan = json.loads(output_path.read_text(encoding="utf-8"))
    serialized = json.dumps(plan)
    assert exit_code == 0
    assert output_path.exists()
    assert summary["plan_path"] == str(output_path.resolve())
    assert summary["plan_status"] == "READY_FOR_REVIEW"
    assert summary["approved_file_count"] == 1
    assert summary["counts_by_source_type"] == {"CODE": 1}
    assert summary["counts_by_file_kind"] == {"implementation": 1}
    assert summary["counts_by_language"] == {"python": 1}
    assert plan["plan_type"] == "CODE_METADATA_ONLY_INGESTION_PLAN"
    assert plan["approved_file_count"] == 1
    assert plan["planned_items"][0]["file_path"] == "src/main.py"
    assert "print('ok')" not in serialized
    assert all(field not in plan["planned_items"][0] for field in ["content", "text", "source_code", "raw_content", "file_content"])


def test_review_metadata_ingestion_plan_valid_no_approved_files(tmp_path, monkeypatch, capsys):
    from scripts import review_code_metadata_ingestion_plan

    approval_manifest = _valid_approval_manifest_payload(tmp_path / "repo", monkeypatch)
    plan, validation_result = build_code_metadata_ingestion_plan(approval_manifest, "approval.json")
    assert validation_result.is_valid is True
    plan_path = tmp_path / "plan.json"
    plan_path.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    before = plan_path.read_text(encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        ["review_code_metadata_ingestion_plan.py", "--plan", str(plan_path)],
    )

    exit_code = review_code_metadata_ingestion_plan.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Plan type: CODE_METADATA_ONLY_INGESTION_PLAN" in captured.out
    assert "Plan status: NO_APPROVED_FILES" in captured.out
    assert "Approved file count: 0" in captured.out
    assert "Planned item count: 0" in captured.out
    assert "Validation valid: True" in captured.out
    assert plan_path.read_text(encoding="utf-8") == before


def test_review_metadata_ingestion_plan_valid_ready_for_review(tmp_path, monkeypatch, capsys):
    from scripts import review_code_metadata_ingestion_plan

    approval_manifest = _set_file_review(
        _valid_approval_manifest_payload(tmp_path / "repo", monkeypatch),
        "src/main.py",
        "APPROVED",
        "INGEST_METADATA_ONLY",
    )
    plan, validation_result = build_code_metadata_ingestion_plan(approval_manifest, "approval.json")
    assert validation_result.is_valid is True
    plan_path = tmp_path / "plan.json"
    plan_path.write_text(json.dumps(plan, indent=2), encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        ["review_code_metadata_ingestion_plan.py", "--plan", str(plan_path)],
    )

    exit_code = review_code_metadata_ingestion_plan.main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Plan status: READY_FOR_REVIEW" in captured.out
    assert "Approved file count: 1" in captured.out
    assert "Planned item count: 1" in captured.out
    assert "CODE: 1" in captured.out
    assert "implementation: 1" in captured.out
    assert "python: 1" in captured.out
    assert "code_content_included: False" in captured.out


def test_review_metadata_ingestion_plan_json_output_shape(tmp_path, monkeypatch, capsys):
    from scripts import review_code_metadata_ingestion_plan

    approval_manifest = _set_file_review(
        _valid_approval_manifest_payload(tmp_path / "repo", monkeypatch),
        "src/main.py",
        "APPROVED",
        "INGEST_METADATA_ONLY",
    )
    plan, validation_result = build_code_metadata_ingestion_plan(approval_manifest, "approval.json")
    assert validation_result.is_valid is True
    plan_path = tmp_path / "plan.json"
    plan_path.write_text(json.dumps(plan, indent=2), encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        ["review_code_metadata_ingestion_plan.py", "--plan", str(plan_path), "--json"],
    )

    exit_code = review_code_metadata_ingestion_plan.main()
    captured = capsys.readouterr()

    result = json.loads(captured.out)
    assert exit_code == 0
    assert result["is_valid"] is True
    assert result["errors"] == []
    assert result["warnings"] == []
    assert result["plan_type"] == "CODE_METADATA_ONLY_INGESTION_PLAN"
    assert result["plan_status"] == "READY_FOR_REVIEW"
    assert result["generated_at_utc"]
    assert result["approved_file_count"] == 1
    assert result["planned_item_count"] == 1
    assert result["repository_git_metadata"]["is_git_repo"] is False
    assert result["safety_metadata_flags"] == {
        "code_content_included": False,
        "code_content_bytes": 0,
        "db_ingestion_performed": False,
        "llm_exposure_performed": False,
        "execution_performed": False,
    }
    assert result["counts_by_source_type"] == {"CODE": 1}
    assert result["counts_by_file_kind"] == {"implementation": 1}
    assert result["counts_by_language"] == {"python": 1}


def test_review_metadata_ingestion_plan_invalid_plan_fails(tmp_path, monkeypatch, capsys):
    from scripts import review_code_metadata_ingestion_plan

    approval_manifest = _set_file_review(
        _valid_approval_manifest_payload(tmp_path / "repo", monkeypatch),
        "src/main.py",
        "APPROVED",
        "INGEST_METADATA_ONLY",
    )
    plan, validation_result = build_code_metadata_ingestion_plan(approval_manifest, "approval.json")
    assert validation_result.is_valid is True
    plan["approved_file_count"] = 2
    plan_path = tmp_path / "plan.json"
    plan_path.write_text(json.dumps(plan, indent=2), encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        ["review_code_metadata_ingestion_plan.py", "--plan", str(plan_path)],
    )

    exit_code = review_code_metadata_ingestion_plan.main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "planned_items count must equal approved_file_count." in captured.err
    assert "Validation valid: False" in captured.out


def test_review_metadata_ingestion_plan_unsafe_safety_flag_fails(tmp_path, monkeypatch, capsys):
    from scripts import review_code_metadata_ingestion_plan

    approval_manifest = _valid_approval_manifest_payload(tmp_path / "repo", monkeypatch)
    plan, validation_result = build_code_metadata_ingestion_plan(approval_manifest, "approval.json")
    assert validation_result.is_valid is True
    plan["db_ingestion_performed"] = True
    plan_path = tmp_path / "plan.json"
    plan_path.write_text(json.dumps(plan, indent=2), encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        ["review_code_metadata_ingestion_plan.py", "--plan", str(plan_path)],
    )

    exit_code = review_code_metadata_ingestion_plan.main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "db_ingestion_performed must be False." in captured.err


def test_review_metadata_ingestion_plan_service_summary_matches_plan(tmp_path, monkeypatch):
    approval_manifest = _set_file_review(
        _valid_approval_manifest_payload(tmp_path / "repo", monkeypatch),
        "src/main.py",
        "APPROVED",
        "INGEST_METADATA_ONLY",
    )
    plan, validation_result = build_code_metadata_ingestion_plan(approval_manifest, "approval.json")
    assert validation_result.is_valid is True

    result = review_code_metadata_ingestion_plan(plan).model_dump()

    assert result["is_valid"] is True
    assert result["plan_status"] == "READY_FOR_REVIEW"
    assert result["planned_item_count"] == 1
    assert result["counts_by_language"] == {"python": 1}
