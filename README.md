# Task CRUD API — Containerized Postgres Edition

A RESTful CRUD (Create, Read, Update, Delete) API built using **FastAPI** and backed by a containerized **PostgreSQL** database. 

This project is the third storage iteration in the series:
`In-Memory (A1)` → `SQLite (A2)` → `Containerized PostgreSQL (A3)`

The external API interface, request/response formats, and status codes remain identical to earlier assignments, but the storage engine is now a real PostgreSQL server running in a Docker container with data persisted using named Docker volumes. The entire stack starts with a single command via **Docker Compose**.

---

## The One Command to Run Everything

To start both the FastAPI application and the PostgreSQL database:

```bash
docker compose up
```

To run in detached (background) mode:

```bash
docker compose up -d
```

To shut down the stack while keeping your data safe in the volume:

```bash
docker compose down
```

---

## Environment Variables & Configuration

Database credentials and connection settings are configured via environment variables and loaded from a `.env` file.

> **Security Note:** Secrets like database passwords must never be committed to source control. The `.env` file is ignored by Git in `.gitignore`. A template file [`.env.example`](.env.example) is committed to show the required configuration.

### Setting up `.env`:

Copy the template:

```bash
cp .env.example .env
```

### Variables defined in `.env.example`:

| Variable | Description | Example (Local Run) | Compose Network Value |
|---|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | `postgres://postgres:dev@localhost:5432/tasks` | `postgres://postgres:dev@db:5432/tasks` |

Inside the Docker Compose network, the API service accesses the database container via the service hostname `db` rather than `localhost`.

---

## API Endpoints

| Method | Endpoint | Description | Request Body | Success Status | Error Status |
|---|---|---|---|---|---|
| `GET` | `/` | API Information | None | `200 OK` | — |
| `GET` | `/health` | Health Check | None | `200 OK` | — |
| `GET` | `/tasks` | List all tasks | None | `200 OK` | — |
| `GET` | `/tasks/{id}` | Retrieve task by ID | None | `200 OK` | `404 Not Found` |
| `POST` | `/tasks` | Create a new task | `{"title": "string"}` | `201 Created` | `400 Bad Request` |
| `PUT` | `/tasks/{id}` | Update title/status | `{"title": "string", "done": boolean}` | `200 OK` | `400 Bad Request`, `404 Not Found` |
| `DELETE` | `/tasks/{id}` | Delete task by ID | None | `204 No Content` | `404 Not Found` |

### Error Responses
All errors return JSON with an informative error message:
- Validation failure (missing or empty title): `{"error": "Title is required"}` (HTTP 400)
- Resource not found: `{"error": "Task not found"}` (HTTP 404)

---

## Sample Request & Response (`curl -i`)

Here is an example request retrieving tasks from the running containerized application:

```bash
$ curl.exe -i http://localhost:3000/tasks
HTTP/1.1 200 OK
date: Wed, 30 Sep 2026 11:07:06 GMT
server: uvicorn
content-length: 211
content-type: application/json

[{"id":1,"title":"Learn FastAPI","done":false},{"id":2,"title":"Build Task API","done":false},{"id":3,"title":"Test endpoints","done":true},{"id":4,"title":"Persistent Task Across Docker Restarts","done":false}]
```

Creating a task:

```bash
$ curl -i -X POST http://localhost:3000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Containerize with Docker"}'
HTTP/1.1 201 Created
date: Wed, 30 Sep 2026 10:57:23 GMT
server: uvicorn
content-length: 56
content-type: application/json

{"id":4,"title":"Containerize with Docker","done":false}
```

---

## Database Verification & Screenshot

The database automatically initializes the `tasks` table if it does not exist and seeds three initial example tasks on first run.

Inspecting the database directly via `psql` inside the container:

```bash
docker compose exec db psql -U postgres -d tasks -c "\dt"
docker compose exec db psql -U postgres -d tasks -c "SELECT * FROM tasks;"
```

![Database Screenshot](images/database-screenshot.png)

---

## Persistence Across Restarts

Data persistence is managed using a named Docker volume (`taskdata`). Even when containers are stopped and removed with `docker compose down`, all tasks remain safe in the volume and are available immediately upon `docker compose up`.

---

## Quickstart for Strangers (Round-Trip Test)

To clone and run this project on any machine with Docker installed:

```bash
git clone https://github.com/ehrishi2007-ui/3_DOCKER.git
cd 3_DOCKER
cp .env.example .env
docker compose up --build
```

The API will be available at `http://localhost:3000`. Interactive documentation (Swagger UI) is accessible at `http://localhost:3000/docs`.
