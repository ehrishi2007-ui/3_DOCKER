import os
import time
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgres://postgres:dev@localhost:5432/tasks")


def get_connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def init_db(max_retries: int = 15, delay: float = 1.0):
    for attempt in range(max_retries):
        try:
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
            return
        except psycopg.OperationalError:
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                raise


def get_all_tasks() -> List[Dict[str, Any]]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks ORDER BY id")
            return cur.fetchall()


def get_task_by_id(task_id: int) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
            return cur.fetchone()


def create_task(title: str, done: bool = False) -> Dict[str, Any]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING *",
                (title, done),
            )
            row = cur.fetchone()
        conn.commit()
        return row


def update_task(task_id: int, title: str, done: bool) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING *",
                (title, done, task_id),
            )
            row = cur.fetchone()
        conn.commit()
        return row


def delete_task(task_id: int) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM tasks WHERE id = %s RETURNING id",
                (task_id,),
            )
            row = cur.fetchone()
        conn.commit()
        return row is not None
