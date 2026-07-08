import uuid
from threading import Lock

from jobs import DownloadJob

downloads = {}

lock = Lock()


def create_download(url, format_id):

    job = DownloadJob(

        id=str(uuid.uuid4()),

        url=url,

        format_id=format_id

    )

    with lock:

        downloads[job.id] = job

    return job.id


def get_download(download_id):

    with lock:

        return downloads.get(download_id)


def update_download(download_id, **kwargs):

    with lock:

        job = downloads.get(download_id)

        if job is None:
            return

        for key, value in kwargs.items():

            setattr(job, key, value)


def delete_download(download_id):

    with lock:

        downloads.pop(download_id, None)
def list_downloads():

    with lock:

        return list(downloads.values())