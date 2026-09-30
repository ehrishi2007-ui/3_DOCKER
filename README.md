# Task CRUD API — Containerized Postgres Edition

A RESTful CRUD (Create, Read, Update, Delete) API built with FastAPI and PostgreSQL running in Docker.

## Stage 0: Run Postgres in Docker

To start Postgres with a persistent volume:

```bash
docker run --name taskdb -e POSTGRES_PASSWORD=dev -e POSTGRES_DB=tasks \
  -p 5432:5432 -v taskdata:/var/lib/postgresql/data -d postgres
```
