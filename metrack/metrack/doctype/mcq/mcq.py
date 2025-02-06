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

import frappe.data
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
		source: DF.SmallText | None
		subject: DF.Data | None
		urls: DF.Table[Urls]
	# end: auto-generated types
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	
	def validate(self):
		self.extract_urls()
		self.check_answer()
	
	def check_answer(self):
		if frappe.flags.in_import:
			self.result = None
		elif self.answer == self.selected_answer:
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
					if url not in seen_urls and url not in [u.url for u in self.urls]:
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

	def onload(self):
		self.set_onload("done_today", frappe.db.count("MCQ", filters={"question_status": "Done", "modified": (">=", frappe.utils.today())}))

	def on_trash(self):
		pass

	@frappe.whitelist()
	def set_tags(self):
		development = frappe.local.conf.developer_mode or frappe.local.dev_server
		if not development:
			return
		from metrack.api.tagging.faiss import set_tags as _set_tags
		_set_tags(self)
		for tag in self.tags:
			tag = frappe.db.escape(tag[0])
			tag = tag.replace(",", "")
			self.add_tag(tag)


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