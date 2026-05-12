import json
import sys

from app.services.answer_mode_service import AnswerMode, RichAnswerPlan, classify_answer_mode
from app.services.golden_question_service import load_golden_manifest, run_golden_questions
from app.services.ingestion_service import ingest_file_bytes
from scripts import run_golden_questions as run_golden_questions_script


def _manifest(tmp_path, questions):
    path = tmp_path / "rich.json"
    path.write_text(
        json.dumps(
            {
                "name": "Rich answer fixture",
                "description": "Fixture manifest",
                "questions": questions,
            }
        ),
        encoding="utf-8",
    )
    return path


def _ingest(db_session, text: str, title: str = "Developer Log - Annual Leave"):
    document, duplicate = ingest_file_bytes(
        db=db_session,
        content=text.encode("utf-8"),
        original_file_name="annual-leave.txt",
        source_type="DEVELOPER_LOG",
        capability_status="IMPLEMENTED",
        title=title,
    )
    assert duplicate is False
    return document


def _ingest_worker_story_benchmark_evidence(db_session):
    evidence = [
        (
            "Worker Story and Worker Calculation Story are the Talking Payslip for worker evidence and explain payroll "
            "outcomes.",
            "Developer Log - Worker Story Purpose",
        ),
        (
            "Worker Story uses SourceTruth and source truth inclusion to show which source truth inputs are included for "
            "a worker in PayRun evidence.",
            "Developer Log - Worker Story SourceTruth",
        ),
        (
            "Interpreted Worked Hours are shown from the current-effective interpreter run with ObjectTime grouping.",
            "Developer Log - Worker Story Interpreted Worked Hours",
        ),
        (
            "Calculated Payroll Outcome shows the current-effective payroll output from PayRun calculation evidence, "
            "including quantity, rate, amount and line proof.",
            "Developer Log - Worker Story Calculated Payroll Outcome",
        ),
        (
            "Decision Story explains why a treatment or line exists. Rate Story explains rate source and rate amount. "
            "DecisionEvidenceIndex and RateSourceEvidenceIndex provide award decision evidence and rate evidence.",
            "Developer Log - Worker Story Decision Rate Evidence",
        ),
        (
            "Worker Story includes Leave and Accrual Outcome evidence using server-owned leave output and ledger evidence.",
            "Developer Log - Worker Story Leave Accrual",
        ),
        (
            "Worker Story includes Payroll Bases & Totals evidence with payroll bases and totals.",
            "Developer Log - Worker Story Payroll Bases Totals",
        ),
        (
            "Movement Review and PayRun Admin Queue evidence explain operator action, review context, evidence and "
            "return context for the reusable Worker Story platform evidence surface.",
            "Developer Log - Worker Story Movement Review",
        ),
        (
            "Worker Story uses current-effective truth from current-effective payroll output and current-effective "
            "interpreter run, with Correction Audit Story where corrections exist.",
            "Developer Log - Worker Story Current Effective Truth",
        ),
        (
            "Worker Story outstanding hardening records limitations, shared Worker Story surface/component work, explicit "
            "break-treatment proof and future reusable story surfaces for evidence explanation.",
            "Developer Log - Worker Story Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_payroll_bases_benchmark_evidence(db_session):
    evidence = [
        (
            "Payroll Bases & Totals are governed payroll basis evidence for operators, not reporting totals. "
            "They explain why payroll bases matter operationally.",
            "Developer Log - Payroll Bases Purpose",
        ),
        (
            "PayrollBucketDefinition and Payroll Bucket Definition evidence define bucket definition, period "
            "definition, calendar policy and membership for payroll basis evidence.",
            "Developer Log - Payroll Bucket Definition",
        ),
        (
            "Payroll Bases & Totals govern worked hours and basis quantity using hours, minutes and quantity evidence.",
            "Developer Log - Payroll Worked Hours Quantity",
        ),
        (
            "Payroll Bases & Totals include gross basis, ordinary basis, superable basis, taxable basis, payroll tax, "
            "WIC and PAYG evidence where formal implementation evidence supports it.",
            "Developer Log - Payroll Basis Types",
        ),
        (
            "Payroll Bases & Totals require current-effective truth, current effective source truth and "
            "current-effective payroll output; stale basis evidence is not safe current truth.",
            "Developer Log - Payroll Current Effective Truth",
        ),
        (
            "PayrollBucketResult and Payroll Bucket Result readiness identifies stale rows and rebuild requirements "
            "before basis evidence is trusted.",
            "Developer Log - Payroll Bucket Result Readiness",
        ),
        (
            "Payroll Bases & Totals connect to Worker Story and Worker Calculation Story as worker evidence in the "
            "platform evidence surface.",
            "Developer Log - Payroll Bases Worker Story",
        ),
        (
            "Payroll Bases & Totals connect to Movement Review and PayRun Admin Queue for operator review of basis "
            "movement evidence.",
            "Developer Log - Payroll Bases Movement Review",
        ),
        (
            "Payroll Bases & Totals outstanding hardening includes limitations, bucket lifecycle, versioning and "
            "future work.",
            "Developer Log - Payroll Bases Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_payrun_admin_queue_benchmark_evidence(db_session):
    evidence = [
        (
            "PayRun Admin Queue is the operator workbench for what needs action now. Command Centre remains the full "
            "evidence and control-room surface, and queue cleanliness is not the same as assurance.",
            "Developer Log - Admin Queue Purpose",
        ),
        (
            "PayRun Admin Queue separates blockers, warnings and ready actions because they have different operational "
            "meaning for operators.",
            "Developer Log - Admin Queue Blockers Warnings Ready",
        ),
        (
            "Worker Attention and dirty contacts belong in the PayRun Admin Queue action workflow for worker attention "
            "and contact changes.",
            "Developer Log - Admin Queue Worker Attention",
        ),
        (
            "PayRun Admin Queue surfaces processing actions and reprocessing actions, but deterministic services remain "
            "payroll calculation truth.",
            "Developer Log - Admin Queue Processing Actions",
        ),
        (
            "Finalisation readiness in PayRun Admin Queue distinguishes blockers and warnings, including amber warnings "
            "that cannot simply be ignored.",
            "Developer Log - Admin Queue Finalisation Readiness",
        ),
        (
            "Assurance Snapshot provides reasonableness, review signals and assurance signals, not hidden calculation "
            "truth; governed assurance thresholds remain hardening.",
            "Developer Log - Admin Queue Assurance Snapshot",
        ),
        (
            "PayRun Admin Queue review surfaces and navigation connect to Worker Story, Payroll Bases & Totals, "
            "Movement Review, PayRun Output and Command Centre.",
            "Developer Log - Admin Queue Review Navigation",
        ),
        (
            "PayRun Admin Queue connects to Worker Story and Worker Calculation Story as worker evidence and review "
            "context.",
            "Developer Log - Admin Queue Worker Story",
        ),
        (
            "PayRun Admin Queue connects to Payroll Bases & Totals payroll bases and basis evidence for operator review.",
            "Developer Log - Admin Queue Payroll Bases",
        ),
        (
            "PayRun Admin Queue connects to Movement Review for operator review and movement evidence.",
            "Developer Log - Admin Queue Movement Review",
        ),
        (
            "PayRun Admin Queue outstanding hardening includes server-owned operation tracker, global queue resolver, "
            "reusable Worker Story surface, governed assurance thresholds and warning acknowledgement.",
            "Developer Log - Admin Queue Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_worker_attention_issue_resolution_benchmark_evidence(db_session):
    evidence = [
        (
            "Worker Attention / Issue Resolution and Worker Attention Centre are the worker-level issue surface for "
            "payroll-affecting blockers, warnings, readiness gaps and deterministic fix links.",
            "Developer Log - Worker Attention Purpose",
        ),
        (
            "WorkerIssue and Worker issue evidence preserve issue scope, issue class, issue type and issue severity "
            "for worker-specific issue handling. IssueScope, IssueClass, IssueType and IssueSeverity describe the "
            "worker issue model, blocker vs warning readiness, recommended action, resolution surface, evidence/story "
            "and not payroll calculation truth.",
            "Developer Log - Worker Issue Model",
        ),
        (
            "Worker Attention surfaces blockers, warnings, worker-level blockers, worker-level warnings and readiness "
            "gaps without treating readiness as proof payroll is correct.",
            "Developer Log - Worker Attention Blockers Warnings",
        ),
        (
            "Deterministic fix links, deterministic fix link records and resolution surfaces provide in-context "
            "remediation, no dead-end issue, server-owned fix targets, backend-owned truth, guided action, governed "
            "user action and audit/evidence where applicable. This is guided action, not Minerva mutation.",
            "Developer Log - Worker Attention Fix Links",
        ),
        (
            "Dirty contact, dirty contacts, payroll-affecting source/configuration change, PayRunContact dirty, "
            "PENDING, contact changes and reprocessing can create worker attention issues. Current PayRun output no "
            "longer safe means reprocessing required, with full contact-level reprocessing default as a platform "
            "safety signal.",
            "Developer Log - Worker Attention Dirty Contact",
        ),
        (
            "Payment allocation readiness, payment execution readiness, payment destination, bank allocation and "
            "payment readiness can create worker attention blockers or warnings.",
            "Developer Log - Worker Attention Payment Allocation",
        ),
        (
            "Tax readiness, deduction readiness and leave readiness are tax/deduction/leave readiness evidence that "
            "can surface worker-level issues.",
            "Developer Log - Worker Attention Tax Deduction Leave",
        ),
        (
            "Negative net pay in gross-to-net context requires governed treatment; obligation, carry-forward, "
            "recovery, write-off and out-of-pay pathways may apply where supported. Negative net pay is not silently "
            "converted to zero and may be a blocker or review-worthy issue depending on policy/evidence.",
            "Developer Log - Worker Attention Negative Net Pay",
        ),
        (
            "Worker Story explains evidence and context for a worker and should expose the same resolution path where "
            "a worker has an issue. Worker Story should explain Worker Attention worker issue evidence as worker "
            "evidence and an explanation surface.",
            "Developer Log - Worker Attention Worker Story",
        ),
        (
            "PayRun Admin Queue and Admin Queue are the operator workbench for what needs action now and broader "
            "action workflow; Worker Attention is the worker-level issue resolution surface. The surfaces are "
            "related but not identical, and Admin Queue and Worker Attention are not the same surface. Minerva "
            "explains relationships, not runtime state.",
            "Developer Log - Worker Attention Admin Queue",
        ),
        (
            "Minerva explains but does not resolve issues, clear blockers, mark dirty, mark PayRunContact dirty, "
            "mutate PayRunContact state, reprocess workers, calculate payroll, approve, suppress, finalise or repair "
            "payroll truth.",
            "Platform Doctrine - Worker Attention Minerva Boundary",
        ),
        (
            "Outstanding hardening remains around Worker Attention status honesty, WorkerIssue issue taxonomy, "
            "resolution workflow, deterministic fix link contracts, dirty-contact/reprocessing propagation and "
            "contract tests.",
            "Developer Log - Worker Attention Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_gross_to_net_benchmark_evidence(db_session):
    evidence = [
        (
            "Gross-to-Net, Gross to Net and GrossToNet are the payroll outcome calculation and payroll outcome "
            "explanation surface that connects gross earnings, payroll output and net pay.",
            "Developer Log - Gross-to-Net Purpose",
        ),
        (
            "Gross earnings, gross pay, payroll output, earnings lines and payroll outcome evidence form the gross "
            "earnings side of the Gross-to-Net chain.",
            "Developer Log - Gross-to-Net Gross Earnings",
        ),
        (
            "Taxable basis, taxable earnings, PAYG, withholding, tax withholding and final withholding connect tax "
            "context to Gross-to-Net. TaxStory, tax evidence and PaymentDate are relevant where tax context is "
            "involved. Payroll Bases relationship and the deterministic tax provider/service boundary matter. Taxable "
            "basis and final withholding are connected to but not the same as general payroll basis evidence unless "
            "that relationship is explained.",
            "Developer Log - Gross-to-Net Taxable Basis PAYG",
        ),
        (
            "Deductions, deduction applications, obligations, obligation recovery and post-tax deductions can affect "
            "net pay where governed policy supports them. Deductions reduce net pay where applicable, while "
            "obligations, reducing-balance recovery, affordability, priority, partial deductions, skipped deductions, "
            "carry-forward, unmet deduction story and linked obligation recovery are governed evidence and not "
            "automatic blind subtraction. Worker Attention and Admin Queue can surface issues.",
            "Developer Log - Gross-to-Net Deductions Obligations",
        ),
        (
            "Negative net pay needs governed treatment such as carry-forward, recovery, obligation and write-off "
            "pathways where formal evidence supports them; it must not be silently converted to zero. Allow, block, "
            "recover later, convert to obligation, write-off and out-of-pay record pathways may apply where supported. "
            "Negative net pay can affect payment execution readiness, Worker Attention issue resolution, financial "
            "consequence and obligation evidence.",
            "Developer Log - Gross-to-Net Negative Net Pay",
        ),
        (
            "Net pay, worker net pay, payment allocation, payment readiness, payment execution readiness, payment "
            "destination and worker net pay consume Gross-to-Net evidence, but Gross-to-Net and Payment Execution are "
            "not the same surface and Gross-to-Net is not payment execution itself.",
            "Developer Log - Gross-to-Net Net Pay Payment Allocation",
        ),
        (
            "Worker Story should explain Gross-to-Net evidence, worker evidence and payroll outcome explanation for "
            "worker-level outcome review.",
            "Developer Log - Gross-to-Net Worker Story",
        ),
        (
            "Finalisation, finalised outcome truth, payment execution and payment execution readiness consume "
            "Gross-to-Net evidence, but Gross-to-Net is not payment execution.",
            "Developer Log - Gross-to-Net Finalisation Payment Execution",
        ),
        (
            "Current-effective payroll output, current effective payroll output, current-effective payroll output "
            "truth, full run, targeted reprocess, current truth, stale output and superseded output determine which "
            "Gross-to-Net outcome is current truth. Worker Story calculated payroll outcome should expose line proof, "
            "amounts, deductions, net pay and audit story.",
            "Developer Log - Gross-to-Net Current Effective Truth",
        ),
        (
            "Minerva does not calculate gross-to-net, withhold tax, apply deductions, change net pay, approve or "
            "resolve negative net pay, generate payment files, finalise PayRuns or mutate operational payroll truth.",
            "Platform Doctrine - Gross-to-Net Minerva Boundary",
        ),
        (
            "Outstanding hardening remains around Gross-to-Net status-honest explanation, negative net pay, taxable "
            "basis, payment allocation and contract tests.",
            "Developer Log - Gross-to-Net Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_rate_source_rate_story_benchmark_evidence(db_session):
    evidence = [
        (
            "RateSource / Rate Story and RateStory are the evidence layer for explaining the selected rate and rate "
            "amount for a payroll line.",
            "Developer Log - Rate Story Purpose",
        ),
        (
            "RateSource and Rate Source selection explain which selected rate was chosen and preserve rate source "
            "selection evidence. Rate Story can identify the selected RateSource, runtime context, evidence basis and "
            "effective date for rate selection.",
            "Developer Log - RateSource Selection",
        ),
        (
            "Rate amount evidence explains where the amount came from, including selected amount, rate value and rate "
            "evidence.",
            "Developer Log - Rate Amount Evidence",
        ),
        (
            "Date-effective rates, date-effective rate and effective date evidence explain which RateSource row applies "
            "for the relevant date. Superseded and historical rates should not be described as current unless in audit "
            "context.",
            "Developer Log - Date Effective Rates",
        ),
        (
            "Award rate, account rate and class rate scope can use award scope, account scope, class scope, RateType "
            "and AwardRateType where formal evidence supports that rate source. Scope resolution depends on "
            "runtime/class/context and selected rate evidence.",
            "Developer Log - Rate Scope Evidence",
        ),
        (
            "Pay guide rate evidence, pay guide evidence, RateSourceEvidenceIndex and Rate Source Evidence Index can "
            "preserve pay guide row, column, page and source text evidence for why a rate amount exists and provide "
            "rate amount support. Evidence limitation honesty is required where pay guide evidence is absent.",
            "Developer Log - Rate Source Evidence Index",
        ),
        (
            "Rate Story is not the same as Decision Story. Decision Story explains entitlement or treatment selection; "
            "Decision Story explains why a treatment or line exists and owns entitlement/treatment logic. Rate Story "
            "explains why a rate/amount was used through selected RateSource and rate amount evidence.",
            "Developer Log - Rate Story Decision Story Boundary",
        ),
        (
            "Worker Story and Worker Calculation Story can expose Rate Story as worker evidence, payroll line "
            "explanation and rate explanation.",
            "Developer Log - Rate Story Worker Story",
        ),
        (
            "Payroll output, calculated payroll outcome, line proof, formula and Gross-to-Net can reference Rate Story "
            "evidence. Gross-to-Net uses output lines and amounts, not Rate Story as calculation authority. Rate Story "
            "supports explanation/audit without making Rate Story the payroll calculation engine.",
            "Developer Log - Rate Story Payroll Output",
        ),
        (
            "Minerva does not select rates, calculate pay, interpret awards at runtime, change RateSource records, "
            "validate payroll correctness, calculate payroll or mutate operational payroll truth. Minerva explains but "
            "does not select rate.",
            "Platform Doctrine - Rate Story Minerva Boundary",
        ),
        (
            "Outstanding hardening remains around RateSource, Rate Story, RateSourceEvidenceIndex, pay guide evidence "
            "and contract tests. RateSource evidence alone does not prove entitlement and pay guide evidence alone "
            "does not prove treatment entitlement.",
            "Developer Log - Rate Story Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_decision_story_benchmark_evidence(db_session):
    evidence = [
        (
            "Decision Story and DecisionStory are the evidence layer for explaining why a payroll treatment, "
            "entitlement, line, rule outcome or calculated payroll decision exists.",
            "Developer Log - Decision Story Purpose",
        ),
        (
            "Treatment selection and entitlement decision evidence explain why a treatment was selected and why the "
            "line exists for a payroll decision. Decision Story explains treatment or entitlement selection from a "
            "configured rule, runtime facts and award/source evidence where available. It is not rate amount selection.",
            "Developer Log - Decision Story Treatment Selection",
        ),
        (
            "DecisionEvidenceIndex and Decision Evidence Index are a compact decision evidence index that links "
            "emitted payroll lines to decision evidence, supports explanation and audit, and can reference award/source "
            "evidence where available. DecisionEvidenceIndex does not by itself prove the full award-source chain and "
            "requires evidence limitation honesty.",
            "Developer Log - Decision Evidence Index",
        ),
        (
            "Award rule, configured rules, runtime facts, source evidence and rule outcome evidence support Decision "
            "Story where formal award/source evidence is available.",
            "Developer Log - Decision Story Award Rule Runtime Facts",
        ),
        (
            "Allowance decision, penalty decision, overtime decision and shift decision evidence explain allowance, "
            "penalty, overtime and shift treatment outcomes. Allowance, penalty, overtime and shift treatment are "
            "explained through runtime facts, configured rules, decision evidence, exact clause/source evidence where "
            "available and a generic limitation where source evidence is incomplete.",
            "Developer Log - Decision Story Allowance Penalty Overtime Shift",
        ),
        (
            "Break treatment, missed break, public holiday decision, minimum engagement and special condition evidence "
            "can explain calculated payroll decision outcomes. Unpaid break evidence where supported, public holiday "
            "treatment, special conditions, configured rules, runtime facts, Worker Story, payroll line explanation "
            "and outstanding hardening remain visible where evidence coverage is incomplete.",
            "Developer Log - Decision Story Break Public Holiday",
        ),
        (
            "Decision Story explains why a treatment or line exists. Decision Story explains why a treatment/line exists "
            "and owns entitlement/treatment logic. Rate Story explains why a rate or amount was used through selected "
            "RateSource and rate amount evidence. Decision Story is not the same as Rate Story. RateSource evidence "
            "alone does not prove entitlement.",
            "Developer Log - Decision Story Rate Story Boundary",
        ),
        (
            "Worker Story can expose Decision Story as worker evidence and payroll line explanation.",
            "Developer Log - Decision Story Worker Story",
        ),
        (
            "Payroll output, calculated payroll outcome, line proof and Gross-to-Net can consume Decision Story "
            "evidence as payroll output amounts/outcomes, explanation and audit evidence, not net-pay calculation "
            "authority.",
            "Developer Log - Decision Story Payroll Output",
        ),
        (
            "Minerva does not select treatments, decide entitlements, interpret awards at runtime, calculate payroll, "
            "change decision evidence, validate payroll correctness or mutate operational payroll truth. Minerva does "
            "not calculate or select treatments and Minerva does not decide entitlements.",
            "Platform Doctrine - Decision Story Minerva Boundary",
        ),
        (
            "Outstanding hardening remains around Decision Story, DecisionEvidenceIndex, contract tests, evidence "
            "limitation honesty and status honesty. DecisionEvidenceIndex alone does not prove the full award-source "
            "chain.",
            "Developer Log - Decision Story Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_payroll_output_benchmark_evidence(db_session):
    evidence = [
        (
            "Payroll Output and PayRun Output are the evidence surface for calculated payroll results, calculated "
            "payroll output, payroll result and calculated payroll result.",
            "Developer Log - Payroll Output Purpose",
        ),
        (
            "Calculated payroll lines, payroll line, output line, line-level payroll outcome and CalcInterpreterLine "
            "represent line-level payroll outcome evidence. Payroll Output should explain amount, quantity and "
            "treatment where formal evidence supports those line attributes.",
            "Developer Log - Payroll Output Lines",
        ),
        (
            "Current-effective output, current effective payroll output and current-effective payroll output truth "
            "separate current truth from stale or superseded output. Current-effective payroll output truth is the "
            "latest/current worker outcome for the process period. Targeted reprocessing versus full run must "
            "preserve current-effective truth, and superseded or stale run rows should not appear as current truth.",
            "Developer Log - Payroll Output Current Effective Truth",
        ),
        (
            "Run Output, PayRun Output and Process Period Output are related but different lenses. Run output explains "
            "results for a PayRun or calculation run, while process-period output is the period-context view; they "
            "should not be collapsed without explanation. Run Output is scoped to the selected run/subrun lens. "
            "Process Period Output should show current-effective whole-period worker truth, and targeted reprocess "
            "should not hide non-target workers from process-period output.",
            "Developer Log - Payroll Output Run Period Lenses",
        ),
        (
            "Worker-level output, worker output, worker payroll output, Worker Story and worker evidence expose "
            "worker-level Payroll Output for review.",
            "Developer Log - Payroll Output Worker Level",
        ),
        (
            "PayRun totals, line totals, payroll totals, output totals and CalcInterpreterRun preserve run-level "
            "summary evidence for Payroll Output.",
            "Developer Log - Payroll Output Totals",
        ),
        (
            "Decision Story explains why a payroll line or treatment exists. Rate Story explains why a selected rate "
            "or rate amount was used. Payroll Output can reference both without selecting treatments or selecting rates.",
            "Developer Log - Payroll Output Decision Rate Story",
        ),
        (
            "Gross-to-Net consumes Payroll Output amounts and lines to explain gross earnings, taxable basis, "
            "deductions, obligations, payroll outcome and net pay. Payroll output lines feed or support the "
            "gross-to-net outcome, but Payroll Output is not payment execution and Minerva does not calculate "
            "gross-to-net.",
            "Developer Log - Payroll Output Gross-to-Net",
        ),
        (
            "Payroll Bases & Totals, Payroll Bases, basis evidence, bucket evidence and basis totals support Payroll "
            "Output explanation but do not replace output lines. Basis results should use current-effective payroll "
            "source truth and may support taxable, superable, payroll tax, WIC, ordinary and worked-hours evidence. "
            "Output totals and basis evidence are related but distinct.",
            "Developer Log - Payroll Output Bases",
        ),
        (
            "Finalisation Readiness and Payment Execution consume Payroll Output evidence downstream. Finalised "
            "outcome truth, payment execution boundary and payment file concerns are downstream boundaries, not "
            "Payroll Output itself. Finalisation readiness uses current-effective output and blockers/warnings, and "
            "payment execution consumes finalised, gross-to-net and payment-ready outcome.",
            "Developer Log - Payroll Output Finalisation Payment",
        ),
        (
            "Minerva does not calculate payroll output, change payroll output lines, finalise PayRuns, approve payroll "
            "output, select treatments, select rates, generate payment files or mutate operational payroll truth. "
            "Payroll Output alone does not prove payroll correctness.",
            "Platform Doctrine - Payroll Output Minerva Boundary",
        ),
        (
            "Outstanding hardening remains around Payroll Output status honesty, current-effective output, contract "
            "tests, Run Output versus Process Period Output boundaries and broader output evidence contracts.",
            "Developer Log - Payroll Output Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_contact_payroll_history_benchmark_evidence(db_session):
    evidence = [
        (
            "Contact Payroll History is the contact/worker-level historical payroll evidence surface for payroll "
            "history, worker payroll history, contact-level payroll history and payroll outcome history.",
            "Developer Log - Contact Payroll History Purpose",
        ),
        (
            "Contact identity, worker history, PayRunContact and PayRun participation show how a contact or worker "
            "participated in process periods and historical PayRuns. Contact Payroll History shows "
            "contact/worker-level payroll history, worker-level output/history and current and historical payroll "
            "evidence, but it is not proof of payroll correctness by itself.",
            "Developer Log - Contact Payroll History Participation",
        ),
        (
            "Current payroll output, current-effective payroll output, current-effective payroll output truth and "
            "historical payroll output distinguish current and historical payroll output. Historical/finalised output "
            "evidence, Run Output and Process Period Output are separate lenses where relevant. Superseded/stale "
            "outputs should not be described as current truth, finalised truth should not be overwritten silently, "
            "and status honesty is required.",
            "Developer Log - Contact Payroll History Output",
        ),
        (
            "Gross-to-Net history, gross to net history, gross earnings history, net pay history and payroll outcome "
            "history are part of the contact payroll history inspection lens.",
            "Developer Log - Contact Payroll History Gross-to-Net",
        ),
        (
            "Contact-level deduction history, contact deductions, contact obligations, deductions, obligations, "
            "reducing balance, recovery context, negative net pay governed treatment and out-of-pay records can "
            "appear as historical payroll evidence. Carry-forward, write-off and recovery implications relate to "
            "Gross-to-Net and Worker Attention, but Contact Payroll History is not automatic net-pay subtraction or "
            "Minerva resolution.",
            "Developer Log - Contact Payroll History Deductions Obligations",
        ),
        (
            "Contact tax, tax/PAYG history, tax history, PAYG, tax readiness evidence, contact payment, payment "
            "allocation, payment readiness history and bank/payment destination context are historical readiness and "
            "outcome signals for Contact Payroll History. The finalisation/payment execution boundary remains visible: "
            "readiness is not payment file generation, and Minerva does not withhold tax or generate payment files.",
            "Developer Log - Contact Payroll History Tax Payment",
        ),
        (
            "Leave history, accrual history, leave/accrual evidence over time, leave accrual, leave evidence, "
            "LeaveLedger, leave output and valuation basis can connect Contact Payroll History to leave and accrual "
            "outcomes through evidence links rather than recalculation.",
            "Developer Log - Contact Payroll History Leave Accrual",
        ),
        (
            "Worker Story, worker evidence, worker-level story, payroll explanation and contact history connect "
            "Contact Payroll History to worker-level explanation.",
            "Developer Log - Contact Payroll History Worker Story",
        ),
        (
            "Movement Review, Admin Queue, PayRun Admin Queue, review context, action workbench and reasonableness "
            "provide movement/review context and operator action context without making those surfaces identical.",
            "Developer Log - Contact Payroll History Review Queue",
        ),
        (
            "Retro history, correction history, retro/replay/correction context, retro replay and correction "
            "implications are future implications and evidence relationships. Historical payroll evidence, finalised "
            "truth preservation, correction, retro and replay pathways, and attributed-period versus paid-period "
            "distinction matter where formal evidence supports them. Contact Payroll History does not silently mutate "
            "history, and it is not proof that Minerva performs retro/replay or corrections.",
            "Developer Log - Contact Payroll History Retro Correction",
        ),
        (
            "Minerva does not calculate payroll history, change historical payroll records, correct payroll outcomes, "
            "perform retro/replay, approve payroll changes, finalise PayRuns or mutate operational payroll truth. "
            "Contact Payroll History alone does not prove payroll correctness.",
            "Platform Doctrine - Contact Payroll History Minerva Boundary",
        ),
        (
            "Outstanding hardening remains around Contact Payroll History status honesty, historical payroll records, "
            "finalised truth, correction implications and broader evidence contracts.",
            "Developer Log - Contact Payroll History Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_movement_review_benchmark_evidence(db_session):
    evidence = [
        (
            "Movement Review is a payroll reasonableness review surface for operators to understand changes, variance "
            "and review-worthy movement.",
            "Developer Log - Movement Review Purpose",
        ),
        (
            "Movement Review is reasonableness evidence, not automatic proof that payroll is wrong.",
            "Developer Log - Movement Review Reasonableness",
        ),
        (
            "Movement Review operates across worker lens and organisation lens, including worker-level and "
            "organisation-level movement views.",
            "Developer Log - Movement Review Lenses",
        ),
        (
            "Movement Review variance depends on comparable period and comparable baseline evidence, with "
            "review-worthy items prioritised.",
            "Developer Log - Movement Review Variance",
        ),
        (
            "Movement Review connects to Payroll Bases & Totals payroll bases and basis evidence for movement "
            "explanations.",
            "Developer Log - Movement Review Payroll Bases",
        ),
        (
            "Movement Review connects to Worker Story for worker-level drill-through, worker evidence and explanation.",
            "Developer Log - Movement Review Worker Story",
        ),
        (
            "Movement Review connects to PayRun Admin Queue and Admin Queue review actions for assurance review actions.",
            "Developer Log - Movement Review Admin Queue",
        ),
        (
            "Movement Review depends on current-effective payroll, current-effective truth and bucket source truth; "
            "stale bucket evidence is not safe current truth.",
            "Developer Log - Movement Review Current Effective Truth",
        ),
        (
            "Movement Review trend-only, rolling average and YTD evidence should not be treated like ordinary "
            "current-period blockers unless governed policy says so.",
            "Developer Log - Movement Review Trend Threshold",
        ),
        (
            "Movement Review filters, filtered lenses, return context, all-worker views and audit views support review.",
            "Developer Log - Movement Review Filters",
        ),
        (
            "Movement Review outstanding hardening includes governed Movement Review Policy, thresholds, comparable "
            "period rules, filtered lenses and historical bucket rebuild governance.",
            "Developer Log - Movement Review Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_comparison_remediation_benchmark_evidence(db_session):
    evidence = [
        (
            "Comparison / Remediation is a governed comparison capability, not a simple top-up adjustment.",
            "Developer Log - Comparison Remediation Purpose",
        ),
        (
            "The comparison model has primary calculated, comparator calculated and actual imported actuals lane "
            "evidence.",
            "Developer Log - Comparison Three Lane Model",
        ),
        (
            "ObjectTime to EmployeeAppointment to AwardPositionClass remains the primary award path and operational "
            "payroll truth.",
            "Developer Log - Comparison Primary Award Path",
        ),
        (
            "Imported actuals and the actuals lane are external outcome truth and imported actual payroll truth, not "
            "calculated interpreter truth.",
            "Developer Log - Comparison Imported Actuals",
        ),
        (
            "AwardComparisonPolicy and Award Comparison Policy govern comparator selection, active lanes, grain, "
            "offset policy, review requirements and variance treatment.",
            "Developer Log - Comparison Policy",
        ),
        (
            "PayRunComparisonRun, PayRun Comparison Run, PayRunComparisonLine and PayRun Comparison Line provide "
            "comparison evidence before variance generation.",
            "Developer Log - Comparison Run Line Evidence",
        ),
        (
            "PayRunVarianceLine and PayRun Variance Line variance line evidence supports remediation top-up lines that "
            "must be typed and explainable.",
            "Developer Log - Comparison Variance Governance",
        ),
        (
            "AwardPositionClassComparisonMap, EmployeeAppointmentAwardClassAssignment and "
            "ObjectTimeClassificationResolution are required because comparator classification and classification lens "
            "mapping cannot be guessed.",
            "Developer Log - Comparison Classification Mapping",
        ),
        (
            "Comparison / Remediation should connect to Worker Story through a future comparison chapter and worker "
            "evidence for remediation evidence.",
            "Developer Log - Comparison Worker Story",
        ),
        (
            "Comparison / Remediation should connect to PayRun Admin Queue for missing policy, unmapped actuals and "
            "variance review actions.",
            "Developer Log - Comparison Admin Queue",
        ),
        (
            "Comparison / Remediation should connect to Movement Review for variance and comparison outcomes; variance "
            "is not automatic proof of error.",
            "Developer Log - Comparison Movement Review",
        ),
        (
            "Comparison / Remediation outstanding hardening remains design doctrine and not yet implemented as a full "
            "runtime capability; future work includes comparison policy, comparison run and line models, variance "
            "generation, classification mapping and Worker Story comparison chapter.",
            "Developer Log - Comparison Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_tax_payg_benchmark_evidence(db_session):
    evidence = [
        (
            "Tax / PAYG is governed withholding calculation evidence and tax evidence, not an LLM calculation.",
            "Developer Log - Tax PAYG Purpose",
        ),
        (
            "Tax / PAYG uses deterministic services and tax providers for withholding calculation; Minerva explains "
            "evidence and status.",
            "Developer Log - Tax PAYG Boundary",
        ),
        (
            "TaxStory and Tax Story should explain source truth, worker tax profile, payroll context, rule pack "
            "selection, component selection, frequency conversion, band/formula calculation, rounding, net-pay effect, "
            "unsupported or skipped rules and audit provenance.",
            "Developer Log - TaxStory Explainability",
        ),
        (
            "Taxable basis and taxable earnings must align with Payroll Bases & Totals and governed basis membership, "
            "not raw flags.",
            "Developer Log - Taxable Basis Payroll Bases",
        ),
        (
            "Worker tax declaration, withholding instruction, withholding inputs and tax profile affect calculation "
            "readiness.",
            "Developer Log - Tax Declaration Withholding Inputs",
        ),
        (
            "ProcessPeriod PaymentDate, payment date and process period provide tax context that should be governed "
            "derived, not hardcoded.",
            "Developer Log - Tax Payment Date",
        ),
        (
            "Pay frequency and provider support must be status-honest for daily, weekly, fortnightly, monthly and "
            "quarterly frequencies, with unsupported frequency status where support is missing.",
            "Developer Log - Tax Pay Frequency",
        ),
        (
            "Gross-to-net, gross to net, net pay, finalised totals, finalised payment memory and PAYG outcome connect "
            "withholding to payment evidence.",
            "Developer Log - Tax Gross Net Finalised Totals",
        ),
        (
            "Supplementary incremental PAYG and supplementary PAYG should be incremental over same-period taxable "
            "earnings, less prior PAYG withheld.",
            "Developer Log - Supplementary PAYG",
        ),
        (
            "Tax / PAYG should connect to Worker Story and PayRun Admin Queue for tax readiness, unsupported states, "
            "correction and reprocessing consequences.",
            "Developer Log - Tax Worker Story Admin Queue",
        ),
        (
            "Unsupported tax scenarios, unsupported frequencies, explicit status, configuration status and review "
            "states should prevent silent success.",
            "Developer Log - Tax Unsupported Review States",
        ),
        (
            "Tax / PAYG outstanding hardening includes provider support, non-weekly frequencies, taxable basis "
            "governance, withholding instruction UI, supplementary tax and full TaxStory.",
            "Developer Log - Tax Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_deductions_obligations_benchmark_evidence(db_session):
    evidence = [
        (
            "Deductions / Obligations are governed application outcomes and governed payroll outcome evidence, not "
            "automatic raw net-pay subtraction.",
            "Developer Log - Deductions Obligations Purpose",
        ),
        (
            "The deduction chain is LibraryDeductionTemplate to AccountDeductionTemplate to ContactPayrollDeduction "
            "to PayRunDeductionApplication. Library templates are advisory accelerators; account templates and worker "
            "instructions become operative configuration.",
            "Developer Log - Deduction Template Chain",
        ),
        (
            "ContactPayrollDeduction is the worker-specific deduction instruction and operative configuration for a "
            "worker deduction.",
            "Developer Log - Worker Deduction Instruction",
        ),
        (
            "PayRunDeductionApplication is PayRun event and outcome memory for requested, taken, skipped and unmet "
            "amounts.",
            "Developer Log - PayRun Deduction Application Memory",
        ),
        (
            "Supplementary deduction memory means supplementary PayRuns must use prior same-period application memory "
            "so recurring deductions do not blindly repeat.",
            "Developer Log - Supplementary Deduction Memory",
        ),
        (
            "Deduction applicability comes before affordability. Affordability, priority, partial, full-only and "
            "carry-forward treatment must be governed and explainable.",
            "Developer Log - Deduction Applicability Affordability Priority",
        ),
        (
            "Skipped, partial, unmet and carry-forward deductions must remain visible and must not silently disappear.",
            "Developer Log - Skipped Partial Unmet Carry Forward",
        ),
        (
            "ContactPayrollObligation and ContactPayrollObligationLedger represent durable obligations and "
            "balance-bearing recovery. Reducing-balance recovery must cap recovery by outstanding balance and complete "
            "with ledger evidence.",
            "Developer Log - Obligation Reducing Balance Recovery",
        ),
        (
            "Negative net pay is a governed outcome requiring policy treatment, not a silent arithmetic side effect.",
            "Developer Log - Negative Net Pay Governance",
        ),
        (
            "Gross-to-net, gross to net, payment execution and remittance surfaces should expose deduction readiness.",
            "Developer Log - Deductions Gross Net Payment Execution",
        ),
        (
            "Deductions / Obligations connect to Worker Story, PayRun Admin Queue and Worker Attention for readiness "
            "and issues.",
            "Developer Log - Deductions Worker Story Admin Queue",
        ),
        (
            "Deductions / Obligations outstanding hardening remains around full UI, remittance, payment execution, "
            "obligation write-off, costing consequences, negative-net-pay policy and deduction tax integration.",
            "Developer Log - Deductions Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_retro_replay_benchmark_evidence(db_session):
    evidence = [
        (
            "Retro / Replay is governed historical correction and evidence replay, not ordinary reprocessing.",
            "Developer Log - Retro Replay Purpose",
        ),
        (
            "Attributed-period truth and paid-period truth must remain distinct for replay correction evidence.",
            "Developer Log - Retro Attributed Paid Period Truth",
        ),
        (
            "Finalised outcome memory records finalised outcomes as historical payment truth and should not be "
            "silently overwritten.",
            "Developer Log - Retro Finalised Outcome Memory",
        ),
        (
            "Current-effective payroll truth is not the same as historical truth or finalised truth.",
            "Developer Log - Retro Current Effective Historical Truth",
        ),
        (
            "Bucket snapshot, basis snapshots, calculation evidence, source hashes and historical bucket evidence "
            "matter for replay.",
            "Developer Log - Retro Bucket Basis Snapshot",
        ),
        (
            "Source change and configuration change should create dependency detection and dirty/replay candidates "
            "rather than hidden recalculation.",
            "Developer Log - Retro Dependency Detection",
        ),
        (
            "Retro PayRuns and retro PayRun evidence differ from supplementary PayRuns and supplementary PayRun "
            "evidence; they are not the same concept.",
            "Developer Log - Retro Supplementary Distinction",
        ),
        (
            "Comparison / Remediation and variance may depend on retro/replay evidence, but comparison is not the "
            "same concept as Retro / Replay.",
            "Developer Log - Retro Comparison Variance",
        ),
        (
            "Retro / Replay should connect to Worker Story at worker level so worker evidence explains retro impacts "
            "and replay impacts.",
            "Developer Log - Retro Worker Story",
        ),
        (
            "PayRun Admin Queue, Admin Queue and Movement Review should surface retro candidates, blockers, review "
            "actions, dependency issues and variance without treating variance as automatic proof of retro error.",
            "Developer Log - Retro Admin Queue Movement Review",
        ),
        (
            "Audit replay should preserve non-destructive history so historical evidence remains auditable through "
            "correction/replay.",
            "Developer Log - Retro Audit Replay",
        ),
        (
            "Retro / Replay outstanding hardening remains future work because full retro/replay implementation and "
            "dependency detection are not complete.",
            "Developer Log - Retro Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_leave_requests_workflow_benchmark_evidence(db_session):
    evidence = [
        (
            "Leave Requests / Leave Workflow is the governed leave request workflow for creating, drafting, "
            "submitting, reviewing, approving, rejecting, reopening, valuing, posting and explaining employee leave "
            "requests. Leave Request and LeaveRequest records represent workflow evidence.",
            "Developer Log - Leave Requests Workflow Purpose",
        ),
        (
            "Request creation and draft editing support create leave request, draft leave, draft editing and leave "
            "request preview before submission.",
            "Developer Log - Leave Requests Draft Editing",
        ),
        (
            "Leave status, status transitions, IdempotencyKey, idempotency and idempotent leave handling should make "
            "workflow actions repeat-safe and explainable.",
            "Developer Log - Leave Requests Status Idempotency",
        ),
        (
            "Leave submission, submit leave, approve leave, reject leave, reopen leave and review leave are governed "
            "workflow transitions driven by operator/user action. Minerva explains the workflow evidence but does "
            "not approve leave or reopen leave requests.",
            "Developer Log - Leave Requests Submission Approval Reopen",
        ),
        (
            "Leave request preview is read-only. Leave overlap, overlap handling, same-type overlap, cross-type "
            "overlap, shortfall substitution, shortfall, proposed plans, apply-plan, child request linkage and "
            "substitution should be explicit workflow evidence where supported. Minerva does not resolve shortfalls.",
            "Developer Log - Leave Requests Overlap Shortfall",
        ),
        (
            "TAKEN leave valuation, leave valuation, leave valuation basis and hard fail behaviour are required when "
            "valuation evidence is mandatory. Ordinary rate, no silent minutes-only fallback, structured processing "
            "error and needs configuration outcomes should be explicit where required inputs are missing. Minerva "
            "does not value leave.",
            "Developer Log - Leave Requests Taken Valuation",
        ),
        (
            "LeaveLedger, leave posting, LeaveLedger posting, leave balance and leave ledger rows are deterministic "
            "platform posting evidence. Accrual, taken, balance movement, parent/child request lineage, posting "
            "evidence and audit/story evidence should distinguish ledger effects. Minerva does not post LeaveLedger "
            "rows or change leave balances.",
            "Developer Log - Leave Requests Ledger Posting",
        ),
        (
            "Leave Source Model, leave applicability, LeaveTypeRule, source applicability and leave source evidence "
            "should be caveated because LeaveTypeRule is policy and calculation content, not final applicability "
            "truth. Contact, EmployeeAppointment, employment/worksite/state dimensions, no entitlement and missing "
            "output distinctions matter where supported. Minerva does not determine entitlement.",
            "Developer Log - Leave Requests Source Applicability",
        ),
        (
            "Worker Story, PayRun, leave request payment, Leave and Accrual Outcome and worker leave evidence connect "
            "Leave Requests / Leave Workflow to worker-level explanation, PayRun processing, leave payment effects, "
            "leave output, valuation and ledger evidence.",
            "Developer Log - Leave Requests Worker Story PayRun",
        ),
        (
            "Finalisation readiness, leave readiness, warnings, blockers, missing leave output, PayRun finalisation, "
            "finalisation boundary and readiness connect leave requests to finalisation readiness without Minerva "
            "finalising PayRuns or calculating payroll.",
            "Developer Log - Leave Requests Finalisation Readiness",
        ),
        (
            "Minerva does not approve leave, calculate leave, post LeaveLedger rows, change leave balances, reopen "
            "leave requests, resolve shortfalls, finalise PayRuns or mutate operational leave or payroll truth. Leave "
            "Requests alone does not prove payroll correctness.",
            "Platform Doctrine - Leave Requests Minerva Boundary",
        ),
        (
            "Outstanding hardening remains around Leave Requests / Leave Workflow, leave workflow, request ownership, "
            "leave hardening, status honesty and broader workflow contracts.",
            "Developer Log - Leave Requests Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_public_holidays_benchmark_evidence(db_session):
    evidence = [
        (
            "Public Holidays are governed date, calendar, location and context evidence that affect payroll treatment, "
            "leave treatment, Worker Story, finalisation readiness and potentially employer liabilities.",
            "Developer Log - Public Holidays Purpose",
        ),
        (
            "PublicHoliday and PublicHolidayGroup source data provide public holiday calendar, date context, observed "
            "days, overrides where supported and governed reference configuration evidence.",
            "Developer Log - Public Holidays Source Calendar",
        ),
        (
            "Public holiday applicability depends on Worksite, WorksitePosition, EmployeeAppointment, state, "
            "jurisdiction and location context rather than a generic date alone. PublicHolidayGroup and governed "
            "context help explain which Public Holiday applies to a worker through EmployeeAppointment, "
            "WorksitePosition and Worksite traversal where supported.",
            "Developer Log - Public Holidays Worksite State",
        ),
        (
            "Public holiday payroll treatment, deterministic payroll interpretation, public holiday treatment "
            "decisions, public holiday decision, entitlement decision and treatment decision are decided by "
            "deterministic payroll services and explained through Decision Story and Payroll Output.",
            "Developer Log - Public Holidays Payroll Decision Story",
        ),
        (
            "Public holiday leave treatment can use DeductsOnPublicHoliday, Leave Requests, LeaveRequest, leave "
            "preview, LeaveLedger and leave posting relationships. Minerva does not approve leave, calculate leave "
            "post LeaveLedger rows or change leave balances.",
            "Developer Log - Public Holidays Leave Interaction",
        ),
        (
            "Worker Story, PayRun Admin Queue, Worker Attention and Finalisation Readiness can surface public holiday "
            "evidence, Decision Story, Payroll Output, payroll evidence, evidence explanation, source/context "
            "visibility, missing public holiday configuration, NEEDS_CONFIGURATION, source context missing, warnings, "
            "blockers and operator evidence.",
            "Developer Log - Public Holidays Operator Readiness",
        ),
        (
            "Minerva explains Public Holiday handling but does not calculate public holiday entitlements, decide "
            "payroll treatment, post payroll output, change PublicHolidayGroup configuration, mutate Worksite, "
            "EmployeeAppointment, PayRun or LeaveRequest truth, determine finalisation readiness or finalise PayRuns.",
            "Platform Doctrine - Public Holidays Minerva Boundary",
        ),
        (
            "Current status and outstanding hardening should remain honest for Public Holidays where formal evidence "
            "is partial around source/configuration coverage, location resolution, leave interaction and operator "
            "readiness surfaces. Public Holidays can relate to employer liabilities and on-costs through state and "
            "location context where formal evidence supports that relationship, but Public Holidays does not own the "
            "broad on-costs domain.",
            "Developer Log - Public Holidays Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_rosters_patterns_scheduling_benchmark_evidence(db_session):
    evidence = [
        (
            "Rosters / Patterns / Scheduling are governed expected-time configuration and work-pattern evidence that "
            "can support ordinary hours, leave basis, public holiday treatment, PayRun processing context, Worker "
            "Story explanation and readiness evidence.",
            "Developer Log - Rosters Patterns Scheduling Purpose",
        ),
        (
            "Pattern, PatternDay and EmployeeAppointmentPattern source data provide roster schedule configuration, "
            "expected work context and governed configuration evidence for Rosters / Patterns / Scheduling.",
            "Developer Log - Rosters Patterns Scheduling Source Configuration",
        ),
        (
            "Roster and pattern applicability depends on EmployeeAppointment, WorksitePosition, Worksite, state, "
            "public holiday context, assignment context and applicability context rather than a generic worker date.",
            "Developer Log - Rosters Patterns Scheduling Appointment Worksite",
        ),
        (
            "Ordinary hours, ordinary-hours expectations, leave basis minutes, schedule pattern relationship, public "
            "holiday context and leave interaction can be supported by roster evidence. Deferred roster-based basis "
            "performance and hardening should remain status-honest.",
            "Developer Log - Rosters Patterns Scheduling Ordinary Hours Leave",
        ),
        (
            "Scheduling context can support payroll interpretation, ObjectTime comparison, source truth review, "
            "expected schedule versus actual worked time, actual/source time rows, ObjectTime as actual source evidence, "
            "Worker Story, Decision Story and Payroll Output explanation without becoming payroll calculation authority.",
            "Developer Log - Rosters Patterns Scheduling Payroll Story",
        ),
        (
            "Worker Attention, PayRun Admin Queue, Admin Queue and Finalisation Readiness can surface missing schedule, "
            "missing pattern, configuration gaps, readiness evidence, NEEDS_CONFIGURATION, NEEDS_CONFIGURATION-style "
            "concepts and status honesty around missing schedule context where formal evidence supports those relationships.",
            "Developer Log - Rosters Patterns Scheduling Readiness",
        ),
        (
            "Minerva explains Rosters / Patterns / Scheduling but does not create rosters, change worker schedules, "
            "mutate Pattern, PatternDay or EmployeeAppointmentPattern truth, mutate ObjectTime, calculate payroll, "
            "decide entitlements, calculate leave, approve leave, determine finalisation readiness, finalise PayRuns "
            "or mutate operational workforce/payroll/leave truth.",
            "Platform Doctrine - Rosters Patterns Scheduling Minerva Boundary",
        ),
        (
            "Current status and outstanding hardening should remain honest for Rosters / Patterns / Scheduling where "
            "formal evidence is partial around roster-based basis performance, schedule configuration, ordinary hours, "
            "leave basis, public holiday treatment and readiness surfaces.",
            "Developer Log - Rosters Patterns Scheduling Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_award_positions_classifications_benchmark_evidence(db_session):
    evidence = [
        (
            "Award Positions / Classifications are governed employment classification evidence that connects award "
            "build, EmployeeAppointment, WorksitePosition, Position, payroll interpretation, RateSource and Rate Story, "
            "Decision Story, Worker Story, comparison/remediation and readiness evidence.",
            "Developer Log - Award Positions Classifications Purpose",
        ),
        (
            "AwardPosition, AwardPositionClass, PositionClass, classification levels, position groups, pay guide and "
            "class evidence come from award build extraction and configuration. Deterministic extraction hardening "
            "and status honesty remain important.",
            "Developer Log - Award Positions Classifications Source Build",
        ),
        (
            "EmployeeAppointment connects through WorksitePosition, Position and Worksite worker assignment, assignment "
            "context and employment classification evidence to the relevant award classification.",
            "Developer Log - Award Positions Classifications Assignment",
        ),
        (
            "Classification context supports payroll interpretation, RateSource selection, Rate Story, Decision Story, "
            "Payroll Output and calculated line evidence, while deterministic payroll services decide runtime outcomes.",
            "Developer Log - Award Positions Classifications Payroll Story",
        ),
        (
            "Comparator classification, award comparison, comparison remediation, imported classification mapping, "
            "classification lenses, comparison classes and primary appointment class evidence support comparison review. "
            "Comparison classes do not automatically replace the primary appointment class.",
            "Developer Log - Award Positions Classifications Comparison",
        ),
        (
            "Worker Story, PayRun Admin Queue, Admin Queue, Worker Attention and Finalisation Readiness can surface "
            "classification evidence, configuration gaps, NEEDS_CONFIGURATION and evidence visibility.",
            "Developer Log - Award Positions Classifications Readiness",
        ),
        (
            "Minerva explains Award Positions / Classifications but does not classify workers, change appointments, "
            "change EmployeeAppointment, WorksitePosition, Position or AwardPositionClass records, select award classes "
            "at runtime, interpret awards at runtime, calculate payroll, decide entitlements, mutate payroll output, "
            "determine finalisation readiness, finalise PayRuns or mutate operational workforce/payroll/award truth.",
            "Platform Doctrine - Award Positions Classifications Minerva Boundary",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_payment_execution_remittance_benchmark_evidence(db_session):
    evidence = [
        (
            "Payment Execution / Remittance is governed payment execution and remittance evidence that turns finalised "
            "payroll outcome into payment and remittance action, not a generic file export.",
            "Developer Log - Payment Execution Purpose",
        ),
        (
            "Payment Execution / Remittance consumes finalised gross-to-net, finalised payroll outcome and payment "
            "outcome evidence; it is not payroll calculation truth.",
            "Developer Log - Payment Execution Finalised Gross Net Source",
        ),
        (
            "Worker net pay requires payment allocation, bank allocation and bank instruction readiness before complete "
            "payment execution.",
            "Developer Log - Payment Execution Worker Net Pay Allocation",
        ),
        (
            "Payment destination readiness matters because missing payment destination or partial payment destinations "
            "may block complete payment execution without invalidating gross-to-net calculation.",
            "Developer Log - Payment Destination Readiness",
        ),
        (
            "Negative net pay is a governed outcome that may interact with obligations, carry-forward, recovery, "
            "write-off and out-of-pay treatment.",
            "Developer Log - Payment Negative Net Pay Obligation",
        ),
        (
            "Deduction remittance and third-party remittance can require third-party payments, payment destinations, "
            "remittance files and reconciliation.",
            "Developer Log - Deduction Third Party Remittance",
        ),
        (
            "Generate Bank File, Bank File, payment file, payment-file execution and Period Close remain governed "
            "payment execution concerns.",
            "Developer Log - Payment File Period Close",
        ),
        (
            "Remittance batching, remittance batch handling, remittance reconciliation and reconciliation should be "
            "visible for remittance evidence.",
            "Developer Log - Remittance Batching Reconciliation",
        ),
        (
            "Payment Execution / Remittance should connect to Worker Attention and PayRun Admin Queue so blockers, "
            "warnings and actions are surfaced.",
            "Developer Log - Payment Worker Attention Admin Queue",
        ),
        (
            "Payment Execution / Remittance should connect to Worker Story and audit evidence for payment allocation, "
            "remittance, skipped, unpaid and unmet amounts.",
            "Developer Log - Payment Worker Story Audit Evidence",
        ),
        (
            "Payment Execution / Remittance outstanding hardening remains around bank file generation, remittance "
            "execution, reconciliation, payment close, obligation write-off financial consequences and UI surfaces.",
            "Developer Log - Payment Execution Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_leave_accrual_processing_benchmark_evidence(db_session):
    evidence = [
        (
            "Leave Accrual / Processing uses Leave Accrual and Leave Processing as deterministic platform outcomes, "
            "not Minerva calculations or generic leave policy advice.",
            "Developer Log - Leave Accrual Processing Purpose",
        ),
        (
            "Leave source truth and applicability decide accrual eligibility; LeaveTypeRule alone is not final "
            "applicability truth and Leave Source Model remains outstanding where formal evidence says so.",
            "Developer Log - Leave Source Truth Applicability",
        ),
        (
            "Accrual basis uses PER_HOUR baseline with minute and hour based accrual quantity where supported.",
            "Developer Log - Leave Accrual Basis Quantity",
        ),
        (
            "Canonical processed payroll result truth such as CalcInterpreterLine and current-effective payroll output "
            "should provide accrual quantity where applicable.",
            "Developer Log - Leave Payroll Output Calc Interpreter",
        ),
        (
            "LeaveType, LeaveTypeRule, AwardRateType-first accrualability and RateType fallback are baseline "
            "configuration directions where formal evidence supports them.",
            "Developer Log - Leave Type Rule Configuration",
        ),
        (
            "LeaveLedger and Leave Ledger record leave accrual, payment and balance movements and should preserve "
            "explanation story evidence.",
            "Developer Log - Leave Ledger Posting",
        ),
        (
            "Leave valuation basis supports TAKEN leave valuation and mandatory valuation should hard failure rather "
            "than silent fallback.",
            "Developer Log - Leave Valuation Basis",
        ),
        (
            "Leave request payment effects occur before payroll interpretation or within payroll interpretation, "
            "while leave accrual occurs after payroll interpretation.",
            "Developer Log - Leave Request Payment Effects",
        ),
        (
            "LeaveProcessRun and PayRun processing should surface finalisation readiness, leave readiness and missing "
            "leave output honestly.",
            "Developer Log - Leave PayRun Processing Finalisation",
        ),
        (
            "Worker Story should explain Leave and Accrual Outcome using server-owned leave output, ledger and "
            "valuation evidence.",
            "Developer Log - Leave Worker Story",
        ),
        (
            "Payroll Bases & Totals may provide governed basis evidence for worked hours, basis quantity and leave "
            "basis quantities.",
            "Developer Log - Leave Payroll Bases",
        ),
        (
            "Leave Accrual / Processing outstanding hardening includes Leave Source Model, full leave-processing "
            "UI/runs, leave request ownership contact-vs-appointment design, leave story polish and finalisation "
            "warning acknowledgement.",
            "Developer Log - Leave Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_finalisation_readiness_benchmark_evidence(db_session):
    evidence = [
        (
            "Finalisation Readiness is the governed readiness gate and assurance gate for whether a PayRun can be "
            "finalised safely; it is not payroll calculation truth and not a simple green means done status.",
            "Developer Log - Finalisation Readiness Purpose",
        ),
        (
            "Finalisation Readiness uses blockers and warnings: red blockers prevent the relevant action, amber "
            "warnings require governed review, and green means ready or cleared for that evidence dimension.",
            "Developer Log - Finalisation Blockers Warnings Green",
        ),
        (
            "Current-effective payroll output matters because stale or superseded PayRun output must not be finalised "
            "as current truth.",
            "Developer Log - Finalisation Current Effective Output",
        ),
        (
            "Worker Attention and Admin Queue surface worker-level blockers, worker-level warnings and ready actions.",
            "Developer Log - Finalisation Worker Attention Admin Queue",
        ),
        (
            "Payroll Bases readiness and Payroll Bases & Totals readiness matter where unresolved basis evidence or "
            "stale basis evidence can affect finalisation.",
            "Developer Log - Finalisation Payroll Bases Readiness",
        ),
        (
            "Leave readiness must surface missing leave output, LeaveLedger evidence or leave valuation basis issues "
            "honestly, including TAKEN leave valuation concerns.",
            "Developer Log - Finalisation Leave Readiness",
        ),
        (
            "Tax readiness, deduction readiness, negative net pay, payment destination readiness and gross-to-net "
            "readiness can affect finalisation or payment execution depending on policy.",
            "Developer Log - Finalisation Tax Deduction Payment Readiness",
        ),
        (
            "Payment execution readiness, payment readiness and bank readiness are related to but distinct from "
            "gross-to-net readiness and payment destination readiness.",
            "Developer Log - Finalisation Payment Execution Readiness",
        ),
        (
            "Finalised outcome truth, finalised outcome and finalised totals should become durable payment outcome "
            "memory and finalised payroll truth once finalised.",
            "Developer Log - Finalisation Outcome Truth",
        ),
        (
            "Warning acknowledgement, warning acknowledgment and finalisation audit evidence must preserve what was "
            "reviewed, accepted or unresolved.",
            "Developer Log - Finalisation Warning Acknowledgement Audit",
        ),
        (
            "Worker Story and review surfaces such as Movement Review and Admin Queue should explain readiness evidence "
            "and worker-specific issues.",
            "Developer Log - Finalisation Worker Story Review Surfaces",
        ),
        (
            "Finalisation Readiness outstanding hardening remains around warning acknowledgement, WorkerAttention "
            "schemas, finalisation policy, server-owned operation and readiness evidence, payment execution readiness "
            "and broader contract tests.",
            "Developer Log - Finalisation Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_leave_source_model_benchmark_evidence(db_session):
    evidence = [
        (
            "Leave Source Model is the governed applicability and source-truth layer for determining whether leave "
            "applies to a worker context.",
            "Developer Log - Leave Source Model Purpose",
        ),
        (
            "Applicability is separate from rule content: LeaveTypeRule is policy calculation content and not the "
            "whole source truth.",
            "Developer Log - Leave Source Applicability Rule Content",
        ),
        (
            "LeaveTypeRule must not be treated as final applicability truth; every active LeaveTypeRule does not mean "
            "every worker should have leave output.",
            "Developer Log - Leave Source Rule Limitations",
        ),
        (
            "Contact scope, EmployeeAppointment scope, contact-level and appointment-level ownership require "
            "appointment-aware leave handling.",
            "Developer Log - Leave Source Contact Appointment Scope",
        ),
        (
            "Leave applicability may depend on Account, EmploymentType, WorksitePosition, Worksite, "
            "EmployeeAppointment, Contact, AwardPositionClass, AwardPosition, Position, Award, State and precedence.",
            "Developer Log - Leave Source Dimensions Precedence",
        ),
        (
            "Leave accrual should consume source applicability decisions instead of trying to infer ad hoc source "
            "truth during accrual.",
            "Developer Log - Leave Source Accrual Connection",
        ),
        (
            "Leave request and payment effects should consume source applicability decisions and respect leave "
            "ownership and request ownership.",
            "Developer Log - Leave Source Request Payment Effects",
        ),
        (
            "Worker Story leave chapters should explain source applicability decisions where leave output or warnings "
            "are shown.",
            "Developer Log - Leave Source Worker Story",
        ),
        (
            "Command Centre and Finalisation Readiness should surface leave readiness and PayRun finalisation warnings "
            "honestly.",
            "Developer Log - Leave Source Command Centre Finalisation",
        ),
        (
            "Leave readiness should distinguish no leave entitlement and leave does not apply from leave output is "
            "missing so missing leave output is not automatically wrong without source truth.",
            "Developer Log - Leave Source Missing Output Detection",
        ),
        (
            "Leave Source Model outstanding hardening remains because it is a planned model and required model, not "
            "complete runtime capability unless formal evidence says so.",
            "Developer Log - Leave Source Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_oncosts_employer_liabilities_benchmark_evidence(db_session):
    evidence = [
        (
            "On-costs and Employer Liabilities are governed employer liability evidence with operator meaning, "
            "not ordinary worker pay and not a reporting add-on.",
            "Developer Log - On-costs Employer Liabilities Purpose",
        ),
        (
            "Employer liability evidence is not worker pay, not worker net pay and not payroll calculation truth; "
            "Minerva does not calculate on-costs.",
            "Developer Log - On-costs Worker Pay Boundary",
        ),
        (
            "RateSource and date-effective rates should live in date-effective RateSource rule-pack configuration "
            "rather than application code, with production truth governed outside code constants.",
            "Developer Log - On-costs RateSource Date Effective",
        ),
        (
            "AwardRateType settings and RateType defaults drive SUPER_ONCOST, PAYROLLTAX_ONCOST and "
            "WORKCOVER_ONCOST; AwardRateType can inherit defaults at build time and diverge by award.",
            "Developer Log - On-costs AwardRateType RateType",
        ),
        (
            "Governed basis membership, bucket membership and basis membership matter because raw flags may seed "
            "defaults, but runtime basis decisions should resolve from governed membership where implemented.",
            "Developer Log - On-costs Governed Basis Membership",
        ),
        (
            "Superannuation on-cost, payroll tax on-cost, WorkCover and WIC have different basis and jurisdiction "
            "implications.",
            "Developer Log - On-costs Liability Types",
        ),
        (
            "State, worksite and runtime location resolution matter for state-scoped RateSource selection and "
            "state-scoped employer liabilities; runtime state and worksite resolution remain outstanding.",
            "Developer Log - On-costs Runtime Location",
        ),
        (
            "PayRun output and Worker Story should distinguish worker-payable lines from employer liability lines "
            "and on-cost evidence.",
            "Developer Log - On-costs PayRun Worker Story",
        ),
        (
            "Payroll Bases & Totals can provide governed basis evidence, basis evidence and basis totals for "
            "liability calculations.",
            "Developer Log - On-costs Payroll Bases",
        ),
        (
            "Finalisation Readiness may depend on unresolved basis or liability configuration where policy requires "
            "that readiness evidence.",
            "Developer Log - On-costs Finalisation Readiness",
        ),
        (
            "Demo fallback account-wide fallback RateSource rows may unblock demos but are not production truth.",
            "Developer Log - On-costs Demo Fallback",
        ),
        (
            "Outstanding hardening remains around runtime state worksite resolution, award creation seeding, "
            "governed basis membership, product tests and production replacement of demo fallback.",
            "Developer Log - On-costs Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_award_build_evidence_benchmark_evidence(db_session):
    evidence = [
        (
            "Award Build and Award Evidence are governed configuration and traceable evidence creation, not runtime "
            "payroll calculation by Minerva.",
            "Developer Log - Award Build Purpose",
        ),
        (
            "Award documents and pay guide evidence are source evidence; build artifacts should preserve row column "
            "page evidence.",
            "Developer Log - Award Document Pay Guide Sources",
        ),
        (
            "RateType is the stable conceptual pay type while AwardRateType is award-scoped treatment and "
            "configuration.",
            "Developer Log - Award RateType AwardRateType",
        ),
        (
            "RateSource stores date-effective rate amounts and rate evidence and must not be replaced by hardcoded "
            "rates.",
            "Developer Log - Award RateSource Evidence",
        ),
        (
            "Classification, position and class evidence should be deterministically derived or reviewed, not guessed.",
            "Developer Log - Award Classification Evidence",
        ),
        (
            "Allowances, penalties, conditions, shift and overtime rules need source evidence and status-honest "
            "configuration.",
            "Developer Log - Award Allowance Penalty Conditions",
        ),
        (
            "DecisionEvidenceIndex and Decision Evidence Index support why a treatment and why a line exists.",
            "Developer Log - Award Decision Evidence Index",
        ),
        (
            "RateSourceEvidenceIndex and Rate Source Evidence Index support why a rate and why an amount was used.",
            "Developer Log - Award Rate Source Evidence Index",
        ),
        (
            "Worker Story should use Decision Story and Rate Story evidence from award build and runtime artifacts "
            "for PayRun interpretation evidence.",
            "Developer Log - Award Worker Story Connection",
        ),
        (
            "NEEDS_CONFIGURATION is a valid award build status and valid build outcome where missing evidence or "
            "missing configuration remains.",
            "Developer Log - Award Needs Configuration",
        ),
        (
            "AwardEvidenceSet and Durable AwardEvidenceSet remain future hardening where durable evidence is still "
            "artifact based or file based.",
            "Developer Log - Award Evidence Set",
        ),
        (
            "Outstanding hardening remains around semantic table classification, durable evidence sets, code/test "
            "verification, parser routing, conditional award regimes and source evidence coverage.",
            "Developer Log - Award Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_imports_actuals_benchmark_evidence(db_session):
    evidence = [
        (
            "Imports / Actuals and Imports and Actuals are governed imported evidence and external source evidence, "
            "not calculated interpreter truth.",
            "Developer Log - Imports Actuals Purpose",
        ),
        (
            "Imported timesheets may become ObjectTime work evidence and timesheet source truth only after validation "
            "and mapping.",
            "Developer Log - Imports Actuals Timesheets",
        ),
        (
            "Imported payroll actuals and payroll actuals are an actuals lane and external outcome lane, not "
            "calculated interpreter output.",
            "Developer Log - Imports Actuals Lane",
        ),
        (
            "Source-system mapping and source system mapping require validation for workers, dates and source rows.",
            "Developer Log - Imports Actuals Source System Mapping",
        ),
        (
            "Pay code mapping, source-system pay code mapping and RateType mapping connect external pay codes to "
            "platform concepts; unmapped actuals should surface as deterministic issues.",
            "Developer Log - Imports Actuals Pay Code RateType",
        ),
        (
            "ImportedPositionClassificationMap, position mapping and classification mapping matter for "
            "source-system classification and source-system position evidence.",
            "Developer Log - Imports Actuals Position Classification",
        ),
        (
            "ObjectTime source truth must preserve source truth, source row and import provenance from imported "
            "source rows.",
            "Developer Log - Imports Actuals ObjectTime Source Truth",
        ),
        (
            "Comparison / Remediation can compare primary calculated, comparator calculated and imported actual "
            "lanes when explaining variance.",
            "Developer Log - Imports Actuals Comparison Remediation",
        ),
        (
            "Reconciliation and Movement Review use imported actuals and source evidence to explain variance and "
            "review outcomes.",
            "Developer Log - Imports Actuals Reconciliation Movement Review",
        ),
        (
            "Worker Story and Admin Queue should surface import provenance, mapping issues, unmapped actuals, "
            "missing classifications and review actions.",
            "Developer Log - Imports Actuals Worker Story Admin Queue",
        ),
        (
            "Evidence provenance and audit should preserve source file, source row, import run, mapping decision, "
            "validation status and story evidence.",
            "Developer Log - Imports Actuals Provenance Audit",
        ),
        (
            "Outstanding hardening remains around actuals lane model, import mapping UI, comparison-line models, "
            "source-system classification mapping, source-row evidence and validation workflows.",
            "Developer Log - Imports Actuals Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_objecttime_source_truth_benchmark_evidence(db_session):
    evidence = [
        (
            "ObjectTime / Source Truth and ObjectTime Source Truth are governed source evidence for work time and "
            "source-row inclusion, not payroll calculation truth and not user-facing worked hours.",
            "Developer Log - ObjectTime Source Truth Purpose",
        ),
        (
            "ObjectTime acts as source evidence with source row and inclusion context for work time.",
            "Developer Log - ObjectTime Source Evidence",
        ),
        (
            "PayRun inclusion uses SourceTruth and Source Truth source inclusion to explain why a worker source row "
            "belongs in a PayRun.",
            "Developer Log - ObjectTime PayRun Inclusion",
        ),
        (
            "Imported source rows and generated source rows must preserve provenance and validation mapping status.",
            "Developer Log - ObjectTime Imported Generated Rows",
        ),
        (
            "SourceTruth and WorkedHours are separate; raw span hours and span hours are not interpreted payable "
            "hours or worked hours.",
            "Developer Log - ObjectTime Worked Hours Boundary",
        ),
        (
            "Current-effective output and current-effective payroll output connect processed source truth to payroll "
            "outcome and current-effective truth.",
            "Developer Log - ObjectTime Current Effective Output",
        ),
        (
            "Worker Story should begin with Source Truth and source inclusion before calculated payroll outcome and "
            "Decision Story.",
            "Developer Log - ObjectTime Worker Story",
        ),
        (
            "Payroll Bases & Totals and leave accrual should consume governed processed payroll and bucket evidence, "
            "not raw source span duration.",
            "Developer Log - ObjectTime Payroll Bases Leave",
        ),
        (
            "Comparison / Remediation, Movement Review and Retro / Replay depend on source truth, provenance and "
            "historical current-effective distinctions.",
            "Developer Log - ObjectTime Comparison Movement Replay",
        ),
        (
            "Correction audit and source truth correction should mark dirty contact and dirty PayRunContact records "
            "for governed reprocessing.",
            "Developer Log - ObjectTime Corrections Dirty Contacts",
        ),
        (
            "Evidence provenance and audit should preserve source file, source row, ObjectTime, correction history "
            "and evidence story.",
            "Developer Log - ObjectTime Provenance Audit",
        ),
        (
            "Outstanding hardening remains around command-centre source hours cleanup, schema contracts, dependency "
            "detection and source-truth provenance coverage.",
            "Developer Log - ObjectTime Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_contacts_employee_appointments_benchmark_evidence(db_session):
    evidence = [
        (
            "Contacts / Employee Appointments use Contact and EmployeeAppointment as governed worker identity "
            "context and employment context, not payroll calculation truth or a generic HR profile.",
            "Developer Log - Contacts Appointments Purpose",
        ),
        (
            "Contact is the worker identity, person payroll identity, worker context and payroll identity context.",
            "Developer Log - Contacts Worker Identity",
        ),
        (
            "EmployeeAppointment and Employee Appointment are the employment assignment and work assignment; "
            "appointment context can carry position worksite classification award dimensions.",
            "Developer Log - Employee Appointment Assignment",
        ),
        (
            "Appointment scope and PayRun admission use source truth, appointment context and worker inclusion.",
            "Developer Log - Contacts PayRun Admission",
        ),
        (
            "Award classification, AwardPositionClass, WorksitePosition, Position and classification evidence belong "
            "under appointment context where appointment-specific truth matters.",
            "Developer Log - Contacts Award Classification Position",
        ),
        (
            "Worksite, state, runtime location, worksite state and state evidence matter for appointment payroll, "
            "award and employer-liability contexts.",
            "Developer Log - Contacts Worksite State Runtime Location",
        ),
        (
            "ObjectTime and source truth source rows connect appointments and contacts to worker inclusion.",
            "Developer Log - Contacts ObjectTime Source Truth",
        ),
        (
            "Leave source, leave applicability and leave accrual may depend on contact scope versus appointment scope.",
            "Developer Log - Contacts Leave Source Accrual",
        ),
        (
            "Worker Story should surface source truth context, and Contact history should eventually surface finalised "
            "payroll outcome memory and cumulative movement.",
            "Developer Log - Contacts Worker Story History",
        ),
        (
            "Worker readiness includes contact-level tax declarations, bank, payment allocation, deductions and "
            "obligations evidence surfaces.",
            "Developer Log - Contacts Worker Readiness",
        ),
        (
            "Dirty contact and dirty contacts mean payroll-affecting changes can make current PayRun output unsafe "
            "until governed reprocessing.",
            "Developer Log - Contacts Dirty Reprocessing",
        ),
        (
            "Comparison and remediation may need classification lens and classification lenses under the appointment "
            "rather than duplicate full appointments.",
            "Developer Log - Contacts Classification Lenses",
        ),
        (
            "Outstanding hardening remains around GUID boundary, schema contracts, contact-level history, "
            "WorkerAttention schemas, appointment classification lenses, leave request ownership, source-truth "
            "provenance and dirty-contact propagation.",
            "Developer Log - Contacts Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_process_period_payrun_lifecycle_benchmark_evidence(db_session):
    evidence = [
        (
            "Process Periods / PayRun Lifecycle uses ProcessPeriod as governed payroll-period context and "
            "payment-event lifecycle evidence, not payroll calculation truth and not a generic date range.",
            "Developer Log - Process Period Lifecycle Purpose",
        ),
        (
            "ProcessPeriod and Process Period use ProcessPeriodGroup and Process Period Group for recurring calendar "
            "policy and payment policy context.",
            "Developer Log - Process Period Group Context",
        ),
        (
            "Open, not-open, not open and closed are distinct period lifecycle states, and closed dominates open.",
            "Developer Log - Process Period Open Closed Lifecycle",
        ),
        (
            "Close rolls forward and roll forward period close may close period state then open next period or create "
            "next period where implemented.",
            "Developer Log - Process Period Close Rolls Forward",
        ),
        (
            "PaymentDate and payment date matter for tax/PAYG and payment context and should be governed derived "
            "calendar policy, not hardcoded.",
            "Developer Log - Process Period PaymentDate",
        ),
        (
            "PayRun creation and PayRun admission happen inside process-period context for worker inclusion and "
            "payment event setup, but admission is not processing.",
            "Developer Log - Process Period PayRun Admission",
        ),
        (
            "RunType and RunPurpose should remain separate run type and run purpose evidence for each "
            "payment/processing event.",
            "Developer Log - PayRun RunType RunPurpose",
        ),
        (
            "Regular PayRun, supplementary PayRun, retro PayRun, termination PayRun, reversal PayRun and adjustment "
            "PayRun are different lifecycle concepts.",
            "Developer Log - PayRun Run Type Distinctions",
        ),
        (
            "PayRunContact is the operational state layer for worker participation, admission and processing state; "
            "dirty PayRunContact records can require review.",
            "Developer Log - PayRunContact Lifecycle",
        ),
        (
            "Current-effective output and current-effective payroll output matter because stale and superseded runs "
            "must not present as current truth for finalisation readiness.",
            "Developer Log - Process Period Current Effective Output",
        ),
        (
            "Finalisation readiness consumes payroll, leave, tax, deductions, payment, bases and worker issues; "
            "payment execution and period close are downstream governed outcomes, not payroll calculation.",
            "Developer Log - Process Period Finalisation Payment Close",
        ),
        (
            "Worker Story, PayRun Admin Queue, Admin Queue and Movement Review should explain worker participation, "
            "readiness and review implications.",
            "Developer Log - Process Period Review Connections",
        ),
        (
            "Outstanding hardening remains around operation trackers, lifecycle contracts, supplementary/retro "
            "policies, payment execution, finalisation warning acknowledgement and broader contract tests.",
            "Developer Log - Process Period Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def _ingest_costing_gl_consequence_benchmark_evidence(db_session):
    evidence = [
        (
            "Costing / GL Consequence Evidence and Costing GL consequence are downstream financial consequence "
            "evidence, not payroll calculation truth, not payment execution and not a completed costing engine.",
            "Developer Log - Costing GL Purpose",
        ),
        (
            "Costing should consume finalised payroll outcome truth, finalised payroll outcome, finalised payroll "
            "outcomes, finalised gross-to-net, payment outcome and liability truth rather than block payroll close or "
            "payment execution performance.",
            "Developer Log - Costing Finalised Outcome Source",
        ),
        (
            "Payment Execution / Remittance, payment execution, remittance, downstream payment and period close can "
            "create financial consequence evidence but remain separate from costing.",
            "Developer Log - Costing Payment Execution Remittance",
        ),
        (
            "Employer liabilities, employer liability, on-costs, on costs, super, payroll tax, WorkCover and WIC can "
            "have costing or GL consequences.",
            "Developer Log - Costing Employer Liability Oncost",
        ),
        (
            "Deductions, deduction obligations and obligations can have financial consequences; obligation write-off, "
            "obligation writeoff, forgiveness, balance reduction and material adjustment may require "
            "GL/provision/costing treatment.",
            "Developer Log - Costing Obligation Writeoff",
        ),
        (
            "Comparison / Remediation remediation variance, variance line and remediation top-up evidence may need "
            "downstream treatment, downstream tax, super, payroll tax, WIC, leave, deduction and costing treatment.",
            "Developer Log - Costing Remediation Variance",
        ),
        (
            "Leave valuation, leave accrual, leave valuation basis, LeaveLedger and accrual evidence may eventually "
            "flow to costing.",
            "Developer Log - Costing Leave Valuation Accrual",
        ),
        (
            "Negative net pay may create recoveries, obligations, write-offs or out-of-pay and out of pay records "
            "with financial consequences.",
            "Developer Log - Costing Negative Net Pay",
        ),
        (
            "Audit story and financial evidence should preserve source outcome, reason, treatment, amount, ledger "
            "status, costing status and deferred accounting design status.",
            "Developer Log - Costing Audit Story",
        ),
        (
            "Deferred/final slice, deferred costing slice, future costing slice and later/final slice language means "
            "status-honest deferred accounting design, not completed costing engine and not a payroll-processing "
            "blocker.",
            "Developer Log - Costing Deferred Slice",
        ),
        (
            "Minerva explains evidence and status, does not post GL entries and does not calculate costing.",
            "Platform Doctrine - Costing Minerva Boundary",
        ),
        (
            "Outstanding hardening remains around costing engine, GL posting, remediation downstream treatment, "
            "negative net pay financial treatment, obligation write-off handling and contract tests.",
            "Developer Log - Costing Outstanding Hardening",
        ),
    ]
    for text, title in evidence:
        _ingest(db_session, text, title=title)


def test_answer_mode_classification_examples():
    assert classify_answer_mode("What is Minerva not allowed to do?") == AnswerMode.DOCTRINE.value
    assert classify_answer_mode("How is Annual Leave managed in the system?") == AnswerMode.PRODUCT_DOMAIN.value
    assert classify_answer_mode("Estimate my leave balance") == AnswerMode.WORKER_FACING.value
    assert classify_answer_mode("Why is worker leave balance wrong?") == AnswerMode.TECHNICAL_SUPPORT.value
    assert classify_answer_mode("Which hardening item explains this?") == AnswerMode.DEVELOPER_PLATFORM.value


def test_rich_answer_plan_is_lightweight_internal_structure():
    plan = RichAnswerPlan(
        answer_mode=AnswerMode.PRODUCT_DOMAIN.value,
        direct_summary="Annual Leave is managed through formal leave services.",
        system_operation_points=["LeaveLedger records accrual and TAKEN rows."],
    )

    assert plan.model_dump()["answer_mode"] == "PRODUCT_DOMAIN"
    assert plan.model_dump()["system_operation_points"] == ["LeaveLedger records accrual and TAKEN rows."]


def test_golden_evaluator_checks_required_answer_sections(db_session, tmp_path):
    _ingest(
        db_session,
        "Annual Leave management uses LeaveType and LeaveTypeRule. LeaveLedger records accrual and TAKEN rows. "
        "PayRun processing includes public holiday valuation evidence and Worker Story output. "
        "The Developer Log also records outstanding hardening for valuation.",
    )
    manifest_path = _manifest(
        tmp_path,
        [
            {
                "id": "rich-sections",
                "question": "How is Annual Leave managed in the system?",
                "answer_mode": "PRODUCT_DOMAIN",
                "expected_source_types": ["DEVELOPER_LOG"],
                "required_answer_sections": [
                    "Direct summary",
                    "How the system works",
                    "Current implementation status",
                    "What remains outstanding",
                ],
                "expected_answer_terms_all": ["LeaveType", "LeaveLedger", "PayRun"],
            }
        ],
    )

    result = run_golden_questions(db_session, manifest_path)

    assert result["all_passed"] is True
    assert result["results"][0]["checks"]["answer_mode"] is True
    assert result["results"][0]["checks"]["required_answer_sections"] is True


def test_golden_evaluator_fails_when_required_answer_section_missing(db_session, tmp_path):
    _ingest(db_session, "General evidence about Annual Leave and LeaveLedger.")
    manifest_path = _manifest(
        tmp_path,
        [
            {
                "id": "missing-section",
                "question": "How is Annual Leave managed in the system?",
                "answer_mode": "PRODUCT_DOMAIN",
                "expected_source_types": ["DEVELOPER_LOG"],
                "required_answer_sections": ["Direct summary", "Intentionally Missing Section"],
            }
        ],
    )

    result = run_golden_questions(db_session, manifest_path)

    assert result["all_passed"] is False
    assert result["results"][0]["checks"]["required_answer_sections"] is False


def test_golden_evaluator_fails_when_forbidden_answer_pattern_matches(db_session, tmp_path):
    _ingest(
        db_session,
        "Annual Leave management uses LeaveType and LeaveTypeRule. LeaveLedger records accrual and TAKEN rows. "
        "PayRun public holiday valuation evidence is shown in Worker Story.",
    )
    manifest_path = _manifest(
        tmp_path,
        [
            {
                "id": "forbidden-pattern",
                "question": "How is Annual Leave managed in the system?",
                "answer_mode": "PRODUCT_DOMAIN",
                "expected_source_types": ["DEVELOPER_LOG"],
                "forbidden_answer_patterns_any": ["Direct\\s+summary"],
            }
        ],
    )

    result = run_golden_questions(db_session, manifest_path)

    assert result["all_passed"] is False
    assert result["results"][0]["checks"]["forbidden_answer_patterns_any"] is False


def test_rich_answer_benchmark_manifest_loads_and_can_be_evaluated(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.annual_leave.json")

    assert manifest["name"] == "Annual Leave rich-answer benchmark"
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.annual_leave.json")
    assert result["total"] == 1
    assert result["results"][0]["checks"]["answer_mode"] is True


def test_worker_story_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.worker_story.json")

    assert manifest["name"] == "Worker Story rich-answer benchmark"
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.worker_story.json")
    assert result["total"] == 5
    assert result["results"][0]["checks"]["answer_mode"] is True


def test_payroll_bases_and_totals_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.payroll_bases_and_totals.json")

    assert manifest["name"] == "Payroll Bases & Totals rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} >= {
        "payroll-bases-and-totals-rich-answer",
        "payroll-bases-current-effective-truth",
        "payroll-bases-vs-reporting-totals",
        "payroll-bases-bucket-definition-membership",
        "payroll-bases-stale-bucket-results",
        "payroll-bases-worker-story-movement-review",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.payroll_bases_and_totals.json")
    assert result["total"] == 6
    assert result["results"][0]["checks"]["answer_mode"] is True


def test_payrun_admin_queue_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.payrun_admin_queue.json")

    assert manifest["name"] == "PayRun Admin Queue rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} >= {
        "payrun-admin-queue-rich-answer",
        "payrun-admin-queue-vs-command-centre",
        "payrun-admin-queue-cleanliness-assurance",
        "payrun-admin-queue-blockers-warnings-ready",
        "payrun-admin-queue-worker-attention-dirty-contacts",
        "payrun-admin-queue-finalisation-readiness",
        "payrun-admin-queue-assurance-snapshot",
        "payrun-admin-queue-review-surface-connections",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.payrun_admin_queue.json")
    assert result["total"] == 8
    assert result["results"][0]["checks"]["answer_mode"] is True


def test_worker_attention_issue_resolution_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.worker_attention_issue_resolution.json")

    assert manifest["name"] == "Worker Attention / Issue Resolution rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} == {
        "worker-attention-issue-resolution-rich-answer",
        "worker-attention-worker-issue-model",
        "worker-attention-deterministic-fix-links",
        "worker-attention-dirty-contact-reprocessing",
        "worker-attention-payment-allocation-negative-net-pay",
        "worker-attention-admin-queue-worker-story-relationship",
    }
    result = run_golden_questions(
        db_session,
        "samples/eval/rich_answer_benchmark.worker_attention_issue_resolution.json",
    )
    assert result["total"] == 6
    assert all(item["checks"]["answer_mode"] is True for item in result["results"])


def test_gross_to_net_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.gross_to_net.json")

    assert manifest["name"] == "Gross-to-Net rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} == {
        "gross-to-net-rich-answer",
        "gross-to-net-gross-earnings-to-net-pay",
        "gross-to-net-taxable-basis-payg",
        "gross-to-net-deductions-obligations",
        "gross-to-net-negative-net-pay",
        "gross-to-net-current-effective-worker-story",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.gross_to_net.json")
    assert result["total"] == 6
    assert all(item["checks"]["answer_mode"] is True for item in result["results"])


def test_rate_source_rate_story_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.rate_source_rate_story.json")

    assert manifest["name"] == "RateSource / Rate Story rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} == {
        "rate-source-rate-story-rich-answer",
        "rate-source-rate-story-selection",
        "rate-source-rate-story-pay-guide-evidence",
        "rate-source-rate-story-vs-decision-story",
        "rate-source-rate-story-date-effective-scoped-rates",
        "rate-source-rate-story-worker-story-gross-to-net",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.rate_source_rate_story.json")
    assert result["total"] == 6
    assert all(item["checks"]["answer_mode"] is True for item in result["results"])


def test_decision_story_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.decision_story.json")

    assert manifest["name"] == "Decision Story rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} == {
        "decision-story-rich-answer",
        "decision-story-why-line-exists",
        "decision-story-decision-evidence-index",
        "decision-story-vs-rate-story",
        "decision-story-allowance-penalty-overtime-shift",
        "decision-story-break-public-holiday-special-conditions",
        "decision-story-worker-story-gross-to-net",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.decision_story.json")
    assert result["total"] == 7
    assert all(item["checks"]["answer_mode"] is True for item in result["results"])


def test_payroll_output_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.payroll_output.json")

    assert manifest["name"] == "Payroll Output rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} == {
        "payroll-output-rich-answer",
        "payroll-output-current-effective-output",
        "payroll-output-run-vs-process-period-output",
        "payroll-output-payroll-lines",
        "payroll-output-gross-to-net",
        "payroll-output-payroll-bases-totals",
        "payroll-output-finalisation-payment-execution",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.payroll_output.json")
    assert result["total"] == 7
    assert all(item["checks"]["answer_mode"] is True for item in result["results"])


def test_leave_requests_workflow_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.leave_requests_workflow.json")

    assert manifest["name"] == "Leave Requests / Leave Workflow rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} == {
        "leave-requests-workflow-rich-answer",
        "leave-requests-workflow-lifecycle-status",
        "leave-requests-workflow-preview-overlap-shortfall",
        "leave-requests-workflow-taken-valuation",
        "leave-requests-workflow-ledger-balances",
        "leave-requests-workflow-source-applicability",
        "leave-requests-workflow-worker-story-payrun-finalisation",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.leave_requests_workflow.json")
    assert result["total"] == 7
    assert all(item["checks"]["answer_mode"] is True for item in result["results"])


def test_public_holidays_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.public_holidays.json")

    assert manifest["name"] == "Public Holidays rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} == {
        "public-holidays-rich-answer",
        "public-holidays-worker-applicability",
        "public-holidays-payroll-treatment",
        "public-holidays-leave-requests-ledger",
        "public-holidays-worker-story-payroll-evidence",
        "public-holidays-missing-configuration-context",
        "public-holidays-employer-liabilities-oncosts",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.public_holidays.json")
    assert result["total"] == 7
    assert all(item["checks"]["answer_mode"] is True for item in result["results"])


def test_rosters_patterns_scheduling_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.rosters_patterns_scheduling.json")

    assert manifest["name"] == "Rosters / Patterns / Scheduling rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} == {
        "rosters-patterns-scheduling-rich-answer",
        "rosters-patterns-scheduling-expected-work-context",
        "rosters-patterns-scheduling-appointments-worksites",
        "rosters-patterns-scheduling-ordinary-hours-leave-basis",
        "rosters-patterns-scheduling-objecttime-boundary",
        "rosters-patterns-scheduling-worker-story-payroll-evidence",
        "rosters-patterns-scheduling-missing-configuration",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.rosters_patterns_scheduling.json")
    assert result["total"] == 7
    assert all(item["checks"]["answer_mode"] is True for item in result["results"])


def test_award_positions_classifications_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.award_positions_classifications.json")

    assert manifest["name"] == "Award Positions / Classifications rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} == {
        "award-positions-classifications-rich-answer",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.award_positions_classifications.json")
    assert result["total"] == 1
    assert all(item["checks"]["answer_mode"] is True for item in result["results"])


def test_contact_payroll_history_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.contact_payroll_history.json")

    assert manifest["name"] == "Contact Payroll History rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} == {
        "contact-payroll-history-rich-answer",
        "contact-payroll-history-payrun-participation",
        "contact-payroll-history-current-historical-output",
        "contact-payroll-history-deductions-obligations-negative-net-pay",
        "contact-payroll-history-tax-payment-readiness",
        "contact-payroll-history-leave-accrual-worker-story",
        "contact-payroll-history-retro-replay-correction",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.contact_payroll_history.json")
    assert result["total"] == 7
    assert all(item["checks"]["answer_mode"] is True for item in result["results"])


def test_movement_review_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.movement_review.json")

    assert manifest["name"] == "Movement Review rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} >= {
        "movement-review-rich-answer",
        "movement-review-review-worthy-not-error",
        "movement-review-organisation-worker-lenses",
        "movement-review-comparable-periods-variance",
        "movement-review-payroll-bases",
        "movement-review-worker-story",
        "movement-review-admin-queue-assurance",
        "movement-review-trend-only-rolling-ytd",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.movement_review.json")
    assert result["total"] == 8
    assert result["results"][0]["checks"]["answer_mode"] is True


def test_comparison_remediation_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.comparison_remediation.json")

    assert manifest["name"] == "Comparison / Remediation rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} >= {
        "comparison-remediation-rich-answer",
        "comparison-remediation-three-lanes",
        "comparison-remediation-primary-award-path",
        "comparison-remediation-imported-actuals",
        "comparison-remediation-policy",
        "comparison-remediation-evidence-before-variance",
        "comparison-remediation-variance-lines-not-manual",
        "comparison-remediation-classification-mapping",
        "comparison-remediation-surface-connections",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.comparison_remediation.json")
    assert result["total"] == 9
    assert result["results"][0]["checks"]["answer_mode"] is True


def test_tax_payg_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.tax_payg.json")

    assert manifest["name"] == "Tax / PAYG rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} >= {
        "tax-payg-rich-answer",
        "tax-payg-minerva-not-calculate",
        "tax-payg-taxstory-explainability",
        "tax-payg-taxable-basis-payroll-bases",
        "tax-payg-payment-date-context",
        "tax-payg-pay-frequency-support",
        "tax-payg-worker-tax-readiness",
        "tax-payg-supplementary-incremental",
        "tax-payg-worker-story-admin-queue",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.tax_payg.json")
    assert result["total"] == 9
    assert result["results"][0]["checks"]["answer_mode"] is True


def test_deductions_obligations_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.deductions_obligations.json")

    assert manifest["name"] == "Deductions / Obligations rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} >= {
        "deductions-obligations-rich-answer",
        "deductions-obligations-template-chain",
        "deductions-obligations-application-memory",
        "deductions-obligations-supplementary-memory",
        "deductions-obligations-applicability-affordability",
        "deductions-obligations-skipped-partial-unmet",
        "deductions-obligations-deduction-vs-obligation",
        "deductions-obligations-reducing-balance",
        "deductions-obligations-negative-net-pay",
        "deductions-obligations-worker-story-admin-queue",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.deductions_obligations.json")
    assert result["total"] == 10
    assert result["results"][0]["checks"]["answer_mode"] is True


def test_retro_replay_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.retro_replay.json")

    assert manifest["name"] == "Retro / Replay rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} >= {
        "retro-replay-rich-answer",
        "retro-replay-attributed-vs-paid-period",
        "retro-replay-finalised-not-overwritten",
        "retro-replay-current-effective-vs-historical",
        "retro-replay-buckets-basis-snapshots",
        "retro-replay-source-dependency-detection",
        "retro-replay-retro-vs-supplementary-payrun",
        "retro-replay-comparison-remediation",
        "retro-replay-worker-story",
        "retro-replay-admin-queue-movement-review",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.retro_replay.json")
    assert result["total"] == 10
    assert result["results"][0]["checks"]["answer_mode"] is True


def test_payment_execution_remittance_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.payment_execution_remittance.json")

    assert manifest["name"] == "Payment Execution / Remittance rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} >= {
        "payment-execution-remittance-rich-answer",
        "payment-execution-remittance-not-payroll-calculation",
        "payment-execution-remittance-finalised-gross-to-net",
        "payment-execution-remittance-worker-net-pay-bank-allocation",
        "payment-execution-remittance-missing-destinations",
        "payment-execution-remittance-negative-net-pay-obligations",
        "payment-execution-remittance-deduction-third-party",
        "payment-execution-remittance-generate-bank-file-period-close",
        "payment-execution-remittance-batching-reconciliation",
        "payment-execution-remittance-worker-attention-admin-queue-worker-story",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.payment_execution_remittance.json")
    assert result["total"] == 10
    assert result["results"][0]["checks"]["answer_mode"] is True


def test_leave_accrual_processing_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.leave_accrual_processing.json")

    assert manifest["name"] == "Leave Accrual / Processing rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} >= {
        "leave-accrual-processing-rich-answer",
        "leave-accrual-processing-minerva-not-calculate",
        "leave-accrual-processing-source-truth",
        "leave-accrual-processing-calc-interpreter-output",
        "leave-accrual-processing-leavetype-rule-role",
        "leave-accrual-processing-leavetyperule-not-final-applicability",
        "leave-accrual-processing-leaveledger-explanation",
        "leave-accrual-processing-taken-valuation-hard-fail",
        "leave-accrual-processing-request-payment-sequencing",
        "leave-accrual-processing-worker-story-payroll-bases",
        "leave-accrual-processing-payrun-finalisation-readiness",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.leave_accrual_processing.json")
    assert result["total"] == 11
    assert result["results"][0]["checks"]["answer_mode"] is True


def test_finalisation_readiness_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.finalisation_readiness.json")

    assert manifest["name"] == "Finalisation Readiness rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} >= {
        "finalisation-readiness-rich-answer",
        "finalisation-readiness-minerva-not-determine",
        "finalisation-readiness-blockers-warnings-green",
        "finalisation-readiness-current-effective-output",
        "finalisation-readiness-worker-attention-admin-queue",
        "finalisation-readiness-payroll-bases",
        "finalisation-readiness-leave-readiness",
        "finalisation-readiness-tax-deduction-payment",
        "finalisation-readiness-payment-vs-gross-to-net",
        "finalisation-readiness-finalised-outcome-truth",
        "finalisation-readiness-warning-acknowledgement-audit",
        "finalisation-readiness-worker-story-review-surfaces",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.finalisation_readiness.json")
    assert result["total"] == 12
    assert result["results"][0]["checks"]["answer_mode"] is True


def test_leave_source_model_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.leave_source_model.json")

    assert manifest["name"] == "Leave Source Model rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} >= {
        "leave-source-model-rich-answer",
        "leave-source-model-leavetyperule-not-final",
        "leave-source-model-applicability-vs-rule-content",
        "leave-source-model-no-entitlement-vs-missing-output",
        "leave-source-model-contact-vs-appointment",
        "leave-source-model-source-dimensions",
        "leave-source-model-accrual-connection",
        "leave-source-model-request-payment-effects",
        "leave-source-model-worker-story",
        "leave-source-model-command-centre-finalisation",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.leave_source_model.json")
    assert result["total"] == 10
    assert result["results"][0]["checks"]["answer_mode"] is True


def test_oncosts_employer_liabilities_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.oncosts_employer_liabilities.json")

    assert manifest["name"] == "On-costs / Employer Liabilities rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} >= {
        "oncosts-employer-liabilities-rich-answer",
        "oncosts-not-worker-pay",
        "oncosts-minerva-not-calculate",
        "oncosts-ratesource-date-effective",
        "oncosts-award-rate-type-settings",
        "oncosts-governed-basis-membership",
        "oncosts-liability-types-jurisdiction",
        "oncosts-state-worksite-location",
        "oncosts-payrun-output-worker-story",
        "oncosts-payroll-bases-connection",
        "oncosts-demo-fallback-not-production",
        "oncosts-finalisation-readiness",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.oncosts_employer_liabilities.json")
    assert result["total"] == 12
    assert result["results"][0]["checks"]["answer_mode"] is True


def test_award_build_evidence_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.award_build_evidence.json")

    assert manifest["name"] == "Award Build / Award Evidence rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} >= {
        "award-build-evidence-rich-answer",
        "award-build-not-runtime-payroll-calculation",
        "award-build-source-documents-pay-guides",
        "award-build-ratetype-vs-awardratetype",
        "award-build-ratesource-date-effective",
        "award-build-classification-position-class",
        "award-build-allowances-penalties-conditions",
        "award-build-decision-evidence-index",
        "award-build-rate-source-evidence-index",
        "award-build-worker-story-decision-rate-story",
        "award-build-needs-configuration-status",
        "award-build-durable-award-evidence-set",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.award_build_evidence.json")
    assert result["total"] == 12
    assert result["results"][0]["checks"]["answer_mode"] is True


def test_imports_actuals_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.imports_actuals.json")

    assert manifest["name"] == "Imports / Actuals rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} >= {
        "imports-actuals-rich-answer",
        "imports-actuals-external-not-interpreter",
        "imports-actuals-imported-timesheet-source-truth",
        "imports-actuals-source-system-mappings",
        "imports-actuals-pay-code-ratetype-mapping",
        "imports-actuals-position-classification-mapping",
        "imports-actuals-objecttime-source-truth",
        "imports-actuals-comparison-remediation-connection",
        "imports-actuals-reconciliation-movement-review",
        "imports-actuals-worker-story-admin-queue",
        "imports-actuals-provenance-audit",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.imports_actuals.json")
    assert result["total"] == 11
    assert result["results"][0]["checks"]["answer_mode"] is True


def test_objecttime_source_truth_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.objecttime_source_truth.json")

    assert manifest["name"] == "ObjectTime / Source Truth rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} >= {
        "objecttime-source-truth-rich-answer",
        "objecttime-source-evidence-not-calculation",
        "objecttime-payrun-inclusion",
        "objecttime-sourcetruth-vs-workedhours",
        "objecttime-raw-span-not-user-worked-hours",
        "objecttime-imported-generated-source-rows",
        "objecttime-current-effective-output",
        "objecttime-worker-story-source-truth",
        "objecttime-payroll-bases-leave-accrual",
        "objecttime-comparison-movement-replay",
        "objecttime-corrections-dirty-reprocessing",
        "objecttime-provenance-audit",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.objecttime_source_truth.json")
    assert result["total"] == 12
    assert result["results"][0]["checks"]["answer_mode"] is True


def test_contacts_employee_appointments_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.contacts_employee_appointments.json")

    assert manifest["name"] == "Contacts / Employee Appointments rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} >= {
        "contacts-employee-appointments-rich-answer",
        "contacts-vs-employeeappointment",
        "contacts-payrun-admission",
        "contacts-objecttime-source-truth",
        "contacts-award-classification-position-worksite",
        "contacts-worksite-state-runtime-location",
        "contacts-leave-source-accrual",
        "contacts-worker-story-history",
        "contacts-readiness-tax-bank-deduction-payment",
        "contacts-dirty-contact-reprocessing",
        "contacts-classification-lenses-not-duplicate-appointments",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.contacts_employee_appointments.json")
    assert result["total"] == 11
    assert result["results"][0]["checks"]["answer_mode"] is True


def test_process_period_payrun_lifecycle_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.process_period_payrun_lifecycle.json")

    assert manifest["name"] == "Process Periods / PayRun Lifecycle rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} >= {
        "process-period-payrun-lifecycle-rich-answer",
        "process-period-vs-processperiodgroup",
        "process-period-open-not-open-closed",
        "process-period-closed-dominates-open",
        "process-period-close-rolls-forward",
        "process-period-paymentdate",
        "process-period-payrun-creation-admission",
        "process-period-runtype-runpurpose",
        "process-period-regular-supplementary-retro",
        "process-period-payruncontact-lifecycle",
        "process-period-admission-not-processing",
        "process-period-current-effective-output",
        "process-period-lifecycle-cross-domain-connections",
    }
    result = run_golden_questions(
        db_session,
        "samples/eval/rich_answer_benchmark.process_period_payrun_lifecycle.json",
    )
    assert result["total"] == 13
    assert result["results"][0]["checks"]["answer_mode"] is True


def test_costing_gl_consequence_rich_answer_benchmark_manifest_loads(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.costing_gl_consequence.json")

    assert manifest["name"] == "Costing / GL Consequence Evidence rich-answer benchmark"
    assert {question["id"] for question in manifest["questions"]} == {
        "costing-gl-consequence-rich-answer",
        "costing-downstream-of-payroll-calculation",
        "costing-finalised-payroll-outcome-truth",
        "costing-payment-execution-remittance",
        "costing-employer-liabilities-oncosts",
        "costing-deduction-obligation-writeoffs",
        "costing-comparison-remediation-variance",
        "costing-leave-valuation-accrual",
        "costing-negative-net-pay-out-of-pay",
        "costing-audit-story-financial-evidence",
        "costing-deferred-final-slice",
    }
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.costing_gl_consequence.json")
    assert result["total"] == 11
    assert all(item["checks"]["answer_mode"] is True for item in result["results"])


def test_worker_story_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_worker_story_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.worker_story.json")

    assert result["name"] == "Worker Story rich-answer benchmark"
    assert result["total"] == 5
    assert result["all_passed"] is True
    assert {item["id"] for item in result["results"]} >= {
        "worker-story-evidence-rich-answer",
        "worker-story-source-truth",
        "worker-story-calculated-payroll-outcome",
        "worker-story-decision-vs-rate-story",
        "worker-story-movement-review-admin-queue",
    }


def test_payroll_bases_and_totals_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_payroll_bases_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.payroll_bases_and_totals.json")

    assert result["name"] == "Payroll Bases & Totals rich-answer benchmark"
    assert result["total"] == 6
    assert result["all_passed"] is True
    assert {item["id"] for item in result["results"]} == {
        "payroll-bases-and-totals-rich-answer",
        "payroll-bases-current-effective-truth",
        "payroll-bases-vs-reporting-totals",
        "payroll-bases-bucket-definition-membership",
        "payroll-bases-stale-bucket-results",
        "payroll-bases-worker-story-movement-review",
    }


def test_payrun_admin_queue_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_payrun_admin_queue_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.payrun_admin_queue.json")

    assert result["name"] == "PayRun Admin Queue rich-answer benchmark"
    assert result["total"] == 8
    assert result["all_passed"] is True
    assert {item["id"] for item in result["results"]} == {
        "payrun-admin-queue-rich-answer",
        "payrun-admin-queue-vs-command-centre",
        "payrun-admin-queue-cleanliness-assurance",
        "payrun-admin-queue-blockers-warnings-ready",
        "payrun-admin-queue-worker-attention-dirty-contacts",
        "payrun-admin-queue-finalisation-readiness",
        "payrun-admin-queue-assurance-snapshot",
        "payrun-admin-queue-review-surface-connections",
    }


def test_worker_attention_issue_resolution_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_worker_attention_issue_resolution_benchmark_evidence(db_session)

    result = run_golden_questions(
        db_session,
        "samples/eval/rich_answer_benchmark.worker_attention_issue_resolution.json",
    )

    assert result["name"] == "Worker Attention / Issue Resolution rich-answer benchmark"
    assert result["total"] == 6
    failures = [
        {
            "id": item["id"],
            "failure_reasons": item["failure_reasons"],
            "failed_checks": [key for key, passed in item["checks"].items() if not passed],
        }
        for item in result["results"]
        if not item["passed"]
    ]
    assert result["all_passed"] is True, json.dumps(failures, indent=2)
    assert {item["id"] for item in result["results"]} == {
        "worker-attention-issue-resolution-rich-answer",
        "worker-attention-worker-issue-model",
        "worker-attention-deterministic-fix-links",
        "worker-attention-dirty-contact-reprocessing",
        "worker-attention-payment-allocation-negative-net-pay",
        "worker-attention-admin-queue-worker-story-relationship",
    }


def test_gross_to_net_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_gross_to_net_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.gross_to_net.json")

    assert result["name"] == "Gross-to-Net rich-answer benchmark"
    assert result["total"] == 6
    failures = [
        {
            "id": item["id"],
            "failure_reasons": item["failure_reasons"],
            "failed_checks": [key for key, passed in item["checks"].items() if not passed],
        }
        for item in result["results"]
        if not item["passed"]
    ]
    assert result["all_passed"] is True, json.dumps(failures, indent=2)
    assert {item["id"] for item in result["results"]} == {
        "gross-to-net-rich-answer",
        "gross-to-net-gross-earnings-to-net-pay",
        "gross-to-net-taxable-basis-payg",
        "gross-to-net-deductions-obligations",
        "gross-to-net-negative-net-pay",
        "gross-to-net-current-effective-worker-story",
    }


def test_rate_source_rate_story_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_rate_source_rate_story_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.rate_source_rate_story.json")

    assert result["name"] == "RateSource / Rate Story rich-answer benchmark"
    assert result["total"] == 6
    failures = [
        {
            "id": item["id"],
            "failure_reasons": item["failure_reasons"],
            "failed_checks": [key for key, passed in item["checks"].items() if not passed],
        }
        for item in result["results"]
        if not item["passed"]
    ]
    assert result["all_passed"] is True, json.dumps(failures, indent=2)
    assert {item["id"] for item in result["results"]} == {
        "rate-source-rate-story-rich-answer",
        "rate-source-rate-story-selection",
        "rate-source-rate-story-pay-guide-evidence",
        "rate-source-rate-story-vs-decision-story",
        "rate-source-rate-story-date-effective-scoped-rates",
        "rate-source-rate-story-worker-story-gross-to-net",
    }


def test_decision_story_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_decision_story_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.decision_story.json")

    assert result["name"] == "Decision Story rich-answer benchmark"
    assert result["total"] == 7
    failures = [
        {
            "id": item["id"],
            "failure_reasons": item["failure_reasons"],
            "failed_checks": [key for key, passed in item["checks"].items() if not passed],
        }
        for item in result["results"]
        if not item["passed"]
    ]
    assert result["all_passed"] is True, json.dumps(failures, indent=2)
    assert {item["id"] for item in result["results"]} == {
        "decision-story-rich-answer",
        "decision-story-why-line-exists",
        "decision-story-decision-evidence-index",
        "decision-story-vs-rate-story",
        "decision-story-allowance-penalty-overtime-shift",
        "decision-story-break-public-holiday-special-conditions",
        "decision-story-worker-story-gross-to-net",
    }


def test_payroll_output_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_payroll_output_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.payroll_output.json")

    assert result["name"] == "Payroll Output rich-answer benchmark"
    assert result["total"] == 7
    failures = [
        {
            "id": item["id"],
            "failure_reasons": item["failure_reasons"],
            "failed_checks": [key for key, passed in item["checks"].items() if not passed],
        }
        for item in result["results"]
        if not item["passed"]
    ]
    assert result["all_passed"] is True, json.dumps(failures, indent=2)
    assert {item["id"] for item in result["results"]} == {
        "payroll-output-rich-answer",
        "payroll-output-current-effective-output",
        "payroll-output-run-vs-process-period-output",
        "payroll-output-payroll-lines",
        "payroll-output-gross-to-net",
        "payroll-output-payroll-bases-totals",
        "payroll-output-finalisation-payment-execution",
    }


def test_leave_requests_workflow_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_leave_requests_workflow_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.leave_requests_workflow.json")

    assert result["name"] == "Leave Requests / Leave Workflow rich-answer benchmark"
    assert result["total"] == 7
    failures = [
        {
            "id": item["id"],
            "failure_reasons": item["failure_reasons"],
            "failed_checks": [key for key, passed in item["checks"].items() if not passed],
        }
        for item in result["results"]
        if not item["passed"]
    ]
    assert result["all_passed"] is True, json.dumps(failures, indent=2)
    assert {item["id"] for item in result["results"]} == {
        "leave-requests-workflow-rich-answer",
        "leave-requests-workflow-lifecycle-status",
        "leave-requests-workflow-preview-overlap-shortfall",
        "leave-requests-workflow-taken-valuation",
        "leave-requests-workflow-ledger-balances",
        "leave-requests-workflow-source-applicability",
        "leave-requests-workflow-worker-story-payrun-finalisation",
    }


def test_public_holidays_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_public_holidays_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.public_holidays.json")

    assert result["name"] == "Public Holidays rich-answer benchmark"
    assert result["total"] == 7
    failures = [
        {
            "id": item["id"],
            "failure_reasons": item["failure_reasons"],
            "failed_checks": [key for key, passed in item["checks"].items() if not passed],
        }
        for item in result["results"]
        if not item["passed"]
    ]
    assert result["all_passed"] is True, json.dumps(failures, indent=2)
    assert all(item["checks"]["forbidden_answer_patterns_any"] is True for item in result["results"])
    assert {item["id"] for item in result["results"]} == {
        "public-holidays-rich-answer",
        "public-holidays-worker-applicability",
        "public-holidays-payroll-treatment",
        "public-holidays-leave-requests-ledger",
        "public-holidays-worker-story-payroll-evidence",
        "public-holidays-missing-configuration-context",
        "public-holidays-employer-liabilities-oncosts",
    }


def test_rosters_patterns_scheduling_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_rosters_patterns_scheduling_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.rosters_patterns_scheduling.json")

    assert result["name"] == "Rosters / Patterns / Scheduling rich-answer benchmark"
    assert result["total"] == 7
    failures = [
        {
            "id": item["id"],
            "failure_reasons": item["failure_reasons"],
            "failed_checks": [key for key, passed in item["checks"].items() if not passed],
        }
        for item in result["results"]
        if not item["passed"]
    ]
    assert result["all_passed"] is True, json.dumps(failures, indent=2)
    assert all(item["checks"]["forbidden_answer_patterns_any"] is True for item in result["results"])
    assert {item["id"] for item in result["results"]} == {
        "rosters-patterns-scheduling-rich-answer",
        "rosters-patterns-scheduling-expected-work-context",
        "rosters-patterns-scheduling-appointments-worksites",
        "rosters-patterns-scheduling-ordinary-hours-leave-basis",
        "rosters-patterns-scheduling-objecttime-boundary",
        "rosters-patterns-scheduling-worker-story-payroll-evidence",
        "rosters-patterns-scheduling-missing-configuration",
    }


def test_award_positions_classifications_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_award_positions_classifications_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.award_positions_classifications.json")

    assert result["name"] == "Award Positions / Classifications rich-answer benchmark"
    assert result["total"] == 1
    failures = [
        {
            "id": item["id"],
            "failure_reasons": item["failure_reasons"],
            "failed_checks": [key for key, passed in item["checks"].items() if not passed],
        }
        for item in result["results"]
        if not item["passed"]
    ]
    assert result["all_passed"] is True, json.dumps(failures, indent=2)
    assert {item["id"] for item in result["results"]} == {
        "award-positions-classifications-rich-answer",
    }


def test_contact_payroll_history_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_contact_payroll_history_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.contact_payroll_history.json")

    assert result["name"] == "Contact Payroll History rich-answer benchmark"
    assert result["total"] == 7
    failures = [
        {
            "id": item["id"],
            "failure_reasons": item["failure_reasons"],
            "failed_checks": [key for key, passed in item["checks"].items() if not passed],
        }
        for item in result["results"]
        if not item["passed"]
    ]
    assert result["all_passed"] is True, json.dumps(failures, indent=2)
    assert {item["id"] for item in result["results"]} == {
        "contact-payroll-history-rich-answer",
        "contact-payroll-history-payrun-participation",
        "contact-payroll-history-current-historical-output",
        "contact-payroll-history-deductions-obligations-negative-net-pay",
        "contact-payroll-history-tax-payment-readiness",
        "contact-payroll-history-leave-accrual-worker-story",
        "contact-payroll-history-retro-replay-correction",
    }


def test_movement_review_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_movement_review_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.movement_review.json")

    assert result["name"] == "Movement Review rich-answer benchmark"
    assert result["total"] == 8
    assert result["all_passed"] is True
    assert {item["id"] for item in result["results"]} == {
        "movement-review-rich-answer",
        "movement-review-review-worthy-not-error",
        "movement-review-organisation-worker-lenses",
        "movement-review-comparable-periods-variance",
        "movement-review-payroll-bases",
        "movement-review-worker-story",
        "movement-review-admin-queue-assurance",
        "movement-review-trend-only-rolling-ytd",
    }


def test_comparison_remediation_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_comparison_remediation_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.comparison_remediation.json")

    assert result["name"] == "Comparison / Remediation rich-answer benchmark"
    assert result["total"] == 9
    assert result["all_passed"] is True
    assert {item["id"] for item in result["results"]} == {
        "comparison-remediation-rich-answer",
        "comparison-remediation-three-lanes",
        "comparison-remediation-primary-award-path",
        "comparison-remediation-imported-actuals",
        "comparison-remediation-policy",
        "comparison-remediation-evidence-before-variance",
        "comparison-remediation-variance-lines-not-manual",
        "comparison-remediation-classification-mapping",
        "comparison-remediation-surface-connections",
    }


def test_tax_payg_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_tax_payg_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.tax_payg.json")

    assert result["name"] == "Tax / PAYG rich-answer benchmark"
    assert result["total"] == 9
    assert result["all_passed"] is True
    assert {item["id"] for item in result["results"]} == {
        "tax-payg-rich-answer",
        "tax-payg-minerva-not-calculate",
        "tax-payg-taxstory-explainability",
        "tax-payg-taxable-basis-payroll-bases",
        "tax-payg-payment-date-context",
        "tax-payg-pay-frequency-support",
        "tax-payg-worker-tax-readiness",
        "tax-payg-supplementary-incremental",
        "tax-payg-worker-story-admin-queue",
    }


def test_deductions_obligations_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_deductions_obligations_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.deductions_obligations.json")

    assert result["name"] == "Deductions / Obligations rich-answer benchmark"
    assert result["total"] == 10
    assert result["all_passed"] is True
    assert {item["id"] for item in result["results"]} == {
        "deductions-obligations-rich-answer",
        "deductions-obligations-template-chain",
        "deductions-obligations-application-memory",
        "deductions-obligations-supplementary-memory",
        "deductions-obligations-applicability-affordability",
        "deductions-obligations-skipped-partial-unmet",
        "deductions-obligations-deduction-vs-obligation",
        "deductions-obligations-reducing-balance",
        "deductions-obligations-negative-net-pay",
        "deductions-obligations-worker-story-admin-queue",
    }


def test_retro_replay_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_retro_replay_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.retro_replay.json")

    assert result["name"] == "Retro / Replay rich-answer benchmark"
    assert result["total"] == 10
    assert result["all_passed"] is True
    assert {item["id"] for item in result["results"]} == {
        "retro-replay-rich-answer",
        "retro-replay-attributed-vs-paid-period",
        "retro-replay-finalised-not-overwritten",
        "retro-replay-current-effective-vs-historical",
        "retro-replay-buckets-basis-snapshots",
        "retro-replay-source-dependency-detection",
        "retro-replay-retro-vs-supplementary-payrun",
        "retro-replay-comparison-remediation",
        "retro-replay-worker-story",
        "retro-replay-admin-queue-movement-review",
    }


def test_payment_execution_remittance_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_payment_execution_remittance_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.payment_execution_remittance.json")

    assert result["name"] == "Payment Execution / Remittance rich-answer benchmark"
    assert result["total"] == 10
    failures = [
        {
            "id": item["id"],
            "failure_reasons": item["failure_reasons"],
            "failed_checks": [key for key, passed in item["checks"].items() if not passed],
        }
        for item in result["results"]
        if not item["passed"]
    ]
    assert result["all_passed"] is True, json.dumps(failures, indent=2)
    assert {item["id"] for item in result["results"]} == {
        "payment-execution-remittance-rich-answer",
        "payment-execution-remittance-not-payroll-calculation",
        "payment-execution-remittance-finalised-gross-to-net",
        "payment-execution-remittance-worker-net-pay-bank-allocation",
        "payment-execution-remittance-missing-destinations",
        "payment-execution-remittance-negative-net-pay-obligations",
        "payment-execution-remittance-deduction-third-party",
        "payment-execution-remittance-generate-bank-file-period-close",
        "payment-execution-remittance-batching-reconciliation",
        "payment-execution-remittance-worker-attention-admin-queue-worker-story",
    }


def test_leave_accrual_processing_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_leave_accrual_processing_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.leave_accrual_processing.json")

    assert result["name"] == "Leave Accrual / Processing rich-answer benchmark"
    assert result["total"] == 11
    failures = [
        {
            "id": item["id"],
            "failure_reasons": item["failure_reasons"],
            "failed_checks": [key for key, passed in item["checks"].items() if not passed],
        }
        for item in result["results"]
        if not item["passed"]
    ]
    assert result["all_passed"] is True, json.dumps(failures, indent=2)
    assert {item["id"] for item in result["results"]} == {
        "leave-accrual-processing-rich-answer",
        "leave-accrual-processing-minerva-not-calculate",
        "leave-accrual-processing-source-truth",
        "leave-accrual-processing-calc-interpreter-output",
        "leave-accrual-processing-leavetype-rule-role",
        "leave-accrual-processing-leavetyperule-not-final-applicability",
        "leave-accrual-processing-leaveledger-explanation",
        "leave-accrual-processing-taken-valuation-hard-fail",
        "leave-accrual-processing-request-payment-sequencing",
        "leave-accrual-processing-worker-story-payroll-bases",
        "leave-accrual-processing-payrun-finalisation-readiness",
    }


def test_finalisation_readiness_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_finalisation_readiness_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.finalisation_readiness.json")

    assert result["name"] == "Finalisation Readiness rich-answer benchmark"
    assert result["total"] == 12
    failures = [
        {
            "id": item["id"],
            "failure_reasons": item["failure_reasons"],
            "failed_checks": [key for key, passed in item["checks"].items() if not passed],
        }
        for item in result["results"]
        if not item["passed"]
    ]
    assert result["all_passed"] is True, json.dumps(failures, indent=2)
    assert {item["id"] for item in result["results"]} == {
        "finalisation-readiness-rich-answer",
        "finalisation-readiness-minerva-not-determine",
        "finalisation-readiness-blockers-warnings-green",
        "finalisation-readiness-current-effective-output",
        "finalisation-readiness-worker-attention-admin-queue",
        "finalisation-readiness-payroll-bases",
        "finalisation-readiness-leave-readiness",
        "finalisation-readiness-tax-deduction-payment",
        "finalisation-readiness-payment-vs-gross-to-net",
        "finalisation-readiness-finalised-outcome-truth",
        "finalisation-readiness-warning-acknowledgement-audit",
        "finalisation-readiness-worker-story-review-surfaces",
    }


def test_leave_source_model_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_leave_source_model_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.leave_source_model.json")

    assert result["name"] == "Leave Source Model rich-answer benchmark"
    assert result["total"] == 10
    failures = [
        {
            "id": item["id"],
            "failure_reasons": item["failure_reasons"],
            "failed_checks": [key for key, passed in item["checks"].items() if not passed],
        }
        for item in result["results"]
        if not item["passed"]
    ]
    assert result["all_passed"] is True, json.dumps(failures, indent=2)
    assert {item["id"] for item in result["results"]} == {
        "leave-source-model-rich-answer",
        "leave-source-model-leavetyperule-not-final",
        "leave-source-model-applicability-vs-rule-content",
        "leave-source-model-no-entitlement-vs-missing-output",
        "leave-source-model-contact-vs-appointment",
        "leave-source-model-source-dimensions",
        "leave-source-model-accrual-connection",
        "leave-source-model-request-payment-effects",
        "leave-source-model-worker-story",
        "leave-source-model-command-centre-finalisation",
    }


def test_oncosts_employer_liabilities_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_oncosts_employer_liabilities_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.oncosts_employer_liabilities.json")

    assert result["name"] == "On-costs / Employer Liabilities rich-answer benchmark"
    assert result["total"] == 12
    failures = [
        {
            "id": item["id"],
            "failure_reasons": item["failure_reasons"],
            "failed_checks": [key for key, passed in item["checks"].items() if not passed],
        }
        for item in result["results"]
        if not item["passed"]
    ]
    assert result["all_passed"] is True, json.dumps(failures, indent=2)
    assert {item["id"] for item in result["results"]} == {
        "oncosts-employer-liabilities-rich-answer",
        "oncosts-not-worker-pay",
        "oncosts-minerva-not-calculate",
        "oncosts-ratesource-date-effective",
        "oncosts-award-rate-type-settings",
        "oncosts-governed-basis-membership",
        "oncosts-liability-types-jurisdiction",
        "oncosts-state-worksite-location",
        "oncosts-payrun-output-worker-story",
        "oncosts-payroll-bases-connection",
        "oncosts-demo-fallback-not-production",
        "oncosts-finalisation-readiness",
    }


def test_award_build_evidence_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_award_build_evidence_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.award_build_evidence.json")

    assert result["name"] == "Award Build / Award Evidence rich-answer benchmark"
    assert result["total"] == 12
    failures = [
        {
            "id": item["id"],
            "failure_reasons": item["failure_reasons"],
            "failed_checks": [key for key, passed in item["checks"].items() if not passed],
        }
        for item in result["results"]
        if not item["passed"]
    ]
    assert result["all_passed"] is True, json.dumps(failures, indent=2)
    assert {item["id"] for item in result["results"]} == {
        "award-build-evidence-rich-answer",
        "award-build-not-runtime-payroll-calculation",
        "award-build-source-documents-pay-guides",
        "award-build-ratetype-vs-awardratetype",
        "award-build-ratesource-date-effective",
        "award-build-classification-position-class",
        "award-build-allowances-penalties-conditions",
        "award-build-decision-evidence-index",
        "award-build-rate-source-evidence-index",
        "award-build-worker-story-decision-rate-story",
        "award-build-needs-configuration-status",
        "award-build-durable-award-evidence-set",
    }


def test_imports_actuals_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_imports_actuals_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.imports_actuals.json")

    assert result["name"] == "Imports / Actuals rich-answer benchmark"
    assert result["total"] == 11
    failures = [
        {
            "id": item["id"],
            "failure_reasons": item["failure_reasons"],
            "failed_checks": [key for key, passed in item["checks"].items() if not passed],
        }
        for item in result["results"]
        if not item["passed"]
    ]
    assert result["all_passed"] is True, json.dumps(failures, indent=2)
    assert {item["id"] for item in result["results"]} == {
        "imports-actuals-rich-answer",
        "imports-actuals-external-not-interpreter",
        "imports-actuals-imported-timesheet-source-truth",
        "imports-actuals-source-system-mappings",
        "imports-actuals-pay-code-ratetype-mapping",
        "imports-actuals-position-classification-mapping",
        "imports-actuals-objecttime-source-truth",
        "imports-actuals-comparison-remediation-connection",
        "imports-actuals-reconciliation-movement-review",
        "imports-actuals-worker-story-admin-queue",
        "imports-actuals-provenance-audit",
    }


def test_objecttime_source_truth_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_objecttime_source_truth_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.objecttime_source_truth.json")

    assert result["name"] == "ObjectTime / Source Truth rich-answer benchmark"
    assert result["total"] == 12
    failures = [
        {
            "id": item["id"],
            "failure_reasons": item["failure_reasons"],
            "failed_checks": [key for key, passed in item["checks"].items() if not passed],
        }
        for item in result["results"]
        if not item["passed"]
    ]
    assert result["all_passed"] is True, json.dumps(failures, indent=2)
    assert {item["id"] for item in result["results"]} == {
        "objecttime-source-truth-rich-answer",
        "objecttime-source-evidence-not-calculation",
        "objecttime-payrun-inclusion",
        "objecttime-sourcetruth-vs-workedhours",
        "objecttime-raw-span-not-user-worked-hours",
        "objecttime-imported-generated-source-rows",
        "objecttime-current-effective-output",
        "objecttime-worker-story-source-truth",
        "objecttime-payroll-bases-leave-accrual",
        "objecttime-comparison-movement-replay",
        "objecttime-corrections-dirty-reprocessing",
        "objecttime-provenance-audit",
    }


def test_contacts_employee_appointments_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_contacts_employee_appointments_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.contacts_employee_appointments.json")

    assert result["name"] == "Contacts / Employee Appointments rich-answer benchmark"
    assert result["total"] == 11
    failures = [
        {
            "id": item["id"],
            "failure_reasons": item["failure_reasons"],
            "failed_checks": [key for key, passed in item["checks"].items() if not passed],
        }
        for item in result["results"]
        if not item["passed"]
    ]
    assert result["all_passed"] is True, json.dumps(failures, indent=2)
    assert {item["id"] for item in result["results"]} == {
        "contacts-employee-appointments-rich-answer",
        "contacts-vs-employeeappointment",
        "contacts-payrun-admission",
        "contacts-objecttime-source-truth",
        "contacts-award-classification-position-worksite",
        "contacts-worksite-state-runtime-location",
        "contacts-leave-source-accrual",
        "contacts-worker-story-history",
        "contacts-readiness-tax-bank-deduction-payment",
        "contacts-dirty-contact-reprocessing",
        "contacts-classification-lenses-not-duplicate-appointments",
    }


def test_process_period_payrun_lifecycle_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_process_period_payrun_lifecycle_benchmark_evidence(db_session)

    result = run_golden_questions(
        db_session,
        "samples/eval/rich_answer_benchmark.process_period_payrun_lifecycle.json",
    )

    assert result["name"] == "Process Periods / PayRun Lifecycle rich-answer benchmark"
    assert result["total"] == 13
    failures = [
        {
            "id": item["id"],
            "failure_reasons": item["failure_reasons"],
            "failed_checks": [key for key, passed in item["checks"].items() if not passed],
        }
        for item in result["results"]
        if not item["passed"]
    ]
    assert result["all_passed"] is True, json.dumps(failures, indent=2)
    assert {item["id"] for item in result["results"]} == {
        "process-period-payrun-lifecycle-rich-answer",
        "process-period-vs-processperiodgroup",
        "process-period-open-not-open-closed",
        "process-period-closed-dominates-open",
        "process-period-close-rolls-forward",
        "process-period-paymentdate",
        "process-period-payrun-creation-admission",
        "process-period-runtype-runpurpose",
        "process-period-regular-supplementary-retro",
        "process-period-payruncontact-lifecycle",
        "process-period-admission-not-processing",
        "process-period-current-effective-output",
        "process-period-lifecycle-cross-domain-connections",
    }


def test_costing_gl_consequence_benchmark_runner_returns_pass_status_with_seeded_evidence(db_session):
    _ingest_costing_gl_consequence_benchmark_evidence(db_session)

    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.costing_gl_consequence.json")

    assert result["name"] == "Costing / GL Consequence Evidence rich-answer benchmark"
    assert result["total"] == 11
    failures = [
        {
            "id": item["id"],
            "failure_reasons": item["failure_reasons"],
            "failed_checks": [key for key, passed in item["checks"].items() if not passed],
        }
        for item in result["results"]
        if not item["passed"]
    ]
    assert result["all_passed"] is True, json.dumps(failures, indent=2)
    assert {item["id"] for item in result["results"]} == {
        "costing-gl-consequence-rich-answer",
        "costing-downstream-of-payroll-calculation",
        "costing-finalised-payroll-outcome-truth",
        "costing-payment-execution-remittance",
        "costing-employer-liabilities-oncosts",
        "costing-deduction-obligation-writeoffs",
        "costing-comparison-remediation-variance",
        "costing-leave-valuation-accrual",
        "costing-negative-net-pay-out-of-pay",
        "costing-audit-story-financial-evidence",
        "costing-deferred-final-slice",
    }


def test_golden_runner_script_reports_worker_story_benchmark_summary(db_session, tmp_path, monkeypatch, capsys):
    _ingest_worker_story_benchmark_evidence(db_session)
    output_path = tmp_path / "worker-story-results.json"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_golden_questions.py",
            "--manifest",
            "samples/eval/rich_answer_benchmark.worker_story.json",
            "--verbose",
            "--json-output",
            str(output_path),
        ],
    )

    exit_code = run_golden_questions_script.main()
    captured = capsys.readouterr()
    result = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert "Golden questions: Worker Story rich-answer benchmark" in captured.out
    assert "Total: 5  Passed: 5  Failed: 0" in captured.out
    assert "[PASS] worker-story-source-truth" in captured.out
    assert result["all_passed"] is True
    assert result["total"] == 5


def test_golden_runner_script_reports_annual_leave_benchmark_summary(db_session, tmp_path, monkeypatch, capsys):
    _ingest(
        db_session,
        "Annual Leave configuration uses LeaveType and LeaveTypeRule. LeaveTypeKind and Rule Cockpit organise "
        "Accrual Payment Governance settings.",
        title="Developer Log - Annual Leave Configuration",
    )
    _ingest(
        db_session,
        "Annual Leave accrual posts LeaveLedger minutes using interpreter truth with no fallback during PayRun.",
        title="Developer Log - Annual Leave Accrual",
    )
    _ingest(
        db_session,
        "Annual Leave TAKEN consumption posts LeaveLedger minutes. Public holiday treatment uses "
        "DeductsOnPublicHoliday with resolver skip behaviour.",
        title="Developer Log - Annual Leave TAKEN",
    )
    _ingest(
        db_session,
        "Annual Leave valuation uses valuation basis, ordinary rate, PayRun snapshot and liability evidence.",
        title="Developer Log - Annual Leave Valuation",
    )
    _ingest(
        db_session,
        "PayRun processing includes Generate Leave Accruals on Process, leave accruals, valuation basis and Admin Queue.",
        title="Developer Log - PayRun Leave Orchestration",
    )
    _ingest(
        db_session,
        "Worker Story includes Leave and Accrual Outcome as server-owned leave output with ledger, valuation basis "
        "and evidence chain.",
        title="Developer Log - Worker Story Leave Evidence",
    )
    _ingest(
        db_session,
        "Annual Leave outstanding hardening includes Leave Source Model, FIFO lot consumption, revaluation and "
        "production hardening.",
        title="Developer Log - Annual Leave Outstanding",
    )
    output_path = tmp_path / "annual-leave-results.json"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_golden_questions.py",
            "--manifest",
            "samples/eval/rich_answer_benchmark.annual_leave.json",
            "--json-output",
            str(output_path),
        ],
    )

    exit_code = run_golden_questions_script.main()
    captured = capsys.readouterr()
    result = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert "Golden questions: Annual Leave rich-answer benchmark" in captured.out
    assert "Total: 1  Passed: 1  Failed: 0" in captured.out
    assert result["all_passed"] is True


def test_golden_runner_script_invalid_manifest_fails_clearly(tmp_path, monkeypatch, capsys):
    invalid_path = tmp_path / "invalid.json"
    invalid_path.write_text("{not valid json", encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        ["run_golden_questions.py", "--manifest", str(invalid_path)],
    )

    exit_code = run_golden_questions_script.main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Golden question evaluation failed" in captured.out
    assert "not valid JSON" in captured.out


def test_run_golden_questions_allow_failures_returns_zero(db_session, tmp_path, monkeypatch):
    manifest_path = _manifest(
        tmp_path,
        [
            {
                "id": "allowed-failure",
                "question": "How is Annual Leave managed in the system?",
                "answer_mode": "PRODUCT_DOMAIN",
                "required_answer_sections": ["Missing Section"],
            }
        ],
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["run_golden_questions.py", "--manifest", str(manifest_path), "--allow-failures"],
    )

    assert run_golden_questions_script.main() == 0
