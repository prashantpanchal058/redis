from .celery_app import celery
import time

@celery.task
def sample_task(seconds: int):
    time.sleep(seconds)
    return {"status": "done", "waited": seconds}