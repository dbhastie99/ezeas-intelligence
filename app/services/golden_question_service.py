import json
import re
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from app.core.enums import ChatRole, normalize_chat_role, normalize_source_type
from app.models.chat import KnowledgeChatMessage, KnowledgeChatSession
from app.schemas.common import SourceReference
from app.services.answer_mode_service import classify_answer_mode, normalize_answer_mode
from app.services.answer_generation_service import generate_grounded_answer
from app.services.audit_service import write_ai_interaction_audit
from app.services.domain_retrieval_plan_service import retrieve_chunks_for_question


class GoldenQuestionError(ValueError):
    pass


def load_golden_manifest(path: str | Path) -> dict[str, Any]:
    manifest_path = Path(path)
    if not manifest_path.exists() or not manifest_path.is_file():
        raise GoldenQuestionError(f"Golden question manifest not found: {manifest_path}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise GoldenQuestionError(f"Golden question manifest is not valid JSON: {exc}") from exc
    if not isinstance(manifest, dict):
        raise GoldenQuestionError("Golden question manifest root must be an object.")
    questions = manifest.get("questions")
    if not isinstance(questions, list):
        raise GoldenQuestionError("Golden question manifest field 'questions' must be a list.")
    for index, question in enumerate(questions):
        if not isinstance(question, dict):
            raise GoldenQuestionError(f"Golden question entry {index} must be an object.")
        if not question.get("id") or not isinstance(question.get("id"), str):
            raise GoldenQuestionError(f"Golden question entry {index} must include a string id.")
        if not question.get("question") or not isinstance(question.get("question"), str):
            raise GoldenQuestionError(f"Golden question entry {index} must include a string question.")
        try:
            for source_type in question.get("expected_source_types", []):
                normalize_source_type(source_type)
            for source_type in question.get("preferred_top_source_types", []):
                normalize_source_type(source_type)
            preferred = question.get("preferred_top_source_type")
            if preferred:
                normalize_source_type(preferred)
            answer_mode = question.get("answer_mode")
            if answer_mode:
                normalize_answer_mode(answer_mode)
        except ValueError as exc:
            raise GoldenQuestionError(f"Golden question entry {index}: {exc}") from exc
    return manifest


def _contains_any(text: str, phrases: list[str]) -> bool:
    lower_text = text.lower()
    return any(phrase.lower() in lower_text for phrase in phrases)


def _contains_all(text: str, phrases: list[str]) -> bool:
    lower_text = text.lower()
    return all(phrase.lower() in lower_text for phrase in phrases)


def _matches_any_pattern(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE) for pattern in patterns)


def _source_phrase_text(source: SourceReference) -> str:
    return " ".join(
        [
            source.snippet or "",
            " ".join(source.matched_phrases),
            source.match_reason or "",
            source.title or "",
        ]
    )


def _source_summary(source: SourceReference) -> dict[str, Any]:
    return {
        "document_id": source.document_id,
        "chunk_id": source.chunk_id,
        "title": source.title,
        "source_type": source.source_type,
        "score": source.score,
        "matched_tokens": source.matched_tokens,
        "matched_phrases": source.matched_phrases,
        "match_reason": source.match_reason,
        "snippet": source.snippet,
        "domain_plan_id": source.domain_plan_id,
        "evidence_group_id": source.evidence_group_id,
        "evidence_group_label": source.evidence_group_label,
    }


