"""Shared ingestion utilities used by both CLI and API layers."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import requests
from requests import Response

from .. import db
from ..db import ImageRecord
from . import processor

IMAGES_DIR = Path(__file__).resolve().parents[2] / "images"


def download_image(url: str) -> Path:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    filename = url.split("/")[-1].split("?")[0]
    target_path = IMAGES_DIR / filename

    if target_path.exists():
        return target_path

    response: Response = requests.get(url, timeout=30)
    response.raise_for_status()
    target_path.write_bytes(response.content)
    return target_path


def ingest_url(url: str) -> ImageRecord:
    """Download an image, extract attributes, and persist to SQLite."""
    image_path = download_image(url)
    pil_image = processor.load_image(image_path)
    attributes = processor.zero_shot_classify(pil_image)
    embedding = processor.encode_image(pil_image).astype(np.float32).tobytes()

    metadata = {
        "source_url": url,
        "attributes": attributes,
    }

    record = ImageRecord(
        filename=image_path.name,
        file_path=str(image_path.resolve()),
        silhouette=attributes.get("silhouette", "Unknown"),
        length=attributes.get("length", "Unknown"),
        sleeve_type=attributes.get("sleeve_type", "Unknown"),
        color=attributes.get("color", "Unknown"),
        metadata_json=json.dumps(metadata),
    )

    db.insert_image(record, embedding)
    return record
