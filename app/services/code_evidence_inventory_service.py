from dataclasses import asdict, dataclass, field
from enum import StrEnum
from pathlib import Path
import re


class CodeEvidenceTargetStatus(StrEnum):
    ACTIVE = "ACTIVE"
    REGISTERED_OPTIONAL = "REGISTERED_OPTIONAL"
    DEFERRED = "DEFERRED"
    UNAVAILABLE = "UNAVAILABLE"


class CodeEvidenceItemType(StrEnum):
    PYTHON_FILE = "PYTHON_FILE"
    TYPESCRIPT_FILE = "TYPESCRIPT_FILE"
    TEST_FILE = "TEST_FILE"
    ROUTE_DEFINITION = "ROUTE_DEFINITION"
    SERVICE_CLASS = "SERVICE_CLASS"
    FUNCTION = "FUNCTION"
    SCHEMA_CLASS = "SCHEMA_CLASS"
    PROMPT_ARTEFACT = "PROMPT_ARTEFACT"
    KNOWLEDGE_DOC = "KNOWLEDGE_DOC"
    EVALUATION_DOC = "EVALUATION_DOC"
    SLICE_KNOWLEDGE_DOC = "SLICE_KNOWLEDGE_DOC"
    UNKNOWN = "UNKNOWN"


