from enum import Enum, auto


class PipelineState(Enum):
    IDLE = auto()
    SCANNING = auto()
    SCAN_REPORT = auto()
    DUPLICATES = auto()
    DUPLICATES_REPORT = auto()
    ORGANIZING = auto()
    COMPLETED = auto()
    STOPPED = auto()
