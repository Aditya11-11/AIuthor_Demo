# embedder.py
import os
from math import ceil
from dotenv import load_dotenv
from rag import RAGSystem


class EmbeddingService:
    def __init__(self, rag_system: RAGSystem):
        load_dotenv()
        apikey=os.getenv("OPENAI_API_KEY")
        self.client = rag_system
        self.embedder = OpenAIEmbeddings(openai_api_key=apikey,model="text-embedding-3-large")

        self.MAX_BATCH_SIZE=int(os.getenv("MAX_BATCH_SIZE"))# get branch size
    # def embed_and_store(self, documents: list):
    #     texts = []
    #     ids = []
    #     metadatas = []

    #     for idx, doc in enumerate(documents):
    #         text = doc.get("question", "") + "\n" + doc.get("srchTextMarkup", "")
    #         texts.append(text)
    #         ids.append(str(doc.get("articleId", idx)))
    #         metadatas.append({
    #             "articleId": doc.get("articleId"),
    #             "createdDate": doc.get("createdDate"),
    #             "articleType": doc.get("articleType", "")
    #         })

    #     vectors = self.embedder.embed_documents(texts)
    #     self.client.insert(ids=ids, documents=texts, metadatas=metadatas, embeddings=vectors)
    
    def embed_and_store(self, documents: list):
        texts = []
        ids = []
        metadatas = []

        for idx, doc in enumerate(documents):
            text = doc.get("question", "") + "\n" + doc.get("srchTextMarkup", "")
            texts.append(text)
            ids.append(str(doc.get("articleId", idx)))
            metadatas.append({
                "articleId": doc.get("articleId"),
                "createdDate": doc.get("createdDate"),
                "articleType": doc.get("articleType", "")
            })

        log.info(f"Embedding {len(texts)} documents in batches...")

        # Generate embeddings
        vectors = self.embedder.embed_documents(texts)

        total = len(texts)
        for i in range(0, total, self.MAX_BATCH_SIZE):
            batch_texts = texts[i:i + self.MAX_BATCH_SIZE]
            batch_vectors = vectors[i:i + self.MAX_BATCH_SIZE]
            batch_ids = ids[i:i + self.MAX_BATCH_SIZE]
            batch_metas = metadatas[i:i + self.MAX_BATCH_SIZE]

            try:
                self.client.insert(
                    ids=batch_ids,
                    documents=batch_texts,
                    embeddings=batch_vectors,
                    metadatas=batch_metas
                )
                log.info(f"Stored batch {i // self.MAX_BATCH_SIZE + 1} of {ceil(total / self.MAX_BATCH_SIZE)}")
            except Exception as e:
                log.error(f"Failed to store batch {i}: {e}")

    def embed_query(self, query: str):
        return self.embedder.embed_query(query)
