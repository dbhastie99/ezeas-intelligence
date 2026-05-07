from app.core.enums import SourceType

SOURCE_AUTHORITY: dict[str, int] = {
    SourceType.PLATFORM_DOCTRINE.value: 100,
    SourceType.HARDENING_LOG.value: 90,
    SourceType.DEVELOPER_LOG.value: 80,
    SourceType.REQUIREMENTS.value: 70,
    SourceType.CHAT_HISTORY.value: 40,
    SourceType.OTHER.value: 10,
    SourceType.SAMPLE.value: 1,
}


def get_source_authority(source_type: str | None) -> int:
    if not source_type:
        return SOURCE_AUTHORITY[SourceType.OTHER.value]
    return SOURCE_AUTHORITY.get(source_type.upper(), SOURCE_AUTHORITY["OTHER"])
