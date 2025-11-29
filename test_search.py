import requests
import json
import time

print("Waiting for server...")
time.sleep(1)

print("Testing /health endpoint...")
try:
    resp = requests.get('http://localhost:8000/health', timeout=5)
    print(f"✅ Health: {resp.status_code}")
except Exception as e:
    print(f"❌ Health failed: {e}")
    exit(1)

print("\nTesting /search endpoint...")
try:
    resp = requests.post(
        'http://localhost:8000/search',
        json={'query': 'navy long sleeve'},
        timeout=15
    )
    result = resp.json()
    print(f"✅ Search: {resp.status_code}")
    print(f"   Filters: {result['filters']}")
    print(f"   Results: {len(result['results'])} matches")
    
    if result['results']:
        top = result['results'][0]
        print(f"   Top result: {top['color']} {top['silhouette']} (similarity: {top['similarity']:.3f})")
    else:
        print("   ⚠️  No results found")
except Exception as e:
    print(f"❌ Search failed: {e}")
    exit(1)
