from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any

from app.services.internal_chat_api_stub_service import NO_ACTION_ATTESTATION, NO_ACTION_ATTESTATION_TEXT
from app.services.internal_chat_orchestrator_service import InternalChatSourceScope


class InternalChatFixtureKey(StrEnum):
    ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED = "ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED"
    POST_FINALISATION_OBJECTTIME_ACTION_SURFACED = "POST_FINALISATION_OBJECTTIME_ACTION_SURFACED"
    POST_FINALISATION_TREATMENT_WORKSPACE_REVIEW_ONLY = (
        "POST_FINALISATION_TREATMENT_WORKSPACE_REVIEW_ONLY"
    )
    ASPHALT_SAFE_CLASSRATES_SEEDED_WITH_GATES = "ASPHALT_SAFE_CLASSRATES_SEEDED_WITH_GATES"
    ASPHALT_CONDITIONAL_SHIFTWORK_REMAINS_GATED = "ASPHALT_CONDITIONAL_SHIFTWORK_REMAINS_GATED"
    CODE_EVIDENCE_CANNOT_PROVE_RUNTIME = "CODE_EVIDENCE_CANNOT_PROVE_RUNTIME"
    ANALYTICS_EVIDENCE_DEFERRED = "ANALYTICS_EVIDENCE_DEFERRED"
    RUNTIME_OBJECT_EVIDENCE_REQUIRED = "RUNTIME_OBJECT_EVIDENCE_REQUIRED"


class FixtureEvidenceStatus(StrEnum):
    SUPPORTED = "SUPPORTED"
    PARTIALLY_SUPPORTED = "PARTIALLY_SUPPORTED"
    NEEDS_RUNTIME_EVIDENCE = "NEEDS_RUNTIME_EVIDENCE"
    DEFERRED_INACTIVE = "DEFERRED_INACTIVE"


