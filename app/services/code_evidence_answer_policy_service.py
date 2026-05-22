from dataclasses import asdict, dataclass, field
from enum import StrEnum


class CodeEvidenceRole(StrEnum):
    DEVELOPER = "DEVELOPER"
    PAYROLL_ADMINISTRATOR = "PAYROLL_ADMINISTRATOR"
    PAYROLL_USER = "PAYROLL_USER"
    CUSTOMER_ADMINISTRATOR = "CUSTOMER_ADMINISTRATOR"
    WORKER = "WORKER"


class CodeEvidenceDisclosureMode(StrEnum):
    TECHNICAL_DISCLOSURE = "TECHNICAL_DISCLOSURE"
    IMPLEMENTATION_CONFIRMATION = "IMPLEMENTATION_CONFIRMATION"
    BACKGROUND_CONFIDENCE_ONLY = "BACKGROUND_CONFIDENCE_ONLY"
    NO_CODE_EVIDENCE = "NO_CODE_EVIDENCE"


RUNTIME_CAVEAT = (
    "Code evidence can support implementation confidence, but code evidence alone "
    "cannot prove production availability, runtime enablement, customer access, "
    "deployed schema state, permissions, live object state, payroll correctness, "
    "payment, or finalisation."
)

DEFAULT_PROHIBITED_CLAIMS = [
    "Code evidence proves production availability.",
    "Code evidence proves runtime enablement.",
    "Code evidence proves customer access.",
    "Code evidence proves a database migration has been applied.",
    "Code evidence proves live object state.",
    "Code evidence proves payroll correctness.",
    "Code evidence proves payment or finalisation occurred.",
    "Code evidence can be used as payroll calculation authority.",
]


@dataclass(frozen=True)
class CodeEvidenceAnswerPolicy:
    role: CodeEvidenceRole
    disclosure_mode: CodeEvidenceDisclosureMode
    can_show_repo_names: bool
    can_show_file_paths: bool
    can_show_symbol_names: bool
    can_show_route_paths: bool
    can_show_test_names: bool
    can_show_raw_code_snippets: bool
    background_confidence_only: bool
    customer_safe: bool
    may_use_code_evidence: bool
    caveats: list[str] = field(default_factory=list)
    prohibited_claims: list[str] = field(default_factory=list)

    def model_dump(self) -> dict:
        payload = asdict(self)
        payload["role"] = self.role.value
        payload["disclosure_mode"] = self.disclosure_mode.value
        return payload


