import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evidence_intake_dry_run_service import (
    DRY_RUN_BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT,
    DRY_RUN_BLOCKED_UNAUTHORISED_INGESTION_CLAIM,
    DRY_RUN_READY_FOR_FUTURE_INTAKE,
    NO_ACTION_ATTESTATION,
)


RECOMMENDED_NEXT_SLICE = (
    "Controlled evidence intake review ledger / no-corpus-mutation v0.1."
)

EXECUTION_FLAG_FIELDS = (
    "ingestion_performed",
    "corpus_mutation_performed",
    "code_evidence_ingestion_performed",
    "db_write_performed",
    "live_retrieval_performed",
    "live_llm_performed",
    "final_answer_generation_performed",
)


@dataclass(frozen=True)
class ControlledEvidenceIntakeDryRunSummaryResult:
    summary_id: str
    dry_run_count: int
    ready_count: int
    needs_review_count: int
    blocked_count: int
    all_non_mutating: bool
    ingestion_performed_any: bool
    corpus_mutation_performed_any: bool
    code_evidence_ingestion_performed_any: bool
    db_write_performed_any: bool
    runtime_or_production_overstatement_count: int
    unauthorised_ingestion_claim_count: int
    recommended_next_slice: str
    required_caveats: tuple[str, ...]
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def summarize_controlled_evidence_intake_dry_runs(
    dry_run_results: Any,
    *,
    recommended_next_slice: str = RECOMMENDED_NEXT_SLICE,
) -> dict[str, Any]:
    results = tuple(dict(result) for result in _as_tuple(dry_run_results))
    flag_state = {field: any(bool(result.get(field)) for result in results) for field in EXECUTION_FLAG_FIELDS}
    all_non_mutating = not any(flag_state.values())
    blocked_count = sum(1 for result in results if _is_blocked(result))
    ready_count = sum(
        1
        for result in results
        if result.get("dry_run_decision") == DRY_RUN_READY_FOR_FUTURE_INTAKE
        and _result_non_mutating(result)
    )
    needs_review_count = len(results) - ready_count - blocked_count
    runtime_count = sum(
        1
        for result in results
        if result.get("dry_run_decision")
        == DRY_RUN_BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    )
    ingestion_count = sum(
        1
        for result in results
        if result.get("dry_run_decision") == DRY_RUN_BLOCKED_UNAUTHORISED_INGESTION_CLAIM
    )
    caveats = _dedupe(
        caveat
        for result in results
        for caveat in _as_tuple(result.get("required_caveats"))
    )

    material = {
        "results": results,
        "ready_count": ready_count,
        "needs_review_count": needs_review_count,
        "blocked_count": blocked_count,
        "all_non_mutating": all_non_mutating,
        "recommended_next_slice": recommended_next_slice,
        "required_caveats": caveats,
    }

    return ControlledEvidenceIntakeDryRunSummaryResult(
        summary_id=_summary_id(material),
        dry_run_count=len(results),
        ready_count=ready_count,
        needs_review_count=needs_review_count,
        blocked_count=blocked_count,
        all_non_mutating=all_non_mutating,
        ingestion_performed_any=flag_state["ingestion_performed"],
        corpus_mutation_performed_any=flag_state["corpus_mutation_performed"],
        code_evidence_ingestion_performed_any=flag_state["code_evidence_ingestion_performed"],
        db_write_performed_any=flag_state["db_write_performed"],
        runtime_or_production_overstatement_count=runtime_count,
        unauthorised_ingestion_claim_count=ingestion_count,
        recommended_next_slice=recommended_next_slice,
        required_caveats=caveats,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(all_non_mutating, blocked_count, needs_review_count),
    ).to_dict()


def build_controlled_evidence_intake_dry_run_summary(
    dry_run_results: Any,
    **metadata: Any,
) -> dict[str, Any]:
    return summarize_controlled_evidence_intake_dry_runs(dry_run_results, **metadata)


def _is_blocked(result: dict[str, Any]) -> bool:
    return str(result.get("dry_run_decision", "")).startswith("DRY_RUN_BLOCKED")


def _result_non_mutating(result: dict[str, Any]) -> bool:
    return not any(bool(result.get(field)) for field in EXECUTION_FLAG_FIELDS)


def _as_tuple(value: Any) -> tuple[Any, ...]:
    if value is None or value == "":
        return ()
    if isinstance(value, tuple):
        return value
    if isinstance(value, list):
        return tuple(value)
    if isinstance(value, set):
        return tuple(sorted(value))
    return (value,)


def _dedupe(values: Any) -> tuple[str, ...]:
    return tuple(dict.fromkeys(str(item) for item in values if str(item)))


def _summary_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "controlled-evidence-intake-dry-run-summary-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]


def _explanation(
    all_non_mutating: bool,
    blocked_count: int,
    needs_review_count: int,
) -> str:
    if all_non_mutating and blocked_count == 0 and needs_review_count == 0:
        return (
            "All dry-run results are non-mutating and ready for a future governed "
            "intake decision; ingestion and corpus mutation remain unauthorised."
        )
    if not all_non_mutating:
        return (
            "One or more dry-run results reported a prohibited execution or mutation "
            "flag; the batch requires review and authorises no ingestion."
        )
    return (
        "The batch contains review or blocked dry-run results; no ingestion or corpus "
        "mutation is authorised."
    )
