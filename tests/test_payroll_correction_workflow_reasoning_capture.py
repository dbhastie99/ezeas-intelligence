from pathlib import Path


REASONING_ARTIFACT = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "knowledge"
    / "payroll_correction_workflow_reasoning_v0_1.md"
)


def _content():
    return REASONING_ARTIFACT.read_text(encoding="utf-8")


def _lower_content():
    return _content().lower()


def test_reasoning_artefact_exists():
    assert REASONING_ARTIFACT.exists()


def test_revised_8_slice_plan_is_recorded():
    content = _content()

    assert "Original 5-Slice Workforce Correction Review Plan" in content
    assert "Revised 8-Slice Workforce Plan" in content
    assert "1. Correction Review Front Door - completed." in content
    assert "2. Persistence + Admin Queue - completed." in content
    assert "3. Supplementary/Retro Readiness Preview - completed." in content
    assert "4. ProcessPeriod Lifecycle + ObjectTime Ingress + Payment Window Routing." in content
    assert "5. Bucket / Semantic Totals Correction Impact Review." in content
    assert "6. Supplementary Delta + Payment Netting Preview." in content
    assert "7. Retro Model + Dependency Scan Foundation." in content
    assert "8. Retro Replay Preview." in content
    assert "replaced the earlier 5-slice plan" in content


def test_finalisation_lock_reasoning_is_captured():
    content = _lower_content()

    assert "processperiod finalisation lock doctrine" in content
    assert "closed for finalisation means payroll managers are reviewing" in content
    assert "admission boundary" in content
    assert "late changes default to correction review" in content


def test_payment_date_reporting_year_reasoning_is_captured():
    content = _lower_content()

    assert "payment date determines reporting period doctrine" in content
    assert "if payment enters the bank after year end" in content
    assert "payment date controls reporting/tax year treatment" in content
    assert "attribution period is not payment period doctrine" in content


def test_off_cycle_payment_period_reasoning_is_captured():
    content = _lower_content()

    assert "fifty late timesheets after finalisation lock" in content
    assert "governed off-cycle payment period" in content
    assert "workers should not be forced to wait until the next regular cycle" in content
    assert "off-cycle payment period doctrine" in content


def test_banking_netting_reasoning_is_captured():
    content = _lower_content()

    assert "banking netting doctrine" in content
    assert "payment-layer netting, not mutation of calculation truth" in content
    assert "payment aggregation across multiple payruns" in content
    assert "calculation identity vs payment aggregation doctrine" in content
    assert "payment aggregation separation doctrine" in content


def test_negative_delta_before_and_after_payment_are_distinguished():
    content = _lower_content()

    assert "negative supplementary delta before banking" in content
    assert "bank payment is $500" in content
    assert "negative delta after payment" in content
    assert "overpayment/recovery review" in content
    assert "cannot be merged into the already executed bank payment" in content


def test_objecttime_change_capture_and_calcinterpreterline_rebuild_distinction():
    content = _lower_content()

    assert "source truth change capture doctrine" in content
    assert "approved timesheet amended after pay finalisation" in content
    assert "preserve source-change evidence" in content
    assert "objecttime changes while payrun is still open" in content
    assert "calcinterpreterline output may be rebuilt or superseded" in content
    assert "open calculation rebuild doctrine" in content
    assert "finalised payroll immutability doctrine" in content


def test_bucket_impact_checkpoint_is_captured():
    content = _lower_content()

    assert "bucket impact checkpoint" in content
    assert "attributed vs processed/payment period" in content
    assert "open vs locked/finalised snapshots" in content
    assert "semantic totals" in content
    assert "delta/source lineage" in content
    assert "double-counting prevention" in content


def test_minerva_question_answer_examples_are_captured():
    content = _content()

    assert "Questions Minerva Must Be Able To Answer" in content
    assert "Why is this retro and not an adjustment into the current pay?" in content
    assert "Why is this supplementary and not dirty reprocessing?" in content
    assert "Why can this negative delta be netted before banking but become recovery after payment?" in content
    assert "Why did the system create an off-cycle payment option?" in content
    assert "Why does payment date matter at year end?" in content
    assert "When do CalcInterpreterLine rows get rebuilt versus preserved?" in content
    assert "Why is the original finalised PayRun not changed?" in content
    assert "What evidence is missing before treatment can be decided?" in content
    assert "Answer pattern:" in content


def test_boundaries_state_reasoning_only_and_no_runtime_execution_claim():
    content = _lower_content()

    assert "no runtime minerva behaviour was added" in content
    assert "no live llm was called" in content
    assert "no chat endpoint was exposed" in content
    assert "no db was accessed" in content
    assert "no corpus mutation occurred" in content
    assert "no workforce-platform code changed" in content
    assert "no analytics code changed" in content
    assert "curated reasoning evidence only" in content
    assert "implementation is pending for future workforce slices" in content
    assert "does not claim runtime execution" in content
