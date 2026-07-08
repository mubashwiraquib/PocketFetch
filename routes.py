from fastapi import APIRouter
from fastapi.responses import FileResponse

from downloader import analyze_url, start_download
from download_manager import (
    create_download,
    get_download,
)
from models import (
    URLRequest,
    DownloadRequest,
    AnalyzeResponse,
)

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
            formats=info["formats"],
        )

    except Exception as e:

        return AnalyzeResponse(
            success=False,
            error=str(e),
        )


@router.post("/download")
async def download(data: DownloadRequest):

    job_id = create_download(
        data.url,
        data.format_id,
    )

    job = get_download(job_id)

    start_download(job)

    return {
        "download_id": job.id,
        "status": job.status,
    }


@router.get("/progress/{download_id}")
async def progress(download_id: str):

    job = get_download(download_id)

    if job is None:

        return {
            "success": False,
            "error": "Download not found",
        }

    return {
        "id": job.id,
        "progress": job.progress,
        "speed": job.speed,
        "eta": job.eta,
        "status": job.status,
        "filename": job.filename,
        "error": job.error,
    }


@router.get("/file/{download_id}")
async def get_file(download_id: str):

    job = get_download(download_id)

    if job is None:

        return {
            "success": False,
            "error": "Download not found",
        }

    if job.filename is None:

        return {
            "success": False,
            "error": "Download not finished",
        }

    return FileResponse(
        path=job.filename,
        filename=job.filename.split("\\")[-1],
    )