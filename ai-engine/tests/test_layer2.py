import sys
import os

# Add the parent directory to sys.path so we can import 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.processing.ingestor import IngestionService
from app.api.schemas import NormalizedFeedback
from datetime import datetime
import time

def test_layer2_ingestion():
    print("\n--- Testing Layer 2: Ingestion & Vector Search ---")
    
    # 1. Initialize Service
    try:
        service = IngestionService()
        print("✅ Ingestion Service Initialized (Qdrant + SentenceTransformer)")
    except Exception as e:
        print(f"❌ Initialization Failed: {e}")
        return

    # 2. Create Dummy Data (Long text to test chunking)
    long_review = "I bought this phone last week. " * 20 + "The battery life is terrible. It dies in 2 hours." + "I bought this phone last week. " * 20
    
    feedback_items = [
        NormalizedFeedback(
            source="amazon",
            content=long_review,
            timestamp=datetime.now(),
            rating=1,
            metadata={"Category": "Electronics", "User": "TestUser"}
        ),
        NormalizedFeedback(
            source="reddit",
            content="Just got the new update. The UI is amazing!",
            timestamp=datetime.now(),
            rating=5,
            metadata={"Subreddit": "technology"}
        )
    ]

    # 3. Ingest Data
    print(f"\nIngesting {len(feedback_items)} items...")
    start_time = time.time()
    num_chunks = service.ingest(feedback_items)
    print(f"✅ Ingested {num_chunks} chunks in {time.time() - start_time:.2f}s")

    # 4. Test Semantic Search
    query = "battery issues"
    print(f"\nSearching for: '{query}'")
    results = service.search(query, limit=1)

    if results:
        top_match = results[0]
        print("✅ Found match!")
        print(f"Score: {top_match['score']:.4f}")
        print(f"Content Preview: {top_match['content'][:100]}...")
        print(f"Metadata: {top_match['metadata']}")
        
        # Verify correctness
        assert "battery" in top_match['content'].lower() or "dies" in top_match['content'].lower()
        assert top_match['metadata']['Category'] == "Electronics"
        print("✅ Semantic Search Verified: 'Battery' query found key sentence & preserved metadata.")
    else:
        print("❌ No results found.")

if __name__ == "__main__":
    test_layer2_ingestion()
