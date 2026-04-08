from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import uuid
import logging

logger = logging.getLogger(__name__)

class QdrantStore:
    def __init__(self, collection_name="fitness_knowledge", host="localhost", port=6333):
        self.collection_name = collection_name
        self.client = QdrantClient(host=host, port=port)
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.vector_size = self.embedding_model.get_sentence_embedding_dimension()
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        try:
            collections = self.client.get_collections().collections
            if not any(c.name == self.collection_name for c in collections):
                logger.info(f"Creating collection {self.collection_name}")
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE),
                )
            else:
                logger.info(f"Collection {self.collection_name} already exists")
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant or get collections: {e}")

    def store_chunks(self, chunks, metadatas):
        points = []
        for chunk, metadata in zip(chunks, metadatas):
            embedding = self.embedding_model.encode(chunk).tolist()
            point_id = str(uuid.uuid4())
            payload = {"text": chunk, "metadata": metadata}
            points.append(PointStruct(id=point_id, vector=embedding, payload=payload))
        
        if points:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            logger.info(f"Stored {len(points)} chunks in Qdrant")

    def search(self, query, top_k=5):
        query_vector = self.embedding_model.encode(query).tolist()
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k
        )
        return results
