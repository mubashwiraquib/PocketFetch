from fastapi import APIRouter

from downloader import analyze_url
from models import URLRequest, AnalyzeResponse

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(data: URLRequest):

    try:
        info = analyze_url(data.url)

        return AnalyzeResponse(
            success=True,
            title=info["title"],
            thumbnail=info["thumbnail"],
            duration=info["duration"],
            formats=info["formats"]
        )

    except Exception as e:
        return AnalyzeResponse(
            success=False,
            error=str(e)
        )