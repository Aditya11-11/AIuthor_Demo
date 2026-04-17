import chromadb
from chromadb.utils import embedding_functions
import os

class RAGSystem:
    def __init__(self, collection_name="book_research"):
        self.client = chromadb.PersistentClient(path="data/chroma")
        # Use default embedding function for now
        self.ef = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name=collection_name, 
            embedding_function=self.ef
        )

    def add_documents(self, documents: list, metadatas: list, ids: list):
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, query_text: str, top_k: int = 5):
        results = self.collection.query(
            query_texts=[query_text],
            n_results=top_k
        )
        return results
