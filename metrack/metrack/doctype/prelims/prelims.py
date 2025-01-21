# Copyright (c) 2024, nishantbhickta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re


class Prelims(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from metrack.metrack.doctype.prelims_items.prelims_items import PrelimsItems
		from metrack.metrack.doctype.urls.urls import Urls

		amended_from: DF.Link | None
		items: DF.Table[PrelimsItems]
		paste_urls: DF.Text | None
		topic: DF.Data
		urls: DF.Table[Urls]
	# end: auto-generated types
	pass

	def validate(self):
		self.get_mcq()
		self.check_items()
		self.extract_urls()
	
	def extract_urls(self):
		extracted_urls = []
		seen_urls = set()  # To track unique URLs
		if self.paste_urls:
			lines = self.paste_urls.strip().split("\n")
			for line in lines:
				match = re.match(r"\[(.*?)\]\((.*?)\)", line.strip())
				if match:
					title, url = match.groups()
					if url not in seen_urls and url not in [url.url for url in self.urls]:  # Check if the URL is unique in both seen_urls and self.urls
						extracted_urls.append({"title": title, "url": url})
						seen_urls.add(url)  # Mark URL as seen
		if extracted_urls:
			for url in extracted_urls:
				self.append("urls", url)

	def get_mcq(self):
		def get_topics():
			return [topic.strip().lower() for topic in self.topic.split(",")]

		def build_query_conditions(topics, fields):
			query_conditions = []
			values = {}
			value_index = 0

			for topic in topics:
				topic_conditions = []
				for field in fields:
					patterns = [
						f"{topic} %",   # Starts with
						f"% {topic}",   # Ends with
						f"{topic}"     # Exact match
					]
					field_conditions = []
					for pattern in patterns:
						placeholder = f"{field}_{value_index}"
						field_conditions.append(f"LOWER(`{field}`) LIKE %({placeholder})s")
						values[placeholder] = pattern
						value_index += 1
					topic_conditions.append("(" + " OR ".join(field_conditions) + ")")
				query_conditions.append("(" + " OR ".join(topic_conditions) + ")")

			return " OR ".join(query_conditions), values

		def fetch_mcq_data(query_conditions, values):
			query = f"""
				SELECT mcq.name, mcq.answer
				FROM `tabMCQ` mcq
				WHERE {query_conditions}
			"""
			return frappe.db.sql(query, values, as_dict=1)

		def append_new_mcqs(data):
			if not hasattr(self, 'items'):
				self.items = []

			existing_questions = {item.get("question") for item in self.items}

			for d in data:
				if d["name"] not in existing_questions:
					self.append('items', {"question": d["name"], "correct_answer": d["answer"]})

		# Main function logic
		fields = ['question', 'a', 'b', 'c', 'd', 'e', 'f', 'explanation']
		topics = get_topics()
		query_conditions, values = build_query_conditions(topics, fields)
		data = fetch_mcq_data(query_conditions, values)
		append_new_mcqs(data)
    
	def check_items(self):
		for item in self.items:
			if not item.answer:
				continue
			item.check = "Right" if item.answer == item.correct_answer else "Wrong"


@frappe.whitelist()
def get_question(question_name):
    question = frappe.get_doc("MCQ", question_name)
    return {
        "name": question.name,
        "question": question.question,
        "subject": question.subject,
        "a": question.a,
        "b": question.b,
        "c": question.c,
        "d": question.d,
        "e": question.e,
        "f": question.f,
        "explanation": question.explanation,
        "correct_answer": question.answer
    }