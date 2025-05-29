# agents/retriever_agent.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle
import os

class RetrieverAgent:
    def __init__(self, index_path="retriever_index"):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index_path = index_path
        self.index = faiss.IndexFlatL2(384)  # Embedding dimension for MiniLM
        self.corpus = []
        self.embeddings = []

        if os.path.exists(f"{index_path}.pkl"):
            self.load_index()

    def build_index(self, documents):
        self.corpus = documents
        self.embeddings = self.model.encode(documents, convert_to_numpy=True)
        self.index.add(np.array(self.embeddings))
        self.save_index()

    def save_index(self):
        with open(f"{self.index_path}.pkl", "wb") as f:
            pickle.dump((self.corpus, self.embeddings), f)

    def load_index(self):
        with open(f"{self.index_path}.pkl", "rb") as f:
            self.corpus, self.embeddings = pickle.load(f)
            self.index.add(np.array(self.embeddings))

    def retrieve(self, query, top_k=3):
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        D, I = self.index.search(query_embedding, top_k)
        results = [self.corpus[i] for i in I[0]]
        return results

if __name__ == "__main__":
    agent = RetrieverAgent()
    if not agent.corpus:
        docs = [
            "TSMC reported a 4% earnings beat this quarter.",
            "Samsung missed earnings expectations by 2%.",
            "Asian tech sentiment is neutral today.",
            "Rising yields in Asia put downward pressure on growth stocks."
        ]
        agent.build_index(docs)

    results = agent.retrieve("Any earnings surprise today?")
    print("Top Results:")
    for res in results:
        print("-", res)
