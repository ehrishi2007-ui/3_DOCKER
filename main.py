from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import repository


@asynccontextmanager
async def lifespan(app: FastAPI):
    repository.init_db()
    yield


app = FastAPI(
    title="Task CRUD API",
    description="Task CRUD API backed by PostgreSQL in Docker",
    version="1.0",
    lifespan=lifespan,
)


@app.get(
    "/",
    summary="API Information",
    description="Returns basic information about the Task API.",
)
async def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get(
    "/health",
    summary="Health Check",
    description="Checks whether the API is running.",
)
async def health():
    return {"status": "healthy"}


@app.get("/tasks", summary="Get All Tasks", description="Returns a list of all tasks.")
async def get_tasks():
    return repository.get_all_tasks()


@app.get(
    "/tasks/{id}",
    summary="Get Task by ID",
    description="Returns a task by its ID.",
)
async def get_task(id: int):
    task = repository.get_task_by_id(id)
    if task is None:
        return JSONResponse(status_code=404, content={"error": "Task not found"})
    return task
