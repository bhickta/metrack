# Copyright (c) 2024, nishantbhickta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from metrack.controllers.search_controller import SearchController


class SubjectiveQuestion(SearchController):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from metrack.metrack.doctype.subjective_question_topic.subjective_question_topic import SubjectiveQuestionTopic

		exam: DF.Link | None
		subjective_question_topic: DF.Table[SubjectiveQuestionTopic]
		title: DF.Text | None
		year: DF.Data | None
	# end: auto-generated types
	pass

	def validate(self):
		self.melisearch_dict = {}
		self.add_documents()