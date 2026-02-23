from fastapi import APIRouter, HTTPException
from app.processing.aggregator import GlobalAggregator

router = APIRouter()
aggregator = GlobalAggregator()

@router.get("/")
def read_root():
    return {"status": "AI Engine Online", "layers_active": [1, 2, 3, 4, 5]}

@router.get("/global-themes")
def get_global_themes():
    """
    Trigger RLM Level 2 Aggregation to get high-level insights.
    """
    try:
        report = aggregator.run_aggregation()
        return {"report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
