from fastapi import APIRouter, HTTPException
from app.api.schemas import ChatRequest
from app.orchestration.graph import app as agent_app
from langchain_core.messages import HumanMessage
import traceback

router = APIRouter()

@router.post("/chat")
def chat_with_agent(request: ChatRequest):
    """
    Ask the AI Agent a question.
    """
    try:
        # Initialize full AgentState to avoid missing key errors in LangGraph
        content = request.question
        inputs = {
            "messages": [HumanMessage(content=content)],
            "question": content,
            "steps": []
        }
        
        print(f"🤖 Agent invoking for question: {content[:50]}...")
        result = agent_app.invoke(inputs)
        
        # Guard against empty messages or unexpected return structure
        if not result or 'messages' not in result or not result['messages']:
            print(f"⚠️ Unexpected agent result: {result}")
            return {"answer": "I'm sorry, I couldn't process that. The analysis engine returned an empty result.", "trace": []}

        last_msg = result['messages'][-1]
        return {
            "answer": last_msg.content, 
            "trace": [m.content for m in result['messages'] if getattr(m, 'type', '') == 'ai']
        }
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Chat Error: {error_msg}")
        traceback.print_exc()
        
        if "429" in error_msg or "Rate limit" in error_msg or "rate_limit" in error_msg:
             raise HTTPException(status_code=429, detail=error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
