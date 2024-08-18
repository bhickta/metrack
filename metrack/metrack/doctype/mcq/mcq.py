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
from dataclasses import dataclass
from metrack.api.scraping.core.insight_ias import QuizScraper

class MCQ(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		a: DF.SmallText | None
		answer: DF.Literal["", "a", "b", "c", "d", "e", "f"]
		b: DF.SmallText | None
		c: DF.SmallText | None
		d: DF.SmallText | None
		e: DF.SmallText | None
		explanation: DF.Text | None
		f: DF.SmallText | None
		omr: DF.Literal["", "a", "b", "c", "d", "e", "f"]
		question: DF.SmallText
		question_status: DF.Link | None
		source: DF.Link
	# end: auto-generated types
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.set_user_settings()

	def validate(self):
		self.clean()
		self.check_omr()

	def check_omr(self):
		if self.omr == self.answer:
			self.workflow_state = 'Done'
		else:
			self.workflow_state = "Not Done"
		self.omr = None
		frappe.msgprint(
			msg=self.workflow_state,
			title=self.answer,
			indicator='green' if self.workflow_state == "Done" else "red",
			as_list=False,
			alert=True
		)

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

	@frappe.whitelist()
	def scrape_insight_ias_quiz(self):
		print('called')
		from_date = '2024-08-01'
		to_date = '2024-08-10'
		urls = generate_urls(from_date, to_date)
		print(urls)
		scraper = QuizScraper()
		quizzes = scraper.scrape_quiz(urls)
		for quiz in quizzes:
			if not quiz:
				continue
			for q in quiz:
				if not frappe.db.exists("Source", q.source):
					frappe.get_doc({
						"doctype": "Source",
						"title": q.source
					}).insert()
				frappe.get_doc({
					"doctype": "MCQ",
					"question": q.question,
					"answer": q.answer,
					"source": q.source,
					"explanation": q.explanation,
					"a": q.a,
					"b": q.b,
					"c": q.c,
					"d": q.d,
					"e": q.e,
					"f": q.f,
					'reference': '<html><a href="{0}">Read More</a></html>'.format(q.url),
				}).insert()


from datetime import datetime, timedelta

def generate_urls(from_date_str, to_date_str):
    urls = []
    
    # Parse the input date strings
    from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
    to_date = datetime.strptime(to_date_str, '%Y-%m-%d')
    
    current_date = from_date
    
    while current_date <= to_date:
        year = current_date.year
        month = current_date.strftime('%m')
        day = current_date.strftime('%d')
        
        # Construct the URL
        url = f'https://www.insightsonindia.com/{year}/{month}/{day}/upsc-editorials-quiz-{day}-{month}-{year}/'
        urls.append(url)
        
        # Move to the next day
        current_date += timedelta(days=1)
    
    return urls