from typing import List
from app.memory.vector.client import VectorDatabase
from app.processing.rlm_agent import RLMFeedbackAnalyzer

class GlobalAggregator:
    def __init__(self):
        self.vector_db = VectorDatabase()
        self.rlm = RLMFeedbackAnalyzer()

    def run_aggregation(self) -> str:
        """
        Fetches all Level 1 summaries and aggregates them into a Global Theme Report.
        """
        print("🔍 Fetching Level 1 Summaries from Qdrant...")
        
        # Use precise metadata filtering to get Level 1 Summaries
        summaries = self.vector_db.scroll_by_metadata(
            key="type", 
            value="summary", 
            limit=100
        )
        
        if not summaries:
            print("⚠️ No Level 1 summaries found to aggregate.")
            return "No data."

        print(f"✅ Found {len(summaries)} summaries. Aggregating...")
        
        # Prepare data for new RLM analyzer
        feedback_data = [
            {
                'content': s.get('content', ''),
                'rating': s.get('rating', 3.0),
                'source': s.get('source', 'summary-store'),
                'timestamp': s.get('timestamp')
            }
            for s in summaries
        ]
        
        analysis = self.rlm.analyze(feedback_data)
        global_report = analysis.get('hierarchical_summary', 'Aggregation failed.')
        
        print("\n" + "="*40)
        print("🌍 GLOBAL THEMES REPORT 🌍")
        print("="*40)
        print(global_report)
        print("="*40 + "\n")
        
        return global_report

if __name__ == "__main__":
    aggregator = GlobalAggregator()
    aggregator.run_aggregation()