@dataclass(frozen=True)
class InternalChatEvidenceFixture:
    key: InternalChatFixtureKey
    title: str
    summary: str
    sample_questions: list[str]
    domain_tags: list[str]
    expected_source_scopes: list[InternalChatSourceScope]
    expected_support_status: FixtureEvidenceStatus
    expected_role_safe_caveats: list[str]
    prohibited_claims: list[str]
    candidate_evidence_metadata: list[dict[str, Any]]
    no_action_attestation: dict[str, bool] = field(default_factory=lambda: dict(NO_ACTION_ATTESTATION))
    no_action_attestation_text: str = NO_ACTION_ATTESTATION_TEXT

    def model_dump(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["key"] = self.key.value
        payload["expected_source_scopes"] = [scope.value for scope in self.expected_source_scopes]
        payload["expected_support_status"] = self.expected_support_status.value
        payload["candidate_evidence_count"] = len(self.candidate_evidence_metadata)
        return payload

    def candidate_evidence(self) -> list[dict[str, Any]]:
        return [dict(item) for item in self.candidate_evidence_metadata]


class InternalChatEvidenceFixtureHarnessService:
    def __init__(self) -> None:
        self._fixtures = _build_fixtures()

    def list_available_fixture_keys(self) -> list[InternalChatFixtureKey]:
        return list(self._fixtures)

    def list_available_fixture_key_values(self) -> list[str]:
        return [key.value for key in self.list_available_fixture_keys()]

    def get_fixture(self, key: InternalChatFixtureKey | str) -> InternalChatEvidenceFixture:
        normalized_key = _normalize_fixture_key(key)
        try:
            return self._fixtures[normalized_key]
        except KeyError:
            raise KeyError(f"Unsupported internal chat fixture key: {key!r}") from None

    def candidate_evidence_for_fixture(self, key: InternalChatFixtureKey | str) -> list[dict[str, Any]]:
        return self.get_fixture(key).candidate_evidence()

    def fixture_pack(self) -> dict[str, Any]:
        return {
            "FixtureHarnessVersion": "MINERVA_INTERNAL_CHAT_EVIDENCE_FIXTURE_HARNESS_V0_1",
            "FixtureOnly": True,
            "LiveLlmCalled": False,
            "DatabaseAccessed": False,
            "RuntimeEvidenceFetched": False,
            "WriteActionPerformed": False,
            "Fixtures": [fixture.model_dump() for fixture in self._fixtures.values()],
        }


def _normalize_fixture_key(key: InternalChatFixtureKey | str) -> InternalChatFixtureKey:
    if isinstance(key, InternalChatFixtureKey):
        return key
    try:
        return InternalChatFixtureKey(str(key).upper())
    except ValueError:
        raise KeyError(f"Unsupported internal chat fixture key: {key!r}") from None


def _build_fixtures() -> dict[InternalChatFixtureKey, InternalChatEvidenceFixture]:
    fixtures = [
        _manual_admitted_draft_processing_fixture(),
        _post_finalisation_objecttime_fixture(),
        _post_finalisation_treatment_workspace_fixture(),
        _asphalt_safe_classrates_fixture(),
        _asphalt_conditional_shiftwork_fixture(),
        _code_evidence_cannot_prove_runtime_fixture(),
        _analytics_deferred_fixture(),
        _runtime_object_evidence_required_fixture(),
    ]
    return {fixture.key: fixture for fixture in fixtures}


def _manual_admitted_draft_processing_fixture() -> InternalChatEvidenceFixture:
    tags = ["manual", "admitted", "draft", "processing", "payrun", "action"]
    return InternalChatEvidenceFixture(
        key=InternalChatFixtureKey.ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED,
        title="Admitted draft manual processing implemented",
        summary=(
            "Safe fixture evidence for the guarded manual admitted draft processing path. "
            "It confirms implementation support, not automation or finalisation."
        ),
        sample_questions=[
            "Can the platform manually process an admitted draft action?",
            "What evidence supports manual admitted draft action processing?",
            "What does code evidence confirm, and what does it not confirm?",
        ],
        domain_tags=tags,
        expected_source_scopes=_standard_static_scopes(),
        expected_support_status=FixtureEvidenceStatus.SUPPORTED,
        expected_role_safe_caveats=[
            "Requires an active PayRunActionDecision and authorised admission.",
            "Requires an existing PayRunContact.",
            "This is not automation, process-all, finalisation, payment, banking, or payroll calculation.",
            "Code evidence cannot prove production or customer availability.",
        ],
        prohibited_claims=_standard_prohibited_claims()
        + [
            "The platform automatically processes all admitted draft actions.",
            "The fixture proves finalisation, payment, or banking occurred.",
        ],
        candidate_evidence_metadata=[
            _evidence(
                "IMPLEMENTATION_STATE_DOC",
                "IMPLEMENTATION_STATE",
                "manual admitted draft processing implementation state",
                tags,
                summary=(
                    "Guarded manual processing is represented as implemented with active "
                    "PayRunActionDecision, authorised admission, and existing PayRunContact requirements."
                ),
                file_path="docs/evaluation/admitted_draft_payrun_bridge_manual_processing_action_v0_1/BASELINE.md",
                source_scope=InternalChatSourceScope.IMPLEMENTATION_STATE,
            ),
            _evidence(
                "ROUTE_DEFINITION",
                "CODE",
                "guarded manual admitted draft processing endpoint",
                tags + ["endpoint", "POST"],
                summary=(
                    "Endpoint POST /api/v1/pay-runs/{id}/pay-process/admitted-draft-actions/process "
                    "is represented as the guarded manual processing surface."
                ),
                repo_name="workforce-platform",
                repo_family="WORKFORCE_PLATFORM",
                file_path="app/api/v1/pay_runs.py",
                route_path="/api/v1/pay-runs/{id}/pay-process/admitted-draft-actions/process",
                source_scope=InternalChatSourceScope.CODE_EVIDENCE,
            ),
            _evidence(
                "SERVICE_CLASS",
                "CODE",
                "AdmittedDraftPayRunProcessingBridgeService",
                tags + ["bridge", "entrypoint", "target_contact_id"],
                summary=(
                    "Processing delegates through AdmittedDraftPayRunProcessingBridgeService; "
                    "PayRunProcessingService.process with target_contact_id remains the processing entrypoint."
                ),
                repo_name="workforce-platform",
                repo_family="WORKFORCE_PLATFORM",
                file_path="app/services/admitted_draft_payrun_processing_bridge_service.py",
                symbol_name="AdmittedDraftPayRunProcessingBridgeService",
                source_scope=InternalChatSourceScope.CODE_EVIDENCE,
            ),
            _evidence(
                "TYPESCRIPT_FILE",
                "CODE",
                "PayRun Detail and Admin Queue manual action wiring",
                tags + ["admin_queue", "payrun_detail", "ui_wiring"],
                summary=(
                    "PayRun Detail and Admin Queue action wiring is represented for manual admitted "
                    "draft action processing."
                ),
                repo_name="workforce-platform",
                repo_family="WORKFORCE_PLATFORM",
                file_path="frontend/src/pay-runs/admittedDraftActions.tsx",
                source_scope=InternalChatSourceScope.CODE_EVIDENCE,
            ),
            _evidence(
                "TEST_FILE",
                "TEST",
                "manual admitted draft processing guardrail tests",
                tags + ["guardrails", "behavioural_evidence"],
                summary=(
                    "Tests cover active decision, authorised admission, existing contact, bridge delegation, "
                    "and not process-all behaviour."
                ),
                repo_name="ezeas-intelligence",
                repo_family="MINERVA",
                file_path="tests/test_admitted_draft_payrun_processing_bridge_source_response.py",
                test_name="test_manual_admitted_draft_processing_bridge_evidence",
                source_scope=InternalChatSourceScope.TEST_EVIDENCE,
            ),
        ],
    )


def _post_finalisation_objecttime_fixture() -> InternalChatEvidenceFixture:
    tags = ["post", "finalisation", "objecttime", "source", "truth", "action", "review"]
    return InternalChatEvidenceFixture(
        key=InternalChatFixtureKey.POST_FINALISATION_OBJECTTIME_ACTION_SURFACED,
        title="Post-finalisation ObjectTime action surfaced",
        summary=(
            "Safe fixture evidence that ObjectTime/source-truth changes after finalisation are surfaced "
            "for review without mutating finalised PayRuns."
        ),
        sample_questions=[
            "What evidence supports the post-finalisation ObjectTime action?",
            "What should I do with this post-finalisation ObjectTime action?",
        ],
        domain_tags=tags,
        expected_source_scopes=_standard_static_scopes(),
        expected_support_status=FixtureEvidenceStatus.SUPPORTED,
        expected_role_safe_caveats=[
            "Finalised PayRuns remain protected.",
            "The action is worker-period scoped.",
            "Treatment review is required before any later execution path.",
            "No finalised mutation occurs from this evidence fixture.",
        ],
        prohibited_claims=_standard_prohibited_claims()
        + ["The fixture proves a finalised PayRun was changed."],
        candidate_evidence_metadata=[
            _evidence(
                "IMPLEMENTATION_STATE_DOC",
                "IMPLEMENTATION_STATE",
                "post-finalisation ObjectTime action implementation state",
                tags,
                summary=(
                    "ObjectTime/source truth changed after finalisation is represented as surfaced in "
                    "Admin Queue while finalised PayRun protection remains in force."
                ),
                file_path="docs/evaluation/post_finalisation_objecttime_action_v0_1/BASELINE.md",
                source_scope=InternalChatSourceScope.IMPLEMENTATION_STATE,
            ),
            _evidence(
                "SERVICE_CLASS",
                "CODE",
                "post-finalisation ObjectTime action surfacing service",
                tags + ["worker_period_scoped", "admin_queue"],
                summary=(
                    "The action is worker-period scoped and routed to treatment review; no finalised "
                    "mutation is represented."
                ),
                repo_name="workforce-platform",
                repo_family="WORKFORCE_PLATFORM",
                file_path="app/services/post_finalisation_objecttime_action_service.py",
                symbol_name="PostFinalisationObjectTimeActionService",
                source_scope=InternalChatSourceScope.CODE_EVIDENCE,
            ),
            _evidence(
                "TEST_FILE",
                "TEST",
                "post-finalisation ObjectTime action guardrail tests",
                tags + ["finalised_protected", "treatment_review_required"],
                summary=(
                    "Tests represent finalised PayRun protection, worker-period scoping, treatment "
                    "review requirement, and no finalised mutation."
                ),
                repo_name="ezeas-intelligence",
                repo_family="MINERVA",
                file_path="tests/test_post_finalisation_objecttime_action_surface.py",
                test_name="test_post_finalisation_objecttime_action_keeps_finalised_payrun_protected",
                source_scope=InternalChatSourceScope.TEST_EVIDENCE,
            ),
        ],
    )


def _post_finalisation_treatment_workspace_fixture() -> InternalChatEvidenceFixture:
    tags = ["post", "finalisation", "treatment", "workspace", "review", "objecttime"]
    return InternalChatEvidenceFixture(
        key=InternalChatFixtureKey.POST_FINALISATION_TREATMENT_WORKSPACE_REVIEW_ONLY,
        title="Post-finalisation treatment workspace review only",
        summary=(
            "Safe fixture evidence that treatment review surfaces are in place while treatment execution, "
            "supplementary, retro, payment, and finalisation execution remain out of scope."
        ),
        sample_questions=[
            "What is available in the treatment workspace after finalisation?",
            "Can ObjectTime be reviewed through the existing source-truth path?",
        ],
        domain_tags=tags,
        expected_source_scopes=_standard_static_scopes(),
        expected_support_status=FixtureEvidenceStatus.PARTIALLY_SUPPORTED,
        expected_role_safe_caveats=[
            "Review treatment is in place.",
            "ObjectTime can be reviewed or edited through the existing source-truth path where allowed.",
            "Worker Story and finalisation details are review surfaces.",
            "Treatment execution remains not implemented.",
            "No supplementary, retro, payment, or finalisation execution is performed.",
        ],
        prohibited_claims=_standard_prohibited_claims()
        + ["The fixture proves treatment execution or supplementary payroll execution."],
        candidate_evidence_metadata=[
            _evidence(
                "IMPLEMENTATION_STATE_DOC",
                "IMPLEMENTATION_STATE",
                "post-finalisation treatment review implementation state",
                tags,
                summary=(
                    "Review treatment is represented as in place; execution remains deferred and no "
                    "payment or finalisation execution is represented."
                ),
                file_path="docs/evaluation/post_finalisation_treatment_workspace_v0_1/BASELINE.md",
                source_scope=InternalChatSourceScope.IMPLEMENTATION_STATE,
            ),
            _evidence(
                "TYPESCRIPT_FILE",
                "CODE",
                "Worker Story and finalisation detail review surfaces",
                tags + ["worker_story", "finalisation_details", "source_truth_path"],
                summary=(
                    "Worker Story and finalisation details are represented as review surfaces for "
                    "ObjectTime/source-truth review where allowed."
                ),
                repo_name="workforce-platform",
                repo_family="WORKFORCE_PLATFORM",
                file_path="frontend/src/pay-runs/postFinalisationTreatmentWorkspace.tsx",
                source_scope=InternalChatSourceScope.CODE_EVIDENCE,
            ),
            _evidence(
                "TEST_FILE",
                "TEST",
                "post-finalisation treatment review-only tests",
                tags + ["review_only", "execution_deferred"],
                summary=(
                    "Tests represent review-only behaviour and absence of treatment execution, "
                    "supplementary, retro, payment, or finalisation execution."
                ),
                repo_name="ezeas-intelligence",
                repo_family="MINERVA",
                file_path="tests/test_post_finalisation_treatment_workspace_review_only.py",
                test_name="test_treatment_workspace_is_review_only",
                source_scope=InternalChatSourceScope.TEST_EVIDENCE,
            ),
        ],
    )


def _asphalt_safe_classrates_fixture() -> InternalChatEvidenceFixture:
    tags = ["asphalt", "safe", "classrates", "ratesource", "DAY1", "OT1", "OT2", "SAT1", "SUN1", "PHOL1"]
    return InternalChatEvidenceFixture(
        key=InternalChatFixtureKey.ASPHALT_SAFE_CLASSRATES_SEEDED_WITH_GATES,
        title="Asphalt safe classRates seeded with gates",
        summary=(
            "Safe fixture evidence that six Asphalt safe classRates are aligned from parsed universe "
            "to materialised RateSource evidence, while remaining columns stay confirmation-gated."
        ),
        sample_questions=[
            "Is the Asphalt safe classRates seeding aligned now?",
            "Which safe Asphalt RateSource columns are materialised?",
        ],
        domain_tags=tags,
        expected_source_scopes=_standard_static_scopes(),
        expected_support_status=FixtureEvidenceStatus.SUPPORTED,
        expected_role_safe_caveats=[
            "DAY1, OT1, OT2, SAT1, SUN1, and PHOL1 are aligned from parsed universe to materialised RateSource evidence.",
            "Step 06 wrote 30 safe classRates rows.",
            "Diagnostic status is SAFE_CLASSRATES_SEEDED_WITH_REMAINING_GATES.",
            "Remaining confirmation-gated RateSource columns remain blocked.",
        ],
        prohibited_claims=_standard_prohibited_claims()
        + ["All Asphalt RateSource columns are confirmed."],
        candidate_evidence_metadata=[
            _evidence(
                "IMPLEMENTATION_STATE_DOC",
                "IMPLEMENTATION_STATE",
                "Asphalt safe classRates implementation state",
                tags + ["SAFE_CLASSRATES_SEEDED_WITH_REMAINING_GATES", "30"],
                summary=(
                    "DAY1, OT1, OT2, SAT1, SUN1, and PHOL1 are represented as aligned; Step 06 wrote "
                    "30 safe classRates rows and returned SAFE_CLASSRATES_SEEDED_WITH_REMAINING_GATES."
                ),
                file_path="docs/evaluation/asphalt_safe_classrates_v0_1/BASELINE.md",
                source_scope=InternalChatSourceScope.IMPLEMENTATION_STATE,
            ),
            _evidence(
                "SERVICE_CLASS",
                "CODE",
                "Asphalt safe classRates seeding step",
                tags + ["step_06", "materialised", "confirmation_gates"],
                summary=(
                    "Safe classRates are materialised from parsed universe to RateSource evidence; "
                    "remaining confirmation-gated columns stay blocked."
                ),
                repo_name="award-configurator-v1",
                repo_family="AWARD_CONFIGURATOR",
                file_path="steps/step_06_seed_asphalt_safe_classrates.py",
                symbol_name="AsphaltSafeClassRatesSeeder",
                source_scope=InternalChatSourceScope.CODE_EVIDENCE,
            ),
            _evidence(
                "TEST_FILE",
                "TEST",
                "Asphalt safe classRates seeding tests",
                tags + ["DAY1", "OT1", "OT2", "SAT1", "SUN1", "PHOL1", "remaining_gates"],
                summary=(
                    "Tests represent the six safe rate codes, 30 seeded rows, and blocked remaining "
                    "confirmation-gated RateSource columns."
                ),
                repo_name="ezeas-intelligence",
                repo_family="MINERVA",
                file_path="tests/test_asphalt_safe_classrates_seeding.py",
                test_name="test_safe_classrates_seeded_with_remaining_gates",
                source_scope=InternalChatSourceScope.TEST_EVIDENCE,
            ),
        ],
    )


def _asphalt_conditional_shiftwork_fixture() -> InternalChatEvidenceFixture:
    tags = ["asphalt", "conditional", "shiftwork", "AFT1", "AFT2", "NGT1", "NGT2", "gated"]
    return InternalChatEvidenceFixture(
        key=InternalChatFixtureKey.ASPHALT_CONDITIONAL_SHIFTWORK_REMAINS_GATED,
        title="Asphalt conditional shiftwork remains gated",
        summary=(
            "Safe fixture evidence that placeholder and propagation support exists, while the dynamic "
            "conditional shift treatment engine remains future/deferred."
        ),
        sample_questions=[
            "What is still deferred for conditional shiftwork?",
            "Are AFT1, AFT2, NGT1, and NGT2 ready for dynamic shift treatment?",
        ],
        domain_tags=tags,
        expected_source_scopes=_standard_static_scopes(),
        expected_support_status=FixtureEvidenceStatus.PARTIALLY_SUPPORTED,
        expected_role_safe_caveats=[
            "AFT1, AFT2, NGT1, and NGT2 exist as placeholders.",
            "RateSource.IsShiftWorker exists and propagation has been hardened.",
            "ObjectTime source ShiftType is exposed in canonical input.",
            "Dynamic shift treatment engine remains future/deferred.",
            "Non-rotating night shift, unrelieved shiftworker overtime, and break/change-to-shift continuation remain gated.",
        ],
        prohibited_claims=_standard_prohibited_claims()
        + ["The fixture proves dynamic conditional shiftwork treatment is implemented."],
        candidate_evidence_metadata=[
            _evidence(
                "IMPLEMENTATION_STATE_DOC",
                "IMPLEMENTATION_STATE",
                "Asphalt conditional shiftwork gated implementation state",
                tags + ["deferred", "future"],
                summary=(
                    "AFT1, AFT2, NGT1, and NGT2 placeholders exist; RateSource.IsShiftWorker and "
                    "ObjectTime ShiftType propagation are represented, while dynamic treatment is deferred."
                ),
                file_path="docs/evaluation/asphalt_conditional_shiftwork_v0_1/BASELINE.md",
                source_scope=InternalChatSourceScope.IMPLEMENTATION_STATE,
            ),
            _evidence(
                "SERVICE_CLASS",
                "CODE",
                "shiftwork propagation and canonical input evidence",
                tags + ["RateSource.IsShiftWorker", "ShiftType", "canonical_input"],
                summary=(
                    "RateSource.IsShiftWorker propagation is hardened and ObjectTime source ShiftType "
                    "is exposed in canonical input."
                ),
                repo_name="award-configurator-v1",
                repo_family="AWARD_CONFIGURATOR",
                file_path="src/asphalt/shiftwork_rate_source_projection.py",
                symbol_name="ShiftworkRateSourceProjection",
                source_scope=InternalChatSourceScope.CODE_EVIDENCE,
            ),
            _evidence(
                "TEST_FILE",
                "TEST",
                "conditional shiftwork remains gated tests",
                tags + ["dynamic_engine_deferred", "night_shift_gated", "overtime_gated"],
                summary=(
                    "Tests represent deferred dynamic shift treatment and remaining gates for "
                    "non-rotating night shift, unrelieved shiftworker overtime, and break/change-to-shift continuation."
                ),
                repo_name="ezeas-intelligence",
                repo_family="MINERVA",
                file_path="tests/test_asphalt_conditional_shiftwork_gates.py",
                test_name="test_conditional_shiftwork_dynamic_treatment_remains_gated",
                source_scope=InternalChatSourceScope.TEST_EVIDENCE,
            ),
        ],
    )


def _code_evidence_cannot_prove_runtime_fixture() -> InternalChatEvidenceFixture:
    tags = ["code", "evidence", "runtime", "production", "customer", "availability", "caveat"]
    return InternalChatEvidenceFixture(
        key=InternalChatFixtureKey.CODE_EVIDENCE_CANNOT_PROVE_RUNTIME,
        title="Code evidence cannot prove runtime",
        summary=(
            "Safe fixture evidence for the evidence hierarchy: code can support implementation "
            "confidence but cannot prove deployment, customer availability, runtime object state, or payroll correctness."
        ),
        sample_questions=[
            "Why can code evidence not prove production/customer runtime availability?",
            "What does code evidence confirm, and what does it not confirm?",
        ],
        domain_tags=tags,
        expected_source_scopes=_standard_static_scopes(),
        expected_support_status=FixtureEvidenceStatus.NEEDS_RUNTIME_EVIDENCE,
        expected_role_safe_caveats=[
            "Code evidence confirms implementation support.",
            "Code cannot prove production deployment.",
            "Code cannot prove customer availability.",
            "Code cannot prove migration applied, runtime object state, or payroll correctness.",
        ],
        prohibited_claims=_standard_prohibited_claims(),
        candidate_evidence_metadata=[
            _evidence(
                "IMPLEMENTATION_STATE_DOC",
                "IMPLEMENTATION_STATE",
                "code evidence hierarchy implementation state",
                tags,
                summary=(
                    "Implementation support can be confirmed from curated static evidence, while "
                    "runtime, production, tenant, customer, migration, and payroll correctness require separate evidence."
                ),
                file_path="docs/evaluation/minerva_code_evidence_answer_support_v0_1/ANSWER_SUPPORT_BASELINE.md",
                source_scope=InternalChatSourceScope.IMPLEMENTATION_STATE,
            ),
            _evidence(
                "SERVICE_CLASS",
                "CODE",
                "code evidence answer support caveat service",
                tags + ["prohibited_claims", "needs_runtime_evidence"],
                summary=(
                    "Answer support requires runtime caveats and blocks claims that code proves "
                    "production availability, customer availability, migration applied, live object state, or payroll correctness."
                ),
                repo_name="ezeas-intelligence",
                repo_family="MINERVA",
                file_path="app/services/code_evidence_answer_support_service.py",
                symbol_name="CodeEvidenceAnswerSupportService",
                source_scope=InternalChatSourceScope.CODE_EVIDENCE,
            ),
            _evidence(
                "TEST_FILE",
                "TEST",
                "code evidence runtime caveat tests",
                tags + ["runtime_availability", "customer_availability", "prohibited_claims"],
                summary=(
                    "Tests represent runtime caveat requirements and prohibited claims for production, "
                    "customer, migration, runtime object, and payroll correctness assertions."
                ),
                repo_name="ezeas-intelligence",
                repo_family="MINERVA",
                file_path="tests/test_code_evidence_answer_support_service.py",
                test_name="test_code_evidence_cannot_prove_runtime_availability",
                source_scope=InternalChatSourceScope.TEST_EVIDENCE,
            ),
        ],
    )


def _analytics_deferred_fixture() -> InternalChatEvidenceFixture:
    tags = ["analytics", "trend", "chart", "deferred", "inactive", "future"]
    return InternalChatEvidenceFixture(
        key=InternalChatFixtureKey.ANALYTICS_EVIDENCE_DEFERRED,
        title="Analytics evidence deferred",
        summary=(
            "Safe fixture evidence that analytics is registered as future/optional evidence but full "
            "analytics intake and interpretation are deferred/inactive in v0.1."
        ),
        sample_questions=[
            "Can Minerva interpret this trend chart?",
            "Is analytics evidence active in v0.1?",
        ],
        domain_tags=tags,
        expected_source_scopes=[InternalChatSourceScope.ANALYTICS_EVIDENCE],
        expected_support_status=FixtureEvidenceStatus.DEFERRED_INACTIVE,
        expected_role_safe_caveats=[
            "Analytics is registered as a future/optional evidence target.",
            "Full analytics evidence intake is deferred/inactive in v0.1.",
            "No chart interpretation should be claimed from this fixture alone.",
        ],
        prohibited_claims=_standard_prohibited_claims()
        + ["The fixture proves a payroll trend chart interpretation."],
        candidate_evidence_metadata=[
            _evidence(
                "KNOWLEDGE_DOC",
                "KNOWLEDGE",
                "analytics evidence deferred knowledge note",
                tags,
                summary=(
                    "Analytics is registered as a future optional evidence target; full analytics "
                    "evidence intake is deferred and inactive in v0.1."
                ),
                file_path="docs/knowledge/minerva_code_evidence_role_model_v0_1.md",
                source_scope=InternalChatSourceScope.PLATFORM_KNOWLEDGE,
            ),
            _evidence(
                "EVALUATION_DOC",
                "EVALUATION",
                "analytics evidence deferred baseline",
                tags,
                summary="Analytics interpretation remains deferred unless a later safe analytics metadata slice supplies evidence.",
                file_path="docs/evaluation/minerva_internal_chat_api_stub_v0_1/API_STUB_BASELINE.md",
                source_scope=InternalChatSourceScope.EVALUATION_BASELINES,
            ),
        ],
    )


def _runtime_object_evidence_required_fixture() -> InternalChatEvidenceFixture:
    tags = ["runtime", "object", "evidence", "tenant", "customer", "availability", "needs_evidence"]
    return InternalChatEvidenceFixture(
        key=InternalChatFixtureKey.RUNTIME_OBJECT_EVIDENCE_REQUIRED,
        title="Runtime object evidence required",
        summary=(
            "Safe fixture evidence that object-specific, tenant, customer, live, or production questions "
            "require authorised runtime object evidence before Minerva may answer."
        ),
        sample_questions=[
            "Is this feature enabled for my tenant?",
            "Why did this worker get overtime?",
            "Was this object available in production?",
        ],
        domain_tags=tags,
        expected_source_scopes=[InternalChatSourceScope.RUNTIME_OBJECT_EVIDENCE],
        expected_support_status=FixtureEvidenceStatus.NEEDS_RUNTIME_EVIDENCE,
        expected_role_safe_caveats=[
            "Object-specific questions require runtime object evidence.",
            "Without runtime object evidence, Minerva must say needs evidence.",
            "Fixture evidence is synthetic and does not prove tenant, customer, live, or production state.",
        ],
        prohibited_claims=_standard_prohibited_claims()
        + ["The fixture proves this tenant has the feature enabled."],
        candidate_evidence_metadata=[
            _evidence(
                "IMPLEMENTATION_STATE_DOC",
                "IMPLEMENTATION_STATE",
                "runtime object evidence required implementation state",
                tags,
                summary=(
                    "Static implementation evidence is not sufficient for object-specific, tenant, "
                    "customer, live, or production availability questions."
                ),
                file_path="docs/evaluation/minerva_internal_chat_orchestrator_envelope_v0_1/CHAT_ORCHESTRATOR_BASELINE.md",
                source_scope=InternalChatSourceScope.IMPLEMENTATION_STATE,
            ),
            _evidence(
                "SERVICE_CLASS",
                "CODE",
                "runtime evidence unsupported scope guard",
                tags + ["unsupported_scope", "needs_more_evidence"],
                summary=(
                    "The internal chat orchestrator recognises runtime object evidence but does not "
                    "fetch it in v0.1; safe metadata must be supplied by a later slice."
                ),
                repo_name="ezeas-intelligence",
                repo_family="MINERVA",
                file_path="app/services/internal_chat_orchestrator_service.py",
                symbol_name="InternalChatOrchestratorService",
                source_scope=InternalChatSourceScope.CODE_EVIDENCE,
            ),
            _evidence(
                "TEST_FILE",
                "TEST",
                "runtime object evidence required tests",
                tags + ["runtime_scope", "needs_more_evidence"],
                summary=(
                    "Tests represent that runtime object scope without supplied runtime metadata requires "
                    "more evidence or remains unsupported."
                ),
                repo_name="ezeas-intelligence",
                repo_family="MINERVA",
                file_path="tests/test_internal_chat_orchestrator_service.py",
                test_name="test_runtime_scope_without_supplied_runtime_metadata_needs_more_evidence",
                source_scope=InternalChatSourceScope.TEST_EVIDENCE,
            ),
        ],
    )


def _standard_static_scopes() -> list[InternalChatSourceScope]:
    return [
        InternalChatSourceScope.PLATFORM_KNOWLEDGE,
        InternalChatSourceScope.IMPLEMENTATION_STATE,
        InternalChatSourceScope.CODE_EVIDENCE,
        InternalChatSourceScope.TEST_EVIDENCE,
        InternalChatSourceScope.PROMPT_ARTEFACTS,
        InternalChatSourceScope.EVALUATION_BASELINES,
    ]


def _standard_prohibited_claims() -> list[str]:
    return [
        "Code evidence proves production availability.",
        "Code evidence proves customer availability.",
        "Code evidence proves runtime enablement.",
        "Code evidence proves a database migration has been applied.",
        "Code evidence proves live object state.",
        "Code evidence proves payroll correctness.",
        "Fixture evidence proves production/customer availability.",
        "Minerva calculated payroll.",
        "Minerva performed a write action.",
        "A final customer-facing answer was generated.",
    ]


def _evidence(
    source_type: str,
    evidence_category: str,
    title: str,
    tags: list[str],
    *,
    summary: str,
    source_scope: InternalChatSourceScope,
    repo_name: str | None = None,
    repo_family: str | None = None,
    file_path: str | None = None,
    symbol_name: str | None = None,
    route_path: str | None = None,
    test_name: str | None = None,
) -> dict[str, Any]:
    return {
        "source_type": source_type,
        "evidence_category": evidence_category,
        "source_scope": source_scope.value,
        "title": title,
        "repo_name": repo_name,
        "repo_family": repo_family,
        "file_path": file_path,
        "symbol_name": symbol_name,
        "route_path": route_path,
        "test_name": test_name,
        "evidence_tags": list(tags) + ["fixture_only", "metadata_only", "no_raw_code"],
        "summary": summary,
        "fixture_only": True,
        "live_runtime_state": False,
        "database_accessed": False,
        "live_llm_called": False,
        "write_action_performed": False,
    }
