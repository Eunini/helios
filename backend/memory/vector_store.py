"""Vector store integration with Chroma for semantic search."""

import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime
import chromadb
from chromadb.config import Settings as ChromaSettings
from core.logger import setup_logger
from core.config import get_settings

logger = setup_logger(__name__)


class VectorStore:
    """Chroma vector store wrapper for business memory."""

    def __init__(self):
        """Initialize Chroma client and collection."""
        settings = get_settings()
        
        # Initialize Chroma client
        self.client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
        
        logger.info(f"Vector store initialized with collection: {settings.CHROMA_COLLECTION_NAME}")

    def add_document(
        self,
        content: str,
        metadata: Dict[str, Any],
        doc_id: Optional[str] = None,
    ) -> str:
        """
        Add a document to the vector store.

        Args:
            content: Document text content
            metadata: Document metadata
            doc_id: Optional document ID (auto-generated if not provided)

        Returns:
            Document ID
        """
        if not doc_id:
            doc_id = str(uuid.uuid4())

        try:
            self.collection.add(
                ids=[doc_id],
                documents=[content],
                metadatas=[{**metadata, "added_at": datetime.utcnow().isoformat()}],
            )
            logger.debug(f"Added document {doc_id} to vector store")
            return doc_id
        except Exception as e:
            logger.error(f"Error adding document: {e}")
            raise

    def search(
        self,
        query: str,
        n_results: int = 5,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents.

        Args:
            query: Search query text
            n_results: Number of results to return
            filters: Optional metadata filters

        Returns:
            List of matching documents with metadata
        """
        try:
            where = filters if filters else None
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where,
            )

            # Format results
            documents = []
            for i in range(len(results["ids"][0])):
                documents.append({
                    "id": results["ids"][0][i],
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i] if results["distances"] else None,
                })

            return documents
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            return []

    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific document by ID."""
        try:
            results = self.collection.get(ids=[doc_id])
            if results["ids"]:
                return {
                    "id": results["ids"][0],
                    "content": results["documents"][0],
                    "metadata": results["metadatas"][0],
                }
            return None
        except Exception as e:
            logger.error(f"Error getting document {doc_id}: {e}")
            return None

    def update_document(
        self,
        doc_id: str,
        content: str,
        metadata: Dict[str, Any],
    ) -> bool:
        """Update an existing document."""
        try:
            self.collection.update(
                ids=[doc_id],
                documents=[content],
                metadatas=[{**metadata, "updated_at": datetime.utcnow().isoformat()}],
            )
            logger.debug(f"Updated document {doc_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating document {doc_id}: {e}")
            return False

    def delete_document(self, doc_id: str) -> bool:
        """Delete a document from the vector store."""
        try:
            self.collection.delete(ids=[doc_id])
            logger.debug(f"Deleted document {doc_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting document {doc_id}: {e}")
            return False

    def search_by_type(
        self,
        doc_type: str,
        query: Optional[str] = None,
        n_results: int = 10,
    ) -> List[Dict[str, Any]]:
        """Search documents by type."""
        filters = {"type": {"$eq": doc_type}} if doc_type else None
        if query:
            return self.search(query, n_results=n_results, filters=filters)
        
        try:
            results = self.collection.get(where=filters)
            documents = []
            for i in range(len(results["ids"])):
                documents.append({
                    "id": results["ids"][i],
                    "content": results["documents"][i],
                    "metadata": results["metadatas"][i],
                })
            return documents
        except Exception as e:
            logger.error(f"Error searching by type {doc_type}: {e}")
            return []

    def clear_collection(self) -> bool:
        """Clear all documents from the collection (for testing/reset)."""
        try:
            # Get all document IDs
            all_docs = self.collection.get()
            if all_docs["ids"]:
                self.collection.delete(ids=all_docs["ids"])
            logger.info("Vector store collection cleared")
            return True
        except Exception as e:
            logger.error(f"Error clearing collection: {e}")
            return False


# Singleton instance
_vector_store: Optional[VectorStore] = None


def get_vector_store() -> VectorStore:
    """Get or create vector store instance."""
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store
