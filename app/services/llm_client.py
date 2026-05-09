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
