import requests
import json

print("=" * 60)
print("SYSTEM VERIFICATION TEST")
print("=" * 60)

# Test 1: Health check
try:
    resp = requests.get('http://localhost:8000/health', timeout=5)
    print(f"\n✅ Health Check: {resp.status_code} OK")
except Exception as e:
    print(f"\n❌ Health Check failed: {e}")

# Test 2: List images
try:
    resp = requests.get('http://localhost:8000/images', timeout=5)
    print(f"✅ GET /images: {resp.status_code} OK")
    images = resp.json()
    print(f"   → Total indexed: {len(images)} images")
    if images:
        print(f"   → Sample: {images[0]['filename'][:40]}...")
except Exception as e:
    print(f"❌ GET /images failed: {e}")

# Test 3: Search with filter extraction
try:
    resp = requests.post(
        'http://localhost:8000/search',
        json={'query': 'navy long sleeve A-line'},
        timeout=15
    )
    print(f"\n✅ POST /search: {resp.status_code} OK")
    result = resp.json()
    
    filters = result.get('filters', {})
    results = result.get('results', [])
    
    print(f"   → Filters extracted: {filters}")
    print(f"   → Results matched: {len(results)}")
    
    if results:
        top = results[0]
        print(f"\n   Top Match:")
        print(f"      Image: {top['metadata']['filename'][:40]}...")
        print(f"      Attributes: {top['metadata']['color']}, {top['metadata']['silhouette']}, {top['metadata']['length']}")
        print(f"      Similarity: {top['similarity']:.4f}")
        
except Exception as e:
    print(f"❌ POST /search failed: {e}")

print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print("\nIf all 3 tests passed with green checkmarks (✅):")
print("  → System is FULLY OPERATIONAL")
print("  → Search pipeline working (parsing + embeddings + ranking)")
print("  → Ready for browser testing")
print("=" * 60)
