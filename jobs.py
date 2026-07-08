from dataclasses import dataclass
from datetime import datetime


@dataclass
class DownloadJob:

    id: str

    url: str

    format_id: str

    progress: float = 0

    speed: float = 0

    eta: int = 0

    status: str = "queued"

    filename: str | None = None

    error: str | None = None

    created_at: datetime = datetime.now()