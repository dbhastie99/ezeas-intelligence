from pathlib import Path
import shutil
from uuid import uuid4

import pytest

from app.services.code_evidence_inventory_service import (
    CodeEvidenceInventoryService,
    CodeEvidenceItemType,
    CodeEvidenceTarget,
    CodeEvidenceTargetStatus,
)


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def workspace_tmp(request):
    root = ROOT / "artifacts" / "test_tmp" / f"{request.node.name}_{uuid4().hex}"
    root.mkdir(parents=True, exist_ok=True)
    try:
        yield root
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _write(path: Path, content: str = "content") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _target(root: Path, repo_name: str = "sample") -> CodeEvidenceTarget:
    return CodeEvidenceTarget(
        repo_name=repo_name,
        repo_family="SAMPLE",
        path=str(root),
        status=CodeEvidenceTargetStatus.ACTIVE,
        disclosure_modes=["TECHNICAL_DISCLOSURE"],
        allowed_roles=["DEVELOPER"],
        included_patterns=["**/*.py", "**/*.ts", "**/*.tsx", "docs/**/*.md"],
        excluded_patterns=[],
    )


def test_default_target_registry_includes_required_repo_families():
    registry = CodeEvidenceInventoryService().default_target_registry()
    names = {target.repo_name for target in registry}

    assert names == {
        "ezeas-intelligence",
        "workforce-platform",
        "award-configurator-v1",
        "ezeas-analytics",
    }


def test_ezeas_analytics_is_registered_but_optional_by_default():
    registry = CodeEvidenceInventoryService().default_target_registry()
    analytics = next(target for target in registry if target.repo_name == "ezeas-analytics")

    assert analytics.repo_family == "ANALYTICS"
    assert analytics.status == CodeEvidenceTargetStatus.REGISTERED_OPTIONAL


def test_missing_external_repo_paths_do_not_fail_and_become_unavailable(workspace_tmp):
    service = CodeEvidenceInventoryService(repo_root=workspace_tmp / "ezeas-intelligence")
    registry = service.default_target_registry()
    by_name = {target.repo_name: target for target in registry}

    assert by_name["workforce-platform"].status == CodeEvidenceTargetStatus.UNAVAILABLE
    assert by_name["award-configurator-v1"].status == CodeEvidenceTargetStatus.UNAVAILABLE
    inventory = service.build_inventory(registry)
    assert inventory.items == []


def test_inventory_excludes_sensitive_cache_dependency_and_build_paths(workspace_tmp):
    for relative in [
        ".env",
        "node_modules/pkg/index.ts",
        ".venv/Lib/site.py",
        "__pycache__/module.py",
        ".pytest_cache/v/cache/nodeids",
        "dist/bundle.ts",
        "build/output.ts",
    ]:
        _write(workspace_tmp / relative, "SECRET = 'x'")
    _write(workspace_tmp / "src" / "service.py", "class SampleService:\n    pass\n")

    inventory = CodeEvidenceInventoryService().build_inventory([_target(workspace_tmp)])

    assert [item.file_path for item in inventory.items if item.item_type == CodeEvidenceItemType.PYTHON_FILE] == [
        "src/service.py"
    ]
    excluded = " ".join(inventory.excluded_paths)
    assert ".env" in excluded
    assert "node_modules" in excluded
    assert ".venv" in excluded
    assert "__pycache__" in excluded
    assert ".pytest_cache" in excluded


