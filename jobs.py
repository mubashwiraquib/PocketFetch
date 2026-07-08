from dataclasses import dataclass


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