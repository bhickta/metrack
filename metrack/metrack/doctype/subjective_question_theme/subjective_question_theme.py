# Copyright (c) 2024, nishantbhickta and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class SubjectiveQuestionTheme(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		section: DF.Link | None
		subject: DF.Link | None
		subtheme: DF.Link | None
		syllabus_theme: DF.Link
		theme: DF.Link | None
		topic: DF.Link | None
	# end: auto-generated types
	pass
