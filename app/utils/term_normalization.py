import re


PROJECT_TERM_ALIASES = {
    "LeaveLedger": ("leaveledger", "leave ledger"),
    "LeaveType": ("leavetype", "leave type"),
    "LeaveTypeRule": ("leavetyperule", "leave type rule"),
    "LeaveTypeKind": ("leavetypekind", "leave type kind"),
    "Deductions / Obligations": ("deductions obligations", "deductions / obligations", "deductions and obligations"),
    "LibraryDeductionTemplate": ("librarydeductiontemplate", "library deduction template"),
    "AccountDeductionTemplate": ("accountdeductiontemplate", "account deduction template"),
    "ContactPayrollDeduction": ("contactpayrolldeduction", "contact payroll deduction"),
    "PayRunDeductionApplication": ("payrundeductionapplication", "payrun deduction application"),
    "ContactPayrollObligation": ("contactpayrollobligation", "contact payroll obligation"),
    "ContactPayrollObligationLedger": ("contactpayrollobligationledger", "contact payroll obligation ledger"),
    "supplementary deduction memory": ("supplementarydeductionmemory", "supplementary deduction memory"),
    "reducing-balance recovery": ("reducing balance recovery", "reducing-balance recovery", "reducingbalancerecovery"),
    "carry-forward": ("carry forward", "carry-forward", "carryforward"),
    "negative net pay": ("negativenetpay", "negative net pay"),
    "Retro / Replay": ("retro replay", "retro / replay"),
    "retro PayRun": ("retropayrun", "retro payrun", "retro pay run"),
    "supplementary PayRun": ("supplementarypayrun", "supplementary payrun", "supplementary pay run"),
    "attributed period": ("attributedperiod", "attributed period"),
    "paid period": ("paidperiod", "paid period"),
    "finalised outcome memory": ("finalized outcome memory", "finalised outcome memory"),
    "dependency detection": ("dependencydetection", "dependency detection"),
    "bucket rebuild": ("bucketrebuild", "bucket rebuild"),
    "historical bucket evidence": ("historicalbucketevidence", "historical bucket evidence"),
    "correction/replay": ("correction replay", "correction/replay"),
    "Worker Story": ("workerstory", "worker story"),
    "Payroll Bases & Totals": ("payroll bases and totals", "payroll bases totals"),
    "PayrollBucketResult": ("payrollbucketresult", "payroll bucket result"),
    "PayrollBucketDefinition": ("payrollbucketdefinition", "payroll bucket definition"),
    "PayRun Admin Queue": ("payrun admin queue", "admin queue", "payrun queue"),
    "Worker Attention": ("workerattention", "worker attention"),
    "dirty contacts": ("dirtycontacts", "dirty contacts"),
    "finalisation readiness": ("finalization readiness", "finalisation readiness"),
    "Assurance Snapshot": ("assurancesnapshot", "assurance snapshot"),
    "Command Centre": ("commandcentre", "command centre", "command center"),
    "Movement Review": ("movementreview", "movement review", "payroll movement review"),
    "review-worthy": ("review worthy", "reviewworthy"),
    "comparable period": ("comparableperiod", "comparable period"),
    "rolling average": ("rollingaverage", "rolling average"),
    "trend-only": ("trend only", "trendonly"),
    "Comparison / Remediation": ("comparison remediation", "comparison / remediation"),
    "Award Comparison": ("awardcomparison", "award comparison"),
    "PayRunComparisonRun": ("payruncomparisonrun", "payrun comparison run"),
    "PayRunComparisonLine": ("payruncomparisonline", "payrun comparison line"),
    "PayRunVarianceLine": ("payrunvarianceline", "payrun variance line"),
    "AwardComparisonPolicy": ("awardcomparisonpolicy", "award comparison policy"),
    "comparator award": ("comparatoraward", "comparator award"),
    "imported actuals": ("importedactuals", "imported actuals"),
    "actuals lane": ("actualslane", "actuals lane"),
    "remediation top-up": ("remediation top up", "remediation top-up", "remediationtopup"),
    "variance line": ("varianceline", "variance line"),
    "AwardPositionClassComparisonMap": ("awardpositionclasscomparisonmap", "award position class comparison map"),
    "EmployeeAppointmentAwardClassAssignment": (
        "employeeappointmentawardclassassignment",
        "employee appointment award class assignment",
    ),
    "ObjectTimeClassificationResolution": ("objecttimeclassificationresolution", "object time classification resolution"),
    "Tax / PAYG": ("tax payg", "tax / payg", "payg"),
    "PAYG withholding": ("paygwithholding", "payg withholding"),
    "TaxStory": ("taxstory", "tax story"),
    "taxable basis": ("taxablebasis", "taxable basis"),
    "taxable earnings": ("taxableearnings", "taxable earnings"),
    "worker tax declaration": ("workertaxdeclaration", "worker tax declaration"),
    "withholding instruction": ("withholdinginstruction", "withholding instruction"),
    "ProcessPeriod PaymentDate": ("processperiodpaymentdate", "process period payment date"),
    "payment date": ("paymentdate", "payment date"),
    "gross-to-net": ("gross to net", "gross-to-net", "grosstonet"),
    "finalised totals": ("finalized totals", "finalised totals"),
    "supplementary incremental PAYG": ("supplementary incremental payg", "supplementaryincrementalpayg"),
    "SourceTruth": ("sourcetruth", "source truth"),
    "DecisionEvidenceIndex": ("decisionevidenceindex", "decision evidence index"),
    "RateSourceEvidenceIndex": ("ratesourceevidenceindex", "rate source evidence index"),
    "current-effective": ("current effective", "currenteffective"),
    "ObjectTime": ("objecttime", "object time"),
    "PayRun": ("payrun", "pay run"),
    "DeductsOnPublicHoliday": ("deductsonpublicholiday", "deducts on public holiday"),
}


def _split_camel_case(value: str) -> str:
    spaced = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", value)
    return re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", spaced)


def normalize_for_term_match(value: str) -> str:
    camel_spaced = _split_camel_case(value)
    lower = camel_spaced.lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", lower)).strip()


def term_variants(term: str) -> set[str]:
    variants = {
        normalize_for_term_match(term),
        re.sub(r"[^a-z0-9]+", "", term.lower()),
    }
    for canonical, aliases in PROJECT_TERM_ALIASES.items():
        canonical_variants = {normalize_for_term_match(canonical), re.sub(r"[^a-z0-9]+", "", canonical.lower())}
        alias_variants = {normalize_for_term_match(alias) for alias in aliases} | {
            re.sub(r"[^a-z0-9]+", "", alias.lower()) for alias in aliases
        }
        if variants & (canonical_variants | alias_variants):
            variants |= canonical_variants | alias_variants
    return {variant for variant in variants if variant}


def normalized_text_forms(value: str) -> set[str]:
    normalized = normalize_for_term_match(value)
    compact = re.sub(r"[^a-z0-9]+", "", value.lower())
    return {normalized, compact}


def contains_normalized_term(text: str, term: str) -> bool:
    forms = normalized_text_forms(text)
    return any(variant in form for variant in term_variants(term) for form in forms)


def contains_any_normalized(text: str, terms: list[str] | tuple[str, ...]) -> bool:
    return any(contains_normalized_term(text, term) for term in terms)


def contains_all_normalized(text: str, terms: list[str] | tuple[str, ...]) -> bool:
    return all(contains_normalized_term(text, term) for term in terms)