class CodeEvidenceAnswerPolicyService:
    def policy_for_role(self, role: CodeEvidenceRole | str) -> CodeEvidenceAnswerPolicy:
        normalized_role = _normalize_role(role)
        if normalized_role == CodeEvidenceRole.DEVELOPER:
            return CodeEvidenceAnswerPolicy(
                role=normalized_role,
                disclosure_mode=CodeEvidenceDisclosureMode.TECHNICAL_DISCLOSURE,
                can_show_repo_names=True,
                can_show_file_paths=True,
                can_show_symbol_names=True,
                can_show_route_paths=True,
                can_show_test_names=True,
                can_show_raw_code_snippets=False,
                background_confidence_only=False,
                customer_safe=False,
                may_use_code_evidence=True,
                caveats=[RUNTIME_CAVEAT, "Raw secrets must never be exposed."],
                prohibited_claims=list(DEFAULT_PROHIBITED_CLAIMS),
            )
        if normalized_role == CodeEvidenceRole.PAYROLL_ADMINISTRATOR:
            return CodeEvidenceAnswerPolicy(
                role=normalized_role,
                disclosure_mode=CodeEvidenceDisclosureMode.IMPLEMENTATION_CONFIRMATION,
                can_show_repo_names=True,
                can_show_file_paths=True,
                can_show_symbol_names=False,
                can_show_route_paths=False,
                can_show_test_names=True,
                can_show_raw_code_snippets=False,
                background_confidence_only=False,
                customer_safe=False,
                may_use_code_evidence=True,
                caveats=[
                    RUNTIME_CAVEAT,
                    "Use implementation confirmation rather than raw code by default.",
                ],
                prohibited_claims=list(DEFAULT_PROHIBITED_CLAIMS),
            )
        if normalized_role == CodeEvidenceRole.PAYROLL_USER:
            return CodeEvidenceAnswerPolicy(
                role=normalized_role,
                disclosure_mode=CodeEvidenceDisclosureMode.BACKGROUND_CONFIDENCE_ONLY,
                can_show_repo_names=False,
                can_show_file_paths=False,
                can_show_symbol_names=False,
                can_show_route_paths=False,
                can_show_test_names=False,
                can_show_raw_code_snippets=False,
                background_confidence_only=True,
                customer_safe=True,
                may_use_code_evidence=True,
                caveats=[
                    RUNTIME_CAVEAT,
                    "Keep the answer operational and do not expose code evidence names by default.",
                ],
                prohibited_claims=list(DEFAULT_PROHIBITED_CLAIMS),
            )
        if normalized_role == CodeEvidenceRole.CUSTOMER_ADMINISTRATOR:
            return CodeEvidenceAnswerPolicy(
                role=normalized_role,
                disclosure_mode=CodeEvidenceDisclosureMode.IMPLEMENTATION_CONFIRMATION,
                can_show_repo_names=False,
                can_show_file_paths=False,
                can_show_symbol_names=False,
                can_show_route_paths=False,
                can_show_test_names=False,
                can_show_raw_code_snippets=False,
                background_confidence_only=False,
                customer_safe=True,
                may_use_code_evidence=True,
                caveats=[
                    RUNTIME_CAVEAT,
                    "Use customer-safe implementation confirmation without internal code paths by default.",
                ],
                prohibited_claims=list(DEFAULT_PROHIBITED_CLAIMS),
            )
        return CodeEvidenceAnswerPolicy(
            role=CodeEvidenceRole.WORKER,
            disclosure_mode=CodeEvidenceDisclosureMode.NO_CODE_EVIDENCE,
            can_show_repo_names=False,
            can_show_file_paths=False,
            can_show_symbol_names=False,
            can_show_route_paths=False,
            can_show_test_names=False,
            can_show_raw_code_snippets=False,
            background_confidence_only=False,
            customer_safe=True,
            may_use_code_evidence=False,
            caveats=[
                RUNTIME_CAVEAT,
                "Workers receive only worker-facing evidence and approved explanations.",
            ],
            prohibited_claims=list(DEFAULT_PROHIBITED_CLAIMS),
        )

    def role_to_disclosure_mapping(self) -> dict[str, str]:
        return {
            role.value: self.policy_for_role(role).disclosure_mode.value
            for role in CodeEvidenceRole
        }

    def may_show_file_paths(self, role: CodeEvidenceRole | str) -> bool:
        return self.policy_for_role(role).can_show_file_paths

    def may_show_symbol_names(self, role: CodeEvidenceRole | str) -> bool:
        return self.policy_for_role(role).can_show_symbol_names

    def may_show_test_names(self, role: CodeEvidenceRole | str) -> bool:
        return self.policy_for_role(role).can_show_test_names

    def may_show_raw_code_snippets(self, role: CodeEvidenceRole | str) -> bool:
        return self.policy_for_role(role).can_show_raw_code_snippets

    def code_cannot_prove_runtime_caveat(self) -> str:
        return RUNTIME_CAVEAT

    def prohibited_claims(self) -> list[str]:
        return list(DEFAULT_PROHIBITED_CLAIMS)


def _normalize_role(role: CodeEvidenceRole | str) -> CodeEvidenceRole:
    if isinstance(role, CodeEvidenceRole):
        return role
    try:
        return CodeEvidenceRole(str(role).upper())
    except ValueError:
        raise ValueError(f"Unsupported code evidence role: {role!r}") from None
