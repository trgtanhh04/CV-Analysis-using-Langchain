import faiss
import numpy as np

class CandidateVectorDB:

    def __init__(self, dim):
        self.id_map = []
        self.index = faiss.IndexFlatL2(dim)

    def add_embedding(self, candidate):
        vectors = []
        for c in candidate:
            if c.embedding:
                vectors.append(c.embedding)
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
    
# class CandidateVectorDB:
    
#     def __init__(self, dim, db_path=None):
#         self.id_map = []
#         self.index = None
#         self.dim = dim 

#         if db_path and os.path.exists(os.path.join(db_path, "vector/index.faiss")) and os.path.exists(os.path.join(db_path, "vector/id_map.pkl")):
#             self.load_db(db_path)
#         else:
#             self.index = faiss.IndexFlatL2(dim)
#             if db_path:
#                 self.db_path = db_path
#             else:
#                 self.db_path = None


#     def add_embedding(self, candidates):
#         vectors = []
#         new_ids = []
#         for c in candidates:
#             if hasattr(c, 'embedding') and c.embedding is not None: 
#                 new_ids.append(c.id)
        
#         if vectors:
#             arr = np.array(vectors, dtype=np.float32)
#             if self.index is None: 
#                 self.index = faiss.IndexFlatL2(self.dim)
#             self.index.add(arr)
#             self.id_map.extend(new_ids)

#     def search(self, query_vec, k=5):
#         if self.index is None or self.index.ntotal == 0:
#             return [], [] 
        
#         arr = np.array([query_vec], dtype=np.float32)
#         distances, indices = self.index.search(arr, k)
        
#         results_ids = []
#         results_distances = []

#         for i in range(len(indices[0])):
#             idx = indices[0][i]
#             if idx != -1 and idx < len(self.id_map): 
#                 results_ids.append(self.id_map[idx])
#                 results_distances.append(float(distances[0][i]))
            
#         return results_ids, results_distances

#     def save_db(self, db_path):
#         """Saves the FAISS index and id_map to the specified path."""
#         if not os.path.exists(db_path):
#             os.makedirs(db_path)
        
#         if self.index:
#             faiss.write_index(self.index, os.path.join(db_path, "vector/index.faiss"))
#         with open(os.path.join(db_path, "vector/id_map.pkl"), "wb") as f:
#             pickle.dump(self.id_map, f)
#         self.db_path = db_path 
#         print(f"Database saved to {db_path}")

#     def load_db(self, db_path):
#         """Loads the FAISS index and id_map from the specified path."""
#         index_file = os.path.join(db_path, "vector/index.faiss")
#         id_map_file = os.path.join(db_path, "vector/id_map.pkl")

#         if not os.path.exists(index_file) or not os.path.exists(id_map_file):
#             print(f"Error: Database files not found in {db_path}")
#             # Initialize a new empty index if files are missing but path was given
#             self.index = faiss.IndexFlatL2(self.dim)
#             self.id_map = []
#             self.db_path = db_path
#             return

#         try:
#             self.index = faiss.read_index(index_file)
#             with open(id_map_file, "rb") as f:
#                 self.id_map = pickle.load(f)
#             self.db_path = db_path

#             if self.index and self.dim != self.index.d:
#                 print(f"Warning: Loaded index dimension ({self.index.d}) differs from provided dimension ({self.dim}). Using loaded dimension.")
#                 self.dim = self.index.d
#             print(f"Database loaded from {db_path}")
#         except Exception as e:
#             print(f"Error loading database from {db_path}: {e}")
#             self.index = faiss.IndexFlatL2(self.dim)
#             self.id_map = []
#             self.db_path = db_path


# # Example Usage (optional, for testing)
# if __name__ == '__main__':
#     # --- Test saving and loading ---
#     mock_dim = 10
#     mock_db_path = "./test_vector_db_data"

#     # Clean up previous test run
#     if os.path.exists(mock_db_path):
#         import shutil
#         shutil.rmtree(mock_db_path)

#     # 1. Create new DB and add data
#     print("\\n--- Test 1: Creating new DB ---")
#     db = CandidateVectorDB(dim=mock_dim, db_path=mock_db_path)
    
#     class MockCandidate:
#         def __init__(self, id, embedding):
#             self.id = id
#             self.embedding = embedding

#     candidates_data = [
#         MockCandidate("id1", np.random.rand(mock_dim).astype(np.float32)),
#         MockCandidate("id2", np.random.rand(mock_dim).astype(np.float32)),
#         MockCandidate("id3", np.random.rand(mock_dim).astype(np.float32))
#     ]
#     db.add_embedding(candidates_data)
#     print(f"ID Map after adding: {db.id_map}")
#     print(f"Index total: {db.index.ntotal if db.index else 0}")

#     # Save it
#     db.save_db(mock_db_path)

#     # 2. Load existing DB
#     print("\\n--- Test 2: Loading existing DB ---")
#     db_loaded = CandidateVectorDB(dim=mock_dim, db_path=mock_db_path) # dim is still needed for potential fallback
#     print(f"Loaded ID Map: {db_loaded.id_map}")
#     print(f"Loaded Index total: {db_loaded.index.ntotal if db_loaded.index else 0}")
#     assert len(db_loaded.id_map) == 3
#     assert db_loaded.index.ntotal == 3

#     # 3. Search
#     print("\\n--- Test 3: Searching ---")
#     query_vector = np.random.rand(mock_dim).astype(np.float32)
#     ids, dists = db_loaded.search(query_vector, k=2)
#     print(f"Search Results IDs: {ids}")
#     print(f"Search Results Distances: {dists}")
#     assert len(ids) <= 2 

#     # 4. Test loading with a non-existent path (should create new)
#     print("\\n--- Test 4: Loading non-existent DB path ---")
#     non_existent_path = "./non_existent_db"
#     if os.path.exists(non_existent_path):
#         import shutil
#         shutil.rmtree(non_existent_path)
#     db_new_path = CandidateVectorDB(dim=mock_dim, db_path=non_existent_path)
#     print(f"New DB ID Map: {db_new_path.id_map}")
#     print(f"New DB Index total: {db_new_path.index.ntotal if db_new_path.index else 0}")
#     assert len(db_new_path.id_map) == 0
#     assert (db_new_path.index is None or db_new_path.index.ntotal == 0) 

#     # 5. Test adding to a loaded DB and re-saving
#     print("\\n--- Test 5: Adding to loaded DB and re-saving ---")
#     db_loaded.add_embedding([MockCandidate("id4", np.random.rand(mock_dim).astype(np.float32))])
#     print(f"ID Map after adding to loaded: {db_loaded.id_map}")
#     print(f"Index total after adding to loaded: {db_loaded.index.ntotal}")
#     assert len(db_loaded.id_map) == 4
#     assert db_loaded.index.ntotal == 4
#     db_loaded.save_db(mock_db_path) 

#     # Verify re-save
#     db_reloaded = CandidateVectorDB(dim=mock_dim, db_path=mock_db_path)
#     assert len(db_reloaded.id_map) == 4
#     assert db_reloaded.index.ntotal == 4
#     print("All tests passed (basic checks).")

#     # Clean up test directory
#     if os.path.exists(mock_db_path):
#         import shutil
#         shutil.rmtree(mock_db_path)
#     if os.path.exists(non_existent_path):
#         import shutil
#         shutil.rmtree(non_existent_path)


