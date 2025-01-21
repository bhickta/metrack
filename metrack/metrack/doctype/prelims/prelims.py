# Copyright (c) 2024, nishantbhickta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Prelims(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from metrack.metrack.doctype.prelims_items.prelims_items import PrelimsItems

		amended_from: DF.Link | None
		items: DF.Table[PrelimsItems]
		topic: DF.Data
	# end: auto-generated types
	pass

	def validate(self):
		self.get_mcq()
		self.check_items()

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
			print(query)
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