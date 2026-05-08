from dataclasses import asdict, dataclass, field
from enum import StrEnum

from app.schemas.common import SourceReference


class AnswerMode(StrEnum):
    DOCTRINE = "DOCTRINE"
    PRODUCT_DOMAIN = "PRODUCT_DOMAIN"
    TECHNICAL_SUPPORT = "TECHNICAL_SUPPORT"
    WORKER_FACING = "WORKER_FACING"
    DEVELOPER_PLATFORM = "DEVELOPER_PLATFORM"
    GENERAL = "GENERAL"


ANSWER_MODE_VALUES = {mode.value for mode in AnswerMode}


@dataclass(frozen=True)
class RichAnswerPlan:
    answer_mode: str
    direct_summary: str = ""
    system_operation_points: list[str] = field(default_factory=list)
    current_status_points: list[str] = field(default_factory=list)
    outstanding_points: list[str] = field(default_factory=list)
    evidence_points: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    source_references: list[SourceReference] = field(default_factory=list)

    def model_dump(self) -> dict:
        data = asdict(self)
        data["source_references"] = [source.model_dump() for source in self.source_references]
        return data


def normalize_answer_mode(value: str | None) -> str:
    normalized = (value or AnswerMode.GENERAL.value).upper()
    if normalized not in ANSWER_MODE_VALUES:
        raise ValueError(f"Invalid answer_mode '{value}'.")
    return normalized


def classify_answer_mode(question: str) -> str:
    normalized = " ".join(question.lower().replace("-", " ").split())

    if "minerva" in normalized and (
        "not allowed" in normalized
        or "boundary" in normalized
        or "boundaries" in normalized
        or "must not" in normalized
        or "cannot" in normalized
    ):
        return AnswerMode.DOCTRINE.value

    if "estimate my" in normalized or "my leave balance" in normalized or normalized.startswith("estimate "):
        return AnswerMode.WORKER_FACING.value

    if ("why is" in normalized or "why are" in normalized or "wrong" in normalized) and (
        "worker" in normalized or "leave balance" in normalized or "payrun" in normalized
    ):
        return AnswerMode.TECHNICAL_SUPPORT.value

    if (
        "hardening item" in normalized
        or "developer log" in normalized
        or "which log" in normalized
        or "source authority" in normalized
        or "platform memory" in normalized
    ):
        return AnswerMode.DEVELOPER_PLATFORM.value

    product_terms = (
        "annual leave",
        "leaveledger",
        "leave management",
        "payrun",
        "worker story",
        "rule cockpit",
        "leave rule",
        "leave rules",
    )
    if any(term in normalized for term in product_terms):
        return AnswerMode.PRODUCT_DOMAIN.value

    doctrine_terms = (
        "rbac before llm",
        "raw json",
        "separate database",
        "chat history override",
        "platform doctrine",
    )
    if any(term in normalized for term in doctrine_terms):
        return AnswerMode.DOCTRINE.value

    return AnswerMode.GENERAL.value
