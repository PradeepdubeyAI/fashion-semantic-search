"""Image and query processing utilities."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

import numpy as np
from PIL import Image
from sentence_transformers.util import cos_sim

from .model_loader import get_models


def load_taxonomy() -> Dict[str, list]:
    """Load fashion attribute taxonomy from taxonomy.json."""
    taxonomy_path = Path(__file__).resolve().parents[2] / "taxonomy.json"
    with open(taxonomy_path, "r") as f:
        return json.load(f)


TAXONOMY = load_taxonomy()


def load_image(image_path: Path) -> Image.Image:
    """Open an image in RGB mode."""
    img = Image.open(image_path)
    return img.convert("RGB")


def encode_image(image: Image.Image) -> np.ndarray:
    """Return the CLIP embedding for an image."""
    models = get_models()
    return models.clip.encode(image, convert_to_numpy=True)


def encode_text(text: str) -> np.ndarray:
    """Return the CLIP embedding for a text query."""
    models = get_models()
    return models.clip.encode(text, convert_to_numpy=True)


def zero_shot_classify(image: Image.Image) -> Dict[str, str]:
    """Derive fashion attributes via zero-shot prompts."""
    models = get_models()
    img_emb = models.clip.encode(image, convert_to_tensor=True)
    attributes: Dict[str, str] = {}

    for category, labels in TAXONOMY.items():
        prompts = [f"a {label} dress" for label in labels]
        text_emb = models.clip.encode(prompts, convert_to_tensor=True)
        scores = cos_sim(img_emb, text_emb)[0]
        best_idx = int(scores.argmax())
        attributes[category] = labels[best_idx]

    return attributes


def parse_query_filters(query: str) -> Dict[str, str]:
    """Extract structured attribute hints from a free-text query."""
    # Fuzzy matching for attribute extraction
    from fuzzywuzzy import fuzz
    filters: Dict[str, str] = {}
    models = get_models()
    doc = models.nlp(query.lower())
    haystack = " ".join(token.text for token in doc)

    for category, labels in TAXONOMY.items():
        for label in labels:
            score = fuzz.token_set_ratio(haystack, label.lower())
            if score >= 75:  # threshold, can tune
                filters[category] = label
                break
    return filters
