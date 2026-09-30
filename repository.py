import os
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgres://postgres:dev@localhost:5432/tasks")


def get_connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    done BOOLEAN NOT NULL DEFAULT FALSE
                )
            """)
            cur.execute("SELECT COUNT(*) AS count FROM tasks")
            row = cur.fetchone()
            count = row["count"] if row else 0
            if count == 0:
                cur.execute(
                    "INSERT INTO tasks (title, done) VALUES (%s, %s)",
                    ("Learn FastAPI", False),
                )
                cur.execute(
                    "INSERT INTO tasks (title, done) VALUES (%s, %s)",
                    ("Build Task API", False),
                )
                cur.execute(
                    "INSERT INTO tasks (title, done) VALUES (%s, %s)",
                    ("Test endpoints", True),
                )
        conn.commit()


def get_all_tasks():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks ORDER BY id")
            return cur.fetchall()


def get_task_by_id(task_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
            return cur.fetchone()
