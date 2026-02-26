import dspy
from dspy.predict.rlm import RLM
from typing import List, Dict, Any

import numpy as np
from sklearn.cluster import AgglomerativeClustering
import os
# ========================================================================
# DSPy Signatures for RLM
# ========================================================================

class FeedbackAnalysisSignature(dspy.Signature):
    """Analyze customer feedback using Python code to extract hierarchical insights.
    
    You have access to helper functions:
    - group_by_similarity(texts, threshold) -> groups similar feedback
    - extract_themes(texts) -> identifies common themes
    - summarize_batch(texts) -> summarizes a list of feedback
    
    Your task is to write Python code that:
    1. Groups feedback by themes/topics
    2. Recursively summarizes each group
    3. Builds a hierarchical understanding
    4. Returns structured insights
    """
    
    feedback_items = dspy.InputField(
        desc="List of dicts with keys: content, rating, source, timestamp"
    )
    analysis = dspy.OutputField(
        desc="Dict with keys: themes (list), critical_issues (list), sentiment (str), hierarchical_summary (str)"
    )

# ========================================================================
# Helper Tools for RLM
# ========================================================================

class RLMHelperTools:
    """Helper functions that dspy.RLM can use for feedback analysis."""
    
    def __init__(self):
        pass
        
    def _get_embedding_model(self):
        import torch
        from sentence_transformers import SentenceTransformer
        if not hasattr(self, '_embedding_model'):
            print("⏳ Loading embedding model into memory (RLM_Agent)...")
            torch.set_num_threads(1)
            self._embedding_model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
        return self._embedding_model
    
    def group_by_similarity(self, texts: List[str], threshold: float = 0.7) -> List[List[str]]:
        """Group similar texts using hierarchical clustering.
        
        Args:
            texts: List of text strings to group
            threshold: Similarity threshold (0-1, higher = more similar required)
            
        Returns:
            List of groups, where each group is a list of similar texts
        """
        if not texts or len(texts) == 1:
            return [texts]
        
        # Generate embeddings
        model = self._get_embedding_model()
        embeddings = model.encode(texts)
        
        # Hierarchical clustering
        clustering = AgglomerativeClustering(
            n_clusters=None,
            distance_threshold=1 - threshold,
            metric='cosine',
            linkage='average'
        )
        labels = clustering.fit_predict(embeddings)
        
        # Group texts by cluster
        groups = {}
        for idx, label in enumerate(labels):
            if label not in groups:
                groups[label] = []
            groups[label].append(texts[idx])
        
        return list(groups.values())
    
    def extract_themes(self, texts: List[str], max_themes: int = 5) -> List[str]:
        """Extract common themes from a list of texts using keyword extraction.
        
        Args:
            texts: List of feedback texts
            max_themes: Maximum number of themes to extract
            
        Returns:
            List of theme keywords
        """
        # Simple keyword extraction (in production, use more sophisticated NLP)
        from collections import Counter
        import re
        
        # Combine all texts
        combined = " ".join(texts).lower()
        
        # Extract words (simple tokenization)
        words = re.findall(r'\b[a-z]{4,}\b', combined)
        
        # Common stop words to filter
        stop_words = {'that', 'this', 'with', 'from', 'have', 'been', 'were', 'would', 'could', 'should'}
        words = [w for w in words if w not in stop_words]
        
        # Get most common
        counter = Counter(words)
        themes = [word for word, count in counter.most_common(max_themes)]
        
        return themes
    
    def summarize_batch(self, texts: List[str]) -> str:
        """Summarize a batch of feedback texts using DSPy.
        
        Args:
            texts: List of feedback texts to summarize
            
        Returns:
            Summary string
        """
        # Use simple DSPy Predict for summarization
        class SimpleSummary(dspy.Signature):
            """Summarize customer feedback into key points."""
            feedback = dspy.InputField()
            summary = dspy.OutputField()
        
        summarizer = dspy.Predict(SimpleSummary)
        combined = "\n".join(texts[:10])  # Limit to avoid token overflow
        
        try:
            result = summarizer(feedback=combined)
            return result.summary
        except Exception as e:
            return f"Summary of {len(texts)} feedback items: {texts[0][:100]}..."

# ========================================================================
# RLM Feedback Analyzer
# ========================================================================

class RLMFeedbackAnalyzer:
    """Main RLM-based feedback analyzer using dspy.RLM for code-based reasoning."""
    
    def __init__(self, model_name: str = "llama-3.1-8b-instant"):
        # Configure DSPy with Groq using dspy.LM
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment")
        
        print("🚀 Initializing dspy.LM with Groq...")
        self.lm = dspy.LM(model=f"groq/{model_name}", api_key=api_key)
        dspy.settings.configure(lm=self.lm)
        
        # Initialize helper tools
        self.tools = RLMHelperTools()
        
        # Initialize RLM with signature string (not class)
        print("🧠 Initializing dspy.RLM...")
        self.rlm = RLM(
            signature="feedback_items -> analysis",
            max_iterations=10
        )
    
    def analyze(self, feedback_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze feedback using RLM code-based reasoning.
        
        Args:
            feedback_items: List of feedback dicts with content, rating, source, timestamp
            
        Returns:
            Analysis dict with themes, issues, sentiment, hierarchical_summary
        """
        print(f"🔍 RLM analyzing {len(feedback_items)} feedback items...")
        
        try:
            # RLM will write Python code to analyze the feedback
            result = self.rlm(feedback_items=feedback_items)
            
            print("✅ RLM analysis complete!")
            print(f"📊 Trajectory: {len(result.trajectory)} steps")
            
            return result.analysis
        
        except Exception as e:
            print(f"❌ RLM analysis failed: {e}")
            # Fallback to simple analysis
            return self._fallback_analysis(feedback_items)
    
    def _fallback_analysis(self, feedback_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fallback analysis if RLM fails."""
        texts = [item.get('content', '') for item in feedback_items]
        themes = self.tools.extract_themes(texts)
        
        return {
            'themes': themes,
            'critical_issues': themes[:3],
            'sentiment': 'mixed',
            'hierarchical_summary': f"Analysis of {len(feedback_items)} items. Top themes: {', '.join(themes[:3])}"
        }
