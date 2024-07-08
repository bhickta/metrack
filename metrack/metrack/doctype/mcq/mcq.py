# Copyright (c) 2024, nishantbhickta and contributors
# For license information, please see license.txt

import frappe
import frappe.desk
import frappe.desk.form
import frappe.desk.form.load
import frappe.desk.form.utils
import frappe.desk.utils
import frappe.model
from frappe.model.document import Document
import frappe.model.utils
import frappe.model.utils.user_settings
import frappe.utils
import ast

class MCQ(Document):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.set_user_settings()

	def validate(self):
		self.clean()

	def after_save(self):
		pass

	def clean(self):
		self.clean_question()
		self.clean_options()

	def clean_question(self):
		self.clean_options()

	def clean_options(self):
		options_fields = ['a', 'b', 'c', 'd', 'e', 'f']
		for field in options_fields:
			self.clean_prefix_options(field)

	def clean_prefix_options(self, field):
		value = self.get_value(field)
		options_startswith = ["a)", "b)", "c)", "d)", "e)", "f)", "(a)", "(b)", "(c)", "(d)", "(e)", "(f)"]
		for opt in options_startswith:
			if value.startswith(opt):
				value = value[len(opt):].strip()
		self.set(field, value)

	def convert_to_frappe_dict(self, d):
		if isinstance(d, dict):
			return frappe._dict({k: self.convert_to_frappe_dict(v) for k, v in d.items()})
		elif isinstance(d, list):
			return [self.convert_to_frappe_dict(i) for i in d]
		else:
			return d

	def navigate(self):
		self.navigate_records(1)

		
	def set_user_settings(self):
		doctype_user_settings = frappe.model.utils.user_settings.get_user_settings(self.doctype)
		self.user_settings = self.convert_to_frappe_dict(frappe.json.loads(doctype_user_settings))
		self.filters = self.user_settings.List.filters
		self.sort_field = self.user_settings.List.sort_by
		self.sort_order  = self.user_settings.List.sort_order

	def navigate_records(self, step):
		return frappe.desk.form.utils.get_next(self.doctype, self.name, step, self.filters, self.sort_order, self.sort_field)