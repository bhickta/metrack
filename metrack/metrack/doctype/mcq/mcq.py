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
import re
from dataclasses import dataclass
# from metrack.api.scraping.core.insight_ias import QuizScraper

class MCQ(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from metrack.metrack.doctype.urls.urls import Urls

		a: DF.SmallText | None
		answer: DF.Literal["", "a", "b", "c", "d", "e", "f"]
		b: DF.SmallText | None
		c: DF.SmallText | None
		d: DF.SmallText | None
		e: DF.SmallText | None
		edit: DF.Check
		explanation: DF.Text | None
		f: DF.SmallText | None
		input_urls: DF.SmallText | None
		metadata: DF.Text | None
		naming_series: DF.Literal["MCQ-.#."]
		question: DF.SmallText | None
		question_status: DF.Link | None
		result: DF.Literal["Skipped", "Right", "Wrong"]
		selected_answer: DF.Literal["", "a", "b", "c", "d", "e", "f"]
		source: DF.Data | None
		subject: DF.Data | None
		urls: DF.Table[Urls]
	# end: auto-generated types
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.post_init(self)
	
	def validate(self):
		self.extract_urls()
		self.check_answer()
	
	def check_answer(self):
		if self.answer == self.selected_answer:
			self.result = "Right"
		elif self.selected_answer and self.selected_answer != self.answer:
			self.result = "Wrong"
		else:
			self.result = "Skipped"

	def extract_urls(self):
		extracted_urls = []
		seen_urls = set()  # To track unique URLs
		if self.input_urls:
			lines = self.input_urls.strip().split("\n")
			for line in lines:
				match = re.match(r"\[(.*?)\]\((.*?)\)", line.strip())
				if match:
					title, url = match.groups()
					# Check if the URL is unique in both seen_urls and self.urls
					if url not in seen_urls and url not in [u["url"] for u in self.urls]:
						extracted_urls.append({"title": title, "url": url})
						seen_urls.add(url)  # Mark URL as seen
		if extracted_urls:
			for url in extracted_urls:
				# Skip URLs containing "metrack" or "localhost"
				if "metrack" in url["url"] or "localhost" in url["url"]:
					continue
				self.append("urls", url)
		# Clear input_urls after processing
		self.input_urls = None
		self.question_status = "Done"


	def post_init(self, *args, **kwargs):
		self.set_user_settings()
  
	def onload(self):
		self.set_onload("done_today", frappe.db.count("MCQ", filters={"question_status": "Done", "modified": (">=", frappe.utils.today())}))
  
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

	def clean(self):
		self.clean_question()
		self.clean_options()

	def on_trash(self):
		pass

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
		return
		doctype_user_settings = frappe.model.utils.user_settings.get_user_settings(self.doctype)
		self.user_settings = self.convert_to_frappe_dict(frappe.json.loads(doctype_user_settings))
		self.filters = self.user_settings.List.filters
		self.sort_field = self.user_settings.List.sort_by
		self.sort_order  = self.user_settings.List.sort_order

	def navigate_records(self, step):
		return frappe.desk.form.utils.get_next(self.doctype, self.name, step, self.filters, self.sort_order, self.sort_field)

	@frappe.whitelist()
	def scrape_insight_ias_quiz(self):
		return
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