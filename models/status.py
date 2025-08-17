from enum import StrEnum


class PaperStatus(StrEnum):
    NEW = "NEW"
    INGESTED = "INGESTED"
    GENERATED = "GENERATED"
    FAILED = "FAILED"