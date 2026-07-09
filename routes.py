from threading import Thread

from fastapi import APIRouter
from fastapi.responses import FileResponse

from downloader import analyze_url, download_format
from download_manager import (
    create_download,
    get_download,
)
from models import (
    URLRequest,
    AnalyzeResponse,
    DownloadRequest,
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
    video_formats=info["video_formats"],
    audio_formats=info["audio_formats"]
)

    except Exception as e:

        return AnalyzeResponse(
            success=False,
            error=str(e),
        )


@router.post("/download")
async def download(data: DownloadRequest):

    download_id = create_download(
        data.url,
        data.format_id,
    )

    job = get_download(download_id)

    thread = Thread(
        target=download_format,
        args=(
            download_id,
            data.url,
            data.format_id,
        ),
        daemon=True,
    )

    thread.start()

    return {
        "download_id": download_id,
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
        "status": job.status,
        "progress": job.progress,
        "speed": job.speed,
        "eta": job.eta,
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
        job.filename,
        filename=job.filename.split("\\")[-1],
    )