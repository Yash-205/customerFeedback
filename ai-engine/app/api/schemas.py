from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class NormalizedFeedback(BaseModel):
    source: str = Field(..., description="The origin platform (e.g., 'amazon', 'reddit', 'app_store')")
    content: str = Field(..., description="The main text body of the feedback")
    timestamp: datetime = Field(..., description="UTC timestamp of when the feedback was created")
    rating: Optional[float] = Field(None, description="Normalized rating (1-5 scale) if applicable")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Platform-specific extra data (e.g., upvotes, verified_purchase)")

    class Config:
        json_schema_extra = {
            "example": {
                "source": "amazon",
                "content": "Great product but battery life is short.",
                "timestamp": "2024-03-12T10:00:00Z",
                "rating": 4.0,
                "metadata": {"verified_purchase": True, "helpful_votes": 12}
            }
        }

class IngestRequest(BaseModel):
    items: List[Dict]  # Flexible dict input for now, normalized inside service if needed

class ChatRequest(BaseModel):
    question: str

