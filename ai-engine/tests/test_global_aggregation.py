import sys
import os

# Ensure app imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.processing.aggregator import GlobalAggregator
from app.memory.vector.client import VectorDatabase
from langchain_core.documents import Document
from sentence_transformers import SentenceTransformer
import time

def test_global_aggregation_live():
    print("\n--- Testing Layer 3 Level 2: Global Aggregation (Live) ---")
    
    if not os.getenv("GROQ_API_KEY"):
        print("⚠️ No GROQ_API_KEY found. Skipping live test.")
        return

    # 1. Setup Data
    print("Preparing mock Level 1 Summaries in Qdrant...")
    vector_db = VectorDatabase()
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Create 15 mock summaries about "Battery Issues" to force aggregation
    mock_summaries = []
    for i in range(15):
        s_text = f"Summary {i}: User complained about battery draining fast and overheating."
        doc = Document(
            page_content=s_text,
            metadata={
                "type": "summary", 
                "level": "document_summary",
                "mock_id": i
            }
        )
        mock_summaries.append(doc)
    
    # Embed and Upsert
    texts = [d.page_content for d in mock_summaries]
    embeddings = model.encode(texts).tolist()
    vector_db.upsert_documents(mock_summaries, embeddings)
    
    print(f"✅ Upserted {len(mock_summaries)} mock summaries.")
    
    # 2. Run Aggregator
    print("\nStarting Global Aggregator...")
    aggregator = GlobalAggregator()
    report = aggregator.run_aggregation()
    
    # 3. Verification
    print("\n--- Verification ---")
    if "battery" in report.lower() or "overheating" in report.lower():
        print("✅ SUCCESS: Global Report identified the core issue (Battery/Overheating).")
    else:
        print("⚠️ Warning: Global Report might be off-topic. Check content.")
        
    if "Aggregating" in report or "Theme" in report: 
         # Rough check if format is somewhat report-like
         pass

if __name__ == "__main__":
    test_global_aggregation_live()
