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
    payroll_output_framed = (
        normalized.startswith("how does payroll output")
        or normalized.startswith("how should payroll output")
        or normalized.startswith("what does current effective payroll output")
        or normalized.startswith("what is the difference between run output and process period output")
        or "payroll output relate" in normalized
        or "payroll output explain" in normalized
    )
    if (
        "worker attention / issue resolution" in normalized
        or "worker attention issue resolution" in normalized
        or "issue resolution" in normalized and "worker" in normalized
        or "worker attention centre" in normalized
        or "workerattention" in normalized and ("issue" in normalized or "resolution" in normalized)
        or "worker issue" in normalized and ("resolution" in normalized or "surface" in normalized or "platform" in normalized)
        or "worker attention" in normalized and (
            "model worker issue" in normalized
            or "worker issues" in normalized
            or "fix an issue" in normalized
            or "guide users" in normalized
            or "dirty contact state" in normalized
            or "payment allocation" in normalized
            or "negative net pay" in normalized
            or ("admin queue" in normalized and "worker story" in normalized and "relate" in normalized)
        )
    ):
        return AnswerMode.PRODUCT_DOMAIN.value
    if (
        "ratesource / rate story" in normalized
        or "ratesource rate story" in normalized
        or "rate source / rate story" in normalized
        or "rate source rate story" in normalized
        or ("rate story" in normalized and ("ratesource" in normalized or "rate source" in normalized))
        or ("rate story" in normalized and ("selected rate" in normalized or "rate amount" in normalized or "platform" in normalized))
        or ("rate story" in normalized and "pay guide" in normalized)
        or ("rate story" in normalized and ("date effective" in normalized or "scoped rates" in normalized or "effective date" in normalized))
        or ("rate story" in normalized and ("worker story" in normalized or "gross to net" in normalized or "payroll output" in normalized))
        or ("ratesource" in normalized and ("rate story" in normalized or "selected rate" in normalized or "rate amount" in normalized or "evidence layer" in normalized))
        or ("rate source" in normalized and ("rate story" in normalized or "selected rate" in normalized or "rate amount" in normalized or "evidence layer" in normalized))
    ):
        return AnswerMode.PRODUCT_DOMAIN.value
    if (
        "what is decision story" in normalized
        or "what is decisionstory" in normalized
        or ("decision story" in normalized and ("platform" in normalized or "evidence layer" in normalized))
        or ("decisionstory" in normalized and ("platform" in normalized or "evidence layer" in normalized))
        or ("decision story" in normalized and ("treatment" in normalized or "entitlement" in normalized or "line exists" in normalized or "payroll decision" in normalized))
        or ("decisionstory" in normalized and ("treatment" in normalized or "entitlement" in normalized or "line exists" in normalized or "payroll decision" in normalized))
        or ("decision story" in normalized and "rate story" in normalized and ("treatment" in normalized or "entitlement" in normalized or "decision evidence" in normalized))
        or ("decision story" in normalized and ("worker story" in normalized or "gross to net" in normalized or "payroll output" in normalized))
        or ("decisionevidenceindex" in normalized and ("decision story" in normalized or "why a treatment" in normalized or "why a line" in normalized))
        or ("decision evidence index" in normalized and ("decision story" in normalized or "why a treatment" in normalized or "why a line" in normalized))
        or ("decisionevidenceindex" in normalized and ("what" in normalized or "used for" in normalized or "explain" in normalized))
        or ("decision evidence index" in normalized and ("what" in normalized or "used for" in normalized or "explain" in normalized))
        or "treatment selection" in normalized
        or "entitlement decision" in normalized
        or "why the line exists" in normalized
        or "why a treatment was selected" in normalized
        or "payroll decision" in normalized and ("why" in normalized or "explain" in normalized)
        or "allowance decision" in normalized
        or "penalty decision" in normalized
        or "overtime decision" in normalized
        or "shift decision" in normalized
        or "public holiday decision" in normalized
        or "public holidays" in normalized
        or "break treatment" in normalized
        or "breaks" in normalized
        or "missed break" in normalized
        or "minimum engagement" in normalized
    ):
        return AnswerMode.PRODUCT_DOMAIN.value
    if (
        payroll_output_framed
        or "what is payroll output" in normalized
        or "what is payrun output" in normalized
        or "what is process period output" in normalized
        or "what is run output" in normalized
        or ("payroll output" in normalized and ("platform" in normalized or "evidence surface" in normalized or "calculated" in normalized))
        or ("payrun output" in normalized and ("platform" in normalized or "evidence" in normalized or "calculated" in normalized))
        or ("process period output" in normalized and ("payroll" in normalized or "payrun" in normalized or "run output" in normalized))
        or ("run output" in normalized and ("process period output" in normalized or "payroll output" in normalized or "platform" in normalized))
        or ("current effective payroll output" in normalized and "payroll output" in normalized)
        or ("current effective output" in normalized and "payroll output" in normalized)
        or ("calculated payroll output" in normalized and ("what" in normalized or "how" in normalized or "explain" in normalized))
    ):
        return AnswerMode.PRODUCT_DOMAIN.value
    if (
        "gross to net" in normalized
        or "gross-to-net" in normalized
        or "grosstonet" in normalized
        or ("gross earnings" in normalized and "net pay" in normalized)
        or ("gross" in normalized and "taxable" in normalized and "net pay" in normalized)
    ):
        return AnswerMode.PRODUCT_DOMAIN.value
    costing_focused_anchor = (
        "finalised payroll outcome" in normalized
        or "finalized payroll outcome" in normalized
        or "payment execution" in normalized
        or "remittance" in normalized
        or "employer liabilities" in normalized
        or "employer liability" in normalized
        or "on costs" in normalized
        or "oncosts" in normalized
        or "deduction obligations" in normalized
        or "deduction obligation" in normalized
        or "write offs" in normalized
        or "write off" in normalized
        or "comparison / remediation" in normalized
        or "comparison remediation" in normalized
        or "remediation variance" in normalized
        or "variance line" in normalized
        or "leave valuation" in normalized
        or "leave accrual" in normalized
        or "negative net pay" in normalized
        or "out of pay" in normalized
        or "audit story" in normalized
        or "financial evidence" in normalized
        or "deferred/final slice" in normalized
        or "deferred final slice" in normalized
        or "payroll processing blocker" in normalized
        or "final slice" in normalized
    )

    if (
        "costing / gl consequence" in normalized
        or "costing and gl consequence" in normalized
        or "costing gl consequence" in normalized
        or ("costing" in normalized and ("gl" in normalized or "financial consequence" in normalized or "financial consequences" in normalized))
        or ("costing" in normalized and costing_focused_anchor)
        or ("gl consequence" in normalized and ("costing" in normalized or "financial" in normalized))
        or ("gl consequences" in normalized and ("costing" in normalized or "financial" in normalized))
        or ("financial consequence" in normalized and ("costing" in normalized or "gl" in normalized))
        or ("financial consequences" in normalized and ("costing" in normalized or "gl" in normalized))
        or ("financial consequence" in normalized and costing_focused_anchor)
        or ("financial consequences" in normalized and costing_focused_anchor)
    ):
        return AnswerMode.PRODUCT_DOMAIN.value

    if (
        "process periods and payrun lifecycle" in normalized
        or "process periods / payrun lifecycle" in normalized
        or (
            "processperiod" in normalized
            and (
                "payrun" in normalized
                or "lifecycle" in normalized
                or "processperiodgroup" in normalized
                or "open" in normalized
                or "closed" in normalized
                or "state" in normalized
                or "governance" in normalized
            )
        )
        or ("process period" in normalized and ("payrun" in normalized or "lifecycle" in normalized))
        or ("processperiodgroup" in normalized and ("calendar" in normalized or "payment" in normalized))
        or ("process period group" in normalized and ("calendar" in normalized or "payment" in normalized))
        or "payrun lifecycle" in normalized
        or ("paymentdate" in normalized and ("process period" in normalized or "payrun lifecycle" in normalized))
        or ("payment date" in normalized and ("process period" in normalized or "payrun lifecycle" in normalized))
        or ("payruncontact" in normalized and ("lifecycle" in normalized or "admission" in normalized))
        or ("runpurpose" in normalized and ("runtype" in normalized or "payrun" in normalized))
        or ("run purpose" in normalized and ("run type" in normalized or "payrun" in normalized))
        or "close rolls forward" in normalized
        or ("admission" in normalized and "processing" in normalized)
        or ("regular" in normalized and "supplementary" in normalized and "retro" in normalized and "payrun" in normalized)
    ):
        return AnswerMode.PRODUCT_DOMAIN.value

    if (
        "contacts and employee appointments" in normalized
        or "contacts / employee appointments" in normalized
        or ("employeeappointment" in normalized and ("contact" in normalized or "worker" in normalized))
        or ("employee appointment" in normalized and ("contact" in normalized or "worker" in normalized))
        or ("contact history" in normalized and ("worker" in normalized or "payroll" in normalized))
        or ("payrun admission" in normalized and ("contact" in normalized or "appointment" in normalized))
        or "worksiteposition" in normalized
        or "awardpositionclass" in normalized
        or ("classification lens" in normalized and ("appointment" in normalized or "contact" in normalized))
        or ("worker readiness" in normalized and ("contact" in normalized or "appointment" in normalized))
        or ("contact" in normalized and ("tax" in normalized or "bank" in normalized or "deduction" in normalized or "payment readiness" in normalized))
        or ("worker attention" in normalized and ("contact" in normalized or "appointment" in normalized))
    ):
        return AnswerMode.PRODUCT_DOMAIN.value

    if (
        "objecttime source truth" in normalized
        or "objecttime / source truth" in normalized
        or ("objecttime" in normalized and "source truth" in normalized)
        or ("objecttime" in normalized and "payrun inclusion" in normalized)
        or ("sourcetruth" in normalized and ("workedhours" in normalized or "worked hours" in normalized))
        or ("raw span hours" in normalized and ("worked hours" in normalized or "objecttime" in normalized))
        or ("span hours" in normalized and ("worked hours" in normalized or "objecttime" in normalized))
        or ("dirty contact" in normalized and ("source truth" in normalized or "objecttime" in normalized))
        or ("reprocessing" in normalized and ("source truth" in normalized or "objecttime" in normalized))
        or ("correction audit" in normalized and ("source truth" in normalized or "objecttime" in normalized))
    ):
        return AnswerMode.PRODUCT_DOMAIN.value

    if (
        "imports and actuals" in normalized
        or "imports / actuals" in normalized
        or "imports actuals" in normalized
        or "imported timesheets" in normalized
        or "imported payroll actuals" in normalized
        or ("payroll actuals" in normalized and ("import" in normalized or "source system" in normalized))
        or ("actuals lane" in normalized and ("import" in normalized or "source system" in normalized))
        or ("source system mapping" in normalized and ("import" in normalized or "actuals" in normalized))
        or ("source-system mapping" in normalized and ("import" in normalized or "actuals" in normalized))
        or ("pay code mapping" in normalized and ("import" in normalized or "actuals" in normalized))
        or ("ratetype mapping" in normalized and ("import" in normalized or "actuals" in normalized))
        or "importedpositionclassificationmap" in normalized
        or "objecttime source truth" in normalized
        or ("source row" in normalized and ("import" in normalized or "actuals" in normalized))
        or "import provenance" in normalized
        or "import run" in normalized
        or ("unmapped actuals" in normalized and ("import" in normalized or "admin queue" in normalized or "mapping" in normalized))
    ):
        return AnswerMode.PRODUCT_DOMAIN.value

    if (
        "award build" in normalized
        or "award evidence" in normalized
        or "awardevidenceset" in normalized
        or "durable award evidence set" in normalized
        or ("pay guide" in normalized and "evidence" in normalized)
        or ("award document" in normalized and ("evidence" in normalized or "build" in normalized))
        or ("needs configuration" in normalized and "award" in normalized)
        or ("needs_configuration" in normalized and "award" in normalized)
        or "decisionevidenceindex" in normalized
        or "decision evidence index" in normalized
        or "ratesourceevidenceindex" in normalized
        or "rate source evidence index" in normalized
    ):
        return AnswerMode.PRODUCT_DOMAIN.value

    if (
        "on costs" in normalized
        or "oncosts" in normalized
        or "employer liabilities" in normalized
        or "employer liability" in normalized
        or "super oncost" in normalized
        or "payrolltax oncost" in normalized
        or "workcover oncost" in normalized
        or "workcover" in normalized
        or "state scoped ratesource" in normalized
    ):
        return AnswerMode.PRODUCT_DOMAIN.value

    if (
        "finalisation readiness" in normalized
        or "finalization readiness" in normalized
        or "warning acknowledgement" in normalized
        or "warning acknowledgment" in normalized
        or "finalised outcome" in normalized
        or "finalized outcome" in normalized
        or ("finalisation" in normalized and ("readiness" in normalized or "blockers" in normalized or "warnings" in normalized))
        or ("finalization" in normalized and ("readiness" in normalized or "blockers" in normalized or "warnings" in normalized))
    ):
        return AnswerMode.PRODUCT_DOMAIN.value

    if (
        "leave accrual processing" in normalized
        or "leave accrual detail" in normalized
        or "leave source model" in normalized
        or "leave valuation basis" in normalized
        or "leave applicability" in normalized
        or "calcinterpreterline" in normalized
        or "calc interpreter line" in normalized
        or "leaveprocessrun" in normalized
        or "leave process run" in normalized
        or "leavetyperule" in normalized
        or "leave type rule" in normalized
        or ("leave accrue" in normalized and "processed" in normalized)
    ):
        return AnswerMode.PRODUCT_DOMAIN.value

    if (
        "payg withholding" in normalized
        or "tax / payg" in normalized
        or "tax payg" in normalized
        or "taxstory" in normalized
        or "tax story" in normalized
    ):
        return AnswerMode.PRODUCT_DOMAIN.value

    if (
        "payment execution remittance" in normalized
        or "payment execution / remittance" in normalized
        or "payment execution and remittance" in normalized
        or "payment execution" in normalized
        or "generate bank file" in normalized
        or "bank file" in normalized
        or "period close" in normalized
        or "payment allocation" in normalized
        or "payment destination" in normalized
        or "bank allocation" in normalized
        or "worker net pay" in normalized
        or "third party remittance" in normalized
        or "remittance batching" in normalized
        or "remittance reconciliation" in normalized
        or "payment file" in normalized
        or "obligation write off" in normalized
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
        or "finalised payroll truth" in normalized
        or "finalized payroll truth" in normalized
        or ("current effective truth" in normalized and "historical truth" in normalized)
        or ("current-effective truth" in normalized and "historical truth" in normalized)
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
        "contacts and employee appointments",
        "contacts / employee appointments",
        "employeeappointment",
        "employee appointment",
        "contact history",
        "payrun admission",
        "worksiteposition",
        "awardpositionclass",
        "classification lens",
        "worker readiness",
        "worker attention",
        "award build",
        "award evidence",
        "awardevidenceset",
        "durable award evidence set",
        "pay guide evidence",
        "needs configuration",
        "needs_configuration",
        "objecttime source truth",
        "objecttime / source truth",
        "objecttime",
        "sourcetruth",
        "source truth",
        "source row",
        "raw span hours",
        "span hours",
        "worked hours",
        "payrun inclusion",
        "current effective output",
        "dirty contact",
        "reprocessing",
        "correction audit",
        "imports and actuals",
        "imports / actuals",
        "imports actuals",
        "imported timesheets",
        "imported payroll actuals",
        "payroll actuals",
        "actuals lane",
        "source system mapping",
        "source-system mapping",
        "pay code mapping",
        "ratetype mapping",
        "importedpositionclassificationmap",
        "objecttime source truth",
        "source row",
        "import provenance",
        "import run",
        "unmapped actuals",
        "on costs",
        "oncosts",
        "employer liabilities",
        "employer liability",
        "super oncost",
        "payrolltax oncost",
        "workcover oncost",
        "workcover",
        "wic",
        "ratesource",
        "rate source",
        "date effective rates",
        "runtime location",
        "state scoped ratesource",
        "account wide fallback",
        "finalisation readiness",
        "finalization readiness",
        "finalisation",
        "finalization",
        "finalised outcome",
        "finalized outcome",
        "warning acknowledgement",
        "warning acknowledgment",
        "blockers",
        "warnings",
        "payroll bases readiness",
        "leave readiness",
        "payment readiness",
        "leave accrual",
        "leave processing",
        "leave source model",
        "leave source truth",
        "leave valuation basis",
        "leave applicability",
        "missing leave output",
        "contact scope",
        "contact versus appointment",
        "employeeappointment scope",
        "employee appointment scope",
        "appointment aware leave",
        "source dimensions",
        "leavetyperule",
        "leave type rule",
        "leavetype",
        "leave type",
        "accrual basis",
        "accrualability",
        "calcinterpreterline",
        "calc interpreter line",
        "current effective payroll output",
        "leaveprocessrun",
        "leave process run",
        "taken leave",
        "per hour",
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
        "finalised payroll truth",
        "finalized payroll truth",
        "historical truth",
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
        "payment execution remittance",
        "payment execution / remittance",
        "payment execution and remittance",
        "payment execution",
        "generate bank file",
        "bank file",
        "period close",
        "payment allocation",
        "payment destination",
        "bank allocation",
        "worker net pay",
        "third party remittance",
        "remittance batching",
        "remittance reconciliation",
        "payment file",
        "obligation write off",
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
