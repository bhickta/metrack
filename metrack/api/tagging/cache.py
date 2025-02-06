import frappe
import os
import pickle
from frappe.utils import get_site_path
from metrack.api.tagging import (
    build_embedding_model,
    build_tag_embeddings,
    build_faiss_index,
)


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
        self.tags = {}
        self.cache_dir = get_site_path("private", "tagging_cache")
        self.cache_file = os.path.join(self.cache_dir, "tagging_cache.pkl")
        self.model_file = os.path.join(self.cache_dir, "embedding_model.pkl")

    def initialize(self):
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

        if os.path.exists(self.cache_file):
            with open(self.cache_file, "rb") as f:
                self.tag_embeddings, self.faiss_index, self.tags = pickle.load(f)
            if os.path.exists(self.model_file):
                with open(self.model_file, "rb") as f:
                    self.model = pickle.load(f)
                return

        self.model = build_embedding_model()
        self.tags = {}
        syllabus = frappe.get_all("Syllabus Theme", fields=["name"], pluck="name")
        for s_name in syllabus:
            s = frappe.get_doc("Syllabus Theme", s_name)
            for f in ["subject", "topic", "section", "theme", "subtheme"]:
                tag = s.get(f, None)
                if tag:
                    if tag not in self.tags:
                        self.tags[tag] = {"origin_name": s_name, "origin_field": f}
        
        self.tag_embeddings = build_tag_embeddings(list(self.tags.keys()), self.model)
        self.faiss_index = build_faiss_index(self.tag_embeddings)

        with open(self.cache_file, "wb") as f:
            pickle.dump((self.tag_embeddings, self.faiss_index, self.tags), f)
        with open(self.model_file, "wb") as f:
            pickle.dump(self.model, f)