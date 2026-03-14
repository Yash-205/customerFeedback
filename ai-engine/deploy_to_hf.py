import os
from huggingface_hub import HfApi

# Configuration
REPO_ID = "Yash205/Customer_Intelligent_Engine"
REPO_TYPE = "space"
FOLDER_TO_UPLOAD = "." # Current directory (ai-engine)

api = HfApi()

print(f"🚀 Deploying '{FOLDER_TO_UPLOAD}' to Hugging Face Space: {REPO_ID}...")

try:
    # Upload the folder
    api.upload_folder(
        folder_path=FOLDER_TO_UPLOAD,
        repo_id=REPO_ID,
        repo_type=REPO_TYPE,
        commit_message="Deploying AI Engine with Qdrant Fallback Fix",
        ignore_patterns=["venv/*", "__pycache__/*", ".git/*", ".env", "*.pyc"]
    )
    print("✅ Deployment triggered successfully!")
    print(f"Check your Hugging Face Space to see the build progress: https://huggingface.co/spaces/{REPO_ID}")
except Exception as e:
    print(f"❌ Deployment failed: {e}")
