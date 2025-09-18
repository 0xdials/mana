import os
import time
from typing import Optional

import psycopg2
from psycopg2 import sql
import redis
from fastapi import FastAPI

SERVICE_NAME = "ai-pipeworks"

PG_DSN = os.getenv("PG_DSN", "postgresql://app:app@postgres:5432/app")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

app = FastAPI(title=SERVICE_NAME)

_pg_conn: Optional[psycopg2.extensions.connection] = None
_redis_client: Optional[redis.Redis] = None

def get_pg_conn() -> psycopg2.extensions.connection:
    """Lazy-init a PostgreSQL connection; keep it simple and blocking."""
    global _pg_conn
    if _pg_conn is None or _pg_conn.closed:
        # keep connect fast; don't hang during startup
        _pg_conn = psycopg2.connect(PG_DSN, connect_timeout=2)
        _pg_conn.autocommit = True
    return _pg_conn

def get_redis() -> redis.Redis:
    """Lazy-init a Redis client."""
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.Redis.from_url(
            REDIS_URL,
            socket_connect_timeout=1,
            socket_timeout=1,
            health_check_interval=0,
        )
    return _redis_client

@app.get("/")
def root():
    return {"service": SERVICE_NAME, "message": "welcome to the infra skeleton"}

@app.get("/healthz")
def healthz():
    ts = int(time.time())
    pg_ok = False
    redis_ok = False

    # Postgres check
    try:
        conn = get_pg_conn()
        with conn.cursor() as cur:
            cur.execute(sql.SQL("SELECT 1"))
            cur.fetchone()
        pg_ok = True
    except Exception:
        pg_ok = False  # don't raise; report false

    # Redis check
    try:
        r = get_redis()
        redis_ok = (r.ping() is True)
    except Exception:
        redis_ok = False

    ok = pg_ok and redis_ok
    return {"ok": ok, "postgres": pg_ok, "redis": redis_ok, "service": SERVICE_NAME, "ts": ts}

