from qdrant_store import QdrantStore

class Retriever:
    def __init__(self):
        self.store = QdrantStore()

    def retrieve(self, query, top_k=5):
        """
        Retrieve relevant chunks from Qdrant based on semantic similarity.
        """
        search_results = self.store.search(query, top_k=top_k)
        
        # Format the context
        contexts = []
        for result in search_results:
            text = result.payload.get("text", "")
            metadata = result.payload.get("metadata", {})
            source = metadata.get("source_file", "Unknown")
            contexts.append(f"[Source: {source}]\n{text}")
            
        return search_results, contexts
