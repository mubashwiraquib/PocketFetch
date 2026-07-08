import os
import threading

import yt_dlp

from config import DOWNLOAD_FOLDER
from download_manager import update_download


def analyze_url(url: str):
    """
    Analyze a URL without downloading it.
    Returns metadata and available video formats.
    """

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    formats = []

    for f in info.get("formats", []):

        # Skip audio-only formats
        if f.get("vcodec") == "none":
            continue

        formats.append(
            {
                "id": f.get("format_id"),
                "resolution": f.get("resolution")
                or f"{f.get('height', '?')}p",
                "ext": f.get("ext"),
                "filesize": f.get("filesize"),
            }
        )

    return {
        "title": info.get("title"),
        "thumbnail": info.get("thumbnail"),
        "duration": info.get("duration"),
        "formats": formats,
    }


def progress_hook(download_id):
    """
    Called automatically by yt-dlp while downloading.
    """

    def hook(data):

        status = data.get("status")

        if status == "downloading":

            downloaded = data.get("downloaded_bytes", 0)

            total = (
                data.get("total_bytes")
                or data.get("total_bytes_estimate")
                or 0
            )

            progress = 0

            if total:
                progress = downloaded / total * 100

            update_download(
                download_id,
                progress=round(progress, 2),
                speed=data.get("speed", 0),
                eta=data.get("eta", 0),
                status="downloading",
            )

        elif status == "finished":

            update_download(
                download_id,
                progress=100,
                status="finished",
            )

    return hook


def download_worker(job):
    """
    Runs inside a background thread.
    """

    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

    ydl_opts = {
        "format": job.format_id,
        "outtmpl": os.path.join(
            DOWNLOAD_FOLDER,
            "%(title)s.%(ext)s",
        ),
        "progress_hooks": [
            progress_hook(job.id),
        ],
    }

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                job.url,
                download=True,
            )

            filename = ydl.prepare_filename(info)

        update_download(
            job.id,
            filename=filename,
            progress=100,
            status="finished",
        )

    except Exception as e:

        update_download(
            job.id,
            status="error",
            error=str(e),
        )


def start_download(job):
    """
    Starts the download in a background thread.
    Returns immediately.
    """

    thread = threading.Thread(
        target=download_worker,
        args=(job,),
        daemon=True,
    )

    thread.start()