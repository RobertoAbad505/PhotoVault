from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class PhotoFile:
    path: str
    name: str
    extension: str
    size: int
    created_at: datetime
