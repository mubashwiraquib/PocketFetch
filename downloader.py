import os
import yt_dlp

from download_manager import update_download

DOWNLOAD_DIR = "downloads"


def analyze_url(url):

    ydl_opts = {
        "quiet": True,
        "skip_download": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(url, download=False)

    formats = []

    for f in info.get("formats", []):

        if f.get("vcodec") == "none":
            continue

        formats.append({
            "id": f.get("format_id"),
            "resolution": f.get("resolution"),
            "ext": f.get("ext"),
            "filesize": f.get("filesize")
        })

    return {

        "title": info.get("title"),

        "thumbnail": info.get("thumbnail"),

        "duration": info.get("duration"),

        "formats": formats

    }


def progress_hook(download_id):

    def hook(data):

        if data["status"] == "downloading":

            downloaded = data.get("downloaded_bytes", 0)

            total = (
                data.get("total_bytes")
                or data.get("total_bytes_estimate")
                or 0
            )

            progress = 0

            if total > 0:
                progress = downloaded / total * 100

            update_download(
                download_id,
                progress=round(progress, 2),
                speed=data.get("speed", 0),
                eta=data.get("eta", 0),
                status="downloading"
            )

        elif data["status"] == "finished":

            update_download(
                download_id,
                progress=100,
                status="finished"
            )

    return hook


def download_format(download_id, url, format_id):

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    ydl_opts = {
        "format": format_id,
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
        "progress_hooks": [
            progress_hook(download_id)
        ]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(url, download=True)

        filename = ydl.prepare_filename(info)

    return filename