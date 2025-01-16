# Copyright (c) 2025, nishantbhickta and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class SyllabusTheme(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		naming_series: DF.Literal["UT-.####."]
		section: DF.Link | None
		subject: DF.Link | None
		subtheme: DF.Link | None
		theme: DF.Link | None
		topic: DF.Link | None
	# end: auto-generated types
	pass
