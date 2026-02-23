import sys
import os

# Ensure app imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.processing.ingestor import IngestionService
from app.api.schemas import NormalizedFeedback
from app.memory.graph.client import Neo4jClient
from datetime import datetime
import time

def test_layer4_graph_live():
    print("\n--- Testing Layer 4: Graph Memory Integration (Live) ---")
    
    if not os.getenv("NEO4J_PASSWORD"):
        print("⚠️ No NEO4J_PASSWORD found. Skipping live test.")
        return

    # 1. Clean Graph (Optional - for test purity, maybe just count before/after)
    # We won't wipe the DB to avoid deleting user data, we'll check for specific new nodes.
    
    service = IngestionService()
    
    # 2. Ingest Feedback with Clear Entities
    content = (
        "I love the new Dark Mode feature on the SuperApp, it saves my eyes at night. "
        "However, the Sync delays are annoying. "
        "I hope the next update fixes the Sync issue."
    )
    
    feedback = NormalizedFeedback(
        source="graph_test",
        content=content,
        timestamp=datetime.now(),
        rating=4.0,
        metadata={"user": "GraphTester01", "product": "SuperApp"}
    )
    
    print("Ingesting feedback...")
    service.ingest([feedback])
    
    # 3. Verify in Neo4j
    print("\nVerifying Graph Nodes...")
    neo = Neo4jClient()
    
    query_user = "MATCH (u:User {id: 'GraphTester01'}) RETURN u"
    query_feature = "MATCH (f:Feature {name: 'Dark Mode'}) RETURN f"
    query_issue = "MATCH (i:Issue) WHERE i.name CONTAINS 'Sync' RETURN i"
    
    with neo.driver.session() as session:
        # Check User
        res = session.run(query_user).single()
        if res:
            print("✅ User 'GraphTester01' found in Graph.")
        else:
            print("❌ User node missing.")

        # Check Entities (Feature/Issue)
        # Note: Extraction depends on LLM, so names might vary slightly ("Dark Mode", "Sync delays").
        # We query loosely.
        
        res_feat = session.run(query_feature).single()
        if res_feat:
            print("✅ Feature 'Dark Mode' found and linked.")
        else:
            print("⚠️ feature 'Dark Mode' not found (LLM might have named it differently).")

        res_iss = session.run(query_issue).single()
        if res_iss:
            print(f"✅ Issue found: {res_iss['i']['name']}")
        else:
            print("⚠️ Sync issue not found.")

    neo.close()

if __name__ == "__main__":
    test_layer4_graph_live()
