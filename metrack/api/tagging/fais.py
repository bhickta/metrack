
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
        tags_with_origins = tagging_cache.tags

        text = " ".join(filter(None, [self.question, self.a, self.b, self.c, self.d, self.e, self.f, self.explanation]))
        ranked_tags = tag_text_with_faiss(text, tag_embeddings, faiss_index, model)

        self.ranked_tags = []
        for tag in ranked_tags:
            origin = tags_with_origins.get(tag[0])
            if origin:
                self.ranked_tags.append({"tag": tag, "meta": tags_with_origins[tag[0]]})

    except Exception as e:
        print(e)
        raise