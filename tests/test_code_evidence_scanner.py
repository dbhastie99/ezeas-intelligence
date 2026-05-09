from app.core.enums import normalize_source_type
from app.services.code_evidence_scanner_service import scan_code_evidence


def _write(path, content: str = "content") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


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


def test_scanner_json_output_shape(tmp_path):
    _write(tmp_path / "src" / "main.py", "print('ok')")
    _write(tmp_path / "README.md", "# ignored")

    result = scan_code_evidence(tmp_path, "sample").model_dump()

    assert result["repo_name"] == "sample"
    assert result["repo_path"] == str(tmp_path.resolve())
    assert result["branch"] is None
    assert result["commit"] is None
    assert result["total_files_scanned"] == 2
    assert result["included_count"] == 1
    assert result["excluded_count"] == 1
    assert result["counts_by_source_type"] == {"CODE": 1}
    assert result["top_exclusion_reasons"] == [{"reason": "unsupported_or_irrelevant_file", "count": 1}]
    assert result["included_files"][0] == {
        "repo_name": "sample",
        "repo_path": str(tmp_path.resolve()),
        "branch": None,
        "commit": None,
        "file_path": "src/main.py",
        "source_type": "CODE",
        "language": "Python",
        "is_test": False,
        "is_generated": False,
        "classification_reason": "code extension",
    }
    assert result["excluded_files"] == [{"file_path": "README.md", "reason": "unsupported_or_irrelevant_file"}]
