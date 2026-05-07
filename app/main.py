from fastapi import FastAPI
from .tasks import sample_task
from celery.result import AsyncResult

app = FastAPI()

@app.post("/run-task")
def run_task(seconds: int = 5):
    task = sample_task.delay(seconds)
    return {"task_id": task.id}

@app.get("/task/{task_id}")
def get_task(task_id: str):
    result = AsyncResult(task_id)
    return {"status": result.status, "result": result.result}