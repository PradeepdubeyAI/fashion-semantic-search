"""FastAPI entry point for the Dress Search backend."""
from __future__ import annotations

import json
from typing import Dict, List

import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .config import get_settings
from . import db
from .services import processor
from .services.ingestion import ingest_url

settings = get_settings()

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.frontend_origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", summary="Health check")
def health_check() -> dict[str, str]:
    """Return a basic health payload for quick diagnostics."""
    return {"status": "ok"}


@app.on_event("startup")
def startup() -> None:
    """Ensure schema exists before handling requests."""
    db.initialize_schema()


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Natural language search query")


class ImageResult(BaseModel):
    id: int
    filename: str
    file_path: str
    silhouette: str | None = None
    length: str | None = None
    sleeve_type: str | None = None
    color: str | None = None
    metadata: dict
    similarity: float | None = None


class SearchResponse(BaseModel):
    filters: Dict[str, str]
    results: List[ImageResult]


class UploadRequest(BaseModel):
    urls: List[str]


class UploadResponse(BaseModel):
    processed: int
    failures: List[str]


def deserialize_vector(blob: bytes) -> np.ndarray:
    arr = np.frombuffer(blob, dtype=np.float32)
    return arr


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if not denom:
        return 0.0
    return float(np.dot(a, b) / denom)


@app.post("/search", response_model=SearchResponse)
def search(payload: SearchRequest) -> SearchResponse:
    """Return ranked images based on embedding similarity and attribute filters."""
    filters = processor.parse_query_filters(payload.query)
    
    # First try exact filter match; if no results, fetch all and rank by similarity
    records = db.fetch_with_filters(filters)
    if not records:
        records = db.fetch_all_embeddings()

    if not records:
        return SearchResponse(filters=filters, results=[])

    query_vector = processor.encode_text(payload.query)

    results: list[ImageResult] = []
    for row in records:
        vector = deserialize_vector(row["vector"])
        similarity = cosine_similarity(query_vector, vector)
        metadata = json.loads(row["metadata_json"])
        results.append(
            ImageResult(
                id=row["id"],
                filename=row["filename"],
                file_path=row["file_path"],
                silhouette=row["silhouette"],
                length=row["length"],
                sleeve_type=row["sleeve_type"],
                color=row["color"],
                metadata=metadata,
                similarity=similarity,
            )
        )

    results.sort(key=lambda r: r.similarity or 0.0, reverse=True)
    return SearchResponse(filters=filters, results=results)


@app.get("/images", response_model=List[ImageResult])
def list_images() -> List[ImageResult]:
    """Return all stored images without similarity scores."""
    rows = db.fetch_images()
    return [
        ImageResult(
            id=row["id"],
            filename=row["filename"],
            file_path=row["file_path"],
            silhouette=row["silhouette"],
            length=row["length"],
            sleeve_type=row["sleeve_type"],
            color=row["color"],
            metadata=json.loads(row["metadata_json"]),
            similarity=None,
        )
        for row in rows
    ]


@app.post("/upload-images", response_model=UploadResponse)
def upload_images(payload: UploadRequest) -> UploadResponse:
    """Accept remote image URLs and ingest them into the database."""
    successes = 0
    failures: list[str] = []

    for url in payload.urls:
        trimmed = url.strip()
        if not trimmed:
            continue
        try:
            ingest_url(trimmed)
            successes += 1
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{trimmed}: {exc}")

    return UploadResponse(processed=successes, failures=failures)
