"""Offline ingestion script to download images, extract attributes, and populate SQLite."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable

from app import db
from app.services.ingestion import ingest_url
from app.services.model_loader import get_models


def load_urls(csv_path: Path) -> Iterable[str]:
    """Yield URLs from a CSV where each line includes an Image URLs column."""
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        for row in reader:
            if not row:
                continue
            value = row[0].strip()
            if value.lower().startswith("http"):
                yield value


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest dress images into SQLite")
    parser.add_argument("csv", type=Path, help="Path to CSV file containing image URLs")
    args = parser.parse_args()

    db.initialize_schema()
    # Trigger model downloads upfront so the first request does not block unexpectedly.
    get_models()

    urls = list(load_urls(args.csv))
    print(f"Found {len(urls)} URLs")
    for url in urls:
        try:
            record = ingest_url(url)
            print(f"Stored {record.filename}")
        except Exception as exc:  # noqa: BLE001
            print(f"Failed to ingest {url}: {exc}")


if __name__ == "__main__":
    main()
