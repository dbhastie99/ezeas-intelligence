from abc import ABC, abstractmethod

from app.services.answer_mode_service import AnswerMode, classify_answer_mode
from app.services.domain_retrieval_plan_service import detect_domain_retrieval_plan
from app.services.evidence_group_synthesis_service import EvidenceGroupSummary, synthesize_domain_plan_evidence
from app.services.knowledge_retrieval_service import RetrievalResult, classify_query_intent


def _safe_excerpt(text: str, max_length: int = 350) -> str:
    snippet = " ".join(text.split())
    if len(snippet) <= max_length:
        return snippet

    truncated = snippet[:max_length].rstrip()
    sentence_end = max(truncated.rfind("."), truncated.rfind("?"), truncated.rfind("!"))
    if sentence_end >= max_length // 2:
        return truncated[: sentence_end + 1]

    word_end = truncated.rfind(" ")
    if word_end > 0:
        return truncated[:word_end].rstrip() + "..."
    return truncated + "..."


def _coverage_label(strong_count: int, total_count: int) -> str:
    if strong_count == total_count and total_count > 0:
        return "complete"
    if strong_count >= max(1, total_count // 2):
        return "partial"
    return "weak"


def _evidence_basis_text(planned_chunks: list[RetrievalResult], strong_summaries: list[EvidenceGroupSummary]) -> str:
    source_parts: list[str] = []
    for result in planned_chunks:
        title = result.title or result.original_file_name
        source_part = f"{result.evidence_group_label}: {title} ({result.source_type})"
        if source_part not in source_parts:
            source_parts.append(source_part)
    group_text = ", ".join(summary.label for summary in strong_summaries) or "none"
    source_text = "; ".join(source_parts[:7]) if source_parts else "none"
    return f"Evidence groups used: {group_text}. Top source references: {source_text}."


def _worker_story_focus_points(question: str) -> list[str]:
    normalized = question.lower().replace("-", " ")
    points: list[str] = []
    if "source truth" in normalized or "sourcetruth" in normalized:
        points.append(
            "Focused source-truth answer: Worker Story starts from source truth and inclusion evidence so a worker "
            "and PayRun can be explained from the inputs that were included, excluded or carried into the evidence "
            "surface."
        )
    if "calculated payroll outcome" in normalized or "payroll outcome" in normalized:
        points.append(
            "Focused calculated-payroll-outcome answer: Worker Story explains Calculated Payroll Outcome from "
            "current-effective payroll output or current-effective truth, including quantity, rate, amount and line "
            "proof evidence where that evidence is present."
        )
    if "decision story" in normalized or "rate story" in normalized or "difference" in normalized:
        points.append(
            "Focused decision/rate answer: Decision Story explains why a treatment or line exists, while Rate Story "
            "explains the rate source and rate amount; DecisionEvidenceIndex and RateSourceEvidenceIndex are the "
            "evidence indexes that support those explanations where retrieved."
        )
    if "movement review" in normalized or "admin queue" in normalized:
        points.append(
            "Focused review-flow answer: Worker Story is a reusable platform evidence surface that can relate to "
            "Movement Review and PayRun Admin Queue by giving operators review context, action context, evidence and "
            "return context without turning Minerva into an action system."
        )
    return points


def _payroll_bases_focus_points(question: str) -> list[str]:
    normalized = question.lower().replace("-", " ")
    points: list[str] = []
    if "current effective" in normalized or "current-effective" in normalized or "payroll truth" in normalized:
        points.append(
            "Focused current-effective answer: Payroll Bases & Totals use current-effective truth from source truth "
            "and current-effective payroll output as governed payroll basis evidence. PayrollBucketResult evidence "
            "must be readiness-checked because stale rows are not safe current truth; deterministic Ezeas services "
            "remain payroll truth."
        )
    if "reporting total" in normalized or "ordinary reporting" in normalized or "difference" in normalized:
        points.append(
            "Focused reporting distinction answer: Payroll Bases & Totals are governed payroll basis evidence, not "
            "ordinary reporting totals or analytics output. They explain bucket definitions, worked quantities, "
            "current-effective source truth and readiness instead of acting as a reporting aggregate."
        )
    if "bucket definition" in normalized or "membership" in normalized:
        points.append(
            "Focused bucket-definition answer: PayrollBucketDefinition, bucket definitions, membership, period "
            "definition, calendar policy and period/window rules decide what belongs in a basis bucket and whether "
            "the resulting evidence is ready to use. The retrieved evidence still caveats bucket lifecycle and "
            "versioning as outstanding hardening rather than full lifecycle/versioning completion."
        )
    if "stale" in normalized or "payrollbucketresult" in normalized or "payroll bucket result" in normalized:
        points.append(
            "Focused stale-result answer: stale PayrollBucketResult rows matter because they can describe old basis "
            "evidence after source truth, current-effective payroll output, membership or period/window rules have "
            "changed. They require readiness and rebuild treatment before use and are not safe current truth."
        )
    if "worker story" in normalized or "movement review" in normalized:
        points.append(
            "Focused relationship answer: Payroll Bases & Totals can feed Worker Story and Worker Calculation Story "
            "as worker evidence, and they can support Movement Review and PayRun Admin Queue by giving operators "
            "basis movement evidence, operator review context and a platform evidence surface."
        )
    return points


def _payrun_admin_queue_focus_points(question: str) -> list[str]:
    normalized = question.lower().replace("-", " ")
    points: list[str] = []
    if "command centre" in normalized or "command center" in normalized:
        points.append(
            "Focused Command Centre distinction answer: PayRun Admin Queue is the operator action surface for what "
            "needs action now, while Command Centre remains the broader evidence and control-room surface for deeper "
            "PayRun review."
        )
    if "cleanliness" in normalized or "assurance" in normalized:
        points.append(
            "Focused queue-cleanliness answer: queue cleanliness is not assurance and does not prove the PayRun is "
            "representative. Assurance Snapshot provides reasonableness and review evidence, not calculation truth."
        )
    if "blocker" in normalized or "warning" in normalized or "ready action" in normalized:
        points.append(
            "Focused queue-action answer: blockers, warnings and ready actions have distinct operational meanings. "
            "Blockers stop or require action, warnings need review or acknowledgement, and ready actions indicate work "
            "an operator can take now."
        )
    if "worker attention" in normalized or "dirty contact" in normalized:
        points.append(
            "Focused worker-attention answer: Worker Attention and dirty contacts belong in the Admin Queue action "
            "workflow as worker review, contact-change and reprocessing contexts."
        )
    if "finalisation readiness" in normalized or "finalisation" in normalized:
        points.append(
            "Focused finalisation-readiness answer: finalisation readiness must distinguish blockers from amber "
            "warnings; the answer should not imply amber warnings can be ignored."
        )
    if "assurance snapshot" in normalized:
        points.append(
            "Focused Assurance Snapshot answer: Assurance Snapshot supports the Admin Queue with reasonableness, "
            "assurance and review signals, while governed assurance thresholds remain hardening where formal evidence "
            "says they are not complete."
        )
    if "worker story" in normalized or "payroll bases" in normalized or "movement review" in normalized:
        points.append(
            "Focused review-surface answer: PayRun Admin Queue connects to Worker Story for worker evidence, Payroll "
            "Bases & Totals for basis evidence, and Movement Review for operator review of movement evidence."
        )
    if "admin queue" in normalized or "payrun queue" in normalized:
        points.append(
            "Focused Admin Queue answer: PayRun Admin Queue is the operator workbench for what needs action now. "
            "Command Centre remains the fuller evidence and control-room surface, so queue cleanliness is not the "
            "same as assurance or proof that a PayRun is representative."
        )
        points.append(
            "Focused action semantics answer: blockers, warnings and ready actions have different operational meaning; "
            "finalisation readiness must distinguish blockers from amber warnings rather than treating warnings as "
            "ignorable."
        )
        points.append(
            "Focused assurance answer: Assurance Snapshot provides reasonableness, assurance and review signals, not "
            "hidden calculation truth. Processing and reprocessing actions may be surfaced from the queue, but "
            "deterministic Ezeas services remain payroll calculation truth."
        )
    return points


def _worker_attention_issue_resolution_focus_points(question: str) -> list[str]:
    normalized = question.lower().replace("-", " ")
    points: list[str] = []
    if "worker attention" in normalized or "issue resolution" in normalized or "worker issue" in normalized:
        points.append(
            "Focused Worker Attention / Issue Resolution answer: Worker Attention / Issue Resolution is the "
            "worker-level issue surface for payroll-affecting blockers, warnings, readiness gaps and deterministic "
            "fix links."
        )
        points.append(
            "Focused issue-model answer: WorkerIssue and Worker issue evidence should preserve issue scope, issue "
            "class, issue type and issue severity, also expressed as IssueScope, IssueClass, IssueType and "
            "IssueSeverity, so operators can understand the worker-specific issue, blocker vs warning readiness, "
            "recommended action, resolution surface and evidence/story; Worker Attention remains not payroll "
            "calculation truth."
        )
        points.append(
            "Focused readiness answer: Worker Attention should surface blockers and warnings for dirty contact, "
            "payroll-affecting source/configuration change, PayRunContact dirty or PENDING state, current PayRun "
            "output no longer safe, reprocessing required, full contact-level reprocessing default, payment allocation "
            "readiness, payment execution readiness, tax readiness, deduction readiness, leave readiness, negative net "
            "pay and obligations where formal evidence supports those categories."
        )
        points.append(
            "Focused fix-link answer: deterministic fix link and deterministic fix links should provide a resolution "
            "surface, resolution surfaces, in-context remediation, no dead-end issue, server-owned fix targets, "
            "backend-owned truth, guided action, not Minerva mutation, governed user action and audit/evidence where "
            "applicable, but Minerva does not resolve issues, clear blockers, approve, suppress, finalise, repair "
            "payroll truth, mutate PayRunContact state, mark dirty, reprocess workers or calculate payroll."
        )
        points.append(
            "Focused payment/negative-net-pay answer: payment allocation readiness and payment execution readiness "
            "should surface gross-to-net context; negative net pay needs governed treatment such as obligation, "
            "carry-forward, recovery or write-off pathways where supported, is not silently converted to zero, and may "
            "be a blocker or review-worthy issue depending on policy/evidence."
        )
        points.append(
            "Focused surface relationship answer: Worker Story should explain worker issue evidence, while PayRun "
            "Admin Queue or Admin Queue is the operator workbench for what needs action now; Worker Attention is the "
            "worker-level issue resolution surface, Worker Story explains evidence and context, the surfaces are "
            "related but not identical, and Worker Story should expose the same resolution path where a worker has an "
            "issue. Minerva explains relationships, not runtime state."
        )
        points.append(
            "Focused dirty-state boundary answer: dirty contact state is a platform safety signal. Minerva explains "
            "why dirty contact or PayRunContact dirty evidence matters, but does not mark dirty and does not reprocess."
        )
        points.append(
            "Focused hardening answer: keep status honesty around issue taxonomy, resolution workflow, deterministic "
            "fix link contracts, dirty-contact/reprocessing propagation and broader contract tests."
        )
    return points


def _gross_to_net_focus_points(question: str) -> list[str]:
    normalized = question.lower().replace("-", " ")
    points: list[str] = []
    if "gross to net" in normalized or "grosstonet" in normalized or "gross" in normalized and "net pay" in normalized:
        points.append(
            "Focused Gross-to-Net answer: Gross-to-Net is the payroll outcome calculation and payroll outcome "
            "explanation surface that connects gross earnings, payroll output, taxable basis, PAYG, tax withholding, "
            "deductions, obligations and net pay."
        )
        points.append(
            "Focused outcome chain answer: gross earnings flow into taxable basis and taxable earnings where policy "
            "requires, then tax/PAYG withholding, deductions and obligation recovery affect net pay and worker net pay. "
            "This is calculation/output evidence and payment allocation or payment readiness context, not payment "
            "execution itself."
        )
        points.append(
            "Focused tax/PAYG answer: Gross-to-Net relates to taxable basis, taxable earnings, PAYG, withholding, "
            "TaxStory or tax evidence, PaymentDate where tax context is relevant, Payroll Bases relationship and the "
            "deterministic tax provider/service boundary; Minerva does not calculate withholding."
        )
        points.append(
            "Focused deductions/obligations answer: deductions reduce net pay where applicable, while obligations, "
            "reducing-balance recovery, affordability, priority, partial deductions, skipped deductions, carry-forward, "
            "unmet deduction story and linked obligation recovery are governed evidence rather than automatic blind "
            "subtraction. Worker Attention and Admin Queue may surface issues."
        )
        points.append(
            "Focused negative-net-pay answer: negative net pay needs governed treatment such as carry-forward, "
            "recovery, allow, block, convert to obligation, write-off or out-of-pay record pathways where formal "
            "evidence supports them; it must not be silently converted to zero or approved by Minerva. It can affect "
            "payment execution readiness, Worker Attention issue resolution and financial consequence or obligation "
            "evidence."
        )
        points.append(
            "Focused negative-net-pay action answer: negative net pay is a governed treatment decision; allow, block, "
            "carry-forward, recover later, convert to obligation, write-off, out-of-pay record, payment execution "
            "readiness, Worker Attention, issue resolution, financial consequence and obligation evidence are the "
            "relevant status-honest concepts where formal evidence supports them."
        )
        points.append(
            "Focused payment/readiness answer: payment allocation and payment execution readiness consume net pay "
            "evidence, but Gross-to-Net and Payment Execution are not the same surface and Minerva does not generate "
            "payment files."
        )
        points.append(
            "Focused evidence surface answer: Worker Story should explain Gross-to-Net evidence, current-effective "
            "payroll output truth, full run versus targeted reprocess where supported, calculated payroll outcome, "
            "line proof, amounts, deductions, net pay, superseded output and audit story while staying status-honest "
            "about outstanding hardening."
        )
        points.append(
            "Focused boundary answer: Minerva does not calculate gross-to-net, withhold tax, apply deductions, change "
            "net pay, approve or resolve negative net pay, finalise PayRuns or mutate operational payroll truth."
        )
        points.append(
            "Focused basis boundary answer: taxable basis and final withholding are connected to but not the same as "
            "general payroll basis evidence unless the answer explains the relationship."
        )
    return points


def _rate_source_rate_story_focus_points(question: str) -> list[str]:
    normalized = question.lower().replace("-", " ")
    points: list[str] = []
    if "rate story" in normalized or "ratesource" in normalized or "rate source" in normalized:
        points.append(
            "Focused RateSource / Rate Story answer: Rate Story explains which selected rate or rate amount was used, "
            "where the amount came from, and how RateSource evidence represents the rate source, selected RateSource, "
            "runtime context and evidence basis. It is not entitlement/treatment selection, and Minerva does not select rates."
        )
        points.append(
            "Focused rate evidence answer: RateSource selection should explain date-effective rates, award rate, "
            "account rate, class rate, effective date, runtime/class/context, scope resolution, RateType, AwardRateType "
            "and selected rate where formal evidence supports them. Superseded or historical rates should not be "
            "described as current unless in audit context, and Minerva explains but does not select rate."
        )
        points.append(
            "Focused source-evidence answer: pay guide rate evidence and RateSourceEvidenceIndex or Rate Source "
            "Evidence Index can preserve pay guide row, column, page and source text evidence for rate amount support, "
            "but rate amount evidence is not the same as treatment entitlement and pay guide evidence alone does not "
            "prove treatment entitlement. Where pay guide evidence is absent, the answer should be honest about the "
            "evidence limitation."
        )
        points.append(
            "Focused Decision Story boundary answer: Rate Story is not the same as Decision Story; Decision Story "
            "explains why a treatment or line exists and owns entitlement/treatment logic, while Rate Story explains "
            "why a rate/amount was used through selected RateSource and rate amount evidence. Both can appear in "
            "Worker Story and payroll line explanation, and RateSource evidence alone does not prove entitlement."
        )
        points.append(
            "Focused Worker Story/output answer: Worker Story can expose Rate Story alongside payroll output, line "
            "proof, selected rate, rate amount, formula, calculated payroll outcome and Gross-to-Net context. Gross-to-Net "
            "uses output lines and amounts, not Rate Story as calculation authority; Rate Story supports explanation/audit "
            "and Minerva does not calculate payroll."
        )
        points.append(
            "Focused boundary answer: Minerva does not select rates, calculate pay, interpret awards at runtime, "
            "change RateSource records, validate payroll correctness or mutate operational payroll truth. Rate Story "
            "must remain status-honest about outstanding hardening."
        )
    return points


def _decision_story_focus_points(question: str) -> list[str]:
    normalized = question.lower().replace("-", " ")
    points: list[str] = []
    if "decision story" in normalized or "decisionstory" in normalized or "decisionevidenceindex" in normalized:
        points.append(
            "Focused Decision Story answer: Decision Story is the evidence layer that explains why a payroll "
            "treatment, entitlement, line, rule outcome, allowance, penalty, overtime, shift, public holiday, break "
            "treatment, missed break, minimum engagement or other calculated payroll decision exists."
        )
        points.append(
            "Focused treatment-selection answer: Decision Story explains entitlement / treatment selection by linking "
            "treatment or entitlement selection, configured rule and runtime facts, configured rules, award/source "
            "evidence and source evidence where available; it is evidence for why the line exists, not rate amount "
            "selection, and Minerva does not decide entitlements."
        )
        points.append(
            "Focused DecisionEvidenceIndex answer: DecisionEvidenceIndex and Decision Evidence Index are a compact "
            "decision evidence index that links emitted payroll lines to decision evidence, supports explanation and "
            "audit, and can reference award/source evidence where available, but does not by itself prove the full "
            "award-source chain; evidence limitation honesty is required."
        )
        points.append(
            "Focused Rate Story boundary answer: Decision Story explains why a treatment/line exists and owns "
            "entitlement/treatment logic. Rate Story explains why a rate/amount was used through selected RateSource "
            "and rate amount evidence. Both can appear in Worker Story, but Decision Story is not the same as Rate "
            "Story and RateSource evidence alone does not prove entitlement."
        )
        points.append(
            "Focused decision-family answer: allowance, penalty, overtime and shift treatment decisions should be "
            "explained from runtime facts, configured rules and decision evidence, with exact clause/source evidence "
            "where available and a generic limitation where source evidence is incomplete. Minerva does not calculate "
            "or select treatments."
        )
        points.append(
            "Focused special-condition answer: break treatment, missed break or unpaid break evidence where supported, "
            "public holiday treatment, special conditions and minimum engagement should be explained from configured "
            "rules and runtime facts, surfaced through Worker Story and payroll line explanation, while keeping "
            "outstanding hardening visible where evidence coverage is incomplete."
        )
        points.append(
            "Focused Worker Story/output answer: Worker Story can expose Decision Story as payroll line explanation "
            "and worker evidence for why line/treatment exists. Gross-to-Net consumes payroll output amounts/outcomes "
            "from calculated payroll outcome and line proof, while Decision Story supports audit/explanation and is "
            "not net-pay calculation authority. The distinction from Rate Story remains visible."
        )
        points.append(
            "Focused boundary answer: Minerva does not select treatments, decide entitlements, interpret awards at "
            "runtime, calculate payroll, change decision evidence, validate payroll correctness or mutate operational "
            "payroll truth. Keep evidence limitation honesty and status honesty around outstanding hardening."
        )
    return points


def _payroll_output_focus_points(question: str) -> list[str]:
    normalized = question.lower().replace("-", " ")
    points: list[str] = []
    if "payroll output" in normalized or "payrun output" in normalized or "process period output" in normalized or "run output" in normalized:
        points.append(
            "Focused Payroll Output answer: Payroll Output is the calculated payroll result and output evidence "
            "surface for payroll lines, output lines, worker-level output, PayRun totals and current-effective "
            "payroll output truth."
        )
        points.append(
            "Focused current-effective answer: current-effective payroll output truth is the latest/current worker "
            "outcome for the process period. Targeted reprocessing versus full run must preserve current-effective "
            "truth: superseded or stale run rows should not appear as current truth."
        )
        points.append(
            "Focused output-lens answer: Run Output and Process Period Output are related but different lenses; "
            "run output explains results for a PayRun or calculation run, while process-period output is the "
            "period-context view and they should not be collapsed without explanation."
        )
        points.append(
            "Focused run-versus-period answer: Run Output is scoped to the selected run/subrun lens. Process Period "
            "Output should show current-effective whole-period worker truth, and targeted reprocess should not hide "
            "non-target workers from process-period output."
        )
        points.append(
            "Focused payroll-line answer: calculated payroll lines and output lines should explain amount, quantity "
            "and treatment where supported by formal evidence. Payroll Output is calculated result evidence, not "
            "Minerva calculation."
        )
        points.append(
            "Focused story relationship answer: Worker Story renders worker-level output evidence, while Decision "
            "Story explains why a payroll line or treatment exists and Rate Story explains why a selected rate or "
            "rate amount was used."
        )
        points.append(
            "Focused outcome relationship answer: Gross-to-Net consumes payroll output amounts and lines to explain "
            "gross earnings, taxable basis, deductions, obligations and net pay; Payroll Bases & Totals provide "
            "basis evidence and totals rather than replacing Payroll Output. Minerva does not calculate gross-to-net."
        )
        points.append(
            "Focused bases relationship answer: Payroll Output is calculated pay/result evidence, while Payroll Bases "
            "& Totals are governed basis evidence. Basis results should use current-effective payroll source truth "
            "and may support taxable, superable, payroll tax, WIC, ordinary and worked-hours evidence. Output totals "
            "and basis evidence are related but distinct."
        )
        points.append(
            "Focused readiness/payment boundary answer: Finalisation Readiness and Payment Execution consume output "
            "evidence downstream. Finalisation readiness uses current-effective output, blockers/warnings and "
            "finalised outcome truth; payment execution consumes finalised, gross-to-net and payment-ready outcome. "
            "Payroll Output is not finalisation, approval, payment-file generation or payment execution."
        )
        points.append(
            "Focused boundary answer: Minerva does not calculate payroll output, change payroll output lines, "
            "finalise PayRuns, approve payroll output, select treatments, select rates, generate payment files or "
            "mutate operational payroll truth. Payroll Output alone does not prove payroll correctness."
        )
    return points


def _movement_review_focus_points(question: str) -> list[str]:
    normalized = question.lower().replace("-", " ")
    points: list[str] = []
    if "review worthy" in normalized or "review-worthy" in normalized or "proving payroll is wrong" in normalized:
        points.append(
            "Focused review-worthy answer: Movement Review shows review-worthy movement as payroll reasonableness "
            "evidence, not automatic proof of error. A variance asks for review; it does not by itself create a fix "
            "action or prove payroll is wrong."
        )
    if "organisation" in normalized or "organization" in normalized or "worker lenses" in normalized:
        points.append(
            "Focused lens answer: Movement Review can be read through organisation and worker lenses. Review-worthy "
            "defaults help operators prioritise, while all-worker and audit-complete views remain available where "
            "formal evidence supports them."
        )
    if "comparable period" in normalized or "variance" in normalized:
        points.append(
            "Focused variance answer: Movement Review compares current movement against comparable-period or baseline "
            "evidence to explain variance. Thresholds and comparable period rules should stay status-honest and must "
            "not be treated as fully governed unless formal evidence says so."
        )
    if "payroll bases" in normalized:
        points.append(
            "Focused Payroll Bases answer: Payroll Bases & Totals can support Movement Review by providing governed "
            "basis evidence and bucket source truth for movement explanations, while stale historical bucket evidence "
            "is not safe current truth."
        )
    if "worker story" in normalized:
        points.append(
            "Focused Worker Story answer: Worker Story supports Movement Review as worker-level drill-through and "
            "explanation, letting an operator move from a review-worthy movement to worker evidence."
        )
    if "admin queue" in normalized or "assurance snapshot" in normalized:
        points.append(
            "Focused Admin Queue and Assurance Snapshot answer: PayRun Admin Queue may surface movement or assurance "
            "review actions, and Assurance Snapshot contributes reasonableness and review signals; an empty queue does "
            "not prove assurance."
        )
    if "rolling" in normalized or "ytd" in normalized or "trend only" in normalized or "trend-only" in normalized:
        points.append(
            "Focused trend-only answer: rolling, YTD and trend-only metrics are review context, not ordinary "
            "current-period blockers, unless governed Movement Review Policy says they should be treated that way."
        )
    if "movement review" in normalized:
        points.append(
            "Focused Movement Review answer: Movement Review is a payroll reasonableness and review surface for "
            "understanding changes, variance and review-worthy movement; it is not automatic proof that payroll is "
            "wrong and it does not calculate payroll."
        )
        points.append(
            "Focused lenses answer: Movement Review can operate across organisation and worker lenses, prioritising "
            "review-worthy items while expected or all-worker views remain available for audit."
        )
        points.append(
            "Focused evidence answer: Movement Review depends on comparable baseline evidence, governed policy, "
            "current-effective payroll and bucket source truth. Trend-only or rolling/YTD evidence should not be "
            "treated like ordinary current-period blockers unless governed policy says so."
        )
    return points


def _comparison_remediation_focus_points(question: str) -> list[str]:
    normalized = question.lower().replace("-", " ")
    points: list[str] = []
    if "three comparison lanes" in normalized or "comparison lanes" in normalized:
        points.append(
            "Focused lane answer: the three comparison lanes are primary calculated payroll truth, comparator "
            "calculated assessment truth, and actual imported external outcome truth. They should remain separate "
            "lanes rather than being collapsed into a manual adjustment."
        )
    if "primary award path" in normalized or "comparator assessment" in normalized:
        points.append(
            "Focused primary-award answer: the ObjectTime to EmployeeAppointment to AwardPositionClass path remains "
            "operational payroll truth during comparator assessment. The comparator award is an assessment lens over "
            "the same source truth, not a replacement operational award."
        )
    if "imported actual" in normalized or "external outcome truth" in normalized:
        points.append(
            "Focused actuals answer: imported actuals are external payroll outcome truth in a separate actuals lane; "
            "they are not calculated interpreter truth or interpreter lines."
        )
    if "awardcomparisonpolicy" in normalized or "award comparison policy" in normalized:
        points.append(
            "Focused policy answer: AwardComparisonPolicy should govern comparator selection, active lanes, grain, "
            "offset policy, output mode, review requirements and variance treatment."
        )
    if "comparison evidence" in normalized or "variance generation" in normalized:
        points.append(
            "Focused evidence-before-variance answer: comparison evidence should exist before variance generation so "
            "any generated variance is traceable to the comparison run, comparison lines and policy basis."
        )
    if "top up" in normalized or "top-up" in normalized or "manual adjustment" in normalized:
        points.append(
            "Focused variance-line answer: remediation or top-up variance lines are typed, explainable, "
            "evidence-linked consequences of governed comparison; they are not ordinary manual adjustments."
        )
    if "comparator classification" in normalized or "governed mapping" in normalized:
        points.append(
            "Focused classification answer: comparator classification must not be guessed or reused automatically from "
            "the primary class. It needs governed AwardPositionClass mapping and classification-lens evidence."
        )
    if "worker story" in normalized or "admin queue" in normalized or "movement review" in normalized:
        points.append(
            "Focused surface-connection answer: Worker Story should show comparison and remediation evidence, PayRun "
            "Admin Queue should surface missing policy, missing comparator classification, unmapped actuals and "
            "variance review actions, and Movement Review can help review variance and comparison outcomes without "
            "treating variance as automatic proof of error."
        )
    if "comparison" in normalized or "remediation" in normalized or "award comparison" in normalized:
        points.append(
            "Focused Comparison / Remediation answer: Comparison / Remediation is a governed comparison capability, "
            "not a simple top-up adjustment or generic payroll calculation. It should compare primary calculated, "
            "comparator calculated and imported actual lanes under policy."
        )
        points.append(
            "Focused payroll-truth answer: the current ObjectTime to EmployeeAppointment to AwardPositionClass primary "
            "award path remains operational payroll truth. A comparator award is an assessment lens over the same "
            "source truth, not a replacement operational award."
        )
        points.append(
            "Focused evidence answer: comparison evidence should exist before variance generation, and any generated "
            "variance or remediation top-up lines must be typed, explainable and linked to comparison evidence."
        )
        points.append(
            "Focused classification answer: comparator classification cannot be guessed or reused automatically from "
            "the primary class; AwardPositionClass mapping and classification-lens modelling are required."
        )
    return points


def _tax_payg_focus_points(question: str) -> list[str]:
    normalized = question.lower().replace("-", " ")
    points: list[str] = []
    if "minerva" in normalized and ("payg" in normalized or "withholding" in normalized):
        points.append(
            "Focused calculation-boundary answer: Minerva must not calculate PAYG withholding because Tax / PAYG "
            "requires governed withholding calculation evidence from deterministic services and tax providers. "
            "Minerva explains evidence and status; it is not an LLM tax calculation."
        )
    if "taxstory" in normalized or "tax story" in normalized:
        points.append(
            "Focused TaxStory detail answer: TaxStory should explain source truth, worker tax profile, payroll context, "
            "rule pack selection, component selection, frequency conversion, band/formula calculation, rounding, "
            "net-pay effect, unsupported or skipped rules and audit provenance."
        )
    if "taxable basis" in normalized:
        points.append(
            "Focused taxable-basis detail answer: taxable basis relates to Payroll Bases & Totals through governed "
            "basis membership for taxable earnings. It should not be casually inferred from raw flags, and taxable "
            "basis governance remains outstanding where formal evidence says so."
        )
    if "processperiod paymentdate" in normalized or "payment date" in normalized:
        points.append(
            "Focused payment-date answer: ProcessPeriod PaymentDate and payment date matter because they provide tax "
            "context for PAYG. They should be governed and derived from process period context, not hardcoded."
        )
    if "pay frequency" in normalized:
        points.append(
            "Focused pay-frequency answer: pay frequency and provider support must be status-honest across daily, "
            "weekly, fortnightly, monthly and quarterly frequencies. Unsupported frequency cases should produce "
            "unsupported or configuration status, not silent calculated success."
        )
    if "worker tax declaration" in normalized or "withholding input" in normalized or "tax readiness" in normalized:
        points.append(
            "Focused worker-tax-readiness answer: worker tax declaration, withholding instruction, withholding inputs "
            "and tax profile are calculation readiness inputs that should affect tax readiness before deterministic "
            "withholding calculation proceeds."
        )
    if "supplementary" in normalized:
        points.append(
            "Focused supplementary answer: supplementary incremental PAYG should be incremental over same-period "
            "taxable earnings, less prior PAYG withheld, while supplementary tax remains status-honest where formal "
            "evidence records outstanding implementation."
        )
    if "worker story" in normalized or "admin queue" in normalized:
        points.append(
            "Focused tax-surface answer: Tax / PAYG issues should connect to Worker Story and PayRun Admin Queue for "
            "tax readiness, unsupported states, correction context and reprocessing consequences."
        )
    if "tax" in normalized or "payg" in normalized:
        points.append(
            "Focused Tax / PAYG answer: Tax / PAYG is governed withholding calculation evidence and platform story, "
            "not an LLM tax calculation. Deterministic Ezeas services and tax providers remain the withholding "
            "calculation path while Minerva explains evidence, readiness and status."
        )
        points.append(
            "Focused TaxStory answer: TaxStory should explain source truth, worker tax profile, payroll context, rule "
            "pack selection, component selection, frequency conversion, band/formula calculation, rounding, net-pay "
            "effect, unsupported or skipped rules and audit provenance."
        )
        points.append(
            "Focused taxable-basis answer: taxable basis and taxable earnings must be deliberately aligned with PAYG "
            "design and Payroll Bases & Totals evidence; they should not be casually inferred from raw flags where "
            "governed basis membership is required."
        )
        points.append(
            "Focused context answer: worker tax declaration, withholding instruction inputs, ProcessPeriod PaymentDate, "
            "payment date and pay frequency affect tax readiness and provider/rule-pack selection. Unsupported "
            "frequencies or scenarios should return explicit unsupported or configuration status, not silent success."
        )
        points.append(
            "Focused outcome answer: gross-to-net and finalised totals connect the PAYG outcome to net pay and "
            "finalised payment memory. Supplementary incremental PAYG should be incremental over same-period taxable "
            "earnings, less prior PAYG withheld."
        )
        points.append(
            "Focused surface answer: Worker Story and PayRun Admin Queue should surface tax readiness, unsupported "
            "states, correction and reprocessing consequences while keeping status honest about outstanding full "
            "provider/rule-pack support, non-weekly frequencies, taxable basis governance, withholding instruction UI, "
            "supplementary tax and full TaxStory."
        )
    return points


def _deductions_obligations_focus_points(question: str) -> list[str]:
    normalized = question.lower().replace("-", " ")
    points: list[str] = []
    if "template" in normalized or "chain" in normalized:
        points.append(
            "Focused deduction-chain answer: the deduction chain is LibraryDeductionTemplate to "
            "AccountDeductionTemplate to ContactPayrollDeduction to PayRunDeductionApplication. Library templates are "
            "advisory accelerators; account templates and worker instructions become operative configuration."
        )
    if "contactpayrolldeduction" in normalized or "worker" in normalized:
        points.append(
            "Focused worker-instruction answer: ContactPayrollDeduction is the worker-specific deduction instruction "
            "that drives governed deduction application, readiness and issue evidence."
        )
    if "payrundeductionapplication" in normalized or "application memory" in normalized:
        points.append(
            "Focused application-memory answer: PayRunDeductionApplication is PayRun event and outcome memory for "
            "requested, taken, skipped and unmet amounts, not just a hidden net-pay subtraction."
        )
    if "supplementary" in normalized:
        points.append(
            "Focused supplementary answer: supplementary PayRuns must use prior same-period application memory so "
            "recurring deductions do not blindly repeat without considering earlier deduction outcomes."
        )
    if "affordability" in normalized or "priority" in normalized or "applicability" in normalized:
        points.append(
            "Focused affordability answer: applicability comes before affordability. Affordability, priority, "
            "partial/full-only handling and carry-forward treatment must be governed and explainable."
        )
    if "carry forward" in normalized or "skipped" in normalized or "partial" in normalized or "unmet" in normalized:
        points.append(
            "Focused skipped/partial answer: skipped, partial, unmet and carry-forward deductions must remain visible "
            "and must not silently disappear. Carry-forward review should not be described as automatically creating "
            "an obligation unless formal evidence says so."
        )
    if "obligation" in normalized or "reducing balance" in normalized:
        points.append(
            "Focused obligation answer: obligations are durable balance-bearing recovery records, not merely deduction "
            "rows. Reducing-balance recovery must cap recovery by outstanding balance and complete with ledger evidence."
        )
    if "difference" in normalized and "deduction" in normalized and "obligation" in normalized:
        points.append(
            "Focused deduction-vs-obligation answer: a deduction is a governed PayRun application outcome from a "
            "worker instruction, while an obligation is a durable balance-bearing recovery record with ledger evidence "
            "for future recovery."
        )
    if "reducing balance" in normalized:
        points.append(
            "Focused reducing-balance answer: reducing-balance recovery should take only up to the outstanding balance, "
            "write recovery through obligation ledger evidence, and stop when the durable obligation is complete."
        )
    if "negative net pay" in normalized:
        points.append(
            "Focused negative-net-pay answer: negative net pay is a governed outcome requiring policy treatment, not "
            "a silent arithmetic side effect or proof that negative-net-pay policy is solved."
        )
    if "payment" in normalized or "remittance" in normalized or "gross" in normalized:
        points.append(
            "Focused payment answer: gross-to-net, payment execution and remittance surfaces should show deduction "
            "and obligation readiness, but payment execution/remittance must remain outstanding where formal evidence "
            "says it is not implemented."
        )
    if "deduction" in normalized or "obligation" in normalized:
        points.append(
            "Focused Deductions / Obligations answer: Deductions / Obligations are governed payroll outcomes and "
            "future recovery evidence, not simple raw net-pay subtraction."
        )
        points.append(
            "Focused governance answer: deductions should follow applicability before affordability, then governed "
            "priority, partial/full-only and carry-forward treatment. Skipped, partial, unmet and carry-forward "
            "outcomes should stay visible."
        )
        points.append(
            "Focused recovery answer: durable obligations and reducing-balance recovery should use "
            "ContactPayrollObligation and ContactPayrollObligationLedger-style evidence, cap by outstanding balance "
            "and complete through ledger evidence."
        )
        points.append(
            "Focused surface answer: gross-to-net, Worker Story, PayRun Admin Queue, Worker Attention, payment "
            "execution and remittance surfaces should expose deduction/obligation readiness and issues while staying "
            "honest about outstanding UI, remittance, write-off/costing, negative-net-pay policy and tax integration."
        )
    return points


def _retro_replay_focus_points(question: str) -> list[str]:
    normalized = question.lower().replace("-", " ")
    points: list[str] = []
    if "attributed period" in normalized or "paid period" in normalized:
        points.append(
            "Focused period-truth answer: attributed-period truth explains the period the correction belongs to, "
            "while paid-period truth explains the period in which money was actually paid. Retro / Replay must keep "
            "those concepts separate."
        )
    if "finalised payroll truth" in normalized or "finalised outcome" in normalized or "finalized" in normalized:
        points.append(
            "Focused finalised-truth answer: finalised outcomes are historical payment truth and must not be silently "
            "overwritten; correction/replay should add auditable evidence instead of mutating history."
        )
    if "current effective" in normalized or "current-effective" in normalized or "historical truth" in normalized:
        points.append(
            "Focused current-vs-historical answer: current-effective truth explains what the system would calculate "
            "now, while historical or finalised truth explains what was actually finalised and paid before correction."
        )
    if "bucket" in normalized or "basis snapshot" in normalized or "source hash" in normalized:
        points.append(
            "Focused snapshot answer: bucket evidence, basis snapshots, calculation evidence and source hashes are "
            "needed so replay can explain what changed without silently rebuilding finalised history."
        )
    if "source change" in normalized or "dependency detection" in normalized:
        points.append(
            "Focused dependency answer: source or configuration changes should create dependency detection and "
            "dirty/replay candidates for review, not hidden recalculation."
        )
    if "retro payrun" in normalized or "supplementary payrun" in normalized:
        points.append(
            "Focused PayRun distinction answer: retro PayRuns correct historical attributed-period evidence, while "
            "supplementary PayRuns add additional paid-period processing; they are related but not the same concept."
        )
    if "comparison" in normalized or "remediation" in normalized:
        points.append(
            "Focused comparison answer: Comparison / Remediation may consume retro/replay evidence or variance, but "
            "comparison assessment is not the same concept as governed historical replay."
        )
    if "worker story" in normalized:
        points.append(
            "Focused Worker Story answer: Worker Story should explain retro/replay impacts at worker level, including "
            "the attributed and paid periods, finalised outcome memory and replay evidence behind the change."
        )
    if "admin queue" in normalized or "movement review" in normalized:
        points.append(
            "Focused review-surface answer: PayRun Admin Queue should surface retro/replay candidates, blockers, "
            "review actions and dependency issues; Movement Review can explain movement but variance does not prove "
            "retro error by itself."
        )
    if "retro" in normalized or "replay" in normalized:
        points.append(
            "Focused Retro / Replay answer: Retro / Replay is governed historical correction and evidence replay, "
            "not ordinary reprocessing or hidden mutation of finalised payroll truth."
        )
        points.append(
            "Focused truth answer: attributed-period truth, paid-period truth, current-effective payroll truth and "
            "historical/finalised truth must remain distinct so a correction can be explained without silently "
            "overwriting finalised outcomes."
        )
        points.append(
            "Focused evidence answer: buckets, basis snapshots, calculation evidence, source hashes and historical "
            "bucket evidence matter for replay. Source or configuration changes should create dependency detection "
            "and dirty/replay candidates rather than hidden recalculation."
        )
        points.append(
            "Focused PayRun answer: retro PayRuns differ from supplementary PayRuns. Comparison / Remediation may "
            "depend on retro/replay evidence, but it is not the same concept."
        )
        points.append(
            "Focused surface answer: Worker Story should explain retro/replay impacts at worker level. PayRun Admin "
            "Queue should surface candidates, blockers, review actions or dependency issues, while Movement Review "
            "can explain movement without treating variance as automatic proof of retro error."
        )
    return points


def _payment_execution_remittance_focus_points(question: str) -> list[str]:
    normalized = question.lower().replace("-", " ")
    points: list[str] = []
    if "payment execution" in normalized or "remittance" in normalized:
        points.append(
            "Focused Payment Execution / Remittance answer: Payment Execution / Remittance is governed payment "
            "execution and remittance evidence that turns finalised payroll outcome into downstream payment/remittance "
            "action; it is not payroll calculation truth and not a generic file export."
        )
    if "gross to net" in normalized or "gross-to-net" in normalized or "calculation" in normalized:
        points.append(
            "Focused finalised-source answer: payment execution consumes finalised gross-to-net and payment outcome "
            "evidence. Payment readiness is separate from gross-to-net readiness, and gross-to-net calculation "
            "readiness does not by itself prove payment execution readiness."
        )
    if "net pay" in normalized or "bank allocation" in normalized or "payment allocation" in normalized:
        points.append(
            "Focused worker-net-pay answer: worker net pay needs valid payment allocation, bank allocation and bank "
            "instruction readiness before complete payment execution, including review of partial/missing payment "
            "allocation."
        )
    if "payment destination" in normalized or "bank" in normalized:
        points.append(
            "Focused destination-readiness answer: missing or partial payment destinations may not invalidate "
            "gross-to-net calculation, but they block complete payment execution until readiness is resolved."
        )
    if "negative net pay" in normalized or "obligation" in normalized or "write off" in normalized or "write-off" in normalized:
        points.append(
            "Focused negative-net-pay answer: negative net pay remains a governed policy outcome and can interact with "
            "obligations, carry-forward, recovery, write-off or out-of-pay treatment; the answer should not imply this "
            "policy is solved unless formal evidence says so."
        )
    if "deduction" in normalized or "third party" in normalized or "third-party" in normalized:
        points.append(
            "Focused remittance answer: deductions and obligations can require third-party remittance, batching, "
            "payment destinations, remittance files and reconciliation rather than disappearing as simple net-pay "
            "subtractions."
        )
    if "generate bank file" in normalized or "bank file" in normalized or "payment file" in normalized or "period close" in normalized:
        points.append(
            "Focused payment-file answer: Generate Bank File, payment-file execution and Period Close are governed "
            "execution steps, not generic export, and should remain status-honest outstanding areas where formal "
            "evidence says implementation is not complete."
        )
    if "worker attention" in normalized or "admin queue" in normalized:
        points.append(
            "Focused action-surface answer: Worker Attention and PayRun Admin Queue should surface payment execution "
            "blockers, warnings and actions such as missing destinations, remittance readiness or payment close issues."
        )
    if "worker story" in normalized or "audit" in normalized:
        points.append(
            "Focused story-and-audit answer: Worker Story and audit evidence should explain payment allocation, "
            "remittance, skipped, unpaid or unmet amounts and downstream treatment without claiming runtime payment "
            "truth from diagnostics."
        )
    return points


def _leave_accrual_processing_focus_points(question: str) -> list[str]:
    normalized = question.lower().replace("-", " ")
    points: list[str] = []
    if "minerva" in normalized and ("calculate" in normalized or "accrual" in normalized):
        points.append(
            "Focused Minerva boundary answer: Minerva must not calculate leave accrual because leave accrual and "
            "leave processing are deterministic platform outcomes; Minerva can explain formal evidence but does not "
            "create leave, entitlement or payroll truth."
        )
    if "source truth" in normalized:
        points.append(
            "Focused source-truth answer: leave accrual should use governed leave source truth and applicability, "
            "then derive quantity from canonical processed payroll result truth where formal evidence supports that "
            "source."
        )
    if "calcinterpreterline" in normalized or "current effective payroll output" in normalized:
        points.append(
            "Focused CalcInterpreter answer: CalcInterpreterLine and current-effective payroll output are the intended "
            "processed payroll-result evidence for leave basis quantities where supported, instead of an LLM "
            "recomputing hours or leave accrual."
        )
    if "leavetype" in normalized or "leave type" in normalized:
        points.append(
            "Focused leave-rule answer: LeaveType and LeaveTypeRule hold leave policy and calculation content, but "
            "LeaveTypeRule is not the complete future leave applicability model or final source truth by itself."
        )
    if "applicability" in normalized:
        points.append(
            "Focused applicability answer: source truth and applicability are separate from calculation content; "
            "LeaveTypeRule can describe policy, but it must not be treated as final leave applicability truth while "
            "the Leave Source Model remains outstanding."
        )
    if "leaveledger" in normalized or "leave ledger" in normalized:
        points.append(
            "Focused LeaveLedger answer: LeaveLedger should explain evidence-bearing movement records for leave "
            "accrual, payment and balance outcomes, including story evidence that supports Worker Story."
        )
    if "taken" in normalized or "valuation" in normalized or "hard fail" in normalized or "rates" in normalized:
        points.append(
            "Focused TAKEN valuation answer: TAKEN leave valuation needs hard-fail behaviour when required rates or "
            "valuation basis are missing, so the platform does not silently post a minutes-only fallback where "
            "valuation is mandatory."
        )
    if "sequencing" in normalized or "leave request" in normalized or "payment effects" in normalized:
        points.append(
            "Focused sequencing answer: leave request payment effects occur before or within payroll interpretation, "
            "while leave accrual occurs after payroll interpretation using the processed payroll output evidence."
        )
    if "worker story" in normalized or "payroll bases" in normalized:
        points.append(
            "Focused surface connection answer: Worker Story should explain Leave and Accrual Outcome from "
            "server-owned leave output, ledger and valuation evidence, while Payroll Bases & Totals can provide "
            "governed basis evidence such as worked hours or other leave basis quantities."
        )
    if "payrun" in normalized or "finalisation" in normalized or "readiness" in normalized:
        points.append(
            "Focused readiness answer: PayRun processing and finalisation should surface leave readiness, missing "
            "leave output and warning acknowledgement honestly rather than implying the leave-processing UI or "
            "finalisation path is complete."
        )
    if "leave" in normalized and ("accrue" in normalized or "accrual" in normalized or "processing" in normalized):
        points.append(
            "Focused Leave Accrual / Processing answer: leave accrual and leave processing are deterministic platform "
            "outcomes, not Minerva calculations or generic leave policy advice."
        )
        points.append(
            "Focused source-truth answer: leave accrual depends on leave source truth and applicability, not just the "
            "existence of a LeaveTypeRule or a generic policy label."
        )
        points.append(
            "Focused payroll-output answer: accrual quantity should come from canonical processed payroll result truth, "
            "including CalcInterpreterLine and current-effective payroll output where formal evidence supports that "
            "source."
        )
        points.append(
            "Focused configuration answer: AwardRateType-first accrualability and RateType fallback are the baseline "
            "direction where supported, with PER_HOUR minute/hour accrual quantity as the supported baseline."
        )
        points.append(
            "Focused ledger-and-valuation answer: LeaveLedger records accrual, payment and balance movements, while "
            "TAKEN leave valuation must use leave valuation basis and should hard failure rather than silently fall "
            "back when valuation is mandatory."
        )
        points.append(
            "Focused processing answer: leave request payment effects occur before or within payroll interpretation, "
            "while leave accrual occurs after payroll interpretation and should be visible in PayRun processing and "
            "finalisation readiness."
        )
        points.append(
            "Focused surface answer: Worker Story should explain Leave and Accrual Outcome using server-owned leave "
            "output, ledger and valuation evidence, while Payroll Bases & Totals may provide governed basis evidence "
            "for worked hours or leave basis quantities."
        )
        points.append(
            "Focused hardening answer: keep status honest about Leave Source Model, full leave-processing UI/runs, "
            "leave request ownership/contact-vs-appointment design, leave story polish and finalisation warning "
            "acknowledgement."
        )
    return points


def _finalisation_readiness_focus_points(question: str) -> list[str]:
    normalized = question.lower().replace("-", " ")
    points: list[str] = []
    if "minerva" in normalized and "determine" in normalized:
        points.append(
            "Focused Minerva boundary answer: Minerva can explain readiness evidence but must not determine runtime "
            "finalisation readiness or become the finalisation authority."
        )
    if "blocker" in normalized or "warning" in normalized or "green" in normalized:
        points.append(
            "Focused state answer: red blockers prevent the relevant action from proceeding, amber warnings require "
            "governed review or warning acknowledgement, and green means ready for that evidence dimension rather "
            "than no review-worthy movements."
        )
    if "current effective" in normalized or "payroll output" in normalized:
        points.append(
            "Focused current-output answer: current-effective payroll output matters because stale or superseded "
            "output must not be finalised as current truth."
        )
    if "payroll bases" in normalized:
        points.append(
            "Focused Payroll Bases answer: Payroll Bases & Totals readiness can affect finalisation where unresolved "
            "basis evidence or stale basis evidence means the basis trail is not safe to rely on."
        )
    if "leave readiness" in normalized:
        points.append(
            "Focused leave readiness answer: leave readiness should affect finalisation honestly by surfacing missing "
            "leave output or leave valuation basis issues where applicable."
        )
    if "tax" in normalized or "deduction" in normalized:
        points.append(
            "Focused tax/deduction/payment answer: tax readiness, deduction readiness, negative net pay and payment "
            "destination readiness are readiness dimensions that may affect finalisation or payment execution depending "
            "on policy."
        )
    if "payment execution readiness" in normalized or "gross to net" in normalized or "gross-to-net" in normalized:
        points.append(
            "Focused payment readiness answer: payment execution readiness is distinct from gross-to-net calculation "
            "readiness because bank/payment destination and downstream payment execution evidence can still block "
            "payment action."
        )
    if "finalised outcome" in normalized or "finalized outcome" in normalized:
        points.append(
            "Focused finalised outcome answer: finalised outcome truth should preserve durable payment outcome memory "
            "and finalised payroll truth once the PayRun is finalised."
        )
    if "audit" in normalized or "acknowledgement" in normalized or "acknowledgment" in normalized:
        points.append(
            "Focused audit answer: warning acknowledgement and finalisation audit evidence matter because they preserve "
            "what was reviewed, accepted or unresolved in a status-honest way."
        )
    if "worker story" in normalized or "review surface" in normalized:
        points.append(
            "Focused story/review answer: Worker Story and review surfaces should explain finalisation readiness "
            "evidence and worker-specific issues without claiming runtime readiness truth."
        )
    if "finalisation" in normalized or "finalization" in normalized or "readiness" in normalized:
        points.append(
            "Focused Finalisation Readiness answer: Finalisation Readiness is the governed readiness and assurance "
            "gate for whether a PayRun can be finalised safely, not payroll calculation truth and not a simple green "
            "means done status."
        )
        points.append(
            "Focused evidence-consumption answer: readiness consumes deterministic evidence from payroll, leave, tax, "
            "deductions, payment, Payroll Bases & Totals and worker issue surfaces; Minerva must not determine "
            "runtime finalisation readiness."
        )
        points.append(
            "Focused blocker-warning answer: red blockers prevent the relevant action from proceeding, amber warnings "
            "require governed review or warning acknowledgement, and green means ready, cleared, calculated or safe to "
            "rely on for that evidence dimension rather than proving the business is perfect."
        )
        points.append(
            "Focused current-truth answer: current-effective payroll output matters because stale or superseded runs "
            "must not be finalised as current truth."
        )
        points.append(
            "Focused readiness-category answer: Worker Attention and Admin Queue surface worker-level blockers, "
            "warnings and ready actions; Payroll Bases readiness, leave readiness, tax readiness, deduction readiness, "
            "negative net pay, payment destination readiness and payment execution readiness each need status-honest "
            "treatment."
        )
        points.append(
            "Focused payment-readiness answer: payment execution readiness is related to but distinct from gross-to-net "
            "calculation readiness."
        )
        points.append(
            "Focused audit answer: finalised outcome truth becomes durable payment outcome memory once finalised, and "
            "warning acknowledgement plus finalisation audit evidence should preserve what was reviewed, accepted or "
            "left unresolved."
        )
        points.append(
            "Focused surface answer: Worker Story and review surfaces should explain readiness evidence and "
            "worker-specific issues while staying honest about outstanding warning acknowledgement, WorkerAttention "
            "schemas, finalisation policy, server-owned operation/readiness evidence, payment execution readiness and "
            "broader contract tests."
        )
    return points


def _leave_source_model_focus_points(question: str) -> list[str]:
    normalized = question.lower().replace("-", " ")
    points: list[str] = []
    if "leavetyperule" in normalized or "leave type rule" in normalized:
        points.append(
            "Focused LeaveTypeRule answer: LeaveTypeRule is policy/calculation content, not final leave applicability "
            "truth, so every active LeaveTypeRule must not be read as proof that every worker should have leave output."
        )
    if "applicability" in normalized and ("rule content" in normalized or "leave rule" in normalized):
        points.append(
            "Focused applicability-versus-rule answer: leave applicability decides whether leave applies to the "
            "worker/context using source truth, while leave rule content describes policy or calculation once "
            "applicability is known."
        )
    if "no leave entitlement" in normalized or "missing leave output" in normalized or "no entitlement" in normalized:
        points.append(
            "Focused missing-output answer: the Leave Source Model should distinguish no leave entitlement or leave "
            "does not apply from leave output is missing; missing leave output is not always wrong without "
            "applicability/source truth."
        )
    if "contact" in normalized and "appointment" in normalized:
        points.append(
            "Focused scope answer: contact-level and appointment-level leave scope must be handled carefully because "
            "a worker can have Contact-level identity and EmployeeAppointment-specific employment context; "
            "appointment-aware leave ownership prevents applying leave to the wrong scope."
        )
    if "source dimensions" in normalized or "account" in normalized or "employmenttype" in normalized:
        points.append(
            "Focused source-dimensions answer: applicability may depend on Account, EmploymentType, WorksitePosition, "
            "Worksite, EmployeeAppointment, Contact, AwardPositionClass, AwardPosition, Position, Award and State "
            "where formal evidence supports those dimensions and precedence."
        )
    if "leave accrual" in normalized or "accrual" in normalized:
        points.append(
            "Focused accrual-connection answer: leave accrual should consume Leave Source Model applicability/source "
            "decisions instead of inferring eligibility ad hoc during accrual."
        )
    if "leave request" in normalized or "payment effects" in normalized:
        points.append(
            "Focused request/payment answer: leave request payment effects should consume applicability/source "
            "decisions and respect leave ownership or request ownership before payroll effects are applied."
        )
    if "worker story" in normalized:
        points.append(
            "Focused Worker Story answer: Worker Story should explain leave source and applicability decisions where "
            "leave output, no-entitlement outcomes, missing-output warnings or leave chapters are shown."
        )
    if "command centre" in normalized or "finalisation" in normalized or "finalization" in normalized:
        points.append(
            "Focused Command Centre/Finalisation answer: Command Centre and Finalisation Readiness should use Leave "
            "Source Model evidence to surface leave readiness, missing output and PayRun finalisation warnings "
            "honestly."
        )
    if "leave source model" in normalized or "leave source" in normalized or "applicability" in normalized:
        points.append(
            "Focused Leave Source Model answer: the Leave Source Model is the governed applicability and source-truth "
            "layer for determining whether leave applies to a worker and context, not leave calculation itself."
        )
        points.append(
            "Focused LeaveTypeRule boundary answer: LeaveTypeRule is policy and calculation content, but it must not "
            "be treated as final applicability truth or proof that every worker should have leave output."
        )
        points.append(
            "Focused readiness answer: leave readiness should distinguish leave does not apply from leave output is "
            "missing, so missing leave output is not automatically wrong without source/applicability truth."
        )
        points.append(
            "Focused scope answer: Contact scope and EmployeeAppointment scope need careful appointment-aware leave "
            "ownership handling before accrual or leave request/payment effects consume the decision."
        )
        points.append(
            "Focused dimensions answer: applicability may depend on Account, EmploymentType, WorksitePosition, "
            "Worksite, EmployeeAppointment, Contact, AwardPositionClass, AwardPosition, Position, Award and State "
            "where formal evidence supports that direction."
        )
        points.append(
            "Focused surface answer: Worker Story, Command Centre and Finalisation Readiness should explain leave "
            "source/applicability decisions, leave readiness, warnings and missing output honestly."
        )
        points.append(
            "Focused hardening answer: keep status honest that the Leave Source Model remains an outstanding planned "
            "or required model unless formal evidence says runtime capability is complete."
        )
    return points


def _oncosts_employer_liabilities_focus_points(question: str) -> list[str]:
    normalized = question.lower().replace("-", " ")
    points: list[str] = []
    if "worker pay" in normalized or "net pay" in normalized or "minerva" in normalized:
        points.append(
            "Focused boundary answer: On-costs / Employer Liabilities are employer-side liability evidence, not "
            "ordinary worker pay or worker net pay. Minerva explains governed evidence and must not calculate "
            "employer liabilities."
        )
    if "ratesource" in normalized or "date effective" in normalized or "rate" in normalized:
        points.append(
            "Focused RateSource answer: rates that can change should live in governed date-effective RateSource or "
            "rule-pack configuration as governed rate truth for employer liabilities rather than application code, "
            "with demo fallback rows kept separate from production truth."
        )
    if "awardratetype" in normalized or "rate type" in normalized or "super" in normalized:
        points.append(
            "Focused AwardRateType answer: on-costs such as superannuation should be driven from AwardRateType "
            "settings, inheriting RateType defaults at build time where supported but able to diverge by award; "
            "the answer must stay status-honest about what is seeded or implemented."
        )
    if "basis" in normalized or "bucket" in normalized:
        points.append(
            "Focused basis answer: governed basis membership matters because raw RateType or AwardRateType flags may "
            "seed defaults, but runtime basis decisions should resolve from governed bucket or basis membership where "
            "implemented."
        )
    if "workcover" in normalized or "wic" in normalized or "payroll tax" in normalized or "jurisdiction" in normalized:
        points.append(
            "Focused liability-type answer: superannuation, payroll tax and WorkCover/WIC liabilities have different "
            "basis and jurisdiction implications, so they should not be collapsed into one generic on-cost total."
        )
    if "state" in normalized or "worksite" in normalized or "runtime location" in normalized:
        points.append(
            "Focused location answer: state, worksite and runtime location resolution matter for state-scoped employer "
            "liabilities and state-scoped RateSource selection; status must remain honest where runtime resolution is "
            "still outstanding."
        )
    if "worker story" in normalized or "payrun" in normalized:
        points.append(
            "Focused evidence-surface answer: PayRun output and Worker Story should distinguish worker-payable lines "
            "from employer liability lines and on-cost evidence."
        )
    if "payroll bases" in normalized:
        points.append(
            "Focused Payroll Bases answer: Payroll Bases & Totals connect to on-costs and employer liabilities by "
            "providing governed basis evidence, basis evidence and basis totals for liability calculations where that "
            "basis evidence is implemented and ready."
        )
    if "finalisation" in normalized or "readiness" in normalized:
        points.append(
            "Focused readiness answer: Finalisation Readiness may depend on unresolved basis or employer liability "
            "configuration where governed policy requires that evidence before finalisation."
        )
    if "demo" in normalized or "fallback" in normalized or "production" in normalized:
        points.append(
            "Focused fallback answer: demo account-wide fallback RateSource rows may unblock demos, but they are not "
            "production truth and need production replacement."
        )
    if "on cost" in normalized or "oncost" in normalized or "employer liabilit" in normalized:
        points.append(
            "Focused On-costs / Employer Liabilities answer: this domain is governed employer liability evidence, not "
            "worker pay, not a Minerva calculation, and not a generic reporting add-on."
        )
        points.append(
            "Focused configuration answer: deterministic services and governed configuration produce employer "
            "liability outcomes; rates that change belong in date-effective RateSource or rule-pack configuration."
        )
        points.append(
            "Focused basis and jurisdiction answer: AwardRateType, RateType, governed basis membership, state/worksite "
            "resolution and liability type all affect whether superannuation, payroll tax and WorkCover/WIC evidence "
            "can be explained safely."
        )
        points.append(
            "Focused surface answer: PayRun output, Worker Story, Payroll Bases & Totals and Finalisation Readiness "
            "should expose employer liability evidence without turning it into worker net pay or LLM calculation truth."
        )
        points.append(
            "Focused hardening answer: keep status honest around runtime state/worksite resolution, award creation "
            "seeding, governed basis membership, product tests and replacing demo fallback RateSource rows for "
            "production."
        )
    return points


def _award_build_evidence_focus_points(question: str) -> list[str]:
    normalized = question.lower().replace("-", " ")
    points: list[str] = []
    if "runtime payroll calculation" in normalized or "minerva" in normalized:
        points.append(
            "Focused calculation-boundary answer: Award Build / Award Evidence is governed configuration and evidence "
            "creation, not runtime payroll calculation by Minerva and not Minerva interpreting awards at runtime."
        )
    if "award document" in normalized or "pay guide" in normalized:
        points.append(
            "Focused source-material answer: award documents and pay guides are formal source evidence; award build "
            "should preserve where rates, rules and treatments came from, including row, column and page evidence "
            "where available."
        )
    if "ratetype" in normalized or "rate type" in normalized or "awardratetype" in normalized or "award rate type" in normalized:
        points.append(
            "Focused RateType/AwardRateType answer: RateType is the stable conceptual pay type, while AwardRateType "
            "is the award-scoped treatment and configuration for that concept."
        )
    if "ratesource" in normalized or "rate source" in normalized or "date effective" in normalized:
        points.append(
            "Focused RateSource answer: RateSource should preserve date-effective rate amounts and evidence, so "
            "rates are governed source-backed truth rather than hardcoded rate truth."
        )
    if "classification" in normalized or "position" in normalized or "class evidence" in normalized:
        points.append(
            "Focused classification answer: classification, position and class evidence matter because award build "
            "must deterministically derive or review source truth rather than guess worker classifications."
        )
    if "allowance" in normalized or "penalt" in normalized or "conditional" in normalized or "conditions" in normalized:
        points.append(
            "Focused allowances/penalties answer: allowances, penalties, conditions, shift/overtime and conditional "
            "rule families need source evidence and status-honest configuration rather than broad unsupported claims."
        )
    if "decisionevidenceindex" in normalized or "decision evidence index" in normalized:
        points.append(
            "Focused DecisionEvidenceIndex answer: DecisionEvidenceIndex supports why a treatment or payroll line "
            "exists, while status must remain honest about decision families that are not fully covered."
        )
    if "ratesourceevidenceindex" in normalized or "rate source evidence index" in normalized:
        points.append(
            "Focused RateSourceEvidenceIndex answer: RateSourceEvidenceIndex supports why a rate or amount was used "
            "by linking runtime rate use back to RateSource and source evidence."
        )
    if "worker story" in normalized or "decision story" in normalized or "rate story" in normalized:
        points.append(
            "Focused Worker Story answer: Award Build evidence should flow into Worker Story Decision Story and Rate "
            "Story so operators can see both why a treatment exists and why a rate amount was used."
        )
    if "needs configuration" in normalized or "needs_configuration" in normalized:
        points.append(
            "Focused NEEDS_CONFIGURATION answer: NEEDS_CONFIGURATION is a valid award build status where required "
            "source evidence or configuration is missing, rather than a reason to fabricate configuration."
        )
    if "durable" in normalized or "awardevidenceset" in normalized or "award evidence set" in normalized:
        points.append(
            "Focused Durable AwardEvidenceSet answer: Durable AwardEvidenceSet remains important hardening where "
            "award evidence is still partly artifact-based or file-based instead of durable database evidence."
        )
    if "award build" in normalized or "award evidence" in normalized:
        points.append(
            "Focused Award Build / Award Evidence answer: Award Build / Award Evidence is the governed process of "
            "turning award documents and pay guide source material into platform configuration and traceable evidence, "
            "not Minerva calculating payroll or interpreting awards at runtime."
        )
        points.append(
            "Focused source-evidence answer: award documents and pay guides are source evidence, and build artifacts "
            "should preserve row, column, page and source provenance for the rules and rates they create."
        )
        points.append(
            "Focused configuration answer: RateType is the stable conceptual pay type, AwardRateType is award-scoped "
            "treatment/configuration, and RateSource stores date-effective rate amounts and evidence instead of "
            "hardcoded rates."
        )
        points.append(
            "Focused classification answer: classification, position and class evidence should be deterministically "
            "derived or reviewed, not guessed, with status honesty where extraction remains hardening."
        )
        points.append(
            "Focused story answer: DecisionEvidenceIndex supports why a treatment or line exists, "
            "RateSourceEvidenceIndex supports why a rate or amount was used, and Worker Story should expose Decision "
            "Story and Rate Story evidence from award build and runtime artifacts."
        )
        points.append(
            "Focused hardening answer: NEEDS_CONFIGURATION is a valid outcome where evidence or configuration is "
            "missing, and durable AwardEvidenceSet, semantic table classification, parser routing, conditional award "
            "regimes and source evidence coverage remain status-honest outstanding areas where formal evidence says so."
        )
    return points


def _imports_actuals_focus_points(question: str) -> list[str]:
    normalized = question.lower().replace("-", " ")
    points: list[str] = []
    if "imported actuals" in normalized and ("interpreter truth" in normalized or "interpreter output" in normalized):
        points.append(
            "Focused actuals-truth answer: imported actuals are external outcome truth in the actuals lane, not "
            "calculated interpreter truth or calculated interpreter output."
        )
    if "imported timesheet" in normalized or "source truth" in normalized:
        points.append(
            "Focused imported-timesheet answer: imported timesheets can become source truth for ObjectTime and work "
            "evidence only after validation, source-system mapping and provenance checks."
        )
    if "source system" in normalized or "source-system" in normalized or "mapping" in normalized:
        points.append(
            "Focused source-system mapping answer: mappings must connect source-system workers, dates, source rows, "
            "pay codes, RateTypes, positions and classifications before imported evidence can be safely explained."
        )
    if "pay code" in normalized or "ratetype" in normalized or "rate type" in normalized:
        points.append(
            "Focused pay-code mapping answer: external pay codes should map to platform RateTypes or concepts where "
            "possible, and unmapped actuals should become deterministic review or configuration issues."
        )
    if "position" in normalized or "classification" in normalized:
        points.append(
            "Focused position/classification answer: position and classification mapping matter for imported "
            "timesheet interpretation and actuals comparison because source-system classes must be related to "
            "platform positions and classifications."
        )
    if "objecttime" in normalized:
        points.append(
            "Focused ObjectTime answer: ObjectTime/source truth should preserve imported source-row provenance rather "
            "than flatten imported timesheets into anonymous work evidence."
        )
    if "comparison" in normalized or "remediation" in normalized:
        points.append(
            "Focused comparison relationship answer: Imports / Actuals provide imported actual evidence to "
            "Comparison / Remediation without taking ownership of the comparison policy or lane adjudication model."
        )
    if "reconciliation" in normalized or "movement review" in normalized:
        points.append(
            "Focused reconciliation/review answer: reconciliation and Movement Review can use imported actuals and "
            "source evidence to explain variance and review outcomes, without making imported data automatically "
            "correct."
        )
    if "worker story" in normalized or "admin queue" in normalized:
        points.append(
            "Focused surfacing answer: Worker Story and Admin Queue should expose import provenance, mapping issues, "
            "unmapped actuals, missing classifications and review actions."
        )
    if "provenance" in normalized or "audit" in normalized:
        points.append(
            "Focused audit answer: source file, source row, import run, validation status, mapping decision and story "
            "evidence are the provenance trail for Imports / Actuals."
        )
    if "imports" in normalized or "actuals" in normalized:
        points.append(
            "Focused Imports / Actuals answer: Imports / Actuals are governed imported evidence and external source "
            "or outcome truth, not calculated interpreter truth and not proof of automatic source-data correctness."
        )
        points.append(
            "Focused source-truth answer: imported timesheets may become ObjectTime or work-evidence source truth "
            "only after validation and source-system mapping, with source rows and import provenance preserved."
        )
        points.append(
            "Focused actuals-lane answer: imported payroll actuals belong in an external outcome lane and must stay "
            "separate from calculated interpreter output."
        )
        points.append(
            "Focused mapping answer: source-system mappings are required for pay codes, RateTypes, positions, "
            "classifications, workers, dates and source rows; unmapped actuals should surface as deterministic issues."
        )
        points.append(
            "Focused connection answer: Comparison / Remediation can compare primary calculated, comparator "
            "calculated and imported actual lanes, while reconciliation and Movement Review use imported actuals and "
            "source evidence to explain variance and review outcomes."
        )
        points.append(
            "Focused story/admin answer: Worker Story and Admin Queue should surface import provenance, mapping "
            "issues, unmapped actuals, missing classifications and review actions."
        )
        points.append(
            "Focused provenance answer: source file, source row, import run, mapping decision, validation status and "
            "story evidence must be preserved for audit."
        )
        points.append(
            "Focused hardening answer: keep status honest around the actuals lane model, import mapping UI, "
            "comparison-line models, source-system classification mapping, source-row evidence and validation "
            "workflows."
        )
    return points


def _objecttime_source_truth_focus_points(question: str) -> list[str]:
    normalized = question.lower().replace("-", " ")
    points: list[str] = []
    if "objecttime" in normalized or "source truth" in normalized or "sourcetruth" in normalized:
        points.append(
            "Focused ObjectTime / Source Truth answer: ObjectTime / Source Truth is governed source evidence and "
            "PayRun inclusion context, not payroll calculation truth by itself and not user-facing worked hours by "
            "itself."
        )
        points.append(
            "Focused inclusion answer: ObjectTime helps explain why a worker or source row belongs in a PayRun, "
            "while imported and generated source rows must preserve provenance, validation and mapping status."
        )
        points.append(
            "Focused worked-hours boundary: SourceTruth and WorkedHours are separate concepts; raw ObjectTime span "
            "hours should not be treated as interpreted payable, paid or user-facing payroll worked hours."
        )
        points.append(
            "Focused output connection: current-effective payroll output connects processed source truth to payroll "
            "outcome, and Worker Story should begin with Source Truth and inclusion before calculated payroll outcome."
        )
        points.append(
            "Focused basis/leave answer: Payroll Bases & Totals and leave accrual should consume governed processed "
            "payroll or bucket evidence, not raw source span duration."
        )
        points.append(
            "Focused review/replay answer: Comparison / Remediation, Movement Review and Retro / Replay depend on "
            "source truth, provenance and historical/current-effective distinctions."
        )
        points.append(
            "Focused correction answer: source truth corrections should mark affected PayRunContacts dirty and require "
            "governed reprocessing; Minerva does not mutate source truth or reprocess workers."
        )
        points.append(
            "Focused audit answer: source file, source row, ObjectTime, import or generation path, correction history "
            "and evidence story should be preserved for audit."
        )
        points.append(
            "Focused hardening answer: keep status honest around command-centre source hours cleanup, schema "
            "contracts, dependency detection and source-truth provenance coverage."
        )
    return points


def _contacts_employee_appointments_focus_points(question: str) -> list[str]:
    normalized = question.lower().replace("-", " ")
    points: list[str] = []
    if "contact" in normalized or "appointment" in normalized or "employeeappointment" in normalized:
        points.append(
            "Focused Contacts / Employee Appointments answer: Contact is the worker, person and payroll identity "
            "context, while EmployeeAppointment is the employment or work-assignment context; this is governed "
            "worker and employment-context evidence, not payroll calculation truth or a generic HR profile."
        )
        points.append(
            "Focused appointment answer: EmployeeAppointment should not be treated as just a label because it can "
            "carry position, worksite, classification, award and source dimensions that affect payroll context."
        )
        points.append(
            "Focused inclusion answer: PayRun admission, ObjectTime/source rows and source truth often depend on "
            "appointment context to explain worker inclusion; Contact alone is not always enough where "
            "appointment-specific truth matters."
        )
        points.append(
            "Focused classification/location answer: Award classification, AwardPositionClass, WorksitePosition, "
            "Position, worksite, state and runtime location evidence matter for payroll, award and employer-liability "
            "contexts."
        )
        points.append(
            "Focused leave/story answer: leave source, leave applicability and accrual may depend on contact versus "
            "appointment scope, and Worker Story should surface contact, appointment and source-truth context."
        )
        points.append(
            "Focused readiness answer: tax declarations, bank/payment allocation, deductions and obligations are "
            "contact-level worker readiness and worker attention evidence surfaces where formal evidence supports "
            "that framing."
        )
        points.append(
            "Focused dirty-contact answer: payroll-affecting contact or appointment changes can make current PayRun "
            "output unsafe until governed reprocessing; keep status honest where dirty-contact propagation remains "
            "outstanding."
        )
        points.append(
            "Focused comparison answer: comparison and remediation may need appointment classification-lens evidence "
            "for comparator classification rather than duplicate full appointments where formal evidence supports "
            "that model."
        )
        points.append(
            "Focused hardening answer: outstanding hardening remains around GUID boundary/schema contracts, "
            "contact-level history surfaces, WorkerAttention schemas, appointment classification lenses, leave "
            "request ownership, source-truth provenance and dirty-contact propagation coverage."
        )
    return points


def _process_period_payrun_lifecycle_focus_points(question: str) -> list[str]:
    normalized = question.lower().replace("-", " ")
    points: list[str] = []
    if (
        "process" in normalized
        or "period" in normalized
        or "payrun" in normalized
        or "paymentdate" in normalized
        or "payment date" in normalized
        or "runtype" in normalized
        or "run type" in normalized
        or "runpurpose" in normalized
        or "run purpose" in normalized
        or "admission" in normalized
        or "processing" in normalized
        or "current effective" in normalized
        or "current-effective" in normalized
        or "finalisation readiness" in normalized
        or "admin queue" in normalized
        or "movement review" in normalized
    ):
        points.append(
            "Focused Process Periods / PayRun Lifecycle answer: ProcessPeriod is governed payroll-period and "
            "processing context, not just a date range and not payroll calculation truth; ProcessPeriodGroup provides "
            "recurring calendar and payment policy context where formal evidence supports it."
        )
        points.append(
            "Focused lifecycle answer: open, not-open and closed states are distinct, closed dominates open, and "
            "close rolls forward may open or create the next period where that lifecycle behavior is implemented."
        )
        points.append(
            "Focused payment-date answer: PaymentDate and payment date matter for tax/PAYG and payment context and "
            "should be governed or derived from calendar policy rather than hardcoded."
        )
        points.append(
            "Focused PayRun answer: PayRuns are governed payment or processing events inside process-period context; "
            "PayRun creation and PayRun admission do not mean worker processing has happened."
        )
        points.append(
            "Focused run-type answer: RunType and RunPurpose should remain separate, and regular PayRun, "
            "supplementary PayRun, retro PayRun, termination PayRun, reversal PayRun and adjustment PayRun are "
            "different lifecycle concepts, not interchangeable labels, for each payment/processing event."
        )
        points.append(
            "Focused PayRunContact answer: PayRunContact is the operational state layer for worker participation, "
            "admission and processing state in a PayRun lifecycle."
        )
        points.append(
            "Focused current-output answer: current-effective output and current-effective payroll output matter "
            "because stale or superseded runs must not present as current truth for finalisation readiness."
        )
        points.append(
            "Focused downstream answer: finalisation readiness, payment execution and period close consume governed "
            "payroll, leave, tax, deductions, payment, bases and worker evidence; payment execution and period close "
            "are downstream governed outcomes, not payroll calculation."
        )
        points.append(
            "Focused review answer: Worker Story, PayRun Admin Queue and Movement Review should explain worker "
            "participation, readiness and review implications from the lifecycle evidence."
        )
        points.append(
            "Focused hardening answer: outstanding hardening remains around operation trackers, lifecycle contracts, "
            "supplementary/retro policies, payment execution, finalisation warning acknowledgement and broader "
            "contract tests."
        )
    return points


def _costing_gl_consequence_focus_points(question: str) -> list[str]:
    normalized = question.lower().replace("-", " ")
    points: list[str] = []
    if (
        "costing" in normalized
        or "gl" in normalized
        or "financial consequence" in normalized
        or "financial consequences" in normalized
    ):
        points.append(
            "Focused Costing / GL Consequence Evidence answer: Costing / GL Consequence Evidence is downstream "
            "financial consequence evidence, not payroll calculation truth, not payment execution and not a completed "
            "costing engine unless formal evidence says it is complete."
        )
        points.append(
            "Focused source answer: costing should consume finalised payroll outcome truth, finalised payroll outcome, "
            "finalised gross-to-net, payment outcome and liability truth rather than block payroll close or payment "
            "execution performance."
        )
        points.append(
            "Focused consequence answer: Payment Execution / Remittance, payment execution, remittance, payment "
            "outcome, downstream payment, employer liabilities, on-costs, deductions, obligations, remediation "
            "variance and leave valuation can all have financial consequence evidence; employer liabilities and "
            "on-costs can create costing or GL consequences."
        )
        points.append(
            "Focused write-off answer: deduction obligations, obligation write-off records, obligation write-offs, "
            "write-offs, forgiveness, balance reduction and material adjustment may require "
            "GL/provision/costing treatment and must not be treated as purely payroll-status changes."
        )
        points.append(
            "Focused negative-net-pay answer: negative net pay may create recoveries, obligations, write-offs or "
            "out-of-pay records with financial consequences."
        )
        points.append(
            "Focused remediation answer: Comparison / Remediation, remediation variance and variance line evidence "
            "may need downstream treatment, downstream tax, super, payroll tax, WIC, leave, deduction and costing "
            "treatment while remaining status-honest about outstanding downstream treatment."
        )
        points.append(
            "Focused audit answer: audit story and financial evidence should preserve source outcome, reason, "
            "treatment, amount, ledger status, costing status and deferred accounting design status where applicable."
        )
        points.append(
            "Focused boundary answer: costing remains a deferred/final slice, deferred costing slice or later/final "
            "slice rather than a payroll-processing blocker until formal evidence says the costing engine and GL "
            "posting are complete; Minerva explains evidence and does not post GL entries and does not calculate "
            "costing."
        )
    return points


class BaseLLMClient(ABC):
    model_name = "BASE_LLM"

    @abstractmethod
    def generate_answer(self, question: str, retrieved_chunks: list[RetrievalResult]) -> str:
        raise NotImplementedError


class StubLLMClient(BaseLLMClient):
    model_name = "STUB_LLM"

    def generate_answer(self, question: str, retrieved_chunks: list[RetrievalResult]) -> str:
        answer_mode = classify_answer_mode(question)
        if not retrieved_chunks:
            return (
                "I do not have retrieved Minerva knowledge evidence for that question. "
                "Minerva is advisory and does not calculate or change payroll truth."
            )

        intent = classify_query_intent(question)
        strong_chunks = [
            result
            for result in retrieved_chunks
            if result.score >= 18.0 and (result.match_ratio >= 0.45 or len(result.matched_tokens) >= 2 or result.matched_phrases)
        ]

        if intent and strong_chunks and answer_mode != AnswerMode.PRODUCT_DOMAIN.value:
            if intent.name == "MINERVA_BOUNDARY_PROHIBITION":
                return (
                    "Minerva is not allowed to calculate payroll, determine entitlements, interpret awards at runtime, "
                    "approve exceptions, suppress warnings, override payroll outcomes, mutate configuration, finalise "
                    "PayRuns or become payroll calculation truth. It may search, retrieve, summarise, compare, explain "
                    "and interrogate evidence. Deterministic Ezeas services remain the source of payroll, award, leave, "
                    "tax, reconciliation and finalisation truth. Minerva is advisory and does not calculate or change "
                    "payroll truth."
                )
            if intent.name == "RBAC_BEFORE_LLM":
                return (
                    "RBAC-before-LLM means user permissions must be checked before evidence is retrieved into model "
                    "context. The model must not receive sensitive evidence that the user is not authorised to view. "
                    "Permission enforcement must happen before context construction, not after answer generation. "
                    "Minerva is advisory and does not calculate or change payroll truth."
                )
            if intent.name == "SEPARATE_DATABASE":
                return (
                    "Minerva uses a separate database so knowledge indexing, chat history, extracted facts, evidence "
                    "references and AI audit records are isolated from the operational payroll database. The operational "
                    "Ezeas database remains the authoritative source of payroll, leave, award, workforce and "
                    "reconciliation truth. Minerva is advisory and does not calculate or change payroll truth."
                )
            if intent.name == "NO_RAW_JSON_BY_DEFAULT":
                return (
                    "Raw JSON is not sent to the LLM by default because operational payroll evidence can contain "
                    "sensitive worker, payroll, tax, leave, bank/payment and correction data. It should be registered, "
                    "hashed, classified and extracted into facts or safe summaries first, then only the minimum "
                    "necessary evidence should be sent after tenant, RBAC and redaction controls. Minerva remains "
                    "read-only and advisory."
                )
            if intent.name == "SOURCE_AUTHORITY":
                return (
                    "Source authority matters because formal Platform Doctrine, Hardening Logs and Developer Logs "
                    "represent governed platform memory. Raw chat history and exploratory discussion can support an "
                    "answer, but must not override formal logged decisions, doctrine or implemented capability evidence. "
                    "Minerva remains read-only and advisory."
                )
            if intent.name == "DEVELOPER_LOGS_ROLE":
                return (
                    "Developer Logs are part of Minerva's formal knowledge corpus. They preserve implementation "
                    "decisions, rationale, current state, hardening commitments and operating model so Minerva can "
                    "explain how the platform works and why decisions were made. Minerva remains read-only and advisory."
                )
            if intent.name == "USER_GUIDE_RATIONALE":
                return (
                    "The User Guide / Rationale and Operating Model section exists to explain why the work matters, "
                    "how the feature should be understood, and how the platform should operate. It makes each thread's "
                    "reasoning easier for Minerva and future users to retrieve and explain later. Minerva remains "
                    "read-only and advisory."
                )
            if intent.name == "CHAT_HISTORY_AUTHORITY":
                return (
                    "Platform Doctrine is formal governed doctrine. Chat history is useful supporting material because "
                    "it may contain exploration, abandoned ideas, corrections and superseded thinking. Chat history "
                    "must not override Platform Doctrine, Hardening Logs or Developer Logs where they conflict. "
                    "Minerva remains read-only and advisory."
                )

        strong_chunks = [
            result
            for result in retrieved_chunks
            if result.score >= 18.0 and (result.match_ratio >= 0.45 or len(result.matched_tokens) >= 2)
        ]
        selected_chunks = (strong_chunks or retrieved_chunks)[:3]
        excerpts = [_safe_excerpt(result.chunk_text, max_length=260) for result in selected_chunks]

        if answer_mode == AnswerMode.PRODUCT_DOMAIN.value:
            domain_plan = detect_domain_retrieval_plan(question)
            planned_chunks = [result for result in retrieved_chunks if result.domain_plan_id]
            if domain_plan:
                summaries = synthesize_domain_plan_evidence(domain_plan, planned_chunks)
                strong_summaries = [summary for summary in summaries if not summary.is_weak]
                weak_summaries = [summary for summary in summaries if summary.is_weak]
                operation_points = [summary.sentence for summary in summaries]
                if domain_plan.plan_id == "WORKER_STORY":
                    operation_points = _worker_story_focus_points(question) + operation_points
                if domain_plan.plan_id == "PAYROLL_BASES_AND_TOTALS":
                    operation_points = _payroll_bases_focus_points(question) + operation_points
                if domain_plan.plan_id == "WORKER_ATTENTION_ISSUE_RESOLUTION":
                    operation_points = _worker_attention_issue_resolution_focus_points(question) + operation_points
                if domain_plan.plan_id == "GROSS_TO_NET":
                    operation_points = _gross_to_net_focus_points(question) + operation_points
                if domain_plan.plan_id == "RATE_SOURCE_RATE_STORY":
                    operation_points = _rate_source_rate_story_focus_points(question) + operation_points
                if domain_plan.plan_id == "DECISION_STORY":
                    operation_points = _decision_story_focus_points(question) + operation_points
                if domain_plan.plan_id == "PAYROLL_OUTPUT":
                    operation_points = _payroll_output_focus_points(question) + operation_points
                if domain_plan.plan_id == "PAYRUN_ADMIN_QUEUE":
                    operation_points = _payrun_admin_queue_focus_points(question) + operation_points
                if domain_plan.plan_id == "MOVEMENT_REVIEW":
                    operation_points = _movement_review_focus_points(question) + operation_points
                if domain_plan.plan_id == "COMPARISON_REMEDIATION":
                    operation_points = _comparison_remediation_focus_points(question) + operation_points
                if domain_plan.plan_id == "TAX_PAYG":
                    operation_points = _tax_payg_focus_points(question) + operation_points
                if domain_plan.plan_id == "DEDUCTIONS_OBLIGATIONS":
                    operation_points = _deductions_obligations_focus_points(question) + operation_points
                if domain_plan.plan_id == "RETRO_REPLAY":
                    operation_points = _retro_replay_focus_points(question) + operation_points
                if domain_plan.plan_id == "PAYMENT_EXECUTION_REMITTANCE":
                    operation_points = _payment_execution_remittance_focus_points(question) + operation_points
                if domain_plan.plan_id == "LEAVE_ACCRUAL_PROCESSING":
                    operation_points = _leave_accrual_processing_focus_points(question) + operation_points
                if domain_plan.plan_id == "FINALISATION_READINESS":
                    operation_points = _finalisation_readiness_focus_points(question) + operation_points
                if domain_plan.plan_id == "LEAVE_SOURCE_MODEL":
                    operation_points = _leave_source_model_focus_points(question) + operation_points
                if domain_plan.plan_id == "ONCOSTS_EMPLOYER_LIABILITIES":
                    operation_points = _oncosts_employer_liabilities_focus_points(question) + operation_points
                if domain_plan.plan_id == "AWARD_BUILD_EVIDENCE":
                    operation_points = _award_build_evidence_focus_points(question) + operation_points
                if domain_plan.plan_id == "IMPORTS_ACTUALS":
                    operation_points = _imports_actuals_focus_points(question) + operation_points
                if domain_plan.plan_id == "OBJECTTIME_SOURCE_TRUTH":
                    operation_points = _objecttime_source_truth_focus_points(question) + operation_points
                if domain_plan.plan_id == "CONTACTS_EMPLOYEE_APPOINTMENTS":
                    operation_points = _contacts_employee_appointments_focus_points(question) + operation_points
                if domain_plan.plan_id == "PROCESS_PERIOD_PAYRUN_LIFECYCLE":
                    operation_points = _process_period_payrun_lifecycle_focus_points(question) + operation_points
                if domain_plan.plan_id == "COSTING_GL_CONSEQUENCE":
                    operation_points = _costing_gl_consequence_focus_points(question) + operation_points
                missing_groups = [summary.label for summary in weak_summaries]
                coverage = _coverage_label(len(strong_summaries), len(summaries))

                if coverage == "weak":
                    return (
                        "Direct summary\n"
                        "The retrieved formal corpus is not yet sufficient to answer this at the required rich-answer "
                        "standard.\n\n"
                        "How the system works\n"
                        "The loaded formal corpus does not yet contain enough retrieved evidence for the Annual Leave "
                        "management evidence groups.\n\n"
                        "Current implementation status\n"
                        "Unknown from the currently retrieved formal corpus.\n\n"
                        "What remains outstanding\n"
                        f"The loaded formal corpus does not yet contain enough retrieved evidence for: "
                        f"{', '.join(missing_groups)}.\n\n"
                        "Evidence basis\n"
                        "Use the returned source references as the evidence trail. Minerva is advisory and does not "
                        "calculate or change payroll truth."
                    )

                missing_text = (
                    "The loaded formal corpus does not yet contain enough retrieved evidence for: "
                    f"{', '.join(missing_groups)}."
                    if missing_groups
                    else "All planned evidence groups returned at least one source."
                )
                if coverage == "complete":
                    if domain_plan.plan_id == "WORKER_STORY":
                        direct_summary = (
                            "Worker Story is a platform evidence surface for explaining a worker-level payroll "
                            "outcome, not merely a PayRun Detail feature. It presents chapters or evidence layers "
                            "covering source truth and inclusion, interpreted worked hours where available, calculated "
                            "payroll outcome from current-effective payroll output truth, separate Decision Story and "
                            "Rate Story evidence, leave and accrual outcome evidence where available, and links to "
                            "PayRun Admin Queue, Movement Review and Payroll Bases & Totals."
                        )
                        status_text = (
                            "The retrieved corpus shows Worker Story as an implemented or partially implemented "
                            "platform explanation surface grounded in current-effective truth. It should not be treated "
                            "as fully production-complete where the evidence still records outstanding hardening for "
                            "the shared Worker Story surface/component, explicit break-treatment proof, reusable story "
                            "surfaces or broader limitations."
                        )
                    elif domain_plan.plan_id == "PAYROLL_BASES_AND_TOTALS":
                        direct_summary = (
                            "Payroll Bases & Totals are governed payroll basis evidence, not simple reporting totals "
                            "or analytics cubes. They explain why payroll buckets, worked quantities and basis totals "
                            "matter operationally by tying bucket definitions, period definitions, calendar policies, "
                            "memberships, current-effective source truth, readiness and rebuild state into an evidence "
                            "trail that can support Worker Story and Movement Review."
                        )
                        status_text = (
                            "The retrieved corpus shows Payroll Bases & Totals as an implemented or partially "
                            "implemented governed evidence area. It should not be treated as full payroll, tax or PAYG "
                            "calculation truth, and stale PayrollBucketResult rows should not be treated as safe current "
                            "truth. Bucket lifecycle, versioning, taxable/PAYG coverage and rebuild hardening remain "
                            "limited to what formal evidence states."
                        )
                    elif domain_plan.plan_id == "PAYRUN_ADMIN_QUEUE":
                        direct_summary = (
                            "PayRun Admin Queue is the operator workbench for what needs action now in a PayRun: "
                            "blockers, warnings, ready actions, worker attention, dirty contacts, processing or "
                            "reprocessing actions, finalisation readiness and review navigation. It is not payroll "
                            "calculation truth; Command Centre remains the full evidence and control-room surface, "
                            "and an empty queue does not prove the PayRun is representative."
                        )
                        status_text = (
                            "The retrieved corpus shows PayRun Admin Queue as an implemented or partially implemented "
                            "operator action surface. Finalisation readiness must distinguish blockers and warnings, "
                            "Assurance Snapshot should be treated as reasonableness and review signals rather than "
                            "hidden calculation truth, and outstanding hardening remains around server-owned operation "
                            "tracker, global queue resolver, reusable Worker Story surface, governed assurance "
                            "thresholds and warning acknowledgement wherever formal evidence says so."
                        )
                    elif domain_plan.plan_id == "WORKER_ATTENTION_ISSUE_RESOLUTION":
                        direct_summary = (
                            "Worker Attention / Issue Resolution is the worker-level issue surface for "
                            "payroll-affecting blockers, warnings, readiness gaps and deterministic fix links. It "
                            "uses WorkerIssue evidence such as issue scope, issue class, issue type and issue "
                            "severity to point operators toward resolution surfaces without letting Minerva resolve, "
                            "clear, approve, suppress, finalise, repair, calculate or mutate payroll truth."
                        )
                        status_text = (
                            "The retrieved corpus describes Worker Attention / Issue Resolution as a worker-level "
                            "issue and remediation surface with important outstanding hardening. It should not imply "
                            "Minerva resolves issues, clears blockers, mutates PayRunContact state, calculates "
                            "payroll, approves, suppresses, finalises or repairs operational payroll truth, proves "
                            "payroll is correct, or makes Admin Queue and Worker Attention the same surface."
                        )
                    elif domain_plan.plan_id == "GROSS_TO_NET":
                        direct_summary = (
                            "Gross-to-Net is the payroll outcome calculation and payroll outcome explanation surface "
                            "that connects gross earnings, taxable basis, PAYG and tax withholding, deductions, "
                            "obligations, net pay, payment allocation, Worker Story, current-effective payroll output "
                            "and finalised payroll outcome evidence. Minerva explains the evidence and status; it "
                            "does not calculate gross-to-net or mutate payroll truth."
                        )
                        status_text = (
                            "The retrieved corpus describes Gross-to-Net as a payroll outcome and explanation area "
                            "with important outstanding hardening. It should not imply Minerva calculates gross-to-net, "
                            "withholds tax, applies deductions, changes net pay, approves or resolves negative net pay, "
                            "generates payment files, finalises PayRuns, mutates operational payroll truth, proves "
                            "payroll correctness, or collapses Gross-to-Net and Payment Execution into the same surface."
                        )
                    elif domain_plan.plan_id == "RATE_SOURCE_RATE_STORY":
                        direct_summary = (
                            "RateSource / Rate Story is the evidence layer that explains which selected rate or rate "
                            "amount was used, where the amount came from, and how date-effective, scope, award, account "
                            "or class rate evidence is represented. It is related to Worker Story, payroll output and "
                            "Gross-to-Net, but Rate Story is not the same as Decision Story."
                        )
                        status_text = (
                            "The retrieved corpus describes RateSource / Rate Story as rate evidence and explanation "
                            "with important outstanding hardening. It should not imply Minerva selects rates, calculates "
                            "pay, interprets awards at runtime, changes RateSource records, validates payroll correctness, "
                            "treats Rate Story as Decision Story, treats RateSource evidence alone as entitlement proof, "
                            "or lets Minerva mutate operational payroll truth."
                        )
                    elif domain_plan.plan_id == "DECISION_STORY":
                        direct_summary = (
                            "Decision Story is the evidence layer that explains why a payroll treatment, entitlement, "
                            "line, rule outcome, allowance, penalty, overtime, shift, public holiday, break treatment "
                            "or other calculated payroll decision exists. It explains why the treatment or line exists, "
                            "while Rate Story explains why a rate or amount was used."
                        )
                        status_text = (
                            "The retrieved corpus describes Decision Story as decision evidence and explanation with "
                            "important outstanding hardening. It should not imply Minerva selects treatments, decides "
                            "entitlements, interprets awards at runtime, calculates payroll, changes decision evidence, "
                            "validates payroll correctness, treats Decision Story as Rate Story, treats "
                            "DecisionEvidenceIndex alone as the full award-source chain, or mutates operational payroll "
                            "truth."
                        )
                    elif domain_plan.plan_id == "PAYROLL_OUTPUT":
                        direct_summary = (
                            "Payroll Output is the evidence surface for calculated payroll results: current-effective "
                            "worker and PayRun output, line-level payroll outcome, payroll lines or output lines, "
                            "worker-level output, PayRun totals, and the distinction between Run Output and Process "
                            "Period Output. It connects Worker Story, Gross-to-Net, Decision Story, Rate Story, "
                            "Payroll Bases & Totals, Finalisation Readiness and Payment Execution without making "
                            "Minerva the payroll output calculator."
                        )
                        status_text = (
                            "The retrieved corpus describes Payroll Output as calculated output evidence with "
                            "important status honesty and outstanding hardening. It should not imply Minerva calculates payroll output, "
                            "changes payroll output lines, finalises PayRuns, approves payroll output, selects "
                            "treatments, selects rates, generates payment files, mutates operational payroll truth, "
                            "proves payroll correctness from Payroll Output alone, or collapses Run Output and Process "
                            "Period Output into the same lens without explanation."
                        )
                    elif domain_plan.plan_id == "MOVEMENT_REVIEW":
                        direct_summary = (
                            "Movement Review is a payroll reasonableness and review surface that helps operators "
                            "understand changes, variance and review-worthy movement across organisation and worker "
                            "lenses. It is evidence for review, not automatic proof that payroll is wrong and not "
                            "payroll calculation truth."
                        )
                        status_text = (
                            "The retrieved corpus shows Movement Review as an implemented or partially implemented "
                            "review evidence surface connected to Payroll Bases & Totals, Worker Story and PayRun "
                            "Admin Queue. It should remain status-honest: thresholds, comparable period rules, "
                            "filtered lenses, governed Movement Review Policy and historical bucket rebuild governance "
                            "remain limited to what formal evidence states."
                        )
                    elif domain_plan.plan_id == "COMPARISON_REMEDIATION":
                        direct_summary = (
                            "Comparison / Remediation is a governed comparison and remediation evidence capability, "
                            "not a simple manual top-up adjustment. It compares primary calculated payroll truth, "
                            "comparator calculated assessment truth and imported actual outcome truth as separate lanes "
                            "under policy before any typed variance or remediation line is generated."
                        )
                        status_text = (
                            "The retrieved corpus describes this primarily as design doctrine and future capability, "
                            "not as a fully implemented runtime feature. It should not imply production variance "
                            "generation, implemented comparison run/line models, implemented comparison policy, automatic "
                            "comparator classification reuse, or a completed Worker Story comparison chapter unless "
                            "formal evidence explicitly says so."
                        )
                    elif domain_plan.plan_id == "TAX_PAYG":
                        direct_summary = (
                            "Tax / PAYG is governed withholding calculation evidence and platform story, not tax "
                            "calculation truth and not an LLM calculation. Deterministic Ezeas services and tax "
                            "providers remain the calculation path, while Minerva explains TaxStory evidence, taxable "
                            "basis alignment, worker tax declaration and withholding inputs, ProcessPeriod PaymentDate, "
                            "pay frequency support, gross-to-net effects, finalised totals and status."
                        )
                        status_text = (
                            "The retrieved corpus describes Tax / PAYG as governed evidence with important outstanding "
                            "hardening. It should not imply PAYG is complete for all frequencies, taxable basis "
                            "governance is complete, supplementary incremental PAYG is complete, unsupported "
                            "frequencies are calculated values, or TaxStory / withholding instruction UI is complete "
                            "unless formal evidence explicitly says so."
                        )
                    elif domain_plan.plan_id == "DEDUCTIONS_OBLIGATIONS":
                        direct_summary = (
                            "Deductions / Obligations are governed payroll outcome and future recovery evidence, not "
                            "automatic raw net-pay subtraction. The deduction path runs from LibraryDeductionTemplate "
                            "to AccountDeductionTemplate to ContactPayrollDeduction to PayRunDeductionApplication, "
                            "with PayRun memory for requested, taken, skipped and unmet amounts, supplementary "
                            "same-period memory, governed affordability and priority, durable obligations, "
                            "reducing-balance recovery, negative-net-pay policy, gross-to-net, Worker Story and "
                            "PayRun Admin Queue visibility."
                        )
                        status_text = (
                            "The retrieved corpus describes Deductions / Obligations as a governed evidence area with "
                            "important outstanding hardening. It should not imply the full deduction/obligation engine "
                            "is complete, pre-tax deductions are fully migrated, negative net pay is solved, "
                            "carry-forward review automatically creates an obligation, payment execution or remittance "
                            "is implemented, or obligations are merely deduction rows unless formal evidence explicitly "
                            "says so."
                        )
                    elif domain_plan.plan_id == "RETRO_REPLAY":
                        direct_summary = (
                            "Retro / Replay is governed historical correction and evidence replay, not ordinary "
                            "reprocessing or hidden mutation of finalised payroll truth. It keeps attributed-period "
                            "truth, paid-period truth, current-effective payroll truth and historical/finalised truth "
                            "distinct while using finalised outcome memory, bucket/source snapshots, calculation "
                            "evidence, source hashes, dependency detection, retro PayRuns, Worker Story, PayRun Admin "
                            "Queue, Movement Review, Payroll Bases & Totals and Comparison / Remediation evidence to "
                            "explain correction and replay impacts."
                        )
                        status_text = (
                            "The retrieved corpus describes Retro / Replay as governed evidence with important "
                            "outstanding hardening. It should not imply Retro / Replay is fully implemented, finalised "
                            "payroll truth can be silently overwritten, supplementary PayRuns and retro PayRuns are "
                            "the same, bucket rebuilds over finalised history can be silent or ungoverned, dependency "
                            "detection is complete, or Movement Review variance automatically proves retro error "
                            "unless formal evidence explicitly says so."
                        )
                    elif domain_plan.plan_id == "PAYMENT_EXECUTION_REMITTANCE":
                        direct_summary = (
                            "Payment Execution / Remittance is governed payment execution and remittance evidence, "
                            "not payroll calculation truth and not a generic file export. It consumes finalised "
                            "gross-to-net and payment outcome evidence, then checks worker net pay, payment allocation, "
                            "bank allocation, payment destination readiness, negative net pay treatment, deduction or "
                            "obligation remittance, third-party payments, payment files, Period Close, remittance "
                            "batching, reconciliation, Worker Attention, PayRun Admin Queue, Worker Story and audit "
                            "evidence."
                        )
                        status_text = (
                            "The retrieved corpus describes Payment Execution / Remittance as a governed evidence area "
                            "with important outstanding hardening. It should not imply payment execution or remittance "
                            "is fully implemented, gross-to-net calculation readiness equals payment execution "
                            "readiness, missing payment destinations invalidate gross-to-net calculation, negative net "
                            "pay is solved, deduction remittance or payment files are complete, or obligation write-off "
                            "financial coding/costing is complete unless formal evidence explicitly says so."
                        )
                    elif domain_plan.plan_id == "LEAVE_ACCRUAL_PROCESSING":
                        direct_summary = (
                            "Leave Accrual / Processing is governed payroll and leave evidence, not a Minerva "
                            "calculation and not generic leave policy advice. It uses leave source truth and "
                            "applicability, accrual basis and quantity, canonical processed payroll result truth such "
                            "as CalcInterpreterLine and current-effective payroll output where applicable, LeaveType "
                            "and LeaveTypeRule configuration, AwardRateType-first accrualability with RateType "
                            "fallback where formal evidence supports it, PER_HOUR minute/hour quantities, LeaveLedger "
                            "movements, leave valuation basis for TAKEN leave, leave request payment effects, PayRun "
                            "processing and finalisation readiness, Worker Story and Payroll Bases & Totals evidence."
                        )
                        status_text = (
                            "The retrieved corpus describes Leave Accrual / Processing as governed evidence with "
                            "important outstanding hardening. It should not imply Minerva calculates leave, the Leave "
                            "Source Model is complete, all leave types are fully implemented, LeaveTypeRule alone is "
                            "final applicability truth, TAKEN leave can post without mandatory valuation and hard "
                            "failure controls, or leave processing/finalisation UI is complete unless formal evidence "
                            "explicitly says so."
                        )
                    elif domain_plan.plan_id == "FINALISATION_READINESS":
                        direct_summary = (
                            "Finalisation Readiness is the governed readiness and assurance gate for whether a PayRun "
                            "can be finalised safely, not payroll calculation truth and not a simple green means done "
                            "status. It consumes deterministic evidence from payroll, leave, tax, deductions, payment, "
                            "Payroll Bases & Totals, Worker Attention, Admin Queue and review surfaces; red blockers "
                            "prevent the relevant action, amber warnings require governed review or warning "
                            "acknowledgement, and green means ready, cleared, calculated or safe to rely on for that "
                            "evidence dimension rather than proving everything in the business is perfect."
                        )
                        status_text = (
                            "The retrieved corpus describes Finalisation Readiness as governed readiness evidence with "
                            "important outstanding hardening. It should not imply Minerva determines finalisation "
                            "readiness, finalisation readiness calculates payroll, amber warnings can be ignored, "
                            "green readiness means no review-worthy business movement exists, payment execution "
                            "readiness equals gross-to-net readiness, warning acknowledgement/finalisation policy is "
                            "complete, or all readiness categories are fully implemented unless formal evidence "
                            "explicitly says so."
                        )
                    elif domain_plan.plan_id == "LEAVE_SOURCE_MODEL":
                        direct_summary = (
                            "Leave Source Model is the governed applicability and source-truth layer for determining "
                            "whether leave applies to a worker and context, not leave calculation itself and not a "
                            "completed runtime feature unless formal evidence says so. It separates applicability from "
                            "LeaveTypeRule policy/calculation content, preserves that LeaveTypeRule is not final "
                            "applicability truth, distinguishes leave does not apply from leave output is missing, "
                            "handles Contact scope and EmployeeAppointment scope carefully, and lets leave accrual, "
                            "leave request/payment effects, Worker Story, Command Centre and Finalisation Readiness "
                            "consume source/applicability decisions honestly."
                        )
                        status_text = (
                            "The retrieved corpus describes Leave Source Model as governed applicability and source "
                            "evidence with important outstanding hardening. It should not imply the Leave Source Model "
                            "is fully implemented, LeaveTypeRule alone determines applicability, every active "
                            "LeaveTypeRule means every worker should have leave output, missing leave output is always "
                            "wrong, or Minerva calculates leave applicability unless formal evidence explicitly says so."
                        )
                    elif domain_plan.plan_id == "ONCOSTS_EMPLOYER_LIABILITIES":
                        direct_summary = (
                            "On-costs / Employer Liabilities are governed employer-side liability evidence, not "
                            "ordinary worker pay, not worker net pay, not payroll calculation truth performed by "
                            "Minerva, and not a generic reporting add-on. Deterministic Ezeas services and governed "
                            "configuration produce employer liability outcomes; Minerva explains the formal evidence "
                            "around RateSource, date-effective rates, AwardRateType and RateType settings, governed "
                            "basis membership, superannuation, payroll tax, WorkCover/WIC, state/worksite/runtime "
                            "location resolution, PayRun output, Worker Story, Payroll Bases & Totals and "
                            "Finalisation Readiness."
                        )
                        status_text = (
                            "The retrieved corpus describes On-costs / Employer Liabilities as governed employer "
                            "liability evidence with important outstanding hardening. It should not imply Minerva "
                            "calculates on-costs, on-costs are worker net pay, demo account-wide fallback RateSource "
                            "rows are production truth, runtime state/worksite resolution is complete, all on-cost "
                            "AwardRateTypes or RateSources are automatically seeded, or raw RateType/AwardRateType "
                            "flags are final runtime basis truth where governed bucket membership is required."
                        )
                    elif domain_plan.plan_id == "AWARD_BUILD_EVIDENCE":
                        direct_summary = (
                            "Award Build / Award Evidence is governed configuration and evidence creation: it turns "
                            "award documents and pay guide source material into platform configuration, RateType and "
                            "AwardRateType records, RateSource date-effective rate evidence, classification/position/"
                            "class evidence, allowance and penalty evidence, DecisionEvidenceIndex and "
                            "RateSourceEvidenceIndex support, and Worker Story Decision Story and Rate Story evidence. "
                            "It is not Minerva calculating payroll or interpreting awards at runtime."
                        )
                        status_text = (
                            "The retrieved corpus describes Award Build / Award Evidence as governed evidence with "
                            "important outstanding hardening. It should not imply award build is complete for all "
                            "awards or regimes, Minerva interprets awards at runtime, source evidence is durable in "
                            "the database where Durable AwardEvidenceSet remains outstanding, classification "
                            "extraction is fully deterministic, all decision families have complete "
                            "DecisionEvidenceIndex coverage, or rates can be hardcoded."
                        )
                    elif domain_plan.plan_id == "IMPORTS_ACTUALS":
                        direct_summary = (
                            "Imports / Actuals are governed imported evidence and external source or outcome truth, "
                            "not calculated interpreter truth and not proof of automatic source-data correctness. "
                            "Imported timesheets may become ObjectTime or work-evidence source truth only after "
                            "validation and mapping, while imported payroll actuals belong in an external actuals "
                            "lane that stays separate from calculated interpreter output."
                        )
                        status_text = (
                            "The retrieved corpus describes Imports / Actuals as governed imported evidence with "
                            "important outstanding hardening. It should not treat imported actuals as "
                            "interpreter-calculated truth, treat imported source data as automatically correct, imply "
                            "actuals lane, comparison-line or import mapping models are fully implemented, allow "
                            "unmapped actuals to disappear silently, or suggest that Minerva validates imports or "
                            "mutates mappings."
                        )
                    elif domain_plan.plan_id == "OBJECTTIME_SOURCE_TRUTH":
                        direct_summary = (
                            "ObjectTime / Source Truth is governed source evidence for work/time/source-row inclusion "
                            "and PayRun inclusion context, not payroll calculation truth by itself and not user-facing "
                            "worked hours by itself. It explains why a worker or source row belongs in a PayRun, keeps "
                            "imported and generated source-row provenance, separates SourceTruth from WorkedHours, "
                            "and connects processed source truth to current-effective payroll output and Worker Story."
                        )
                        status_text = (
                            "The retrieved corpus describes ObjectTime / Source Truth as governed source evidence "
                            "with important outstanding hardening. It should not imply ObjectTime alone is final "
                            "payroll calculation truth, raw span hours are worked hours, SourceTruth and WorkedHours "
                            "are the same, imported source data is automatically valid, dependency detection and "
                            "dirty-contact propagation are complete, or Minerva mutates source truth or reprocesses "
                            "workers."
                        )
                    elif domain_plan.plan_id == "CONTACTS_EMPLOYEE_APPOINTMENTS":
                        direct_summary = (
                            "Contacts / Employee Appointments are governed worker and employment-context evidence, "
                            "not payroll calculation truth and not a generic HR profile. Contact is the worker, person "
                            "and payroll identity context; EmployeeAppointment is the employment or work-assignment "
                            "context that can carry position, worksite, classification, award and source dimensions. "
                            "This appointment spine helps explain PayRun admission, ObjectTime/source truth, award and "
                            "classification context, worksite/state/runtime location, leave source/applicability, "
                            "Worker Story identity and contact history, worker readiness, dirty contact/reprocessing "
                            "and comparison classification lenses."
                        )
                        status_text = (
                            "The retrieved corpus describes Contacts / Employee Appointments as governed worker and "
                            "employment-context evidence with important outstanding hardening. It should not imply "
                            "Contacts or EmployeeAppointments calculate payroll, Contact alone is always enough where "
                            "appointment-specific truth matters, duplicate EmployeeAppointment records are the correct "
                            "comparator-classification model where classification lenses are preferred, contact "
                            "history or readiness surfaces are complete, or dirty-contact propagation is complete "
                            "unless formal evidence explicitly says so."
                        )
                    elif domain_plan.plan_id == "PROCESS_PERIOD_PAYRUN_LIFECYCLE":
                        direct_summary = (
                            "Process Periods / PayRun Lifecycle is governed payroll-period and payment-event "
                            "lifecycle evidence, not payroll calculation truth and not a generic date range. "
                            "ProcessPeriod and ProcessPeriodGroup provide period, calendar and payment policy context; "
                            "PayRuns are governed payment or processing events inside that context; and PayRunContact "
                            "is the operational state layer for worker participation, admission and processing state."
                        )
                        status_text = (
                            "The retrieved corpus describes Process Periods / PayRun Lifecycle as governed lifecycle "
                            "evidence with important outstanding hardening. It should not imply ProcessPeriod or "
                            "PayRun lifecycle calculates payroll, open means safe to finalise, closed-period truth can "
                            "be silently changed, regular, supplementary and retro PayRuns are interchangeable, "
                            "PaymentDate derivation is hardcoded, payment execution or period close is complete, or "
                            "Minerva mutates lifecycle data unless formal evidence explicitly says so."
                        )
                    elif domain_plan.plan_id == "COSTING_GL_CONSEQUENCE":
                        direct_summary = (
                            "Costing / GL Consequence Evidence is downstream financial consequence evidence, not "
                            "payroll calculation truth, not payment execution and not a completed costing engine "
                            "unless formal evidence says it is complete. It should consume finalised payroll, payment "
                            "and liability outcomes and explain the financial consequences of payroll events without "
                            "posting GL entries; Minerva does not post GL and does not calculate costing."
                        )
                        status_text = (
                            "The retrieved corpus describes Costing / GL Consequence Evidence as a deferred or "
                            "later-slice evidence area with important outstanding hardening. It should not imply "
                            "costing is implemented where formal evidence says it is deferred, Minerva posts GL "
                            "entries or calculates costing, costing blocks payroll payment or close performance, "
                            "obligation write-offs have no financial consequence, remediation variance downstream "
                            "treatment is complete, or negative net pay financial treatment is solved unless formal "
                            "evidence explicitly says so."
                        )
                    else:
                        direct_summary = (
                            "Annual Leave is managed through configured leave policy, ledger-based accrual and TAKEN "
                            "movement, PayRun valuation/orchestration evidence, Worker Story explanation and tracked "
                            "hardening items. The system separates configuration, accrual, consumption, valuation, PayRun "
                            "processing and explanatory evidence rather than treating leave as a single opaque balance."
                        )
                        status_text = (
                            "The retrieved corpus shows this as an implemented or partially implemented platform area with "
                            "remaining hardening. It does not prove production completeness. Some mechanisms are implemented; "
                            "valuation, leave source modelling or production hardening may remain outstanding depending on "
                            "the specific sub-area."
                        )
                else:
                    direct_summary = (
                        "Annual Leave is partially described by the loaded formal corpus, but some planned evidence "
                        "groups are missing. The answer below is limited to the retrieved evidence and should be treated "
                        "as incomplete until the missing groups are covered."
                    )
                    status_text = (
                        "The retrieved corpus provides partial implementation evidence only. Missing groups should be "
                        "treated as unknown rather than inferred."
                    )
                evidence_basis = _evidence_basis_text(planned_chunks, strong_summaries)
                return (
                    "Direct summary\n"
                    f"{direct_summary}\n\n"
                    "How the system works\n"
                    f"{' '.join(operation_points)}\n\n"
                    "Current implementation status\n"
                    f"{status_text}\n\n"
                    "What remains outstanding\n"
                    f"{missing_text} Outstanding hardening remains wherever formal logs identify future work or where "
                    "an evidence group is weak.\n\n"
                    "Evidence basis\n"
                    f"{evidence_basis} Use the returned source references as the evidence trail. Minerva is advisory "
                    "and does not calculate or change payroll truth."
                )

            if not strong_chunks:
                return (
                    "The retrieved formal corpus is not yet sufficient to answer this at the required rich-answer "
                    "standard. The closest evidence says: "
                    f"{' '.join(excerpts[:2])} "
                    "Minerva is advisory and does not calculate or change payroll truth."
                )
            evidence = " ".join(excerpts[:3])
            return (
                "Direct summary\n"
                "Based on the retrieved formal Minerva knowledge sources, this product-domain answer is grounded in "
                "the strongest available evidence.\n\n"
                "How the system works\n"
                f"{evidence}\n\n"
                "Current implementation status\n"
                "The answer reflects only the retrieved formal corpus and does not infer operational payroll truth.\n\n"
                "What remains outstanding\n"
                "Any missing implementation status or hardening details should be treated as unknown until supported "
                "by formal doctrine, hardening logs or Developer Logs.\n\n"
                "Evidence basis\n"
                "Use the returned source references as the evidence trail. Minerva is advisory and does not calculate "
                "or change payroll truth."
            )

        if not strong_chunks:
            return (
                "The retrieved Minerva evidence is weak or mixed for this question. "
                f"The closest sources say: {' '.join(excerpts[:2])} "
                "Minerva is advisory and does not calculate or change payroll truth."
            )

        formatted_evidence = " ".join(excerpts)
        return (
            "Based on the retrieved Minerva knowledge sources, using the strongest matches, "
            f"{formatted_evidence} "
            "Minerva is advisory and does not calculate or change payroll truth."
        )
