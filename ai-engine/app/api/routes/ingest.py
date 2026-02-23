from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.api.schemas import IngestRequest, NormalizedFeedback
from app.processing.ingestor import IngestionService

router = APIRouter()
ingestor = IngestionService()

@router.post("/ingest")
def ingest_feedback(request: IngestRequest):
    """
    Ingest a batch of feedback. 
    Triggers: Chunking -> Vector Embed -> RLM Summarization -> Graph Extraction.
    """
    try:
        norm_items = []
        for item in request.items:
            norm_items.append(
                NormalizedFeedback(
                    source=item.get("source", "api_upload"),
                    content=item.get("content", ""),
                    rating=item.get("rating", 3.0),
                    timestamp=datetime.now(),
                    metadata=item.get("metadata", {})
                )
            )
        
        result = ingestor.ingest(norm_items)
        
        # Return detailed status for frontend display
        return {
            "message": "✅ RLM Analysis Complete!",
            "processed_chunks": result.get("chunk_count", 0),
            "rlm_analysis": {
                "themes": result.get("themes", []),
                "critical_issues": result.get("critical_issues", []),
                "summary": result.get("hierarchical_summary", ""),
                "entities_stored": result.get("entities_count", 0)
            },
            "status": "success"
        }
    
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "Rate limit" in error_msg or "rate_limit" in error_msg:
             print(f"⚠️ Rate Limit Hit: {error_msg}")
             raise HTTPException(status_code=429, detail=error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
