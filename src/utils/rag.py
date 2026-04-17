import chromadb
import os
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

    def add_documents(self, documents: list, metadatas: list, ids: list):
        embeddings = []
        for doc in documents:
            res = self.genai_client.models.embed_content(
                model="text-embedding-004",# this is latest embedding model for text only is require multilanguage change this to text-multilanual-embedding-002
                contents=doc,
                config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
            )
            embeddings.append(res.embeddings[0].values)
            
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings
        )

    def query(self, query_text: str, top_k: int = 7):
        res = self.genai_client.models.embed_content(
            model="text-embedding-004", # same for multilingual query
            contents=query_text,
            config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY")
        )
        query_embeddings = res.embeddings[0].values
        
        results = self.collection.query(
            query_embeddings=[query_embeddings],
            n_results=top_k
        )
        return results
