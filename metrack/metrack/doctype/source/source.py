# Copyright (c) 2024, nishantbhickta and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from metrack.controllers.search_controller import SearchController


class Source(SearchController):
	def validate(self):
		self.get_index()
		print(self.add_documents())