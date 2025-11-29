from app.services.processor import TAXONOMY
print("✅ Taxonomy loaded from taxonomy.json (not hardcoded)")
print(f"Categories: {list(TAXONOMY.keys())}")
print(f"Sample - Colors: {TAXONOMY['color']}")
