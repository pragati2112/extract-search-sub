import datetime
import shutil
from pathlib import Path
from fastapi import File, UploadFile, APIRouter, BackgroundTasks, Body
import math
import os
from server.extraction import extract_subtitles
from server.read_srt import read_srt_file, search_subtitle
from server.worker import celery_app

router = APIRouter()


def upload_video(file_path, filename, bucket_name):
    pass


def generate_desired_directories():
    desired_directory_path = 'server/uploads' + os.sep + 'srts'
    if not os.path.exists(desired_directory_path):
        os.makedirs(desired_directory_path)


@router.post("/upload", response_description="Upload video")
async def media(background_task: BackgroundTasks, video_file: UploadFile = File(...)):
    extension = video_file.filename.split('.')[-1]
    new_file_name = str(math.floor(datetime.datetime.now().timestamp()))
    filename = new_file_name + '.' + extension

    generate_desired_directories()

    destination = Path('server/uploads/' + filename)
    with destination.open("wb") as buffer:
        shutil.copyfileobj(video_file.file, buffer)

    file_path = 'server/uploads/' + filename

    # send task to celery to upload video OR can use background tasks of fast api--

    # task_name = 'upload_video'
    # celery_app.send_task(task_name, args=[file_path, upload_bucket])
    # background_task.add_task(upload_video(file_path, filename, bucket_name=''))

    # close the file
    video_file.file.close()

    # use cc-extractor--  to extract subtitles
    out_path = 'server/uploads/srts/' + new_file_name + '.srt'
    video_id = extract_subtitles(file_path, out_path, video_id=new_file_name)
    return {'video_id': video_id}


@router.post("/search-subtitles", response_description="Search for subtitles")
async def search(data=Body(...)):
    return search_subtitle(data['subtitle'], data['video_id'])
