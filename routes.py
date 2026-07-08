from fastapi import APIRouter
from downloader import analyze_url
from models import URLRequest, AnalyzeResponse
from downloader import analyze_url, download_format
from models import DownloadRequest
from fastapi.responses import FileResponse
from download_manager import create_download
from download_manager import get_download

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
@router.post("/download")
async def download(data: DownloadRequest):

    try:

        file_path = download_format(
            data.url,
            data.format_id
        )

        return FileResponse(
            file_path,
            filename=file_path.split("\\")[-1]
        )

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
@router.post("/download")

async def start_download(data: DownloadRequest):

    download_id = create_download(
        data.url,
        data.format_id
    )

    return {
        "download_id": download_id
    }
@router.get("/progress/{download_id}")

async def progress(download_id):

    return get_download(download_id)