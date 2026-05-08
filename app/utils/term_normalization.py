import re


PROJECT_TERM_ALIASES = {
    "LeaveLedger": ("leaveledger", "leave ledger"),
    "LeaveType": ("leavetype", "leave type"),
    "LeaveTypeRule": ("leavetyperule", "leave type rule"),
    "LeaveTypeKind": ("leavetypekind", "leave type kind"),
    "Worker Story": ("workerstory", "worker story"),
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
