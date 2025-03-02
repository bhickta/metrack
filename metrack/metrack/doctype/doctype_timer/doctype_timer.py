# Copyright (c) 2025, nishantbhickta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class DoctypeTimer(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		doc: DF.Link
		incremental: DF.Duration
		initial: DF.Duration
		is_enabled: DF.Check
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		target: DF.Float
	# end: auto-generated types
	pass

@frappe.whitelist()
def is_timer(doc):
    is_timer = frappe.db.exists("Doctype Timer", {"doc": doc, "is_enabled": 1})
    return True if is_timer else False