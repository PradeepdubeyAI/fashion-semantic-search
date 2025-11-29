"""SQLite helper utilities for persisting images and embeddings."""
from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

DB_FILENAME = "dress_search.db"
BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / DB_FILENAME


SCHEMA_STATEMENTS: Iterable[str] = (
    """
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL UNIQUE,
        file_path TEXT NOT NULL,
        silhouette TEXT,
        length TEXT,
        sleeve_type TEXT,
        color TEXT,
        metadata_json TEXT NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS embeddings (
        image_id INTEGER PRIMARY KEY,
        vector BLOB NOT NULL,
        FOREIGN KEY(image_id) REFERENCES images(id) ON DELETE CASCADE
    );
    """,
)


def get_connection() -> sqlite3.Connection:
    """Return a connection to the project database, creating directories as needed."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_schema() -> None:
    """Create tables if they do not exist."""
    with get_connection() as conn:
        cursor = conn.cursor()
        for statement in SCHEMA_STATEMENTS:
            cursor.executescript(statement)
        conn.commit()


@dataclass(slots=True)
class ImageRecord:
    filename: str
    file_path: str
    silhouette: str
    length: str
    sleeve_type: str
    color: str
    metadata_json: str


def insert_image(record: ImageRecord, vector: bytes) -> None:
    """Persist an image record and its embedding as an atomic operation."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO images (filename, file_path, silhouette, length, sleeve_type, color, metadata_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.filename,
                record.file_path,
                record.silhouette,
                record.length,
                record.sleeve_type,
                record.color,
                record.metadata_json,
            ),
        )
        image_id = cursor.lastrowid
        cursor.execute(
            """
            INSERT OR REPLACE INTO embeddings (image_id, vector) VALUES (?, ?)
            """,
            (image_id, vector),
        )
        conn.commit()


def fetch_all_embeddings() -> Sequence[sqlite3.Row]:
    """Return every image row joined with its embedding."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT images.*, embeddings.vector FROM images
            JOIN embeddings ON images.id = embeddings.image_id
            ORDER BY images.id
            """
        )
        return cursor.fetchall()


def fetch_images() -> Sequence[sqlite3.Row]:
    """Return all image metadata without embeddings."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, filename, file_path, silhouette, length, sleeve_type, color, metadata_json
            FROM images ORDER BY id
            """
        )
        return cursor.fetchall()


def fetch_with_filters(filters: Mapping[str, str]) -> Sequence[sqlite3.Row]:
    """Return images joined with embeddings filtered by provided columns."""
    clauses = []
    params: list[str] = []
    for column in ("silhouette", "length", "sleeve_type", "color"):
        value = filters.get(column)
        if value:
            clauses.append(f"images.{column} = ?")
            params.append(value)

    where_clause = f"WHERE {' AND '.join(clauses)}" if clauses else ""

    query = f"""
        SELECT images.*, embeddings.vector FROM images
        JOIN embeddings ON images.id = embeddings.image_id
        {where_clause}
        ORDER BY images.id
    """

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
