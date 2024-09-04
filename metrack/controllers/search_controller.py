import meilisearch
from frappe.model.document import Document
from meilisearch.index import Index
from typing import Optional
import frappe


class SearchController(Document):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.meilisearch_client = meilisearch.Client("http://meilisearch:7700")
    
    def set_meilisearch_dict(self):
        if self.melisearch_fields:
            self.melisearch_dict = {
                key: value for key, value in self.as_dict(no_nulls=True).items()
                if key in self.melisearch_fields
            }
    
    def create_index(self, index=None):
        if not index:
            index = self.doctype
        self.meilisearch_client.create_index(index)

    def get_index(self, index: str=None, create: bool=True) -> Optional[Index]:
        out = None
        if not index:
            index = self.doctype
        try:
            out = self.meilisearch_client.get_index(index)
        except meilisearch.errors.MeilisearchApiError as e:
            if create:
                self.create_index(index)
                out = self.meilisearch_client.get_index(index)
        finally:
            return out

    def delete_index(self, index: str=None):
        if not index:
            index = self.doctype
        self.meilisearch_client.delete_index(index)
    
    def add_documents(self, index: str=None, documents: list=[]):
        if not index:
            index = self.doctype
        if not documents:
            documents = [self.melisearch_dict or self.as_dict(no_nulls=True)]
        documents[0].update({"id": self.name})
        self.meilisearch_client.index(index).add_documents(documents)
    
    def delete_documents(self, index: str=None, documents: list=[]):
        if not index:
            index = self.doctype
        if not documents:
            documents.append(self.name)
        self.meilisearch_client.index(index).delete_documents(documents)
    
    def task_info(self, task):
        print(self.meilisearch_client.get_task(30))