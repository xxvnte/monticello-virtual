import os
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import quote_plus

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

POSTGRES_HOST = "db.yxobdkldjhinxmwfsure.supabase.co"
POSTGRES_PORT = 5432
POSTGRES_DB = "postgres"
POSTGRES_USER = "postgres"

_pool = None


def resolve_database_url():
    password = os.getenv("DB_PASSWORD", "").strip()
    if not password:
        raise ValueError("Falta DB_PASSWORD en el archivo .env")
    encoded_password = quote_plus(password)
    return (
        f"postgresql://{POSTGRES_USER}:{encoded_password}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}?sslmode=require"
    )


def get_pool():
    global _pool
    if _pool is None:
        _pool = ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            dsn=resolve_database_url(),
            cursor_factory=RealDictCursor,
        )
    return _pool


def connect():
    return psycopg2.connect(resolve_database_url(), cursor_factory=RealDictCursor)


@contextmanager
def get_connection():
    pool = get_pool()
    connection = pool.getconn()
    try:
        yield connection
    except Exception:
        connection.rollback()
        raise
    finally:
        pool.putconn(connection)