EXCLUDED_DIR_NAMES = {
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "artifacts",
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
SENSITIVE_NAME_TOKENS = {
    "credential",
    "credentials",
    "secret",
    "secrets",
    "token",
    "tokens",
}
BINARY_EXTENSIONS = {
    ".7z",
    ".db",
    ".dll",
    ".dump",
    ".exe",
    ".gif",
    ".ico",
    ".jar",
    ".jpg",
    ".jpeg",
    ".pdf",
    ".pem",
    ".png",
    ".pyc",
    ".p12",
    ".pfx",
    ".sqlite",
    ".sqlite3",
    ".so",
    ".zip",
}
SUPPORTED_EXTENSIONS = {".md", ".py", ".ts", ".tsx"}
MAX_FILE_BYTES = 250_000

CLASS_RE = re.compile(r"^\s*class\s+([A-Za-z_][A-Za-z0-9_]*)", re.MULTILINE)
PY_FUNCTION_RE = re.compile(r"^\s*def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", re.MULTILINE)
TS_FUNCTION_RE = re.compile(
    r"(?:export\s+)?(?:async\s+)?function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\("
    r"|(?:export\s+)?const\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(?:async\s*)?\(",
    re.MULTILINE,
)
ROUTE_RE = re.compile(
    r"@(?:app|router|api_router)\.(?:get|post|put|patch|delete|options|head)\(\s*[\"']([^\"']+)[\"']"
    r"|(?:APIRouter|Router)\s*\([^)]*prefix\s*=\s*[\"']([^\"']+)[\"']",
    re.MULTILINE,
)


@dataclass(frozen=True)
class CodeEvidenceTarget:
    repo_name: str
    repo_family: str
    path: str
    status: CodeEvidenceTargetStatus
    disclosure_modes: list[str] = field(default_factory=list)
    allowed_roles: list[str] = field(default_factory=list)
    included_patterns: list[str] = field(default_factory=list)
    excluded_patterns: list[str] = field(default_factory=list)

    def model_dump(self) -> dict:
        payload = asdict(self)
        payload["status"] = self.status.value
        return payload


@dataclass(frozen=True)
class CodeEvidenceItem:
    repo_name: str
    repo_family: str
    file_path: str
    item_type: CodeEvidenceItemType
    symbol_name: str | None = None
    route_path: str | None = None
    test_name: str | None = None
    evidence_tags: list[str] = field(default_factory=list)
    raw_code_snippet: str | None = None

    def model_dump(self) -> dict:
        payload = asdict(self)
        payload["item_type"] = self.item_type.value
        return payload


@dataclass(frozen=True)
class CodeEvidenceInventory:
    targets: list[CodeEvidenceTarget]
    items: list[CodeEvidenceItem]
    excluded_paths: list[str] = field(default_factory=list)
    raw_code_snippets_included: bool = False
    read_only: bool = True
    database_access_performed: bool = False
    live_llm_calls_performed: bool = False
    code_execution_performed: bool = False
    repo_mutation_performed: bool = False

    def model_dump(self) -> dict:
        return {
            "targets": [target.model_dump() for target in self.targets],
            "items": [item.model_dump() for item in self.items],
            "excluded_paths": list(self.excluded_paths),
            "raw_code_snippets_included": self.raw_code_snippets_included,
            "read_only": self.read_only,
            "database_access_performed": self.database_access_performed,
            "live_llm_calls_performed": self.live_llm_calls_performed,
            "code_execution_performed": self.code_execution_performed,
            "repo_mutation_performed": self.repo_mutation_performed,
        }


class CodeEvidenceInventoryService:
    def __init__(self, repo_root: str | Path | None = None) -> None:
        self.repo_root = Path(repo_root or Path(__file__).resolve().parents[2]).resolve()

    def default_target_registry(self) -> list[CodeEvidenceTarget]:
        project_root = self.repo_root.parent
        ezeas_intelligence = self.repo_root
        workforce_platform = project_root / "workforce-platform"
        award_configurator = project_root / "award-configurator-v1"
        analytics = project_root / "ezeas-analytics"
        return [
            self._target("ezeas-intelligence", "MINERVA", ezeas_intelligence, active_if_exists=True),
            self._target("workforce-platform", "WORKFORCE_PLATFORM", workforce_platform, active_if_exists=True),
            self._target("award-configurator-v1", "AWARD_CONFIGURATOR", award_configurator, active_if_exists=True),
            CodeEvidenceTarget(
                repo_name="ezeas-analytics",
                repo_family="ANALYTICS",
                path=str(analytics),
                status=CodeEvidenceTargetStatus.REGISTERED_OPTIONAL,
                disclosure_modes=[
                    "TECHNICAL_DISCLOSURE",
                    "IMPLEMENTATION_CONFIRMATION",
                    "BACKGROUND_CONFIDENCE_ONLY",
                ],
                allowed_roles=["DEVELOPER", "PAYROLL_ADMINISTRATOR", "CUSTOMER_ADMINISTRATOR"],
                included_patterns=["docs/**/*.md", "src/**/*.py", "src/**/*.ts", "tests/**/*.py"],
                excluded_patterns=sorted(EXCLUDED_DIR_NAMES | SENSITIVE_NAME_TOKENS),
            ),
        ]

    def build_inventory(
        self,
        targets: list[CodeEvidenceTarget] | None = None,
        include_raw_code_snippets: bool = False,
    ) -> CodeEvidenceInventory:
        registry = list(targets or self.default_target_registry())
        items: list[CodeEvidenceItem] = []
        excluded_paths: list[str] = []
        for target in registry:
            if target.status != CodeEvidenceTargetStatus.ACTIVE:
                continue
            root = Path(target.path)
            if not root.exists() or not root.is_dir():
                continue
            target_items, target_excluded = self.inventory_target(target, include_raw_code_snippets)
            items.extend(target_items)
            excluded_paths.extend(target_excluded)
        return CodeEvidenceInventory(
            targets=registry,
            items=sorted(items, key=lambda item: (item.repo_name, item.file_path, item.item_type.value, item.symbol_name or "")),
            excluded_paths=sorted(excluded_paths),
            raw_code_snippets_included=include_raw_code_snippets and any(item.raw_code_snippet for item in items),
        )

    def inventory_target(
        self,
        target: CodeEvidenceTarget,
        include_raw_code_snippets: bool = False,
    ) -> tuple[list[CodeEvidenceItem], list[str]]:
        root = Path(target.path).resolve()
        if not root.exists() or not root.is_dir():
            unavailable_target = CodeEvidenceTarget(
                **{**target.model_dump(), "status": CodeEvidenceTargetStatus.UNAVAILABLE.value}
            )
            return [], [f"{unavailable_target.repo_name}:UNAVAILABLE"]
        items: list[CodeEvidenceItem] = []
        excluded_paths: list[str] = []
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            relative_path = path.relative_to(root).as_posix()
            reason = self.exclusion_reason(path, root)
            if reason:
                excluded_paths.append(f"{target.repo_name}:{relative_path}:{reason}")
                continue
            if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue
            text = _read_text(path)
            if text is None:
                excluded_paths.append(f"{target.repo_name}:{relative_path}:unreadable_or_binary")
                continue
            items.extend(_items_for_file(target, relative_path, path, text, include_raw_code_snippets))
        return items, excluded_paths

    def available_target_registry(self) -> list[CodeEvidenceTarget]:
        return [
            self._target(
                target.repo_name,
                target.repo_family,
                Path(target.path),
                active_if_exists=target.status == CodeEvidenceTargetStatus.ACTIVE,
            )
            if target.status != CodeEvidenceTargetStatus.REGISTERED_OPTIONAL
            else target
            for target in self.default_target_registry()
        ]

    def exclusion_reason(self, path: Path, repo_root: Path) -> str | None:
        relative_parts = [part.lower() for part in path.resolve().relative_to(repo_root.resolve()).parts]
        name = path.name.lower()
        stem = path.stem.lower()
        if any(part in EXCLUDED_DIR_NAMES for part in relative_parts[:-1]):
            return "excluded_directory"
        if name == ".env" or name.startswith(".env."):
            return "environment_file"
        if any(token in stem for token in SENSITIVE_NAME_TOKENS):
            return "sensitive_name"
        if path.suffix.lower() in BINARY_EXTENSIONS:
            return "binary_file"
        try:
            if path.stat().st_size > MAX_FILE_BYTES:
                return "large_file"
        except OSError:
            return "unreadable"
        return None

    def _target(self, repo_name: str, repo_family: str, path: Path, active_if_exists: bool) -> CodeEvidenceTarget:
        status = CodeEvidenceTargetStatus.ACTIVE if active_if_exists and path.exists() else CodeEvidenceTargetStatus.UNAVAILABLE
        return CodeEvidenceTarget(
            repo_name=repo_name,
            repo_family=repo_family,
            path=str(path),
            status=status,
            disclosure_modes=[
                "TECHNICAL_DISCLOSURE",
                "IMPLEMENTATION_CONFIRMATION",
                "BACKGROUND_CONFIDENCE_ONLY",
            ],
            allowed_roles=["DEVELOPER", "PAYROLL_ADMINISTRATOR", "PAYROLL_USER", "CUSTOMER_ADMINISTRATOR"],
            included_patterns=["**/*.py", "**/*.ts", "**/*.tsx", "docs/**/*.md", "tests/**/*.py"],
            excluded_patterns=sorted(EXCLUDED_DIR_NAMES | SENSITIVE_NAME_TOKENS),
        )


def _items_for_file(
    target: CodeEvidenceTarget,
    relative_path: str,
    path: Path,
    text: str,
    include_raw_code_snippets: bool,
) -> list[CodeEvidenceItem]:
    item_type = _file_item_type(relative_path, path)
    snippet = text[:500] if include_raw_code_snippets else None
    tags = _tags_for_file(relative_path, item_type)
    items = [
        CodeEvidenceItem(
            repo_name=target.repo_name,
            repo_family=target.repo_family,
            file_path=relative_path,
            item_type=item_type,
            evidence_tags=tags,
            raw_code_snippet=snippet,
        )
    ]
    if path.suffix.lower() == ".py":
        items.extend(_python_symbol_items(target, relative_path, text))
    if path.suffix.lower() in {".ts", ".tsx"}:
        items.extend(_typescript_symbol_items(target, relative_path, text))
    for route_path in _detect_routes(text):
        items.append(
            CodeEvidenceItem(
                repo_name=target.repo_name,
                repo_family=target.repo_family,
                file_path=relative_path,
                item_type=CodeEvidenceItemType.ROUTE_DEFINITION,
                route_path=route_path,
                evidence_tags=["route_definition", "implementation_support"],
            )
        )
    return items


def _python_symbol_items(target: CodeEvidenceTarget, relative_path: str, text: str) -> list[CodeEvidenceItem]:
    items: list[CodeEvidenceItem] = []
    for class_name in CLASS_RE.findall(text):
        if class_name.endswith("Service"):
            item_type = CodeEvidenceItemType.SERVICE_CLASS
            tags = ["service_class", "implementation_support"]
        elif class_name.endswith(("Schema", "Model", "Request", "Response")):
            item_type = CodeEvidenceItemType.SCHEMA_CLASS
            tags = ["schema_class", "implementation_support"]
        else:
            continue
        items.append(
            CodeEvidenceItem(
                repo_name=target.repo_name,
                repo_family=target.repo_family,
                file_path=relative_path,
                item_type=item_type,
                symbol_name=class_name,
                evidence_tags=tags,
            )
        )
    for function_name in PY_FUNCTION_RE.findall(text):
        if function_name.startswith("test_"):
            items.append(
                CodeEvidenceItem(
                    repo_name=target.repo_name,
                    repo_family=target.repo_family,
                    file_path=relative_path,
                    item_type=CodeEvidenceItemType.TEST_FILE,
                    symbol_name=function_name,
                    test_name=function_name,
                    evidence_tags=["test_function", "behavioural_evidence"],
                )
            )
        else:
            items.append(
                CodeEvidenceItem(
                    repo_name=target.repo_name,
                    repo_family=target.repo_family,
                    file_path=relative_path,
                    item_type=CodeEvidenceItemType.FUNCTION,
                    symbol_name=function_name,
                    evidence_tags=["function", "implementation_support"],
                )
            )
    return items


def _typescript_symbol_items(target: CodeEvidenceTarget, relative_path: str, text: str) -> list[CodeEvidenceItem]:
    items: list[CodeEvidenceItem] = []
    for match in TS_FUNCTION_RE.findall(text):
        function_name = next(name for name in match if name)
        items.append(
            CodeEvidenceItem(
                repo_name=target.repo_name,
                repo_family=target.repo_family,
                file_path=relative_path,
                item_type=CodeEvidenceItemType.FUNCTION,
                symbol_name=function_name,
                evidence_tags=["function", "ui_or_typescript_reference", "implementation_support"],
            )
        )
    return items


def _file_item_type(relative_path: str, path: Path) -> CodeEvidenceItemType:
    lower_path = relative_path.lower()
    suffix = path.suffix.lower()
    if lower_path.startswith("docs/codex_prompts/") and suffix == ".md":
        return CodeEvidenceItemType.PROMPT_ARTEFACT
    if lower_path.startswith("docs/evaluation/") and suffix == ".md":
        return CodeEvidenceItemType.EVALUATION_DOC
    if lower_path.startswith("docs/knowledge/") and lower_path.endswith("_source_response.md"):
        return CodeEvidenceItemType.SLICE_KNOWLEDGE_DOC
    if lower_path.startswith("docs/knowledge/") and suffix == ".md":
        return CodeEvidenceItemType.KNOWLEDGE_DOC
    if _is_test_path(lower_path):
        return CodeEvidenceItemType.TEST_FILE
    if suffix == ".py":
        return CodeEvidenceItemType.PYTHON_FILE
    if suffix in {".ts", ".tsx"}:
        return CodeEvidenceItemType.TYPESCRIPT_FILE
    return CodeEvidenceItemType.UNKNOWN


def _tags_for_file(relative_path: str, item_type: CodeEvidenceItemType) -> list[str]:
    tags = ["code_evidence", "metadata_only"]
    if item_type == CodeEvidenceItemType.TEST_FILE:
        tags.append("test_evidence")
    if item_type in {
        CodeEvidenceItemType.KNOWLEDGE_DOC,
        CodeEvidenceItemType.SLICE_KNOWLEDGE_DOC,
        CodeEvidenceItemType.EVALUATION_DOC,
        CodeEvidenceItemType.PROMPT_ARTEFACT,
    }:
        tags.append("minerva_document")
    if "ui" in relative_path.lower() or relative_path.lower().endswith((".ts", ".tsx")):
        tags.append("ui_reference")
    return tags


def _detect_routes(text: str) -> list[str]:
    routes = []
    for match in ROUTE_RE.findall(text):
        route_path = match[0] or match[1]
        if route_path:
            routes.append(route_path)
    return sorted(set(routes))


def _is_test_path(lower_path: str) -> bool:
    name = lower_path.rsplit("/", 1)[-1]
    return (
        lower_path.startswith("tests/")
        or "/tests/" in lower_path
        or name.startswith("test_")
        or name.endswith("_test.py")
        or ".test." in name
        or ".spec." in name
    )


def _read_text(path: Path) -> str | None:
    try:
        content = path.read_bytes()
    except OSError:
        return None
    if b"\0" in content:
        return None
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        return None
