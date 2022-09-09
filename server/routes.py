import datetime
import shutil
from pathlib import Path
from fastapi import File, UploadFile, APIRouter, BackgroundTasks, Body
import math
import os
from server.extraction import extract_subtitles
from server.read_srt import search_subtitle

router = APIRouter()

uploads_dir = 'server/uploads/'
strs_uploads = 'server/uploads/srts/'


def generate_desired_directories():
    if not os.path.exists(strs_uploads):
        os.makedirs(strs_uploads)


@router.post("/upload", response_description="Upload video")
async def media(background_task: BackgroundTasks, video_file: UploadFile = File(...)):
    extension = video_file.filename.split('.')[-1]
    new_file_name = str(math.floor(datetime.datetime.now().timestamp()))
    filename = new_file_name + '.' + extension

    generate_desired_directories()

    destination = Path(uploads_dir + filename)
    with destination.open("wb") as buffer:
        shutil.copyfileobj(video_file.file, buffer)

    file_path = uploads_dir + filename

    # send task to celery to upload video OR can use background tasks of fast api--

    # task_name = 'upload_video'
    # celery_app.send_task(task_name, args=[file_path, upload_bucket])
    # background_task.add_task(upload_video(file_path, filename, bucket_name=''))

    # close the file
    video_file.file.close()

    # use cc-extractor--  to extract subtitles
    out_path = strs_uploads + new_file_name + '.srt'
    background_task.add_task(extract_subtitles, file_path=file_path, out_path=out_path, video_id=new_file_name)

    return {'status': 'File processing', 'video_id': new_file_name}


@router.post("/search-subtitles", response_description="Search for subtitles")
async def search(video_id=None, subtitle: str = ''):
    return search_subtitle(video_id, subtitle)
