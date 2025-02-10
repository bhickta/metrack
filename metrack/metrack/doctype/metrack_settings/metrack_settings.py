# Copyright (c) 2025, nishantbhickta and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class MetrackSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from metrack.metrack.doctype.assignment.assignment import Assignment
		from metrack.metrack.doctype.doctype_timer.doctype_timer import DoctypeTimer

		auto_reporting: DF.Table[Assignment]
		per_mcq_interval: DF.Duration | None
		per_mcq_interval_increment: DF.Duration | None
		timers: DF.Table[DoctypeTimer]
	# end: auto-generated types
	pass
