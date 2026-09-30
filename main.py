from contextlib import asynccontextmanager
from fastapi import FastAPI, Response
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


@app.post(
    "/tasks",
    status_code=201,
    summary="Create Task",
    description="Creates a new task.",
)
async def create_task(task: dict):
    if not isinstance(task, dict):
        return JSONResponse(status_code=400, content={"error": "Invalid request body"})
    title = task.get("title")
    if title is None or not str(title).strip():
        return JSONResponse(status_code=400, content={"error": "Title is required"})
    done = bool(task.get("done", False))
    new_task = repository.create_task(title=str(title).strip(), done=done)
    return new_task


@app.put(
    "/tasks/{id}",
    summary="Update Task",
    description="Updates the title and/or completion status of a task.",
)
async def update_task(id: int, updated_task: dict):
    if not isinstance(updated_task, dict) or not updated_task:
        return JSONResponse(
            status_code=400, content={"error": "Request body cannot be empty"}
        )

    existing_task = repository.get_task_by_id(id)
    if existing_task is None:
        return JSONResponse(status_code=404, content={"error": "Task not found"})

    title = updated_task.get("title", existing_task["title"])
    if "title" in updated_task and not str(title).strip():
        return JSONResponse(status_code=400, content={"error": "Title is required"})

    done = updated_task.get("done", existing_task["done"])
    if not isinstance(done, bool):
        done = bool(done)

    task = repository.update_task(task_id=id, title=str(title).strip(), done=done)
    return task


@app.delete(
    "/tasks/{id}",
    status_code=204,
    summary="Delete Task",
    description="Deletes a task by its ID.",
)
async def delete_task(id: int):
    existing_task = repository.get_task_by_id(id)
    if existing_task is None:
        return JSONResponse(status_code=404, content={"error": "Task not found"})

    repository.delete_task(id)
    return Response(status_code=204)
