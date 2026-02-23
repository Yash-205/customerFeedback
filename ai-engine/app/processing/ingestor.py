from typing import List, Dict
from collections import defaultdict
from langchain_core.documents import Document
from sentence_transformers import SentenceTransformer
from app.api.schemas import NormalizedFeedback
from app.processing.chunker import FeedbackChunker
from app.memory.vector.client import VectorDatabase
from app.processing.rlm_agent import RLMFeedbackAnalyzer  # Using dspy.RLM
from app.memory.graph.client import Neo4jClient

class IngestionService:
    def __init__(self):
        self.chunker = FeedbackChunker()
        self.vector_db = VectorDatabase()
        self.rlm = RLMFeedbackAnalyzer()  # Using dspy.RLM for code-based analysis
        self.graph_db = Neo4jClient()
        # Load local embedding model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def ingest(self, feedback_items: List[NormalizedFeedback]):
        # 1. Chunking
        documents = self.chunker.chunk_feedback(feedback_items)
        if not documents:
            return {"chunk_count": 0}
            
        print(f"Split {len(feedback_items)} feedback items into {len(documents)} chunks.")

        
        # 2. RLM Analysis (Layer 3) - NEW APPROACH
        print(f"🧠 RLM analyzing {len(feedback_items)} feedback items...")
        
        # Prepare feedback data for RLM
        feedback_data = [
            {
                'content': item.content,
                'rating': item.rating,
                'source': item.source,
                'timestamp': item.timestamp.isoformat() if item.timestamp else None
            }
            for item in feedback_items
        ]
        
        try:
            # RLM will write Python code to hierarchically analyze feedback
            rlm_analysis = self.rlm.analyze(feedback_data)
            
            print(f"✅ RLM Analysis Complete:")
            print(f"   Themes: {rlm_analysis.get('themes', [])}")
            print(f"   Critical Issues: {rlm_analysis.get('critical_issues', [])}")
            
            # Create a single hierarchical summary document
            hierarchical_summary = rlm_analysis.get('hierarchical_summary', '')
            if hierarchical_summary:
                summary_doc = Document(
                    page_content=hierarchical_summary,
                    metadata={
                        'type': 'rlm_summary',
                        'level': 'hierarchical',
                        'total_items': len(feedback_items),
                        'themes': rlm_analysis.get('themes', []),
                        'critical_issues': rlm_analysis.get('critical_issues', []),
                        'sentiment': rlm_analysis.get('sentiment', 'unknown')
                    }
                )
                summary_documents = [summary_doc]
                
                # --- LAYER 4: GRAPH STORAGE ---
                # Extract entities from RLM analysis
                print(f"🕸️ Storing RLM insights in graph...")
                entities = [
                    {'name': theme, 'type': 'Theme', 'sentiment': 'neutral'}
                    for theme in rlm_analysis.get('themes', [])
                ] + [
                    {'name': issue, 'type': 'Issue', 'sentiment': 'negative'}
                    for issue in rlm_analysis.get('critical_issues', [])
                ]
                
                if entities:
                    self.graph_db.store_summary_intelligence(
                        hierarchical_summary,
                        summary_doc.metadata,
                        entities
                    )
                # ------------------------------
        
        except Exception as e:
            print(f"❌ RLM analysis failed: {e}")
            print("   Falling back to no summarization...")
            summary_documents = []

        # 3. Embedding & Storage (Mix of Raw Chunks + Summaries)
        all_docs = documents + summary_documents
        print(f"Upserting {len(documents)} chunks + {len(summary_documents)} summaries...")
        
        texts = [doc.page_content for doc in all_docs]
        embeddings = self.model.encode(texts).tolist()

        self.vector_db.upsert_documents(all_docs, embeddings)
        
        return {
            "chunk_count": len(documents),
            "summary_count": len(summary_documents),
            "themes": rlm_analysis.get('themes', []) if 'rlm_analysis' in locals() else [],
            "critical_issues": rlm_analysis.get('critical_issues', []) if 'rlm_analysis' in locals() else [],
            "hierarchical_summary": rlm_analysis.get('hierarchical_summary', '') if 'rlm_analysis' in locals() else "",
            "entities_count": len(entities) if 'entities' in locals() else 0
        }

    def search(self, query: str, limit: int = 5):
        query_vector = self.model.encode([query])[0].tolist()
        return self.vector_db.search(query_vector, limit)
