# Copyright (c) 2025, nishantbhickta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from metrack.metrack.doctype.task.task import assigned_tasks


class DailySelfReporting(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from metrack.metrack.doctype.daily_self_reporting_item.daily_self_reporting_item import DailySelfReportingItem

		amended_from: DF.Link | None
		items: DF.Table[DailySelfReportingItem]
		naming_series: DF.Literal["DSR-.####."]
		posting_date: DF.Date
		user: DF.Link
	# end: auto-generated types
	pass

	def validate(self):
		if not self.user or self.user == "User":
			self.user = frappe.session.user
		if not self.posting_date:
			self.posting_date = frappe.utils.now()

	def before_insert(self):
		if not self.items:
			self.fetch_default_values()

	@frappe.whitelist()
	def fetch_default_values(self):
		for task in assigned_tasks(self.user):
			self.append("items", {"task": task[0], "status": "Success", "posting_date": self.posting_date})