def _evaluate_question(question_spec: dict[str, Any], answer: str, sources: list[SourceReference]) -> dict[str, Any]:
    checks: dict[str, bool] = {}
    failure_reasons: list[str] = []

    expected_answer_mode = question_spec.get("answer_mode")
    if expected_answer_mode:
        actual_answer_mode = classify_answer_mode(question_spec["question"])
        checks["answer_mode"] = actual_answer_mode == expected_answer_mode
        if not checks["answer_mode"]:
            failure_reasons.append(f"Expected answer mode {expected_answer_mode}, got {actual_answer_mode}")
    else:
        checks["answer_mode"] = True

    expected_source_types = question_spec.get("expected_source_types", [])
    if expected_source_types:
        checks["expected_source_type_present"] = any(source.source_type in expected_source_types for source in sources)
        if not checks["expected_source_type_present"]:
            failure_reasons.append(f"No source matched expected source types: {expected_source_types}")
    else:
        checks["expected_source_type_present"] = True

    preferred_top_source_types = question_spec.get("preferred_top_source_types")
    if preferred_top_source_types:
        checks["preferred_top_source_type"] = bool(sources and sources[0].source_type in preferred_top_source_types)
        if not checks["preferred_top_source_type"]:
            actual = sources[0].source_type if sources else None
            failure_reasons.append(
                f"Preferred top source types {preferred_top_source_types} did not include top source type; got {actual}"
            )
    else:
        preferred_top_source_type = question_spec.get("preferred_top_source_type")
        if preferred_top_source_type:
            checks["preferred_top_source_type"] = bool(sources and sources[0].source_type == preferred_top_source_type)
            if not checks["preferred_top_source_type"]:
                actual = sources[0].source_type if sources else None
                failure_reasons.append(f"Preferred top source type {preferred_top_source_type} was not top; got {actual}")
        else:
            checks["preferred_top_source_type"] = True

    source_phrases = question_spec.get("expected_phrases_any", [])
    if source_phrases:
        source_text = " ".join(_source_phrase_text(source) for source in sources)
        checks["expected_source_phrase_any"] = _contains_any(source_text, source_phrases)
        if not checks["expected_source_phrase_any"]:
            failure_reasons.append(f"No source snippet/matched phrase contained any of: {source_phrases}")
    else:
        checks["expected_source_phrase_any"] = True

    source_terms_any = question_spec.get("expected_source_terms_any", [])
    if source_terms_any:
        source_text = " ".join(_source_phrase_text(source) for source in sources)
        checks["expected_source_terms_any"] = _contains_any(source_text, source_terms_any)
        if not checks["expected_source_terms_any"]:
            failure_reasons.append(f"No source snippet/matched phrase contained any expected terms: {source_terms_any}")
    else:
        checks["expected_source_terms_any"] = True

    source_terms_all = question_spec.get("expected_source_terms_all", [])
    if source_terms_all:
        source_text = " ".join(_source_phrase_text(source) for source in sources)
        checks["expected_source_terms_all"] = _contains_all(source_text, source_terms_all)
        if not checks["expected_source_terms_all"]:
            failure_reasons.append(f"Source snippets/matched phrases did not contain all expected terms: {source_terms_all}")
    else:
        checks["expected_source_terms_all"] = True

    top_source_phrases = question_spec.get("required_top_source_phrases_any", [])
    if top_source_phrases:
        top_source_text = _source_phrase_text(sources[0]) if sources else ""
        checks["required_top_source_phrase_any"] = _contains_any(top_source_text, top_source_phrases)
        if not checks["required_top_source_phrase_any"]:
            failure_reasons.append(f"Top source did not contain any required phrase: {top_source_phrases}")
    else:
        checks["required_top_source_phrase_any"] = True

    answer_phrases = question_spec.get("expected_answer_phrases_any", [])
    if answer_phrases:
        checks["expected_answer_phrase_any"] = _contains_any(answer, answer_phrases)
        if not checks["expected_answer_phrase_any"]:
            failure_reasons.append(f"Answer did not contain any of: {answer_phrases}")
    else:
        checks["expected_answer_phrase_any"] = True

    answer_phrases_all = question_spec.get("expected_answer_phrases_all", [])
    if answer_phrases_all:
        checks["expected_answer_phrases_all"] = _contains_all(answer, answer_phrases_all)
        if not checks["expected_answer_phrases_all"]:
            failure_reasons.append(f"Answer did not contain all required phrases: {answer_phrases_all}")
    else:
        checks["expected_answer_phrases_all"] = True

    answer_terms_any = question_spec.get("expected_answer_terms_any", [])
    if answer_terms_any:
        checks["expected_answer_terms_any"] = _contains_any(answer, answer_terms_any)
        if not checks["expected_answer_terms_any"]:
            failure_reasons.append(f"Answer did not contain any expected terms: {answer_terms_any}")
    else:
        checks["expected_answer_terms_any"] = True

    answer_terms_all = question_spec.get("expected_answer_terms_all", [])
    if answer_terms_all:
        checks["expected_answer_terms_all"] = _contains_all(answer, answer_terms_all)
        if not checks["expected_answer_terms_all"]:
            failure_reasons.append(f"Answer did not contain all expected terms: {answer_terms_all}")
    else:
        checks["expected_answer_terms_all"] = True

    forbidden_answer_phrases = question_spec.get("forbidden_answer_phrases_any", [])
    if forbidden_answer_phrases:
        checks["forbidden_answer_phrases_any"] = not _contains_any(answer, forbidden_answer_phrases)
        if not checks["forbidden_answer_phrases_any"]:
            failure_reasons.append(f"Answer contained a forbidden phrase from: {forbidden_answer_phrases}")
    else:
        checks["forbidden_answer_phrases_any"] = True

    required_sections = question_spec.get("required_answer_sections", [])
    if required_sections:
        checks["required_answer_sections"] = _contains_all(answer, required_sections)
        if not checks["required_answer_sections"]:
            failure_reasons.append(f"Answer did not contain all required sections: {required_sections}")
    else:
        checks["required_answer_sections"] = True

    forbidden_patterns = question_spec.get("forbidden_answer_patterns_any", [])
    if forbidden_patterns:
        checks["forbidden_answer_patterns_any"] = not _matches_any_pattern(answer, forbidden_patterns)
        if not checks["forbidden_answer_patterns_any"]:
            failure_reasons.append(f"Answer matched a forbidden pattern from: {forbidden_patterns}")
    else:
        checks["forbidden_answer_patterns_any"] = True

    passed = all(checks.values())
    return {"passed": passed, "checks": checks, "failure_reasons": failure_reasons}


