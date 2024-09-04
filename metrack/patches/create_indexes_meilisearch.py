import meilisearch

class MeiliSearchHandler:
    def __init__(self, base_url="http://meilisearch:7700"):
        self.client = meilisearch.Client(base_url)
        self.doctypes = self.get_doctype_lists()
        self.action_map = self.get_action_map()

    def execute(self, action="create_index"):
        """Executes the specified action for each doctype."""
        if action not in self.action_map:
            raise ValueError(f"Action {action} is not supported.")
        
        action_func = self.action_map[action]
        for doctype in self.doctypes:
            action_func(doctype)

    def create_index(self, doctype):
        """Creates an index for a given doctype."""
        self.client.create_index(doctype)

    def delete_index(self, doctype):
        """Deletes an index for a given doctype."""
        self.client.index(doctype).delete()

    def get_doctype_lists(self):
        """Returns the list of doctypes to operate on."""
        return ["MCQ", "Source"]

    def get_action_map(self):
        """Maps actions to corresponding functions."""
        return {
            "create_index": self.create_index,
            "delete_index": self.delete_index,
        }

meili_handler = MeiliSearchHandler()
# meili_handler.execute("create_index")
# meili_handler.execute("delete_index")