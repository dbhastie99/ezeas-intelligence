import json
import subprocess
import sys
from pathlib import Path
from subprocess import CompletedProcess

from app.core.enums import normalize_source_type
from app.services.code_evidence_scanner_service import scan_code_evidence


def _write(path, content: str = "content") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _mock_non_git(monkeypatch) -> None:
    def fake_run(command, check, capture_output, text):
        return CompletedProcess(command, 128, stdout="", stderr="not a git repository")

    monkeypatch.setattr("app.services.repository_metadata_service.subprocess.run", fake_run)


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
    }
    readme = files["README.md"]
    assert readme["file_path"] == "README.md"
    assert readme["language"] == "markdown"
    assert readme["file_kind"] == "documentation"
    assert readme["classification_reason"] == "project documentation evidence"
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
    assert payload["included_count"] == 1
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
