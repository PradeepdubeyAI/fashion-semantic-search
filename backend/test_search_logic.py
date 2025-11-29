#!/usr/bin/env python
"""Direct test of search logic without server."""
import sys
sys.path.insert(0, '/backend')

from app.services.processor import parse_query_filters, encode_text
from app.db import fetch_all_embeddings
import numpy as np

query = "navy long sleeve"
print(f"Query: {query}")

# Test filter extraction
filters = parse_query_filters(query)
print(f"Filters extracted: {filters}")

# Test text encoding
query_vector = encode_text(query)
print(f"Query embedding shape: {query_vector.shape}")

# Test embedding retrieval
records = fetch_all_embeddings()
print(f"Total images with embeddings: {len(records)}")

# Show first image
if records:
    first = records[0]
    print(f"\nFirst image: ID={first['id']}, color={first['color']}, sleeve={first['sleeve_type']}")
    print(f"Embedding size: {len(first['vector'])} bytes")
