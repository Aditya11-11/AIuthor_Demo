import chromadb
import os
import uuid
from google import genai
from google.genai import types

class RAGSystem:
    def __init__(self, collection_name="book_research"):
        self.client = chromadb.PersistentClient(path="data/chroma")
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found for RAG embeddings.")
        self.genai_client = genai.Client(api_key=api_key)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        
    def embed_text(self, text: str, task_type: str = "RETRIEVAL_DOCUMENT") -> list:
        """Get embeddings using Gemini."""
        response = self.genai_client.models.embed_content(
            model="gemini-embedding-001",
            contents=text,
            config=types.EmbedContentConfig(task_type=task_type)
        )
        return response.embeddings[0].values

    def add_text(self, text: str, metadata: dict = None, id: str = None):
        """embed and store a single piece of text."""
        if not id:
            id = str(uuid.uuid4())
        embedding = self.embed_text(text)
        self.collection.add(
            documents=[text],
            metadatas=[metadata] if metadata else [{}],
            ids=[id],
            embeddings=[embedding]
        )

    def add_documents(self, documents: list, metadatas: list, ids: list):
        embeddings = []
        for doc in documents:
            embeddings.append(self.embed_text(doc))
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings
        )

    def query(self, query_text: str, top_k: int = 7):
        query_embeddings = self.embed_text(query_text, task_type="RETRIEVAL_QUERY")
        results = self.collection.query(
            query_embeddings=[query_embeddings],
            n_results=top_k
        )
        return results
