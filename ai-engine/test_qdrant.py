import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv()
url = os.getenv("QDRANT_URL_ENDPOINT")
api_key = os.getenv("QDRANT_API_KEY")

print("Testing with original URL:", url)
try:
    c1 = QdrantClient(url=url, api_key=api_key)
    print("c1 collections:", c1.get_collections())
except Exception as e:
    print("c1 failed:", e)

url_port = url + ":6333" if not url.endswith("6333") else url
print("\nTesting with URL + port 6333:", url_port)
try:
    c2 = QdrantClient(url=url_port, api_key=api_key)
    print("c2 collections:", c2.get_collections())
except Exception as e:
    print("c2 failed:", e)

print("\nTesting with url as url param directly")
try:
    c3 = QdrantClient(url, api_key=api_key)
    print("c3 collections:", c3.get_collections())
except Exception as e:
    print("c3 failed:", e)

