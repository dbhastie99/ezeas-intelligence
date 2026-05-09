from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from app.core.enums import SourceType


CODE_EXTENSIONS = {
    ".cs": "C#",
    ".go": "Go",
    ".java": "Java",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".php": "PHP",
    ".py": "Python",
    ".rb": "Ruby",
    ".rs": "Rust",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
}
CONTRACT_EXTENSIONS = {
    ".graphql": "GraphQL",
    ".proto": "Protocol Buffers",
}
SCHEMA_EXTENSIONS = {
    ".sql": "SQL",
}
STRUCTURED_EXTENSIONS = {
    ".json": "JSON",
    ".yaml": "YAML",
    ".yml": "YAML",
}
SUPPORTED_EXTENSIONS = set(CODE_EXTENSIONS) | set(CONTRACT_EXTENSIONS) | set(SCHEMA_EXTENSIONS) | set(
    STRUCTURED_EXTENSIONS
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
    is_test: bool
    is_generated: bool
    classification_reason: str

    def model_dump(self) -> dict[str, Any]:
        return asdict(self)


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
            "total_files_scanned": self.total_files_scanned,
            "included_count": self.included_count,
            "excluded_count": self.excluded_count,
            "counts_by_source_type": self.counts_by_source_type,
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
        source_type, language, is_test, is_generated, reason = classification
        included.append(
            CodeEvidenceFile(
                repo_name=repo_name,
                repo_path=str(root),
                branch=None,
                commit=None,
                file_path=relative_path,
                source_type=source_type,
                language=language,
                is_test=is_test,
                is_generated=is_generated,
                classification_reason=reason,
            )
        )

    return CodeEvidenceScanResult(
        repo_name=repo_name,
        repo_path=str(root),
        branch=None,
        commit=None,
        included_files=included,
        excluded_files=excluded,
    )


def classify_code_evidence_file(path: str | Path, repo_root: str | Path | None = None) -> tuple[str, str, bool, bool, str] | None:
    file_path = Path(path)
    extension = file_path.suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        return None

    relative_parts = _path_parts(file_path, repo_root)
    normalized_name = file_path.name.lower()
    normalized_path = "/".join(relative_parts).lower()
    is_test = _is_test_file(relative_parts)
    is_generated = _is_generated_file(file_path, relative_parts)

    if is_test:
        return SourceType.TEST.value, _language_for_extension(extension), True, is_generated, "test path or filename pattern"
    if _is_api_contract(file_path, normalized_path):
        return (
            SourceType.API_CONTRACT.value,
            _language_for_extension(extension),
            False,
            is_generated,
            "API contract filename, folder, or extension",
        )
    if _is_migration(relative_parts, normalized_name):
        return SourceType.MIGRATION.value, _language_for_extension(extension), False, is_generated, "migration path or filename"
    if _is_schema(relative_parts, normalized_name, extension):
        return SourceType.SCHEMA.value, _language_for_extension(extension), False, is_generated, "schema path or SQL extension"
    if extension in CODE_EXTENSIONS:
        return SourceType.CODE.value, _language_for_extension(extension), False, is_generated, "code extension"
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
    return (
        path.suffix.lower() in CONTRACT_EXTENSIONS
        or "openapi" in name
        or "swagger" in name
        or "api_contract" in normalized_path
        or "api-contract" in normalized_path
    )


def _is_migration(parts: list[str], normalized_name: str) -> bool:
    lower_parts = [part.lower() for part in parts]
    return (
        "migrations" in lower_parts[:-1]
        or "migration" in lower_parts[:-1]
        or "alembic" in lower_parts[:-1]
        or "versions" in lower_parts[:-1]
        or "migration" in normalized_name
    )


def _is_schema(parts: list[str], normalized_name: str, extension: str) -> bool:
    lower_parts = [part.lower() for part in parts]
    return extension == ".sql" or "schema" in normalized_name or "schemas" in lower_parts[:-1]


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


def _language_for_extension(extension: str) -> str:
    return (
        CODE_EXTENSIONS.get(extension)
        or CONTRACT_EXTENSIONS.get(extension)
        or SCHEMA_EXTENSIONS.get(extension)
        or STRUCTURED_EXTENSIONS.get(extension)
        or "Unknown"
    )


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
