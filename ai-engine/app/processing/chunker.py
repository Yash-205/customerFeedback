from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.api.schemas import NormalizedFeedback

class FeedbackChunker:
    def __init__(self, chunk_size: int = 1024, chunk_overlap: int = 200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    def chunk_feedback(self, feedback_items: List[NormalizedFeedback]) -> List[Document]:
        documents = []
        
        for item in feedback_items:
            base_metadata = item.metadata.copy()
            base_metadata.update({
                "source": item.source,
                "timestamp": item.timestamp.isoformat() if item.timestamp else None,
                "rating": item.rating,
                "parent_id": f"{item.source}_{item.timestamp}_{hash(item.content)}" # Simple unique ID logic
            })

            chunks = self.text_splitter.split_text(item.content)
            
            for i, chunk_text in enumerate(chunks):
                chunk_metadata = base_metadata.copy()
                chunk_metadata["chunk_index"] = i
                
                doc = Document(
                    page_content=chunk_text,
                    metadata=chunk_metadata
                )
                documents.append(doc)
                
        return documents