def test_inventory_detects_service_class_function_and_test_names(workspace_tmp):
    _write(
        workspace_tmp / "app" / "services" / "sample_service.py",
        "\n".join(
            [
                "class PayrollEvidenceService:",
                "    pass",
                "",
                "class PayrollEvidenceSchema:",
                "    pass",
                "",
                "def build_inventory():",
                "    return []",
            ]
        ),
    )
    _write(
        workspace_tmp / "tests" / "test_sample_service.py",
        "def test_detects_named_behaviour():\n    assert True\n",
    )

    inventory = CodeEvidenceInventoryService().build_inventory([_target(workspace_tmp)])
    items = inventory.items

    assert any(item.item_type == CodeEvidenceItemType.SERVICE_CLASS and item.symbol_name == "PayrollEvidenceService" for item in items)
    assert any(item.item_type == CodeEvidenceItemType.SCHEMA_CLASS and item.symbol_name == "PayrollEvidenceSchema" for item in items)
    assert any(item.item_type == CodeEvidenceItemType.FUNCTION and item.symbol_name == "build_inventory" for item in items)
    assert any(item.item_type == CodeEvidenceItemType.TEST_FILE and item.test_name == "test_detects_named_behaviour" for item in items)


def test_inventory_detects_route_like_strings_from_fastapi_router_files(workspace_tmp):
    _write(
        workspace_tmp / "app" / "routes" / "payroll.py",
        "\n".join(
            [
                "from fastapi import APIRouter",
                "router = APIRouter(prefix='/payroll')",
                "",
                "@router.post('/payruns/{payrun_id}/process')",
                "def process_payrun(payrun_id: str):",
                "    return {'ok': True}",
            ]
        ),
    )

    inventory = CodeEvidenceInventoryService().build_inventory([_target(workspace_tmp)])
    routes = {item.route_path for item in inventory.items if item.item_type == CodeEvidenceItemType.ROUTE_DEFINITION}

    assert "/payroll" in routes
    assert "/payruns/{payrun_id}/process" in routes


def test_inventory_records_prompt_artefacts_and_knowledge_docs(workspace_tmp):
    _write(workspace_tmp / "docs" / "codex_prompts" / "2026-05-21_prompt.md", "# Prompt")
    _write(workspace_tmp / "docs" / "knowledge" / "slice_v0_1.md", "# Knowledge")
    _write(workspace_tmp / "docs" / "knowledge" / "slice_v0_1_source_response.md", "# Source")
    _write(workspace_tmp / "docs" / "evaluation" / "slice" / "ANSWER_EVALUATION_BASELINE.md", "# Eval")

    inventory = CodeEvidenceInventoryService().build_inventory([_target(workspace_tmp)])
    types = {item.file_path: item.item_type for item in inventory.items}

    assert types["docs/codex_prompts/2026-05-21_prompt.md"] == CodeEvidenceItemType.PROMPT_ARTEFACT
    assert types["docs/knowledge/slice_v0_1.md"] == CodeEvidenceItemType.KNOWLEDGE_DOC
    assert types["docs/knowledge/slice_v0_1_source_response.md"] == CodeEvidenceItemType.SLICE_KNOWLEDGE_DOC
    assert types["docs/evaluation/slice/ANSWER_EVALUATION_BASELINE.md"] == CodeEvidenceItemType.EVALUATION_DOC


def test_raw_code_snippets_are_not_included_by_default(workspace_tmp):
    _write(workspace_tmp / "src" / "service.py", "def calculate():\n    return 1\n")

    inventory = CodeEvidenceInventoryService().build_inventory([_target(workspace_tmp)])

    assert inventory.raw_code_snippets_included is False
    assert all(item.raw_code_snippet is None for item in inventory.items)


def test_inventory_is_read_only_and_does_not_mutate_files(workspace_tmp):
    source = workspace_tmp / "src" / "service.py"
    _write(source, "def calculate():\n    return 1\n")
    before_content = source.read_text(encoding="utf-8")
    before_files = sorted(path.relative_to(workspace_tmp).as_posix() for path in workspace_tmp.rglob("*"))

    inventory = CodeEvidenceInventoryService().build_inventory([_target(workspace_tmp)])

    after_content = source.read_text(encoding="utf-8")
    after_files = sorted(path.relative_to(workspace_tmp).as_posix() for path in workspace_tmp.rglob("*"))
    assert inventory.read_only is True
    assert inventory.repo_mutation_performed is False
    assert after_content == before_content
    assert after_files == before_files
