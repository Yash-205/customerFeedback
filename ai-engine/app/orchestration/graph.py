from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from app.orchestration.state import AgentState
from app.abilities.tools import search_vector_memory, fetch_global_themes, query_graph_memory
import os

# 1. Initialize LLM (Groq)
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    # Use dummy for testing or raise error
    raise ValueError("GROQ_API_KEY not found in environment.")

llm = ChatGroq(
    temperature=0, 
    model_name="llama-3.1-8b-instant",
    api_key=groq_api_key
)

# 2. Define Tools
tools = [search_vector_memory, query_graph_memory, fetch_global_themes]

# 3. Bind Tools to LLM
llm_with_tools = llm.bind_tools(tools)

# 4. Define Nodes
def agent_node(state):
    """
    Invokes the LLM to decide on the next step (tool call or final answer).
    """
    messages = state.get("messages", [])
    if not messages:
        # Initial user query from state['question'] if messages empty
        messages = [
            SystemMessage(content="You are an expert AI Analyst. Use your tools (Vector Search, Graph Query, Global Themes) to answer user questions with evidence."),
            HumanMessage(content=state["question"])
        ]
    
    response = llm_with_tools.invoke(messages)
    return {"messages": [response], "steps": ["Agent Reasoning"]}

# 5. Build Graph
workflow = StateGraph(dict) # Using generic dict for simplicity or AgentState if we map it properly
# Ideally we use MessagesState from langgraph, but let's stick to our custom or simple dict for MVP.

# Actually, to use `tools_condition` and `ToolNode` easily, we should use the standard message graph structure.
from langgraph.graph import MessagesState

class AgentState(MessagesState):
    question: str
    steps: list

workflow = StateGraph(AgentState)

workflow.add_node("agent", agent_node)
workflow.add_node("tools", ToolNode(tools))

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    tools_condition,
)

workflow.add_edge("tools", "agent")

app = workflow.compile()
