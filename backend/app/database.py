import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import Generator, Optional, Any, Dict
from dotenv import load_dotenv
import os

load_dotenv()

# Database configuration
DB_CONFIG = {
    'dbname': 'notes_db',
    'user': 'postgres',
    'password': os.getenv("DB_PASSWORD"),
    'host': 'localhost',
    'port': '5433',
}

@contextmanager
def get_db_connection() -> Generator[psycopg2.extensions.connection, None, None]:
    """
    Context manager to get a database connection.
    """
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()

def execute_query(query: str, params: Optional[tuple] = None) -> None:
    """
    Execute a query that does not return results (e.g., INSERT, UPDATE, DELETE).
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            conn.commit()

def fetch_query(query: str, params: Optional[tuple] = None) -> list[Dict[str, Any]]:
    """
    Execute a query that returns results (e.g., SELECT).
    """
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            results = cur.fetchall()
            return results
        
def initialize_database() -> None:
    """
    Initialize the database with necessary tables.
    """
    create_files_table_query = """
    CREATE TABLE IF NOT EXISTS files (
        id SERIAL PRIMARY KEY,
        file_id VARCHAR(255) UNIQUE NOT NULL,
        filename VARCHAR(255) NOT NULL,
        upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    execute_query(create_files_table_query)

    create_notes_table_query = """
    CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    file_id VARCHAR(255) UNIQUE NOT NULL
        REFERENCES files(file_id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    model VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    execute_query(create_notes_table_query)


def save_file(file_id: str, filename: str):
    """
    Save file metadata to the database.
    """
    query = """
    INSERT INTO files (file_id, filename)
    VALUES (%s, %s)
    ON CONFLICT (file_id)
    DO UPDATE SET filename = EXCLUDED.filename
    """
    execute_query(query, (file_id, filename))


def get_notes_by_file_id(file_id: str):
    query = "SELECT content FROM notes WHERE file_id = %s"
    results = fetch_query(query, (file_id,))
    return results[0]["content"] if results else None


def save_notes(file_id: str, content: str, model: str):
    query = """
    INSERT INTO notes (file_id, content, model)
    VALUES (%s, %s, %s)
    ON CONFLICT (file_id)
    DO UPDATE SET content = EXCLUDED.content
    """
    execute_query(query, (file_id, content, model))
