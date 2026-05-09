from enum import StrEnum


class SourceType(StrEnum):
    PLATFORM_DOCTRINE = "PLATFORM_DOCTRINE"
    HARDENING_LOG = "HARDENING_LOG"
    DEVELOPER_LOG = "DEVELOPER_LOG"
    REQUIREMENTS = "REQUIREMENTS"
    CODE = "CODE"
    TEST = "TEST"
    SCHEMA = "SCHEMA"
    MIGRATION = "MIGRATION"
    API_CONTRACT = "API_CONTRACT"
    CHAT_HISTORY = "CHAT_HISTORY"
    OTHER = "OTHER"
    SAMPLE = "SAMPLE"


class CapabilityStatus(StrEnum):
    IMPLEMENTED = "IMPLEMENTED"
    PHASE_ONE = "PHASE_ONE"
    DOCTRINE = "DOCTRINE"
    OUTSTANDING_HARDENING = "OUTSTANDING_HARDENING"
    FUTURE_ROADMAP = "FUTURE_ROADMAP"
    DESIGN_DISCUSSION = "DESIGN_DISCUSSION"
    UNKNOWN = "UNKNOWN"


class DocumentStatus(StrEnum):
    ACTIVE = "ACTIVE"
    SUPERSEDED = "SUPERSEDED"


class ChatRole(StrEnum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"


SOURCE_TYPE_VALUES = {item.value for item in SourceType}
CAPABILITY_STATUS_VALUES = {item.value for item in CapabilityStatus}
DOCUMENT_STATUS_VALUES = {item.value for item in DocumentStatus}
CHAT_ROLE_VALUES = {item.value for item in ChatRole}


def normalize_source_type(value: str | None) -> str:
    normalized = (value or SourceType.OTHER.value).upper()
    if normalized not in SOURCE_TYPE_VALUES:
        raise ValueError(f"Invalid source_type '{value}'.")
    return normalized


def normalize_capability_status(value: str | None) -> str:
    normalized = (value or CapabilityStatus.UNKNOWN.value).upper()
    if normalized not in CAPABILITY_STATUS_VALUES:
        raise ValueError(f"Invalid capability_status '{value}'.")
    return normalized


def normalize_document_status(value: str | None) -> str:
    normalized = (value or DocumentStatus.ACTIVE.value).upper()
    if normalized not in DOCUMENT_STATUS_VALUES:
        raise ValueError(f"Invalid document_status '{value}'.")
    return normalized


def normalize_chat_role(value: str) -> str:
    normalized = value.upper()
    if normalized not in CHAT_ROLE_VALUES:
        raise ValueError(f"Invalid chat role '{value}'.")
    return normalized
