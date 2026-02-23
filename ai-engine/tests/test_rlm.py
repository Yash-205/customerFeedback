from unittest.mock import MagicMock
import sys
import os

# Ensure app imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock dspy first to avoid requiring API keys for this test
import dspy
from app.abilities.summarization import SummarizationSignature, RecursiveSummarizationSignature
from app.processing.rlm import RecursiveSummarizer

def test_recursive_summarization_mock():
    print("\n--- Testing Layer 3: Recursive Summarization (RLM) ---")

    # 1. Initialize RLM (Mocked)
    rlm = RecursiveSummarizer(model_name="openai/gpt-4o-mini")
    
    # Mock the internal DSPy modules
    # Simulates Level 1 returns a short summary
    rlm.summarizer = MagicMock()
    rlm.summarizer.return_value.summary = "Level 1 Summary: Found issues with X."
    
    # Simulates Level 2+ returns a combined summary
    rlm.recursive_summarizer = MagicMock()
    rlm.recursive_summarizer.return_value.meta_summary = "Level 2 Summary: Combined complaints about X and Y."

    # 2. Create Dummy Chunks
    # 7 chunks. Batch size 5. Should result in 2 batches -> 2 Level 1 summaries -> 1 Final summary.
    chunks = [f"Chunk {i}" for i in range(7)]
    
    # 3. Predict the Flow
    # Expected: 
    # Batch 1 (Chunk 0-4) -> L1 Summary A
    # Batch 2 (Chunk 5-6) -> L1 Summary B
    # Recursion (L1 A + L1 B) -> Final Summary
    
    # We test the public method? Actually the public method 'recursive_summarize' expects *summaries* as input
    # wait, the logic in rlm.py is:
    # summarize_chunk_batch(chunks) -> str
    # recursive_summarize(summaries) -> str
    
    # So we need a wrapper function or test the logic flow manually?
    # Let's test `recursive_summarize` directly with a list of "Level 1 summaries"
    
    level_1_summaries = [f"Summary {i}" for i in range(7)]
    print(f"Input: {len(level_1_summaries)} Level 1 summaries.")
    
    final_insight = rlm.recursive_summarize(level_1_summaries, batch_size=5)
    
    print(f"Output: {final_insight}")
    
    # Verification
    # Logic: 7 items, batch 5.
    # Round 1: [Sum 0-4] -> New Sum 1. [Sum 5-6] -> New Sum 2.
    # Round 2: [New Sum 1, New Sum 2] -> Final Sum.
    # Total calls to recursive_summarizer should be 3 (2 in Round 1, 1 in Round 2).
    
    call_count = rlm.recursive_summarizer.call_count
    print(f"Recursion Steps (LLM Calls): {call_count}")
    
    if call_count == 3:
        print("✅ Recursion Logic Verified: Correctly batched and reduced 7 items to 1.")
    else:
        print(f"❌ Recursion Logic Failed: Expected 3 calls, got {call_count}.")

if __name__ == "__main__":
    try:
        test_recursive_summarization_mock()
    except ImportError:
        print("❌ Error: DSPy not installed. Please run 'pip install dspy-ai'.")
    except Exception as e:
        print(f"❌ Error: {e}")
