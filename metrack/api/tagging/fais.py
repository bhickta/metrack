
import frappe
from .cache import TaggingCache
from metrack.api.tagging import tag_text_with_faiss

tagging_cache = TaggingCache()

@frappe.whitelist()
def set_tags(self):
    try:
        tagging_cache.initialize()
        model = tagging_cache.model
        tag_embeddings = tagging_cache.tag_embeddings
        faiss_index = tagging_cache.faiss_index
        text = " ".join(filter(None, [self.question, self.a, self.b, self.c, self.d, self.e, self.f, self.explanation]))
        ranked_tags = tag_text_with_faiss(text, tag_embeddings, faiss_index, model)
        self.tags = ranked_tags

    except Exception as e:
        frappe.log_error(f"Error in set_tags: {str(e)}", title="Tagging Error")
        raise