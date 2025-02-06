import frappe
import os
import pickle
from frappe.utils import get_site_path
from metrack.api.tagging import (
    build_embedding_model,
    build_tag_embeddings,
    build_faiss_index,
)


class TaggingCache:
    def __init__(self):
        self.model = None
        self.tag_embeddings = None
        self.faiss_index = None
        self.tags = None
        self.cache_dir = get_site_path("private", "tagging_cache")
        self.cache_file = os.path.join(self.cache_dir, "tagging_cache.pkl")
        self.model_file = os.path.join(self.cache_dir, "embedding_model.pkl")

    def initialize(self):
        # Check if cache files exist, if so, load them
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

        # Load precomputed cache if available
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "rb") as f:
                self.tag_embeddings, self.faiss_index = pickle.load(f)
            if os.path.exists(self.model_file):
                with open(self.model_file, "rb") as f:
                    self.model = pickle.load(f)
                return

        # If not cached, build everything
        self.model = build_embedding_model()  # Build the model only once
        self.tags = frappe.get_all("Syllabus Theme", fields=["theme"], pluck="theme")
        self.tag_embeddings = build_tag_embeddings(self.tags, self.model)  # Precompute embeddings
        self.faiss_index = build_faiss_index(self.tag_embeddings)  # Build FAISS index

        # Cache the results for future use
        with open(self.cache_file, "wb") as f:
            pickle.dump((self.tag_embeddings, self.faiss_index), f)
        with open(self.model_file, "wb") as f:
            pickle.dump(self.model, f)