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

    if (
        "payg withholding" in normalized
        or "tax / payg" in normalized
        or "tax payg" in normalized
        or "taxstory" in normalized
        or "tax story" in normalized
    ):
        return AnswerMode.PRODUCT_DOMAIN.value

    if (
        "retro replay" in normalized
        or "retro / replay" in normalized
        or "retro payrun" in normalized
        or "retro pay run" in normalized
        or "attributed period" in normalized
        or "paid period" in normalized
        or "finalised outcome memory" in normalized
        or "finalized outcome memory" in normalized
        or "dependency detection" in normalized
        or "historical bucket evidence" in normalized
        or "correction replay" in normalized
    ):
        return AnswerMode.PRODUCT_DOMAIN.value

    if (
        "deductions obligations" in normalized
        or "deductions / obligations" in normalized
        or "deductions and obligations" in normalized
        or "deduction and obligation" in normalized
        or ("deduction" in normalized and "obligation" in normalized)
        or "deduction template chain" in normalized
        or "payrundeductionapplication" in normalized
        or "payrun deduction application" in normalized
        or "supplementary payruns" in normalized and "deduction memory" in normalized
        or "applicability before affordability" in normalized
        or "reducing balance recovery" in normalized
        or "negative net pay" in normalized
    ):
        return AnswerMode.PRODUCT_DOMAIN.value

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
        "deductions obligations",
        "deductions / obligations",
        "deductions and obligations",
        "deduction and obligation",
        "deduction template chain",
        "deduction memory",
        "librarydeductiontemplate",
        "library deduction template",
        "accountdeductiontemplate",
        "account deduction template",
        "contactpayrolldeduction",
        "contact payroll deduction",
        "payrundeductionapplication",
        "payrun deduction application",
        "contactpayrollobligation",
        "contact payroll obligation",
        "contactpayrollobligationledger",
        "contact payroll obligation ledger",
        "supplementary deduction memory",
        "reducing balance recovery",
        "reducing-balance recovery",
        "carry forward",
        "carry-forward",
        "applicability before affordability",
        "negative net pay",
        "retro replay",
        "retro / replay",
        "retro payrun",
        "retro pay run",
        "attributed period",
        "paid period",
        "finalised outcome memory",
        "finalized outcome memory",
        "dependency detection",
        "bucket rebuild",
        "historical bucket evidence",
        "correction replay",
        "payrun",
        "worker story",
        "worker calculation story",
        "talking payslip",
        "source truth",
        "sourcetruth",
        "calculated payroll outcome",
        "decision story",
        "rate story",
        "payroll bases",
        "payroll bases and totals",
        "payrollbucketresult",
        "payroll bucket result",
        "payrollbucketdefinition",
        "payroll bucket definition",
        "movement review",
        "payroll movement review",
        "review-worthy",
        "reasonableness",
        "comparable period",
        "current period blockers",
        "current-period blockers",
        "rolling",
        "rolling average",
        "trend only",
        "trend-only",
        "ytd",
        "comparison remediation",
        "comparison / remediation",
        "award comparison",
        "payruncomparisonrun",
        "payrun comparison run",
        "payruncomparisonline",
        "payrun comparison line",
        "payrunvarianceline",
        "payrun variance line",
        "awardcomparisonpolicy",
        "award comparison policy",
        "comparator award",
        "comparator classification",
        "comparison evidence",
        "comparison lane",
        "primary award path",
        "imported actuals",
        "actuals lane",
        "remediation top-up",
        "remediation top up",
        "ordinary manual adjustment",
        "ordinary manual adjustments",
        "tax payg",
        "tax / payg",
        "payg",
        "payg withholding",
        "taxstory",
        "tax story",
        "taxable basis",
        "taxable earnings",
        "worker tax declaration",
        "withholding instruction",
        "processperiod paymentdate",
        "payment date",
        "pay frequency",
        "gross to net",
        "gross-to-net",
        "finalised totals",
        "supplementary incremental payg",
        "admin queue",
        "payrun admin queue",
        "payrun queue",
        "worker attention",
        "dirty contacts",
        "finalisation readiness",
        "assurance snapshot",
        "command centre",
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
