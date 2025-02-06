
import frappe
from .cache import TaggingCache
from metrack.api.tagging import tag_text_with_faiss

tagging_cache = TaggingCache()

@frappe.whitelist()
def set_tags(self):
    try:
        # Initialize the cache (model, embeddings, faiss index) only once
        tagging_cache.initialize()

        # Use the cached model, embeddings, and faiss index
        model = tagging_cache.model
        tag_embeddings = tagging_cache.tag_embeddings
        faiss_index = tagging_cache.faiss_index

        # Get the question text and get ranked tags
        text = self.question + " " + self.explanation
        ranked_tags = tag_text_with_faiss(text, tag_embeddings, faiss_index, model)

        # Optionally, you could save ranked_tags to a database field or return them for later use
        self.tags = ranked_tags

    except Exception as e:
        frappe.log_error(f"Error in set_tags: {str(e)}", title="Tagging Error")
        raise