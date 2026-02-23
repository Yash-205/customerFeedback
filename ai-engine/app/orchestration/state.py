from typing import TypedDict, List, Dict, Any, Optional

class AgentState(TypedDict):
    """
    Represents the state of our RLM Agent.
    """
    question: str
    
    # Evidence from different memory layers
    vector_evidence: List[str]      # Layer 2: Raw Chunks
    graph_evidence: List[Dict]      # Layer 4: Entities & Relationships
    global_themes: str              # Layer 3: Global Aggregation
    
    # Reasoning
    steps: List[str]                # Trace of thought
    answer: str                     # Final output
