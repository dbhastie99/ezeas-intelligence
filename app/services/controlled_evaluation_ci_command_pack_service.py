import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any


COMMAND_PACK_TYPE = "CONTROLLED_EVALUATION_CI_COMMAND_PACK"

NO_ACTION_ATTESTATION = (
    "No runtime, exposure, endpoint, DB, corpus, Code Evidence, live LLM, final "
    "answer generation, UI, deployment, production, migration, credential, or "
    "cross-repo runtime action is authorised by this command pack metadata."
)


@dataclass(frozen=True)
class ControlledEvaluationCiCommandPackResult:
    command_pack_id: str
    command_pack_type: str
    commands: tuple[dict[str, str], ...]
    expected_outputs: tuple[str, ...]
    stop_conditions: tuple[str, ...]
    prohibited_commands: tuple[str, ...]
    safe_for_local_execution: bool
    safe_for_final_answer_generation: bool
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_controlled_evaluation_ci_command_pack() -> dict[str, Any]:
    commands = (
        {
            "command_id": "focused-batch-harness-tests",
            "shell": "PowerShell",
            "command": (
                "python -m pytest tests\\test_controlled_evaluation_batch_harness_service.py"
            ),
        },
        {
            "command_id": "focused-golden-baseline-tests",
            "shell": "PowerShell",
            "command": (
                "python -m pytest tests\\test_controlled_evaluation_report_golden_baselines.py"
            ),
        },
        {
            "command_id": "focused-summary-export-tests",
            "shell": "PowerShell",
            "command": (
                "python -m pytest "
                "tests\\test_controlled_evaluation_summary_export_service.py "
                "tests\\test_controlled_evaluation_ci_command_pack_service.py"
            ),
        },
        {
            "command_id": "compile-deterministic-services",
            "shell": "PowerShell",
            "command": (
                "python -m py_compile "
                "app\\services\\controlled_evaluation_batch_harness_service.py "
                "app\\services\\controlled_evaluation_batch_summary_service.py "
                "app\\services\\controlled_evaluation_summary_export_service.py "
                "app\\services\\controlled_evaluation_ci_command_pack_service.py"
            ),
        },
        {
            "command_id": "diff-whitespace-check",
            "shell": "PowerShell",
            "command": "git diff --check",
        },
        {
            "command_id": "pytest-temp-absence-check",
            "shell": "PowerShell",
            "command": (
                "if (Test-Path .pytest_tmp) { throw '.pytest_tmp exists' } "
                "else { Write-Output '.pytest_tmp absent' }"
            ),
        },
    )
    expected_outputs = (
        "Focused pytest commands complete without failures.",
        "py_compile completes without syntax errors.",
        "git diff --check reports no whitespace errors.",
        ".pytest_tmp absence check reports .pytest_tmp absent.",
    )
    stop_conditions = (
        "Stop on any focused pytest failure.",
        "Stop on any py_compile failure.",
        "Stop on any git diff --check failure.",
        "Stop if .pytest_tmp exists after command execution.",
    )
    prohibited_commands = (
        "Database access, migration, validation, read, or write commands.",
        "Live LLM, chat, endpoint, route, or final-answer-generation commands.",
        "Corpus mutation or Code Evidence ingestion commands.",
        "workforce-platform or ezeas-analytics runtime commands.",
    )
    material = {
        "command_pack_type": COMMAND_PACK_TYPE,
        "commands": commands,
        "expected_outputs": expected_outputs,
        "stop_conditions": stop_conditions,
        "prohibited_commands": prohibited_commands,
    }

    return ControlledEvaluationCiCommandPackResult(
        command_pack_id=_command_pack_id(material),
        command_pack_type=COMMAND_PACK_TYPE,
        commands=commands,
        expected_outputs=expected_outputs,
        stop_conditions=stop_conditions,
        prohibited_commands=prohibited_commands,
        safe_for_local_execution=True,
        safe_for_final_answer_generation=False,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=(
            "PowerShell-only deterministic local regression command metadata for "
            "controlled evaluation summaries and golden baseline checks."
        ),
    ).to_dict()


def _command_pack_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    digest = hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:16]
    return f"controlled-evaluation-ci-command-pack-{digest}"
