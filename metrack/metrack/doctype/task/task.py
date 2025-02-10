# Copyright (c) 2025, nishantbhickta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Task(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from metrack.metrack.doctype.assignment.assignment import Assignment

		assignments: DF.Table[Assignment]
		description: DF.LongText | None
		is_disabled: DF.Check
		title: DF.Data
	# end: auto-generated types
	pass

def assigned_tasks(user):
    return frappe.db.sql(f"""
        SELECT
            a.parent
        FROM 
            `tabAssignment` AS a
        LEFT JOIN 
            `tabTask` AS t ON a.parent = t.name
        WHERE 
            a.parenttype = 'Task'
            AND a.user = '{user}'
            AND t.is_disabled = 0
    """)