"""Model loader that ensures heavyweight artifacts are loaded once."""
from __future__ import annotations

from functools import lru_cache

from sentence_transformers import SentenceTransformer
import spacy


CLIP_MODEL_NAME = "clip-ViT-B-32"
SPACY_MODEL_NAME = "en_core_web_sm"


class ModelBundle:
    """Container for all ML artifacts used by the service."""

    def __init__(self) -> None:
        self.clip = SentenceTransformer(CLIP_MODEL_NAME)
        self.nlp = spacy.load(SPACY_MODEL_NAME)


@lru_cache(maxsize=1)
def get_models() -> ModelBundle:
    """Return a cached bundle of models."""
    return ModelBundle()
