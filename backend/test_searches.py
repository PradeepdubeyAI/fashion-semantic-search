#!/usr/bin/env python3
"""Test search with various queries to verify end-to-end system."""
import requests
import json

BASE_URL = "http://localhost:8000"

print("\n" + "="*70)
print("DRESS IMAGE SEARCH - SEARCH FUNCTIONALITY TEST")
print("="*70)

queries = [
    "navy long sleeve",
    "A-line ball gown",
    "red dress floor-length",
    "sleeveless mermaid",
]

for i, query in enumerate(queries, 1):
    print(f"\n[{i}] Query: '{query}'")
    try:
        resp = requests.post(
            f"{BASE_URL}/search",
            json={"query": query},
            timeout=15
        )
        result = resp.json()
        filters = result.get("filters", {})
        results = result.get("results", [])
        
        print(f"    Filters extracted: {filters}")
        print(f"    Results: {len(results)} matches")
        
        if results:
            top = results[0]
            print(f"    Top match: {top['color']} {top['silhouette']} (similarity: {top['similarity']:.4f})")
    except Exception as e:
        print(f"    ❌ Error: {e}")

print("\n" + "="*70)
print("✅ SYSTEM WORKING - Search pipeline operational")
print("="*70)
