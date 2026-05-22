from app.services.code_evidence_answer_policy_service import (
    CodeEvidenceAnswerPolicyService,
    CodeEvidenceDisclosureMode,
    CodeEvidenceRole,
)


def test_developer_maps_to_technical_disclosure():
    policy = CodeEvidenceAnswerPolicyService().policy_for_role(CodeEvidenceRole.DEVELOPER)

    assert policy.disclosure_mode == CodeEvidenceDisclosureMode.TECHNICAL_DISCLOSURE


def test_payroll_administrator_maps_to_implementation_confirmation():
    policy = CodeEvidenceAnswerPolicyService().policy_for_role(CodeEvidenceRole.PAYROLL_ADMINISTRATOR)

    assert policy.disclosure_mode == CodeEvidenceDisclosureMode.IMPLEMENTATION_CONFIRMATION


def test_payroll_user_maps_to_background_confidence_only():
    policy = CodeEvidenceAnswerPolicyService().policy_for_role(CodeEvidenceRole.PAYROLL_USER)

    assert policy.disclosure_mode == CodeEvidenceDisclosureMode.BACKGROUND_CONFIDENCE_ONLY
    assert policy.background_confidence_only is True


def test_customer_administrator_maps_to_customer_safe_implementation_confirmation():
    policy = CodeEvidenceAnswerPolicyService().policy_for_role(CodeEvidenceRole.CUSTOMER_ADMINISTRATOR)

    assert policy.disclosure_mode == CodeEvidenceDisclosureMode.IMPLEMENTATION_CONFIRMATION
    assert policy.customer_safe is True
    assert policy.can_show_file_paths is False


def test_worker_maps_to_no_code_evidence():
    policy = CodeEvidenceAnswerPolicyService().policy_for_role(CodeEvidenceRole.WORKER)

    assert policy.disclosure_mode == CodeEvidenceDisclosureMode.NO_CODE_EVIDENCE
    assert policy.may_use_code_evidence is False


def test_developer_can_see_file_function_and_test_references():
    policy = CodeEvidenceAnswerPolicyService().policy_for_role("DEVELOPER")

    assert policy.can_show_file_paths is True
    assert policy.can_show_symbol_names is True
    assert policy.can_show_test_names is True
    assert policy.can_show_route_paths is True


def test_payroll_administrator_gets_implementation_confirmation_without_raw_code():
    policy = CodeEvidenceAnswerPolicyService().policy_for_role("PAYROLL_ADMINISTRATOR")

    assert policy.may_use_code_evidence is True
    assert policy.can_show_file_paths is True
    assert policy.can_show_test_names is True
    assert policy.can_show_raw_code_snippets is False


def test_payroll_user_cannot_see_file_test_or_function_names_by_default():
    policy = CodeEvidenceAnswerPolicyService().policy_for_role("PAYROLL_USER")

    assert policy.can_show_file_paths is False
    assert policy.can_show_test_names is False
    assert policy.can_show_symbol_names is False


def test_worker_cannot_use_code_evidence():
    policy = CodeEvidenceAnswerPolicyService().policy_for_role("WORKER")

    assert policy.may_use_code_evidence is False
    assert policy.can_show_file_paths is False
    assert policy.can_show_test_names is False
    assert policy.can_show_symbol_names is False


def test_every_policy_includes_code_cannot_prove_runtime_caveat():
    service = CodeEvidenceAnswerPolicyService()

    for role in CodeEvidenceRole:
        policy = service.policy_for_role(role)
        caveats = " ".join(policy.caveats)
        assert "cannot prove production availability" in caveats
        assert "runtime enablement" in caveats


def test_prohibited_claims_include_production_runtime_and_customer_availability_from_code_alone():
    prohibited_claims = CodeEvidenceAnswerPolicyService().prohibited_claims()
    joined = " ".join(prohibited_claims)

    assert "production availability" in joined
    assert "runtime enablement" in joined
    assert "customer access" in joined


def test_raw_code_snippets_are_disabled_by_default_for_all_roles_in_v0_1():
    service = CodeEvidenceAnswerPolicyService()

    for role in CodeEvidenceRole:
        assert service.policy_for_role(role).can_show_raw_code_snippets is False
