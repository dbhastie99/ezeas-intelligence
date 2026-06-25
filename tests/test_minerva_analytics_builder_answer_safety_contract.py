import json
from pathlib import Path


CONTRACT_PATH = Path("metadata/minerva/analytics_builder_answer_safety_contract.v0_1.json")


def _load_contract():
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def _all_contract_text(contract):
    return json.dumps(contract, sort_keys=True)


def test_analytics_builder_answer_safety_contract_parses():
    contract = _load_contract()

    assert contract["contract_id"] == "analytics_builder_answer_safety_contract_v0_1"
    assert contract["domain_key"] == "analytics_builder_guide"
    assert contract["production_answer_use_allowed"] is False


def test_analytics_builder_safety_contract_blocks_final_paid_overclaims():
    text = _all_contract_text(_load_contract())

    assert "Final-paid payroll truth remains UNPROVEN / Blocked" in text
    assert "Final-paid payroll truth must remain UNPROVEN / Blocked" in text
    assert "Final-paid payroll truth is proven" in text
    assert "not enough governed proof" in text


def test_analytics_builder_safety_contract_blocks_payrollledger_as_bank_paid_proof():
    text = _all_contract_text(_load_contract())

    assert "PayrollLedger does not prove bank-paid truth" in text
    assert "PayrollLedger is bank-paid proof" in text
    assert "settlement, remittance, bank acceptance, or final-paid evidence" in text


def test_analytics_builder_safety_contract_blocks_calcinterpreterline_as_payment_execution():
    text = _all_contract_text(_load_contract())

    assert "CalcInterpreterLine is calculation/detail evidence" in text
    assert "CalcInterpreterLine proves payment execution" in text
    assert "CalcInterpreterLine must not be described as payment execution evidence" in text


def test_analytics_builder_safety_contract_blocks_objecttime_as_payment_finality():
    text = _all_contract_text(_load_contract())

    assert "ObjectTime is source-context evidence" in text
    assert "ObjectTime proves payment finality" in text
    assert "ObjectTime must not be described as payment finality" in text


def test_analytics_builder_safety_contract_says_zero_certified_assets_unless_source_says_otherwise():
    contract = _load_contract()
    text = _all_contract_text(contract)

    assert contract["portfolio_guardrails"]["certified_assets_count"] == 0
    assert "Current v0.2 Certified asset count is zero" in text
    assert "Certified may be used only when source metadata says Certified" in text


def test_analytics_builder_safety_contract_preserves_required_status_terms():
    contract = _load_contract()

    assert contract["required_status_terms"]["proof_statuses"] == [
        "PROVEN",
        "LIKELY",
        "POSSIBLE",
        "DISPROVEN",
        "UNPROVEN",
    ]
    assert contract["required_status_terms"]["certification_statuses"] == [
        "Diagnostic",
        "Transitional",
        "Blocked",
        "Certified",
    ]


def test_analytics_builder_safety_contract_blocks_visual_certification_proof():
    text = _all_contract_text(_load_contract())

    assert "Visual rendering is not certification proof" in text
    assert "A rendered visual proves certification" in text
    assert "Visual rendering is not validation proof" in text
