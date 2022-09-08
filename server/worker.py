from celery import Celery

celery_app = Celery('upload_video', broker='amqp://127.0.0.1:5672//')


@celery_app.task
def upload_video(file_path, bucket_name):
    print('upload video')
