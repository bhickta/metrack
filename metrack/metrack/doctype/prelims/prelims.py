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
		fields = ['question', 'a', 'b', 'c', 'd', 'e', 'f', 'explanation']
		topics = [topic.strip().lower() for topic in self.topic.split(",")]  # Split and clean topics
		
		query_conditions = []
		for topic in topics:
			topic_conditions = [f"LOWER(`{field}`) LIKE %s" for field in fields]
			query_conditions.append(f"({' OR '.join(topic_conditions)})")  # Group conditions for each topic
		
		query = f"""
			SELECT mcq.name, mcq.answer
			FROM `tabMCQ` mcq
			WHERE {" OR ".join(query_conditions)}
		"""
		
		values = [f"%{topic}%" for topic in topics for _ in fields]

		data = frappe.db.sql(query, values, as_dict=1)

		if not hasattr(self, 'items'):
			self.items = []

		existing_questions = {item.get("question") for item in self.items}

		for d in data:
			if d.name not in existing_questions:
				self.append('items', {"question": d.name, "correct_answer": d.answer})
    
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
        "explanation": question.explanation,
        "correct_answer": question.answer
    }