def run_golden_questions(
    db: Session,
    manifest_path: str | Path,
    top_k: int = 5,
    create_audit: bool = False,
) -> dict[str, Any]:
    manifest = load_golden_manifest(manifest_path)
    results: list[dict[str, Any]] = []

    for question_spec in manifest["questions"]:
        question = question_spec["question"]
        retrieved_chunks = retrieve_chunks_for_question(db=db, query=question, top_k=top_k)
        answer, sources, model_name, prompt_policy = generate_grounded_answer(question, retrieved_chunks)
        audit_id = None

        if create_audit:
            session = KnowledgeChatSession(Title=f"golden:{question_spec['id']}")
            db.add(session)
            db.flush()
            db.add(
                KnowledgeChatMessage(
                    KnowledgeChatSessionId=session.KnowledgeChatSessionId,
                    Role=normalize_chat_role(ChatRole.USER.value),
                    Content=question,
                )
            )
            db.add(
                KnowledgeChatMessage(
                    KnowledgeChatSessionId=session.KnowledgeChatSessionId,
                    Role=normalize_chat_role(ChatRole.ASSISTANT.value),
                    Content=answer,
                )
            )
            db.flush()
            audit = write_ai_interaction_audit(
                db=db,
                user_question=question,
                response_text=answer,
                source_references=sources,
                model_name=model_name,
                prompt_policy=prompt_policy,
                chat_session_id=session.KnowledgeChatSessionId,
            )
            db.commit()
            audit_id = audit.AIInteractionAuditId

        evaluation = _evaluate_question(question_spec, answer, sources)
        results.append(
            {
                "id": question_spec["id"],
                "question": question,
                "passed": evaluation["passed"],
                "checks": evaluation["checks"],
                "failure_reasons": evaluation["failure_reasons"],
                "answer": answer,
                "top_sources": [_source_summary(source) for source in sources],
                "audit_id": audit_id,
            }
        )

    passed_count = sum(1 for result in results if result["passed"])
    return {
        "name": manifest.get("name"),
        "description": manifest.get("description"),
        "total": len(results),
        "passed": passed_count,
        "failed": len(results) - passed_count,
        "all_passed": passed_count == len(results),
        "create_audit": create_audit,
        "results": results,
    }
