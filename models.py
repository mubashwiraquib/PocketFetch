from pydantic import BaseModel


class URLRequest(BaseModel):
    url: str


class DownloadRequest(BaseModel):
    url: str
    format_id: str


class MediaFormat(BaseModel):

    id: str | None = None

    resolution: str | None = None

    ext: str | None = None

    filesize: int | None = None


class AnalyzeResponse(BaseModel):

    success: bool

    title: str | None = None

    thumbnail: str | None = None

    duration: int | None = None

    formats: list[MediaFormat] = []

    error: str | None = None

class ProgressResponse(BaseModel):

    progress: float

    speed: float

    eta: int

    status: str

    filename: str | None = None

    error: str | None = None