from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from .tasks import schedule_task
from celery.result import AsyncResult
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/schedule-task/{task_id}")
async def schedule_task_api(
    task_id: int,
    message: str,
    execute_at: datetime
):
    print("hii")
    if execute_at <= datetime.utcnow():
        raise HTTPException(
            status_code=400,
            detail="Invalid execution time, please choose any future time"
        )

    task = schedule_task.apply_async(
        args=[task_id, message],
        eta=execute_at
    )

    return {
        "task_id": task.id,
        "message": f"Task {task_id} scheduled for execution at {execute_at}"
    }


@app.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    result = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result
    }