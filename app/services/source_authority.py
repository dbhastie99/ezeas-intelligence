SOURCE_AUTHORITY: dict[str, int] = {
    "PLATFORM_DOCTRINE": 100,
    "HARDENING_LOG": 90,
    "DEVELOPER_LOG": 80,
    "REQUIREMENTS": 70,
    "CHAT_HISTORY": 40,
    "OTHER": 10,
}


def get_source_authority(source_type: str | None) -> int:
    if not source_type:
        return SOURCE_AUTHORITY["OTHER"]
    return SOURCE_AUTHORITY.get(source_type.upper(), SOURCE_AUTHORITY["OTHER"])
