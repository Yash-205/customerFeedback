import sys
import os
from dotenv import load_dotenv

# Load env variables (including GROQ_API_KEY)
load_dotenv()

# Ensure app imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    import dspy
    from app.processing.rlm import RecursiveSummarizer
except ImportError:
    print("❌ Error: DSPy not installed. Please run 'pip install dspy-ai'.")
    sys.exit(1)

def test_rlm_live_groq():
    print("\n--- Testing RLM with Groq (Live Integration) ---")
    
    # Check for API Key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ Error: GROQ_API_KEY not found in environment variables.")
        return

    # Initialize RLM (Should pick up Groq key automatically)
    try:
        rlm = RecursiveSummarizer(model_name="groq/llama3-70b-8192")
    except Exception as e:
        print(f"❌ Error initializing RLM: {e}")
        return

    print(f"✅ RLM Initialized with LM: {rlm.lm}")
    
    # Test Data: 3 simple chunks
    chunks = [
        "The battery lasts only 4 hours on a full charge. Very disappointing.",
        "Charging is slow, takes forever to get to 100%.",
        "Battery drains even when not in use. Fix this!"
    ]
    
    print(f"\nSummarizing {len(chunks)} chunks...")
    
    try:
        # Step 1: Batch Summarization (Level 1)
        summary = rlm.summarize_chunk_batch(chunks)
        print("\n--- Generated Summary ---")
        print(summary)
        
        if "battery" in summary.lower() or "charge" in summary.lower():
             print("\n✅ Success! The summary captures the battery issues.")
        else:
             print("\n⚠️ Warning: Summary might not be accurate. Check output.")
             
    except Exception as e:
        print(f"\n❌ Error during summarization: {e}")

if __name__ == "__main__":
    test_rlm_live_groq()
