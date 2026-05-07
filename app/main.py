from fastapi import FastAPI, HTTPException
from celery import Celery
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Celery Configuration
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

# Create Celery instance
celery = Celery(
    "tasks",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)


@celery.task
def schedule_task(task_id: int, message: str):
    pass


@app.post("/schedule-task/{task_id}")
async def schedule_task_api(
    task_id: int,
    message: str,
    execute_at: datetime
):
    print(datetime.utcnow())
    if execute_at <= datetime.utcnow():
        raise HTTPException(
            status_code=400,
            detail="Invalid execution time, please choose any future time"
        )

    schedule_task.apply_async(
        args=[task_id, message],
        eta=execute_at
    )

    return {
        "message": f"task {task_id} scheduled for execution at {execute_at}"
    }