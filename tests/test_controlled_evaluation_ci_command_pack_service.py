from app.services.controlled_evaluation_ci_command_pack_service import (
    build_controlled_evaluation_ci_command_pack,
)


PROHIBITED_COMMAND_TERMS = (
    "psql",
    "sqlcmd",
    "alembic",
    "migrate",
    "openai",
    "llm",
    "chat",
    "uvicorn",
    "fastapi",
    "route",
    "endpoint",
    "corpus",
    "ingest",
    "code evidence",
    "workforce-platform",
    "ezeas-analytics",
    "final answer",
)


def _pack():
    return build_controlled_evaluation_ci_command_pack()


def _commands_text(pack):
    return "\n".join(command["command"].lower() for command in pack["commands"])


def test_command_pack_uses_powershell_syntax_only():
    pack = _pack()

    assert all(command["shell"] == "PowerShell" for command in pack["commands"])
    assert all("&&" not in command["command"] for command in pack["commands"])


def test_includes_focused_batch_harness_test_command():
    assert (
        "python -m pytest tests\\test_controlled_evaluation_batch_harness_service.py"
        in _commands_text(_pack())
    )


def test_includes_golden_baselines_test_command():
    assert (
        "python -m pytest tests\\test_controlled_evaluation_report_golden_baselines.py"
        in _commands_text(_pack())
    )


def test_includes_py_compile_commands_for_relevant_deterministic_services():
    commands = _commands_text(_pack())

    assert "python -m py_compile" in commands
    assert "app\\services\\controlled_evaluation_batch_harness_service.py" in commands
    assert "app\\services\\controlled_evaluation_batch_summary_service.py" in commands
    assert "app\\services\\controlled_evaluation_summary_export_service.py" in commands
    assert "app\\services\\controlled_evaluation_ci_command_pack_service.py" in commands


def test_includes_git_diff_check_command():
    assert "git diff --check" in _commands_text(_pack())


def test_includes_pytest_tmp_check_command():
    assert "test-path .pytest_tmp" in _commands_text(_pack())


def test_excludes_db_commands():
    commands = _commands_text(_pack())

    assert "psql" not in commands
    assert "sqlcmd" not in commands
    assert "alembic" not in commands
    assert "migrate" not in commands


def test_excludes_live_llm_commands():
    commands = _commands_text(_pack())

    assert "openai" not in commands
    assert "llm" not in commands


def test_excludes_chat_endpoint_and_route_commands():
    commands = _commands_text(_pack())

    assert "chat" not in commands
    assert "endpoint" not in commands
    assert "route" not in commands
    assert "uvicorn" not in commands


def test_excludes_corpus_mutation_commands():
    assert "corpus" not in _commands_text(_pack())


def test_excludes_code_evidence_ingestion_commands():
    commands = _commands_text(_pack())

    assert "code evidence" not in commands
    assert "ingest" not in commands


def test_excludes_workforce_platform_or_analytics_runtime_commands():
    commands = _commands_text(_pack())

    assert "workforce-platform" not in commands
    assert "ezeas-analytics" not in commands


def test_excludes_final_answer_generation_commands():
    assert "final answer" not in _commands_text(_pack())


def test_command_pack_is_never_safe_for_final_answer_generation():
    assert _pack()["safe_for_final_answer_generation"] is False


def test_output_is_deterministic_for_repeated_input():
    assert _pack() == _pack()
