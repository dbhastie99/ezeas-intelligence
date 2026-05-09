from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from app.core.enums import SourceType
from app.services.repository_metadata_service import RepositoryMetadata, resolve_repository_metadata


CODE_EXTENSIONS = {
    ".cs": "csharp",
    ".go": "go",
    ".java": "java",
    ".js": "javascript",
    ".jsx": "javascript/react",
    ".php": "php",
    ".py": "python",
    ".rb": "ruby",
    ".rs": "rust",
    ".ts": "typescript",
    ".tsx": "typescript/react",
}
CONTRACT_EXTENSIONS = {
    ".graphql": "graphql",
    ".proto": "protocol-buffers",
}
SCHEMA_EXTENSIONS = {
    ".sql": "sql",
}
STRUCTURED_EXTENSIONS = {
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
}
DOCUMENTATION_EXTENSIONS = {
    ".md": "markdown",
}
CONFIG_EXTENSIONS = {
    ".cfg": "config",
    ".css": "css",
    ".html": "html",
    ".ini": "config",
    ".scss": "scss",
    ".toml": "toml",
}
SPECIAL_FILENAMES = {
    "dockerfile": "dockerfile",
    "package.json": "node-project",
    "pyproject.toml": "python-project",
    "requirements.txt": "python-requirements",
}
SUPPORTED_EXTENSIONS = (
    set(CODE_EXTENSIONS)
    | set(CONTRACT_EXTENSIONS)
    | set(SCHEMA_EXTENSIONS)
    | set(STRUCTURED_EXTENSIONS)
    | set(DOCUMENTATION_EXTENSIONS)
    | set(CONFIG_EXTENSIONS)
)

EXCLUDED_DIR_NAMES = {
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "bin",
    "build",
    "coverage",
    "dist",
    "htmlcov",
    "node_modules",
    "obj",
    "out",
    "output",
    "outputs",
    "target",
    "venv",
}
GENERATED_DIR_NAMES = {
    ".cache",
    "cache",
    "caches",
    "generated",
    "gen",
    "tmp",
}
SENSITIVE_NAME_TOKENS = {
    "credential",
    "credentials",
    "secret",
    "secrets",
    "token",
    "tokens",
}
SENSITIVE_EXTENSIONS = {
    ".key",
    ".pem",
    ".p12",
    ".pfx",
}
BINARY_EXTENSIONS = {
    ".7z",
    ".dll",
    ".exe",
    ".gif",
    ".ico",
    ".jar",
    ".jpg",
    ".jpeg",
    ".pdf",
    ".png",
    ".pyc",
    ".so",
    ".zip",
}


