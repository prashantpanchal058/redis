from .celery_app import celery

@celery.task
def schedule_task(task_id: int, message: str):
    # your task logic here
    print(f"Executing task {task_id} with message: {message}")
    return {"task_id": task_id, "message": message}