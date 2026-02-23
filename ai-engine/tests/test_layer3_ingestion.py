import sys
import os

# Ensure app imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.processing.ingestor import IngestionService
from app.api.schemas import NormalizedFeedback
from datetime import datetime

def test_layer3_ingestion_live():
    print("\n--- Testing Layer 3: RLM Ingestion (Live) ---")
    
    if not os.getenv("GROQ_API_KEY"):
        print("⚠️ No GROQ_API_KEY found. Skipping live test.")
        return

    service = IngestionService()
    
    # 1. Create Dummy Feedback (Long enough to be interesting)
    # 3 sentences about screen issues.
    content = (
        "The screen on this device is terrible. It flickers constantly when brightness is low. "
        "I tried updating the drivers but the flickering persists. "
        "Also, the colors look washed out compared to my old phone. "
        "Very disappointed with the display quality."
    )
    
    feedback = NormalizedFeedback(
        source="manual_test",
        content=content,
        timestamp=datetime.now(),
        rating=2.0,
        metadata={"user": "tester", "product": "DeviceX"}
    )
    
    print("Ingesting feedback...")
    # This should trigger: Chunking -> Summarization -> Embedding -> Upsert
    total_docs = service.ingest([feedback])
    
    print(f"✅ Ingestion complete. Total stored documents: {total_docs}")
    
    # Expectation: 
    # Chunks: Maybe 1 or 2 (depending on length vs 500 chars).
    # Summary: 1.
    # Total should be > 1.
    
    if total_docs > 1:
        print("✅ Verified: Summaries were generated (Total > Chunks).")
    else:
        print("⚠️ Warning: Total docs low. Maybe summary failed?")

    # 2. Verification via Search
    print("\nSearching for 'display quality'...")
    results = service.search("display quality", limit=5)
    
    found_summary = False
    for res in results:
        meta = res.get("metadata", {})
        doc_type = meta.get("type", "chunk")
        score = res.get("score", 0)
        print(f" - [{doc_type}] Score: {score:.3f} | Content: {res['content'][:50]}...")
        
        if doc_type == "summary":
            found_summary = True
            print("   (Found a summary document!)")

    if found_summary:
        print("\n✅ SUCCESS: RLM Summary successfully stored and retrieved!")
    else:
        print("\n⚠️ Warning: No summary document found in top results.")

if __name__ == "__main__":
    test_layer3_ingestion_live()
