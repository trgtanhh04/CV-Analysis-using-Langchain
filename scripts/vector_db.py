import faiss
import numpy as np
import json

class CandidateFaissIndex:

    def __init__(self, dim):
        self.id_map = []
        self.index = faiss.IndexFlatL2(dim)

    def add_embedding(self, candidate):
        vectors = []
        for c in candidate:
            if c.embedding:
                vector = json.loads(c.embedding)
                vectors.append(vector)
                self.id_map.append(c.id)
        if vectors:
            arr = np.array(vectors, dtype=np.float32)
            self.index.add(arr)

    def search(self, query_vec, k=5):
        arr = np.array([query_vec], dtype=np.float32)
        D, I = self.index.search(arr, k)
        results = []
        for i in I[0]:
            results.append(self.id_map[i])
        return results