@dataclass(frozen=True)
class CodeEvidenceFile:
    repo_name: str
    repo_path: str
    branch: str | None
    commit: str | None
    file_path: str
    source_type: str
    language: str
    file_kind: str
    is_test: bool
    is_generated: bool
    classification_reason: str
    review_status: str = "PENDING_REVIEW"
    review_notes: list[str] | None = None
    proposed_ingestion_action: str = "DO_NOT_INGEST_YET"

    def model_dump(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["review_notes"] = self.review_notes or []
        return payload


@dataclass(frozen=True)
class CodeEvidenceExcludedFile:
    file_path: str
    reason: str

    def model_dump(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CodeEvidenceScanResult:
    repo_name: str
    repo_path: str
    branch: str | None
    commit: str | None
    repository_metadata: RepositoryMetadata
    included_files: list[CodeEvidenceFile]
    excluded_files: list[CodeEvidenceExcludedFile]

    @property
    def total_files_scanned(self) -> int:
        return len(self.included_files) + len(self.excluded_files)

    @property
    def included_count(self) -> int:
        return len(self.included_files)

    @property
    def excluded_count(self) -> int:
        return len(self.excluded_files)

    @property
    def counts_by_source_type(self) -> dict[str, int]:
        return dict(Counter(item.source_type for item in self.included_files))

    @property
    def counts_by_language(self) -> dict[str, int]:
        return dict(Counter(item.language for item in self.included_files))

    @property
    def counts_by_file_kind(self) -> dict[str, int]:
        return dict(Counter(item.file_kind for item in self.included_files))

    @property
    def top_exclusion_reasons(self) -> list[dict[str, Any]]:
        counts = Counter(item.reason for item in self.excluded_files)
        return [{"reason": reason, "count": count} for reason, count in counts.most_common()]

    @property
    def safety_summary(self) -> dict[str, Any]:
        exclusion_counts = Counter(item.reason for item in self.excluded_files)
        return {
            "unsafe_files_excluded_count": (
                exclusion_counts["environment_file"]
                + exclusion_counts["private_key"]
                + exclusion_counts["sensitive_name"]
            ),
            "generated_or_cache_excluded_count": (
                exclusion_counts["generated_or_cache_directory"] + exclusion_counts["generated_file"]
            ),
            "binary_files_excluded_count": exclusion_counts["binary_file"],
            "included_code_content_bytes": 0,
            "code_content_captured": False,
            "database_ingestion_performed": False,
            "llm_exposure_performed": False,
        }

    def model_dump(self) -> dict[str, Any]:
        return {
            "repo_name": self.repo_name,
            "repo_path": self.repo_path,
            "branch": self.branch,
            "commit": self.commit,
            "repository_metadata": self.repository_metadata.model_dump(),
            "approval_required": True,
            "approval_status": "PENDING_REVIEW",
            "approval_notes": [],
            "approved_file_count": 0,
            "rejected_file_count": 0,
            "total_files_scanned": self.total_files_scanned,
            "included_count": self.included_count,
            "excluded_count": self.excluded_count,
            "counts_by_source_type": self.counts_by_source_type,
            "counts_by_language": self.counts_by_language,
            "counts_by_file_kind": self.counts_by_file_kind,
            "top_exclusion_reasons": self.top_exclusion_reasons,
            "safety_summary": self.safety_summary,
            "included_files": [item.model_dump() for item in self.included_files],
            "excluded_files": [item.model_dump() for item in self.excluded_files],
        }


def scan_code_evidence(repo_path: str | Path, repo_name: str) -> CodeEvidenceScanResult:
    root = Path(repo_path).resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError("repo_path must be an existing directory.")
    if not repo_name.strip():
        raise ValueError("repo_name is required.")

    repository_metadata = resolve_repository_metadata(root, repo_name)
    included: list[CodeEvidenceFile] = []
    excluded: list[CodeEvidenceExcludedFile] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative_path = _relative_path(path, root)
        exclusion_reason = _exclusion_reason(path, root)
        if exclusion_reason:
            excluded.append(CodeEvidenceExcludedFile(file_path=relative_path, reason=exclusion_reason))
            continue
        classification = classify_code_evidence_file(path, root)
        if classification is None:
            excluded.append(CodeEvidenceExcludedFile(file_path=relative_path, reason="unsupported_or_irrelevant_file"))
            continue
        included.append(
            CodeEvidenceFile(
                repo_name=repo_name,
                repo_path=str(root),
                branch=repository_metadata.branch,
                commit=repository_metadata.commit,
                file_path=relative_path,
                source_type=classification.source_type,
                language=classification.language,
                file_kind=classification.file_kind,
                is_test=classification.is_test,
                is_generated=classification.is_generated,
                classification_reason=classification.classification_reason,
            )
        )

    return CodeEvidenceScanResult(
        repo_name=repo_name,
        repo_path=str(root),
        branch=repository_metadata.branch,
        commit=repository_metadata.commit,
        repository_metadata=repository_metadata,
        included_files=included,
        excluded_files=excluded,
    )


@dataclass(frozen=True)
class CodeEvidenceClassification:
    source_type: str
    language: str
    file_kind: str
    is_test: bool
    is_generated: bool
    classification_reason: str


def classify_code_evidence_file(path: str | Path, repo_root: str | Path | None = None) -> CodeEvidenceClassification | None:
    file_path = Path(path)
    extension = file_path.suffix.lower()
    normalized_name = file_path.name.lower()
    if extension not in SUPPORTED_EXTENSIONS and normalized_name not in SPECIAL_FILENAMES:
        return None

    relative_parts = _path_parts(file_path, repo_root)
    normalized_path = "/".join(relative_parts).lower()
    is_test = _is_test_file(relative_parts)
    is_generated = _is_generated_file(file_path, relative_parts)
    language = _language_for_file(file_path)

    if is_test:
        return CodeEvidenceClassification(
            SourceType.TEST.value,
            language,
            "test",
            True,
            is_generated,
            "test path or filename pattern",
        )
    if _is_migration(relative_parts, normalized_name):
        return CodeEvidenceClassification(
            SourceType.MIGRATION.value,
            language,
            "migration",
            False,
            is_generated,
            "migration path or filename",
        )
    if _is_schema(relative_parts, normalized_name, extension):
        return CodeEvidenceClassification(
            SourceType.SCHEMA.value,
            language,
            "schema",
            False,
            is_generated,
            "schema or model path, filename, or SQL extension",
        )
    if _is_api_contract(file_path, normalized_path):
        return CodeEvidenceClassification(
            SourceType.API_CONTRACT.value,
            language,
            "api_contract",
            False,
            is_generated,
            "API contract filename, route, controller, or API path",
        )
    if _is_project_manifest(normalized_name):
        return CodeEvidenceClassification(
            SourceType.CODE.value,
            language,
            "project_manifest",
            False,
            is_generated,
            "project manifest filename",
        )
    if extension in DOCUMENTATION_EXTENSIONS:
        return CodeEvidenceClassification(
            SourceType.CODE.value,
            language,
            "documentation",
            False,
            is_generated,
            "project documentation evidence",
        )
    if _is_config_file(file_path):
        return CodeEvidenceClassification(
            SourceType.CODE.value,
            language,
            "config",
            False,
            is_generated,
            "configuration or build metadata file",
        )
    if extension in CODE_EXTENSIONS:
        return CodeEvidenceClassification(
            SourceType.CODE.value,
            language,
            "implementation",
            False,
            is_generated,
            "code extension",
        )
    return None


def _exclusion_reason(path: Path, repo_root: Path) -> str | None:
    parts = _path_parts(path, repo_root)
    lower_parts = [part.lower() for part in parts]
    name = path.name.lower()
    stem = path.stem.lower()

    if any(part in EXCLUDED_DIR_NAMES for part in lower_parts[:-1]):
        return "excluded_directory"
    if any(part in GENERATED_DIR_NAMES or part.endswith("_cache") or part.endswith("-cache") for part in lower_parts[:-1]):
        return "generated_or_cache_directory"
    if name == ".env" or name.startswith(".env."):
        return "environment_file"
    if path.suffix.lower() in SENSITIVE_EXTENSIONS or "private_key" in stem or "private-key" in stem:
        return "private_key"
    if any(token in stem for token in SENSITIVE_NAME_TOKENS):
        return "sensitive_name"
    if _is_generated_file(path, parts):
        return "generated_file"
    if path.suffix.lower() in BINARY_EXTENSIONS or _looks_binary(path):
        return "binary_file"
    return None


def _is_test_file(parts: list[str]) -> bool:
    lower_parts = [part.lower() for part in parts]
    filename = lower_parts[-1]
    return (
        "test" in lower_parts[:-1]
        or "tests" in lower_parts[:-1]
        or filename.startswith("test_")
        or filename.endswith("_test.py")
        or ".test." in filename
        or ".spec." in filename
    )


def _is_api_contract(path: Path, normalized_path: str) -> bool:
    name = path.name.lower()
    path_tokens = set(normalized_path.split("/"))
    return (
        path.suffix.lower() in CONTRACT_EXTENSIONS
        or "openapi" in name
        or "swagger" in name
        or "api_contract" in normalized_path
        or "api-contract" in normalized_path
        or bool(path_tokens & {"api", "apis", "route", "routes", "controller", "controllers"})
    )


def _is_migration(parts: list[str], normalized_name: str) -> bool:
    lower_parts = [part.lower() for part in parts]
    return (
        "migrations" in lower_parts[:-1]
        or "migration" in lower_parts[:-1]
        or "alembic" in lower_parts[:-1]
        or "versions" in lower_parts[:-1]
        or normalized_name.startswith(("migration_", "migrate_"))
        or "migration" in normalized_name
        or (normalized_name[:4].isdigit() and normalized_name.endswith((".sql", ".py")))
    )


def _is_schema(parts: list[str], normalized_name: str, extension: str) -> bool:
    lower_parts = [part.lower() for part in parts]
    return (
        extension == ".sql"
        or "schema" in normalized_name
        or "schemas" in lower_parts[:-1]
        or "models" in lower_parts[:-1]
        or normalized_name in {"models.py", "schema.py", "schemas.py"}
    )


def _is_generated_file(path: Path, parts: list[str]) -> bool:
    lower_parts = [part.lower() for part in parts]
    name = path.name.lower()
    return (
        any(part in GENERATED_DIR_NAMES for part in lower_parts[:-1])
        or "generated" in name
        or name.endswith(".g.cs")
        or name.endswith(".designer.cs")
        or name.endswith(".min.js")
    )


def _language_for_file(path: Path) -> str:
    normalized_name = path.name.lower()
    if normalized_name in SPECIAL_FILENAMES:
        return SPECIAL_FILENAMES[normalized_name]
    return _language_for_extension(path.suffix.lower())


def _language_for_extension(extension: str) -> str:
    return (
        CODE_EXTENSIONS.get(extension)
        or CONTRACT_EXTENSIONS.get(extension)
        or SCHEMA_EXTENSIONS.get(extension)
        or STRUCTURED_EXTENSIONS.get(extension)
        or DOCUMENTATION_EXTENSIONS.get(extension)
        or CONFIG_EXTENSIONS.get(extension)
        or "unknown"
    )


def _is_project_manifest(normalized_name: str) -> bool:
    return normalized_name in {"package.json", "pyproject.toml", "requirements.txt"}


def _is_config_file(path: Path) -> bool:
    normalized_name = path.name.lower()
    return normalized_name == "dockerfile" or path.suffix.lower() in (set(STRUCTURED_EXTENSIONS) | set(CONFIG_EXTENSIONS))


def _path_parts(path: Path, repo_root: str | Path | None) -> list[str]:
    if repo_root is None:
        return list(path.parts)
    try:
        return list(path.resolve().relative_to(Path(repo_root).resolve()).parts)
    except ValueError:
        return list(path.parts)


def _relative_path(path: Path, repo_root: Path) -> str:
    return path.relative_to(repo_root).as_posix()


def _looks_binary(path: Path) -> bool:
    try:
        sample = path.read_bytes()[:4096]
    except OSError:
        return True
    return b"\0" in sample
