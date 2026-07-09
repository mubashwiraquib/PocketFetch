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

    video_formats = []

    audio_formats = []

    for f in info.get("formats", []):

        item = {

            "id": f.get("format_id"),

            "ext": f.get("ext"),

            "filesize": f.get("filesize"),

            "resolution": (
                f.get("resolution")
                or (
                    f"{f.get('height')}p"
                    if f.get("height")
                    else "Audio"
                )
            )

        }

        if (
             f.get("vcodec") == "none"
            and f.get("acodec") != "none"
            and f.get("ext") != "mhtml"
             ):

           audio_formats.append(item)

        elif (
        f.get("vcodec") != "none"
        and f.get("ext") != "mhtml"
        ):

           video_formats.append(item)

    return {

        "title": info.get("title"),

        "thumbnail": info.get("thumbnail"),

        "duration": info.get("duration"),

        "video_formats": video_formats,

        "audio_formats": audio_formats

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
                status="processing"
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

    print("DEBUG:", filename)

    update_download(
        download_id,
        filename=filename,
        progress=100,
        status="finished",
    )

    print("DEBUG: status updated")

    return filename