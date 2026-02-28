import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any
from langchain_core.documents import Document

class VectorDatabase:
    def __init__(self, collection_name: str = "feedback_vectors"):
        self.collection_name = collection_name
        
        url = os.getenv("QDRANT_URL_ENDPOINT")
        api_key = os.getenv("QDRANT_API_KEY")

        if url and api_key:
            print(f"🚀 Connecting to Qdrant Cloud: {url}...")
            self.client = QdrantClient(url=url, api_key=api_key)
        else:
            print("⚠️ No Credentials found. Using In-Memory Qdrant.")
            self.client = QdrantClient(":memory:")
        
        # Ensure collection exists
        self._create_collection_if_not_exists()

    def _create_collection_if_not_exists(self):
        collections = self.client.get_collections()
        if self.collection_name not in [c.name for c in collections.collections]:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=384,
                    distance=models.Distance.COSINE
                )
            )
            print(f"✅ Collection '{self.collection_name}' created.")
        
        # Create payload index for 'type' (safe to call even if exists)
        self.client.create_payload_index(
            collection_name=self.collection_name,
            field_name="type",
            field_schema=models.PayloadSchemaType.KEYWORD
        )

    def upsert_documents(self, documents: List[Document], embeddings: List[List[float]]):
        points = []
        for i, (doc, vector) in enumerate(zip(documents, embeddings)):
            points.append(
                models.PointStruct(
                    id=i,  # Simple integer ID for MVP. Use UUID in prod.
                    vector=vector,
                    payload={
                        "content": doc.page_content,
                        **doc.metadata
                    }
                )
            )
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search(self, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit
        ).points
        return [
            {
                "score": hit.score,
                "content": hit.payload.get("content"),
                "metadata": {k:v for k,v in hit.payload.items() if k != "content"}
            }
            for hit in results
        ]

    def scroll_by_metadata(self, key: str, value: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Scrolls through the collection to find points matching a metadata filter.
        Returns a list of payload dictionaries.
        """
        filter_condition = models.Filter(
            must=[
                models.FieldCondition(
                    key=key,
                    match=models.MatchValue(value=value)
                )
            ]
        )
        
        # Use scroll to get points
        # Note: scroll returns (points, next_page_offset). 
        # For this MVP, we just get the first page/batch defined by limit.
        points, _ = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=filter_condition,
            limit=limit,
            with_payload=True,
            with_vectors=False
        )
        
        return [p.payload for p in points]
