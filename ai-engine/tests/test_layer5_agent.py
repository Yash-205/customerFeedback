import sys
import os
from langchain_core.messages import HumanMessage

# Ensure app imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.orchestration.graph import app

def test_layer5_agent_live():
    print("\n--- Testing Layer 5: Agentic Orchestration (Live) ---")
    
    if not os.getenv("GROQ_API_KEY"):
        print("⚠️ No GROQ_API_KEY found. Skipping live test.")
        return

    # 1. Test Global/Vector Query
    query1 = "What are the main issues users are reporting about the SuperApp?"
    print(f"\nQUERY 1: '{query1}'")
    
    inputs = {"messages": [HumanMessage(content=query1)]}
    
    # Stream capability allows us to see steps
    print("Agent Reasoning Trace:")
    for output in app.stream(inputs):
        for key, value in output.items():
            print(f"--- Node: {key} ---")
            # print(value) # Full state dump (noisy)
            if key == "agent":
                last_msg = value["messages"][-1]
                if last_msg.tool_calls:
                    print(f"🛠️  Agent decided to call: {last_msg.tool_calls[0]['name']}")
                else:
                    print(f"🤖 Agent Answer: {last_msg.content[:100]}...")

    # 2. Test Graph Query
    query2 = "Which users mentioned 'Sync delays'?"
    print(f"\nQUERY 2: '{query2}'")
    
    inputs2 = {"messages": [HumanMessage(content=query2)]}
    for output in app.stream(inputs2):
        for key, value in output.items():
            if key == "agent":
                last_msg = value["messages"][-1]
                if last_msg.tool_calls:
                    print(f"🛠️  Agent decided to call: {last_msg.tool_calls[0]['name']}")

    print("\n✅ Agent Test Complete.")

if __name__ == "__main__":
    test_layer5_agent_live()
