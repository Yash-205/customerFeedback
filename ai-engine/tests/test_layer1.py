from fastapi.testclient import TestClient
from app.api.main import app
import io
import pandas as pd
import json

client = TestClient(app)

def create_dummy_csv(data):
    df = pd.DataFrame(data)
    csv_bytes = df.to_csv(index=False).encode('utf-8')
    return io.BytesIO(csv_bytes)

def test_metadata_preservation():
    print("\n--- Testing Metadata Preservation (Category, Region, etc.) ---")
    data = {
        "User Review": ["Battery life is terrible.", "Love the new design."],
        "Date": ["2024-01-01", "2024-01-02"],
        "Rating": [1, 5],
        # These are the columns the user is worried about missing:
        "Category": ["Electronics", "Fashion"],
        "Product ID": ["SKU-123", "SKU-456"],
        "User Region": ["US", "EU"],
        "Vip Customer": [True, False]
    }
    csv_file = create_dummy_csv(data)
    
    response = client.post(
        "/api/v1/upload/generic",
        files={"file": ("metadata_test.csv", csv_file, "text/csv")}
    )
    
    if response.status_code == 200:
        print("✅ Success! Data Normalized.")
        output = response.json()
        
        # Verify first item
        item = output[0]
        print("\n--- Normalized Item Structure ---")
        print(f"Content:   {item['content']}")
        print(f"Timestamp: {item['timestamp']}")
        print(f"Rating:    {item['rating']}")
        print(f"Metadata:  {json.dumps(item['metadata'], indent=2)}")
        
        # Assertion: Ensure metadata contains the extra columns
        assert item['metadata']['Category'] == "Electronics"
        assert item['metadata']['Product ID'] == "SKU-123"
        assert item['metadata']['User Region'] == "US"
        print("\n✅ Verification: 'Category', 'Product ID', etc. are SAFELY stored in metadata!")
    else:
        print(f"❌ Failed: {response.text}")

if __name__ == "__main__":
    try:
        test_metadata_preservation()
    except Exception as e:
        print(f"❌ Error: {e}")
