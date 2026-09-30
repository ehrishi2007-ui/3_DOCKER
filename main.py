from contextlib import asynccontextmanager
from fastapi import FastAPI
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
