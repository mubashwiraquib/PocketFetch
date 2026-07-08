import yt_dlp


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