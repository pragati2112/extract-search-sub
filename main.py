import datetime
import shutil
from pathlib import Path
from fastapi import File, UploadFile, APIRouter, BackgroundTasks, Body, jsonable_encoder
import math
import os
from extraction import extract_subtitles
from read_srt import read_srt_file, search_subtitle
from worker import celery_app
router = APIRouter()


def upload_video(file_path, filename, bucket_name):
    pass


def generate_desired_directories():
    desired_directory_path = 'uploads' + os.sep + 'srts'
    if not os.path.exists(desired_directory_path):
        os.makedirs(desired_directory_path)


@router.post("/upload/video", response_description="Upload video")
async def media(background_task: BackgroundTasks, video_file: UploadFile = File(...)):
    extension = video_file.filename.split('.')[-1]
    new_file_name = str(math.floor(datetime.datetime.now().timestamp()))
    filename = new_file_name + '.' + extension

    generate_desired_directories()

    destination = Path('uploads/' + filename)
    with destination.open("wb") as buffer:
        shutil.copyfileobj(video_file.file, buffer)

    file_path = 'uploads/' + filename

    # send task to celery to upload video OR can use background tasks of fast api--

    # task_name = 'upload_video'
    # celery_app.send_task(task_name, args=[file_path, upload_bucket])
    background_task.add_task(upload_video(file_path, filename, bucket_name=''))

    # close the file
    video_file.file.close()

    # use cc-extractor--  to extract subtitles
    out_path = 'uploads/srts/' + new_file_name + '.srt'
    extract_subtitles(file_path, out_path)

    # read srt file and save subtitles to dynamodb
    read_srt_file(out_path, video_id=new_file_name)

    return {'message': 'File uploaded!'}


@router.post("/search/subtitles", response_description="Search for subtitles")
async def search(data: Body(...)):
    data = jsonable_encoder(data)
    return search_subtitle(data['subtitle'], data['video_id'])
